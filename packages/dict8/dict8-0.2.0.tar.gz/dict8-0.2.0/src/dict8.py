# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <https://unlicense.org>
import dataclasses as dc
import functools
import types
import typing as t


@functools.partial(lambda x: x())
class missing:
    def __bool__(self):
        return False

    def __repr__(self):
        return f"{__name__}.missing"


Path = t.Tuple[str, ...]


class UnMappable(Exception):
    ...


class Mapper(dict):
    def __init__(self, kv: t.Iterable[t.Tuple[t.Hashable, t.Any]], merger: "Merger"):
        self.merger = merger
        super().__init__(kv)

    def create(self, key_values: t.Iterator):
        return dict(key_values)

    @classmethod
    def test(cls, value: t.Any) -> bool:
        return isinstance(value, t.Mapping)


class MutableMapper(Mapper):
    @classmethod
    def test(cls, value: t.Any) -> bool:
        return (
            issubclass(value, t.MutableMapping)
            if isinstance(value, type)
            else isinstance(value, t.MutableMapping)
        )


MapperType = t.Type[Mapper]


@dc.dataclass
class Merger:
    func: t.Callable
    mapper: t.List[MapperType] = dc.field(default_factory=list)

    def add(self, *mappers: t.Type[Mapper]):
        self.mapper.extend(mappers)

    def test(self, value: t.Any) -> t.Optional[MapperType]:
        return next(
            (
                mapper
                for mapper in (*reversed(self.mapper), MutableMapper, Mapper)
                if mapper.test(value)
            ),
            None,
        )

    def map(self, value: t.Any) -> Mapper:
        if mapper := self.test(value):
            return mapper(value, self)
        else:
            raise UnMappable(value)

    def __call__(self, a: t.Any, b: t.Any, path: Path = (), /, **kv: t.Any) -> t.Any:
        a, b = self.map(a), self.map(b)

        a_keys, b_keys = set(a), set(b)
        old, common, new = a_keys - b_keys, a_keys & b_keys, b_keys - a_keys

        key_values = (
            (k, v)
            for values in (
                ((k, self.func(a[k], missing, path + (k,), **kv)) for k in old),
                ((k, self.func(a[k], b[k], path + (k,), **kv)) for k in common),
                ((k, self.func(missing, b[k], path + (k,), **kv)) for k in new),
            )
            for k, v in values
            if v is not missing
        )
        merged = a.create(key_values)
        return merged


@t.overload
def ion(*mapper: MapperType) -> t.Type[Merger]:
    ...  # pragma: nocover


@t.overload
def ion(func: t.Callable) -> Merger:  # noqa: F811
    ...  # pragma: nocover


def ion(  # noqa: F811
    func: t.Union[MapperType, t.Callable], *mapper: MapperType
) -> t.Union[Merger, t.Callable]:
    if isinstance(func, type) and issubclass(func, Mapper):
        mapper = (func,) + mapper

        def wrapper(func: t.Callable) -> Merger:
            merger = create_merger(func)
            merger.add(*mapper)
            return merger

        return wrapper
    return create_merger(func)


def create_merger(func) -> Merger:
    """Create a new Merger subclass, to have a proper doc string and annotations."""
    f = Merger.__call__
    g = types.FunctionType(
        f.__code__,
        f.__globals__,
        name=f.__name__,
        argdefs=f.__defaults__,
        closure=f.__closure__,
    )
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    g.__doc__ = func.__doc__
    g.__annotations__ = func.__annotations__

    NewMerger = dc.make_dataclass(
        func.__name__,
        [(f.name, f.type, f) for f in dc.fields(Merger)],
        bases=(Merger,),
        namespace={"__call__": g},
    )
    return NewMerger(func)


class DataclassMapper(Mapper):
    get_fields: t.Callable = functools.partial(dc.fields)

    def __init__(self, value: t.Any, merger: Merger):
        self.is_class = isinstance(value, type)
        self.fields: t.Dict[str, t.Any] = {f.name: f for f in self.get_fields(value)}

        if self.is_class:
            self.cls = value
            super().__init__(
                (
                    (name, f.type if merger.test(f.type) else self.field_default(f))
                    for name, f in self.fields.items()
                ),
                merger,
            )
        else:
            self.cls = type(value)
            super().__init__(
                ((name, getattr(value, name)) for name in self.fields), merger
            )

    def create(self, key_values: t.Iterator) -> t.Any:
        return self.cls(**dict((k, v) for k, v in key_values if k in self.fields))

    @classmethod
    def test(cls, value) -> bool:
        return dc.is_dataclass(value)

    @classmethod
    def field_default(cls, f) -> t.Any:
        return (
            f.default_factory()
            if f.default_factory is not dc.MISSING
            else f.default
            if f.default is not dc.MISSING
            else missing
        )


@ion(DataclassMapper)
def merge(
    a: t.Any,
    b: t.Any,
    path: Path = (),
    /,
    override: t.Optional[t.Callable] = None,
    nothing_new: bool = False,
    remove_old: bool = False,
    keep_type: bool = True,
    **kv: t.Any,
) -> t.Any:
    """Merge two mappable objects into one.

    :param a: object a
    :param b: object b
    :param path: the path of keys
    :param override: a function to override b
    :param nothing_new: skip new keys if they ar not in a
    :param remove_old: skip old keys if they are not in b
    :param keep_type: b must have similar type like a
    """
    try:
        return merge(
            a,
            b,
            path,
            override=override,
            nothing_new=nothing_new,
            remove_old=remove_old,
            keep_type=keep_type,
            **kv,
        )
    except UnMappable:
        if callable(override):
            b = override(a, b, path, **kv)
        return (
            b
            if (a is missing and not nothing_new)
            or (b is missing and remove_old)
            or (
                b is not missing
                and not keep_type
                or issubclass(
                    isinstance(b, type) and b or type(b),
                    isinstance(a, type) and a or type(a),
                )
            )
            else a
        )


try:
    import attr as a

    class AttrMapper(DataclassMapper):
        def get_fields(self, value: t.Any) -> t.Tuple[a.Attribute, ...]:
            return a.fields(value if self.is_class else type(value))

        def create(self, key_values: t.Iterator) -> t.Any:
            return self.cls(**dict((k, v) for k, v in key_values if k in self.fields))

        @classmethod
        def test(cls, value) -> bool:
            return a.has(value)

        @classmethod
        def field_default(cls, f) -> t.Any:
            return (
                f.default()
                if isinstance(f.default, a.Factory)
                else f.default
                if f.default is not a.NOTHING
                else missing
            )

    merge.add(AttrMapper)
except ImportError:  # pragma: nocover
    ...

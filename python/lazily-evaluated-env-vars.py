import numbers
import os
from collections.abc import Callable, Iterable, MutableSequence, Sequence
from dataclasses import KW_ONLY, dataclass
from functools import cached_property
from math import ceil, floor, trunc
from typing import Any, ClassVar, Never, Self, TypeVar, cast, overload, override

type Missing = object
MISSING: Missing = object()

T = TypeVar("T")

# with contextlib.suppress(Exception):
#     _ = load_dotenv()


@dataclass
class Setting(Sequence[str]):
    """Lazily evaluated class representing an environment variable.

    Args:
        name: The name of the environment variable
        default: The default value of the environment variable

    Attributes:
        value: Eagerly evaluate the value of the environment variable
    """

    name: str
    _ = KW_ONLY
    default: str | Missing = MISSING

    str_methods: ClassVar[dict[str, Callable[..., str | bytes]]] = {
        name: method
        for name, method in str.__dict__.items()
        if not name.startswith("__")
        and not name.endswith("__")
        and not isinstance(method, staticmethod)
    }

    def __post_init__(self) -> None:
        if isinstance(self.default, str) or self.default is MISSING:
            return
        msg = (
            "Setting's `default` argument must be a string if provided, not "
            f"{type(self.default).__name__}"
        )
        raise TypeError(msg)

    def __get__(self, obj: object, objtype: type | None = None) -> str:
        """Evaluate the value of the environment variable when accessed.

        Returns:
            The value of the environment variable
        """
        return self.value

    @cached_property
    def value(self) -> str:
        """Evaluate the value of the environment variable.

        Returns:
            The value of the environment variable
        """
        if self.default is MISSING:
            return os.environ[self.name]
        return cast("str", os.environ.get(self.name, self.default))

    def __getattr__(self, name: str) -> Callable[..., str | bytes] | Any:  # noqa: ANN401
        """Add builtin string methods to the Setting class by accessing a string method.

        Args:
            name: The name of the string method

        Returns:
            The string method
        """
        if name in type(self).str_methods:
            return lambda *args, **kwargs: cast(
                "str | bytes", str.__dict__[name](self.value, *args, **kwargs)
            )
        return super().__getattribute__(name)

    @override
    def __len__(self) -> int:
        return len(self.value)

    @override
    def __getitem__(self, index: int | slice) -> str:
        return self.value[index]


@dataclass
class FloatSetting(numbers.Real):
    """Lazily evaluated class representing a float environment variable.

    Args:
        name: The name of the environment variable
        default: The default value of the environment variable

    Attributes:
        value: Eagerly evaluate the value of the environment variable
    """

    name: str
    _ = KW_ONLY
    default: str | Missing = MISSING

    def __post_init__(self) -> None:
        if isinstance(self.default, str) or self.default is MISSING:
            return
        msg = (
            "Setting's `default` argument must be a string if provided, not "
            f"{type(self.default).__name__}"
        )
        raise TypeError(msg)

    def __get__(self, obj: object, objtype: type | None = None) -> float:
        """Evaluate the value of the environment variable when accessed.

        Returns:
            The value of the environment variable
        """
        return self.value

    @cached_property
    def value(self) -> float:
        """Evaluate the value of the environment variable.

        Returns:
            The value of the environment variable
        """
        if self.default is MISSING:
            value = os.environ[self.name]
        value = cast("str", os.environ.get(self.name, self.default))

        try:
            return float(value)
        except ValueError as err:
            msg = f"Environment variable '{self.name}' with value '{value}' cannot be converted to a float"
            raise ValueError(msg) from err

    @override
    def __abs__(self) -> float:
        return abs(self.value)

    @override
    def __add__(self, other: object) -> float | complex:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value + other.value
        if isinstance(other, complex | float | int):
            return self.value + other
        return NotImplemented

    @override
    def __ceil__(self) -> int:
        return ceil(self.value)

    @override
    def __float__(self) -> float:
        return self.value

    @override
    def __floor__(self) -> int:
        return floor(self.value)

    @override
    def __floordiv__(self, other: "float | FloatSetting | IntSetting") -> float:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value // other.value
        return self.value // other

    @override
    def __le__(self, other: "float | FloatSetting | IntSetting") -> bool:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value <= other.value
        return self.value <= other

    @override
    def __lt__(self, other: "float | FloatSetting | IntSetting") -> bool:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value < other.value
        return self.value < other

    @override
    def __mod__(self, other: "float | FloatSetting | IntSetting") -> float:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value % other.value
        return self.value % other

    @override
    def __mul__(self, other: "complex | FloatSetting | IntSetting") -> complex:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value * other.value
        return self.value * other

    @override
    def __neg__(self) -> float:
        return -self.value

    @override
    def __pos__(self) -> float:
        return self.value

    @override
    def __pow__(self, other: "float | FloatSetting | IntSetting") -> float:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value**other.value
        return self.value**other

    @overload
    def __round__(self, ndigits: None) -> int: ...

    @overload
    def __round__(self, ndigits: int) -> float: ...

    @override
    def __round__(self, ndigits: int | None = None) -> float | int:
        return round(self.value, ndigits)

    @override
    def __truediv__(self, other: "complex | FloatSetting | IntSetting") -> complex:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value / other.value
        return self.value / other

    @override
    def __trunc__(self) -> int:
        return trunc(self.value)

    __radd__ = __add__
    __rmul__ = __mul__

    @override
    def __rfloordiv__(self, other: "float | FloatSetting | IntSetting") -> float:
        if isinstance(other, FloatSetting | IntSetting):
            return other.value // self.value
        return other // self.value

    @override
    def __rmod__(self, other: "float | FloatSetting | IntSetting") -> float:
        if isinstance(other, FloatSetting | IntSetting):
            return other.value % self.value
        return other % self.value

    @override
    def __rpow__(self, other: "complex | FloatSetting | IntSetting") -> complex:
        if isinstance(other, FloatSetting | IntSetting):
            return other.value**self.value
        return other**self.value

    @override
    def __rtruediv__(self, other: "complex | FloatSetting | IntSetting") -> complex:
        if isinstance(other, FloatSetting | IntSetting):
            return other.value / self.value
        return other / self.value


@dataclass
class IntSetting(numbers.Real):
    """Lazily evaluated class representing a integer environment variable.

    Args:
        name: The name of the environment variable
        default: The default value of the environment variable

    Attributes:
        value: Eagerly evaluate the value of the environment variable
    """

    name: str
    _ = KW_ONLY
    default: str | Missing = MISSING

    def __post_init__(self) -> None:
        if isinstance(self.default, str) or self.default is MISSING:
            return
        msg = (
            "Setting's `default` argument must be a string if provided, not "
            f"{type(self.default).__name__}"
        )
        raise TypeError(msg)

    def __get__(self, obj: object, objtype: type | None = None) -> int:
        """Evaluate the value of the environment variable when accessed.

        Returns:
            The value of the environment variable
        """
        return self.value

    @cached_property
    def value(self) -> int:
        """Evaluate the value of the environment variable.

        Returns:
            The value of the environment variable
        """
        if self.default is MISSING:
            value = os.environ[self.name]
        value = cast("str", os.environ.get(self.name, self.default))

        try:
            return int(value)
        except ValueError as err:
            msg = f"Environment variable '{self.name}' with value '{value}' cannot be converted to an int"
            raise ValueError(msg) from err

    @override
    def __abs__(self) -> int:
        return abs(self.value)

    @override
    def __add__(self, other: object) -> complex:
        if isinstance(other, IntSetting | FloatSetting):
            return self.value + other.value
        if isinstance(other, complex | float | int):
            return self.value + other
        return NotImplemented

    @override
    def __ceil__(self) -> int:
        return ceil(self.value)

    @override
    def __float__(self) -> float:
        return self.value

    @override
    def __floor__(self) -> int:
        return floor(self.value)

    @override
    def __floordiv__(self, other: "float | FloatSetting | IntSetting") -> float:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value // other.value
        return self.value // other

    @override
    def __le__(self, other: "float | FloatSetting | IntSetting") -> bool:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value <= other.value
        return self.value <= other

    @override
    def __lt__(self, other: "float | FloatSetting | IntSetting") -> bool:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value < other.value
        return self.value < other

    @override
    def __mod__(self, other: "float | FloatSetting | IntSetting") -> float:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value % other.value
        return self.value % other

    @override
    def __mul__(self, other: "complex | FloatSetting | IntSetting") -> complex:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value * other.value
        return self.value * other

    @override
    def __neg__(self) -> int:
        return -self.value

    @override
    def __pos__(self) -> int:
        return self.value

    @override
    def __pow__(self, other: "float | FloatSetting | IntSetting") -> float:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value**other.value
        return self.value**other

    @overload
    def __round__(self, ndigits: None) -> int: ...

    @overload
    def __round__(self, ndigits: int) -> float: ...

    @override
    def __round__(self, ndigits: int | None = None) -> int:
        return round(self.value, ndigits)

    @override
    def __truediv__(self, other: "complex | FloatSetting | IntSetting") -> complex:
        if isinstance(other, FloatSetting | IntSetting):
            return self.value / other.value
        return self.value / other

    @override
    def __trunc__(self) -> int:
        return trunc(self.value)

    __radd__ = __add__
    __rmul__ = __mul__

    @override
    def __rfloordiv__(self, other: "float | FloatSetting | IntSetting") -> float:
        if isinstance(other, FloatSetting | IntSetting):
            return other.value // self.value
        return other // self.value

    @override
    def __rmod__(self, other: "float | FloatSetting | IntSetting") -> float:
        if isinstance(other, FloatSetting | IntSetting):
            return other.value % self.value
        return other % self.value

    @override
    def __rpow__(self, other: "complex | FloatSetting | IntSetting") -> complex:
        if isinstance(other, FloatSetting | IntSetting):
            return other.value**self.value
        return other**self.value

    @override
    def __rtruediv__(self, other: "complex | FloatSetting | IntSetting") -> complex:
        if isinstance(other, FloatSetting | IntSetting):
            return other.value / self.value
        return other / self.value


@dataclass
class ListSetting[T](MutableSequence[T]):
    """Lazily evaluated class representing a list environment variable.

    This class is used when your environment variable represents a list type value.

    It will parse the environment variable by splitting the string, stripping each
    element of the resulting list, the optionally calling a function on each of the
    values of the list.

    Args:
        name: The name of the environment variable
        item_callable: Callable to apply to each item of the list
        sep: Separator value used to split the environment variable string
        max_split: The maximum number of splits to the environment variable string
        default: The default value of the environment variable string (not a list)

    Attributes:
        value: Eagerly evaluate the value of the environment variable
    """

    name: str
    _ = KW_ONLY
    item_callable: Callable[[str], T] | None = None
    sep: str = " "
    max_split: int = -1
    default: str | Missing = MISSING

    list_methods: ClassVar[dict[str, Callable[..., str | bytes]]] = {
        name: method
        for name, method in list.__dict__.items()
        if not name.startswith("__")
        and not name.endswith("__")
        and not isinstance(method, staticmethod)
    }

    def __post_init__(self) -> None:
        if isinstance(self.default, str) or self.default is MISSING:
            return
        msg = (
            "Setting's `default` argument must be a string if provided, not "
            f"{type(self.default).__name__}"
        )
        raise TypeError(msg)

    def __get__(
        self, obj: object, objtype: type | None = None
    ) -> MutableSequence[str | T] | MutableSequence[str]:
        """Evaluate the environment variable and parse it into a list when accessed.

        Returns:
            The value of the environment variable as a list
        """
        return self.value

    @cached_property
    def value(self) -> MutableSequence[str | T] | MutableSequence[str]:
        """Evaluate the environment variable and parse it into a list when accessed.

        Returns:
            The value of the environment variable as a list
        """
        if self.default is MISSING:
            unparsed = os.environ[self.name]
        else:
            unparsed = cast("str", os.environ.get(self.name, self.default))

        list_ver = [s.strip() for s in unparsed.split(self.sep, self.max_split)]
        if self.item_callable is None:
            return list_ver
        return [self.item_callable(v) for v in list_ver]

    def __getattr__(self, name: str) -> Callable[..., list[T]] | Any:  # noqa: ANN401
        """Add builtin list methods to the ListSetting class by accessing a list method.

        Args:
            name: The name of the list method

        Returns:
            The list method
        """
        if name in type(self).list_methods:
            return lambda *args, **kwargs: cast(
                "list[T]", str.__dict__[name](self.value, *args, **kwargs)
            )
        return super().__getattribute__(name)

    @override
    def __len__(self) -> int:
        return len(self.value)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> Self: ...

    @override
    def __getitem__(self, index: int | slice) -> str | T | Self:
        if isinstance(index, slice):
            out = type(self)(
                self.name,
                item_callable=self.item_callable,
                sep=self.sep,
                max_split=self.max_split,
                default=self.default,
            )
            out.value = self.value[index]
            return out
        return self.value[index]

    @overload
    def __setitem__(self, index: int, value: str) -> None: ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[T]) -> None: ...

    @override
    def __setitem__(self, index: int | slice, value: str | Iterable[T]) -> None:
        self.value[index] = value

    @override
    def __delitem__(self, index: int | slice) -> None:
        del self.value[index]

    def insert(self, index: int, value: str | T) -> None:
        self.value.insert(index, value)

    def __bool__(self) -> bool:
        return bool(self.value)


class Config:
    def __new__(cls, *_, **__) -> Never:  # noqa: ANN002, ANN003
        msg = "The ConfigBase and and subclasses are not meant to be instantiated"
        raise TypeError(msg)

    example: Setting = Setting("EXAMPLE")
    list_example: ListSetting[str] = ListSetting("LIST_EXAMPLE")

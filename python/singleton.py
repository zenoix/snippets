from __future__ import annotations

from threading import Lock
from typing import Any, Generic, TypeVar, override

T = TypeVar("T")


class SingletonMeta(type, Generic[T]):
    _instances: dict[SingletonMeta[T], T] = {}  # noqa: RUF012

    _lock: Lock = Lock()

    @override
    def __call__(cls, *args: Any, **kwargs: Any) -> T:
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

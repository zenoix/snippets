from __future__ import annotations

from threading import Lock
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Singleton(type, Generic[T]):
    _instances: dict[Singleton[T], T] = {}  # noqa: RUF012

    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> T:  # noqa: ANN401
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

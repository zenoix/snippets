from __future__ import annotations

from threading import Lock
from typing import Any, override


# Using metaclasses
class SingletonMeta[T](type):
    _instances: dict[SingletonMeta[T], T] = {}  # noqa: RUF012

    _lock: Lock = Lock()

    @override
    def __call__(cls, *args: Any, **kwargs: Any) -> T:
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# Using an initializer function
class _Singleton:
    _instance: _Singleton | None = None

    def __init__(self) -> None:
        raise NotImplementedError


def get_singleton(*args: Any, **kwargs: Any) -> _Singleton:
    if _Singleton._instance is None:
        _Singleton._instance = _Singleton(*args, **kwargs)
    return _Singleton._instance

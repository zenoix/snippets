"""FastAPI logging using loguru.

This snippet is adapted from Timnology's youtube video.
"""

import logging
import os
import sys
from enum import StrEnum, auto
from typing import override

import uvicorn
from fastapi import FastAPI
from loguru import logger


class Environments(StrEnum):
    DEV = auto()
    STAGING = auto()
    PROD = auto()


class InvalidEnvironmentError(Exception):
    pass


env = os.getenv("ENV")

if env is None or env.lower() not in Environments:
    msg = (
        "invalid environment: expected one of "
        f"{', '.join(repr(environment.value) for environment in Environments)}, "
        f"got: '{env if env else ''}'"
    )
    raise InvalidEnvironmentError(msg)
else:
    ENV = Environments(env.lower())

logger.remove()
_ = logger.add(sys.stdout, serialize=ENV == Environments.PROD)


class InterceptHandler(logging.Handler):
    @override
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers.clear()
uvicorn_logger.setLevel(logging.INFO)
uvicorn_logger.addHandler(InterceptHandler())

app = FastAPI(title="API With Logging")


@app.get("/")
async def root() -> dict[str, str]:
    logger.info("Health check requested")
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000, log_config=None)

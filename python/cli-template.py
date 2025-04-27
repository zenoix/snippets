"""Template for CLI programs written in Python.

This template is a modified version of anthonywritescode's one on Youtube.
"""

import argparse
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass
class ProgramArgs:
    """Dataclass for parsed program args.

    This is used for static type checking.
    """

    example: str


def main(argv: Sequence[str] | None = None) -> int:
    """Docstring first line goes here.

    Args:
        argv: The argument strings to the program

    Returns:
        The exit code of the program (non-zero means an error occurred)
    """
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("-e", "--example", help="...")
    args = ProgramArgs(**parser.parse_args(argv).__dict__)  # pyright: ignore[reportAny]

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

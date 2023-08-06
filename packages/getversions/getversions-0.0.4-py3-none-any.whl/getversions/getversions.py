"""
Module to print the available and installed versions of a package in the repository.
"""

from __future__ import annotations

import sys
from typing import Optional

from getversions.core import get_avail_installed_versions, parse_args

if sys.version_info[:2] >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence


def print_avail_versions(package_name: str) -> None:
    """
    Print the available versions from the repository, and if the installed version
    is among them, mark it.
    """
    avail_versions, installed_version = get_avail_installed_versions(package_name)
    for version in avail_versions:
        if version != installed_version:
            print(version)
        else:
            print(f"*{version}")


def main(args: Optional[Sequence[str]] = None) -> int:
    """
    Process command line arguments if they are present, and call `print_avail_versions`
    with the relevant arguments.

    Args:
        args: Arguments to be processed by `parse_args`. Defaults to the command
        line arguments.

    Returns:
        0 to indicate success.
    """
    # https://github.com/python/mypy/issues/4145
    parsed_args = parse_args(__spec__.name, args)  # type: ignore
    print_avail_versions(parsed_args.package_name)
    return 0


if __name__ == "__main__":
    raise (SystemExit(main()))

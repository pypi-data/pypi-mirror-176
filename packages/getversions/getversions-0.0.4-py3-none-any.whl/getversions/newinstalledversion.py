"""
Module to determine if the installed version of a package is available in the
repository.
"""

from __future__ import annotations

import sys
from typing import Optional

from getversions.core import get_avail_installed_versions, parse_args

if sys.version_info[:2] >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence


def is_installed_version_in_repo(package_name: str) -> bool:
    """Return `True` if the installed version is available in the repository."""
    avail_versions, installed_version = get_avail_installed_versions(package_name)
    return installed_version in avail_versions


def main(args: Optional[Sequence[str]] = None) -> int:
    """
    Process command line arguments if they are present, and call
    `is_installed_version_in_repo` with the relevant arguments.

    Args:
        args: Arguments to be processed by `parse_args`. Defaults to the command
        line arguments.

    Returns:
        0 if the installed version is not available in the repository, and is hence
        a new version.
    """
    # https://github.com/python/mypy/issues/4145
    parsed_args = parse_args(__spec__.name, args)  # type: ignore
    return is_installed_version_in_repo(parsed_args.package_name)


if __name__ == "__main__":
    raise (SystemExit(main()))

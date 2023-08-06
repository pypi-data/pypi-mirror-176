"""
Module to print the available and installed versions of a package in the repository.
"""

from __future__ import annotations

import sys
from typing import Optional

from getversions.core import get_avail_installed_versions

if sys.version_info[:2] >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence


def main(args: Optional[Sequence[str]] = None) -> int:
    """
    Print the available versions from the repository, and if the installed version
    is among them, mark it.
    """
    avail_versions, installed_version = get_avail_installed_versions(args)
    for version in avail_versions:
        if version != installed_version:
            print(version)
        else:
            print(f"*{version}")
    return 0


if __name__ == "__main__":
    raise (SystemExit(main()))

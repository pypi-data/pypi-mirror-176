"""
Module to determine if the installed version of a package is available in the
repository.
"""

from __future__ import annotations

import sys
from typing import Optional

from getversions.core import get_avail_installed_versions

if sys.version_info[:2] >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence


def main(args: Optional[Sequence[str]] = None) -> bool:
    """Return 1 if the installed version is available in the repository."""
    avail_versions, installed_version = get_avail_installed_versions(args)
    return installed_version in avail_versions


if __name__ == "__main__":
    raise (SystemExit(main()))

"""Module to get the available versions in the repository of a Python package."""

from __future__ import annotations

import argparse
import subprocess
import sys
from typing import Callable, Optional, NamedTuple, Tuple

if sys.version_info[:2] >= (3, 9):
    from collections.abc import Iterable, Sequence
else:
    from typing import Iterable, Sequence

VersionStrategy = Callable[[str], Iterable[str]]


def get_pip_version() -> Tuple[int, ...]:
    """Get the version of pip."""
    pip_version_out = subprocess.check_output(
        [sys.executable, "-m", "pip", "--version"], text=True
    )
    version_str = pip_version_out.split()[1]
    version_str_parts = version_str.split(".")
    version_int_parts = map(int, version_str_parts)
    return tuple(version_int_parts)


def index_versions_strategy(package_name: str) -> Iterable[str]:
    """Use `pip index versions` to get available versions."""
    pip_index_versions_out = subprocess.check_output(
        [sys.executable, "-m", "pip", "index", "versions", package_name],
        stderr=subprocess.DEVNULL,
        text=True,
    )
    avail_versions_line = pip_index_versions_out.split("\n")[1]
    avail_versions_str = avail_versions_line.split(": ")[1]
    avail_versions_list = avail_versions_str.split(", ")
    return avail_versions_list


def double_equal_strategy(package_name: str) -> Iterable[str]:
    """Use an unspecifed version to get available versions."""
    raise NotImplementedError


def legacy_resolver_strategy(package_name: str) -> Iterable[str]:
    """Use an unspecified version with the legacy resolver to get available versions."""
    raise NotImplementedError


def not_implemented_strategy(package_name: str) -> Iterable[str]:
    """
    Use an unimplemented strategy that raises an exception when no other strategies
    are available.
    """
    raise NotImplementedError


def get_version_strategy(pip_version: Tuple[int, ...]) -> VersionStrategy:
    """Get the strategy to use based on the version of pip."""
    if pip_version >= (21, 2, 0):
        return index_versions_strategy
    if pip_version >= (21, 1, 0):
        return double_equal_strategy
    if pip_version >= (20, 3, 0):
        return legacy_resolver_strategy
    if pip_version >= (9, 0, 0):
        return double_equal_strategy
    return not_implemented_strategy


def get_installed_version(package_name: str) -> str:
    """Get the installed version of a package."""
    pip_list_out = subprocess.check_output(
        [sys.executable, "-m", "pip", "show", package_name], text=True
    )
    version_line = pip_list_out.split("\n")[1]
    version_str = version_line.split(": ")[1]
    return version_str


class ParsedArgs(NamedTuple):
    """Parsed agruments."""

    package_name: str


def parse_args(args: Optional[Sequence[str]] = None) -> ParsedArgs:
    """Parse and iterable of arguments, or the command line arguments."""
    parser = argparse.ArgumentParser("python -m getversions.getversions")
    parser.add_argument("package_name")
    parsed_args = parser.parse_args(args)
    return ParsedArgs(parsed_args.package_name)


def main(args: Optional[Sequence[str]] = None) -> int:
    """Print the available versions for a package."""
    parsed_args = parse_args(args)
    pip_version = get_pip_version()
    strategy = get_version_strategy(pip_version)
    avail_versions = strategy(parsed_args.package_name)
    installed_version = get_installed_version(parsed_args.package_name)
    for version in avail_versions:
        if version != installed_version:
            print(version)
        else:
            print(f"*{version}")
    return 0


if __name__ == "__main__":
    raise (SystemExit(main()))

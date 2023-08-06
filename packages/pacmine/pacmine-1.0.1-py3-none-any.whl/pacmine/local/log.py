from __future__ import annotations

from typing import List
from columnar import columnar
from termcolor import colored, cprint

from ..core.search_result import SearchResult
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..remote.dl_result import DownloadResult


def print_search_results(search_results: List[SearchResult]) -> None:
    cols = [
        colored("Name", attrs=["bold"]),
        colored("Slug", attrs=["bold"]),
        colored("Description", attrs=["bold"]),
        colored("Last Updated", attrs=["bold"]),
        colored("Supported Loaders", attrs=["bold"]),
    ]

    table = columnar(
        data=[result.get_row() for result in search_results],
        headers=cols,
        no_borders=False,
    )

    print(table)


def print_installed_mods(local_mods: List[DownloadResult]) -> None:
    cols = [
        colored("Slug", attrs=["bold"]),
        colored("Last Updated", attrs=["bold"]),
        colored("Source", attrs=["bold"]),
    ]

    table = columnar(
        data=[mod.get_row() for mod in local_mods], headers=cols, no_borders=False
    )

    print(table)

    info(f"{len(local_mods)} mods currently installed")


def print_installed_slugs(local_mods: List[str]) -> None:
    print(*local_mods)


def info(msg: str) -> None:
    cprint(f" {msg}", color="cyan")


def success(msg: str) -> None:
    cprint(f" {msg}", color="green")


def warning(msg: str) -> None:
    cprint(f"⚠️ {msg}", color="yellow")


def error(msg: str) -> None:
    cprint(f" {msg}", color="red")

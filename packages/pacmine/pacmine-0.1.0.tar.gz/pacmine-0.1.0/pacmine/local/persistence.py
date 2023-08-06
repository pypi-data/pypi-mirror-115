from pathlib import Path
from typing import List, Tuple

from semantic_version import Version

from ..core.loaders import Loaders
from ..remote.dl_result import DownloadResult


class Persistor:
    def __init__(self, location: str):
        self.location = Path(location)

    def is_valid(self) -> bool:
        raise NotImplementedError

    def new(self, version: Version, loader: Loaders) -> None:
        raise NotImplementedError

    def get_installed_mods(self) -> List[DownloadResult]:
        raise NotImplementedError

    def get_installed_slugs(self) -> List[str]:
        raise NotImplementedError

    def is_installed(self, slug: DownloadResult) -> bool:
        raise NotImplementedError

    def add(self, mod: DownloadResult) -> None:
        raise NotImplementedError

    def remove(self, slug: str) -> None:
        raise NotImplementedError

    def get_metadata(self) -> Tuple[Version, Loaders]:
        raise NotImplementedError

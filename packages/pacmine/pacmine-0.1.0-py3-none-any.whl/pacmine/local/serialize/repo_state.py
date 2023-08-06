from typing import List
from semantic_version import Version

from ...core.loaders import Loaders
from ...remote.dl_result import DownloadResult


class State:
    def __init__(self, version: Version, loader: Loaders):
        self.version = version
        self.loader = loader
        self.installed_mods: List[DownloadResult] = []

    def is_valid(self) -> bool:
        return self.version is not None and self.loader is not None

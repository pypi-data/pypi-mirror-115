from typing import List
from semantic_version import Version

from . import api
from .curse_api import CurseAPI
from .dl_result import DownloadResult
from .modrinth_api import ModrinthAPI
from ..core.exceptions import ModNotFoundException, VersionNotFoundException
from ..core.loaders import Loaders
from ..core.search_result import SearchResult


class Gateway:
    def __init__(self):
        self.curse_api = CurseAPI(api.curse_base)
        self.modrinth_api = ModrinthAPI(api.modrinth_base)

    def search(self, search_term) -> List[SearchResult]:
        curse_results = self.curse_api.search(search_term)
        modrinth_results = self.modrinth_api.search(search_term)

        return sorted((*curse_results, *modrinth_results), key=lambda x: x.name)

    def download(self, slug: str, version: Version, loader: Loaders) -> DownloadResult:
        try:
            return self.curse_api.download(slug, version, loader)
        except (ModNotFoundException, VersionNotFoundException):
            return self.modrinth_api.download(slug, version, loader)

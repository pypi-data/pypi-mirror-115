from typing import List, Dict

import arrow
from semantic_version import Version

from . import api
from .api import API, Sites
from .dl_result import DownloadResult
from ..core.exceptions import ModNotFoundException, VersionNotFoundException
from ..core.search_result import SearchResult
from ..core.loaders import Loaders


class CurseAPI(API):
    def search(self, search_term: str) -> List[SearchResult]:
        results = API.get_json(self._make_search_url(search_term))

        mods = []
        for mod in results:
            if not SearchResult.is_valid(mod):
                continue

            name = mod["name"]
            desc = mod["summary"]
            slug = mod["slug"]
            updated = mod["dateModified"]
            modloaders = mod["modLoaders"]
            id = mod["id"]

            mods.append(SearchResult(name, slug, desc, updated, modloaders, id))

        return mods

    def download(self, slug: str, version: Version, loader: Loaders) -> DownloadResult:
        mod_id = self._slug_to_id(slug)

        download_info = self._get_best_download(mod_id, version, loader)

        date_uploaded = download_info["fileDate"]
        upload_link = download_info["downloadUrl"]
        file_name = download_info["fileName"]

        api.get_file(upload_link, file_name)

        return DownloadResult(slug, mod_id, date_uploaded, file_name, Sites.Curseforge)

    def _make_search_url(self, search_term: str) -> str:
        return (
            f"{self._base_url}/search?gameId=432&sectionId=6&searchFilter={search_term}"
        )

    def _make_files_url(self, mod_id: str) -> str:
        return f"{self._base_url}/{mod_id}/files"

    def _slug_to_id(self, slug: str) -> str:
        mod_results = self.search(slug)

        for result in mod_results:
            if result.slug == slug:
                return result.id
        else:
            raise ModNotFoundException

    def _get_best_download(
        self, mod_id: str, version: Version, loader: Loaders
    ) -> Dict:
        files = API.get_json(self._make_files_url(mod_id))

        valid_loaders = [
            file for file in files if get_loader(file["modules"]) == loader
        ]

        valid_versions = [
            v_file
            for v_file in valid_loaders
            if version in api.parse_versions(v_file["gameVersion"])
        ]

        if not valid_versions:
            raise VersionNotFoundException

        to_download = max(
            valid_versions, key=lambda x: arrow.get(x["fileDate"]), default=None
        )

        return to_download


def get_loader(modules: Dict) -> Loaders:
    if any("fabric.mod.json" in module["foldername"] for module in modules):
        return Loaders.Fabric

    if any("pack.mcmeta" in module["foldername"] for module in modules):
        return Loaders.Forge

    return Loaders.Unknown

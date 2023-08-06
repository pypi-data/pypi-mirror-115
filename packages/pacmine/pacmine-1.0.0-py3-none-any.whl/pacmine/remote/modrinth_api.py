from typing import List, Dict

import arrow
from semantic_version import Version

from . import api
from .dl_result import DownloadResult
from ..core.exceptions import ModNotFoundException, VersionNotFoundException
from ..core.loaders import Loaders
from ..core.search_result import SearchResult
from ..remote.api import API, Sites


class ModrinthAPI(API):
    def search(self, search_term: str) -> List[SearchResult]:
        results = API.get_json(self._make_search_url(search_term))

        if "hits" not in results:
            return []

        mods = []
        for mod in results["hits"]:
            mod_id = mod["mod_id"].replace("local-", "")
            name = mod["title"]
            slug = mod["slug"]
            desc = mod["description"]
            updated = mod["date_modified"]
            modloaders = mod["categories"]

            mods.append(SearchResult(name, slug, desc, updated, modloaders, mod_id))

        return mods

    def download(self, slug: str, version: Version, loader: Loaders) -> DownloadResult:
        mod_id = self._slug_to_id(slug)

        download_info = self._get_best_download(mod_id, version, loader)

        date_uploaded = download_info["date_published"]
        upload_link = download_info["files"][0]["url"]
        file_name = download_info["files"][0]["filename"]

        api.get_file(upload_link, file_name)

        return DownloadResult(slug, mod_id, date_uploaded, file_name, Sites.Modrinth)

    def _make_search_url(self, search_term: str) -> str:
        return f"{self._base_url}/mod?query={search_term}"

    def _make_files_url(self, mod_id: str) -> str:
        return f"{self._base_url}/mod/{mod_id}/version"

    def _slug_to_id(self, slug: str) -> str:
        mod_results = self.search(slug)

        for result in mod_results:
            if result.slug == slug:
                return result.id
        else:
            raise ModNotFoundException

    def _get_best_download(self, mod_id, version, loader) -> Dict:
        files = API.get_json(self._make_files_url(mod_id))

        valid_loaders = [file for file in files if loader.value in file["loaders"]]

        valid_versions = [
            v_file
            for v_file in valid_loaders
            if version in api.parse_versions(v_file["game_versions"])
        ]

        if not valid_versions:
            raise VersionNotFoundException

        to_download = max(
            valid_versions, key=lambda x: arrow.get(x["date_published"]), default=None
        )

        return to_download

from __future__ import annotations

import requests

from enum import Enum
from tqdm import tqdm
from semantic_version import Version
from typing import List, Dict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dl_result import DownloadResult
from ..core.search_result import SearchResult
from ..core.loaders import Loaders


curse_base = "https://addons-ecs.forgesvc.net/api/v2/addon"
modrinth_base = "https://api.modrinth.com/api/v1"

_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}


class API:
    def __init__(self, base_url: str):
        self._base_url = base_url

    def search(self, search_term: str) -> List[SearchResult]:
        raise NotImplementedError

    def download(self, slug: str, version: Version, loader: Loaders) -> DownloadResult:
        raise NotImplementedError

    @staticmethod
    def get_json(url: str) -> Dict:
        return requests.get(url, headers=_headers).json()


def parse_versions(game_versions: List[str]) -> List[Version]:
    versions = []
    for version in game_versions:
        try:
            versions.append(Version.coerce(version))
        except ValueError:
            continue

    return versions


def get_file(url: str, filename: str, with_progress: bool = False) -> None:
    r = requests.get(url, stream=with_progress)
    with open(filename, "wb") as f:
        if with_progress:
            pbar = tqdm(unit="B", total=int(r.headers["Content-Length"]))
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    pbar.update(len(chunk))
                    f.write(chunk)
        else:
            f.write(r.content)


class Sites(Enum):
    Curseforge = "CurseForge"
    Modrinth = "Modrinth"

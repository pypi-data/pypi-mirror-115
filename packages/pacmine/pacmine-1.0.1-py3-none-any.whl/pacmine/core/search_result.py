from __future__ import annotations

import arrow

from typing import List, Dict
from termcolor import colored

from .loaders import Loaders


class SearchResult:
    def __init__(
        self,
        name: str,
        slug: str,
        desc: str,
        updated: str,
        modloaders: List[str],
        mod_id: str,
    ):
        self.name = name
        self.slug = slug
        self.desc = desc
        self.updated = arrow.get(updated)
        self.modloaders = [
            loader
            for loader in map(Loaders.from_str, modloaders)
            if loader != Loaders.Unknown
        ]
        self.id = mod_id

    def get_row(self) -> List:
        return [
            colored(self.name, color="green"),
            self.slug,
            self.desc,
            self.updated.format("YYYY-MM-DD"),
            ", ".join(loader.name for loader in self.modloaders),
        ]

    @staticmethod
    def is_valid(api_data: Dict) -> bool:
        keys = ["name", "summary", "dateModified", "modLoaders", "id"]

        return all(key in api_data for key in keys)

    def __repr__(self):
        return self.name

from __future__ import annotations

import arrow

from typing import List

from .api import Sites


class DownloadResult:
    def __init__(
        self, slug: str, mod_id: str, date_updated: str, filename: str, source: Sites
    ):
        self.slug = slug
        self.mod_id = mod_id
        self.date_updated = arrow.get(date_updated)
        self.filename = filename
        self.source = source

    def get_row(self) -> List[str]:
        return [self.slug, self.date_updated.format("YYYY-MM-DD"), self.source.value]

    def __eq__(self, other: DownloadResult) -> bool:
        return (
            self.slug == other.slug
            and self.mod_id == other.mod_id
            and self.date_updated == other.date_updated
            and self.filename == other.filename
            and self.source == other.source
        )

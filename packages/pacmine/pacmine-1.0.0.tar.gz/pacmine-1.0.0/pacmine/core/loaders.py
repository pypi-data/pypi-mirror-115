from __future__ import annotations

from enum import Enum


class Loaders(Enum):
    Forge = "forge"
    Fabric = "fabric"
    Unknown = "unknown"

    @staticmethod
    def from_str(enum_string: str) -> Loaders:
        if enum_string.lower() == "forge":
            return Loaders.Forge
        if enum_string.lower() == "fabric":
            return Loaders.Fabric
        return Loaders.Unknown

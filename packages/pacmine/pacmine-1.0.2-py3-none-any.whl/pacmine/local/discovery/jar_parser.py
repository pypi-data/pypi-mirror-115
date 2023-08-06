import json

from pathlib import Path
from typing import Optional
from zipfile import ZipFile

from ...remote.dl_result import DownloadResult
from ...core.loaders import Loaders

_fabric_file = "fabric.mod.json"
_forge_file = "META-INF/mods.toml"


def parse_jar(jar_file: Path) -> Optional[DownloadResult]:
    jar_type = _jar_type(jar_file)

    with ZipFile(jar_file, "r") as unzipped_jar:
        if jar_type == Loaders.Fabric:
            return _parse_fabric(unzipped_jar)

        if jar_type == Loaders.Forge:
            return _parse_force(unzipped_jar)


def _parse_fabric(file: ZipFile) -> DownloadResult:
    with file.open(_fabric_file) as json_file:
        full_doc = json_file.read().decode("utf-8", "ignore")
        mod_data = json.loads(full_doc, strict=False)


def _parse_force(file: ZipFile) -> DownloadResult:
    pass


def _jar_type(jar_file: Path) -> Loaders:
    with ZipFile(jar_file, "r") as f:
        if _is_forge(f):
            return Loaders.Forge
        if _is_fabric(f):
            return Loaders.Fabric
    return Loaders.Unknown


def _is_fabric(zip_file: ZipFile) -> bool:
    return _fabric_file in zip_file.namelist()


def _is_forge(zip_file: ZipFile) -> bool:
    return _forge_file in zip_file.namelist()

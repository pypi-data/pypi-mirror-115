import os
import pickle
from typing import List, Tuple
from semantic_version import Version

from .repo_state import State
from ...core.exceptions import ModNotFoundException
from ...core.loaders import Loaders
from ...local.persistence import Persistor
from ...remote.dl_result import DownloadResult


FILE_NAME = "mods.pkl"


class Serializer(Persistor):
    def get_metadata(self) -> Tuple[Version, Loaders]:
        state = self._read_pickle()
        return state.version, state.loader

    def is_valid(self) -> bool:
        if os.path.exists(FILE_NAME):
            state = self._read_pickle()
            return state.is_valid()

    def new(self, version: Version, loader: Loaders) -> None:
        state = State(version, loader)
        self._write_pickle(state)

    def get_installed_mods(self) -> List[DownloadResult]:
        state = self._read_pickle()

        return sorted(state.installed_mods, key=lambda x: x.slug)

    def get_installed_slugs(self) -> List[str]:
        state = self._read_pickle()

        return _get_slugs(state)

    def is_installed(self, slug: str) -> bool:
        state = self._read_pickle()

        return slug in _get_slugs(state)

    def add(self, mod: DownloadResult) -> None:
        state = self._read_pickle()

        if mod not in state.installed_mods:
            state.installed_mods.append(mod)

        self._write_pickle(state)

    def remove(self, slug: str) -> None:
        state = self._read_pickle()

        if slug not in _get_slugs(state):
            raise ModNotFoundException

        for mod in state.installed_mods:
            if mod.slug == slug:
                os.remove(mod.filename)
                state.installed_mods.remove(mod)
                break

        self._write_pickle(state)

    def _read_pickle(self) -> State:
        with open(self.location.joinpath(FILE_NAME), "rb") as infile:
            return pickle.load(infile)

    def _write_pickle(self, state: State) -> None:
        with open(self.location.joinpath(FILE_NAME), "wb") as outfile:
            pickle.dump(state, outfile)


def _get_slugs(state: State) -> List[str]:
    return [mod.slug for mod in state.installed_mods]

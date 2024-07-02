from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, List, Mapping, Iterable

from .artifact import Artifact
from .base_model import BaseModel


@dataclass
class Download(BaseModel):
    sha1: str = None
    size: int = None
    url: str = None
    provided: bool = False

    def __init__(self, sha1: str, size: int, url: str, provided: bool = False):
        self.sha1 = sha1
        self.size = size
        self.url = url
        self.provided = provided


@dataclass
class LibraryDownload(Download):
    path: str = None

    def __init__(self, sha1: str, size: int, url: str, path: str, provided: bool = False):
        super().__init__(sha1, size, url, provided)
        self.path = path

    def getPath(self) -> str:
        return self.path

    def getSha1(self) -> str:
        return self.sha1

    def getProvided(self) -> bool:
        return self.provided


@dataclass
class Downloads(BaseModel):
    artifact: LibraryDownload
    classifiers: Dict[str, LibraryDownload] = None

    def getArtifact(self) -> LibraryDownload:
        return self.artifact

    def getClassifiers(self) -> Set[LibraryDownload]:
        return set() if self.classifiers is None else set(self.classifiers.values())


@dataclass
class Library(BaseModel):
    name: Artifact
    downloads: Downloads

    def getName(self) -> Artifact:
        return self.name

    def getDownloads(self) -> Downloads:
        return self.downloads


class Version(BaseModel):
    id: str
    downloads: Dict[str, Download] = {}
    libraries: List[Library]

    def __init__(self, id: str, downloads: Dict[str, Download], libraries: List[Library]):
        self.id = id
        self.downloads = downloads
        self.libraries = libraries

    def getDownload(self, key: str) -> Optional[Download]:
        return self.downloads.get(key)

    def getLibraries(self) -> List[Library]:
        return self.libraries or []

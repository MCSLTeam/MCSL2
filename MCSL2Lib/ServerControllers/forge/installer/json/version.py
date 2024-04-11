from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, List

from .artifact import Artifact
from .base_model import BaseModel


@dataclass
class Version(BaseModel):
    id: str
    downloads: Dict[str, 'Version.Download']
    libraries: list

    def getDownload(self, key: str) -> Optional['Version.Download']:
        return self.downloads.get(key)

    def getLibraries(self) -> List[Library]:
        return self.libraries or []

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

        def getProvided(self) -> bool:
            return self.provided

    @dataclass
    class Downloads(BaseModel):
        artifact: 'Version.LibraryDownload'
        classifiers: Dict[str, 'Version.LibraryDownload'] = None

        def getArtifact(self) -> 'Version.LibraryDownload':
            return self.artifact

        def getClassifiers(self) -> Set['Version.LibraryDownload']:
            return set() if self.classifiers is None else set(self.classifiers.values())

        @classmethod
        def artifact_factory(cls, item) -> 'Version.LibraryDownload':
            return Version.LibraryDownload(**item)

        @classmethod
        def classifiers_factory(cls, items) -> Dict[str, 'Version.LibraryDownload']:
            return {k: Version.LibraryDownload(**v) for k, v in items.items()} if items is not None else None

    @dataclass
    class Library(BaseModel):
        name: Artifact
        downloads: 'Version.Downloads'

        def getName(self) -> Artifact:
            return self.name

        def getDownloads(self) -> 'Version.Downloads':
            return self.downloads

        @classmethod
        def name_factory(cls, item) -> Artifact:
            return Artifact.from_(item)

        @classmethod
        def downloads_factory(cls, item) -> 'Version.Downloads':
            return Version.Downloads.of(item)

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .base_model import BaseModel


@dataclass
class Artifact(BaseModel):
    domain: str
    name: str
    version: str
    classifier: str = None
    ext: str = "jar"

    # Caches so we don't rebuild every time we're asked.
    path: str = None
    file: str = None
    descriptor: str = None

    @staticmethod
    def from_(descriptor: str) -> "Artifact":
        pts = descriptor.split(":")
        domain = pts[0]
        name = pts[1]

        last = len(pts) - 1
        idx = pts[last].find("@")

        if idx != -1:
            ext = pts[last][idx + 1:]
            pts[last] = pts[last][:idx]
        else:
            ext = "jar"

        version = pts[2]
        classifier = pts[3] if len(pts) > 3 else None

        file = name + "-" + version
        if classifier is not None:
            file += "-" + classifier
        file += "." + ext

        path = domain.replace(".", "/") + "/" + name + "/" + version + "/" + file

        return Artifact(
            domain=domain,
            name=name,
            version=version,
            classifier=classifier,
            ext=ext,
            path=path,
            file=file,
            descriptor=descriptor,
        )

    @classmethod
    def __from_raw__(cls, data: Any) -> "Artifact":
        return Artifact.from_(data)

    def getLocalPath(self, base: Path) -> Path:
        return base / self.path.replace("/", os.sep)

    def getDescriptor(self) -> str:
        return self.descriptor

    def getPath(self) -> str:
        return self.path

    def getDomain(self) -> str:
        return self.domain

    def getName(self) -> str:
        return self.name

    def getVersion(self) -> str:
        return self.version

    def getClassifier(self) -> str:
        return self.classifier

    def getExt(self) -> str:
        return self.ext

    def getFilename(self) -> str:
        return self.file

    def __str__(self) -> str:
        return self.descriptor

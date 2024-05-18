from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Iterable, Mapping

from .artifact import Artifact
from .base_model import BaseModel
from .mirror import Mirror
from .spec import Spec
from .version import Version
from ..download_utils import DownloadUtils


@dataclass
class Install(Spec):
    profile: str
    version: str
    icon: str
    minecraft: str
    json: str
    logo: str
    path: Artifact
    urlIcon: str
    welcome: str
    mirrorList: str

    libraries: List[Version.Library]
    processors: List['Install.Processor']  # type: List[Install.Processor]
    data: Dict[str, 'Install.DataFile']  # type: Dict[str, Install.DataFile]

    # non-serializable
    mirror: Mirror
    triedMirrors: bool = False

    hideClient: bool = False
    hideServer: bool = False
    hideExtract: bool = False
    hideOffline: bool = False

    def getProfile(self) -> str:
        return self.profile

    def getVersion(self) -> str:
        return self.version

    def getIcon(self) -> str:
        return self.icon

    def getMinecraft(self) -> str:
        return self.minecraft

    def getJson(self) -> str:
        return self.json

    def getLogo(self) -> str:
        return self.logo

    def getPath(self) -> Artifact:
        return self.path

    def getUrlIcon(self) -> str:
        return "/url.png" if self.urlIcon is None else self.urlIcon

    def getWelcome(self) -> str:
        return "" if self.welcome is None else self.welcome

    def getMirrorList(self) -> str:
        return self.mirrorList

    def getMirror(self) -> Optional[Mirror]:
        from ..simple_installer import SimpleInstaller

        custom_mirror = SimpleInstaller.mirror

        if (self.mirror is not None):
            return self.mirror
        if (custom_mirror is not None):
            self.mirror = Mirror("Mirror", "", "", custom_mirror if custom_mirror is None else "")
            return self.mirror
        if self.getMirrorList() is None:
            return None
        if (not self.triedMirrors):
            self.triedMirrors = True
            list_: List[Mirror] = DownloadUtils.downloadMirrors(self.getMirrorList())
            self.mirror = None if not list_ else list_[random.randint(0, len(list_) - 1)]
        return self.mirror

    def getLibraries(self) -> List[Version.Library]:
        return [] if self.libraries is None else self.libraries

    def getProcessors(self, side: str) -> List['Install.Processor']:
        if self.processors is None:
            return []
        return [p for p in self.processors if p.isSide(side)]

    def getData(self, client: bool) -> Dict[str, str]:
        if self.data is None:
            return {}
        return {k: (v.client if client else v.server) for k, v in self.data.items()}

    @classmethod
    def libraries_factory(cls, items: Iterable):
        rv = []
        for i in items:
            rv.append(Version.Library.of(i))
        return rv

    @classmethod
    def processors_factory(cls, items: Iterable):
        return [Install.Processor.of(i) for i in items]

    @classmethod
    def data_factory(cls, items: Mapping[str, Mapping]):
        return {k: Install.DataFile(**v) for k, v in items.items()}

    @classmethod
    def path_factory(cls, item):
        return Artifact.from_(item)

    @dataclass
    class Processor(BaseModel):
        sides: List[str] = None
        jar: Artifact = None
        classpath: List[Artifact] = None
        args: List[str] = None
        outputs: Dict[str, str] = None

        def isSide(self, side: str) -> bool:
            return self.sides is None or side in self.sides

        def getJar(self) -> Artifact:
            return self.jar

        def getClasspath(self) -> List[Artifact]:
            return [] if self.classpath is None else self.classpath

        def getArgs(self) -> List[str]:
            return [] if self.args is None else self.args

        def getOutputs(self) -> Dict[str, str]:
            return {} if self.outputs is None else self.outputs

        @classmethod
        def jar_factory(cls, item):
            return Artifact.from_(item)

        @classmethod
        def classpath_factory(cls, items: Iterable):
            return [Artifact.from_(i) for i in items]

    @dataclass
    class DataFile:
        # /**
        #  * Can be in the following formats:
        #  * [value] - An absolute path to an artifact located in the target maven style repo.
        #  * 'value' - A string literal, remove the 's and use this value
        #  * value - A file in the installer package, to be extracted to a temp folder, and then have the absolute path in replacements.
        #  */

        client: str = None
        server: str = None

        def getClient(self) -> str:
            return self.client

        def getServer(self) -> str:
            return self.server

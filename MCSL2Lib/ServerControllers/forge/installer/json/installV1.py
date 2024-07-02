from dataclasses import dataclass
from typing import Optional

from .install import Install


@dataclass
class InstallV1(Install):
    serverJarPath: Optional[str] = None

    @staticmethod
    def from_installV0(v0: Install) -> "InstallV1":
        self = InstallV1.of({})
        self.profile = v0.profile
        self.version = v0.version
        self.icon = v0.icon
        self.minecraft = v0.minecraft
        self.json = v0.json
        self.logo = v0.logo
        self.path = v0.path

        self.welcome = v0.welcome
        self.mirrorList = v0.mirrorList
        self.hideClient = v0.hideClient
        self.hideServer = v0.hideServer
        self.hideExtract = v0.hideExtract
        self.libraries = v0.libraries
        self.processors = v0.processors
        self.data = v0.data
        # for not used
        # self.urlIcon = v0.urlIcon
        return self

    def getServerJarPath(self) -> str:
        if self.serverJarPath is None:
            return "{ROOT}/minecraft_server.{MINECRAFT_VERSION}.jar"

        return self.serverJarPath

#     Copyright 2024, MCSL Team, mailto:services@mcsl.com.cn
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
from abc import ABCMeta, abstractmethod
from typing import List


class BasePlugin(metaclass=ABCMeta):
    def __init__(self):
        self.pluginName: str = ""
        self.version: str = ""
        self.description: str = []
        self.author: List[str] = []
        self.authorEmail: List[str] = []
        self.icon: str = None
        self.isEnabled: bool = False
        self.isLoaded: bool = False
        self.LOAD = None
        self.ENABLE = None
        self.DISABLE = None

    @abstractmethod
    def register_loadFunc(self, load_fn):
        pass

    @abstractmethod
    def register_enableFunc(self, enable_fn):
        pass

    @abstractmethod
    def register_disableFunc(self, disable_fn):
        pass


class BasePluginLoader:
    @classmethod
    @abstractmethod
    def load(cls, pluginName: str):
        pass


class BasePluginManager(metaclass=ABCMeta):
    @abstractmethod
    def disablePlugin(self, plugin: BasePlugin):
        pass

    @abstractmethod
    def loadPlugin(self, plugin: BasePlugin):
        pass

    @abstractmethod
    def enablePlugin(self, plugin: BasePlugin):
        pass

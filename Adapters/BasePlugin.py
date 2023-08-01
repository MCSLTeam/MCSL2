from abc import ABCMeta, abstractmethod
from typing import List


class BasePlugin(metaclass=ABCMeta):

    def __init__(self):
        self.pluginName: str = ""
        self.version: str = ""
        self.description: str = []
        self.author: List[str] = []
        self.authorEmail: List[str] = []
        self.isEnabled: bool = False
        self.isLoaded: bool = False
        self.fn_Load = None
        self.fn_Enable = None
        self.fn_Disable = None

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

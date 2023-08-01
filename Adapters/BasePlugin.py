from abc import ABCMeta, abstractmethod
from typing import List


class BasePlugin(metaclass=ABCMeta):

    def __init__(self):
        self.plugin_name: str = ""
        self.version: str = ""
        self.description: str = []
        self.author: List[str] = []
        self.author_email: List[str] = []
        self.is_enabled: bool = False
        self.is_loaded: bool = False
        self.load_func = None
        self.enable_func = None
        self.disable_func = None

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
    def load(cls, plugin_name: str):
        pass


class BasePluginManager(metaclass=ABCMeta):

    @abstractmethod
    def disable(self, plugin: BasePlugin):
        pass

    @abstractmethod
    def load(self, plugin: BasePlugin):
        pass

    @abstractmethod
    def enable(self, plugin: BasePlugin):
        pass

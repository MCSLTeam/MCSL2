from __future__ import annotations

from Adapters.BasePlugin import BasePlugin, BasePluginLoader, BasePluginManager, BasePluginFn
import os


class Plugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.plugin_type: str = "common"

    def register_loadFunc(self, load_fn):
        self.load_func = load_fn

    def register_enableFunc(self, enable_fn):
        self.enable_func = enable_fn

    def register_disableFunc(self, disable_fn):
        self.disable_func = disable_fn


class PluginLoader(BasePluginLoader):
    @classmethod
    def load(cls, pluginName: str) -> Plugin | None:
        imported_plugin: Plugin = __import__("plugin." + pluginName + "." + pluginName, fromlist=[pluginName])
        imported_plugin = imported_plugin.__getattribute__("test")
        if imported_plugin.__class__.__name__ == Plugin.__name__:
            return imported_plugin
        else:
            return None


class PluginManager(BasePluginManager):
    def __init__(self):
        self.pluginDict: {str, Plugin} = {}

    def disable(self, plugin_name: str) -> (bool, str):
        plugin: Plugin = self.pluginDict.pop(plugin_name, default=None)
        if plugin is None:
            return False
        if plugin.disable_func is None:
            BasePluginFn.disable()
        else:
            plugin.disable_func()

    def load(self, plugin_name: str):
        plugin: Plugin = PluginLoader.load(plugin_name)
        if plugin is None:
            return
        else:
            self.pluginDict[plugin_name] = plugin

    def enable(self, plugin_name: str):
        plugin: Plugin = self.pluginDict.get(plugin_name, default=None)
        if plugin is None:
            return False
        if plugin.disable_func is None:
            BasePluginFn.enable()
        else:
            plugin.enable_func()

    def load_all(self):
        path = os.getcwd() + "//plugin"
        path_list = next(os.walk(path))[1]
        for pluginName in path_list:
            self.load(pluginName)
        print(self.pluginDict)

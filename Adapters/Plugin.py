from __future__ import annotations

import json
import threading
from threading import Thread
from typing import List

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SmoothScrollArea

from Adapters.BasePlugin import BasePlugin, BasePluginLoader, BasePluginManager

import os

from MCSL2Lib.pluginWidget import singlePluginWidget


class Plugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self._plugin_type: str = "common"

    def register_loadFunc(self, load_fn):
        self.load_func = load_fn

    def register_enableFunc(self, enable_fn):
        self.enable_func = enable_fn

    def register_disableFunc(self, disable_fn):
        self.disable_func = disable_fn


class PluginLoader(BasePluginLoader):
    @classmethod
    def load(cls, pluginName: str) -> Plugin | None:
        imported_plugin: Plugin = __import__(f"plugin.{pluginName}.{pluginName}", fromlist=[pluginName])
        imported_plugin = imported_plugin.__getattribute__("test")
        try:
            imported_plugin.plugin_name = pluginName
            with open(f"plugin//{pluginName}//config.json", 'r',encoding="utf-8") as f:
                imported_config = json.loads(f.read())
            imported_plugin.version = imported_config["version"]
            imported_plugin.description = imported_config["description"]
            imported_plugin.author = imported_config["author"]
            imported_plugin.author_email = imported_config["author_email"]
        except:
            raise Warning("读取配置错误", pluginName)
        if imported_plugin.__class__.__name__ == Plugin.__name__:
            return imported_plugin
        else:
            return None


class PluginManager(BasePluginManager):
    def __init__(self):
        self.pluginDict: {str, Plugin} = {}
        self.thread_pool: List[Thread] = []

    def disable(self, plugin_name: str) -> (bool, str):
        plugin: Plugin = self.pluginDict.pop(plugin_name, default=None)
        if plugin is None:
            return False
        if plugin.disable_func is not None:
            plugin.disable_func()

    def load(self, plugin_name: str):
        plugin: Plugin = PluginLoader.load(plugin_name)
        if plugin is None:
            return
        else:
            if plugin.load_func is not None:
                plugin.load_func()
            self.pluginDict[plugin_name] = plugin

    def enable(self, plugin_name: str):
        plugin: Plugin = self.pluginDict.get(plugin_name, default=None)
        if plugin is None:
            return False
        if plugin.enable_func is not None:
            plugin.enable_func()

    def load_all(self):
        path = os.getcwd() + "//plugin"
        path_list = next(os.walk(path))[1]
        for pluginName in path_list:
            self.load(pluginName)
        print(self.pluginDict)

    def enable_all(self):
        for plugin_name in self.pluginDict.keys():
            plugin: Plugin = self.pluginDict.get(plugin_name)
            if plugin.enable_func is not None:
                try:
                    self.enable(plugin_name)
                except:
                    continue

    def disable_all(self):
        self.is_disabled_all = True

    def show(self,gridLayout_3:QVBoxLayout):
        for pluginName in self.pluginDict.keys():
            plugin: Plugin = self.pluginDict.get(pluginName)
            plugin_widget = singlePluginWidget()
            plugin_widget.pluginName.setText(plugin.plugin_name)
            plugin_widget.pluginMoreInfo.setText(plugin.description)
            gridLayout_3.addWidget(plugin_widget)


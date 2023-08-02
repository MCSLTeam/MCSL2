from __future__ import annotations
from json import loads
# import threading
from threading import Thread
from typing import List

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QVBoxLayout
from Adapters.BasePlugin import BasePlugin, BasePluginLoader, BasePluginManager
from os import walk, getcwd
from MCSL2Lib.pluginWidget import singlePluginWidget


class Plugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self._pluginType: str = "common"

    def register_loadFunc(self, fn_Load):
        self.LOAD = fn_Load

    def register_enableFunc(self, fn_Enable):
        self.ENABLE = fn_Enable

    def register_disableFunc(self, fn_Disable):
        self.DISABLE = fn_Disable


class PluginLoader(BasePluginLoader):
    @classmethod
    def load(cls, pluginName: str) -> Plugin | None:
        importedPlugin: Plugin = __import__(f"Plugins.{pluginName}.{pluginName}", fromlist=[pluginName])
        importedPlugin = importedPlugin.__getattribute__(pluginName)
        try:
            importedPlugin.pluginName = pluginName
            with open(f"Plugins//{pluginName}//config.json", 'r',encoding="utf-8") as f:
                importedPluginConfig: dict = loads(f.read())
            importedPlugin.version = importedPluginConfig.get("version")
            importedPlugin.description = importedPluginConfig.get("description")
            importedPlugin.author = importedPluginConfig.get("author")
            importedPlugin.authorEmail = importedPluginConfig.get("author_email")
            if "icon" in importedPluginConfig:
                importedPlugin.icon = importedPluginConfig.get("icon")


        except:
            raise Warning("读取配置错误", pluginName)
        if importedPlugin.__class__.__name__ == Plugin.__name__:
            return importedPlugin
        else:
            return None


class PluginManager(BasePluginManager):
    def __init__(self):
        self.pluginDict: {str, Plugin} = {}
        self.threadPool: List[Thread] = []

    def disablePlugin(self, pluginName: str) -> (bool, str):
        '''禁用插件'''
        plugin: Plugin = self.pluginDict.pop(pluginName, default=None)
        if plugin is None:
            return False
        if plugin.DISABLE is not None:
            plugin.DISABLE()

    def enablePlugin(self, pluginName: str):
        '''启用插件但不加载'''
        plugin: Plugin = self.pluginDict.get(pluginName, default=None)
        if plugin is None:
            return False
        if plugin.ENABLE is not None:
            plugin.ENABLE()

    def loadPlugin(self, pluginName: str):
        '''加载插件'''
        plugin: Plugin = PluginLoader.load(pluginName)
        if plugin is None:
            return
        else:
            if plugin.LOAD is not None:
                plugin.LOAD()
            self.pluginDict[pluginName] = plugin

    def loadAllPlugins(self):
        '''加载所有插件'''
        path = getcwd() + "\\Plugins"
        try:
            pathList = next(walk(path))[1]
            for pluginName in pathList:
                self.loadPlugin(pluginName)
            print(self.pluginDict)
        except Exception as e:
            pass

    def enableAllPlugins(self):
        '''启用所有插件但不加载'''
        for pluginName in self.pluginDict.keys():
            plugin: Plugin = self.pluginDict.get(pluginName)
            if plugin.ENABLE is not None:
                try:
                    self.enablePlugin(pluginName)
                except:
                    continue

    def disableAllPlugins(self):
        '''禁用所有插件'''
        self.is_disabled_all = True

    def initSinglePluginsWidget(self,gridLayout_3:QVBoxLayout):
        for pluginName in self.pluginDict.keys():
            plugin: Plugin = self.pluginDict.get(pluginName)
            pluginWidget = singlePluginWidget()
            pluginWidget.pluginName.setText(f"{plugin.pluginName} {plugin.version}  By {plugin.author}")
            pluginWidget.pluginMoreInfo.setText(plugin.description)
            if plugin.icon is None:
                pluginWidget.pluginIcon.setPixmap(QPixmap(":/built-InIcons/MCSL2.png"))
                pluginWidget.pluginIcon.setFixedSize(50,50)
            else:
                pluginWidget.pluginIcon.setPixmap(QPixmap(f":/Plugins//{pluginName}//{plugin.icon}"))
                pluginWidget.pluginIcon.setFixedSize(50, 50)
            gridLayout_3.addWidget(pluginWidget)


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
        importedPlugin: Plugin = __import__(
            f"Plugins.{pluginName}.{pluginName}", fromlist=[pluginName]
        )
        importedPlugin = importedPlugin.__getattribute__(pluginName)
        try:
            importedPlugin.pluginName = pluginName
            with open(
                f"Plugins//{pluginName}//config.json", "r", encoding="utf-8"
            ) as f:
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
        """禁用插件"""
        plugin: Plugin = self.pluginDict.get(pluginName)
        plugin.isEnabled = False
        if plugin is None:
            return False,None
        if plugin.DISABLE is not None:
            try:
                plugin.DISABLE()
            except:
                return False,plugin.pluginName
        return True,plugin.pluginName

    def decideEnableOrDisable(self, pluginName: str, switchBtnStatus: bool):
        if switchBtnStatus:
            self.enablePlugin(pluginName)
        else:
            self.disablePlugin(pluginName)

    def enablePlugin(self, pluginName: str):
        """启用插件"""
        plugin: Plugin = self.pluginDict.get(pluginName)
        if plugin is None:
            return False
        if plugin.ENABLE is not None:
            try:
                plugin.isEnabled = True
                plugin.ENABLE()
            except:
                raise Warning("未完全卸载", plugin.pluginName)

    def loadPlugin(self, pluginName: str):
        """加载插件但不启用"""
        plugin: Plugin = PluginLoader.load(pluginName)
        plugin.isLoaded = True
        if plugin is None:
            return
        else:
            if plugin.LOAD is not None:
                plugin.LOAD()
            self.pluginDict[pluginName] = plugin

    def loadAllPlugins(self):
        """加载所有插件但不启用"""
        path = getcwd() + "\\Plugins"
        pathList = next(walk(path))[1]
        for pluginName in pathList:
            try:
                self.loadPlugin(pluginName)
            except Exception as e:
                raise Warning("加载插件错误")
        print(self.pluginDict)

    def enableAllPlugins(self):
        """启用所有插件"""
        for pluginName in self.pluginDict.keys():
            plugin: Plugin = self.pluginDict.get(pluginName)
            if plugin.ENABLE is not None:
                try:
                    self.enablePlugin(pluginName)
                except:
                    continue

    def disableAllPlugins(self):
        """禁用所有插件"""
        self.is_disabled_all = True

    def initSinglePluginsWidget(self, gridLayout_3: QVBoxLayout):
        for pluginName in self.pluginDict.keys():
            plugin: Plugin = self.pluginDict.get(pluginName)
            pluginWidget = singlePluginWidget()
            pluginWidget.pluginName.setText(
                f"{plugin.pluginName}  版本：{plugin.version}  作者： {plugin.author}"
            )
            pluginWidget.pluginMoreInfo.setText(f"注释：{plugin.description}")
            if plugin.icon is None:
                pluginWidget.pluginIcon.setPixmap(QPixmap(":/built-InIcons/MCSL2.png"))
                pluginWidget.pluginIcon.setFixedSize(50, 50)
            else:
                import os

                url = os.path.dirname(os.path.abspath(__file__))  # 文件夹
                url = os.path.abspath(os.path.join(url, ".."))
                pluginWidget.pluginIcon.setPixmap(
                    QPixmap(f"{url}\\Plugins\\{pluginName}\\{plugin.icon}")
                )
                pluginWidget.pluginIcon.setFixedSize(50, 50)

            # 设置槽函数
            pluginWidget.SwitchButton.checkedChanged.connect(
                lambda: self.decideEnableOrDisable(
                    pluginName, switchBtnStatus=pluginWidget.SwitchButton.isChecked()
                )
            )

            gridLayout_3.addWidget(pluginWidget)
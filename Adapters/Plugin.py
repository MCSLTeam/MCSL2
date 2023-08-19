from __future__ import annotations
from json import loads

# import threading
from threading import Thread
from typing import List

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QSpacerItem
from Adapters.BasePlugin import BasePlugin, BasePluginLoader, BasePluginManager
from os import walk, getcwd, path as ospath
from MCSL2Lib.pluginWidget import singlePluginWidget
from MCSL2Lib.variables import PluginVariables
from MCSL2Lib.variables import Singleton

pluginVariables = PluginVariables()


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
    """插件加载器"""

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
    """插件管理器"""

    def __init__(self):
        self.pluginDict: {str, Plugin} = {}
        self.threadPool: List[Thread] = []

    def disablePlugin(self, pluginName: str) -> (bool, str):
        """禁用插件"""
        plugin: Plugin = self.pluginDict.get(pluginName)
        plugin.isEnabled = False
        if plugin is None:
            return False, None
        if plugin.DISABLE is not None:
            try:
                plugin.DISABLE()
            except:
                return False, plugin.pluginName
        return True, plugin.pluginName

    def decideEnableOrDisable(self, pluginName: str, switchBtnStatus: bool):
        pluginName = pluginName.replace("switchBtn_", "")
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
        try:
            pathList = next(walk(path))[1]
        except StopIteration:
            return
        for pluginName in pathList:
            try:
                self.loadPlugin(pluginName)
            except Exception as e:
                raise Warning("加载插件错误")

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

    def initSinglePluginsWidget(self, pluginsVerticalLayout: QVBoxLayout):
        """初始化插件页Widget"""
        for pluginName in self.pluginDict.keys():
            plugin: Plugin = self.pluginDict.get(pluginName)
            self.pluginWidget = singlePluginWidget()

            # 设置信息
            self.pluginWidget.pluginName.setText(f"{plugin.pluginName}")
            self.pluginWidget.pluginVer.setText(f"版本:   {plugin.version}")
            self.pluginWidget.pluginAuthor.setText(f"作者:   {plugin.author}")
            self.pluginWidget.pluginTip.setText(f"注释:   {plugin.description}")

            # 设置图标
            if plugin.icon is None:
                self.pluginWidget.pluginIcon.setPixmap(QPixmap(":/built-InIcons/MCSL2.png"))
            elif plugin.icon[0] == ":":
                self.pluginWidget.pluginIcon.setPixmap(QPixmap(plugin.icon))
            else:
                url = ospath.dirname(ospath.abspath(__file__))  # 文件夹
                url = ospath.abspath(ospath.join(url, ".."))
                self.pluginWidget.pluginIcon.setPixmap(
                    QPixmap(f"{url}\\Plugins\\{pluginName}\\{plugin.icon}")
                )
            self.pluginWidget.pluginIcon.setFixedSize(60, 60)
            ASwitchBtn = self.pluginWidget.SwitchButton
            ASwitchBtn.setObjectName(f"switchBtn_{pluginName}")
            pluginVariables.pluginSwitchBtnDict.update({pluginName: ASwitchBtn})

            # 设置槽函数
            ASwitchBtn.selfCheckedChanged.connect(
                lambda instance, checked: self.decideEnableOrDisable(
                    pluginName=instance.objectName(),
                    switchBtnStatus=checked,
                )
            )

            pluginsVerticalLayout.addWidget(self.pluginWidget)

        serversScrollAreaSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        pluginsVerticalLayout.addItem(serversScrollAreaSpacer)

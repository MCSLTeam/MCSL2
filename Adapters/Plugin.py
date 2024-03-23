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
from __future__ import annotations

from json import loads
from os import walk, getcwd, path as osp
from shutil import rmtree
from threading import Thread
from typing import List

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QSpacerItem
from qfluentwidgets import (
    MessageBox,
    LineEdit,
    InfoBar,
    InfoBarPosition,
    FluentIcon as FIF,
    isDarkTheme,
)

from Adapters.BasePlugin import BasePlugin, BasePluginLoader, BasePluginManager
from MCSL2Lib.Resources.icons import *  # noqa: F401 F403
from MCSL2Lib.Widgets.pluginWidget import singlePluginWidget, PluginSwitchButton
from MCSL2Lib.utils import openLocalFile, readFile
from MCSL2Lib.variables import GlobalMCSL2Variables


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


class PluginType:
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
            importedPluginConfig: dict = loads(readFile(f"Plugins//{pluginName}//config.json"))
            importedPlugin.version = importedPluginConfig.get("version")
            importedPlugin.description = importedPluginConfig.get("description")
            importedPlugin.author = importedPluginConfig.get("author")
            importedPlugin.authorEmail = importedPluginConfig.get("author_email")
            if "icon" in importedPluginConfig:
                importedPlugin.icon = importedPluginConfig.get("icon")

        except Exception:
            raise Warning("读取配置错误", pluginName)
        if importedPlugin.__class__.__name__ == Plugin.__name__:
            return importedPlugin
        else:
            return None

    @classmethod
    def getInfo(cls, pluginName: str) -> PluginType:
        pluginType = PluginType()
        pluginType.pluginName = pluginName
        importedPluginConfig: dict = loads(readFile(f"Plugins//{pluginName}//config.json"))
        pluginType.version = importedPluginConfig.get("version")
        pluginType.description = importedPluginConfig.get("description")
        pluginType.author = importedPluginConfig.get("author")
        pluginType.authorEmail = importedPluginConfig.get("author_email")
        if "icon" in importedPluginConfig:
            pluginType.icon = importedPluginConfig.get("icon")

        return pluginType


class PluginManager(BasePluginManager):
    """插件管理器"""

    def __init__(self):
        self.loadedPlugin: {str, Plugin} = {}
        self.allPlugins: {str, PluginType} = {}
        self.threadPool: List[Thread] = []
        self.isDelMsgShowed: int = 0
        self.pluginsScrollAreaSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        self.isOpenedFolder: int = 0

    def disablePlugin(self, pluginName: str) -> (bool, str):
        """禁用插件"""
        plugin: Plugin = self.loadedPlugin.get(pluginName)
        if plugin is None:
            return False, None
        plugin.isEnabled = False
        if plugin.DISABLE is not None:
            try:
                plugin.DISABLE()
            except Exception:
                del self.loadedPlugin[pluginName]
                return False, plugin.pluginName
        del self.loadedPlugin[pluginName]
        return True, plugin.pluginName

    def decideEnableOrDisable(self, pluginButton: PluginSwitchButton, switchBtnStatus: bool):
        pluginName = pluginButton.objectName().replace("switchBtn_", "")
        if switchBtnStatus:
            try:
                self.enablePlugin(pluginName)
            except Warning as e:
                raise Exception(e)
        else:
            self.disablePlugin(pluginName)

    def enablePlugin(self, pluginName: str):
        """启用插件"""
        if self.loadedPlugin.get(pluginName) is not None:
            return True
        plugin: Plugin = self.loadPlugin(pluginName)
        if plugin is None:
            return False
        if plugin.ENABLE is not None:
            try:
                plugin.isEnabled = True
                plugin.ENABLE()
            except Exception:
                raise Warning("未完全卸载", plugin.pluginName)

    def loadPlugin(self, pluginName: str) -> Plugin | None:
        """加载插件但不启用"""
        plugin: Plugin = PluginLoader.load(pluginName)
        plugin.isLoaded = True
        if plugin is None:
            return None
        else:
            if plugin.LOAD is not None:
                plugin.LOAD()
            self.loadedPlugin[pluginName] = plugin
            return plugin

    def readPlugin(self, pluginName: str):
        """读取插件但不启用"""
        plugin: PluginType = PluginLoader.getInfo(pluginName)
        if plugin.pluginName == "":
            self.allPlugins.pop(pluginName)
        else:
            self.allPlugins[pluginName] = plugin

    def readAllPlugins(self, firstLoad):
        """读取所有插件但不启用"""
        path = getcwd() + "\\Plugins"
        try:
            self.pathList = next(walk(path))[1]
            if not firstLoad:
                for i in self.pathListBackup:
                    if i not in self.pathList:
                        self.allPlugins.pop(i)
                        self.pathListBackup.pop(self.pathListBackup.index(i))
                    else:
                        pass
            self.pathListBackup = self.pathList
        except StopIteration:
            return
        for pluginName in self.pathList:
            if pluginName.startswith("__"):
                continue
            try:
                self.readPlugin(pluginName)
            except Exception as e:
                raise Warning(f"加载插件错误: {e}")

    def enableAllPlugins(self):
        """启用所有插件"""
        for pluginName in self.loadedPlugin.keys():
            plugin: Plugin = self.loadedPlugin.get(pluginName)
            if plugin.ENABLE is not None:
                try:
                    self.enablePlugin(pluginName)
                except Exception:
                    continue

    def disableAllPlugins(self):
        """禁用所有插件"""
        self.is_disabled_all = True

    def initSinglePluginsWidget(self, pluginsVerticalLayout: QVBoxLayout):
        """初始化插件页Widget"""
        # 先把旧的清空，但是必须先删除Spacer
        try:
            pluginsVerticalLayout.removeItem(self.pluginsScrollAreaSpacer)
        except Exception:
            pass

        for i in reversed(range(pluginsVerticalLayout.count())):
            pluginsVerticalLayout.itemAt(i).widget().deleteLater()

        for pluginName, plugin in self.allPlugins.items():
            self.pluginWidget = singlePluginWidget(icon=plugin.icon)
            # 设置图标
            if plugin.icon is None:
                # 无图标
                self.pluginWidget.pluginIcon.setPixmap(QPixmap(":/built-InIcons/MCSL2.png"))
            elif plugin.icon[0] == ":":
                # 内置图标
                self.pluginWidget.pluginIcon.setPixmap(QPixmap(plugin.icon))
            elif plugin.icon.startswith("FIF.") or plugin.icon.startswith("FluentIcon."):
                # qfluentwidgets控件库图标
                self.pluginWidget.setPluginIcon(
                    getattr(FIF, plugin.icon.replace("FIF.", "").replace("FluentIcon.", ""))
                )
            else:
                # 文件图标
                url = osp.dirname(osp.abspath(__file__))  # 文件夹
                url = osp.abspath(osp.join(url, ".."))
                self.pluginWidget.pluginIcon.setPixmap(
                    QPixmap(f"{url}\\Plugins\\{pluginName}\\{plugin.icon}")
                )
            self.pluginWidget.pluginIcon.setFixedSize(60, 60)
            self.pluginWidget.SwitchButton.setObjectName(f"switchBtn_{pluginName}")
            self.pluginWidget.openFolderButton.setObjectName(f"openFolderBtn_{pluginName}")
            self.pluginWidget.deleteBtn.setObjectName(f"deleteBtn_{pluginName}")
            self.pluginWidget.setObjectName(f"pluginWidget_{pluginName}")

            # 设置信息
            self.pluginWidget.pluginName.setText(f"{plugin.pluginName}")
            self.pluginWidget.pluginVer.setText(f"版本: {plugin.version}")
            self.pluginWidget.pluginAuthor.setText(f"作者: {plugin.author}")
            self.pluginWidget.pluginTip.setText(f"说明: {plugin.description}")

            # 设置槽函数
            self.pluginWidget.SwitchButton.selfCheckedChanged.connect(
                lambda instance, checked: {
                    self.decideEnableOrDisable(pluginButton=instance, switchBtnStatus=checked),
                }
            )
            self.pluginWidget.openFolderButton.selfClicked.connect(
                lambda instance: openLocalFile(f".\\Plugins\\{instance}\\")
            )
            self.pluginWidget.deleteBtn.selfClicked.connect(
                lambda instance: self.deletePlugin(instance, self.pluginWidget.deleteBtn.window())
            )

            pluginsVerticalLayout.addWidget(self.pluginWidget)

        pluginsVerticalLayout.addItem(self.pluginsScrollAreaSpacer)

    def deletePlugin(self, pluginName, parent):
        if not self.isDelMsgShowed:
            w = MessageBox(
                self.tr(f'你真的要删除插件"{pluginName}"?吗？'),
                self.tr("删除后，这个插件将会消失不见！\n此操作是不可逆的！你确定这么做吗？"),
                parent,
            )
            w.yesButton.setText("取消")
            w.cancelButton.setText("删除")
            w.cancelSignal.connect(lambda: self.deletePluginConfirm(pluginName, parent))
            w.exec()
            self.isDelMsgShowed = 1
        else:
            self.isDelMsgShowed = 0

    def deletePluginConfirm(self, pluginName, parent):
        self.isDelMsgShowed = 0
        title = f'你真的要删除插件"{pluginName}"?'
        content = f'此操作是不可逆的！它会失去很久，很久！\n如果真的要删除，请在下方输入框内输入"{pluginName}"，然后点击“删除”按钮：'  # noqa: E501
        w2 = MessageBox(title, content, parent)
        w2.yesButton.setText(self.tr("取消"))
        w2.cancelButton.setText(self.tr("删除"))
        w2.cancelButton.setStyleSheet(
            GlobalMCSL2Variables.darkWarnBtnStyleSheet
            if isDarkTheme()
            else GlobalMCSL2Variables.lightWarnBtnStyleSheet
        )
        w2.cancelButton.setEnabled(False)
        confirmLineEdit = LineEdit(w2)
        confirmLineEdit.textChanged.connect(
            lambda: self.compareDeletePluginName(
                name=pluginName, LineEditText=confirmLineEdit.text(), parent=parent
            )
        )
        confirmLineEdit.setPlaceholderText(self.tr(f'在此输入"{pluginName}"'))
        parent.deleteBtnEnabled.connect(w2.cancelButton.setEnabled)
        w2.cancelSignal.connect(lambda: self.deletePluginFile(pluginName, parent))
        w2.textLayout.addWidget(confirmLineEdit)
        w2.exec()

    def compareDeletePluginName(self, name, LineEditText, parent):
        parent.deleteBtnEnabled.emit(name == LineEditText)

    def deletePluginFile(self, pluginName, parent):
        if self.disablePlugin(pluginName)[0]:
            rmtree(f"Plugins//{pluginName}")
        else:
            InfoBar.error(
                title="提示",
                content=f"删除插件{pluginName}失败！",
                duration=2000,
                position=InfoBarPosition.BOTTOM_LEFT,
                parent=parent,
            )

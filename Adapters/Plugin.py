from __future__ import annotations
from qfluentwidgets import MessageBox, LineEdit, InfoBar, InfoBarPosition
from json import loads
from os import walk, getcwd, path as ospath, startfile
from threading import Thread
from typing import List
from shutil import rmtree
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QSpacerItem

from Adapters.BasePlugin import BasePlugin, BasePluginLoader, BasePluginManager
from MCSL2Lib.pluginWidget import singlePluginWidget, PluginSwitchButton
from MCSL2Lib.publicFunctions import isDarkTheme
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

    @classmethod
    def getInfo(cls, pluginName: str) -> PluginType:
        pluginType = PluginType()
        pluginType.pluginName = pluginName
        with open(f"Plugins//{pluginName}//config.json", "r", encoding="utf-8") as f:
            importedPluginConfig: dict = loads(f.read())
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

    def disablePlugin(self, pluginName: str) -> (bool, str):
        """禁用插件"""
        plugin: Plugin = self.loadedPlugin.get(pluginName)
        if plugin is None:
            return False, None
        plugin.isEnabled = False
        if plugin.DISABLE is not None:
            try:
                plugin.DISABLE()
            except:
                del self.loadedPlugin[pluginName]
                return False, plugin.pluginName
        del self.loadedPlugin[pluginName]
        return True, plugin.pluginName

    def decideEnableOrDisable(
        self, pluginButton: PluginSwitchButton, switchBtnStatus: bool
    ):
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
            except:
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
        if plugin is None:
            return
        else:
            self.allPlugins[pluginName] = plugin

    def readAllPlugins(self):
        """读取所有插件但不启用"""
        path = getcwd() + "\\Plugins"
        try:
            pathList = next(walk(path))[1]
        except StopIteration:
            return
        for pluginName in pathList:
            # TODO 这里需要更清晰的报错提示
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
                except:
                    continue

    def disableAllPlugins(self):
        """禁用所有插件"""
        self.is_disabled_all = True

    def initSinglePluginsWidget(self, pluginsVerticalLayout: QVBoxLayout):
        """初始化插件页Widget"""
        for pluginName, plugin in self.allPlugins.items():
            self.pluginWidget = singlePluginWidget()

            # 设置信息
            self.pluginWidget.pluginName.setText(f"{plugin.pluginName}")
            self.pluginWidget.pluginVer.setText(f"版本:   {plugin.version}")
            self.pluginWidget.pluginAuthor.setText(f"作者:   {plugin.author}")
            self.pluginWidget.pluginTip.setText(f"注释:   {plugin.description}")

            # 设置图标
            if plugin.icon is None:
                self.pluginWidget.pluginIcon.setPixmap(
                    QPixmap(":/built-InIcons/MCSL2.png")
                )
            elif plugin.icon[0] == ":":
                self.pluginWidget.pluginIcon.setPixmap(QPixmap(plugin.icon))
            else:
                url = ospath.dirname(ospath.abspath(__file__))  # 文件夹
                url = ospath.abspath(ospath.join(url, ".."))
                self.pluginWidget.pluginIcon.setPixmap(
                    QPixmap(f"{url}\\Plugins\\{pluginName}\\{plugin.icon}")
                )
            self.pluginWidget.pluginIcon.setFixedSize(60, 60)
            self.pluginWidget.SwitchButton.setObjectName(f"switchBtn_{pluginName}")
            self.pluginWidget.openFolderButton.setObjectName(
                f"openFolderBtn_{pluginName}"
            )
            self.pluginWidget.deleteBtn.setObjectName(f"deleteBtn_{pluginName}")

            # 设置槽函数
            self.pluginWidget.SwitchButton.selfCheckedChanged.connect(
                lambda instance, checked: {
                    self.decideEnableOrDisable(
                        pluginButton=instance, switchBtnStatus=checked
                    ),
                }
            )
            self.pluginWidget.openFolderButton.selfClicked.connect(
                lambda instance: startfile(f".\\Plugins\\{instance}\\")
            )
            self.pluginWidget.deleteBtn.selfClicked.connect(
                lambda instance: self.deletePlugin(
                    instance, self.pluginWidget.deleteBtn.window()
                )
            )

            pluginsVerticalLayout.addWidget(self.pluginWidget)

        serversScrollAreaSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        pluginsVerticalLayout.addItem(serversScrollAreaSpacer)

    def deletePlugin(self, pluginName, parent):
        if not self.isDelMsgShowed:
            w = MessageBox(
                f'你真的要删除插件"{pluginName}"?吗？', "删除后，这个插件将会消失不见！\n此操作是不可逆的！你确定这么做吗？", parent
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
        content = f'此操作是不可逆的！它会失去很久，很久！\n如果真的要删除，请在下方输入框内输入"{pluginName}"，然后点击“删除”按钮：'
        w2 = MessageBox(title, content, parent)
        w2.yesButton.setText("取消")
        w2.cancelButton.setText("删除")
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
        confirmLineEdit.setPlaceholderText(f'在此输入"{pluginName}"')
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

#     Copyright 2023, MCSL Team, mailto:lxhtz.dl@qq.com
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
"""
The main window of MCSL2.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QApplication
from qfluentwidgets import (
    NavigationBar,
    NavigationItemPosition,
    isDarkTheme,
    FluentIcon as FIF,
    Theme,
    setTheme,
    setThemeColor,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    HyperlinkButton,
)
from qframelesswindow import FramelessWindow, TitleBar

from Adapters.Plugin import PluginManager
from MCSL2Lib.interfaceController import StackedWidget
from MCSL2Lib.homePage import HomePage
from MCSL2Lib.configurePage import ConfigurePage
from MCSL2Lib.serverManagerPage import ServerManagerPage
from MCSL2Lib.downloadPage import DownloadPage
from MCSL2Lib.consolePage import ConsolePage
from MCSL2Lib.pluginPage import PluginPage
from MCSL2Lib.settingsPage import SettingsPage
from MCSL2Lib.selectJavaPage import SelectJavaPage
from MCSL2Lib.selectNewJavaPage import SelectNewJavaPage
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import (
    ConfigureServerVariables,
    EditServerVariables,
    GlobalMCSL2Variables,
    PluginVariables,
    ServerVariables,
)
from MCSL2Lib import icons as _  # noqa: F401
from MCSL2Lib.settingsController import SettingsController
from MCSL2Lib.serverController import (
    MinecraftServerResMonitorThread,
    MojangEula,
    ServerHandler,
    ServerHelper,
    ServerLauncher,
)
from MCSL2Lib.publicFunctions import openWebUrl

serverVariables = ServerVariables()
settingsController = SettingsController()
configureServerVariables = ConfigureServerVariables()
editServerVariables = EditServerVariables()
serverHelper = ServerHelper()
pluginVariables = PluginVariables()


class CustomTitleBar(TitleBar):
    """标题栏"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # 图标
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 20)
        self.hBoxLayout.insertWidget(
            1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter
        )
        self.window().windowIconChanged.connect(self.setIcon)

        # 标题
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(
            2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter
        )
        self.titleLabel.setObjectName("titleLabel")
        self.window().windowTitleChanged.connect(self.setTitle)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))

    def resizeEvent(self, e):
        pass


@Singleton
class Window(FramelessWindow):
    """程序主窗口"""

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        # 读取程序设置，不放在第一位就会爆炸！
        settingsController._readSettings(firstLoad=True)

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self.stackWidget = StackedWidget(self)

        # 定义子页面
        self.homeInterface = HomePage()
        self.configureInterface = ConfigurePage()
        self.downloadInterface = DownloadPage()
        self.consoleInterface = ConsolePage()
        self.pluginsInterface = PluginPage()
        self.settingsInterface = SettingsPage()
        self.serverManagerInterface = ServerManagerPage()

        # 定义隐藏的子页面
        self.selectJavaPage = SelectJavaPage()
        self.selectNewJavaPage = SelectNewJavaPage()  # 草泥马摆烂偷懒！！！好好好！！！CV大法嘎嘎好！

        # 设置主题
        configThemeList = ["auto", "dark", "light"]
        qfluentwidgetsThemeList = [Theme.AUTO, Theme.DARK, Theme.LIGHT]
        setTheme(
            qfluentwidgetsThemeList[
                configThemeList.index(settingsController.fileSettings["theme"])
            ]
        )
        setThemeColor(str(settingsController.fileSettings["themeColor"]))

        self.initLJQtSlot()

        self.initLayout()

        self.initNavigation()

        self.initWindow()

        serverHelper.loadAtLaunch()

        self.initPluginSystem()

    def initPluginSystem(self):
        """初始化插件系统"""
        pluginManager: PluginManager = pluginVariables.pluginManager
        pluginManager.loadAllPlugins()
        pluginManager.initSinglePluginsWidget(self.pluginsInterface.pluginsVerticalLayout)

    def switchTo(self, widget):
        """换页"""
        self.stackWidget.setCurrentWidget(widget)

    def initLayout(self):
        """初始化布局"""
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationBar)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        """初始化导航栏"""
        self.addSubInterface(
            self.homeInterface, FIF.HOME, "主页", selectedIcon=FIF.HOME_FILL
        )
        self.addSubInterface(self.configureInterface, FIF.ADD_TO, "新建")
        self.addSubInterface(self.serverManagerInterface, FIF.LIBRARY, "管理")
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, "下载")
        self.addSubInterface(self.consoleInterface, FIF.ALIGNMENT, "终端")
        self.addSubInterface(self.pluginsInterface, FIF.APPLICATION, "插件")
        self.addSubInterface(
            self.settingsInterface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM
        )

        self.stackWidget.addWidget(self.selectJavaPage)
        self.stackWidget.addWidget(self.selectNewJavaPage)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.navigationBar.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        """初始化窗口"""
        self.setWindowIcon(QIcon(":/built-InIcons/MCSL2.png"))
        self.setWindowTitle(f"MCSL {GlobalMCSL2Variables.MCSL2Version}")
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.resize(w // 2, h // 2)
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setQss()

    def addSubInterface(
        self,
        interface,
        icon,
        text: str,
        position=NavigationItemPosition.TOP,
        selectedIcon=None,
    ):
        """添加子页面"""
        self.stackWidget.addWidget(interface)
        self.navigationBar.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            selectedIcon=selectedIcon,
            position=position,
        )

    def setQss(self):
        """设置Qss"""
        color = "dark" if isDarkTheme() else "light"
        with open(f"resource/{color}/demo.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def onCurrentInterfaceChanged(self, index):
        """导航栏触发器"""
        widget = self.stackWidget.widget(index)
        self.navigationBar.setCurrentItem(widget.objectName())

    def initLJQtSlot(self):
        """定义无法直接设置的Qt信号槽"""

        # 新建服务器
        self.configureInterface.noobDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.configureInterface.noobDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(1)
        )
        self.configureInterface.noobDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: InfoBar.info(
                title="切换到MCSLAPI",
                content="因为FastMirror没有Java啊 (",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        )
        self.configureInterface.extendedDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.configureInterface.extendedDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(1)
        )
        self.configureInterface.extendedDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: InfoBar.info(
                title="切换到MCSLAPI",
                content="因为FastMirror没有Java啊 (",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        )
        self.configureInterface.noobDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.configureInterface.noobDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(
                self.settingsInterface.downloadSourceList.index(
                    settingsController.fileSettings["downloadSource"]
                )
            )
        )
        self.configureInterface.extendedDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.configureInterface.extendedDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(
                self.settingsInterface.downloadSourceList.index(
                    settingsController.fileSettings["downloadSource"]
                )
            )
        )
        self.selectJavaPage.backBtn.clicked.connect(
            lambda: self.switchTo(self.configureInterface)
        )
        self.configureInterface.noobJavaListPushBtn.clicked.connect(
            lambda: self.switchTo(self.selectJavaPage)
        )
        self.configureInterface.noobJavaListPushBtn.clicked.connect(
            lambda: self.selectJavaPage.refreshPage(configureServerVariables.javaPath)
        )
        self.configureInterface.extendedJavaListPushBtn.clicked.connect(
            lambda: self.switchTo(self.selectJavaPage)
        )
        self.configureInterface.extendedJavaListPushBtn.clicked.connect(
            lambda: self.selectJavaPage.refreshPage(configureServerVariables.javaPath)
        )
        self.selectJavaPage.setJavaVer.connect(self.configureInterface.setJavaVer)
        self.selectJavaPage.setJavaPath.connect(self.configureInterface.setJavaPath)

        # 主页
        self.homeInterface.newServerBtn.clicked.connect(
            lambda: self.switchTo(self.configureInterface)
        )
        self.homeInterface.selectServerBtn.clicked.connect(
            lambda: self.switchTo(self.serverManagerInterface)
        )
        self.homeInterface.selectServerBtn.clicked.connect(
            self.serverManagerInterface.refreshServers
        )
        serverHelper.serverName.connect(self.homeInterface.afterSelectedServer)
        serverHelper.backToHomePage.connect(lambda: self.switchTo(self.homeInterface))
        serverHelper.startBtnStat.connect(self.homeInterface.startServerBtn.setEnabled)
        self.homeInterface.startServerBtn.clicked.connect(self.startServer)

        # 设置
        self.settingsInterface.selectThemeColorBtn.colorChanged.connect(setThemeColor)

        # 管理服务器
        self.stackWidget.currentChanged.connect(
            self.serverManagerInterface.onPageChangedRefresh
        )
        self.serverManagerInterface.editDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.serverManagerInterface.editDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(1)
        )
        self.serverManagerInterface.editDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: InfoBar.info(
                title="切换到MCSLAPI",
                content="因为FastMirror没有Java啊 (",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        )
        self.serverManagerInterface.editJavaListPushBtn.clicked.connect(
            lambda: self.switchTo(self.selectNewJavaPage)
        )
        self.serverManagerInterface.editJavaListPushBtn.clicked.connect(
            lambda: self.selectNewJavaPage.refreshPage(editServerVariables.javaPath)
        )
        self.serverManagerInterface.editDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.serverManagerInterface.editDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(
                self.settingsInterface.downloadSourceList.index(
                    settingsController.fileSettings["downloadSource"]
                )
            )
        )
        self.selectNewJavaPage.backBtn.clicked.connect(
            lambda: self.switchTo(self.serverManagerInterface)
        )
        self.selectNewJavaPage.setJavaPath.connect(
            self.serverManagerInterface.setJavaPath
        )

        # 终端
        ServerHandler().serverLogOutput.connect(
            self.consoleInterface.colorConsoleText
        )
        self.consoleInterface.sendCommandButton.clicked.connect(
            lambda: self.sendCommand(
                command=self.consoleInterface.commandLineEdit.text()
            )
        )
        if settingsController.fileSettings["clearConsoleWhenStopServer"]:
            ServerHandler().AServer.serverProcess.finished.connect(
                lambda: self.consoleInterface.serverOutput.setPlainText("")
            )

    def startServer(self):
        """启动服务器总函数，直接放这里得了"""
        firstTry = ServerLauncher().startServer()
        if not firstTry:
            w = MessageBox(
                title="提示",
                content="你并未同意Minecraft的最终用户许可协议。\n未同意，服务器将无法启动。\n可点击下方的按钮查看Eula。\n同意Eula后，请尝试再次开启服务器",
                parent=self,
            )
            w.yesButton.setText("同意")
            w.yesButton.clicked.connect(lambda: MojangEula().acceptEula())
            w.cancelButton.setText("拒绝")
            eulaBtn = HyperlinkButton()
            eulaBtn.setText("Eula")
            eulaBtn.clicked.connect(lambda: openWebUrl(MojangEula().eulaURL))
            w.buttonLayout.addWidget(eulaBtn, 1, Qt.AlignVCenter)
            w.exec()
        else:
            self.switchTo(self.consoleInterface)
            self.consoleInterface.serverOutput.setPlainText("")
            self.serverMemThread = MinecraftServerResMonitorThread(self)
            self.serverMemThread.memPercent.connect(self.consoleInterface.setMemView)
            self.serverMemThread.cpuPercent.connect(self.consoleInterface.setCPUView)
            ServerHandler().serverClosed.connect(
                lambda: self.serverMemThread.terminate()
            )
            self.serverMemThread.start()

    def sendCommand(self, command):
        if ServerHandler().isServerRunning():
            ServerHandler().sendCommand(command=command)
            self.consoleInterface.commandLineEdit.clear()
        else:
            w = MessageBox(
                title="失败",
                content="服务器并未开启，请先开启服务器。",
                parent=self,
            )
            w.yesButton.setText("好")
            w.cancelButton.setParent(None)
            w.exec()

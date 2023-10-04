#     Copyright 2023, MCSL Team, mailto:lxhtt@vip.qq.com
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
import sys
from traceback import format_exception
from types import TracebackType
from typing import Type
from platform import system
from PyQt5.QtCore import (
    QEvent,
    QObject,
    Qt,
    QTimer,
    pyqtSlot,
    QSize,
    pyqtSignal,
    QThread,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from qfluentwidgets import (
    NavigationItemPosition,
    FluentIcon as FIF,
    Theme,
    setTheme,
    setThemeColor,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    HyperlinkButton,
    FluentWindow,
    SplashScreen,
)
from Adapters.Plugin import PluginManager
from MCSL2Lib import MCSL2VERSION
from MCSL2Lib.Controllers.aria2ClientController import (
    Aria2Controller,
    initializeAria2Configuration,
    Aria2BootThread,
)
from MCSL2Lib.Controllers.serverController import (
    MinecraftServerResMonitorUtil,
    MojangEula,
    ServerHandler,
    ServerHelper,
    ServerLauncher,
)
from MCSL2Lib.Controllers.settingsController import SettingsController
from MCSL2Lib.utils import MCSL2Logger
from MCSL2Lib.Pages.configurePage import ConfigurePage
from MCSL2Lib.Pages.consolePage import ConsolePage
from MCSL2Lib.Pages.downloadPage import DownloadPage
from MCSL2Lib.Pages.homePage import HomePage
from MCSL2Lib.Pages.pluginPage import PluginPage
from MCSL2Lib.Pages.selectJavaPage import SelectJavaPage
from MCSL2Lib.Pages.selectNewJavaPage import SelectNewJavaPage
from MCSL2Lib.Pages.serverManagerPage import ServerManagerPage
from MCSL2Lib.Pages.settingsPage import SettingsPage
from MCSL2Lib.Resources.icons import *  # noqa: F401
from MCSL2Lib.Widgets.exceptionWidget import ExceptionWidget
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.utils import (
    isDarkTheme,
    exceptionFilter,
    ExceptionFilterMode,
    workingThreads,
)
from platform import version as systemVersion
from MCSL2Lib.variables import (
    ConfigureServerVariables,
    EditServerVariables,
    GlobalMCSL2Variables,
    ServerVariables,
    SettingsVariables,
)

serverVariables = ServerVariables()
settingsController = SettingsController()
configureServerVariables = ConfigureServerVariables()
editServerVariables = EditServerVariables()
serverHelper = ServerHelper()
settingsVariables = SettingsVariables()


pageLoadConfig = [
    {"type": HomePage, "targetObj": "homeInterface", "flag": "homeInterfaceLoaded"},
    {
        "type": ConsolePage,
        "targetObj": "consoleInterface",
        "flag": "consoleInterfaceLoaded",
    },
    {
        "type": PluginPage,
        "targetObj": "pluginsInterface",
        "flag": "pluginsInterfaceLoaded",
    },
    {
        "type": SettingsPage,
        "targetObj": "settingsInterface",
        "flag": "settingsInterfaceLoaded",
    },
    {
        "type": ServerManagerPage,
        "targetObj": "serverManagerInterface",
        "flag": "serverManagerInterfaceLoaded",
    },
    {
        "type": SelectNewJavaPage,
        "targetObj": "selectNewJavaPage",
        "flag": "selectNewJavaPageLoaded",
    },
    {
        "type": SelectJavaPage,
        "targetObj": "selectJavaPage",
        "flag": "selectJavaPageLoaded",
    },
    {
        "type": DownloadPage,
        "targetObj": "downloadInterface",
        "flag": "downloadInterfaceLoaded",
    },
    {
        "type": ConfigurePage,
        "targetObj": "configureInterface",
        "flag": "configureInterfaceLoaded",
    },
]


class InterfaceLoaded(QObject):
    homeInterfaceLoaded = False
    configureInterfaceLoaded = False
    downloadInterfaceLoaded = False
    consoleInterfaceLoaded = False
    pluginsInterfaceLoaded = False
    settingsInterfaceLoaded = False
    serverManagerInterfaceLoaded = False
    selectJavaPageLoaded = False
    selectNewJavaPageLoaded = False

    initNavigationFinished = False
    initQtSlotFinished = False
    initPluginSystemFinished = False

    mainWindowInited = False

    def canInitNavigation(self):
        return (
            self.homeInterfaceLoaded
            and self.configureInterfaceLoaded
            and self.downloadInterfaceLoaded
            and self.consoleInterfaceLoaded
            and self.pluginsInterfaceLoaded
            and self.settingsInterfaceLoaded
            and self.serverManagerInterfaceLoaded
        )

    def canInitQtSlot(self):
        return (
            self.configureInterfaceLoaded
            and self.selectJavaPageLoaded
            and self.homeInterfaceLoaded
            and self.serverManagerInterfaceLoaded
            and self.consoleInterfaceLoaded
            and self.selectNewJavaPageLoaded
            and self.downloadInterfaceLoaded
        )

    def canInitPluginSystem(self):
        return self.pluginsInterfaceLoaded

    def allPageLoaded(self):
        return (
            self.homeInterfaceLoaded
            and self.configureInterfaceLoaded
            and self.downloadInterfaceLoaded
            and self.consoleInterfaceLoaded
            and self.pluginsInterfaceLoaded
            and self.settingsInterfaceLoaded
            and self.serverManagerInterfaceLoaded
            and self.selectJavaPageLoaded
            and self.selectNewJavaPageLoaded
        )


loaded = InterfaceLoaded()


class PageLoader(QThread):
    loadFinished = pyqtSignal(object, str, str)

    def __init__(
        self, pageType: Type[QWidget], targetObj: str, flag: str, callback=None
    ):
        super().__init__()
        self.pageType = pageType
        self.targetObj = targetObj
        self.flag = flag
        self.page = None
        self.loadFinished.connect(callback)

    def run(self) -> None:
        # 强行切换上下文,留给UI线程进行刷新
        self.yieldCurrentThread()
        self.loadFinished.emit(self.pageType, self.targetObj, self.flag)


@Singleton
class Window(FluentWindow):
    """程序主窗口"""

    deleteBtnEnabled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        # 读取程序设置，不放在第一位就会爆炸！
        settingsController.initialize(firstLoad=True)
        self.mySetTheme()
        self.initWindow()
        self.setWindowTitle(f"MCSL {MCSL2VERSION}")
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        self.oldHook = sys.excepthook
        self.pluginManager: PluginManager = PluginManager()

        # if experiment := settingsController.fileSettings.get(
        #     "enableExperimentalFeatures", False
        # ):
        #     MCSL2Logger.warning(f"实验性功能已设置为{experiment}")

        self.homeInterface = None  # type: HomePage
        self.configureInterface = None  # type: ConfigurePage
        self.downloadInterface = None  # type: DownloadPage
        self.consoleInterface = None  # type: ConsolePage
        self.pluginsInterface = None  # type: PluginPage
        self.settingsInterface = None  # type: SettingsPage
        self.serverManagerInterface = None  # type: ServerManagerPage
        self.selectJavaPage = None  # type: SelectJavaPage
        self.selectNewJavaPage = None  # type: SelectNewJavaPage

        # 页面加载器
        loaders = []
        for config in pageLoadConfig:
            loader = PageLoader(
                config["type"],
                config["targetObj"],
                config["flag"],
                self.onPageLoaded,
            )
            loaders.append(loader)

        for loader in loaders:
            loader.start()

        initializeAria2Configuration()

        self.initSafeQuitController()

        loaded.mainWindowInited = True
        GlobalMCSL2Variables.isLoadFinished = (
            False if not loaded.allPageLoaded() else True
        )

    @pyqtSlot(object, str, str)
    def onPageLoaded(self, pageType, targetObj, flag):
        setattr(self, targetObj, pageType(self))
        setattr(loaded, flag, True)
        if loaded.allPageLoaded():
            self.initNavigation()
            serverHelper.loadAtLaunch()
            self.initQtSlot()
            self.initPluginSystem()
            if settingsController.fileSettings["checkUpdateOnStart"]:
                self.settingsInterface.checkUpdate(parent=self)
            self.consoleInterface.installEventFilter(self)
            sys.excepthook = self.catchExceptions
            self.startAria2Client()
            self.splashScreen.finish()
            self.splashScreen.deleteLater()
            self.update()

    @pyqtSlot(bool)
    def onAria2Loaded(self, flag: bool):
        if flag:
            InfoBar.success(
                title="Aria2下载引擎启动成功。",
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        else:
            InfoBar.error(
                title="Aria2下载引擎启动失败",
                content="请检查是否安装了Aria2。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def closeEvent(self, a0) -> None:
        if ServerHandler().isServerRunning():
            box = MessageBox("是否退出MCSL2？", "服务器正在运行。\n\n请在退出前先关闭服务器。", parent=self)
            box.yesButton.setText("取消")
            box.cancelButton.setText("安全关闭并退出")
            box.cancelButton.setStyleSheet(
                GlobalMCSL2Variables.darkWarnBtnStyleSheet
                if isDarkTheme()
                else GlobalMCSL2Variables.lightWarnBtnStyleSheet
            )
            if box.exec() == 1:
                a0.ignore()
                return

            process = ServerHandler().Server.serverProcess
            process.finished.connect(self.close)
            process.write(b"stop\n")
            self.exitingMsgBox.show()
            self.quitTimer.start()

            a0.ignore()
            return
        try:
            workingThreads.closeAllThreads()
            if Aria2Controller.shutDown():
                super().closeEvent(a0)
        finally:
            super().closeEvent(a0)

    def onForceExit(self):
        process = ServerHandler().Server.serverProcess
        process.kill()

    def catchExceptions(
        self, ty: Type[BaseException], value: BaseException, _traceback: TracebackType
    ):
        """
        全局捕获异常，并弹窗显示
        :param ty: 异常的类型
        :param value: 异常的对象
        :param _traceback: 异常的traceback
        """
        # 过滤部分异常
        mode = exceptionFilter(ty, value, _traceback)

        if mode == ExceptionFilterMode.PASS:
            MCSL2Logger.info(f"忽略了异常：{ty} {value} {_traceback}")
            return

        elif mode == ExceptionFilterMode.RAISE:
            MCSL2Logger.error(f"捕捉到异常：{ty} {value} {_traceback}")
            return self.oldHook(ty, value, _traceback)

        elif mode == ExceptionFilterMode.RAISE_AND_PRINT:
            tracebackString = "".join(format_exception(ty, value, _traceback))
            exceptionWidget = ExceptionWidget(tracebackString)
            box = MessageBox("程序出现异常", "", self)
            box.yesButton.setText("确认并复制到剪切板")
            box.cancelButton.setText("知道了")
            box.contentLabel.deleteLater()
            box.textLayout.addWidget(exceptionWidget.exceptionScrollArea)
            box.yesSignal.connect(
                lambda: QApplication.clipboard().setText(tracebackString)
            )
            box.yesSignal.connect(exceptionWidget.deleteLater)
            box.cancelSignal.connect(exceptionWidget.deleteLater)
            box.exec()
            return self.oldHook(ty, value, _traceback)

    def initPluginSystem(self, firstLoad=True):
        """初始化插件系统"""
        self.pluginManager.readAllPlugins(firstLoad)
        self.pluginManager.initSinglePluginsWidget(
            self.pluginsInterface.pluginsVerticalLayout
        )

    def initNavigation(self):
        """初始化导航栏"""
        self.addSubInterface(self.homeInterface, FIF.HOME, "主页")
        self.addSubInterface(self.configureInterface, FIF.ADD_TO, "新建")
        self.addSubInterface(self.serverManagerInterface, FIF.LIBRARY, "管理")
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, "下载")
        self.addSubInterface(self.consoleInterface, FIF.COMMAND_PROMPT, "终端")
        self.addSubInterface(self.pluginsInterface, FIF.APPLICATION, "插件")
        self.navigationInterface.addSeparator()
        self.navigationInterface.setExpandWidth(200)
        self.addSubInterface(
            self.settingsInterface,
            FIF.SETTING,
            "设置",
            position=NavigationItemPosition.BOTTOM,
        )

        self.stackedWidget.addWidget(self.selectJavaPage)
        self.stackedWidget.addWidget(self.selectNewJavaPage)

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        """初始化窗口"""

        self.setWindowIcon(QIcon(":/built-InIcons/MCSL2.png"))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.resize(w // 2, int(h // 1.5))
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def mySetTheme(self):
        setTheme(Theme.DARK if isDarkTheme() else Theme.LIGHT)
        if "windows" in system().lower():
            if int(systemVersion().split(".")[-1]) >= 22000:
                self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())
            else:
                self.windowEffect.setAcrylicEffect(
                    self.winId(),
                    gradientColor="F2F2F2" if isDarkTheme() else "F2F2F299",
                )
        setThemeColor(str(settingsController.fileSettings["themeColor"]))

    def initSafeQuitController(self):
        # 安全退出控件
        self.exitingMsgBox = MessageBox(
            "正在退出MCSL2", "安全关闭服务器中...\n\nMCSL2稍后将自行退出。", parent=self
        )
        self.exitingMsgBox.cancelButton.hide()
        self.exitingMsgBox.yesButton.setText("强制结束服务器并退出")
        self.exitingMsgBox.yesButton.setStyleSheet(
            GlobalMCSL2Variables.darkWarnBtnStyleSheet
            if isDarkTheme()
            else GlobalMCSL2Variables.lightWarnBtnStyleSheet
        )
        self.exitingMsgBox.yesButton.clicked.connect(self.onForceExit)
        self.exitingMsgBox.yesButton.setEnabled(False)
        self.exitingMsgBox.hide()
        self.quitTimer = QTimer(self)
        self.quitTimer.setInterval(3000)
        self.quitTimer.timeout.connect(
            lambda: self.exitingMsgBox.yesButton.setEnabled(True)
        )

    def initQtSlot(self):
        """定义无法直接设置的Qt信号槽"""

        # 新建服务器
        self.configureInterface.noobDownloadJavaPrimaryPushBtn.clicked.connect(
            self.downloadInterface.getMCSLAPI
        )
        self.configureInterface.noobDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(1)
        )
        self.configureInterface.noobDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.configureInterface.noobDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(1)
        )
        self.configureInterface.extendedDownloadJavaPrimaryPushBtn.clicked.connect(
            self.downloadInterface.getMCSLAPI
        )
        self.configureInterface.extendedDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(1)
        )
        self.configureInterface.extendedDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.configureInterface.extendedDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(1)
        )
        self.configureInterface.noobDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.configureInterface.noobDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(
                settingsVariables.downloadSourceList.index(
                    settingsController.fileSettings["downloadSource"]
                )
            )
        )
        self.configureInterface.extendedDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.configureInterface.extendedDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(
                settingsVariables.downloadSourceList.index(
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

        # 设置器
        serverHelper.startBtnStat.connect(self.settingsRunner_autoRunLastServer)
        # 管理服务器
        self.serverManagerInterface.editDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(1)
        )
        self.serverManagerInterface.editDownloadJavaPrimaryPushBtn.clicked.connect(
            self.downloadInterface.getMCSLAPI
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
        self.serverManagerInterface.editDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
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
                settingsVariables.downloadSourceList.index(
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
        ServerHandler().serverLogOutput.connect(self.consoleInterface.colorConsoleText)
        if settingsController.fileSettings["clearConsoleWhenStopServer"]:
            ServerHandler().serverClosed.connect(
                lambda: self.consoleInterface.serverOutput.setPlainText("")
            )

        # 性能优化
        self.stackedWidget.currentChanged.connect(
            self.serverManagerInterface.onPageChangedRefresh
        )
        self.stackedWidget.currentChanged.connect(
            self.downloadInterface.onPageChangedRefresh
        )
        self.stackedWidget.currentChanged.connect(
            self.settingsInterface.onPageChangedRefresh
        )

    def startServer(self):
        """启动服务器总函数，直接放这里得了"""
        firstTry = ServerLauncher().startServer()
        if not firstTry:
            w = MessageBox(
                title="提示",
                content="你并未同意Minecraft的最终用户许可协议。\n未同意，服务器将无法启动。\n可点击下方的按钮查看Eula。\n同意Eula后，服务器将会启动。",
                parent=self,
            )
            w.yesButton.setText("同意")
            w.yesSignal.connect(MojangEula().acceptEula)
            w.yesSignal.connect(self.startServer)
            w.cancelButton.setText("拒绝")
            eulaBtn = HyperlinkButton(
                url="https://aka.ms/MinecraftEULA", text="Eula", icon=FIF.LINK
            )
            w.buttonLayout.addWidget(eulaBtn, 1, Qt.AlignVCenter)
            w.exec()
        else:
            self.switchTo(self.consoleInterface)
            self.navigationInterface.setCurrentItem(self.consoleInterface.objectName())
            self.consoleInterface.serverOutput.setPlainText("")
            self.serverMemThread = MinecraftServerResMonitorUtil(self)
            self.serverMemThread.memPercent.connect(self.consoleInterface.setMemView)
            self.serverMemThread.cpuPercent.connect(self.consoleInterface.setCPUView)
            try:
                self.consoleInterface.exitServer.clicked.disconnect()
            except TypeError:
                pass
            ServerHandler().serverClosed.connect(
                self.serverMemThread.onServerClosedHandler
            )
            ServerHandler().serverClosed.connect(
                self.consoleInterface.exitServer.clicked.disconnect
            )
            ServerHandler().serverClosed.connect(
                lambda: self.consoleInterface.exitServer.clicked.connect(
                    self.homeInterface.startServerBtn.click
                )
            )
            ServerHandler().serverClosed.connect(
                lambda: self.consoleInterface.exitServer.setText("开启服务器")
            )
            self.consoleInterface.exitServer.clicked.connect(
                self.consoleInterface.runQuickMenu_StopServer
            )
            self.consoleInterface.exitServer.setText("关闭服务器")
            GlobalMCSL2Variables.isLoadFinished = True

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if not GlobalMCSL2Variables.isLoadFinished:
            return super().eventFilter(a0, a1)

        if a0 == self.consoleInterface and a1.type() == QEvent.KeyPress:
            if a1.key() == Qt.Key_Return or a1.key() == Qt.Key_Enter:
                if (
                    self.stackedWidget.view.currentIndex() == 4
                    and self.consoleInterface.commandLineEdit
                ):
                    self.consoleInterface.sendCommandButton.click()
                    return True
            elif a1.key() == Qt.Key_Up:
                if (
                    self.stackedWidget.view.currentIndex() == 4
                    and self.consoleInterface.commandLineEdit
                ):
                    if len(
                        GlobalMCSL2Variables.userCommandHistory
                    ) and GlobalMCSL2Variables.upT > -len(
                        GlobalMCSL2Variables.userCommandHistory
                    ):
                        GlobalMCSL2Variables.upT -= 1
                        lastCommand = GlobalMCSL2Variables.userCommandHistory[
                            GlobalMCSL2Variables.upT
                        ]
                        self.consoleInterface.commandLineEdit.setText(lastCommand)
                        return True
            elif a1.key() == Qt.Key_Down:
                if (
                    self.stackedWidget.view.currentIndex() == 4
                    and self.consoleInterface.commandLineEdit
                ):
                    if (
                        len(GlobalMCSL2Variables.userCommandHistory)
                        and GlobalMCSL2Variables.upT < 0
                    ):
                        GlobalMCSL2Variables.upT += 1
                        nextCommand = GlobalMCSL2Variables.userCommandHistory[
                            GlobalMCSL2Variables.upT
                        ]
                        self.consoleInterface.commandLineEdit.setText(nextCommand)
                        return True
                    if (
                        len(GlobalMCSL2Variables.userCommandHistory)
                        and GlobalMCSL2Variables.upT == 0
                    ):
                        self.consoleInterface.commandLineEdit.setText("")
                        return True
        return super().eventFilter(a0, a1)

    def startAria2Client(self):
        bootThread = Aria2BootThread(self)
        bootThread.loaded.connect(self.onAria2Loaded)
        bootThread.finished.connect(bootThread.deleteLater)
        bootThread.finished.connect(self.splashScreen.finish)
        bootThread.start()

    @pyqtSlot(bool)
    def settingsRunner_autoRunLastServer(self, startBtnStat):
        """设置：启动时自动运行上次运行的服务器"""
        if settingsController.fileSettings["autoRunLastServer"]:
            if startBtnStat:
                InfoBar.info(
                    title="MCSL2功能提醒",
                    content="您开启了“启动时自动运行上次运行的服务器”功能。\n正在启动上次运行的服务器...",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.homeInterface,
                )
                self.homeInterface.startServerBtn.click()
                InfoBar.info(
                    title="功能提醒",
                    content="您开启了“启动时自动运行上次运行的服务器”功能。\n正在启动上次运行的服务器...",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.consoleInterface,
                )
            else:
                InfoBar.info(
                    title="功能提醒",
                    content="虽然您开启了“启动时自动运行上次运行的服务器”功能，\n但由于上次开启记录不存在，或上次开启的服务器已被删除，\n无法启动服务器。\n您仍然可以手动开启服务器。",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.homeInterface,
                )

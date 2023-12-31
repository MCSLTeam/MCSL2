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
from platform import system
from platform import version as systemVersion
from traceback import format_exception
from types import TracebackType
from typing import Type
from PyQt5.QtCore import (
    Qt,
    QTimer,
    pyqtSlot,
    QSize,
    pyqtSignal,
    QThreadPool,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (
    NavigationItemPosition,
    FluentIcon as FIF,
    setTheme,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    SplashScreen,
    isDarkTheme,
)
from Adapters.Plugin import PluginManager
from MCSL2Lib import MCSL2VERSION
from MCSL2Lib.ProgramControllers.aria2ClientController import (
    Aria2Controller,
    initializeAria2Configuration,
    Aria2BootThread,
)
from MCSL2Lib.ProgramControllers.settingsController import cfg
from MCSL2Lib.Pages.configurePage import ConfigurePage
from MCSL2Lib.Pages.consoleCenterPage import ConsoleCenterPage
from MCSL2Lib.Pages.downloadPage import DownloadPage
from MCSL2Lib.Pages.homePage import HomePage
from MCSL2Lib.Pages.pluginPage import PluginPage
from MCSL2Lib.Pages.selectJavaPage import SelectJavaPage
from MCSL2Lib.Pages.selectNewJavaPage import SelectNewJavaPage
from MCSL2Lib.Pages.serverManagerPage import ServerManagerPage
from MCSL2Lib.Pages.settingsPage import SettingsPage
from MCSL2Lib.Resources.icons import *  # noqa: F401 F403
from MCSL2Lib.Widgets.exceptionWidget import ExceptionWidget
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.utils import MCSL2Logger
from MCSL2Lib.utils import (
    exceptionFilter,
    ExceptionFilterMode,
    workingThreads,
)
from MCSL2Lib.variables import (
    ConfigureServerVariables,
    EditServerVariables,
    GlobalMCSL2Variables,
    ServerVariables,
    SettingsVariables,
)

try:
    from MCSL2Lib.verification import VerifyFluentWindowBase
except Exception:
    from qfluentwidgets import FluentWindow as VerifyFluentWindowBase


serverVariables = ServerVariables()
configureServerVariables = ConfigureServerVariables()
editServerVariables = EditServerVariables()
settingsVariables = SettingsVariables()

# pageLoadConfig = [
#     {"type": HomePage, "targetObj": "homeInterface", "flag": "homeInterfaceLoaded"},
#     {
#         "type": ConsoleCenterPage,
#         "targetObj": "consoleInterface",
#         "flag": "consoleInterfaceLoaded",
#     },
#     {
#         "type": PluginPage,
#         "targetObj": "pluginsInterface",
#         "flag": "pluginsInterfaceLoaded",
#     },
#     {
#         "type": SettingsPage,
#         "targetObj": "settingsInterface",
#         "flag": "settingsInterfaceLoaded",
#     },
#     {
#         "type": ServerManagerPage,
#         "targetObj": "serverManagerInterface",
#         "flag": "serverManagerInterfaceLoaded",
#     },
#     {
#         "type": SelectNewJavaPage,
#         "targetObj": "selectNewJavaPage",
#         "flag": "selectNewJavaPageLoaded",
#     },
#     {
#         "type": SelectJavaPage,
#         "targetObj": "selectJavaPage",
#         "flag": "selectJavaPageLoaded",
#     },
#     {
#         "type": DownloadPage,
#         "targetObj": "downloadInterface",
#         "flag": "downloadInterfaceLoaded",
#     },
#     {
#         "type": ConfigurePage,
#         "targetObj": "configureInterface",
#         "flag": "configureInterfaceLoaded",
#     },
# ]


# class InterfaceLoaded(QObject):
#     homeInterfaceLoaded = False
#     configureInterfaceLoaded = False
#     downloadInterfaceLoaded = False
#     consoleInterfaceLoaded = False
#     pluginsInterfaceLoaded = False
#     settingsInterfaceLoaded = False
#     serverManagerInterfaceLoaded = False
#     selectJavaPageLoaded = False
#     selectNewJavaPageLoaded = False

#     initNavigationFinished = False
#     initQtSlotFinished = False
#     initPluginSystemFinished = False

#     mainWindowInited = False

#     # def canInitNavigation(self):
#     #     return (
#     #         self.homeInterfaceLoaded
#     #         and self.configureInterfaceLoaded
#     #         and self.downloadInterfaceLoaded
#     #         and self.consoleInterfaceLoaded
#     #         and self.pluginsInterfaceLoaded
#     #         and self.settingsInterfaceLoaded
#     #         and self.serverManagerInterfaceLoaded
#     #     )

#     # def canInitQtSlot(self):
#     #     return (
#     #         self.configureInterfaceLoaded
#     #         and self.selectJavaPageLoaded
#     #         and self.homeInterfaceLoaded
#     #         and self.serverManagerInterfaceLoaded
#     #         and self.consoleInterfaceLoaded
#     #         and self.selectNewJavaPageLoaded
#     #         and self.downloadInterfaceLoaded
#     #     )

#     # def canInitPluginSystem(self):
#     #     return self.pluginsInterfaceLoaded

#     def allPageLoaded(self):
#         return (
#             self.homeInterfaceLoaded
#             and self.configureInterfaceLoaded
#             and self.downloadInterfaceLoaded
#             and self.consoleInterfaceLoaded
#             and self.pluginsInterfaceLoaded
#             and self.settingsInterfaceLoaded
#             and self.serverManagerInterfaceLoaded
#             and self.selectJavaPageLoaded
#             and self.selectNewJavaPageLoaded
#         )


# loaded = InterfaceLoaded()


# class PageLoader(QThread):
#     loadFinished = pyqtSignal(object, str, str)

#     def __init__(self, pageType: Type[QWidget], targetObj: str, flag: str, callback=None):
#         super().__init__()
#         self.pageType = pageType
#         self.targetObj = targetObj
#         self.flag = flag
#         self.page = None
#         self.loadFinished.connect(callback)

#     def run(self) -> None:
#         # 强行切换上下文,留给UI线程进行刷新
#         self.yieldCurrentThread()
#         self.loadFinished.emit(self.pageType, self.targetObj, self.flag)


@Singleton
class Window(VerifyFluentWindowBase):
    """程序主窗口"""

    startFetchingNotice = pyqtSignal()
    deleteBtnEnabled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.testMode = False
        self.mySetTheme()
        self.initWindow()
        self.setWindowTitle(f"MCServerLauncher {MCSL2VERSION}{' 测试版' if self.testMode else ''}")

        self.oldHook = sys.excepthook
        sys.excepthook = self.catchExceptions
        self.pluginManager: PluginManager = PluginManager()

        # if experiment := cfg.get(
        #     "enableExperimentalFeatures", False
        # ):
        #     MCSL2Logger.warning(f"实验性功能已设置为{experiment}")

        # self.homeInterface = None  # type: HomePage
        # self.configureInterface = None  # type: ConfigurePage
        # self.downloadInterface = None  # type: DownloadPage
        # self.consoleInterface = None  # type: ConsoleCenterPage
        # self.pluginsInterface = None  # type: PluginPage
        # self.settingsInterface = None  # type: SettingsPage
        # self.serverManagerInterface = None  # type: ServerManagerPage
        # self.selectJavaPage = None  # type: SelectJavaPage
        # self.selectNewJavaPage = None  # type: SelectNewJavaPage
        self.homeInterface = HomePage(self)
        self.configureInterface = ConfigurePage(self)
        self.downloadInterface = DownloadPage(self)
        self.consoleInterface = ConsoleCenterPage(self)
        self.pluginsInterface = PluginPage(self)
        self.settingsInterface = SettingsPage(self)
        self.serverManagerInterface = ServerManagerPage(self)
        self.selectJavaPage = SelectJavaPage(self)
        self.selectNewJavaPage = SelectNewJavaPage(self)

        # # 页面加载器
        # loaders = []
        # for config in pageLoadConfig:
        #     loader = PageLoader(
        #         config["type"],
        #         config["targetObj"],
        #         config["flag"],
        #         self.onPageLoaded,
        #     )
        #     loaders.append(loader)

        # for loader in loaders:
        #     loader.start()

        initializeAria2Configuration()

        self.initSafeQuitController()

        # loaded.mainWindowInited = True
        # GlobalMCSL2Variables.isLoadFinished = False if not loaded.allPageLoaded() else True

        self.startFetchingNotice.connect(self.homeInterface.noticeThread.start)
        self.initNavigation()
        self.initQtSlot()
        self.initPluginSystem()
        if cfg.get(cfg.checkUpdateOnStart):
            self.settingsInterface.checkUpdate(parent=self)
        self.consoleInterface.installEventFilter(self)
        self.startAria2Client()
        self.splashScreen.finish()
        self.update()
        if self.testMode:
            self.testVerifyBox.show()
            self.navigationInterface.setEnabled(False)
            self.stackedWidget.setEnabled(False)
        else:
            self.testNotPassFlag = False
            pass
        self.startFetchingNotice.emit()

    @pyqtSlot(bool)
    def onAria2Loaded(self, flag: bool):
        if flag:
            InfoBar.success(
                title=self.tr("Aria2下载引擎启动成功。"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        else:
            InfoBar.error(
                title=self.tr("Aria2下载引擎启动失败"),
                content=self.tr("请检查是否安装了Aria2。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        self.startFetchingNotice.emit()

    def closeEvent(self, a0) -> None:
        if ServerHandler().isServerRunning():
            box = MessageBox(
                self.tr("是否退出MCSL2？"),
                self.tr("服务器正在运行。\n\n请在退出前先关闭服务器。"),
                parent=self,
            )
            box.yesButton.setText(self.tr("取消"))
            box.cancelButton.setText(self.tr("安全关闭并退出"))
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

        # close thread pool
        QThreadPool.globalInstance().clear()
        QThreadPool.globalInstance().waitForDone()
        QThreadPool.globalInstance().deleteLater()

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
            MCSL2Logger.error(msg=f"捕捉到异常：{ty} {value} {_traceback}")
            return self.oldHook(ty, value, _traceback)

        elif mode == ExceptionFilterMode.RAISE_AND_PRINT:
            tracebackString = "".join(format_exception(ty, value, _traceback))
            MCSL2Logger.error(msg=tracebackString)
            exceptionWidget = ExceptionWidget(tracebackString)
            box = MessageBox(self.tr("程序出现异常"), "", self)
            box.yesButton.setText(self.tr("确认并复制到剪切板"))
            box.cancelButton.setText(self.tr("知道了"))
            box.contentLabel.setParent(None)
            box.contentLabel.deleteLater()
            del box.contentLabel
            box.textLayout.addWidget(exceptionWidget.exceptionScrollArea)
            box.yesSignal.connect(lambda: QApplication.clipboard().setText(tracebackString))
            box.yesSignal.connect(box.deleteLater)
            box.cancelSignal.connect(box.deleteLater)
            box.yesSignal.connect(exceptionWidget.deleteLater)
            box.cancelSignal.connect(exceptionWidget.deleteLater)
            box.exec()
            return self.oldHook(ty, value, _traceback)

    def initPluginSystem(self, firstLoad=True):
        """初始化插件系统"""
        self.pluginManager.readAllPlugins(firstLoad)
        self.pluginManager.initSinglePluginsWidget(self.pluginsInterface.pluginsVerticalLayout)

    def initNavigation(self):
        """初始化导航栏"""
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr("主页"))
        self.addSubInterface(self.configureInterface, FIF.ADD_TO, self.tr("新建"))
        self.addSubInterface(self.serverManagerInterface, FIF.LIBRARY, self.tr("管理"))
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, self.tr("下载"))
        self.addSubInterface(self.consoleInterface, FIF.ROBOT, self.tr("监控"))
        self.addSubInterface(self.pluginsInterface, FIF.APPLICATION, self.tr("插件"))
        self.navigationInterface.addSeparator()
        self.navigationInterface.setExpandWidth(200)
        self.addSubInterface(
            self.settingsInterface,
            FIF.SETTING,
            self.tr("设置"),
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
        self.resize(int(w // 1.5), int(h // 1.5))
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def mySetTheme(self):
        if "windows" in system().lower():
            if int(systemVersion().split(".")[-1]) >= 22000:
                self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())
            else:
                pass
        setTheme(cfg.theme)
        # setThemeColor(cfg.get(cfg.themeColor))

    def initSafeQuitController(self):
        # 安全退出控件
        self.exitingMsgBox = MessageBox(
            self.tr("正在退出MCSL2"),
            self.tr("安全关闭服务器中...\n\nMCSL2稍后将自行退出。"),
            parent=self,
        )
        self.exitingMsgBox.cancelButton.hide()
        self.exitingMsgBox.yesButton.setText(self.tr("强制结束服务器并退出"))
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
        self.quitTimer.timeout.connect(lambda: self.exitingMsgBox.yesButton.setEnabled(True))

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
                settingsVariables.downloadSourceList.index(cfg.get(cfg.downloadSource))
            )
        )
        self.configureInterface.extendedDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )
        self.configureInterface.extendedDownloadCorePrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(
                settingsVariables.downloadSourceList.index(cfg.get(cfg.downloadSource))
            )
        )
        self.selectJavaPage.backBtn.clicked.connect(lambda: self.switchTo(self.configureInterface))
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
        self.homeInterface.downloadBtn.clicked.connect(
            lambda: self.switchTo(self.downloadInterface)
        )

        # 管理服务器
        self.serverManagerInterface.editDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: self.downloadInterface.downloadStackedWidget.setCurrentIndex(1)
        )
        self.serverManagerInterface.editDownloadJavaPrimaryPushBtn.clicked.connect(
            self.downloadInterface.getMCSLAPI
        )
        self.serverManagerInterface.editDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: InfoBar.info(
                title=self.tr("切换到MCSLAPI"),
                content=self.tr("因为FastMirror没有Java啊 ("),
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
                settingsVariables.downloadSourceList.index(cfg.get(cfg.downloadSource))
            )
        )
        self.selectNewJavaPage.backBtn.clicked.connect(
            lambda: self.switchTo(self.serverManagerInterface)
        )
        self.selectNewJavaPage.setJavaPath.connect(self.serverManagerInterface.setJavaPath)

        # fmt: off
        self.pluginsInterface.refreshPluginListBtn.clicked.connect(self.initPluginSystem)
        self.stackedWidget.currentChanged.connect(self.serverManagerInterface.onPageChangedRefresh)
        self.stackedWidget.currentChanged.connect(self.downloadInterface.onPageChangedRefresh)
        # fmt: on

    def startAria2Client(self):
        bootThread = Aria2BootThread(self)
        bootThread.loaded.connect(self.onAria2Loaded)
        bootThread.finished.connect(bootThread.deleteLater)
        bootThread.finished.connect(self.splashScreen.finish)
        bootThread.start()

    # @pyqtSlot(bool)
    # def settingsRunner_autoRunLastServer(self, startBtnStat):
    #     """设置：启动时自动运行上次运行的服务器"""
    #     if cfg.get(cfg.autoRunLastServer):
    #         if startBtnStat:
    #             InfoBar.info(
    #                 title=self.tr("MCSL2功能提醒"),
    #                 content=self.tr(
    #                     "您开启了“启动时自动运行上次运行的服务器”功能。\n正在启动上次运行的服务器..."
    #                 ),
    #                 orient=Qt.Horizontal,
    #                 isClosable=True,
    #                 position=InfoBarPosition.TOP,
    #                 duration=3000,
    #                 parent=self.homeInterface,
    #             )
    #             self.homeInterface.startServerBtn.click()
    #             InfoBar.info(
    #                 title=self.tr("功能提醒"),
    #                 content=self.tr(
    #                     "您开启了“启动时自动运行上次运行的服务器”功能。\n正在启动上次运行的服务器..."
    #                 ),
    #                 orient=Qt.Horizontal,
    #                 isClosable=True,
    #                 position=InfoBarPosition.TOP,
    #                 duration=3000,
    #                 parent=self.consoleInterface,
    #             )
    #         else:
    #             InfoBar.info(
    #                 title=self.tr("功能提醒"),
    #                 content=self.tr(
    #                     "虽然您开启了“启动时自动运行上次运行的服务器”功能，\n但由于上次开启记录不存在，或上次开启的服务器已被删除，\n无法启动服务器。\n您仍然可以手动开启服务器。"
    #                 ),
    #                 orient=Qt.Horizontal,
    #                 isClosable=True,
    #                 position=InfoBarPosition.TOP,
    #                 duration=3000,
    #                 parent=self.homeInterface,
    #             )

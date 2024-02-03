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
    Dialog,
    SplashScreen,
    isDarkTheme,
)
from Adapters.Plugin import PluginManager
from MCSL2Lib import DEV_VERSION, MCSL2VERSION
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


@Singleton
class Window(VerifyFluentWindowBase):
    """程序主窗口"""

    deleteBtnEnabled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.previewFlag = False
        self.mySetTheme()
        self.initWindow()
        self.setWindowTitle(
            f"MCServerLauncher {MCSL2VERSION}{' 测试版 ' if self.previewFlag else ''}{DEV_VERSION if self.previewFlag else ''}"  # noqa: E501
        )

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
        self.consoleCenterInterface = ConsoleCenterPage(self)
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
        self.homeInterface.noticeThread.start()
        initializeAria2Configuration()
        # loaded.mainWindowInited = True
        # GlobalMCSL2Variables.isLoadFinished = False if not loaded.allPageLoaded() else True

        self.initNavigation()
        self.initQtSlot()
        self.initPluginSystem()
        if cfg.get(cfg.checkUpdateOnStart):
            self.settingsInterface.checkUpdate(parent=self)
        self.startAria2Client()
        self.splashScreen.finish()
        self.update()
        if self.previewFlag:
            self.passSignal.connect(lambda: self.homeInterface.setEnabled(True))
            self.passSignal.connect(lambda: self.configureInterface.setEnabled(True))
            self.passSignal.connect(lambda: self.downloadInterface.setEnabled(True))
            self.passSignal.connect(lambda: self.consoleCenterInterface.setEnabled(True))
            self.passSignal.connect(lambda: self.pluginsInterface.setEnabled(True))
            self.passSignal.connect(lambda: self.settingsInterface.setEnabled(True))
            self.passSignal.connect(lambda: self.serverManagerInterface.setEnabled(True))
            self.passSignal.connect(lambda: self.selectJavaPage.setEnabled(True))
            self.passSignal.connect(lambda: self.selectNewJavaPage.setEnabled(True))
            self.testVerifyBox.show()
            self.navigationInterface.setEnabled(False)
            self.stackedWidget.setEnabled(False)
            self.homeInterface.setEnabled(False)
            self.configureInterface.setEnabled(False)
            self.downloadInterface.setEnabled(False)
            self.consoleCenterInterface.setEnabled(False)
            self.pluginsInterface.setEnabled(False)
            self.settingsInterface.setEnabled(False)
            self.serverManagerInterface.setEnabled(False)
            self.selectJavaPage.setEnabled(False)
            self.selectNewJavaPage.setEnabled(False)
        else:
            self.testNotPassFlag = False
            pass

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

    def closeEvent(self, a0) -> None:
        if self.consoleCenterInterface.isAnyServerRunning():
            box = MessageBox(
                self.tr("现在你无法退出MCSL2"),
                self.tr("仍有服务器正在运行。\n请在退出前关闭所有服务器。"),
                parent=self,
            )
            box.yesButton.setText(self.tr("了解"))
            box.cancelButton.setParent(None)
            box.cancelButton.deleteLater()
            box.exec_()
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
            box = Dialog(
                self.tr("MCSL2 发生未经处理的异常"),
                content=self.tr("如果有能力可自行解决，无法解决请积极反馈！"),
                parent=None,
            )
            box.titleBar.show()
            box.setTitleBarVisible(False)
            box.yesButton.setText(self.tr("确认并复制到剪切板"))
            box.cancelButton.setText(self.tr("知道了"))
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
        self.navigationInterface.setExpandWidth(170)
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr("主页"))
        self.addSubInterface(self.configureInterface, FIF.ADD_TO, self.tr("新建"))
        self.addSubInterface(self.serverManagerInterface, FIF.LIBRARY, self.tr("管理"))
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, self.tr("下载"))
        self.addSubInterface(self.consoleCenterInterface, FIF.ROBOT, self.tr("监控"))
        self.addSubInterface(self.pluginsInterface, FIF.APPLICATION, self.tr("插件"))
        self.navigationInterface.addSeparator()
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
        setTheme(cfg.theme, lazy=True)
        # setThemeColor(cfg.get(cfg.themeColor), lazy=True)

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

        self.serverManagerInterface.runningServerCardGenerated.connect(
            self.consoleCenterInterface.addRunningCard
        )

    def startAria2Client(self):
        bootThread = Aria2BootThread(self)
        bootThread.loaded.connect(self.onAria2Loaded)
        bootThread.finished.connect(bootThread.deleteLater)
        bootThread.finished.connect(self.splashScreen.finish)
        bootThread.start()

#     Copyright 2023, MCSL Team, mailto:lxhtt@mcsl.com.cn
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

from PyQt5.QtCore import QEvent, QObject, Qt, QThread, QTimer
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
from MCSL2Lib import icons as _  # noqa: F401
from MCSL2Lib.configurePage import ConfigurePage
from MCSL2Lib.consolePage import ConsolePage
from MCSL2Lib.downloadPage import DownloadPage
from MCSL2Lib.homePage import HomePage
from MCSL2Lib.interfaceController import StackedWidget
from MCSL2Lib.pluginPage import PluginPage
from MCSL2Lib.publicFunctions import openWebUrl
from MCSL2Lib.selectJavaPage import SelectJavaPage
from MCSL2Lib.selectNewJavaPage import SelectNewJavaPage
from MCSL2Lib.serverController import (
    MinecraftServerResMonitorThread,
    MojangEula,
    ServerHandler,
    ServerHelper,
    ServerLauncher,
)
from MCSL2Lib.serverManagerPage import ServerManagerPage
from MCSL2Lib.settingsController import SettingsController
from MCSL2Lib.settingsPage import SettingsPage
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import (
    ConfigureServerVariables,
    EditServerVariables,
    GlobalMCSL2Variables,
    PluginVariables,
    ServerVariables,
)

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


class CloseServerThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        try:
            pass
        finally:
            pass


class ExitAndCloseServerMsgBox(MessageBox):
    def __init__(self, title: str, content: str, *args, **kwargs):
        super().__init__(title, content, *args, **kwargs)
        self.closeThread = CloseServerThread(self.parent())
        self.closeThread.finished.connect(self.close)

    def exec(self) -> int:
        self.closeThread.start()
        return super().exec()


@Singleton
class Window(FramelessWindow):
    """程序主窗口"""

    def __init__(self):
        super().__init__()
        self.oldHook = sys.excepthook
        sys.excepthook = self.catchExceptions

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
        # 注册快捷键
        self.consoleInterface.installEventFilter(self)

        self.exitingMsgBox = MessageBox("正在关闭", "正在关闭服务器,稍后将退出", parent=self)
        # 安全退出控件
        self.exitingMsgBox.setModal(True)
        self.exitingMsgBox.cancelButton.hide()
        self.exitingMsgBox.yesButton.setText("强制退出")
        self.exitingMsgBox.yesButton.clicked.connect(self.onForceExit)
        self.exitingMsgBox.yesButton.setEnabled(False)
        self.exitingMsgBox.hide()
        self.quitTimer = QTimer(self)
        self.quitTimer.setInterval(3000)
        self.quitTimer.timeout.connect(
            lambda: self.exitingMsgBox.yesButton.setEnabled(True)
        )

    def closeEvent(self, a0) -> None:
        if ServerHandler().isServerRunning():
            box = MessageBox("进程退出", "服务器正在运行，退出前请关闭服务器", parent=self)
            box.yesButton.setText("取消")
            box.cancelButton.setText("关闭并退出")
            if box.exec() == 1:
                a0.ignore()
                return

            self.serverMemThread.quit()
            process = ServerHandler().Server.serverProcess
            process.finished.connect(self.close)
            process.write(b"stop\n")
            self.exitingMsgBox.show()
            self.quitTimer.start()

            a0.ignore()
            return
        a0.accept()

    def onForceExit(self):
        process = ServerHandler().Server.serverProcess
        process.kill()

    def catchExceptions(self, ty, value, _traceback):
        """
        全局捕获异常，并弹窗显示
        :param ty: 异常的类型
        :param value: 异常的对象
        :param _traceback: 异常的traceback
        """
        tracebackFormat = format_exception(ty, value, _traceback)
        tracebackString = "".join(tracebackFormat)
        box = MessageBox("程序出现异常", tracebackString, parent=self)
        box.yesButton.setText("确认并复制到剪切板")
        if box.exec() == 1:
            QApplication.clipboard().setText(tracebackString)
        self.oldHook(ty, value, _traceback)

    def initPluginSystem(self):
        """初始化插件系统"""
        pluginManager: PluginManager = PluginManager()
        pluginManager.loadAllPlugins()
        pluginManager.initSinglePluginsWidget(
            self.pluginsInterface.pluginsVerticalLayout
        )

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
        ServerHandler().serverLogOutput.connect(self.consoleInterface.colorConsoleText)
        if settingsController.fileSettings["clearConsoleWhenStopServer"]:
            ServerHandler().AServer.serverProcess.finished.connect(
                lambda: self.consoleInterface.serverOutput.setPlainText("")
            )

        # 下载
        self.stackWidget.currentChanged.connect(
            self.downloadInterface.onPageChangedRefresh
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
            w.yesSignal.connect(lambda: MojangEula().acceptEula())
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

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a0 == self.consoleInterface and a1.type() == QEvent.KeyPress:
            if a1.key() == Qt.Key_Return or a1.key() == Qt.Key_Enter:
                if (
                    self.stackWidget.view.currentIndex() == 4
                    and self.consoleInterface.commandLineEdit
                ):
                    self.consoleInterface.sendCommandButton.click()
                    return True
            if a1.key() == Qt.Key_Up:
                if (
                    self.stackWidget.view.currentIndex() == 4
                    and self.consoleInterface.commandLineEdit
                ):
                    if (
                        GlobalMCSL2Variables.userCommandHistory != []
                        and GlobalMCSL2Variables.upT
                        > -len(GlobalMCSL2Variables.userCommandHistory)
                    ):
                        lastCommand = GlobalMCSL2Variables.userCommandHistory[
                            GlobalMCSL2Variables.upT - 1
                        ]
                        GlobalMCSL2Variables.upT -= 1
                        self.consoleInterface.commandLineEdit.setText(lastCommand)
                        return True
            if a1.key() == Qt.Key_Down:
                if (
                    self.stackWidget.view.currentIndex() == 4
                    and self.consoleInterface.commandLineEdit
                ):
                    if (
                        GlobalMCSL2Variables.userCommandHistory != []
                        and GlobalMCSL2Variables.upT
                        < 0
                    ):
                        nextCommand = GlobalMCSL2Variables.userCommandHistory[
                            GlobalMCSL2Variables.upT + 1
                        ]
                        GlobalMCSL2Variables.upT += 1
                        self.consoleInterface.commandLineEdit.setText(nextCommand)
                        return True
                    if (
                        GlobalMCSL2Variables.userCommandHistory != []
                        and GlobalMCSL2Variables.upT
                        == 0
                    ):
                        self.consoleInterface.commandLineEdit.setText("")
                        return True
        print(GlobalMCSL2Variables.userCommandHistory)
        print(GlobalMCSL2Variables.upT)
        return super().eventFilter(a0, a1)

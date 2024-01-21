from PyQt5.QtCore import (
    Qt,
    QSize,
    QRect,
    QEvent,
    QObject,
    pyqtSignal,
    pyqtSlot,
    QTimer,
)
from PyQt5.QtWidgets import (
    QSizePolicy,
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QFrame,
    QLayout,
    QLabel,
    QCompleter,
    QApplication,
    QFileDialog,
    QFileSystemModel,
)
from qfluentwidgets import (
    HyperlinkButton,
    MessageBox,
    ComboBox,
    LineEdit,
    ListWidget,
    TreeView,
    TabBar,
    PlainTextEdit,
    PrimaryPushButton,
    PrimaryToolButton,
    ProgressRing,
    PushButton,
    SegmentedWidget,
    SimpleCardWidget,
    StrongBodyLabel,
    SubtitleLabel,
    SwitchButton,
    ToggleButton,
    TransparentPushButton,
    VerticalSeparator,
    FluentIcon as FIF,
    ToolTip,
    isDarkTheme,
    InfoBarPosition,
    InfoBar,
    TabCloseButtonDisplayMode,
)
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from PyQt5.QtGui import QIcon, QCursor, QColor, QPainter, QTextCharFormat, QBrush
from qframelesswindow import TitleBar
from MCSL2Lib.ProgramControllers.interfaceController import EraseStackedWidget, MySmoothScrollArea
from MCSL2Lib.Resources.icons import *  # noqa: F401 F403
from MCSL2Lib.ProgramControllers.settingsController import cfg
from MCSL2Lib.ServerControllers.processCreator import _MinecraftEULA, ServerLauncher
from MCSL2Lib.ServerControllers.serverErrorHandler import ServerErrorHandler
from MCSL2Lib.ServerControllers.serverUtils import (
    MinecraftServerResMonitorUtil,
    readServerProperties,
    backupServer,
    backupSaves,
)
from os import path as osp
import sys
from re import search
from typing import Dict
from MCSL2Lib.Widgets.playersControllerMainWidget import playersController
from MCSL2Lib.utils import MCSL2Logger, openLocalFile
from MCSL2Lib.variables import GlobalMCSL2Variables, ServerVariables


class ErrorHandlerToggleButton(ToggleButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        self.tip = ToolTip("已开启")
        self.toggled.connect(self.toggleToolTip)

    def toggleToolTip(self):
        if self.isChecked():
            self.tip = ToolTip("已开启")
        else:
            self.tip = ToolTip("已关闭")

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a1.type() == QEvent.ToolTip:
            self.tip.move(QCursor.pos())
            self.tip.show()
            return True
        if a1.type() == QEvent.Leave:
            self.tip.hide()
            return True
        return super().eventFilter(a0, a1)


class ServerWindowTitleBar(TitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.placeholderLabel = QLabel(self)
        self.placeholderLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertWidget(0, self.placeholderLabel, 0, Qt.AlignRight | Qt.AlignVCenter)

        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
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
        if isDarkTheme():
            self.setStyleSheet(
                """
                    ServerWindowTitleBar>QLabel#titleLabel {
                        color: white;
                        background: transparent;
                        font: 13px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                        padding: 0 4px
                    }
                    MinimizeButton {
                        qproperty-normalColor: white;
                        qproperty-normalBackgroundColor: transparent;
                        qproperty-hoverColor: white;
                        qproperty-hoverBackgroundColor: rgba(255, 255, 255, 26);
                        qproperty-pressedColor: white;
                        qproperty-pressedBackgroundColor: rgba(255, 255, 255, 51)
                    }


                    MaximizeButton {
                        qproperty-normalColor: white;
                        qproperty-normalBackgroundColor: transparent;
                        qproperty-hoverColor: white;
                        qproperty-hoverBackgroundColor: rgba(255, 255, 255, 26);
                        qproperty-pressedColor: white;
                        qproperty-pressedBackgroundColor: rgba(255, 255, 255, 51)
                    }

                    CloseButton {
                        qproperty-normalColor: white;
                        qproperty-normalBackgroundColor: transparent;
                    }
                """
            )
        else:
            self.setStyleSheet(
                """
                ServerWindowTitleBar>QLabel#titleLabel {
                    color: black;
                    background: transparent;
                    font: 13px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                    padding: 0 4px
                }


                MinimizeButton {
                    qproperty-normalColor: black;
                    qproperty-normalBackgroundColor: transparent;
                    qproperty-hoverColor: black;
                    qproperty-hoverBackgroundColor: rgba(0, 0, 0, 26);
                    qproperty-pressedColor: black;
                    qproperty-pressedBackgroundColor: rgba(0, 0, 0, 51)
                }


                MaximizeButton {
                    qproperty-normalColor: black;
                    qproperty-normalBackgroundColor: transparent;
                    qproperty-hoverColor: black;
                    qproperty-hoverBackgroundColor: rgba(0, 0, 0, 26);
                    qproperty-pressedColor: black;
                    qproperty-pressedBackgroundColor: rgba(0, 0, 0, 51)
                }

                CloseButton {
                    qproperty-normalColor: black;
                    qproperty-normalBackgroundColor: transparent;
                }
                """
            )

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class ServerWindow(BackgroundAnimationWidget, FramelessWindow):
    playersControllerBtnEnabled = pyqtSignal(bool)

    def __init__(
        self,
        config: ServerVariables,
        launcher: ServerLauncher,
        manageBtn: PrimaryPushButton,
        manageBackupBtn: PushButton,
    ):
        self._isMicaEnabled = False
        super().__init__()
        self.errMsg = ""
        self.configEditorContainerDict: Dict[QWidget] = {}
        self.configEditorDict: Dict[PlainTextEdit] = {}
        self.playersList = []
        self.playersControllerBtnEnabled.emit(False)
        self.serverConfig = config
        self.serverLauncher = launcher
        self.serverBridge = None
        self.monitorWidget = None
        self.manageBtn = manageBtn
        self.manageBtn.setEnabled(False)
        self.manageBtn.setText("已开启")
        self.manageBackupBtn = manageBackupBtn
        self.manageBackupBtn.setEnabled(False)
        self.initWindow()
        self.setupInterface()
        self.setupOverviewPage()
        self.setupCommandPage()
        self.setupEditorPage()
        self.setupScheduleTasksPage()
        self.setupAnalyzePage()
        self.initTexts()
        self.initNavigation()
        self.stackedWidget.setCurrentIndex(0)
        self.setObjectName("serverWindow")
        cfg.themeChangedFinished.connect(self._onThemeChangedFinished)
        self.setMicaEffectEnabled(True)
        self.initSlots()
        self.startServer()
        self.initSafelyQuitController()

    def closeEvent(self, a0) -> None:
        if self.serverBridge.isServerRunning():
            box = MessageBox(
                self.tr("是否关闭此窗口？"),
                self.tr("服务器正在运行，请在退出前先关闭服务器。"),
                parent=self,
            )
            box.yesButton.setText(self.tr("取消"))
            box.cancelButton.setText(self.tr("关闭并退出"))
            box.cancelButton.setStyleSheet(
                GlobalMCSL2Variables.darkWarnBtnStyleSheet
                if isDarkTheme()
                else GlobalMCSL2Variables.lightWarnBtnStyleSheet
            )
            if box.exec() == 1:
                a0.ignore()
                return

            self.serverBridge.serverProcess.process.finished.connect(self.close)
            self.stopServer(forceNoErrorHandler=True)
            self.exitingMsgBox.show()
            self.quitTimer.start()
            try:
                self.monitorWidget.setParent(None)
            except Exception:
                pass

            a0.ignore()
            return
        else:
            try:
                self.monitorWidget.setParent(None)
            except Exception:
                pass
            self.manageBtn.setEnabled(True)
            self.manageBackupBtn.setEnabled(True)
            self.manageBtn.setText("启动")

        super().closeEvent(a0)

    def genRunScript(self, save=False):
        script = (
            f"cd \"{osp.abspath('Servers' + self.serverConfig.serverName)}\"\n"
            + self.serverConfig.javaPath
            + " "
            + " ".join(self.serverLauncher.jvmArg)
        )
        if save:
            return script
        else:
            (w := MessageBox("生成启动脚本", "", parent=self)).contentLabel.setParent(None)
            w.yesButton.setText("保存")
            w.yesSignal.connect(self.saveRunScript)
            (copyWidget := QWidget()).setLayout((cmdLayout := QHBoxLayout()))

            copyBtn = PushButton(icon=FIF.COPY, text="复制", parent=w)
            copyBtn.setFixedHeight(200)
            copyBtn.clicked.connect(lambda: QApplication.clipboard().setText(script))
            copyBtn.clicked.connect(
                lambda: InfoBar.success(
                    "已复制",
                    "",
                    orient=Qt.Horizontal,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                    duration=1500,
                    parent=self,
                )
            )

            textEdit = PlainTextEdit(parent=w)
            textEdit.setReadOnly(True)
            textEdit.setPlainText(script)
            textEdit.setFixedSize(QSize(400, 200))

            cmdLayout.addWidget(textEdit, 0, Qt.AlignRight)
            cmdLayout.addWidget(copyBtn, 1, Qt.AlignRight)
            w.textLayout.addWidget(copyWidget)
            w.show()

    def saveRunScript(self):
        with open(
            file=QFileDialog.getSaveFileName(
                self,
                f"MCSL2服务器 - {self.serverConfig.serverName} 保存启动脚本",
                f"Run {self.serverConfig.serverName}.bat",
                "Batch(*.bat);;Shell(*.sh)",
            )[0],
            mode="w+",
            encoding="utf-8",
        ) as script:
            script.write(self.genRunScript(save=True))

    def initSafelyQuitController(self):
        # 安全退出控件
        self.exitingMsgBox = MessageBox(
            self.tr(f"安全关闭服务器“{self.serverConfig.serverName}”中..."),
            "稍安勿躁。如果长时间没有反应，请尝试强制关闭服务器。",
            parent=self,
        )
        self.exitingMsgBox.cancelButton.hide()
        self.exitingMsgBox.yesButton.setText(self.tr("强制结束服务器"))
        self.exitingMsgBox.yesButton.setStyleSheet(
            GlobalMCSL2Variables.darkWarnBtnStyleSheet
            if isDarkTheme()
            else GlobalMCSL2Variables.lightWarnBtnStyleSheet
        )
        self.exitingMsgBox.yesButton.clicked.connect(self.serverBridge.serverProcess.process.kill)
        self.exitingMsgBox.yesButton.setEnabled(False)
        self.exitingMsgBox.hide()
        self.quitTimer = QTimer(self)
        self.quitTimer.setInterval(4500)
        self.quitTimer.timeout.connect(lambda: self.exitingMsgBox.yesButton.setEnabled(True))

    def setupInterface(self):
        self.gridLayout = QGridLayout(self)

        self.serverSegmentedWidget = SegmentedWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverSegmentedWidget.sizePolicy().hasHeightForWidth())
        self.serverSegmentedWidget.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.serverSegmentedWidget, 1, 1, 1, 2)
        spacerItem = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 2)
        self.stackedWidget = EraseStackedWidget(self)

    def setupOverviewPage(self):
        self.overviewPage = QWidget()
        self.overviewPage.setObjectName("overviewPage")
        self.overviewPageLayout = QGridLayout(self.overviewPage)
        self.overviewSeparator = VerticalSeparator(self.overviewPage)
        self.overviewSeparator.setMinimumSize(QSize(5, 0))
        self.overviewSeparator.setMaximumSize(QSize(5, 16777215))
        self.overviewPageLayout.addWidget(self.overviewSeparator, 0, 1, 7, 1)
        self.backupServerBtn = PushButton(self.overviewPage)
        self.backupServerBtn.setFixedSize(QSize(160, 32))
        self.overviewPageLayout.addWidget(self.backupServerBtn, 2, 2, 1, 1)
        self.toggleServerBtn = PrimaryPushButton(self.overviewPage)
        self.toggleServerBtn.setFixedSize(QSize(160, 32))
        self.overviewPageLayout.addWidget(self.toggleServerBtn, 4, 2, 1, 1)
        self.genRunScriptBtn = PushButton(self.overviewPage)
        self.genRunScriptBtn.setFixedSize(QSize(160, 32))
        self.overviewPageLayout.addWidget(self.genRunScriptBtn, 3, 2, 1, 1)
        self.openServerFolder = PushButton(self.overviewPage)
        self.openServerFolder.setFixedSize(QSize(160, 32))
        self.overviewPageLayout.addWidget(self.openServerFolder, 0, 2, 1, 1)
        self.backupSavesBtn = PushButton(self.overviewPage)
        self.backupSavesBtn.setFixedSize(QSize(160, 32))
        self.overviewPageLayout.addWidget(self.backupSavesBtn, 1, 2, 1, 1)
        self.overviewScrollArea = MySmoothScrollArea(self.overviewPage)
        self.overviewScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.overviewScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.overviewScrollArea.setWidgetResizable(True)
        self.overviewScrollArea.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.overviewScrollArea.setMinimumWidth(320)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 491, 575))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.serverResMonitorTitle = SubtitleLabel(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverResMonitorTitle.sizePolicy().hasHeightForWidth())
        self.serverResMonitorTitle.setSizePolicy(sizePolicy)
        self.verticalLayout_3.addWidget(self.serverResMonitorTitle)
        self.serverResMonitorWidget = SimpleCardWidget(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverResMonitorWidget.sizePolicy().hasHeightForWidth())
        self.serverResMonitorWidget.setSizePolicy(sizePolicy)
        self.serverResMonitorWidget.setFixedHeight(165)
        self.horizontalLayout = QHBoxLayout(self.serverResMonitorWidget)
        self.serverRAMMonitorWidget = QWidget(self.serverResMonitorWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverRAMMonitorWidget.sizePolicy().hasHeightForWidth())
        self.serverRAMMonitorWidget.setSizePolicy(sizePolicy)
        self.serverRAMMonitorLayout = QGridLayout(self.serverRAMMonitorWidget)
        self.serverRAMMonitorLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.serverRAMMonitorLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.serverRAMMonitorRing = ProgressRing(self.serverRAMMonitorWidget)
        self.serverRAMMonitorRing.setTextVisible(True)
        self.serverRAMMonitorLayout.addWidget(self.serverRAMMonitorRing, 1, 1, 1, 1)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.serverRAMMonitorLayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.serverRAMMonitorTitle = StrongBodyLabel(self.serverRAMMonitorWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverRAMMonitorTitle.sizePolicy().hasHeightForWidth())
        self.serverRAMMonitorTitle.setSizePolicy(sizePolicy)
        self.serverRAMMonitorTitle.setAlignment(Qt.AlignCenter)
        self.serverRAMMonitorLayout.addWidget(self.serverRAMMonitorTitle, 0, 0, 1, 3)
        self.horizontalLayout.addWidget(self.serverRAMMonitorWidget)
        self.resSeparator = VerticalSeparator(self.serverResMonitorWidget)
        self.horizontalLayout.addWidget(self.resSeparator)
        self.serverCPUMonitorWidget = QWidget(self.serverResMonitorWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverCPUMonitorWidget.sizePolicy().hasHeightForWidth())
        self.serverCPUMonitorWidget.setSizePolicy(sizePolicy)
        self.gridLayout_4 = QGridLayout(self.serverCPUMonitorWidget)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 1, 2, 1, 1)
        self.serverCPUMonitorRing = ProgressRing(self.serverCPUMonitorWidget)
        self.serverCPUMonitorRing.setTextVisible(True)
        self.gridLayout_4.addWidget(self.serverCPUMonitorRing, 1, 1, 1, 1)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem4, 1, 0, 1, 1)
        self.serverCPUMonitorTitle = StrongBodyLabel(self.serverCPUMonitorWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverCPUMonitorTitle.sizePolicy().hasHeightForWidth())
        self.serverCPUMonitorTitle.setSizePolicy(sizePolicy)
        self.serverCPUMonitorTitle.setAlignment(Qt.AlignCenter)
        self.gridLayout_4.addWidget(self.serverCPUMonitorTitle, 0, 0, 1, 3)
        self.horizontalLayout.addWidget(self.serverCPUMonitorWidget)
        self.verticalLayout_3.addWidget(self.serverResMonitorWidget)
        self.existPlayersTitle = SubtitleLabel(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.existPlayersTitle.sizePolicy().hasHeightForWidth())
        self.existPlayersTitle.setSizePolicy(sizePolicy)
        self.verticalLayout_3.addWidget(self.existPlayersTitle)
        self.existPlayersWidget = SimpleCardWidget(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.existPlayersWidget.sizePolicy().hasHeightForWidth())
        self.existPlayersWidget.setSizePolicy(sizePolicy)
        self.existPlayersWidget.setMinimumSize(QSize(0, 250))
        self.existPlayersWidget.setMaximumSize(QSize(16777215, 250))
        self.verticalLayout_2 = QVBoxLayout(self.existPlayersWidget)
        self.existPlayersListWidget = ListWidget(self.existPlayersWidget)
        self.verticalLayout_2.addWidget(self.existPlayersListWidget)
        self.verticalLayout_3.addWidget(self.existPlayersWidget)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.overviewScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.overviewPageLayout.addWidget(self.overviewScrollArea, 0, 0, 7, 1)
        self.stackedWidget.addWidget(self.overviewPage)

    def setupCommandPage(self):
        self.commandPage = QWidget()
        self.commandPage.setObjectName("commandPage")
        self.commandPageLayout = QGridLayout(self.commandPage)
        self.commandLineEdit = LineEdit(self.commandPage)
        self.commandLineEdit.setClearButtonEnabled(True)
        self.commandPageLayout.addWidget(self.commandLineEdit, 5, 0, 1, 4)
        self.sendCommandButton = PrimaryToolButton(FIF.SEND_FILL, self.commandPage)
        self.sendCommandButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sendCommandButton.setEnabled(False)
        self.commandPageLayout.addWidget(self.sendCommandButton, 5, 4, 1, 1)
        self.serverOutput = PlainTextEdit(self.commandPage)
        self.serverOutput.setFrameShape(QFrame.NoFrame)
        self.serverOutput.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.serverOutput.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.serverOutput.setReadOnly(True)
        self.commandPageLayout.addWidget(self.serverOutput, 0, 0, 5, 5)
        self.initQuickMenu()
        self.setupCommandCompleter()
        self.stackedWidget.addWidget(self.commandPage)

    def setupEditorPage(self):
        self.configEditorPage = QWidget()
        self.configEditorPage.setObjectName("configEditorPage")
        self.configEditorPageLayout = QGridLayout(self.configEditorPage)
        self.configEditorPageLayout.setObjectName("gridLayout_7")
        self.configEditorStackedWidget = EraseStackedWidget(self.configEditorPage)
        self.configEditorStackedWidget.setObjectName("configEditorStackedWidget")
        self.configEditorPageLayout.addWidget(self.configEditorStackedWidget, 1, 1, 1, 1)
        self.configEditorTabBar = TabBar(self.configEditorPage)
        self.configEditorTabBar.setAddButtonVisible(False)
        self.configEditorTabBar.setMovable(False)
        self.configEditorTabBar.setScrollable(False)
        self.configEditorTabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        self.configEditorTabBar.setObjectName("configEditorTabBar")
        self.configEditorPageLayout.addWidget(self.configEditorTabBar, 0, 1, 1, 1)
        self.configEditorFileTreeView = TreeView(self.configEditorPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configEditorFileTreeView.sizePolicy().hasHeightForWidth())
        self.configEditorFileTreeView.setSizePolicy(sizePolicy)
        self.configEditorFileTreeView.setMinimumSize(QSize(200, 0))
        self.configEditorFileTreeView.setFrameShape(QFrame.NoFrame)
        self.configEditorFileTreeView.setFrameShadow(QFrame.Plain)
        self.configEditorFileTreeView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.configEditorFileTreeView.setObjectName("configEditorFileTreeView")
        self.configFileTreeModel = QFileSystemModel()
        self.configFileTreeModel.setRootPath("")
        self.configFileTreeModel.setNameFilters([
            "*.yml",
            "*.json",
            "*.conf",
            "*.ini",
            "*.properties",
            "*.xml",
            "*.yaml",
            "*.tmlp",
            "*.toml",
            "*.txt",
            "*.log",
            "*.sh",
            "*.bat",
            "*.cmd",
            "*.ps1",
            "*.psm1",
            "*.psd1",
            "*.ps1xml",
            "*.dsc",
            "*.dscx",
            "*.dscx12",
            "*.*.ps1xml",
        ])
        self.configFileTreeModel.setNameFilterDisables(False)
        self.configEditorFileTreeView.setModel(self.configFileTreeModel)
        self.configEditorFileTreeView.setRootIndex(
            self.configFileTreeModel.index(osp.abspath(f"Servers/{self.serverConfig.serverName}"))
        )
        self.configEditorFileTreeView.setHeaderHidden(True)
        self.configEditorFileTreeView.setColumnHidden(1, True)
        self.configEditorFileTreeView.setColumnHidden(2, True)
        self.configEditorFileTreeView.setColumnHidden(3, True)
        self.configEditorFileTreeView.selectionModel().selectionChanged.connect(
            self.createConfigEditor
        )
        self.configEditorTabBar.tabCloseRequested.connect(self.removeConfigEditor)
        self.configEditorPageLayout.addWidget(self.configEditorFileTreeView, 0, 0, 2, 1)
        self.stackedWidget.addWidget(self.configEditorPage)

    def setupScheduleTasksPage(self):
        self.scheduleTasksPage = QWidget()
        self.scheduleTasksPage.setObjectName("scheduleTasksPage")
        self.scheduleTasksPageLayout = QGridLayout(self.scheduleTasksPage)
        self.scheduleTasksScrollArea = MySmoothScrollArea(self.scheduleTasksPage)
        self.scheduleTasksScrollArea.setFrameShape(QFrame.NoFrame)
        self.scheduleTasksScrollArea.setFrameShadow(QFrame.Plain)
        self.scheduleTasksScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scheduleTasksScrollArea.setWidgetResizable(True)
        self.scheduleTasksScrollArea.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.scheduleTasksWidgetContents = QWidget()
        self.scheduleTasksWidgetContents.setGeometry(QRect(0, 0, 668, 537))
        self.scheduleTasksScrollArea.setWidget(self.scheduleTasksWidgetContents)
        self.scheduleTasksPageLayout.addWidget(self.scheduleTasksScrollArea, 2, 0, 1, 4)
        self.exportScheduleConfigBtn = PushButton(self.scheduleTasksPage)
        self.scheduleTasksPageLayout.addWidget(self.exportScheduleConfigBtn, 1, 2, 1, 1)
        spacerItem3 = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.scheduleTasksPageLayout.addItem(spacerItem3, 1, 3, 1, 1)
        self.addScheduleTaskBtn = PushButton(self.scheduleTasksPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addScheduleTaskBtn.sizePolicy().hasHeightForWidth())
        self.addScheduleTaskBtn.setSizePolicy(sizePolicy)
        self.scheduleTasksPageLayout.addWidget(self.addScheduleTaskBtn, 1, 0, 1, 1)
        self.importScheduleConfigBtn = PushButton(self.scheduleTasksPage)
        self.scheduleTasksPageLayout.addWidget(self.importScheduleConfigBtn, 1, 1, 1, 1)
        self.stackedWidget.addWidget(self.scheduleTasksPage)

    def setupAnalyzePage(self):
        self.analyzePage = QWidget()
        self.analyzePage.setObjectName("analyzePage")

        self.analyzePageLayout = QGridLayout(self.analyzePage)
        self.errTitle = SubtitleLabel(self.analyzePage)
        self.analyzeSeparator = VerticalSeparator(self.analyzePage)
        self.startAnalyze = PrimaryPushButton(self.analyzePage)
        self.errTextEdit = PlainTextEdit(self.analyzePage)
        self.resultTextEdit = PlainTextEdit(self.analyzePage)
        self.resultTextEdit.setReadOnly(True)
        self.resultTitle = SubtitleLabel(self.analyzePage)
        self.copyResultBtn = PushButton(self.analyzePage)
        self.switchAnalyzeProviderBtn = SwitchButton(self.analyzePage)

        self.analyzePageLayout.addWidget(self.errTitle, 2, 0, 1, 1)
        self.analyzePageLayout.addWidget(self.analyzeSeparator, 3, 1, 2, 1)
        self.analyzePageLayout.addWidget(self.startAnalyze, 4, 0, 1, 1)
        self.analyzePageLayout.addWidget(self.errTextEdit, 3, 0, 1, 1)
        self.analyzePageLayout.addWidget(self.resultTextEdit, 3, 2, 1, 1)
        self.analyzePageLayout.addWidget(self.resultTitle, 2, 2, 1, 1)
        self.analyzePageLayout.addWidget(self.copyResultBtn, 4, 2, 1, 1)
        self.analyzePageLayout.addItem(
            QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed), 1, 0, 1, 3
        )
        self.analyzePageLayout.addWidget(self.switchAnalyzeProviderBtn, 0, 0, 1, 3)
        self.stackedWidget.addWidget(self.analyzePage)
        self.gridLayout.addWidget(self.stackedWidget, 2, 1, 2, 1)

    def initQuickMenu(self):
        self.quickMenu = SimpleCardWidget(self.commandPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quickMenu.sizePolicy().hasHeightForWidth())
        self.quickMenu.setSizePolicy(sizePolicy)
        self.quickMenu.setMinimumSize(QSize(125, 340))
        self.quickMenu.setMaximumSize(QSize(125, 16777215))
        self.quickMenuLayout = QVBoxLayout(self.quickMenu)
        self.quickMenuTitleLabel = StrongBodyLabel(self.quickMenu)
        self.quickMenuLayout.addWidget(self.quickMenuTitleLabel)
        self.difficulty = ComboBox(self.quickMenu)
        self.difficulty.setMinimumSize(QSize(0, 30))
        self.quickMenuLayout.addWidget(self.difficulty)
        self.gamemode = TransparentPushButton(self.quickMenu)
        self.gamemode.setMinimumSize(QSize(0, 30))
        self.quickMenuLayout.addWidget(self.gamemode)
        self.whiteList = TransparentPushButton(self.quickMenu)
        self.whiteList.setMinimumSize(QSize(0, 30))
        self.quickMenuLayout.addWidget(self.whiteList)
        self.op = TransparentPushButton(self.quickMenu)
        self.op.setMinimumSize(QSize(0, 30))
        self.quickMenuLayout.addWidget(self.op)
        self.kickPlayers = TransparentPushButton(self.quickMenu)
        self.kickPlayers.setMinimumSize(QSize(0, 30))
        self.quickMenuLayout.addWidget(self.kickPlayers)
        self.banPlayers = TransparentPushButton(self.quickMenu)
        self.banPlayers.setMinimumSize(QSize(0, 30))
        self.quickMenuLayout.addWidget(self.banPlayers)
        self.saveServer = TransparentPushButton(self.quickMenu)
        self.saveServer.setMinimumSize(QSize(0, 30))
        self.quickMenuLayout.addWidget(self.saveServer)
        self.exitServer = TransparentPushButton(self.quickMenu)
        self.exitServer.setMinimumSize(QSize(0, 30))
        self.quickMenuLayout.addWidget(self.exitServer)
        self.killServer = TransparentPushButton(self.quickMenu)
        self.killServer.setMinimumSize(QSize(0, 30))
        self.quickMenuLayout.addWidget(self.killServer)
        self.errorHandler = ToggleButton(self.quickMenu)
        self.quickMenuLayout.addWidget(self.errorHandler)
        self.commandPageLayout.addWidget(self.quickMenu, 0, 5, 1, 1)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.commandPageLayout.addItem(spacerItem2, 1, 5, 5, 1)

        self.gamemode.clicked.connect(self.initQuickMenu_GameMode)
        self.difficulty.currentIndexChanged.connect(self.runQuickMenu_Difficulty)
        self.whiteList.clicked.connect(self.initQuickMenu_WhiteList)
        self.op.clicked.connect(self.initQuickMenu_Operator)
        self.kickPlayers.clicked.connect(self.initQuickMenu_Kick)
        self.banPlayers.clicked.connect(self.initQuickMenu_BanOrPardon)
        self.saveServer.clicked.connect(lambda: self.sendCommand("save-all"))
        self.exitServer.clicked.connect(self.runQuickMenu_StopServer)
        self.killServer.clicked.connect(self.runQuickMenu_KillServer)
        self.errorHandler.setChecked(False)

    def initTexts(self):
        self.difficulty.addItems([
            self.tr("和平"),
            self.tr("简单"),
            self.tr("普通"),
            self.tr("困难"),
        ])
        self.backupServerBtn.setText("备份服务器")
        self.openServerFolder.setText("打开服务器目录")
        self.backupSavesBtn.setText("备份存档")
        self.genRunScriptBtn.setText("生成启动脚本")
        self.toggleServerBtn.setText("启动服务器")
        self.serverResMonitorTitle.setText("服务器资源占用")
        self.serverRAMMonitorTitle.setText("RAM：[curr/max]")
        self.serverCPUMonitorTitle.setText("CPU：")
        self.existPlayersTitle.setText("在线玩家列表")
        self.quickMenuTitleLabel.setText("快捷菜单：")
        self.difficulty.setText("游戏难度")
        self.gamemode.setText("游戏模式")
        self.whiteList.setText("白名单")
        self.op.setText("管理员")
        self.kickPlayers.setText("踢人")
        self.banPlayers.setText("封禁")
        self.saveServer.setText("保存存档")
        self.exitServer.setText("关闭服务器")
        self.killServer.setText("强制关闭")
        self.errorHandler.setText("报错分析")
        self.exportScheduleConfigBtn.setText("导出")
        self.addScheduleTaskBtn.setText("添加计划任务")
        self.importScheduleConfigBtn.setText("导入")
        self.errTitle.setText("含报错的日志：")
        self.startAnalyze.setText("开始分析")
        self.resultTitle.setText("分析结果：")
        self.copyResultBtn.setText("复制")
        self.switchAnalyzeProviderBtn.setText("当前：使用本地模块分析")
        self.switchAnalyzeProviderBtn.setOnText("当前：使用CrashMC分析")
        self.switchAnalyzeProviderBtn.setOffText("当前：使用本地模块分析")
        self.commandLineEdit.setPlaceholderText("在此输入指令，回车或点击右边按钮发送，不需要加/")
        self.serverOutput.setPlaceholderText(self.tr("请先开启服务器！不开服务器没有日志！"))

    def initSlots(self):
        self.commandLineEdit.textChanged.connect(
            lambda: self.sendCommandButton.setEnabled(self.commandLineEdit.text() != "")
        )
        self.sendCommandButton.clicked.connect(
            lambda: self.sendCommand(command=self.commandLineEdit.text())
        )
        self.commandLineEdit.returnPressed.connect(
            lambda: self.sendCommand(command=self.commandLineEdit.text())
        )
        self.openServerFolder.clicked.connect(
            lambda: openLocalFile(f"Servers/{self.serverConfig.serverName}")
        )
        self.genRunScriptBtn.clicked.connect(self.genRunScript)
        self.backupServerBtn.clicked.connect(
            lambda: backupServer(serverName=self.serverConfig.serverName, parent=self)
        )
        self.backupSavesBtn.clicked.connect(
            lambda: backupSaves(serverConfig=self.serverConfig, parent=self)
        )

    def initNavigation(self):
        self.serverSegmentedWidget.addItem(
            routeKey="overviewPage",
            text="服务器概览",
            onClick=lambda: self.stackedWidget.setCurrentWidget(self.overviewPage),
            icon=FIF.INFO,
        )
        self.serverSegmentedWidget.addItem(
            routeKey="commandPage",
            text="快捷终端",
            onClick=lambda: self.stackedWidget.setCurrentWidget(self.commandPage),
            icon=FIF.COMMAND_PROMPT,
        )
        self.serverSegmentedWidget.addItem(
            routeKey="backupPage",
            text="编辑配置文件",
            onClick=lambda: self.stackedWidget.setCurrentWidget(self.configEditorPage),
            icon=FIF.LABEL,
        )
        self.serverSegmentedWidget.addItem(
            routeKey="scheduleTasksPage",
            text="计划任务",
            onClick=lambda: self.stackedWidget.setCurrentWidget(self.scheduleTasksPage),
            icon=FIF.HISTORY,
        )
        self.serverSegmentedWidget.addItem(
            routeKey="analyzePage",
            text="错误分析",
            onClick=lambda: self.stackedWidget.setCurrentWidget(self.analyzePage),
            icon=FIF.SEARCH_MIRROR,
        )
        self.serverSegmentedWidget.setCurrentItem("overviewPage")

    def initWindow(self):
        """初始化窗口"""

        self.setTitleBar(ServerWindowTitleBar(self))
        self.setWindowTitle(f"MCSL2服务器 - {self.serverConfig.serverName}")

        self.setWindowIcon(QIcon(f":/built-InIcons/{self.serverConfig.serverIconName}"))
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.resize(int(w // 1.5), int(h // 1.5))
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def _normalBackgroundColor(self):
        if not self.isMicaEffectEnabled():
            return QColor(32, 32, 32) if isDarkTheme() else QColor(243, 243, 243)

        return QColor(0, 0, 0, 0)

    def _onThemeChangedFinished(self):
        if self.isMicaEffectEnabled():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.backgroundColor)
        painter.drawRect(self.rect())

    def setMicaEffectEnabled(self, isEnabled: bool):
        """set whether the mica effect is enabled, only available on Win11"""
        if sys.platform != "win32" or sys.getwindowsversion().build < 22000:
            return

        self._isMicaEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self._normalBackgroundColor())

    def isMicaEffectEnabled(self):
        return self._isMicaEnabled

    def getRunningStatus(self):
        if self.serverBridge is None:
            return False
        elif not self.serverBridge.isServerRunning():
            return False
        else:
            return True

    def setupCommandCompleter(self):
        intellisense = QCompleter(
            GlobalMCSL2Variables.MinecraftBuiltInCommand, self.commandLineEdit
        )
        intellisense.setCaseSensitivity(Qt.CaseInsensitive)
        self.commandLineEdit.setCompleter(intellisense)

    def _showNoAcceptEULAMsg(self, validator: _MinecraftEULA):
        w = MessageBox(
            title=self.tr("提示"),
            content=self.tr(
                "你并未同意Minecraft的最终用户许可协议。\n请先同意EULA才可启动服务器。\n可点击下方的按钮查看Eula，或直接点击同意按钮。"
            ),
            parent=self,
        )
        w.yesButton.setText(self.tr("同意"))
        w.yesSignal.connect(validator.acceptEula)
        w.yesSignal.connect(self.startServer)
        w.cancelButton.setText(self.tr("拒绝"))
        eulaBtn = HyperlinkButton(url="https://aka.ms/MinecraftEULA", text="Eula", icon=FIF.LINK)
        w.buttonLayout.addWidget(eulaBtn, 1, Qt.AlignVCenter)
        w.exec_()

    def startServer(self):
        if self.serverBridge is not None:
            if not self.serverBridge.isServerRunning():
                t = self.serverBridge.startServer()
                if isinstance(t, _MinecraftEULA):
                    self._showNoAcceptEULAMsg(t)
                else:
                    self.registerResMonitor()
                    self.registerCommandOutput()
                    self.registerStartServerComponents()
                    self.serverBridge.serverProcess.process.finished.connect(
                        self.unRegisterCommandOutput
                    )
                    return
            else:
                return
        else:
            t = self.serverLauncher.start()
            if isinstance(t, _MinecraftEULA):
                self._showNoAcceptEULAMsg(t)
            else:
                self.serverBridge = t
                self.registerResMonitor()
                self.registerCommandOutput()
                self.registerStartServerComponents()

    def stopServer(self, forceNoErrorHandler=False):
        if self.serverBridge is not None:
            self.serverBridge.stopServer()
            self.killServer.setEnabled(True)
            self.toggleServerBtn.setEnabled(True)
            self.exitServer.setEnabled(True)
            self.unRegisterResMonitor()
            self.unRegisterStartServerComponents()
            if self.errorHandler.isChecked() and not forceNoErrorHandler:
                self.showErrorHandlerReport()

    def registerStartServerComponents(self):
        self.toggleServerBtn.setText(self.tr("关闭服务器"))
        self.exitServer.setText(self.tr("关闭服务器"))
        try:
            self.toggleServerBtn.clicked.disconnect()
        except (AttributeError, TypeError):
            pass
        try:
            self.exitServer.clicked.disconnect()
        except (AttributeError, TypeError):
            pass
        self.toggleServerBtn.clicked.connect(self.runQuickMenu_StopServer)
        self.exitServer.clicked.connect(self.runQuickMenu_StopServer)
        self.backupSavesBtn.setEnabled(False)
        self.backupServerBtn.setEnabled(False)
        self.manageBackupBtn.setEnabled(False)

    def unRegisterStartServerComponents(self):
        self.toggleServerBtn.setText(self.tr("开启服务器"))
        self.exitServer.setText(self.tr("开启服务器"))
        try:
            self.toggleServerBtn.clicked.disconnect()
        except (AttributeError, TypeError):
            pass
        try:
            self.exitServer.clicked.disconnect()
        except (AttributeError, TypeError):
            pass
        self.toggleServerBtn.clicked.connect(self.startServer)
        self.exitServer.clicked.connect(self.startServer)
        self.backupSavesBtn.setEnabled(True)
        self.backupServerBtn.setEnabled(True)
        self.manageBackupBtn.setEnabled(True)

    def registerCommandOutput(self):
        try:
            self.serverBridge.serverLogOutput.disconnect(self.colorConsoleText)
        except (AttributeError, TypeError):
            pass
        self.serverBridge.serverLogOutput.connect(self.colorConsoleText)

    def unRegisterCommandOutput(self):
        try:
            self.serverBridge.serverLogOutput.disconnect(self.colorConsoleText)
        except (AttributeError, TypeError):
            pass

    def registerResMonitor(self):
        self.serverMemThread = MinecraftServerResMonitorUtil(
            serverConfig=self.serverConfig, bridge=self.serverBridge, parent=self
        )
        self.serverMemThread.memPercent.connect(self.setMemView)
        self.serverMemThread.cpuPercent.connect(self.setCPUView)
        self.serverBridge.serverClosed.connect(self.unRegisterResMonitor)

    def unRegisterResMonitor(self):
        self.serverMemThread.onServerClosedHandler()
        try:
            self.serverMemThread.memPercent.disconnect(self.setMemView)
        except (AttributeError, TypeError):
            pass
        try:
            self.serverMemThread.cpuPercent.disconnect(self.setCPUView)
        except (AttributeError, TypeError):
            pass
        self.serverMemThread.deleteLater()

    @pyqtSlot(float)
    def setMemView(self, mem):
        self.serverRAMMonitorTitle.setText(
            f"RAM：{str(round(mem, 2))}{self.serverConfig.memUnit}/{self.serverConfig.maxMem}{self.serverConfig.memUnit}"  # noqa: E501
        )
        self.serverRAMMonitorRing.setValue(int(int(mem) / self.serverConfig.maxMem * 100))

    @pyqtSlot(float)
    def setCPUView(self, cpuPercent):
        self.serverCPUMonitorRing.setValue(int(cpuPercent))

    @pyqtSlot(str)
    def colorConsoleText(self, serverOutput):
        readServerProperties(self.serverConfig)
        fmt = QTextCharFormat()
        # fmt: off
        greenText = ["INFO", "Info", "info", "tip", "tips", "hint", "HINT", "提示"]
        orangeText = ["WARN", "Warning", "warn", "alert", "ALERT", "Alert", "CAUTION", "Caution", "警告"]  # noqa: E501
        redText = ["ERR", "Err", "Fatal", "FATAL", "Critical", "Danger", "DANGER", "错", "at java", "at net", "at oolloo", "Caused by", "at sun"]  # noqa: E501
        blueText = ["DEBUG", "Debug", "debug", "调试", "TEST", "Test", "Unknown command", "MCSL2"]
        color = [QColor(52, 185, 96), QColor(196, 139, 33), QColor(214, 39, 21), QColor(22, 122, 232)]  # noqa: E501
        for keyword in greenText:
            if keyword in serverOutput:
                fmt.setForeground(QBrush(color[0]))
        for keyword in orangeText:
            if keyword in serverOutput:
                fmt.setForeground(QBrush(color[1]))
        for keyword in redText:
            if keyword in serverOutput:
                fmt.setForeground(QBrush(color[2]))
        for keyword in blueText:
            if keyword in serverOutput:
                fmt.setForeground(QBrush(color[3]))
        self.serverOutput.mergeCurrentCharFormat(fmt)
        serverOutput = (
            serverOutput.replace("[38;2;170;170;170m", "")
            .replace("[38;2;255;170;0m", "")
            .replace("[38;2;255;255;255m", "")
            .replace("[0m", "")
            .replace("[38;2;255;255;85m", "")
            .replace("[38;2;255;255;0m", "")
            .replace("[38;2;255;85;85m", "")
            .replace("[38;2;255;255;255m", "")
            .replace("[3m", "")
            .replace("[m[", "[")
            .replace("[32m", "")
            .replace("Preparing spawn area", self.tr("准备生成点区域中"))
            .replace("main/INFO", self.tr("主类/信息"))
            .replace("main/WARN", self.tr("主类/警告"))
            .replace("main/ERROR", self.tr("主类/错误"))
            .replace("main/FATAL", self.tr("主类/致命错误"))
            .replace("main/DEBUG", self.tr("主类/调试信息"))
            .replace("INFO", self.tr("信息"))
            .replace("WARN", self.tr("警告"))
            .replace("ERROR", self.tr("错误"))
            .replace("FATAL", self.tr("致命错误"))
            .replace("DEBUG", self.tr("调试信息"))
            .replace("Server thread", self.tr("服务器线程"))
            .replace("Server-Worker", self.tr("服务器工作进程"))
            .replace("DEBUG", self.tr("调试信息"))
            .replace("Forge Version Check", self.tr("Forge版本检查"))
            .replace("ModLauncher running: args", self.tr("ModLauncher运行中: 参数"))
            .replace("All chunks are saved", self.tr("所有区块已保存"))
            .replace("Saving the game (this may take a moment!)", self.tr("保存游戏存档中（可能需要一些时间）"))  # noqa: E501
            .replace("Saved the game", self.tr("已保存游戏存档"))
            .replace("[33m[", "[")
            .replace("[", "[")
        )
        if "Disabling terminal, you're running in an unsupported environment." in serverOutput:
            return
        if "Advanced terminal features are not available in this environment" in serverOutput:
            return
        if "Unable to instantiate org.fusesource.jansi.WindowsAnsiOutputStream" in serverOutput:
            return
        if "Loading libraries, please wait..." in serverOutput:
            self.playersList.clear()
            serverOutput = self.tr("[MCSL2 | 提示]：服务器正在启动，请稍后...\n") + serverOutput
            InfoBar.info(
                title=self.tr("提示"),
                content=self.tr("服务器正在启动，请稍后..."),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=2222,
                parent=self,
            )
        self.serverOutput.appendPlainText(serverOutput)
        if search(r"(?=.*Done)(?=.*!)", serverOutput):
            fmt.setForeground(QBrush(color[3]))
            self.serverOutput.mergeCurrentCharFormat(fmt)
            try:
                ip = self.serverConfig.serverProperties["server-ip"]
                ip = "127.0.0.1" if ip == "" else ip
            except KeyError:
                ip = "127.0.0.1"
            port = self.serverConfig.serverProperties.get("server-port", 25565)
            self.serverOutput.appendPlainText(
                self.tr(f"[MCSL2 | 提示]：服务器启动完毕！\n[MCSL2 | 提示]：如果本机开服，IP 地址为{ip}，端口为{port}。\n[MCSL2 | 提示]：如果外网开服,或使用了内网穿透等服务，连接地址为你的相关服务地址。")  # noqa: E501
            )
            InfoBar.success(
                title=self.tr("提示"),
                content=self.tr(f"服务器启动完毕！\n如果本机开服，IP 地址为{ip}，端口为{port}。\n如果外网开服,或使用了内网穿透等服务，连接地址为你的相关服务地址。"),  # noqa: E501
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self,
            )
            self.initQuickMenu_Difficulty()
        if "�" in serverOutput:
            fmt.setForeground(QBrush(color[1]))
            self.serverOutput.mergeCurrentCharFormat(fmt)
            self.serverOutput.appendPlainText(
                self.tr("[MCSL2 | 警告]：服务器疑似输出非法字符，也有可能是无法被当前编码解析的字符。请尝试更换编码。")  # noqa: E501
            )
            InfoBar.warning(
                title=self.tr("警告"),
                content=self.tr("服务器疑似输出非法字符，也有可能是无法被当前编码解析的字符。\n请尝试更换编码。"),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=2222,
                parent=self,
            )
        if self.errorHandler.isChecked():
            self.errMsg += ServerErrorHandler.detect(serverOutput)
        if (
            "logged in with entity id" in serverOutput
            or " left the game" in serverOutput
        ):
            self.recordPlayers(serverOutput)

    def showErrorHandlerReport(self):
        if self.errMsg != "":
            w = MessageBox("错误分析器日志", self.errMsg, self)
            w.cancelButton.setParent(None)
            w.exec_()
        else:
            w = MessageBox(
                "错误分析器日志", "本次没有检测到任何MCSL2内置错误分析可用解决方案。", self
            )
            w.cancelButton.setParent(None)
            w.exec_()

    def recordPlayers(self, serverOutput: str):
        if "logged in with entity id" in serverOutput:
            try:
                self.playersList.append(str(str(serverOutput).split("INFO]: ")[1].split("[/")[0]))
                return
            except Exception:
                pass

            try:
                # 若不成功，尝试提取玩家名字
                # [11:49:05] [Server thread/INFO] [minecraft/PlayerList]: Ares_Connor[/127.0.0.1:63854] logged in with entity id 229 at (7.258252218995321, 65.0, 11.09627995098097)  # noqa: E501
                # 提取玩家名字
                name = serverOutput
                name = name.split("]: ")[1].split("[/")[0]
                self.playersList.append(name)
                self.existPlayersListWidget.clear()
                self.existPlayersListWidget.addItems(self.playersList)
            except Exception as e:
                MCSL2Logger.error(
                    msg=f"extract player name failed\nonRecordPlayers::login {serverOutput}",
                    exc=e,
                )

        elif " left the game" in serverOutput:
            try:
                # fmt: off
                self.playersList.pop(self.playersList.index(str(str(serverOutput).split("INFO]: ")[1].split(" left the game")[0])))  # noqa: E501
                return
            except Exception:
                pass

            try:  # 若不成功，尝试提取玩家名字
                # [11:53:52] [Server thread/INFO] [minecraft/DedicatedServer]: Ares_Connor left the game  # noqa: E501
                name = serverOutput
                name = name.split("]: ")[1].split(" left the game")[0].strip()
                self.playersList.pop(self.playersList.index(name))
                self.existPlayersListWidget.clear()
                self.existPlayersListWidget.addItems(self.playersList)
            except Exception as e:
                MCSL2Logger.error(
                    msg=f"extract player name failed\nonRecordPlayers::logout {serverOutput}",
                    exc=e,
                )

    # def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
    #     if a0 == self.commandPage and a1.type() == QEvent.KeyPress:
    #         if a1.key() == Qt.Key_Return or a1.key() == Qt.Key_Enter:
    #             if self.stackedWidget.currentIndex() == 1 and self.commandLineEdit:
    #                 self.sendCommandButton.click()
    #                 return True
    #         elif a1.key() == Qt.Key_Up:
    #             if self.stackedWidget.currentIndex() == 1 and self.commandLineEdit:
    #                 if len(
    #                     GlobalMCSL2Variables.userCommandHistory
    #                 ) and GlobalMCSL2Variables.upT > -len(GlobalMCSL2Variables.userCommandHistory):
    #                     GlobalMCSL2Variables.upT -= 1
    #                     lastCommand = GlobalMCSL2Variables.userCommandHistory[
    #                         GlobalMCSL2Variables.upT
    #                     ]
    #                     self.commandLineEdit.setText(lastCommand)
    #                     return True
    #         elif a1.key() == Qt.Key_Down:
    #             if self.stackedWidget.currentIndex() == 1 and self.commandLineEdit:
    #                 if (
    #                     len(GlobalMCSL2Variables.userCommandHistory)
    #                     and GlobalMCSL2Variables.upT < 0
    #                 ):
    #                     GlobalMCSL2Variables.upT += 1
    #                     nextCommand = GlobalMCSL2Variables.userCommandHistory[
    #                         GlobalMCSL2Variables.upT
    #                     ]
    #                     self.commandLineEdit.setText(nextCommand)
    #                     return True
    #                 if (
    #                     len(GlobalMCSL2Variables.userCommandHistory)
    #                     and GlobalMCSL2Variables.upT == 0
    #                 ):
    #                     self.commandLineEdit.setText("")
    #                     return True
    #     return super().eventFilter(a0, a1)

    def showServerNotOpenMsg(self):
        """弹出服务器未开启提示"""
        w = MessageBox(
            title=self.tr("失败"),
            content=self.tr("服务器并未开启，请先开启服务器。"),
            parent=self,
        )
        w.yesButton.setText(self.tr("好"))
        w.cancelButton.setParent(None)
        w.cancelButton.deleteLater()
        w.exec_()

    def sendCommand(self, command):
        if self.getRunningStatus():
            if command != "":
                self.serverBridge.sendCommand(command=command)
                self.commandLineEdit.clear()
                GlobalMCSL2Variables.userCommandHistory.append(command)
                GlobalMCSL2Variables.upT = 0
            else:
                pass
        else:
            self.showServerNotOpenMsg()

    def lineEditChecker(self, text):
        if text != "":
            self.playersControllerBtnEnabled.emit(True)
        else:
            self.playersControllerBtnEnabled.emit(False)

    def getKnownServerPlayers(self) -> str:
        players = self.tr("无玩家加入")
        if len(self.playersList):
            players = ""
            for player in self.playersList:
                players += f"{player}\n"
        else:
            pass
        return players

    def initQuickMenu_Difficulty(self):
        """快捷菜单-服务器游戏难度"""
        textDiffiultyList = ["peaceful", "easy", "normal", "hard"]
        if self.getRunningStatus():
            try:
                self.difficulty.setCurrentIndex(
                    int(self.serverConfig.serverProperties["difficulty"])
                )
            except ValueError:
                self.difficulty.setCurrentIndex(
                    int(textDiffiultyList.index(self.serverConfig.serverProperties["difficulty"]))
                )
            except Exception:
                pass
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_Difficulty(self):
        textDiffiultyList = ["peaceful", "easy", "normal", "hard"]
        self.sendCommand(f"difficulty {textDiffiultyList[self.difficulty.currentIndex()]}")

    def initQuickMenu_GameMode(self):
        """快捷菜单-游戏模式"""
        if self.getRunningStatus():
            gamemodeWidget = playersController()
            gamemodeWidget.mode.addItems([
                self.tr("生存"),
                self.tr("创造"),
                self.tr("冒险"),
                self.tr("旁观"),
            ])
            gamemodeWidget.mode.setCurrentIndex(0)
            gamemodeWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=gamemodeWidget.who.text())
            )
            gamemodeWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox(self.tr("服务器游戏模式"), self.tr("设置服务器游戏模式"), self)
            w.yesButton.setText(self.tr("确定"))
            w.cancelButton.setText(self.tr("取消"))
            w.textLayout.addWidget(gamemodeWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(
                lambda: self.runQuickMenu_GameMode(
                    gamemode=gamemodeWidget.mode.currentIndex(),
                    player=gamemodeWidget.who.text(),
                )
            )
            w.exec_()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_GameMode(self, gamemode: int, player: str):
        gameModeList = ["survival", "creative", "adventure", "spectator"]
        if self.getRunningStatus():
            self.serverBridge.sendCommand(command=f"gamemode {gameModeList[gamemode]} {player}")
        else:
            self.showServerNotOpenMsg()
            # TODO: rollback

    def initQuickMenu_WhiteList(self):
        """快捷菜单-白名单"""
        if self.getRunningStatus():
            whiteListWidget = playersController()
            whiteListWidget.mode.addItems([self.tr("添加(add)"), self.tr("删除(remove)")])
            whiteListWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=whiteListWidget.who.text())
            )
            whiteListWidget.playersTip.setText(self.getKnownServerPlayers())
            content = (
                self.tr("请确保服务器的白名单功能处于启用状态。\n")
                + self.tr("启用：/whitelist on\n")
                + self.tr("关闭：/whitelist off\n")
                + self.tr("列出当前白名单：/whitelist list\n")
                + self.tr("重新加载白名单：/whitelist reload")
            )
            w = MessageBox(self.tr("白名单"), content, self)
            w.yesButton.setText(self.tr("确定"))
            w.cancelButton.setText(self.tr("取消"))
            w.textLayout.addWidget(whiteListWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(
                lambda: self.runQuickMenu_WhiteList(
                    mode=whiteListWidget.mode.currentIndex(),
                    player=whiteListWidget.who.text(),
                )
            )
            w.exec_()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_WhiteList(self, mode: int, player: str):
        whiteListMode = ["add", "remove"]
        if self.getRunningStatus():
            self.serverBridge.sendCommand(command=f"whitelist {whiteListMode[mode]} {player}")
        else:
            self.showServerNotOpenMsg()

    def initQuickMenu_Operator(self):
        """快捷菜单-服务器管理员"""
        if self.getRunningStatus():
            opWidget = playersController()
            opWidget.mode.addItems([self.tr("添加"), self.tr("删除")])
            opWidget.mode.setCurrentIndex(0)
            opWidget.who.textChanged.connect(lambda: self.lineEditChecker(text=opWidget.who.text()))
            opWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox(self.tr("服务器管理员"), self.tr("添加或删除管理员"), self)
            w.yesButton.setText(self.tr("确定"))
            w.cancelButton.setText(self.tr("取消"))
            w.textLayout.addWidget(opWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(
                lambda: self.runQuickMenu_Operator(
                    mode=opWidget.mode.currentIndex(), player=opWidget.who.text()
                )
            )
            w.exec_()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_Operator(self, mode: int, player: str):
        commandPrefixList = ["op", "deop"]
        if self.getRunningStatus():
            self.serverBridge.sendCommand(command=f"{commandPrefixList[mode]} {player}")
        else:
            self.showServerNotOpenMsg()

    def initQuickMenu_Kick(self):
        """快捷菜单-踢人"""
        if self.getRunningStatus():
            kickWidget = playersController()
            kickWidget.mode.setParent(None)
            kickWidget.mode.deleteLater()
            kickWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=kickWidget.who.text())
            )
            kickWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox(self.tr("踢出玩家"), self.tr("踢出服务器中的玩家"), self)
            w.yesButton.setText(self.tr("确定"))
            w.cancelButton.setText(self.tr("取消"))
            w.textLayout.addWidget(kickWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(lambda: self.runQuickMenu_Kick(player=kickWidget.who.text()))
            w.exec_()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_Kick(self, player: str):
        self.serverBridge.sendCommand(command=f"kick {player}")

    def initQuickMenu_BanOrPardon(self):
        """快捷菜单-封禁或解禁玩家"""
        if self.getRunningStatus():
            banOrPardonWidget = playersController()
            banOrPardonWidget.mode.addItems([self.tr("封禁"), self.tr("解禁")])
            banOrPardonWidget.mode.setCurrentIndex(0)
            banOrPardonWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=banOrPardonWidget.who.text())
            )
            banOrPardonWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox(self.tr("封禁或解禁玩家"), "ban/pardon", self)
            w.yesButton.setText(self.tr("确定"))
            w.cancelButton.setText(self.tr("取消"))
            w.textLayout.addWidget(banOrPardonWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(
                lambda: self.runQuickMenu_BanOrPardon(
                    mode=banOrPardonWidget.mode.currentIndex(),
                    player=banOrPardonWidget.who.text(),
                )
            )
            w.exec_()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_BanOrPardon(self, mode: int, player: str):
        commandPrefixList = ["ban", "pardon"]
        self.serverBridge.sendCommand(command=f"{commandPrefixList[mode]} {player}")

    def runQuickMenu_StopServer(self):
        if self.getRunningStatus():
            self.killServer.setEnabled(False)
            self.toggleServerBtn.setEnabled(False)
            self.exitServer.setEnabled(False)
            box = MessageBox(self.tr("正常关闭服务器"), self.tr("你确定要关闭服务器吗？"), self)
            box.yesSignal.connect(self.stopServer)
            box.cancelButton.clicked.connect(lambda: self.killServer.setEnabled(True))
            box.cancelButton.clicked.connect(lambda: self.toggleServerBtn.setEnabled(True))
            box.cancelButton.clicked.connect(lambda: self.exitServer.setEnabled(True))
            box.exec_()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_KillServer(self):
        """快捷菜单-强制关闭服务器"""
        if self.getRunningStatus():
            self.killServer.setEnabled(False)
            self.toggleServerBtn.setEnabled(False)
            self.exitServer.setEnabled(False)
            w = MessageBox(
                self.tr("强制关闭服务器"),
                self.tr("确定要强制关闭服务器吗？\n有可能导致数据丢失！\n请确保存档已经保存！"),
                self,
            )
            w.yesButton.setText(self.tr("算了"))
            w.cancelButton.setText(self.tr("强制关闭"))
            w.cancelSignal.connect(self.serverBridge.haltServer)
            w.cancelSignal.connect(lambda: self.killServer.setEnabled(True))
            w.cancelSignal.connect(lambda: self.toggleServerBtn.setEnabled(True))
            w.cancelSignal.connect(lambda: self.exitServer.setEnabled(True))
            w.cancelSignal.connect(
                lambda: InfoBar.warning(
                    title=self.tr("警告"),
                    content=self.tr("正在结束服务器..."),
                    orient=Qt.Horizontal,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                    duration=800,
                    parent=self,
                )
            )
            w.exec_()
            self.unRegisterResMonitor()
            self.unRegisterStartServerComponents()
        else:
            self.showServerNotOpenMsg()

    def createConfigEditor(self, selected, deselected):
        print(self.configEditorDict)
        filePath = self.sender().model().filePath(selected.indexes()[0]).replace("\\", "/")  # type: str
        if osp.isdir(filePath):
            print(1)
            return
        if filePath in self.configEditorTabBar.itemMap:
            self.configEditorTabBar.setCurrentTab(filePath)
            print(2)
            return
        else:
            print(3)
            try:
                with open(filePath, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception as e:
                InfoBar.info(
                    title="抱歉",
                    content=f"MCSL2无法打开此文件，原因：\n{e.with_traceback()}",
                    orient=Qt.Horizontal,
                    parent=self,
                    duration=1500,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                )
                return

            fileName = osp.basename(filePath)
            container = QWidget()
            containerLayout = QGridLayout(container)
            containerLayout.addWidget((p := PlainTextEdit(container)), 0, 0)
            p.setPlainText(text)
            self.configEditorStackedWidget.addWidget(container)
            self.configEditorTabBar.addTab(
                routeKey=filePath,
                text=fileName,
                icon=FIF.LABEL,
                onClick=lambda: self.configEditorStackedWidget.setCurrentWidget(container),
            )
            self.configEditorTabBar.setCurrentTab(filePath)
            self.configEditorStackedWidget.setCurrentWidget(container)
            self.configEditorContainerDict.update({filePath: container})
            self.configEditorDict.update({filePath: p})

    @pyqtSlot(int)
    def removeConfigEditor(self, i):
        with open(self.configEditorTabBar.items[i]._routeKey, "r", encoding="utf-8") as f:
            tmpText = f.read()
        if (
            newText := self.configEditorDict[
                self.configEditorTabBar.items[i]._routeKey
            ].toPlainText()
        ) != tmpText:
            with open(self.configEditorTabBar.items[i]._routeKey, "w+", encoding="utf-8") as nf:
                nf.write(newText)

            InfoBar.info(
                title="提示",
                content=f"已自动保存{self.configEditorTabBar.items[i]._routeKey}",
                orient=Qt.Horizontal,
                parent=self,
                duration=1500,
                isClosable=False,
                position=InfoBarPosition.TOP,
            )

        self.configEditorStackedWidget.removeWidget(
            self.configEditorContainerDict[self.configEditorTabBar.items[i]._routeKey]
        )
        self.configEditorContainerDict[self.configEditorTabBar.items[i]._routeKey].deleteLater()

        self.configEditorDict.pop(self.configEditorTabBar.items[i]._routeKey)

        self.configEditorContainerDict.pop(self.configEditorTabBar.items[i]._routeKey)

        self.configEditorTabBar.removeTab(i)

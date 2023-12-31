from PyQt5.QtCore import Qt, QSize, QRect, QEvent, QObject, pyqtSignal, pyqtSlot
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
)
from qfluentwidgets import (
    HyperlinkButton,
    MessageBox,
    ComboBox,
    LineEdit,
    ListWidget,
    Pivot,
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
)
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from PyQt5.QtGui import QIcon, QCursor, QColor, QPainter, QTextCharFormat, QColor, QBrush, QCursor
from qframelesswindow import TitleBar
from MCSL2Lib.ProgramControllers.interfaceController import EraseStackedWidget, MySmoothScrollArea
from MCSL2Lib.Resources.icons import *  # noqa: F401 F403
from MCSL2Lib.ProgramControllers.settingsController import cfg
from MCSL2Lib.ServerController.processCreator import _MinecraftEULA, ServerLauncher
from MCSL2Lib.ServerController.serverErrorHandler import ServerErrorHandler
from MCSL2Lib.ServerController.serverUtils import (
    MinecraftServerResMonitorUtil,
    readServerProperties,
)
import sys
from re import search
from MCSL2Lib.utils import MCSL2Logger
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

    def __init__(self, config: ServerVariables, launcher: ServerLauncher):
        self._isMicaEnabled = False
        super().__init__()
        self.errMsg = ""
        self.playersList = []
        self.playersControllerBtnEnabled.emit(False)
        self.serverConfig = config
        self.serverLauncher = launcher
        self.serverProcessHandler = None
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
        self.installEventFilter(self)

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
        self.overviewScrollArea.setFrameShape(QFrame.NoFrame)
        self.overviewScrollArea.setFrameShadow(QFrame.Plain)
        self.overviewScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.overviewScrollArea.setWidgetResizable(True)
        self.overviewScrollArea.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
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
        self.serverResMonitorWidget.setMinimumSize(QSize(0, 165))
        self.serverResMonitorWidget.setMaximumSize(QSize(16777215, 165))
        self.horizontalLayout = QHBoxLayout(self.serverResMonitorWidget)
        self.serverRAMMonitorWidget = QWidget(self.serverResMonitorWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverRAMMonitorWidget.sizePolicy().hasHeightForWidth())
        self.serverRAMMonitorWidget.setSizePolicy(sizePolicy)
        self.serverRAMMonitorLayout = QGridLayout(self.serverRAMMonitorWidget)
        self.serverRAMMonitorLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.serverRAMMonitorTitle = StrongBodyLabel(self.serverRAMMonitorWidget)
        self.serverRAMMonitorLayout.addWidget(self.serverRAMMonitorTitle, 0, 0, 1, 1)
        self.serverRAMMonitorRing = ProgressRing(self.serverRAMMonitorWidget)
        self.serverRAMMonitorRing.setTextVisible(True)
        self.serverRAMMonitorLayout.addWidget(self.serverRAMMonitorRing, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.serverRAMMonitorWidget)
        self.resSeparator = VerticalSeparator(self.serverResMonitorWidget)
        self.horizontalLayout.addWidget(self.resSeparator)
        self.serverCPUMonitorWidget = QWidget(self.serverResMonitorWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverCPUMonitorWidget.sizePolicy().hasHeightForWidth())
        self.serverCPUMonitorWidget.setSizePolicy(sizePolicy)
        self.serverCPUMonitorLayout = QGridLayout(self.serverCPUMonitorWidget)
        self.serverCPUMonitorTitle = StrongBodyLabel(self.serverCPUMonitorWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverCPUMonitorTitle.sizePolicy().hasHeightForWidth())
        self.serverCPUMonitorTitle.setSizePolicy(sizePolicy)
        self.serverCPUMonitorLayout.addWidget(self.serverCPUMonitorTitle, 0, 0, 1, 1)
        self.serverCPUMonitorRing = ProgressRing(self.serverCPUMonitorWidget)
        self.serverCPUMonitorRing.setTextVisible(False)
        self.serverCPUMonitorLayout.addWidget(self.serverCPUMonitorRing, 1, 0, 1, 1)
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
        self.configEditorPageLayout = QVBoxLayout(self.configEditorPage)
        self.configEditorPivot = Pivot(self.configEditorPage)
        self.configEditorPageLayout.addWidget(self.configEditorPivot)
        self.configEditorStackedWidget = EraseStackedWidget(self.configEditorPage)
        self.configEditorPageLayout.addWidget(self.configEditorStackedWidget)
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
        self.serverCPUMonitorTitle.setText("CPU：[percent]")
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
        self.commandLineEdit.textChanged.connect(
            lambda: self.sendCommandButton.setEnabled(self.commandLineEdit.text() != "")
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
        self.setWindowTitle("MCSL2服务器 - ")

        self.setWindowIcon(QIcon(":/built-InIcons/MCSL2.png"))
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
        w.show()

    def startServer(self):
        if self.serverProcessHandler is not None:
            if not self.serverProcessHandler.isServerRunning():
                t = self.serverProcessHandler.startServer()
                if isinstance(t, _MinecraftEULA):
                    self._showNoAcceptEULAMsg(t)
                else:
                    return
            else:
                return
        else:
            t = self.serverLauncher.start()
            if isinstance(t, _MinecraftEULA):
                self._showNoAcceptEULAMsg(t)
            else:
                self.serverProcessHandler = t

    def registerResMonitor(self):
        self.serverMemThread = MinecraftServerResMonitorUtil(self)
        self.serverMemThread.memPercent.connect(self.setMemView)
        self.serverMemThread.cpuPercent.connect(self.setCPUView)

        self.serverProcessHandler.serverClosed.connect(self.unRegisterResMonitor)

    def unRegisterResMonitor(self):
        self.serverMemThread.memPercent.disconnect(self.setMemView)
        self.serverMemThread.cpuPercent.disconnect(self.setCPUView)
        self.serverMemThread.onServerClosedHandler()
        self.serverMemThread.deleteLater()
        del self.serverMemThread

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
        readServerProperties()
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
                position=InfoBarPosition.TOP,
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
                self.tr("[MCSL2 | 提示]：服务器启动完毕！\n[MCSL2 | 提示]：如果本机开服，IP 地址为") + ip + self.tr("，端口为") + port + self.tr("。\n[MCSL2 | 提示]：如果外网开服,或使用了内网穿透等服务，连接地址为你的相关服务地址。")  # noqa: E501
            )
            InfoBar.success(
                title=self.tr("提示"),
                content=self.tr("服务器启动完毕！\n如果本机开服，IP 地址为") + ip + self.tr("，端口为") + port + self.tr("。\n如果外网开服,或使用了内网穿透等服务，连接地址为你的相关服务地址。"),  # noqa: E501
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
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
        if self.errorHandler.isChecked():
            if self.errMsg != "":
                w = MessageBox("错误分析器日志", self.errMsg, self)
                w.cancelButton.setParent(None)
                w.show()
            else:
                w = MessageBox(
                    "错误分析器日志", "本次没有检测到任何MCSL2内置错误分析可用解决方案。", self
                )
                w.cancelButton.setParent(None)
                w.show()

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
            except Exception as e:
                MCSL2Logger.error(
                    msg=f"extract player name failed\nonRecordPlayers::logout {serverOutput}",
                    exc=e,
                )

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a0 == self.commandPage and a1.type() == QEvent.KeyPress:
            if a1.key() == Qt.Key_Return or a1.key() == Qt.Key_Enter:
                if self.stackedWidget.currentIndex() == 1 and self.commandLineEdit:
                    self.sendCommandButton.click()
                    return True
            elif a1.key() == Qt.Key_Up:
                if self.stackedWidget.currentIndex() == 1 and self.commandLineEdit:
                    if len(
                        GlobalMCSL2Variables.userCommandHistory
                    ) and GlobalMCSL2Variables.upT > -len(GlobalMCSL2Variables.userCommandHistory):
                        GlobalMCSL2Variables.upT -= 1
                        lastCommand = GlobalMCSL2Variables.userCommandHistory[
                            GlobalMCSL2Variables.upT
                        ]
                        self.commandLineEdit.setText(lastCommand)
                        return True
            elif a1.key() == Qt.Key_Down:
                if self.stackedWidget.currentIndex() == 1 and self.commandLineEdit:
                    if (
                        len(GlobalMCSL2Variables.userCommandHistory)
                        and GlobalMCSL2Variables.upT < 0
                    ):
                        GlobalMCSL2Variables.upT += 1
                        nextCommand = GlobalMCSL2Variables.userCommandHistory[
                            GlobalMCSL2Variables.upT
                        ]
                        self.commandLineEdit.setText(nextCommand)
                        return True
                    if (
                        len(GlobalMCSL2Variables.userCommandHistory)
                        and GlobalMCSL2Variables.upT == 0
                    ):
                        self.commandLineEdit.setText("")
                        return True
        return super().eventFilter(a0, a1)

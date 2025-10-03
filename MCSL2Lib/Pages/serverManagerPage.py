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
Manage exists Minecraft servers.
"""

from json import dump, loads, dumps
from os import getcwd, rename, path as osp, remove
import platform
from shutil import copy, rmtree
from pyqt5_concurrent.TaskExecutor import TaskExecutor  # type: ignore

from PyQt5.QtCore import Qt, QRect, QSize, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import (
    QApplication,
    QSizePolicy,
    QFrame,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QSpacerItem,
    QHBoxLayout,
    QFileDialog,
)
from qfluentwidgets import (
    BodyLabel,
    ComboBox,
    PixmapLabel,
    LineEdit,
    PlainTextEdit,
    PrimaryPushButton,
    PushButton,
    StrongBodyLabel,
    SubtitleLabel,
    TextEdit,
    TitleLabel,
    TransparentToolButton,
    FluentIcon as FIF,
    Dialog,
    MessageBox,
    InfoBar,
    InfoBarPosition,
    StateToolTip,
    isDarkTheme,
    FlowLayout,
)

from MCSL2Lib.ProgramControllers import javaDetector
from MCSL2Lib.ProgramControllers.interfaceController import ChildStackedWidget
from MCSL2Lib.ServerControllers.processCreator import ServerConfigConstructor
from MCSL2Lib.ServerControllers.serverInstaller import ForgeInstaller
from MCSL2Lib.ProgramControllers.serverValidator import ServerValidator
from MCSL2Lib.ProgramControllers.settingsController import cfg
from MCSL2Lib.Resources.icons import *  # noqa: F401 F403
from MCSL2Lib.ProgramControllers.interfaceController import MySmoothScrollArea
from MCSL2Lib.ServerControllers.windowCreator import ServerWindow
from MCSL2Lib.ServerControllers.processCreator import ServerLauncher
from MCSL2Lib.ServerControllers.serverUtils import backupServer, backupSaves
from MCSL2Lib.Widgets.noServerTip import NoServerWidget
from MCSL2Lib.Widgets.serverManagerWidget import SingleServerManager
from MCSL2Lib.Widgets.singleRunningServerWidget import RunningServerHeaderCardWidget
from MCSL2Lib.Widgets.exceptionWidget import ExceptionWidget
from MCSL2Lib.singleton import Singleton

# from MCSL2Lib.Controllers.interfaceController import ChildStackedWidget
from MCSL2Lib.utils import (
    openLocalFile,
    readGlobalServerConfig,
    MCSL2Logger,
    readFile,
    writeFile,
)
from MCSL2Lib.variables import GlobalMCSL2Variables, EditServerVariables


editServerVariables = EditServerVariables()


@Singleton
class ServerManagerPage(QWidget):
    """服务器管理页"""

    deleteBtnEnabled = pyqtSignal(bool)
    runningServerCardGenerated = pyqtSignal(RunningServerHeaderCardWidget)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.javaFindWorkThreadFactory = javaDetector.JavaFindWorkThreadFactory()
        self.javaFindWorkThreadFactory.fSearch = True
        self.javaFindWorkThreadFactory.signalConnect = self.autoDetectJavaFinished
        self.javaFindWorkThreadFactory.finishSignalConnect = self.onJavaFindWorkThreadFinished

        self.serverList = []
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.gridLayout_2 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayout_2.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.gridLayout_2.addWidget(self.subTitleLabel, 1, 0, 1, 1)
        self.stackedWidget = ChildStackedWidget(self.titleLimitWidget)
        self.stackedWidget.setObjectName("stackedWidget")

        self.serversPage = QWidget()
        self.serversPage.setObjectName("serversPage")

        self.verticalLayout_2 = QVBoxLayout(self.serversPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.serversSmoothScrollArea = MySmoothScrollArea(self.serversPage)
        self.serversSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.serversSmoothScrollArea.setFrameShadow(QFrame.Plain)
        self.serversSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.serversSmoothScrollArea.setWidgetResizable(True)
        self.serversSmoothScrollArea.setObjectName("serversSmoothScrollArea")

        self.serversScrollAreaWidgetContents = QWidget()
        self.serversScrollAreaWidgetContents.setGeometry(QRect(0, 0, 640, 452))
        self.serversScrollAreaWidgetContents.setObjectName("serversScrollAreaWidgetContents")

        self.flowLayout = FlowLayout(self.serversScrollAreaWidgetContents)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setObjectName("flowLayout")

        self.serversSmoothScrollArea.setWidget(self.serversScrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.serversSmoothScrollArea)
        self.stackedWidget.addWidget(self.serversPage)
        self.editServerPage = QWidget()
        self.editServerPage.setObjectName("editServerPage")

        self.gridLayout_3 = QGridLayout(self.editServerPage)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.editServerScrollArea = MySmoothScrollArea(self.editServerPage)
        self.editServerScrollArea.setFrameShape(QFrame.NoFrame)
        self.editServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.editServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.editServerScrollArea.setWidgetResizable(True)
        self.editServerScrollArea.setObjectName("editServerScrollArea")

        self.editServerScrollAreaContents = QWidget()
        self.editServerScrollAreaContents.setGeometry(QRect(0, -427, 623, 871))
        self.editServerScrollAreaContents.setObjectName("editServerScrollAreaContents")

        self.editNewServerScrollAreaVerticalLayout_2 = QVBoxLayout(
            self.editServerScrollAreaContents
        )
        self.editNewServerScrollAreaVerticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.editNewServerScrollAreaVerticalLayout_2.setObjectName(
            "editNewServerScrollAreaVerticalLayout_2"
        )

        self.editSetJavaWidget = QWidget(self.editServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editSetJavaWidget.sizePolicy().hasHeightForWidth())
        self.editSetJavaWidget.setSizePolicy(sizePolicy)
        self.editSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.editSetJavaWidget.setObjectName("editSetJavaWidget")

        self.gridLayout_6 = QGridLayout(self.editSetJavaWidget)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.editAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(self.editSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.editAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.editAutoDetectJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.editAutoDetectJavaPrimaryPushBtn.setObjectName("editAutoDetectJavaPrimaryPushBtn")

        self.gridLayout_6.addWidget(self.editAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1)
        self.editJavaSubtitleLabel = SubtitleLabel(self.editSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editJavaSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.editJavaSubtitleLabel.setObjectName("editJavaSubtitleLabel")

        self.gridLayout_6.addWidget(self.editJavaSubtitleLabel, 0, 0, 1, 1)
        self.editJavaListPushBtn = PushButton(self.editSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editJavaListPushBtn.sizePolicy().hasHeightForWidth())
        self.editJavaListPushBtn.setSizePolicy(sizePolicy)
        self.editJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.editJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.editJavaListPushBtn.setObjectName("editJavaListPushBtn")

        self.gridLayout_6.addWidget(self.editJavaListPushBtn, 3, 2, 1, 1)
        self.editManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(self.editSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.editManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.editManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.editManuallyAddJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.editManuallyAddJavaPrimaryPushBtn.setObjectName("editManuallyAddJavaPrimaryPushBtn")

        self.gridLayout_6.addWidget(self.editManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1)
        self.editDownloadJavaPrimaryPushBtn = PrimaryPushButton(self.editSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.editDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.editDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.editDownloadJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.editDownloadJavaPrimaryPushBtn.setObjectName("editDownloadJavaPrimaryPushBtn")

        self.gridLayout_6.addWidget(self.editDownloadJavaPrimaryPushBtn, 3, 1, 1, 1)
        self.editJavaTextEdit = TextEdit(self.editSetJavaWidget)
        self.editJavaTextEdit.setObjectName("editJavaTextEdit")

        self.gridLayout_6.addWidget(self.editJavaTextEdit, 2, 0, 2, 1)
        self.editNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetJavaWidget)
        self.editSetMemWidget = QWidget(self.editServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editSetMemWidget.sizePolicy().hasHeightForWidth())
        self.editSetMemWidget.setSizePolicy(sizePolicy)
        self.editSetMemWidget.setObjectName("editSetMemWidget")

        self.gridLayout_7 = QGridLayout(self.editSetMemWidget)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.editToSymbol = SubtitleLabel(self.editSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editToSymbol.sizePolicy().hasHeightForWidth())
        self.editToSymbol.setSizePolicy(sizePolicy)
        self.editToSymbol.setObjectName("editToSymbol")

        self.gridLayout_7.addWidget(self.editToSymbol, 1, 2, 1, 1)
        self.editMemUnitComboBox = ComboBox(self.editSetMemWidget)
        self.editMemUnitComboBox.setObjectName("editMemUnitComboBox")
        self.gridLayout_7.addWidget(self.editMemUnitComboBox, 1, 4, 1, 1)
        self.editMaxMemLineEdit = LineEdit(self.editSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editMaxMemLineEdit.sizePolicy().hasHeightForWidth())
        self.editMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.editMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.editMaxMemLineEdit.setObjectName("editMaxMemLineEdit")

        self.gridLayout_7.addWidget(self.editMaxMemLineEdit, 1, 3, 1, 1)
        self.editMemSubtitleLabel = SubtitleLabel(self.editSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editMemSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.editMemSubtitleLabel.setObjectName("editMemSubtitleLabel")

        self.gridLayout_7.addWidget(self.editMemSubtitleLabel, 0, 1, 1, 1)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem2, 1, 5, 1, 1)
        self.editMinMemLineEdit = LineEdit(self.editSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editMinMemLineEdit.sizePolicy().hasHeightForWidth())
        self.editMinMemLineEdit.setSizePolicy(sizePolicy)
        self.editMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.editMinMemLineEdit.setObjectName("editMinMemLineEdit")

        self.gridLayout_7.addWidget(self.editMinMemLineEdit, 1, 1, 1, 1)
        self.editNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetMemWidget)
        self.editSetCoreWidget = QWidget(self.editServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editSetCoreWidget.sizePolicy().hasHeightForWidth())
        self.editSetCoreWidget.setSizePolicy(sizePolicy)
        self.editSetCoreWidget.setObjectName("editSetCoreWidget")

        self.gridLayout_8 = QGridLayout(self.editSetCoreWidget)
        self.gridLayout_8.setObjectName("gridLayout_8")

        self.editDownloadCorePrimaryPushBtn = PrimaryPushButton(self.editSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.editDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.editDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.editDownloadCorePrimaryPushBtn.setObjectName("editDownloadCorePrimaryPushBtn")

        self.gridLayout_8.addWidget(self.editDownloadCorePrimaryPushBtn, 1, 3, 1, 1)
        self.editCoreSubtitleLabel = SubtitleLabel(self.editSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editCoreSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.editCoreSubtitleLabel.setObjectName("editCoreSubtitleLabel")

        self.gridLayout_8.addWidget(self.editCoreSubtitleLabel, 0, 1, 1, 1)
        self.coreLineEdit = LineEdit(self.editSetCoreWidget)
        self.coreLineEdit.setObjectName("coreLineEdit")

        self.gridLayout_8.addWidget(self.coreLineEdit, 1, 1, 1, 1)
        self.editManuallyAddCorePrimaryPushBtn = PrimaryPushButton(self.editSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.editManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.editManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.editManuallyAddCorePrimaryPushBtn.setObjectName("editManuallyAddCorePrimaryPushBtn")

        self.gridLayout_8.addWidget(self.editManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1)
        self.editNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetCoreWidget)
        self.editSetDeEncodingWidget = QWidget(self.editServerScrollAreaContents)
        self.editSetDeEncodingWidget.setObjectName("editSetDeEncodingWidget")

        self.gridLayout_9 = QGridLayout(self.editSetDeEncodingWidget)
        self.gridLayout_9.setObjectName("gridLayout_9")

        self.editOutputDeEncodingComboBox = ComboBox(self.editSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.editOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.editOutputDeEncodingComboBox.setObjectName("editOutputDeEncodingComboBox")

        self.gridLayout_9.addWidget(self.editOutputDeEncodingComboBox, 2, 1, 1, 1)
        self.editDeEncodingSubtitleLabel = SubtitleLabel(self.editSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.editDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.editDeEncodingSubtitleLabel.setObjectName("editDeEncodingSubtitleLabel")

        self.gridLayout_9.addWidget(self.editDeEncodingSubtitleLabel, 0, 0, 1, 1)
        self.editInputDeEncodingComboBox = ComboBox(self.editSetDeEncodingWidget)
        self.editInputDeEncodingComboBox.setText("")
        self.editInputDeEncodingComboBox.setObjectName("editInputDeEncodingComboBox")

        self.gridLayout_9.addWidget(self.editInputDeEncodingComboBox, 3, 1, 1, 1)
        self.editOutputDeEncodingLabel = StrongBodyLabel(self.editSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.editOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.editOutputDeEncodingLabel.setObjectName("editOutputDeEncodingLabel")

        self.gridLayout_9.addWidget(self.editOutputDeEncodingLabel, 2, 0, 1, 1)
        self.editInputDeEncodingLabel = StrongBodyLabel(self.editSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editInputDeEncodingLabel.sizePolicy().hasHeightForWidth())
        self.editInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.editInputDeEncodingLabel.setObjectName("editInputDeEncodingLabel")

        self.gridLayout_9.addWidget(self.editInputDeEncodingLabel, 3, 0, 1, 1)
        self.editNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetDeEncodingWidget)
        self.editSetJVMArgWidget = QWidget(self.editServerScrollAreaContents)
        self.editSetJVMArgWidget.setObjectName("editSetJVMArgWidget")

        self.gridLayout_10 = QGridLayout(self.editSetJVMArgWidget)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.editJVMArgSubtitleLabel = SubtitleLabel(self.editSetJVMArgWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.editJVMArgSubtitleLabel.setObjectName("editJVMArgSubtitleLabel")

        self.gridLayout_10.addWidget(self.editJVMArgSubtitleLabel, 0, 0, 1, 1)
        self.JVMArgPlainTextEdit = PlainTextEdit(self.editSetJVMArgWidget)
        self.JVMArgPlainTextEdit.setObjectName("JVMArgPlainTextEdit")

        self.gridLayout_10.addWidget(self.JVMArgPlainTextEdit, 1, 0, 1, 1)
        self.editNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetJVMArgWidget)
        self.editSetServerIconWidget = QWidget(self.editServerScrollAreaContents)
        self.editSetServerIconWidget.setObjectName("editSetServerIconWidget")

        self.gridLayout_4 = QGridLayout(self.editSetServerIconWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.tipLabel = BodyLabel(self.editSetServerIconWidget)
        self.tipLabel.setObjectName("tipLabel")

        self.gridLayout_4.addWidget(self.tipLabel, 2, 0, 1, 4)
        self.editServerIcon = ComboBox(self.editSetServerIconWidget)
        self.editServerIcon.setObjectName("editServerIcon")

        self.gridLayout_4.addWidget(self.editServerIcon, 4, 0, 1, 1)
        self.editServerIconSubtitleLabel = SubtitleLabel(self.editSetServerIconWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editServerIconSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.editServerIconSubtitleLabel.setSizePolicy(sizePolicy)
        self.editServerIconSubtitleLabel.setObjectName("editServerIconSubtitleLabel")

        self.gridLayout_4.addWidget(self.editServerIconSubtitleLabel, 0, 0, 1, 1)
        self.editServerPixmapLabel = PixmapLabel(self.editSetServerIconWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editServerPixmapLabel.sizePolicy().hasHeightForWidth())
        self.editServerPixmapLabel.setSizePolicy(sizePolicy)
        self.editServerPixmapLabel.setObjectName("editServerPixmapLabel")

        self.gridLayout_4.addWidget(self.editServerPixmapLabel, 4, 2, 1, 1)
        spacerItem3 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 4, 1, 1, 1)
        self.editNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetServerIconWidget)
        self.editSetServerNameWidget = QWidget(self.editServerScrollAreaContents)
        self.editSetServerNameWidget.setObjectName("editSetServerNameWidget")

        self.verticalLayout_5 = QVBoxLayout(self.editSetServerNameWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.editServerNameSubtitleLabel = SubtitleLabel(self.editSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editServerNameSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.editServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.editServerNameSubtitleLabel.setObjectName("editServerNameSubtitleLabel")

        self.verticalLayout_5.addWidget(self.editServerNameSubtitleLabel)
        self.editServerNameLineEdit = LineEdit(self.editSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editServerNameLineEdit.sizePolicy().hasHeightForWidth())
        self.editServerNameLineEdit.setSizePolicy(sizePolicy)
        self.editServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.editServerNameLineEdit.setObjectName("editServerNameLineEdit")

        self.verticalLayout_5.addWidget(self.editServerNameLineEdit)
        self.editSaveServerPrimaryPushBtn = PrimaryPushButton(self.editSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.editSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.editSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.editSaveServerPrimaryPushBtn.setObjectName("editSaveServerPrimaryPushBtn")

        self.verticalLayout_5.addWidget(self.editSaveServerPrimaryPushBtn)
        self.editNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetServerNameWidget)
        spacerItem4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.editNewServerScrollAreaVerticalLayout_2.addItem(spacerItem4)
        self.editServerScrollArea.setWidget(self.editServerScrollAreaContents)
        self.gridLayout_3.addWidget(self.editServerScrollArea, 1, 0, 1, 1)
        self.editServerTitleWidget = QWidget(self.editServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editServerTitleWidget.sizePolicy().hasHeightForWidth())
        self.editServerTitleWidget.setSizePolicy(sizePolicy)
        self.editServerTitleWidget.setObjectName("editServerTitleWidget")

        self.horizontalLayout_4 = QHBoxLayout(self.editServerTitleWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.editServerBackPushBtn = TransparentToolButton(
            FIF.PAGE_LEFT, self.editServerTitleWidget
        )
        self.editServerBackPushBtn.setObjectName("editServerBackPushBtn")

        self.horizontalLayout_4.addWidget(self.editServerBackPushBtn)
        self.editServerSubtitleLabel = SubtitleLabel(self.editServerTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editServerSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editServerSubtitleLabel.setSizePolicy(sizePolicy)
        self.editServerSubtitleLabel.setObjectName("editServerSubtitleLabel")
        self.horizontalLayout_4.addWidget(self.editServerSubtitleLabel)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.gridLayout_3.addWidget(self.editServerTitleWidget, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.editServerPage)
        self.gridLayout_2.addWidget(self.stackedWidget, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 2, 2)

        self.setObjectName("ManagerInterface")

        self.subTitleLabel.setText(self.tr("在此处，管理你所有的服务器。"))
        self.titleLabel.setText(self.tr("管理"))
        self.editAutoDetectJavaPrimaryPushBtn.setText(self.tr("自动查找 Java"))
        self.editJavaSubtitleLabel.setText(self.tr("Java: "))
        self.editJavaListPushBtn.setText(self.tr("Java 列表"))
        self.editManuallyAddJavaPrimaryPushBtn.setText(self.tr("手动导入"))
        self.editDownloadJavaPrimaryPushBtn.setText(self.tr("下载 Java"))
        self.editToSymbol.setText("~")
        self.editMemSubtitleLabel.setText(self.tr("内存"))
        self.editDownloadCorePrimaryPushBtn.setText(self.tr("下载核心"))
        self.editCoreSubtitleLabel.setText(self.tr("核心"))
        self.editManuallyAddCorePrimaryPushBtn.setText(self.tr("重新导入"))
        self.editDeEncodingSubtitleLabel.setText(self.tr("编码设置"))
        self.editOutputDeEncodingLabel.setText(self.tr("控制台输出编码 (优先级高于全局设置)"))
        self.editInputDeEncodingLabel.setText(self.tr("指令输入编码 (优先级高于全局设置)"))
        self.editJVMArgSubtitleLabel.setText(self.tr("JVM 参数"))
        self.JVMArgPlainTextEdit.setPlaceholderText(self.tr("可选，用一个空格分组"))
        self.editServerIconSubtitleLabel.setText(self.tr("服务器图标"))
        self.tipLabel.setText(
            self.tr("提示：此处设置的是服务器在 MCSL2 中显示的图标，不能代表服务器 MOTD 的图标。")
        )
        self.editServerNameSubtitleLabel.setText(self.tr("服务器名称"))
        self.editServerNameLineEdit.setPlaceholderText(self.tr("不能包含非法字符"))
        self.editSaveServerPrimaryPushBtn.setText(self.tr("保存！"))
        self.editServerBackPushBtn.clicked.connect(self.goBack)
        self.serversSmoothScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.editServerScrollArea.setAttribute(Qt.WA_StyledBackground)

        self.editJavaTextEdit.setPlaceholderText(self.tr("写错了就启动不了了（悲"))
        self.editMinMemLineEdit.setPlaceholderText(self.tr("整数"))
        self.editMaxMemLineEdit.setPlaceholderText(self.tr("整数"))
        self.editServerNameLineEdit.setPlaceholderText(self.tr("不能包含非法字符"))
        self.JVMArgPlainTextEdit.setPlaceholderText(self.tr("可选，用一个空格分组"))
        self.editOutputDeEncodingComboBox.addItems(
            [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI")]
            if platform.system().lower() == "windows"
            else [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030")]
        )
        self.editInputDeEncodingComboBox.addItems(
            [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI")]
            if platform.system().lower() == "windows"
            else [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030")]
        )
        self.editMemUnitComboBox.addItems([self.tr("M"), self.tr("G")])

        self.editManuallyAddJavaPrimaryPushBtn.clicked.connect(self.replaceJavaManually)
        self.editAutoDetectJavaPrimaryPushBtn.clicked.connect(self.autoDetectJava)
        self.editSaveServerPrimaryPushBtn.clicked.connect(self.finishEditServer)
        self.coreLineEdit.setEnabled(False)
        self.iconsList = [
            self.tr("铁砧"),
            self.tr("布料"),
            self.tr("圆石"),
            self.tr("命令方块"),
            self.tr("工作台"),
            self.tr("鸡蛋"),
            self.tr("玻璃"),
            self.tr("金块"),
            self.tr("草方块"),
            self.tr("草径"),
            self.tr("Java"),
            self.tr("MCSL2"),
            self.tr("Paper 核心"),
            self.tr("红石块"),
            self.tr("关闭的红石灯"),
            self.tr("打开的红石灯"),
            self.tr("Spigot核心"),
        ]
        self.editServerIcon.addItems(self.iconsList)
        self.editServerIcon.setMaxVisibleItems(8)

    def goBack(self):
        # 没改就直接退出
        if self.checkDuplicateConfig():
            self.stackedWidget.setCurrentIndex(0)
            self.disconnectEditServerSlot()
        # 改了得确认
        else:
            w = MessageBox(
                parent=self,
                title=self.tr("是否要退出此页面？"),
                content=self.tr("任何没有保存的修改都会消失！你确定要这么做吗？"),
            )
            w.yesButton.setText(self.tr("取消"))
            w.cancelButton.setText(self.tr("退出"))
            w.cancelButton.setStyleSheet(
                GlobalMCSL2Variables.darkWarnBtnStyleSheet
                if isDarkTheme()
                else GlobalMCSL2Variables.lightWarnBtnStyleSheet
            )
            w.cancelButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
            w.cancelButton.clicked.connect(self.disconnectEditServerSlot)
            w.cancelButton.clicked.connect(self.refreshServers)
            w.exec()

    @pyqtSlot(int)
    def onPageChangedRefresh(self, currentChanged):
        if currentChanged == 2:
            self.refreshServers()

    def releaseMemory(self):
        self.flowLayout.takeAllWidgets()

    def refreshServers(self):
        """刷新服务器列表主逻辑"""
        # 读取全局设置
        globalConfig = readGlobalServerConfig()
        serverList = [config["name"] for config in globalConfig if "name" in config]
        if len(globalConfig):
            self.releaseMemory()
            # 添加新的
            for i in range(len(globalConfig)):
                # 获取服务器类型,默认为 java
                serverType = globalConfig[i].get("server_type", "java")
                
                self.flowLayout.addWidget(
                    SingleServerManager(
                        mem=f"{globalConfig[i]['min_memory']}{globalConfig[i]['memory_unit']}~{globalConfig[i]['max_memory']}{globalConfig[i]['memory_unit']}",
                        coreFileName=f"{globalConfig[i]['core_file_name']}",
                        javaPath=f"{globalConfig[i]['java_path']}",
                        serverName=f"{globalConfig[i]['name']}",
                        icon=QPixmap(f":/built-InIcons/{globalConfig[i]['icon']}"),
                        btnSlot=self.scrollAreaProcessor,
                        i=i,
                        serverType=serverType,  # 传递服务器类型
                        parent=self.serversSmoothScrollArea,
                    )
                )
            self.serverList = serverList
        else:
            self.releaseMemory()
            noServerWidget = NoServerWidget()
            self.flowLayout.addWidget(noServerWidget)

    # 判断第几个
    def scrollAreaProcessor(self):
        self.globalServerConfig = readGlobalServerConfig()
        type = str(self.sender().objectName()).split("!")[0]
        index = int(str(self.sender().objectName()).split("!")[1])
        if type == "startServer":
            self.startServer(index=index)
        elif type == "editServer":
            self.initEditServerInterface(index=index)
        elif type == "editServerConfig":
            self.startServer(index=index, isEditingConfig=True)
        elif type == "backupFullServer":
            backupServer(
                ServerConfigConstructor.loadServerConfig(index=index).serverName,
                parent=self,
            )
        elif type == "backupServerSaves":
            backupSaves(ServerConfigConstructor.loadServerConfig(index=index), parent=self)
        elif type == "openDataFolder":
            openLocalFile(f"./Servers/{self.globalServerConfig[index]['name']}")
        elif type == "deleteServer":
            self.deleteServer_Step1(index=index)

    ##################
    #    删除服务器    #
    ##################
    def deleteServer_Step1(self, index):
        """删除服务器步骤1，询问是否删除"""
        # exec() 返回1:取消，0:继续(此处)
        title = self.tr('是否要删除服务器"') + self.globalServerConfig[index]["name"] + '"?'
        content = self.tr("此操作是不可逆的！你确定这么做吗？")
        w = MessageBox(title, content, self)
        w.yesButton.setText(self.tr("取消"))
        w.cancelButton.setText(self.tr("删除"))
        w.cancelButton.setStyleSheet(
            GlobalMCSL2Variables.darkWarnBtnStyleSheet
            if isDarkTheme()
            else GlobalMCSL2Variables.lightWarnBtnStyleSheet
        )
        if w.exec() == 1:
            return

        """删除服务器步骤2：输入确认"""
        globalConfig: list = readGlobalServerConfig()
        title = self.tr('你真的要删除服务器"') + globalConfig[index]["name"] + self.tr('"?')
        content = (
            self.tr('此操作是不可逆的！它会失去很久，很久！\n如果真的要删除，请在下方输入框内输入"')
            + globalConfig[index]["name"]
            + self.tr('"，然后点击「删除」按钮：')
        )
        w2 = MessageBox(title, content, self)
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
            lambda: self.compareDeleteServerName(
                name=globalConfig[index]["name"], LineEditText=confirmLineEdit.text()
            )
        )
        confirmLineEdit.setPlaceholderText(self.tr('在此输入"') + globalConfig[index]["name"] + '"')
        self.deleteBtnEnabled.connect(w2.cancelButton.setEnabled)
        w2.textLayout.addWidget(confirmLineEdit)
        if w2.exec() == 1:
            return

        """删除服务器步骤3：弹窗提示正在删除"""
        globalConfig: list = readGlobalServerConfig()
        delServerName = globalConfig[index]["name"]

        self.deletingServerStateToolTip = StateToolTip(
            self.tr("删除服务器"), self.tr("请稍后，正在删除..."), self
        )
        self.deletingServerStateToolTip.move(self.deletingServerStateToolTip.getSuitablePos())
        self.deletingServerStateToolTip.show()

        # 真正删除服务器文件夹

        globalServerList = loads(readFile(r"MCSL2/MCSL2_ServerList.json"))
        globalServerList["MCSLServerList"].pop(index)
        writeFile(r"MCSL2/MCSL2_ServerList.json", dumps(globalServerList, indent=4))

        def onFinished(_):
            self.deletingServerStateToolTip.setState(True)
            self.deletingServerStateToolTip = None
            self.refreshServers()

        TaskExecutor.run(rmtree, f"Servers/{delServerName}").then(
            onSuccess=lambda: self.deletingServerStateToolTip.setContent(self.tr("删除完毕。")),
            onFailed=lambda e: self.deletingServerStateToolTip.setContent(
                self.tr("删除失败！\n") + str(e)
            ),
            onFinished=onFinished,
        )

    def compareDeleteServerName(self, name, LineEditText):
        """删除服务器步骤2：输入确认的检查，不一样就不启用删除按钮直到输入正确"""
        self.deleteBtnEnabled.emit(name == LineEditText)

    ##################
    #    编辑服务器    #
    ##################
    def initEditServerInterface(self, index):
        """初始化编辑服务器界面"""
        self.autoDetectJava()
        globalConfig: list = readGlobalServerConfig()
        self.stackedWidget.setCurrentIndex(1)
        self.serverIndex = index
        
        # 获取服务器类型
        serverType = globalConfig[index].get("server_type", "java")
        isBedrockServer = (serverType == "bedrock")
        
        # 自动填充旧配置。在下方初始化变量之前不应调用任何的editServerVariables的属性
        self.editServerSubtitleLabel.setText(
            self.tr("编辑服务器") + f"-{globalConfig[index]['name']}"
            + (self.tr(" [基岩版]") if isBedrockServer else "")
        )
        
        # 根据服务器类型显示/隐藏控件
        if isBedrockServer:
            # 隐藏Java相关控件
            self.editSetJavaWidget.setVisible(False)
            # 隐藏内存相关控件
            self.editSetMemWidget.setVisible(False)
            # 隐藏JVM参数控件
            self.editSetJVMArgWidget.setVisible(False)
            self.editDownloadCorePrimaryPushBtn.setVisible(False)
            self.editManuallyAddCorePrimaryPushBtn.setVisible(False)
        else:
            # 显示所有Java版控件
            self.editSetJavaWidget.setVisible(True)
            self.editSetMemWidget.setVisible(True)
            self.editSetJVMArgWidget.setVisible(True)
            self.editDownloadCorePrimaryPushBtn.setVisible(True)
            self.editManuallyAddCorePrimaryPushBtn.setVisible(True)
            
            # 填充Java版配置
            self.editJavaTextEdit.setText(globalConfig[index]["java_path"])
            self.editMinMemLineEdit.setText(str(globalConfig[index]["min_memory"]))
            self.editMaxMemLineEdit.setText(str(globalConfig[index]["max_memory"]))
            self.editMemUnitComboBox.setCurrentIndex(
                editServerVariables.memUnitList.index(globalConfig[index]["memory_unit"])
            )
            totalJVMArg = ""
            for arg in globalConfig[index]["jvm_arg"]:
                totalJVMArg += f"{arg} "
            totalJVMArg = totalJVMArg.strip()
            self.JVMArgPlainTextEdit.setPlainText(totalJVMArg)
        
        # 通用配置(Java版和基岩版都有)
        self.editOutputDeEncodingComboBox.setCurrentIndex(
            editServerVariables.consoleDeEncodingList.index(globalConfig[index]["output_decoding"])
        )
        self.editInputDeEncodingComboBox.setCurrentIndex(
            editServerVariables.consoleDeEncodingList.index(globalConfig[index]["input_encoding"])
        )
        self.coreLineEdit.setText(globalConfig[index]["core_file_name"])
        self.editServerNameLineEdit.setText(globalConfig[index]["name"])

        self.editServerPixmapLabel.setPixmap(
            QPixmap(f":/built-InIcons/{globalConfig[index]['icon']}")
        )
        self.editServerIcon.setCurrentIndex(
            editServerVariables.iconsFileNameList.index(globalConfig[index]["icon"])
        )
        self.editServerPixmapLabel.setFixedSize(QSize(60, 60))

        """初始化变量"""
        editServerVariables.minMem = globalConfig[index]["min_memory"]
        editServerVariables.maxMem = globalConfig[index]["max_memory"]
        editServerVariables.coreFileName = globalConfig[index]["core_file_name"]
        (editServerVariables.selectedJavaPath) = globalConfig[index]["java_path"]
        editServerVariables.memUnit = globalConfig[index]["memory_unit"]
        editServerVariables.jvmArg = globalConfig[index]["jvm_arg"]
        editServerVariables.serverName = globalConfig[index]["name"]
        (editServerVariables.consoleOutputDeEncoding) = globalConfig[index]["output_decoding"]
        (editServerVariables.consoleInputDeEncoding) = globalConfig[index]["input_encoding"]
        editServerVariables.icon = globalConfig[index]["icon"]
        try:
            editServerVariables.serverType = globalConfig[index]["server_type"]
            editServerVariables.extraData = globalConfig[index]["extra_data"]
        except Exception:
            pass
        self.syncVariables()
        # 初始化QtSlot
        self.connectEditServerSlot(isBedrockServer)

    def syncVariables(self):
        editServerVariables.oldMinMem = editServerVariables.minMem
        editServerVariables.oldMaxMem = editServerVariables.maxMem
        editServerVariables.oldCoreFileName = editServerVariables.coreFileName
        editServerVariables.oldSelectedJavaPath = editServerVariables.selectedJavaPath
        editServerVariables.oldMemUnit = editServerVariables.memUnit
        editServerVariables.oldJVMArg = editServerVariables.jvmArg
        editServerVariables.oldServerName = editServerVariables.serverName
        editServerVariables.oldConsoleOutputDeEncoding = editServerVariables.consoleOutputDeEncoding
        editServerVariables.oldConsoleInputDeEncoding = editServerVariables.consoleInputDeEncoding
        editServerVariables.oldIcon = editServerVariables.icon
        editServerVariables.oldServerType = editServerVariables.serverType
        editServerVariables.oldExtraData = editServerVariables.extraData

    def connectEditServerSlot(self, isBedrockServer=False):
        """连接编辑服务器的信号槽"""
        # 基岩版服务器不连接Java和内存相关的槽
        if not isBedrockServer:
            self.editJavaTextEdit.textChanged.connect(self.changeJavaPath)
            self.editMinMemLineEdit.textChanged.connect(self.changeMinMem)
            self.editMaxMemLineEdit.textChanged.connect(self.changeMaxMem)
            self.editMemUnitComboBox.currentIndexChanged.connect(self.changeMemUnit)
            self.JVMArgPlainTextEdit.textChanged.connect(self.changeJVMArg)
        
        # 通用槽连接(Java版和基岩版都需要)
        self.editManuallyAddCorePrimaryPushBtn.clicked.connect(
            self.changeBedrockCore if isBedrockServer else self.changeCore
        )
        self.editOutputDeEncodingComboBox.currentIndexChanged.connect(self.changeOutputDeEncoding)
        self.editInputDeEncodingComboBox.currentIndexChanged.connect(self.changeInputDeEncoding)
        self.editServerIcon.currentIndexChanged.connect(
            lambda: self.changeIcon(iconIndex=self.editServerIcon.currentIndex())
        )
        self.editServerNameLineEdit.textChanged.connect(self.changeServerName)

    def disconnectEditServerSlot(self):
        self.editJavaTextEdit.textChanged.disconnect()
        self.editMinMemLineEdit.textChanged.disconnect()
        self.editMaxMemLineEdit.textChanged.disconnect()
        self.editMemUnitComboBox.currentIndexChanged.disconnect()
        self.editManuallyAddCorePrimaryPushBtn.clicked.disconnect()
        self.editOutputDeEncodingComboBox.currentIndexChanged.disconnect()
        self.editInputDeEncodingComboBox.currentIndexChanged.disconnect()
        self.editServerIcon.currentIndexChanged.disconnect()
        self.editServerNameLineEdit.textChanged.disconnect()
        self.JVMArgPlainTextEdit.textChanged.disconnect()

    def changeIcon(self, iconIndex):
        """改图标用"""
        editServerVariables.icon = editServerVariables.iconsFileNameList[iconIndex]
        self.editServerPixmapLabel.setPixmap(
            QPixmap(f":/built-InIcons/{editServerVariables.iconsFileNameList[iconIndex]}")
        )
        self.editServerPixmapLabel.setFixedSize(QSize(60, 60))

    def changeJavaPath(self):
        editServerVariables.selectedJavaPath = self.editJavaTextEdit.toPlainText()

    def changeMinMem(self):
        editServerVariables.minMem = self.editMinMemLineEdit.text()

    def changeMaxMem(self):
        editServerVariables.maxMem = self.editMaxMemLineEdit.text()

    def changeMemUnit(self):
        editServerVariables.memUnit = self.editMemUnitComboBox.currentText()

    def changeCore(self):
        """手动更换服务器核心"""
        tmpCorePath = str(
            QFileDialog.getOpenFileName(
                self,
                self.tr("选择 *.jar 文件"),
                getcwd(),
                self.tr("Java 可执行文件 (*.jar)"),
            )[0]
        )
        if tmpCorePath != "":
            editServerVariables.corePath = tmpCorePath
            editServerVariables.coreFileName = tmpCorePath.split("/")[-1]
            InfoBar.success(
                title=self.tr("已修改，但未保存"),
                content=self.tr("核心文件名: ") + editServerVariables.coreFileName,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            self.coreLineEdit.setText(editServerVariables.coreFileName)
        else:
            InfoBar.warning(
                title=self.tr("未修改"),
                content=self.tr("你并没有选择服务器核心。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def changeBedrockCore(self):
        """手动更换基岩版服务器核心"""
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            file_filter = self.tr(
                "基岩版服务器 (*.zip *.exe);;压缩包 (*.zip);;可执行文件 (*.exe);;所有文件 (*)"
            )
        else:
            file_filter = self.tr("基岩版服务器 (*.zip *);;压缩包 (*.zip);;所有文件 (*)")
        
        tmpCorePath = str(
            QFileDialog.getOpenFileName(
                self,
                self.tr("选择基岩版服务器文件"),
                getcwd(),
                file_filter,
            )[0]
        )
        
        if tmpCorePath != "":
            editServerVariables.corePath = tmpCorePath
            editServerVariables.coreFileName = tmpCorePath.split("/")[-1]
            InfoBar.success(
                title=self.tr("已修改，但未保存"),
                content=self.tr("核心文件名: ") + editServerVariables.coreFileName,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            self.coreLineEdit.setText(editServerVariables.coreFileName)
        else:
            InfoBar.warning(
                title=self.tr("未修改"),
                content=self.tr("你并没有选择服务器核心。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def changeOutputDeEncoding(self):
        editServerVariables.consoleOutputDeEncoding = editServerVariables.consoleDeEncodingList[
            self.editOutputDeEncodingComboBox.currentIndex()
        ]

    def changeInputDeEncoding(self):
        editServerVariables.consoleInputDeEncoding = editServerVariables.consoleDeEncodingList[
            self.editInputDeEncodingComboBox.currentIndex()
        ]

    def changeServerName(self):
        editServerVariables.serverName = self.editServerNameLineEdit.text()

    def changeJVMArg(self):
        editServerVariables.jvmArg = self.JVMArgPlainTextEdit.toPlainText().split(" ")

    def replaceJavaManually(self):
        """手动导入Java"""
        tmpJavaPath = str(
            QFileDialog.getOpenFileName(
                self,
                self.tr("选择 java.exe 程序"),
                getcwd(),
                self.tr("Java 主程序 (java.exe)"),
            )[0]
        )
        if tmpJavaPath != "":
            if v := javaDetector.getJavaVersion(tmpJavaPath):
                tmpNewJavaPath = editServerVariables.javaPath.copy()
                if javaDetector.Java(tmpJavaPath, v) not in tmpNewJavaPath:
                    tmpNewJavaPath.append(javaDetector.Java(tmpJavaPath, v))
                    InfoBar.success(
                        title=self.tr("已添加"),
                        content=self.tr(
                            "Java路径: "
                            + tmpJavaPath
                            + "\n版本: "
                            + v
                            + "\n但你还需要继续到 Java 列表中选取。"
                        ),
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self,
                    )
                else:
                    InfoBar.warning(
                        title=self.tr("未添加"),
                        content=self.tr(
                            "此 Java 已被添加过，也有可能是自动查找 Java 时已经搜索到了。请检查 Java 列表。"  # noqa: E501
                        ),
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=4848,
                        parent=self,
                    )
                editServerVariables.javaPath.clear()
                editServerVariables.javaPath = tmpNewJavaPath
            else:
                InfoBar.error(
                    title=self.tr("添加失败"),
                    content=self.tr("此 Java 无效！"),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
        else:
            InfoBar.warning(
                title=self.tr("未添加"),
                content=self.tr("你并没有选择 Java。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def autoDetectJava(self):
        """自动查找Java"""
        # 防止同时多次运行worker线程
        self.editAutoDetectJavaPrimaryPushBtn.setEnabled(False)
        self.javaFindWorkThreadFactory.create().start()

    @pyqtSlot(list)
    def autoDetectJavaFinished(self, _JavaPaths: list):
        """自动查找Java结果处理"""
        if osp.exists("MCSL2/AutoDetectJavaHistory.txt"):
            remove("MCSL2/AutoDetectJavaHistory.txt")
        if osp.exists("MCSL2/AutoDetectJavaHistory.json"):
            remove("MCSL2/AutoDetectJavaHistory.json")

        with open("MCSL2/MCSL2_DetectedJava.json", "w+", encoding="utf-8") as SaveFoundedJava:
            tmpNewJavaPath = editServerVariables.javaPath
            editServerVariables.javaPath = list(
                {p[:-1] for p in SaveFoundedJava.readlines()}.union(
                    set(editServerVariables.javaPath)
                ).union(set(_JavaPaths))
            )
            editServerVariables.javaPath.sort(key=lambda x: x.version, reverse=False)
            for d in editServerVariables.javaPath:
                if d not in tmpNewJavaPath:
                    tmpNewJavaPath.append(d)
                else:
                    pass
            editServerVariables.javaPath.clear()
            editServerVariables.javaPath = tmpNewJavaPath

            JavaPathList = [
                {"Path": e.path, "Version": e.version} for e in editServerVariables.javaPath
            ]
            dump(
                {"java": JavaPathList},
                SaveFoundedJava,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    @pyqtSlot(int)
    def onJavaFindWorkThreadFinished(self, sequenceNumber):
        """自动查找Java结束后的处理"""
        if sequenceNumber > 1:
            InfoBar.success(
                title=self.tr("查找完毕"),
                content=self.tr("一共搜索到了")
                + str(len(editServerVariables.javaPath))
                + self.tr("个 Java。\n请单击「Java列表」按钮查看、选择。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

        self.editAutoDetectJavaPrimaryPushBtn.setEnabled(True)

    def setJavaPath(self, selectedJavaPath):
        """选择Java后处理Java路径"""
        editServerVariables.selectedJavaPath = selectedJavaPath
        self.editJavaTextEdit.setText(selectedJavaPath)

    def finishEditServer(self):
        """完成修改服务器的检查触发器"""
        dupCode = self.checkDuplicateConfig()
        # 重复不保存
        if dupCode:
            w = MessageBox(
                title=self.tr("失败"),
                content=self.tr("都没改就不需要保存了，退出即可"),
                parent=self,
            )
            w.yesButton.setText(self.tr("好"))
            w.cancelButton.setParent(None)
            w.cancelButton.deleteLater()
            del w.cancelButton
            w.exec()
        else:
            editServerVariables.memUnit = editServerVariables.memUnitList[
                self.editMemUnitComboBox.currentIndex()
            ]
            # 检查
            check = ServerValidator().check(
                v=editServerVariables,
                minMem=self.editMinMemLineEdit.text(),
                maxMem=self.editMaxMemLineEdit.text(),
                name=self.editServerNameLineEdit.text(),
                jvmArg=self.JVMArgPlainTextEdit.toPlainText(),
            )
            # 如果出错
            if check[1] != 0:
                title = self.tr("编辑服务器失败！存在") + str(check[1]) + self.tr("个问题。")
                detail_text = (
                    check[0]
                    + "\n----------------------------\n"
                    + self.tr(
                        "请根据上方提示，修改后再尝试保存。\n如果确认自己填写的没有问题，请联系开发者。"
                    )
                )
                w = MessageBox(title, "", self)
                w.yesButton.setText(self.tr("好的"))
                w.yesSignal.connect(w.deleteLater)
                detail_widget = ExceptionWidget(detail_text)
                w.textLayout.addWidget(detail_widget.exceptionScrollArea)
                w.contentLabel.setParent(None)
                w.contentLabel.deleteLater()
                w.cancelButton.setParent(None)
                w.cancelButton.deleteLater()
                del w.cancelButton
                w.exec()
            else:
                totalJVMArg: str = "\n".join(editServerVariables.jvmArg)
                title = self.tr("请再次检查你设置的参数是否有误：")
                content = (
                    self.tr("Java: ")
                    + editServerVariables.selectedJavaPath
                    + "\n"
                    + self.tr("Java版本: ")
                    + editServerVariables.selectedJavaVersion
                    + "\n"
                    + self.tr("内存: ")
                    + str(editServerVariables.minMem)
                    + editServerVariables.memUnit
                    + "~"
                    + str(editServerVariables.maxMem)
                    + editServerVariables.memUnit
                    + "\n"
                    + self.tr("服务器核心: ")
                    + editServerVariables.corePath
                    + "\n"
                    + self.tr("服务器核心文件名: ")
                    + editServerVariables.coreFileName
                    + "\n"
                    + self.tr("输出编码设置: ")
                    + self.editOutputDeEncodingComboBox.itemText(
                        editServerVariables.consoleDeEncodingList.index(
                            editServerVariables.consoleOutputDeEncoding
                        )
                    )
                    + "\n"
                    + self.tr("输入编码设置: ")
                    + self.editInputDeEncodingComboBox.itemText(
                        editServerVariables.consoleDeEncodingList.index(
                            editServerVariables.consoleInputDeEncoding
                        )
                    )
                    + "\n"
                    + self.tr("JVM参数: \n")
                    + "    "
                    + totalJVMArg
                    + "\n"
                    + self.tr("服务器名称: ")
                    + editServerVariables.serverName
                )
            w = MessageBox(title, "", self)
            w.yesButton.setText(self.tr("无误，覆盖"))
            w.yesSignal.connect(self.confirmForgeServer)
            w.cancelButton.setText(self.tr("我再看看"))
            detail_widget = ExceptionWidget(content)
            w.textLayout.addWidget(detail_widget.exceptionScrollArea)
            w.contentLabel.setParent(None)
            w.contentLabel.deleteLater()
            w.exec()

    def confirmForgeServer(self):
        if editServerVariables.coreFileName != editServerVariables.oldCoreFileName:
            w = MessageBox(
                self.tr("这是不是一个 Forge 服务器？"),
                self.tr(
                    "由于 Forge 的安装比较离谱，所以我们需要询问您以对此类服务器进行特殊优化。"
                ),
                self,
            )
            w.yesButton.setText(self.tr("是"))
            w.cancelButton.setText(self.tr("不是"))
            # 如果选yes
            if w.exec() == 1:
                editServerVariables.serverType = "forge"
                self.saveEditedServer()
        else:
            self.saveEditedServer()

    def saveEditedServer(self):
        """真正的保存服务器函数"""
        exit0Msg = self.tr("修改服务器「") + editServerVariables.serverName + self.tr("」成功！")
        exit1Msg = self.tr("修改服务器「") + editServerVariables.serverName + self.tr("」失败！")
        exitCode = 0

        # 检查JVM参数防止意外无法启动服务器
        for arg in editServerVariables.jvmArg:
            if arg == "" or arg == " ":
                editServerVariables.jvmArg.pop(editServerVariables.jvmArg.index(arg))

        serverConfig = {
            "name": editServerVariables.serverName,
            "core_file_name": editServerVariables.coreFileName,
            "java_path": editServerVariables.selectedJavaPath,
            "min_memory": editServerVariables.minMem,
            "max_memory": editServerVariables.maxMem,
            "memory_unit": editServerVariables.memUnit,
            "jvm_arg": editServerVariables.jvmArg,
            "output_decoding": editServerVariables.consoleOutputDeEncoding,
            "input_encoding": editServerVariables.consoleInputDeEncoding,
            "icon": editServerVariables.icon,
            "server_type": editServerVariables.serverType,
            "extra_data": editServerVariables.extraData,
        }
        # 复制核心
        try:
            if editServerVariables.coreFileName != editServerVariables.oldCoreFileName:
                copy(
                    editServerVariables.corePath,
                    f"Servers//{editServerVariables.serverName}//{editServerVariables.coreFileName}",
                )
                w2 = MessageBox(
                    title=self.tr("提示"),
                    content=self.tr("是否需要删除旧的服务器核心？"),
                    parent=self,
                )
                w2.yesButton.setText(self.tr("需要"))
                w2.cancelButton.setText(self.tr("不需要"))
                w2.yesSignal.connect(
                    remove(
                        f"Servers//{editServerVariables.oldServerName}//{editServerVariables.oldCoreFileName}"
                    )
                )
                w2.exec()
            elif (
                osp.getsize(
                    f"Servers//{editServerVariables.serverName}//{editServerVariables.oldCoreFileName}"
                )
                != osp.getsize(
                    f"Servers//{editServerVariables.serverName}//{editServerVariables.coreFileName}"
                )
                and editServerVariables.coreFileName == editServerVariables.oldCoreFileName
            ):
                remove(
                    f"Servers//{editServerVariables.oldServerName}//{editServerVariables.oldCoreFileName}"
                )
                copy(
                    editServerVariables.corePath,
                    f"Servers//{editServerVariables.serverName}//{editServerVariables.coreFileName}",
                )
        except Exception as e:
            exitCode = 1
            exit1Msg += f"\n{e}"

        # 改名
        try:
            if editServerVariables.serverName != editServerVariables.oldServerName:
                rename(
                    f"Servers//{editServerVariables.oldServerName}//",
                    f"Servers//{editServerVariables.serverName}//",
                )
        except Exception as e:
            exitCode = 1
            exit1Msg += f"\n{e}"

        # 写入全局配置
        try:
            globalServerList = loads(readFile(r"MCSL2/MCSL2_ServerList.json"))
            globalServerList["MCSLServerList"].pop(self.serverIndex)
            globalServerList["MCSLServerList"].insert(0, serverConfig)
            writeFile(r"MCSL2/MCSL2_ServerList.json", dumps(globalServerList, indent=4))
            exitCode = 0
        except Exception as e:
            exitCode = 1
            exit1Msg += f"\n{e}"

        # 写入单独配置
        try:
            if not cfg.get(cfg.onlySaveGlobalServerConfig):
                writeFile(
                    f"Servers//{editServerVariables.serverName}//MCSL2ServerConfig.json",
                    dumps(serverConfig, indent=4),
                )
            else:
                InfoBar.info(
                    title=self.tr("功能提醒"),
                    content=self.tr(
                        "您在设置中开启了「只保存全局服务器设置」。\n将不会保存单独服务器设置。\n这有可能导致服务器迁移较为繁琐。"
                    ),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
            exitCode = 0
        except Exception as e:
            exitCode = 1
            exit1Msg += f"\n{e}"

        self.syncVariables()

        if exitCode == 0:
            if (
                editServerVariables.serverType == "forge"
                and editServerVariables.serverName != editServerVariables.oldServerName
            ):
                self.installingForgeStateToolTip = StateToolTip(
                    self.tr("安装 Forge"), self.tr("请稍后，正在安装..."), self
                )
                self.installingForgeStateToolTip.move(
                    self.installingForgeStateToolTip.getSuitablePos()
                )
                self.installingForgeStateToolTip.show()

                try:
                    self.forgeInstaller = ForgeInstaller(
                        serverPath=f"Servers//{editServerVariables.serverName}",
                        file=editServerVariables.coreFileName,
                        java=editServerVariables.selectedJavaPath,
                        logDecode=cfg.get(cfg.outputDeEncoding),
                        isEditing=self.serverIndex,
                    )
                    editServerVariables.extraData["forge_version"] = (
                        self.forgeInstaller.forgeVersion
                    )
                    self.forgeInstaller.installFinished.connect(self.afterInstallingForge)
                    self.forgeInstaller.asyncInstall()
                except Exception as e:
                    self.afterInstallingForge(False, e.args)
            else:
                InfoBar.success(
                    title=self.tr("成功"),
                    content=exit0Msg,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
            self.editServerBackPushBtn.click()
        else:
            InfoBar.error(
                title=self.tr("失败"),
                content=exit1Msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        self.refreshServers()

    @pyqtSlot(bool, str)
    def afterInstallingForge(self, installFinished, message):
        if installFinished:
            self.installingForgeStateToolTip.setContent(self.tr("安装成功！"))
            self.installingForgeStateToolTip.setState(True)
            self.installingForgeStateToolTip = None
        else:
            self.installingForgeStateToolTip.setContent(self.tr("安装失败！") + message)
            self.installingForgeStateToolTip.setState(True)
            self.installingForgeStateToolTip = None
            MCSL2Logger.warning(f"{self.__class__.__name__} 回滚")
        if hasattr(
            self, "forgeInstaller"
        ):  # 有可能创建forgeInstaller就抛出了异常(如invalid forge installer等),故需要判断是否初始化
            del self.forgeInstaller
        editServerVariables.resetToDefault()  # 重置

    def checkDuplicateConfig(self):
        """
        检查更改前后是否有配置变化\n
        """
        return (
            editServerVariables.oldMinMem == editServerVariables.minMem
            and editServerVariables.oldMaxMem == editServerVariables.maxMem
            and editServerVariables.oldCoreFileName == editServerVariables.coreFileName
            and editServerVariables.oldSelectedJavaPath == editServerVariables.selectedJavaPath
            and editServerVariables.oldMemUnit == editServerVariables.memUnit
            and editServerVariables.oldJVMArg == editServerVariables.jvmArg
            and editServerVariables.oldServerName == editServerVariables.serverName
            and editServerVariables.oldConsoleOutputDeEncoding
            == editServerVariables.consoleOutputDeEncoding
            and editServerVariables.oldConsoleInputDeEncoding
            == editServerVariables.consoleInputDeEncoding
            and editServerVariables.oldIcon == editServerVariables.icon
        )

    def startServer(self, index, isEditingConfig=False):
        v = ServerConfigConstructor.loadServerConfig(index=index)
        if not isEditingConfig:
            (
                w := ServerWindow(
                    v,
                    ServerLauncher(v),
                    manageBtn=self.sender(),
                    manageBackupBtnList=self.sender()
                    .parent()
                    .parent()
                    .actionsCommandBar.backupActionsList,
                    isEditingConfig=isEditingConfig,
                )
            ).show()
        else:
            (
                w := ServerWindow(
                    v,
                    ServerLauncher(v),
                    manageBtn=self.sender().parent().parent().parent().runBtn,
                    manageBackupBtnList=self.sender().parent().backupActionsList,
                    isEditingConfig=isEditingConfig,
                )
            ).show()
        w.monitorWidget = RunningServerHeaderCardWidget(
            serverName=v.serverName, serverConsole=w
        ).itSelf
        self.runningServerCardGenerated.emit(w.monitorWidget)

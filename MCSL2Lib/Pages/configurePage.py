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
Configure new server page.
"""
from json import loads, dumps
from os import getcwd, mkdir, remove, path as osp
from shutil import copy, rmtree

from PyQt5.QtCore import Qt, QSize, QRect, pyqtSlot
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QHBoxLayout,
    QFrame,
    QFileDialog,
    QStackedWidget,
)
from qfluentwidgets import (
    ComboBox,
    LineEdit,
    PlainTextEdit,
    PrimaryPushButton,
    PushButton,
    SmoothScrollArea,
    StrongBodyLabel,
    SubtitleLabel,
    TitleLabel,
    TransparentToolButton,
    FluentIcon as FIF,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    HyperlinkButton,
    StateToolTip,
)

from MCSL2Lib.Controllers import javaDetector
# from MCSL2Lib.Controllers.interfaceController import ChildStackedWidget
from MCSL2Lib.Controllers.serverController import MojangEula
from MCSL2Lib.Controllers.serverInstaller import ForgeInstaller
from MCSL2Lib.Controllers.settingsController import SettingsController
from MCSL2Lib.ImportServerTypes.importMCSLv1 import MCSLv1
from MCSL2Lib.ImportServerTypes.importMCSLv2 import MCSLv2
from MCSL2Lib.ImportServerTypes.importMCSM8 import MCSM8
from MCSL2Lib.ImportServerTypes.importMCSM9 import MCSM9
from MCSL2Lib.ImportServerTypes.importMSL3 import MSL3
from MCSL2Lib.ImportServerTypes.importNoShellArchives import NoShellArchives
from MCSL2Lib.ImportServerTypes.importNullCraft import NullCraft
from MCSL2Lib.ImportServerTypes.importServerArchiveSite import ServerArchiveSite
from MCSL2Lib.ImportServerTypes.importShellArchives import ShellArchives
from MCSL2Lib.Widgets.DownloadEntryViewerWidget import DownloadEntryBox
from MCSL2Lib.Widgets.ForgeInstallProgressWidget import ForgeInstallerProgressBox
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import (
    GlobalMCSL2Variables,
    ConfigureServerVariables,
    ServerVariables,
    SettingsVariables,
)
from MCSL2Lib.Controllers.logController import MCSL2Logger

MCSLLogger = MCSL2Logger()
settingsController = SettingsController()
configureServerVariables = ConfigureServerVariables()
settingsVariables = SettingsVariables()
serverVariables = ServerVariables()


@Singleton
class ConfigurePage(QWidget):
    """新建服务器页"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.javaFindWorkThreadFactory = javaDetector.JavaFindWorkThreadFactory()
        self.javaFindWorkThreadFactory.fuzzySearch = True
        self.javaFindWorkThreadFactory.signalConnect = self.autoDetectJavaFinished
        self.javaFindWorkThreadFactory.finishSignalConnect = (
            self.onJavaFindWorkThreadFinished
        )
        self.javaFindWorkThreadFactory.create().start()

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.verticalLayout = QVBoxLayout(self.titleLimitWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.subTitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.verticalLayout.addWidget(self.subTitleLabel)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 1, 1)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.newServerStackedWidget = QStackedWidget(self)
        self.newServerStackedWidget.setObjectName("newServerStackedWidget")

        self.guideNewServerPage = QWidget()
        self.guideNewServerPage.setObjectName("guideNewServerPage")

        self.guideNewServerVerticalLayout = QVBoxLayout(self.guideNewServerPage)
        self.guideNewServerVerticalLayout.setObjectName("guideNewServerVerticalLayout")

        self.noobNewServerWidget = QWidget(self.guideNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobNewServerWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobNewServerWidget.setSizePolicy(sizePolicy)
        self.noobNewServerWidget.setMinimumSize(QSize(0, 132))
        self.noobNewServerWidget.setObjectName("noobNewServerWidget")

        self.guideNoobHorizontalLayout = QHBoxLayout(self.noobNewServerWidget)
        self.guideNoobHorizontalLayout.setObjectName("guideNoobHorizontalLayout")

        self.noobNewServerBtn = PrimaryPushButton(self.noobNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobNewServerBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobNewServerBtn.setSizePolicy(sizePolicy)
        self.noobNewServerBtn.setMinimumSize(QSize(215, 33))
        self.noobNewServerBtn.setMaximumSize(QSize(215, 33))
        self.noobNewServerBtn.setObjectName("noobNewServerBtn")

        self.guideNoobHorizontalLayout.addWidget(self.noobNewServerBtn)
        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.guideNoobHorizontalLayout.addItem(spacerItem1)
        self.noobNewServerIntro = StrongBodyLabel(self.noobNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobNewServerIntro.sizePolicy().hasHeightForWidth()
        )
        self.noobNewServerIntro.setSizePolicy(sizePolicy)
        self.noobNewServerIntro.setTextFormat(Qt.MarkdownText)
        self.noobNewServerIntro.setObjectName("noobNewServerIntro")

        self.guideNoobHorizontalLayout.addWidget(self.noobNewServerIntro)
        self.guideNewServerVerticalLayout.addWidget(self.noobNewServerWidget)
        self.extendedNewServerWidget = QWidget(self.guideNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedNewServerWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedNewServerWidget.setSizePolicy(sizePolicy)
        self.extendedNewServerWidget.setMinimumSize(QSize(0, 132))
        self.extendedNewServerWidget.setObjectName("extendedNewServerWidget")

        self.guideExtendedHorizontalLayout = QHBoxLayout(self.extendedNewServerWidget)
        self.guideExtendedHorizontalLayout.setObjectName(
            "guideExtendedHorizontalLayout"
        )

        self.extendedNewServerBtn = PrimaryPushButton(self.extendedNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedNewServerBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedNewServerBtn.setSizePolicy(sizePolicy)
        self.extendedNewServerBtn.setMinimumSize(QSize(215, 33))
        self.extendedNewServerBtn.setMaximumSize(QSize(215, 33))
        self.extendedNewServerBtn.setObjectName("extendedNewServerBtn")

        self.guideExtendedHorizontalLayout.addWidget(self.extendedNewServerBtn)
        spacerItem2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.guideExtendedHorizontalLayout.addItem(spacerItem2)
        self.extendedNewServerIntro = StrongBodyLabel(self.extendedNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedNewServerIntro.sizePolicy().hasHeightForWidth()
        )
        self.extendedNewServerIntro.setSizePolicy(sizePolicy)
        self.extendedNewServerIntro.setTextFormat(Qt.MarkdownText)
        self.extendedNewServerIntro.setObjectName("extendedNewServerIntro")

        self.guideExtendedHorizontalLayout.addWidget(self.extendedNewServerIntro)
        self.guideNewServerVerticalLayout.addWidget(self.extendedNewServerWidget)
        self.importNewServerWidget = QWidget(self.guideNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerWidget.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerWidget.setSizePolicy(sizePolicy)
        self.importNewServerWidget.setMinimumSize(QSize(0, 132))
        self.importNewServerWidget.setObjectName("importNewServerWidget")

        self.guideImportHorizontalLayout = QHBoxLayout(self.importNewServerWidget)
        self.guideImportHorizontalLayout.setObjectName("guideImportHorizontalLayout")

        self.importNewServerBtn = PrimaryPushButton(self.importNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerBtn.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerBtn.setSizePolicy(sizePolicy)
        self.importNewServerBtn.setMinimumSize(QSize(215, 33))
        self.importNewServerBtn.setMaximumSize(QSize(215, 33))
        self.importNewServerBtn.setObjectName("importNewServerBtn")

        self.guideImportHorizontalLayout.addWidget(self.importNewServerBtn)
        spacerItem3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.guideImportHorizontalLayout.addItem(spacerItem3)
        self.importNewServerIntro = StrongBodyLabel(self.importNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerIntro.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerIntro.setSizePolicy(sizePolicy)
        self.importNewServerIntro.setTextFormat(Qt.MarkdownText)
        self.importNewServerIntro.setObjectName("importNewServerIntro")

        self.guideImportHorizontalLayout.addWidget(self.importNewServerIntro)
        self.guideNewServerVerticalLayout.addWidget(self.importNewServerWidget)
        self.newServerStackedWidget.addWidget(self.guideNewServerPage)
        self.noobNewServerPage = QWidget()
        self.noobNewServerPage.setObjectName("noobNewServerPage")

        self.noobNewServerGridLayout = QGridLayout(self.noobNewServerPage)
        self.noobNewServerGridLayout.setObjectName("noobNewServerGridLayout")

        self.noobNewServerScrollArea = SmoothScrollArea(self.noobNewServerPage)
        self.noobNewServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.noobNewServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.noobNewServerScrollArea.setWidgetResizable(True)
        self.noobNewServerScrollArea.setObjectName("noobNewServerScrollArea")
        self.noobNewServerScrollArea.setFrameShape(QFrame.NoFrame)

        self.noobNewServerScrollAreaContents = QWidget()
        self.noobNewServerScrollAreaContents.setGeometry(QRect(0, -100, 586, 453))
        self.noobNewServerScrollAreaContents.setObjectName(
            "noobNewServerScrollAreaContents"
        )

        self.noobNewServerScrollAreaVerticalLayout = QVBoxLayout(
            self.noobNewServerScrollAreaContents
        )
        self.noobNewServerScrollAreaVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.noobNewServerScrollAreaVerticalLayout.setObjectName(
            "noobNewServerScrollAreaVerticalLayout"
        )

        self.noobSetJavaWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSetJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobSetJavaWidget.setSizePolicy(sizePolicy)
        self.noobSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.noobSetJavaWidget.setObjectName("noobSetJavaWidget")

        self.gridLayout_3 = QGridLayout(self.noobSetJavaWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.noobJavaSubtitleLabel = SubtitleLabel(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobJavaSubtitleLabel.setObjectName("noobJavaSubtitleLabel")

        self.gridLayout_3.addWidget(self.noobJavaSubtitleLabel, 0, 0, 1, 1)
        self.noobJavaInfoLabel = SubtitleLabel(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobJavaInfoLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobJavaInfoLabel.setSizePolicy(sizePolicy)
        self.noobJavaInfoLabel.setObjectName("noobJavaInfoLabel")

        self.gridLayout_3.addWidget(self.noobJavaInfoLabel, 0, 1, 1, 1)
        self.noobSetJavaBtnWidget = QWidget(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSetJavaBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobSetJavaBtnWidget.setSizePolicy(sizePolicy)
        self.noobSetJavaBtnWidget.setObjectName("noobSetJavaBtnWidget")

        self.horizontalLayout_6 = QHBoxLayout(self.noobSetJavaBtnWidget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.noobDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.noobSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobDownloadJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobDownloadJavaPrimaryPushBtn.setObjectName(
            "noobDownloadJavaPrimaryPushBtn"
        )

        self.horizontalLayout_6.addWidget(self.noobDownloadJavaPrimaryPushBtn)
        self.noobManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.noobSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobManuallyAddJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobManuallyAddJavaPrimaryPushBtn.setObjectName(
            "noobManuallyAddJavaPrimaryPushBtn"
        )

        self.horizontalLayout_6.addWidget(self.noobManuallyAddJavaPrimaryPushBtn)
        self.noobAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.noobSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobAutoDetectJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobAutoDetectJavaPrimaryPushBtn.setObjectName(
            "noobAutoDetectJavaPrimaryPushBtn"
        )

        self.horizontalLayout_6.addWidget(self.noobAutoDetectJavaPrimaryPushBtn)
        self.noobJavaListPushBtn = PushButton(self.noobSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobJavaListPushBtn.setSizePolicy(sizePolicy)
        self.noobJavaListPushBtn.setMinimumSize(QSize(90, 0))
        self.noobJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobJavaListPushBtn.setObjectName("noobJavaListPushBtn")

        self.horizontalLayout_6.addWidget(self.noobJavaListPushBtn)
        spacerItem4 = QSpacerItem(127, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.gridLayout_3.addWidget(self.noobSetJavaBtnWidget, 1, 0, 1, 2)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetJavaWidget)
        self.noobSetMemWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSetMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobSetMemWidget.setSizePolicy(sizePolicy)
        self.noobSetMemWidget.setObjectName("noobSetMemWidget")

        self.gridLayout_4 = QGridLayout(self.noobSetMemWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")

        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem5, 1, 5, 1, 1)
        self.noobMinMemLineEdit = LineEdit(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noobMinMemLineEdit.setSizePolicy(sizePolicy)
        self.noobMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noobMinMemLineEdit.setObjectName("noobMinMemLineEdit")

        self.gridLayout_4.addWidget(self.noobMinMemLineEdit, 1, 1, 1, 1)
        self.noobMemUnitLabel = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobMemUnitLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobMemUnitLabel.setSizePolicy(sizePolicy)
        self.noobMemUnitLabel.setObjectName("noobMemUnitLabel")

        self.gridLayout_4.addWidget(self.noobMemUnitLabel, 1, 4, 1, 1)
        self.noobMaxMemLineEdit = LineEdit(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noobMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.noobMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noobMaxMemLineEdit.setObjectName("noobMaxMemLineEdit")

        self.gridLayout_4.addWidget(self.noobMaxMemLineEdit, 1, 3, 1, 1)
        self.noobToSymbol = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobToSymbol.sizePolicy().hasHeightForWidth())
        self.noobToSymbol.setSizePolicy(sizePolicy)
        self.noobToSymbol.setObjectName("noobToSymbol")

        self.gridLayout_4.addWidget(self.noobToSymbol, 1, 2, 1, 1)
        self.noobMemSubtitleLabel = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobMemSubtitleLabel.setObjectName("noobMemSubtitleLabel")

        self.gridLayout_4.addWidget(self.noobMemSubtitleLabel, 0, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetMemWidget)
        self.noobSetCoreWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSetCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobSetCoreWidget.setSizePolicy(sizePolicy)
        self.noobSetCoreWidget.setObjectName("noobSetCoreWidget")

        self.gridLayout_5 = QGridLayout(self.noobSetCoreWidget)
        self.gridLayout_5.setObjectName("gridLayout_5")

        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem6, 1, 3, 1, 1)
        self.noobDownloadCorePrimaryPushBtn = PrimaryPushButton(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobDownloadCorePrimaryPushBtn.setObjectName(
            "noobDownloadCorePrimaryPushBtn"
        )

        self.gridLayout_5.addWidget(self.noobDownloadCorePrimaryPushBtn, 1, 2, 1, 1)
        self.noobManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.noobSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobManuallyAddCorePrimaryPushBtn.setObjectName(
            "noobManuallyAddCorePrimaryPushBtn"
        )

        self.gridLayout_5.addWidget(self.noobManuallyAddCorePrimaryPushBtn, 1, 1, 1, 1)

        self.noobAddCoreFromDownloadedPrimaryPushBtn = PrimaryPushButton(
            self.noobSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobAddCoreFromDownloadedPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobAddCoreFromDownloadedPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobAddCoreFromDownloadedPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobAddCoreFromDownloadedPrimaryPushBtn.setObjectName(
            "noobAddCoreFromDownloadedPrimaryPushBtn"
        )

        self.gridLayout_5.addWidget(self.noobAddCoreFromDownloadedPrimaryPushBtn, 1, 3, 1, 1)

        self.noobCoreSubtitleLabel = SubtitleLabel(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobCoreSubtitleLabel.setObjectName("noobCoreSubtitleLabel")

        self.gridLayout_5.addWidget(self.noobCoreSubtitleLabel, 0, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetCoreWidget)
        self.noobSetServerNameWidget = QWidget(self.noobNewServerScrollAreaContents)
        self.noobSetServerNameWidget.setObjectName("noobSetServerNameWidget")

        self.verticalLayout_4 = QVBoxLayout(self.noobSetServerNameWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.noobServerNameSubtitleLabel = SubtitleLabel(self.noobSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobServerNameSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobServerNameSubtitleLabel.setObjectName("noobServerNameSubtitleLabel")

        self.verticalLayout_4.addWidget(self.noobServerNameSubtitleLabel)
        self.noobServerNameLineEdit = LineEdit(self.noobSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noobServerNameLineEdit.setSizePolicy(sizePolicy)
        self.noobServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.noobServerNameLineEdit.setObjectName("noobServerNameLineEdit")

        self.verticalLayout_4.addWidget(self.noobServerNameLineEdit)
        self.noobSaveServerPrimaryPushBtn = PrimaryPushButton(
            self.noobSetServerNameWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.noobSaveServerPrimaryPushBtn.setObjectName("noobSaveServerPrimaryPushBtn")

        self.verticalLayout_4.addWidget(self.noobSaveServerPrimaryPushBtn)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(
            self.noobSetServerNameWidget
        )
        spacerItem7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.noobNewServerScrollAreaVerticalLayout.addItem(spacerItem7)
        self.noobNewServerScrollArea.setWidget(self.noobNewServerScrollAreaContents)
        self.noobNewServerGridLayout.addWidget(self.noobNewServerScrollArea, 2, 2, 1, 1)
        self.noobTitleWidget = QWidget(self.noobNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobTitleWidget.sizePolicy().hasHeightForWidth()
        )
        self.noobTitleWidget.setSizePolicy(sizePolicy)
        self.noobTitleWidget.setObjectName("noobTitleWidget")

        self.horizontalLayout_4 = QHBoxLayout(self.noobTitleWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.noobBackToGuidePushButton = TransparentToolButton(
            FIF.PAGE_LEFT, self.noobTitleWidget
        )
        self.noobBackToGuidePushButton.setObjectName("noobBackToGuidePushButton")

        self.horizontalLayout_4.addWidget(self.noobBackToGuidePushButton)
        self.noobSubtitleLabel = SubtitleLabel(self.noobTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobSubtitleLabel.setObjectName("noobSubtitleLabel")

        self.horizontalLayout_4.addWidget(self.noobSubtitleLabel)
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.noobNewServerGridLayout.addWidget(self.noobTitleWidget, 0, 1, 2, 2)
        spacerItem9 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.noobNewServerGridLayout.addItem(spacerItem9, 0, 0, 3, 1)
        self.newServerStackedWidget.addWidget(self.noobNewServerPage)

        self.extendedNewServerPage = QWidget()
        self.extendedNewServerPage.setObjectName("extendedNewServerPage")

        self.gridLayout_2 = QGridLayout(self.extendedNewServerPage)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.extendedTitleWidget = QWidget(self.extendedNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedTitleWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedTitleWidget.setSizePolicy(sizePolicy)
        self.extendedTitleWidget.setObjectName("extendedTitleWidget")

        self.horizontalLayout_5 = QHBoxLayout(self.extendedTitleWidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.extendedBackToGuidePushButton = TransparentToolButton(
            FIF.PAGE_LEFT, self.extendedTitleWidget
        )
        self.extendedBackToGuidePushButton.setObjectName(
            "extendedBackToGuidePushButton"
        )

        self.horizontalLayout_5.addWidget(self.extendedBackToGuidePushButton)
        self.extendedSubtitleLabel = SubtitleLabel(self.extendedTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedSubtitleLabel.setObjectName("extendedSubtitleLabel")

        self.horizontalLayout_5.addWidget(self.extendedSubtitleLabel)
        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem10)
        self.gridLayout_2.addWidget(self.extendedTitleWidget, 0, 1, 1, 1)
        self.extendedNewServerScrollArea = SmoothScrollArea(self.extendedNewServerPage)
        self.extendedNewServerScrollArea.setFrameShape(QFrame.NoFrame)
        self.extendedNewServerScrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.extendedNewServerScrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.extendedNewServerScrollArea.setWidgetResizable(True)
        self.extendedNewServerScrollArea.setObjectName("extendedNewServerScrollArea")

        self.extendedNewServerScrollAreaContents = QWidget()
        self.extendedNewServerScrollAreaContents.setGeometry(QRect(0, 0, 594, 734))
        self.extendedNewServerScrollAreaContents.setObjectName(
            "extendedNewServerScrollAreaContents"
        )

        self.noobNewServerScrollAreaVerticalLayout_2 = QVBoxLayout(
            self.extendedNewServerScrollAreaContents
        )
        self.noobNewServerScrollAreaVerticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.noobNewServerScrollAreaVerticalLayout_2.setObjectName(
            "noobNewServerScrollAreaVerticalLayout_2"
        )

        self.extendedSetJavaWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSetJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedSetJavaWidget.setSizePolicy(sizePolicy)
        self.extendedSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.extendedSetJavaWidget.setObjectName("extendedSetJavaWidget")

        self.gridLayout_6 = QGridLayout(self.extendedSetJavaWidget)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.extendedJavaSubtitleLabel = SubtitleLabel(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedJavaSubtitleLabel.setObjectName("extendedJavaSubtitleLabel")

        self.gridLayout_6.addWidget(self.extendedJavaSubtitleLabel, 0, 0, 1, 1)
        self.extendedJavaInfoLabel = SubtitleLabel(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedJavaInfoLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedJavaInfoLabel.setSizePolicy(sizePolicy)
        self.extendedJavaInfoLabel.setObjectName("extendedJavaInfoLabel")

        self.gridLayout_6.addWidget(self.extendedJavaInfoLabel, 0, 1, 1, 1)
        self.extendedSetJavaBtnWidget = QWidget(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSetJavaBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedSetJavaBtnWidget.setSizePolicy(sizePolicy)
        self.extendedSetJavaBtnWidget.setObjectName("extendedSetJavaBtnWidget")

        self.horizontalLayout_7 = QHBoxLayout(self.extendedSetJavaBtnWidget)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.extendedDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.extendedSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedDownloadJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.extendedDownloadJavaPrimaryPushBtn.setObjectName(
            "extendedDownloadJavaPrimaryPushBtn"
        )

        self.horizontalLayout_7.addWidget(self.extendedDownloadJavaPrimaryPushBtn)
        self.extendedManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.extendedSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedManuallyAddJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.extendedManuallyAddJavaPrimaryPushBtn.setObjectName(
            "extendedManuallyAddJavaPrimaryPushBtn"
        )

        self.horizontalLayout_7.addWidget(self.extendedManuallyAddJavaPrimaryPushBtn)
        self.extendedAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.extendedSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedAutoDetectJavaPrimaryPushBtn.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.extendedAutoDetectJavaPrimaryPushBtn.setObjectName(
            "extendedAutoDetectJavaPrimaryPushBtn"
        )

        self.horizontalLayout_7.addWidget(self.extendedAutoDetectJavaPrimaryPushBtn)
        self.extendedJavaListPushBtn = PushButton(self.extendedSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedJavaListPushBtn.setSizePolicy(sizePolicy)
        self.extendedJavaListPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.extendedJavaListPushBtn.setObjectName("extendedJavaListPushBtn")

        self.horizontalLayout_7.addWidget(self.extendedJavaListPushBtn)
        spacerItem11 = QSpacerItem(127, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem11)
        self.gridLayout_6.addWidget(self.extendedSetJavaBtnWidget, 1, 0, 1, 2)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetJavaWidget
        )
        self.extendedSetMemWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSetMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedSetMemWidget.setSizePolicy(sizePolicy)
        self.extendedSetMemWidget.setObjectName("extendedSetMemWidget")

        self.gridLayout_7 = QGridLayout(self.extendedSetMemWidget)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.extendedMinMemLineEdit = LineEdit(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.extendedMinMemLineEdit.setSizePolicy(sizePolicy)
        self.extendedMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedMinMemLineEdit.setObjectName("extendedMinMemLineEdit")

        self.gridLayout_7.addWidget(self.extendedMinMemLineEdit, 1, 1, 1, 1)
        self.extendedMemSubtitleLabel = SubtitleLabel(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedMemSubtitleLabel.setObjectName("extendedMemSubtitleLabel")

        self.gridLayout_7.addWidget(self.extendedMemSubtitleLabel, 0, 1, 1, 1)
        self.extendedMaxMemLineEdit = LineEdit(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.extendedMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.extendedMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedMaxMemLineEdit.setObjectName("extendedMaxMemLineEdit")

        self.gridLayout_7.addWidget(self.extendedMaxMemLineEdit, 1, 3, 1, 1)
        self.extendedToSymbol = SubtitleLabel(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.extendedToSymbol.setSizePolicy(sizePolicy)
        self.extendedToSymbol.setObjectName("extendedToSymbol")

        self.gridLayout_7.addWidget(self.extendedToSymbol, 1, 2, 1, 1)
        spacerItem12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem12, 1, 5, 1, 1)
        self.extendedMemUnitComboBox = ComboBox(self.extendedSetMemWidget)
        self.extendedMemUnitComboBox.setObjectName("extendedMemUnitComboBox")

        self.gridLayout_7.addWidget(self.extendedMemUnitComboBox, 1, 4, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetMemWidget
        )
        self.extendedSetCoreWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSetCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.extendedSetCoreWidget.setSizePolicy(sizePolicy)
        self.extendedSetCoreWidget.setObjectName("extendedSetCoreWidget")

        self.gridLayout_8 = QGridLayout(self.extendedSetCoreWidget)
        self.gridLayout_8.setObjectName("gridLayout_8")

        spacerItem13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem13, 1, 3, 1, 1)
        self.extendedDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.extendedSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedDownloadCorePrimaryPushBtn.setObjectName(
            "extendedDownloadCorePrimaryPushBtn"
        )

        self.gridLayout_8.addWidget(self.extendedDownloadCorePrimaryPushBtn, 1, 2, 1, 1)
        self.extendedManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.extendedSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedManuallyAddCorePrimaryPushBtn.setObjectName(
            "extendedManuallyAddCorePrimaryPushBtn"
        )

        self.gridLayout_8.addWidget(
            self.extendedManuallyAddCorePrimaryPushBtn, 1, 1, 1, 1
        )
        self.extendedCoreSubtitleLabel = SubtitleLabel(self.extendedSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedCoreSubtitleLabel.setObjectName("extendedCoreSubtitleLabel")

        self.gridLayout_8.addWidget(self.extendedCoreSubtitleLabel, 0, 1, 1, 1)
        self.extendedAddCoreFromDownloadedPrimaryPushBtn = PrimaryPushButton(self.extendedSetCoreWidget)
        self.extendedAddCoreFromDownloadedPrimaryPushBtn.setObjectName("extendedAddCoreFromDownloadedPrimaryPushBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedAddCoreFromDownloadedPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedAddCoreFromDownloadedPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.gridLayout_8.addWidget(self.extendedAddCoreFromDownloadedPrimaryPushBtn, 1, 3, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetCoreWidget
        )
        self.extendedSetDeEncodingWidget = QWidget(
            self.extendedNewServerScrollAreaContents
        )
        self.extendedSetDeEncodingWidget.setObjectName("extendedSetDeEncodingWidget")

        self.gridLayout_9 = QGridLayout(self.extendedSetDeEncodingWidget)
        self.gridLayout_9.setObjectName("gridLayout_9")

        self.extendedOutputDeEncodingComboBox = ComboBox(
            self.extendedSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.extendedOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.extendedOutputDeEncodingComboBox.setObjectName(
            "extendedOutputDeEncodingComboBox"
        )

        self.gridLayout_9.addWidget(self.extendedOutputDeEncodingComboBox, 2, 1, 1, 1)
        self.extendedDeEncodingSubtitleLabel = SubtitleLabel(
            self.extendedSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedDeEncodingSubtitleLabel.setObjectName(
            "extendedDeEncodingSubtitleLabel"
        )

        self.gridLayout_9.addWidget(self.extendedDeEncodingSubtitleLabel, 0, 0, 1, 1)
        self.extendedInputDeEncodingComboBox = ComboBox(
            self.extendedSetDeEncodingWidget
        )
        self.extendedInputDeEncodingComboBox.setText("")
        self.extendedInputDeEncodingComboBox.setObjectName(
            "extendedInputDeEncodingComboBox"
        )

        self.gridLayout_9.addWidget(self.extendedInputDeEncodingComboBox, 3, 1, 1, 1)
        self.extendedOutputDeEncodingLabel = StrongBodyLabel(
            self.extendedSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.extendedOutputDeEncodingLabel.setObjectName(
            "extendedOutputDeEncodingLabel"
        )

        self.gridLayout_9.addWidget(self.extendedOutputDeEncodingLabel, 2, 0, 1, 1)
        self.extendedInputDeEncodingLabel = StrongBodyLabel(
            self.extendedSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.extendedInputDeEncodingLabel.setObjectName("extendedInputDeEncodingLabel")

        self.gridLayout_9.addWidget(self.extendedInputDeEncodingLabel, 3, 0, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetDeEncodingWidget
        )
        self.extendedSetJVMArgWidget = QWidget(self.extendedNewServerScrollAreaContents)
        self.extendedSetJVMArgWidget.setObjectName("extendedSetJVMArgWidget")

        self.gridLayout_10 = QGridLayout(self.extendedSetJVMArgWidget)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.extendedJVMArgSubtitleLabel = SubtitleLabel(self.extendedSetJVMArgWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedJVMArgSubtitleLabel.setObjectName("extendedJVMArgSubtitleLabel")

        self.gridLayout_10.addWidget(self.extendedJVMArgSubtitleLabel, 0, 0, 1, 1)
        self.JVMArgPlainTextEdit = PlainTextEdit(self.extendedSetJVMArgWidget)
        self.JVMArgPlainTextEdit.setObjectName("JVMArgPlainTextEdit")

        self.gridLayout_10.addWidget(self.JVMArgPlainTextEdit, 1, 0, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetJVMArgWidget
        )
        self.extendedSetServerNameWidget = QWidget(
            self.extendedNewServerScrollAreaContents
        )
        self.extendedSetServerNameWidget.setObjectName("extendedSetServerNameWidget")

        self.verticalLayout_5 = QVBoxLayout(self.extendedSetServerNameWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.extendedServerNameSubtitleLabel = SubtitleLabel(
            self.extendedSetServerNameWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedServerNameSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedServerNameSubtitleLabel.setObjectName(
            "extendedServerNameSubtitleLabel"
        )

        self.verticalLayout_5.addWidget(self.extendedServerNameSubtitleLabel)
        self.extendedServerNameLineEdit = LineEdit(self.extendedSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.extendedServerNameLineEdit.setSizePolicy(sizePolicy)
        self.extendedServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedServerNameLineEdit.setObjectName("extendedServerNameLineEdit")

        self.verticalLayout_5.addWidget(self.extendedServerNameLineEdit)
        self.extendedSaveServerPrimaryPushBtn = PrimaryPushButton(
            self.extendedSetServerNameWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.extendedSaveServerPrimaryPushBtn.setObjectName(
            "extendedSaveServerPrimaryPushBtn"
        )

        self.verticalLayout_5.addWidget(self.extendedSaveServerPrimaryPushBtn)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(
            self.extendedSetServerNameWidget
        )
        spacerItem14 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.noobNewServerScrollAreaVerticalLayout_2.addItem(spacerItem14)
        self.extendedNewServerScrollArea.setWidget(
            self.extendedNewServerScrollAreaContents
        )
        self.gridLayout_2.addWidget(self.extendedNewServerScrollArea, 1, 1, 1, 1)
        spacerItem15 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem15, 0, 0, 2, 1)
        self.newServerStackedWidget.addWidget(self.extendedNewServerPage)
        self.importNewServerPage = QWidget()
        self.importNewServerPage.setObjectName("importNewServerPage")

        self.gridLayout_21 = QGridLayout(self.importNewServerPage)
        self.gridLayout_21.setObjectName("gridLayout_21")

        self.importTitleWidget = QWidget(self.importNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importTitleWidget.sizePolicy().hasHeightForWidth()
        )
        self.importTitleWidget.setSizePolicy(sizePolicy)
        self.importTitleWidget.setObjectName("importTitleWidget")

        self.horizontalLayout_10 = QHBoxLayout(self.importTitleWidget)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.importBackToGuidePushButton = TransparentToolButton(
            FIF.PAGE_LEFT, self.importTitleWidget
        )
        self.importBackToGuidePushButton.setObjectName("importBackToGuidePushButton")

        self.horizontalLayout_10.addWidget(self.importBackToGuidePushButton)
        self.importSubtitleLabel = SubtitleLabel(self.importTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.importSubtitleLabel.setSizePolicy(sizePolicy)
        self.importSubtitleLabel.setObjectName("importSubtitleLabel")
        self.horizontalLayout_10.addWidget(self.importSubtitleLabel)

        self.horizontalLayout_10.addWidget(self.importSubtitleLabel)
        spacerItem16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem16)
        self.gridLayout_21.addWidget(self.importTitleWidget, 0, 1, 1, 1)
        spacerItem19 = QSpacerItem(20, 406, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_21.addItem(spacerItem19, 0, 0, 2, 1)
        self.importNewServerStackWidget = QStackedWidget(self.importNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerStackWidget.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerStackWidget.setSizePolicy(sizePolicy)
        self.importNewServerStackWidget.setObjectName("importNewServerStackWidget")
        self.importNewServerFirstGuide = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerFirstGuide.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerFirstGuide.setSizePolicy(sizePolicy)
        self.importNewServerFirstGuide.setObjectName("importNewServerFirstGuide")
        self.gridLayout_11 = QGridLayout(self.importNewServerFirstGuide)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.importNewServerTypeComboBox = ComboBox(self.importNewServerFirstGuide)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerTypeComboBox.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerTypeComboBox.setSizePolicy(sizePolicy)
        self.importNewServerTypeComboBox.setMinimumSize(QSize(240, 35))
        self.importNewServerTypeComboBox.setMaximumSize(QSize(240, 35))
        self.importNewServerTypeComboBox.setObjectName("importNewServerTypeComboBox")
        self.gridLayout_11.addWidget(self.importNewServerTypeComboBox, 3, 3, 1, 1)
        spacerItem20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem20, 3, 0, 4, 1)
        spacerItem21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem21, 3, 5, 4, 1)
        spacerItem22 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem22, 6, 3, 1, 1)
        self.importNewServerFirstGuideTitle = SubtitleLabel(
            self.importNewServerFirstGuide
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerFirstGuideTitle.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerFirstGuideTitle.setSizePolicy(sizePolicy)
        self.importNewServerFirstGuideTitle.setObjectName(
            "importNewServerFirstGuideTitle"
        )
        self.gridLayout_11.addWidget(self.importNewServerFirstGuideTitle, 1, 3, 1, 1)
        self.goBtnWidget = QWidget(self.importNewServerFirstGuide)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.goBtnWidget.sizePolicy().hasHeightForWidth())
        self.goBtnWidget.setSizePolicy(sizePolicy)
        self.goBtnWidget.setObjectName("goBtnWidget")
        self.horizontalLayout = QHBoxLayout(self.goBtnWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.goBtn = TransparentToolButton(FIF.PAGE_RIGHT, self.goBtnWidget)
        self.goBtn.setMinimumSize(QSize(80, 80))
        self.goBtn.setMaximumSize(QSize(80, 80))
        self.goBtn.setIconSize(QSize(80, 80))
        self.goBtn.setObjectName("goBtn")
        self.horizontalLayout.addWidget(self.goBtn)
        self.gridLayout_11.addWidget(self.goBtnWidget, 5, 3, 1, 1)
        spacerItem23 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_11.addItem(spacerItem23, 4, 3, 1, 1)
        spacerItem24 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_11.addItem(spacerItem24, 2, 3, 1, 1)
        spacerItem25 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem25, 0, 0, 1, 6)
        self.importNewServerStackWidget.addWidget(self.importNewServerFirstGuide)

        self.noShellArchives = NoShellArchives()
        self.importNewServerStackWidget.addWidget(self.noShellArchives)

        self.shellArchives = ShellArchives()
        self.importNewServerStackWidget.addWidget(self.shellArchives)

        self.serverArchiveSite = ServerArchiveSite()
        self.importNewServerStackWidget.addWidget(self.serverArchiveSite)

        self.MCSLv1 = MCSLv1()
        self.importNewServerStackWidget.addWidget(self.MCSLv1)

        self.MCSLv2 = MCSLv2()
        self.importNewServerStackWidget.addWidget(self.MCSLv2)

        self.MSL3 = MSL3()
        self.importNewServerStackWidget.addWidget(self.MSL3)

        self.NullCraft = NullCraft()
        self.importNewServerStackWidget.addWidget(self.NullCraft)

        self.MCSM8 = MCSM8()
        self.importNewServerStackWidget.addWidget(self.MCSM8)

        self.MCSM9 = MCSM9()
        self.importNewServerStackWidget.addWidget(self.MCSM9)
        self.gridLayout_21.addWidget(self.importNewServerStackWidget, 1, 1, 1, 1)
        self.newServerStackedWidget.addWidget(self.importNewServerPage)
        self.gridLayout.addWidget(self.newServerStackedWidget, 2, 2, 1, 1)

        self.setObjectName("ConfigureInterface")

        self.importNewServerStackWidget.setCurrentIndex(0)

        self.noobNewServerScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.extendedNewServerScrollArea.setAttribute(Qt.WA_StyledBackground)

        # 引导页
        self.titleLabel.setText("新建服务器")
        self.subTitleLabel.setText("有3种方式供你选择。")
        self.noobNewServerBtn.setText("简易模式")
        self.noobNewServerIntro.setText(
            "保留基础配置。\n" " - Java\n" " - 服务器核心\n" " - 最小最大内存\n" " - 服务器名称"
        )
        self.extendedNewServerBtn.setText("进阶模式")
        self.extendedNewServerIntro.setText(
            "在简易模式基础上\n" "，\n" "还能设置：\n" " - 内存单位\n" " - 控制台流编码\n" " - JVM参数"
        )
        self.importNewServerBtn.setText("导入")
        self.importNewServerIntro.setText("暂未完成。")

        # 简易模式
        self.noobJavaSubtitleLabel.setText("Java:")
        self.noobJavaInfoLabel.setText("[选择的Java的信息]")
        self.noobDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.noobManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.noobAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.noobJavaListPushBtn.setText("Java列表")
        self.noobMemUnitLabel.setText("M")
        self.noobToSymbol.setText("~")
        self.noobMemSubtitleLabel.setText("内存:")
        self.noobDownloadCorePrimaryPushBtn.setText("下载核心")
        self.noobManuallyAddCorePrimaryPushBtn.setText("手动导入")
        self.noobAddCoreFromDownloadedPrimaryPushBtn.setText("从下载的核心中导入")
        self.noobCoreSubtitleLabel.setText("核心：")
        self.noobServerNameSubtitleLabel.setText("服务器名称：")
        self.noobSaveServerPrimaryPushBtn.setText("保存！")
        self.noobSubtitleLabel.setText("简易模式")
        self.noobMinMemLineEdit.setPlaceholderText("整数")
        self.noobMaxMemLineEdit.setPlaceholderText("整数")
        self.noobServerNameLineEdit.setPlaceholderText("不能包含非法字符")

        # 进阶模式
        self.extendedSubtitleLabel.setText("进阶模式")
        self.extendedJavaSubtitleLabel.setText("Java:")
        self.extendedJavaInfoLabel.setText("[选择的Java的信息]")
        self.extendedDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.extendedManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.extendedAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.extendedJavaListPushBtn.setText("Java列表")
        self.extendedMemSubtitleLabel.setText("内存:")
        self.extendedToSymbol.setText("~")
        self.extendedDownloadCorePrimaryPushBtn.setText("下载核心")
        self.extendedManuallyAddCorePrimaryPushBtn.setText("手动导入")
        self.extendedAddCoreFromDownloadedPrimaryPushBtn.setText("从下载的核心中导入")
        self.extendedCoreSubtitleLabel.setText("核心：")
        self.extendedDeEncodingSubtitleLabel.setText("编码设置：")
        self.extendedOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.extendedInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.extendedJVMArgSubtitleLabel.setText("JVM参数：")
        self.JVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.extendedServerNameSubtitleLabel.setText("服务器名称：")
        self.extendedSaveServerPrimaryPushBtn.setText("保存！")
        self.extendedMinMemLineEdit.setPlaceholderText("整数")
        self.extendedMaxMemLineEdit.setPlaceholderText("整数")
        self.extendedServerNameLineEdit.setPlaceholderText("不能包含非法字符")
        self.extendedOutputDeEncodingComboBox.addItems(
            ["跟随全局", "UTF-8", "GB18030", "ANSI(推荐)"]
        )
        self.extendedOutputDeEncodingComboBox.setCurrentIndex(0)
        self.extendedInputDeEncodingComboBox.addItems(
            ["跟随全局", "UTF-8", "GB18030", "ANSI(推荐)"]
        )
        self.extendedInputDeEncodingComboBox.setCurrentIndex(0)
        self.extendedMemUnitComboBox.addItems(["M", "G"])
        self.extendedMemUnitComboBox.setCurrentIndex(0)

        # 导入
        self.importSubtitleLabel.setText("导入")
        self.importNewServerFirstGuideTitle.setText("  请选择导入服务器的方式：")
        self.importNewServerTypeComboBox.addItems(
            [
                "选择一项",
                "导入 不含开服脚本的 完整的 服务器",
                "导入 含开服脚本的 完整的 服务器",
                "导入 服务器 存档(没有开服脚本、没有服务器核心)",
                "导入 MCSL 1 的服务器",
                "导入 MCSL 2 的服务器",
                "导入 MSL 的服务器",
                "导入 灵工艺我的世界「轻」开服器 的服务器",
                "导入 MCSManager 8 的服务器",
                "导入 MCSManager 9 的服务器",
            ]
        )

        # 引导页绑定
        self.noobNewServerBtn.clicked.connect(self.newServerStackedWidgetNavigation)
        self.extendedNewServerBtn.clicked.connect(self.newServerStackedWidgetNavigation)
        self.importNewServerBtn.clicked.connect(self.newServerStackedWidgetNavigation)

        # 简易模式绑定
        self.noobBackToGuidePushButton.clicked.connect(
            lambda: self.newServerStackedWidget.setCurrentIndex(0)
        )
        self.noobDownloadJavaPrimaryPushBtn.clicked.connect(
            lambda: InfoBar.info(
                title="切换到MCSLAPI",
                content="因为FastMirror没有Java啊 (",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent(),
            )
        )
        self.extendedDownloadJavaPrimaryPushBtn.clicked.connect(
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
        self.noobManuallyAddJavaPrimaryPushBtn.clicked.connect(self.addJavaManually)
        self.noobAutoDetectJavaPrimaryPushBtn.clicked.connect(self.autoDetectJava)
        self.noobManuallyAddCorePrimaryPushBtn.clicked.connect(self.addCoreManually)
        self.noobAddCoreFromDownloadedPrimaryPushBtn.clicked.connect(self.showDownloadEntries)
        self.noobSaveServerPrimaryPushBtn.clicked.connect(self.finishNewServer)

        # 进阶模式绑定
        self.extendedBackToGuidePushButton.clicked.connect(
            lambda: self.newServerStackedWidget.setCurrentIndex(0)
        )
        self.extendedManuallyAddJavaPrimaryPushBtn.clicked.connect(self.addJavaManually)
        self.extendedAutoDetectJavaPrimaryPushBtn.clicked.connect(self.autoDetectJava)
        self.extendedManuallyAddCorePrimaryPushBtn.clicked.connect(self.addCoreManually)
        self.extendedAddCoreFromDownloadedPrimaryPushBtn.clicked.connect(self.showDownloadEntries)
        self.extendedSaveServerPrimaryPushBtn.clicked.connect(self.finishNewServer)

        # 导入法绑定
        self.importBackToGuidePushButton.clicked.connect(
            lambda: self.newServerStackedWidget.setCurrentIndex(0)
        )
        self.goBtn.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(
                self.importNewServerTypeComboBox.currentIndex()
            )
        )

        self.noobNewServerScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.extendedNewServerScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.noShellArchives.noShellArchivesBackToMain.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(0)
        )
        self.shellArchives.shellArchivesBackToMain.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(0)
        )
        self.serverArchiveSite.serverArchiveSiteBackToMain.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(0)
        )
        self.MCSLv1.MCSLv1BackToMain.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(0)
        )
        self.MCSLv2.MCSLv2BackToMain.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(0)
        )
        self.MSL3.MSL3BackToMain.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(0)
        )
        self.NullCraft.NullCraftBackToMain.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(0)
        )
        self.MCSM8.MCSM8BackToMain.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(0)
        )
        self.MCSM9.MCSM9BackToMain.clicked.connect(
            lambda: self.importNewServerStackWidget.setCurrentIndex(0)
        )

        self.settingsRunner_newServerType()
        # self.importNewServerBtn.setEnabled(False)

    def settingsRunner_newServerType(self):
        self.newServerStackedWidget.setCurrentIndex(
            settingsVariables.newServerTypeList.index(
                settingsController.fileSettings["newServerType"]
            )
        )

    def newServerStackedWidgetNavigation(self):
        """决定新建服务器的方式"""
        naviList = [
            "PlaceHolder",
            self.noobNewServerBtn,
            self.extendedNewServerBtn,
            self.importNewServerBtn,
        ]
        self.newServerStackedWidget.setCurrentIndex(naviList.index(self.sender()))

    def addJavaManually(self):
        """手动添加Java"""
        selectedJavaPath = str(
            QFileDialog.getOpenFileName(self, "选择java.exe程序", getcwd(), "java.exe")[0]
        )
        if selectedJavaPath != "":
            selectedJavaPath = selectedJavaPath.replace("/", "\\")
            if v := javaDetector.getJavaVersion(selectedJavaPath):
                currentJavaPaths = configureServerVariables.javaPath
                if (
                        java := javaDetector.Java(selectedJavaPath, v)
                ) not in currentJavaPaths:
                    currentJavaPaths.append(javaDetector.Java(selectedJavaPath, v))
                    javaDetector.sortJavaList(currentJavaPaths)
                    InfoBar.success(
                        title="已添加",
                        content=f"Java路径：{selectedJavaPath}\n版本：{v}\n但你还需要继续到Java列表中选取。",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self,
                    )
                else:
                    InfoBar.warning(
                        title="未添加",
                        content="此Java已被添加过，也有可能是自动查找Java时已经搜索到了。请检查Java列表。",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=4848,
                        parent=self,
                    )
                javaDetector.saveJavaList(currentJavaPaths)
            else:
                InfoBar.error(
                    title="添加失败",
                    content="此Java无效！",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
        else:
            InfoBar.warning(
                title="未添加",
                content="你并没有选择Java。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def autoDetectJava(self):
        """自动查找Java"""
        # 防止同时多次运行worker线程
        self.noobAutoDetectJavaPrimaryPushBtn.setEnabled(False)
        self.extendedAutoDetectJavaPrimaryPushBtn.setEnabled(False)
        self.javaFindWorkThreadFactory.create().start()

    @pyqtSlot(list)
    def autoDetectJavaFinished(self, _JavaPaths: list):
        """自动查找Java结果处理"""
        if osp.exists("MCSL2/AutoDetectJavaHistory.txt"):
            remove("MCSL2/AutoDetectJavaHistory.txt")
        if osp.exists("MCSL2/AutoDetectJavaHistory.json"):
            remove("MCSL2/AutoDetectJavaHistory.json")

        savedJavaList = javaDetector.loadJavaList()
        invaildJavaList = []
        javaList = javaDetector.combineJavaList(
            savedJavaList, _JavaPaths, invaild=invaildJavaList
        )
        javaDetector.sortJavaList(javaList, reverse=False)
        configureServerVariables.javaPath = javaList
        javaDetector.saveJavaList(javaList)
        for java in invaildJavaList:
            InfoBar.error(
                title=f"Java: {java.version} 已失效",
                content=f"位于{java.path}的{java.version}已失效",
            )

    @pyqtSlot(int)
    def onJavaFindWorkThreadFinished(self, sequenceNumber):
        """自动查找Java结束后的处理"""
        if sequenceNumber > 1:
            InfoBar.success(
                title="查找完毕",
                content=f"一共搜索到了{len(configureServerVariables.javaPath)}个Java。\n请单击“Java列表”按钮查看、选择。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

        self.noobAutoDetectJavaPrimaryPushBtn.setEnabled(True)
        self.extendedAutoDetectJavaPrimaryPushBtn.setEnabled(True)

    def addCoreManually(self):
        """手动添加服务器核心"""
        tmpCorePath = str(
            QFileDialog.getOpenFileName(self, "选择*.jar文件", getcwd(), "*.jar")[0]
        ).replace("/", "\\")
        if tmpCorePath != "":
            configureServerVariables.corePath = tmpCorePath
            configureServerVariables.coreFileName = tmpCorePath.split("\\")[-1]
            InfoBar.success(
                title="已添加",
                content=f"核心文件名：{configureServerVariables.coreFileName}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        else:
            InfoBar.warning(
                title="未添加",
                content=f"你并没有选择服务器核心。\n当前核心:{'未添加' if not (a := configureServerVariables.coreFileName) else a}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def showDownloadEntries(self):
        """显示下载条目"""
        self.downloadEntry = DownloadEntryBox(self)
        if self.downloadEntry.exec() == 1:
            coreName, coreType, mcVersion, buildVersion = [e.text() for e in
                                                           self.downloadEntry.entryView.selectedItems()]
            configureServerVariables.corePath = osp.join("MCSL2", "Downloads", coreName)
            configureServerVariables.coreFileName = coreName
            configureServerVariables.serverType = coreType.lower()
            configureServerVariables.extraData = {
                "mc_version": mcVersion,
                "build_version": buildVersion
            }
            InfoBar.success(
                title="已添加",
                content=f"核心文件名：{configureServerVariables.coreFileName}\n类型:{coreType}\nMC版本:{mcVersion}\n构建版本:{buildVersion}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        else:
            InfoBar.warning(
                title="未添加",
                content=f"你并没有选择服务器核心。\n当前核心:{'未添加' if not (a := configureServerVariables.coreFileName) else a}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        del self.downloadEntry
        self.downloadEntry = None

    def checkJavaSet(self):
        """检查Java设置"""
        if configureServerVariables.selectedJavaPath != "":
            return "Java检查: 正常", 0
        else:
            return "Java检查: 出错，缺失", 1

    def checkMemSet(self, currentNewServerType):
        """检查内存设置"""
        minMemLineEditItems = [
            None,
            self.noobMinMemLineEdit,
            self.extendedMinMemLineEdit,
        ]
        maxMemLineEditItems = [
            None,
            self.noobMaxMemLineEdit,
            self.extendedMaxMemLineEdit,
        ]

        # 是否为空
        if (
                minMemLineEditItems[currentNewServerType].text() != ""
                and maxMemLineEditItems[currentNewServerType].text() != ""
        ):
            # 是否是数字
            if (
                    minMemLineEditItems[currentNewServerType].text().isdigit()
                    and maxMemLineEditItems[currentNewServerType].text().isdigit()
            ):
                # 是否为整数
                if (
                        int(minMemLineEditItems[currentNewServerType].text()) % 1 == 0
                        and int(maxMemLineEditItems[currentNewServerType].text()) % 1 == 0
                ):
                    # 是否为整数
                    if int(minMemLineEditItems[currentNewServerType].text()) <= int(
                            maxMemLineEditItems[currentNewServerType].text()
                    ):
                        # 设!
                        configureServerVariables.minMem = int(
                            minMemLineEditItems[currentNewServerType].text()
                        )
                        configureServerVariables.maxMem = int(
                            maxMemLineEditItems[currentNewServerType].text()
                        )
                        return "内存检查: 正常", 0

                    else:
                        return "内存检查: 出错, 最小内存必须小于等于最大内存", 1
                else:
                    return "内存检查: 出错, 不为整数", 1
            else:
                return "内存检查: 出错, 不为数字", 1
        else:
            return "内存检查: 出错, 内容为空", 1

    def checkCoreSet(self):
        """检查核心设置"""
        if (
                configureServerVariables.corePath != ""
                and configureServerVariables.coreFileName != ""
        ):
            return "核心检查: 正常", 0
        else:
            return "核心检查: 出错，缺失", 1

    def checkServerNameSet(self, currentNewServerType):
        """检查服务器名称设置"""
        errText = "服务器名称检查: 出错"
        isError: int
        illegalServerCharacterList = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
        serverNameLineEditItems = [
            None,
            self.noobServerNameLineEdit,
            self.extendedServerNameLineEdit,
        ]
        illegalServerNameList = [
            "aux",
            "prn",
            "con",
            "lpt1",
            "lpt2",
            "nul",
            "com0",
            "com1",
            "com2",
            "com3",
            "com4",
            "com5",
            "com6",
            "com7",
            "com8",
            "com9",
        ]

        for i in range(len(illegalServerNameList)):
            if (
                    illegalServerNameList[i]
                    == serverNameLineEditItems[currentNewServerType].text()
            ):
                errText += "，名称与操作系统冲突"
                isError = 1
                break
            else:
                isError = 0
        for eachIllegalServerCharacter in illegalServerCharacterList:
            if (
                    not eachIllegalServerCharacter
                        in serverNameLineEditItems[currentNewServerType].text()
            ):
                pass
            else:
                errText += "，名称含有不合法字符"
                isError = 1
                break
        if serverNameLineEditItems[currentNewServerType].text() == "":
            errText += "，未填写"
            isError = 1
        if isError == 1:
            return errText, isError
        else:
            configureServerVariables.serverName = serverNameLineEditItems[
                currentNewServerType
            ].text()
            return "服务器名称检查: 正常", isError

    def checkDeEncodingSet(self, currentNewServerType):
        """检查编码设置"""
        # Noob
        if currentNewServerType == 1:
            configureServerVariables.consoleOutputDeEncoding = (
                configureServerVariables.consoleDeEncodingList[0]
            )
            configureServerVariables.consoleInputDeEncoding = (
                configureServerVariables.consoleDeEncodingList[0]
            )
            return "编码检查：正常（自动处理）", 0
        # Extended
        elif currentNewServerType == 2:
            configureServerVariables.consoleOutputDeEncoding = (
                configureServerVariables.consoleDeEncodingList[
                    self.extendedOutputDeEncodingComboBox.currentIndex()
                ]
            )
            configureServerVariables.consoleInputDeEncoding = (
                configureServerVariables.consoleDeEncodingList[
                    self.extendedInputDeEncodingComboBox.currentIndex()
                ]
            )
            return "编码检查：正常（手动设置）", 0

    def checkJVMArgSet(self, currentNewServerType):
        """检查JVM参数设置"""
        if currentNewServerType == 2:
            # 有写
            if self.JVMArgPlainTextEdit.toPlainText() != "":
                configureServerVariables.jvmArg = (
                    self.JVMArgPlainTextEdit.toPlainText().split(" ")
                )
                return "JVM参数检查：正常（手动设置）", 0
            # 没写
            else:
                configureServerVariables.jvmArg = ["-Dlog4j2.formatMsgNoLookups=true"]
                return "JVM参数检查：正常（无手动参数，自动启用log4j2防护）", 0
        elif currentNewServerType == 1:
            configureServerVariables.jvmArg = ["-Dlog4j2.formatMsgNoLookups=true"]
            return "JVM参数检查：正常（无手动参数，自动启用log4j2防护）", 0

    def checkMemUnitSet(self, currentNewServerType):
        """检查JVM内存堆单位设置"""
        if currentNewServerType == 1:
            configureServerVariables.memUnit = configureServerVariables.memUnitList[0]
            return "JVM内存堆单位检查：正常（自动设置）", 0
        elif currentNewServerType == 2:
            configureServerVariables.memUnit = configureServerVariables.memUnitList[
                self.extendedMemUnitComboBox.currentIndex()
            ]
            return "JVM内存堆单位检查：正常（手动设置）", 0

    def setJavaPath(self, selectedJavaPath):
        """选择Java后处理Java路径"""
        configureServerVariables.selectedJavaPath = selectedJavaPath

    def setJavaVer(self, selectedJavaVer):
        """选择Java后处理Java版本"""
        configureServerVariables.selectedJavaVersion = selectedJavaVer
        javaVersionLabelItems = [
            None,
            self.noobJavaInfoLabel,
            self.extendedJavaInfoLabel,
        ]
        javaVersionLabelItems[self.newServerStackedWidget.currentIndex()].setText(
            f"已选择，版本{selectedJavaVer}"
        )

    def finishNewServer(self):
        """完成新建服务器的检查触发器"""
        # 定义
        currentNewServerType = self.newServerStackedWidget.currentIndex()
        # 检查
        javaResult = self.checkJavaSet()
        memResult = self.checkMemSet(currentNewServerType)
        coreResult = self.checkCoreSet()
        serverNameResult = self.checkServerNameSet(currentNewServerType)
        consoleDeEncodingResult = self.checkDeEncodingSet(currentNewServerType)
        jvmArgResult = self.checkJVMArgSet(currentNewServerType)
        memUnitResult = self.checkMemUnitSet(currentNewServerType)
        totalResultMsg = (
            f"{javaResult[0]}\n"
            f"{memResult[0]}\n"
            f"{memUnitResult[0]}\n"
            f"{coreResult[0]}\n"
            f"{serverNameResult[0]}\n"
            f"{consoleDeEncodingResult[0]}\n"
            f"{jvmArgResult[0]}"
        )
        totalResultIndicator = [
            javaResult[1],
            memResult[1],
            memUnitResult[1],
            coreResult[1],
            serverNameResult[1],
            consoleDeEncodingResult[1],
            jvmArgResult[1],
        ]
        # 错了多少
        errCount = 0
        for indicator in totalResultIndicator:
            if indicator == 1:
                errCount += 1
            else:
                pass
        # 如果出错
        if errCount != 0:
            title = f"创建服务器失败！有{errCount}个问题。"
            content = f"{totalResultMsg}\n----------------------------\n请根据上方提示，修改后再尝试保存。\n如果确认自己填写的没有问题，请联系开发者。"
            w = MessageBox(title, content, self)
            w.yesButton.setText("好的")
            w.cancelButton.setParent(None)
            w.exec()
        else:
            totalJVMArg: str = "\n".join(configureServerVariables.jvmArg)
            title = f"请再次检查你设置的参数是否有误："
            content = (
                f"{totalResultMsg}\n"
                f"----------------------------\n"
                f"Java：{configureServerVariables.selectedJavaPath}\n"
                f"Java版本：{configureServerVariables.selectedJavaVersion}\n"
                f"内存：{str(configureServerVariables.minMem)}{configureServerVariables.memUnit}~{str(configureServerVariables.maxMem)}{configureServerVariables.memUnit}\n"
                f"服务器核心：{configureServerVariables.corePath}\n"
                f"服务器核心文件名：{configureServerVariables.coreFileName}\n"
                f"输出编码设置：{self.extendedOutputDeEncodingComboBox.itemText(configureServerVariables.consoleDeEncodingList.index(configureServerVariables.consoleOutputDeEncoding))}\n"
                f"输入编码设置：{self.extendedInputDeEncodingComboBox.itemText(configureServerVariables.consoleDeEncodingList.index(configureServerVariables.consoleInputDeEncoding))}\n"
                f"JVM参数：\n"
                f"    {totalJVMArg}\n"
                f"服务器名称：{configureServerVariables.serverName}"
            )
            w = MessageBox(title, content, self)
            w.yesButton.setText("无误，添加")
            w.yesSignal.connect(self.preNewServerDispatcher)
            w.cancelButton.setText("我再看看")
            w.exec()

    def preNewServerDispatcher(self):
        """
        在self.saveNewServer() >>前<< (pre)，处理不同serverType而引起的差异性!
        """
        serverType = configureServerVariables.serverType

        # serverType dispatcher: 总的处理关于serverType不同而引起的新建服务器前的差异性!
        if serverType == "forge":  # case 1
            w = MessageBox(
                "这是Forge安装器", "是否需要自动安装Forge服务端？", self
            )
            w.yesButton.setText("是")
            w.cancelButton.setText("不需要")
            # 如果选no
            if w.exec() == 0:
                configureServerVariables.serverType = ""
                configureServerVariables.extraData = {}

        elif serverType == "vanilla":  # case 2

            pass

        else:
            if (t := ForgeInstaller.isPossibleForgeInstaller(configureServerVariables.corePath)) is not None:
                mcVersion, forgeVersion = t
                w = MessageBox(
                    "这是不是一个Forge服务器？",
                    f"检测到可能为{mcVersion}版本的Forge：{forgeVersion}\n另外,由于Forge的安装比较离谱，所以我们需要询问您以对此类服务器进行特殊优化。",
                    self
                )
                w.yesButton.setText("是")
                w.cancelButton.setText("不是")
                # 如果选yes
                if w.exec() == 1:
                    configureServerVariables.serverType = "forge"

        self.saveNewServer()  # 真正执行保存服务器

    def postNewServerDispatcher(self, exit0Msg=""):
        """
        在self.saveNewServer() >>后<< (post)，处理不同serverType而引起的差异性!
        其实通常是在self.saveNewServer()复制完核心后执行的，用于处理类似forge安装等
        """
        if configureServerVariables.serverType == "forge":
            self.installingForgeStateToolTip = StateToolTip(
                "安装Forge", "请稍后，正在安装...", self
            )
            self.installingForgeStateToolTip.move(
                self.installingForgeStateToolTip.getSuitablePos()
            )
            self.installingForgeStateToolTip.show()
            try:

                self.forgeInstaller = ForgeInstaller(
                    serverPath=f"Servers//{configureServerVariables.serverName}",
                    file=configureServerVariables.coreFileName,
                    java=configureServerVariables.selectedJavaPath,
                    logDecode=settingsController.fileSettings["outputDeEncoding"],
                )

                configureServerVariables.extraData[
                    "forge_version"
                ] = self.forgeInstaller.forgeVersion
                self.forgeInstaller.installFinished.connect(self.afterInstallingForge)

                # init installerLogViewer
                self.installerLogViewer = ForgeInstallerProgressBox(self.forgeInstaller.installerLogOutput, self)
                self.installerLogViewer.yesButton.clicked.connect(lambda: self.forgeInstaller.cancelInstall())
                self.installerLogViewer.cancelButton.clicked.connect(lambda: self.installerLogViewer.hide())
                self.installerLogViewer.setModal(True)
                self.forgeInstaller.downloadServerProgress.connect(lambda text:{
                    self.installerLogViewer.titleLabel.setText(f"Forge安装器{text}"),
                })
                self.forgeInstaller.downloadServerFinished.connect(lambda _: {
                    self.installerLogViewer.titleLabel.setText(f"Forge安装器(正在安装...)")
                })
                self.installerLogViewer.show()

                self.forgeInstaller.asyncInstall()
            except Exception as e:
                self.afterInstallingForge(False, e.args)
                self.addNewServerRollback()
        else:
            InfoBar.success(
                title="成功",
                content=exit0Msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def saveNewServer(self):
        """真正的保存服务器函数"""
        exit0Msg = f'添加服务器"{configureServerVariables.serverName}"成功！'
        exit1Msg = f'添加服务器"{configureServerVariables.serverName}"失败！'
        exitCode = 0

        # 检查JVM参数防止意外无法启动服务器
        for arg in configureServerVariables.jvmArg:
            if arg == "" or arg == " ":
                configureServerVariables.jvmArg.pop(
                    configureServerVariables.jvmArg.index(arg)
                )

        serverConfig = {
            "name": configureServerVariables.serverName,
            "core_file_name": configureServerVariables.coreFileName,
            "java_path": configureServerVariables.selectedJavaPath,
            "min_memory": configureServerVariables.minMem,
            "max_memory": configureServerVariables.maxMem,
            "memory_unit": configureServerVariables.memUnit,
            "jvm_arg": configureServerVariables.jvmArg,
            "output_decoding": configureServerVariables.consoleOutputDeEncoding,
            "input_encoding": configureServerVariables.consoleInputDeEncoding,
            "icon": "Grass.png",
            "server_type": configureServerVariables.serverType,
            "extra_data": configureServerVariables.extraData,
        }

        # 新建文件夹
        try:
            mkdir(f"Servers//{configureServerVariables.serverName}")
        except FileExistsError:
            InfoBar.error(
                title="失败",
                content="已存在同名服务器!,请更改服务器名",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            return

        # 写入全局配置
        try:
            with open(
                    r"MCSL2/MCSL2_ServerList.json", "r", encoding="utf-8"
            ) as globalServerListFile:
                # old
                globalServerList = loads(globalServerListFile.read())
                globalServerListFile.close()

            with open(
                    r"MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
            ) as newGlobalServerListFile:
                # 添加新的
                globalServerList["MCSLServerList"].append(serverConfig)
                newGlobalServerListFile.write(dumps(globalServerList, indent=4))
            exitCode = 0
        except Exception as e:
            exitCode = 1
            exit1Msg += f"\n{e}"

        # 写入单独配置
        try:
            if not settingsController.fileSettings["onlySaveGlobalServerConfig"]:
                with open(
                        f"Servers//{configureServerVariables.serverName}//MCSL2ServerConfig.json",
                        "w+",
                        encoding="utf-8",
                ) as serverListFile:
                    serverListFile.write(dumps(serverConfig, indent=4))
            else:
                InfoBar.info(
                    title="功能提醒",
                    content=f"您在设置中开启了“只保存全局服务器设置”。\n将不会保存单独服务器设置。\n这有可能导致服务器迁移较为繁琐。",
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

        # 复制核心
        try:
            copy(
                configureServerVariables.corePath,
                f"./Servers/{configureServerVariables.serverName}/{configureServerVariables.coreFileName}",
            )
        except Exception as e:
            exitCode = 1
            exit1Msg += f"\n{e}"

        # 自动同意Mojang Eula
        if settingsController.fileSettings["acceptAllMojangEula"]:
            tmpServerName = serverVariables.serverName
            serverVariables.serverName = configureServerVariables.serverName
            MinecraftEulaInfoBar = InfoBar(
                icon=FIF.INFO,
                title="功能提醒",
                content="您开启了“创建时自动同意服务器的Eula”功能。\n如需要查看Minecraft Eula，请点击右边的按钮。",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=10000,
                position=InfoBarPosition.TOP,
                parent=self,
            )
            MinecraftEulaInfoBar.setCustomBackgroundColor('white', '#202020')
            MinecraftEulaInfoBar.addWidget(
                HyperlinkButton(
                    url="https://aka.ms/MinecraftEULA",
                    text="Eula",
                    parent=MinecraftEulaInfoBar,
                    icon=FIF.LINK,
                )
            )
            MinecraftEulaInfoBar.show()
            MojangEula().acceptEula()
            serverVariables.serverName = tmpServerName

        if exitCode == 0:

            self.postNewServerDispatcher(
                exit0Msg=exit0Msg)  # 后处理各种应serverType不同而引起的差异性，例如serverType==forge时，需要执行自动安装等等...

            if settingsController.fileSettings["clearAllNewServerConfigInProgram"]:
                configureServerVariables.resetToDefault()
                if self.newServerStackedWidget.currentIndex() == 1:
                    self.noobJavaInfoLabel.setText("[选择的Java的信息]")
                    self.noobMinMemLineEdit.setText("")
                    self.noobMaxMemLineEdit.setText("")
                    self.noobServerNameLineEdit.setText("")
                elif self.newServerStackedWidget.currentIndex() == 2:
                    self.extendedJavaInfoLabel.setText("[选择的Java的信息]")
                    self.extendedMinMemLineEdit.setText("")
                    self.extendedMaxMemLineEdit.setText("")
                    self.extendedServerNameLineEdit.setText("")
                    self.extendedOutputDeEncodingComboBox.setCurrentIndex(0)
                    self.extendedInputDeEncodingComboBox.setCurrentIndex(0)
                    self.JVMArgPlainTextEdit.setPlainText("")
                InfoBar.info(
                    title="功能提醒",
                    content="”新建服务器后立刻清空相关设置项“已被开启。\n这是一个强迫症功能。如果需要关闭，请转到设置页。",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )

        else:
            InfoBar.error(
                title="失败",
                content=exit1Msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def addNewServerRollback(self):
        """新建服务器失败后的回滚"""
        if osp.exists(serverDir := f"Servers//{configureServerVariables.serverName}"):  # 防止出现重复回滚的操作
            # 删除文件夹
            rmtree(serverDir)
            # 删除全局配置
            with open(
                    r"MCSL2/MCSL2_ServerList.json", "r", encoding="utf-8"
            ) as globalServerListFile:
                # old
                globalServerList = loads(globalServerListFile.read())
                globalServerListFile.close()

            with open(
                    r"MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
            ) as newGlobalServerListFile:
                # 删除新的
                globalServerList["MCSLServerList"].pop()
                newGlobalServerListFile.write(dumps(globalServerList, indent=4))

    @pyqtSlot(bool)
    def afterInstallingForge(self, installFinished, args=...):
        self.installerLogViewer.hide()
        self.installerLogViewer.close()
        self.installerLogViewer.deleteLater()
        if installFinished:
            self.installingForgeStateToolTip.setContent("安装成功！")
            self.installingForgeStateToolTip.setState(True)
            self.installingForgeStateToolTip = None
        else:
            self.installingForgeStateToolTip.setContent(f"怪，安装失败！{args if args is not ... else ''}")
            self.installingForgeStateToolTip.setState(True)
            self.installingForgeStateToolTip = None
            self.addNewServerRollback()
            MCSLLogger.warning(f"{self.__class__.__name__} 回滚")
        if hasattr(self, "forgeInstaller"):  # 有可能在创建forgeInstaller那边就抛出了异常(例如invalid forge installer 等等),故 需要判断是否已经初始化
            del self.forgeInstaller
        configureServerVariables.resetToDefault()  # 重置

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
Download page with FastMirror, MCSL-Sync, and PolarsAPI.
"""

from os import path as osp, remove

from PyQt5.QtCore import Qt, QSize, QRect, pyqtSlot
from PyQt5.QtWidgets import (
    QSizePolicy,
    QWidget,
    QFrame,
    QGridLayout,
    QVBoxLayout,
    QSpacerItem,
    QStackedWidget,
    QButtonGroup,
)
from PyQt5 import sip

from qfluentwidgets import (
    StrongBodyLabel,
    SubtitleLabel,
    TitleLabel,
    PushButton,
    FluentIcon as FIF,
    MessageBox,
    InfoBarPosition,
    InfoBar,
    StateToolTip,
    TransparentPushButton,
    TransparentTogglePushButton,
    VerticalSeparator,
    BodyLabel,
    HyperlinkButton,
    LineEdit,
)

from MCSL2Lib.Widgets.DownloadEntryViewerWidget import DownloadEntryBox
from MCSL2Lib.Widgets.DownloadProgressWidget import DownloadCard
from MCSL2Lib.ProgramControllers.DownloadAPI.FastMirrorAPI import (
    FetchFastMirrorAPIThreadFactory,
    FetchFastMirrorAPICoreVersionThreadFactory,
)
from MCSL2Lib.Widgets.PolarsWidgets import PolarsTypeWidget
from MCSL2Lib.Widgets.FastMirrorWidgets import (
    FastMirrorBuildListWidget,
    FastMirrorCorePushButton,
    FastMirrorVersionButton,
)
from MCSL2Lib.Widgets.MCSLSyncWidgets import (
    MCSLSyncCorePushButton,
    MCSLSyncVersionButton,
)
from MCSL2Lib.ProgramControllers.DownloadAPI.MCSLSyncAPI import (
    FetchMCSLSyncCoreListThreadFactory,
    FetchMCSLSyncCoreVersionsThreadFactory,
    FetchMCSLSyncCoreBuildsThreadFactory,
    FetchMCSLSyncBuildDetailsThreadFactory,
)
from MCSL2Lib.ProgramControllers.DownloadAPI.PolarsAPI import (
    FetchPolarsAPICoreThreadFactory,
    FetchPolarsAPITypeThreadFactory,
)
from MCSL2Lib.ProgramControllers.multiThreadDownloadController import MultiThreadDownloadController
from MCSL2Lib.ProgramControllers.interfaceController import (
    MySmoothScrollArea,
)
from MCSL2Lib.ProgramControllers.settingsController import cfg
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.Resources.icons import *  # noqa: F401 F403
from MCSL2Lib.utils import openLocalFile
from MCSL2Lib.variables import (
    DownloadVariables,
    SettingsVariables,
)

downloadVariables = DownloadVariables()
settingsVariables = SettingsVariables()


@Singleton
class DownloadPage(QWidget):
    """下载页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # fmt: off
        self.fetchFMAPIThreadFactory = FetchFastMirrorAPIThreadFactory()
        self.fetchFMAPICoreVersionThreadFactory = FetchFastMirrorAPICoreVersionThreadFactory()

        self.fetchMCSLSyncCoreListThreadFactory = FetchMCSLSyncCoreListThreadFactory()
        self.fetchMCSLSyncCoreVersionsThreadFactory = FetchMCSLSyncCoreVersionsThreadFactory()
        self.fetchMCSLSyncCoreBuildsThreadFactory = FetchMCSLSyncCoreBuildsThreadFactory()
        self.fetchMCSLSyncBuildDetailsThreadFactory = FetchMCSLSyncBuildDetailsThreadFactory()

        self.fetchPolarsAPITypeThreadFactory = FetchPolarsAPITypeThreadFactory()
        self.fetchPolarsAPICoreThreadFactory = FetchPolarsAPICoreThreadFactory()
        # fmt: on

        # 线程管理
        self.active_threads = []
        self.mcsl_sync_build_threads = []

        # 初始化临时变量
        self._pending_builds = []
        self._completed_builds = 0
        self._total_builds = 0

        self.fmBtnGroup = QButtonGroup(self)
        self.fmVersionBtnGroup = QButtonGroup(self)
        self.mcsLSyncCoreBtnGroup = QButtonGroup(self)
        self.mcsLSyncVersionBtnGroup = QButtonGroup(self)
        self.polarsBtnGroup = QButtonGroup(self)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")
        self.gridLayout_4 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout_4.addWidget(self.titleLabel, 0, 0, 1, 1)

        self.createCustomDownloadBtn = TransparentPushButton(
            text=self.tr("自定义下载"), parent=self.titleLimitWidget, icon=FIF.ADD_TO
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createCustomDownloadBtn.sizePolicy().hasHeightForWidth())
        self.createCustomDownloadBtn.setSizePolicy(sizePolicy)
        self.createCustomDownloadBtn.setObjectName("createCustomDownloadBtn")
        self.gridLayout_4.addWidget(self.createCustomDownloadBtn, 0, 1, 1, 1)

        self.openDownloadFolderBtn = TransparentPushButton(
            text=self.tr("打开下载文件夹"),
            parent=self.titleLimitWidget,
            icon=FIF.FOLDER,
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openDownloadFolderBtn.sizePolicy().hasHeightForWidth())
        self.openDownloadFolderBtn.setSizePolicy(sizePolicy)
        self.openDownloadFolderBtn.setObjectName("openDownloadFolderBtn")
        self.gridLayout_4.addWidget(self.openDownloadFolderBtn, 0, 2, 1, 1)

        self.openDownloadEntriesBtn = TransparentPushButton(
            text=self.tr("打开下载记录"), parent=self.titleLimitWidget, icon=FIF.MENU
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openDownloadEntriesBtn.sizePolicy().hasHeightForWidth())
        self.openDownloadEntriesBtn.setSizePolicy(sizePolicy)
        self.openDownloadEntriesBtn.setObjectName("openDownloadEntriesBtn")
        self.gridLayout_4.addWidget(self.openDownloadEntriesBtn, 0, 3, 1, 1)

        self.showDownloadingItemBtn = TransparentTogglePushButton(
            text=self.tr("展开下载中列表"), parent=self.titleLimitWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showDownloadingItemBtn.sizePolicy().hasHeightForWidth())
        self.showDownloadingItemBtn.setSizePolicy(sizePolicy)
        self.showDownloadingItemBtn.setObjectName("showDownloadingItemBtn")
        self.gridLayout_4.addWidget(self.showDownloadingItemBtn, 0, 4, 1, 1)

        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")
        self.gridLayout_4.addWidget(self.subTitleLabel, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 2, 3)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.downloadStackedWidget = QStackedWidget(self)
        self.downloadStackedWidget.setObjectName("downloadStackedWidget")

        self.downloadWithFastMirror = QWidget()
        self.downloadWithFastMirror.setObjectName("downloadWithFastMirror")

        self.gridLayout_2 = QGridLayout(self.downloadWithFastMirror)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.versionSubtitleLabel = SubtitleLabel(self.downloadWithFastMirror)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.versionSubtitleLabel.setSizePolicy(sizePolicy)
        self.versionSubtitleLabel.setObjectName("versionSubtitleLabel")

        self.gridLayout_2.addWidget(self.versionSubtitleLabel, 0, 1, 1, 1)
        self.coreListSmoothScrollArea = MySmoothScrollArea(self.downloadWithFastMirror)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coreListSmoothScrollArea.sizePolicy().hasHeightForWidth())
        self.coreListSmoothScrollArea.setSizePolicy(sizePolicy)
        self.coreListSmoothScrollArea.setMinimumSize(QSize(160, 0))
        self.coreListSmoothScrollArea.setMaximumSize(QSize(160, 16777215))
        self.coreListSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.coreListSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.coreListSmoothScrollArea.setWidgetResizable(True)
        self.coreListSmoothScrollArea.setObjectName("coreListSmoothScrollArea")

        self.coreListScrollAreaWidgetContents = QWidget()
        self.coreListScrollAreaWidgetContents.setGeometry(QRect(0, 0, 200, 349))
        self.coreListScrollAreaWidgetContents.setObjectName("coreListScrollAreaWidgetContents")

        self.verticalLayout_14 = QVBoxLayout(self.coreListScrollAreaWidgetContents)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")

        self.coreListLayout = QVBoxLayout()
        self.coreListLayout.setObjectName("coreListLayout")

        self.verticalLayout_14.addLayout(self.coreListLayout)
        self.coreListSmoothScrollArea.setWidget(self.coreListScrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.coreListSmoothScrollArea, 1, 0, 1, 1)
        self.buildSubtitleLabel = SubtitleLabel(self.downloadWithFastMirror)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buildSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.buildSubtitleLabel.setSizePolicy(sizePolicy)
        self.buildSubtitleLabel.setObjectName("buildSubtitleLabel")
        self.gridLayout_2.addWidget(self.buildSubtitleLabel, 0, 2, 1, 1)
        self.coreListSubtitleLabel = SubtitleLabel(self.downloadWithFastMirror)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coreListSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.coreListSubtitleLabel.setSizePolicy(sizePolicy)
        self.coreListSubtitleLabel.setObjectName("coreListSubtitleLabel")
        self.gridLayout_2.addWidget(self.coreListSubtitleLabel, 0, 0, 1, 1)
        self.versionSmoothScrollArea = MySmoothScrollArea(self.downloadWithFastMirror)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionSmoothScrollArea.sizePolicy().hasHeightForWidth())
        self.versionSmoothScrollArea.setSizePolicy(sizePolicy)
        self.versionSmoothScrollArea.setMinimumSize(QSize(160, 0))
        self.versionSmoothScrollArea.setMaximumSize(QSize(160, 16777215))
        self.versionSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.versionSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.versionSmoothScrollArea.setWidgetResizable(True)
        self.versionSmoothScrollArea.setObjectName("versionSmoothScrollArea")

        self.versionScrollAreaWidgetContents = QWidget()
        self.versionScrollAreaWidgetContents.setGeometry(QRect(0, 0, 170, 349))
        self.versionScrollAreaWidgetContents.setObjectName("versionScrollAreaWidgetContents")

        self.verticalLayout_13 = QVBoxLayout(self.versionScrollAreaWidgetContents)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")

        self.versionLayout = QVBoxLayout()
        self.versionLayout.setObjectName("versionLayout")

        self.verticalLayout_13.addLayout(self.versionLayout)
        self.versionSmoothScrollArea.setWidget(self.versionScrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.versionSmoothScrollArea, 1, 1, 1, 1)
        self.refreshFastMirrorAPIBtn = PushButton(
            icon=FIF.UPDATE, text=self.tr("刷新"), parent=self.downloadWithFastMirror
        )
        self.refreshFastMirrorAPIBtn.setObjectName("refreshFastMirrorAPIBtn")

        self.gridLayout_2.addWidget(self.refreshFastMirrorAPIBtn, 0, 3, 1, 1)
        self.buildScrollArea = MySmoothScrollArea(self.downloadWithFastMirror)
        self.buildScrollArea.setMinimumSize(QSize(304, 0))
        self.buildScrollArea.setFrameShape(QFrame.NoFrame)
        self.buildScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.buildScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.buildScrollArea.setWidgetResizable(True)
        self.buildScrollArea.setObjectName("buildScrollArea")

        self.buildScrollAreaWidgetContents = QWidget()
        self.buildScrollAreaWidgetContents.setGeometry(QRect(0, 0, 346, 349))
        self.buildScrollAreaWidgetContents.setObjectName("buildScrollAreaWidgetContents")

        self.verticalLayout_2 = QVBoxLayout(self.buildScrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.buildLayout = QVBoxLayout()
        self.buildLayout.setObjectName("buildLayout")

        self.verticalLayout_2.addLayout(self.buildLayout)
        self.buildScrollArea.setWidget(self.buildScrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.buildScrollArea, 1, 2, 1, 2)
        self.downloadStackedWidget.addWidget(self.downloadWithFastMirror)

        self.downloadWithMCSLSync = QWidget()
        self.downloadWithMCSLSync.setObjectName("downloadWithMCSLSync")

        self.gridLayout_3 = QGridLayout(self.downloadWithMCSLSync)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.mcsLSyncVersionSubtitleLabel = SubtitleLabel(self.downloadWithMCSLSync)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mcsLSyncVersionSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.mcsLSyncVersionSubtitleLabel.setSizePolicy(sizePolicy)
        self.mcsLSyncVersionSubtitleLabel.setObjectName("mcsLSyncVersionSubtitleLabel")

        self.gridLayout_3.addWidget(self.mcsLSyncVersionSubtitleLabel, 0, 1, 1, 1)
        self.mcsLSyncCoreListSmoothScrollArea = MySmoothScrollArea(self.downloadWithMCSLSync)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mcsLSyncCoreListSmoothScrollArea.sizePolicy().hasHeightForWidth()
        )
        self.mcsLSyncCoreListSmoothScrollArea.setSizePolicy(sizePolicy)
        self.mcsLSyncCoreListSmoothScrollArea.setMinimumSize(QSize(160, 0))
        self.mcsLSyncCoreListSmoothScrollArea.setMaximumSize(QSize(160, 16777215))
        self.mcsLSyncCoreListSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.mcsLSyncCoreListSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mcsLSyncCoreListSmoothScrollArea.setWidgetResizable(True)
        self.mcsLSyncCoreListSmoothScrollArea.setObjectName("mcsLSyncCoreListSmoothScrollArea")

        self.mcsLSyncCoreListScrollAreaWidgetContents = QWidget()
        self.mcsLSyncCoreListScrollAreaWidgetContents.setGeometry(QRect(0, 0, 200, 349))
        self.mcsLSyncCoreListScrollAreaWidgetContents.setObjectName(
            "mcsLSyncCoreListScrollAreaWidgetContents"
        )

        self.verticalLayout_15 = QVBoxLayout(self.mcsLSyncCoreListScrollAreaWidgetContents)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")

        self.mcsLSyncCoreListLayout = QVBoxLayout()
        self.mcsLSyncCoreListLayout.setObjectName("mcsLSyncCoreListLayout")

        self.verticalLayout_15.addLayout(self.mcsLSyncCoreListLayout)
        self.mcsLSyncCoreListSmoothScrollArea.setWidget(
            self.mcsLSyncCoreListScrollAreaWidgetContents
        )
        self.gridLayout_3.addWidget(self.mcsLSyncCoreListSmoothScrollArea, 1, 0, 1, 1)
        self.mcsLSyncBuildSubtitleLabel = SubtitleLabel(self.downloadWithMCSLSync)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mcsLSyncBuildSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.mcsLSyncBuildSubtitleLabel.setSizePolicy(sizePolicy)
        self.mcsLSyncBuildSubtitleLabel.setObjectName("mcsLSyncBuildSubtitleLabel")
        self.gridLayout_3.addWidget(self.mcsLSyncBuildSubtitleLabel, 0, 2, 1, 1)
        self.mcsLSyncCoreListSubtitleLabel = SubtitleLabel(self.downloadWithMCSLSync)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mcsLSyncCoreListSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.mcsLSyncCoreListSubtitleLabel.setSizePolicy(sizePolicy)
        self.mcsLSyncCoreListSubtitleLabel.setObjectName("mcsLSyncCoreListSubtitleLabel")
        self.gridLayout_3.addWidget(self.mcsLSyncCoreListSubtitleLabel, 0, 0, 1, 1)
        self.mcsLSyncVersionSmoothScrollArea = MySmoothScrollArea(self.downloadWithMCSLSync)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mcsLSyncVersionSmoothScrollArea.sizePolicy().hasHeightForWidth()
        )
        self.mcsLSyncVersionSmoothScrollArea.setSizePolicy(sizePolicy)
        self.mcsLSyncVersionSmoothScrollArea.setMinimumSize(QSize(160, 0))
        self.mcsLSyncVersionSmoothScrollArea.setMaximumSize(QSize(160, 16777215))
        self.mcsLSyncVersionSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.mcsLSyncVersionSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mcsLSyncVersionSmoothScrollArea.setWidgetResizable(True)
        self.mcsLSyncVersionSmoothScrollArea.setObjectName("mcsLSyncVersionSmoothScrollArea")

        self.mcsLSyncVersionScrollAreaWidgetContents = QWidget()
        self.mcsLSyncVersionScrollAreaWidgetContents.setGeometry(QRect(0, 0, 170, 349))
        self.mcsLSyncVersionScrollAreaWidgetContents.setObjectName(
            "mcsLSyncVersionScrollAreaWidgetContents"
        )

        self.verticalLayout_16 = QVBoxLayout(self.mcsLSyncVersionScrollAreaWidgetContents)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")

        self.mcsLSyncVersionLayout = QVBoxLayout()
        self.mcsLSyncVersionLayout.setObjectName("mcsLSyncVersionLayout")

        self.verticalLayout_16.addLayout(self.mcsLSyncVersionLayout)
        self.mcsLSyncVersionSmoothScrollArea.setWidget(self.mcsLSyncVersionScrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.mcsLSyncVersionSmoothScrollArea, 1, 1, 1, 1)
        self.refreshMCSLSyncBtn = PushButton(
            icon=FIF.UPDATE, text=self.tr("刷新"), parent=self.downloadWithMCSLSync
        )
        self.refreshMCSLSyncBtn.setObjectName("refreshMCSLSyncBtn")

        self.gridLayout_3.addWidget(self.refreshMCSLSyncBtn, 0, 3, 1, 1)
        self.mcsLSyncBuildScrollArea = MySmoothScrollArea(self.downloadWithMCSLSync)
        self.mcsLSyncBuildScrollArea.setMinimumSize(QSize(304, 0))
        self.mcsLSyncBuildScrollArea.setFrameShape(QFrame.NoFrame)
        self.mcsLSyncBuildScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mcsLSyncBuildScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mcsLSyncBuildScrollArea.setWidgetResizable(True)
        self.mcsLSyncBuildScrollArea.setObjectName("mcsLSyncBuildScrollArea")

        self.mcsLSyncBuildScrollAreaWidgetContents = QWidget()
        self.mcsLSyncBuildScrollAreaWidgetContents.setGeometry(QRect(0, 0, 346, 349))
        self.mcsLSyncBuildScrollAreaWidgetContents.setObjectName(
            "mcsLSyncBuildScrollAreaWidgetContents"
        )

        self.verticalLayout_17 = QVBoxLayout(self.mcsLSyncBuildScrollAreaWidgetContents)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")

        self.mcsLSyncBuildLayout = QVBoxLayout()
        self.mcsLSyncBuildLayout.setObjectName("mcsLSyncBuildLayout")

        self.verticalLayout_17.addLayout(self.mcsLSyncBuildLayout)
        self.mcsLSyncBuildScrollArea.setWidget(self.mcsLSyncBuildScrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.mcsLSyncBuildScrollArea, 1, 2, 1, 2)
        self.downloadStackedWidget.addWidget(self.downloadWithMCSLSync)

        self.downloadWithPolarsAPI = QWidget()
        self.downloadWithPolarsAPI.setObjectName("downloadWithPolarsAPI")

        self.gridLayout_5 = QGridLayout(self.downloadWithPolarsAPI)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")

        self.polarsCoreScrollArea = MySmoothScrollArea(self.downloadWithPolarsAPI)
        self.polarsCoreScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.polarsCoreScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.polarsCoreScrollArea.setWidgetResizable(True)
        self.polarsCoreScrollArea.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.polarsCoreScrollArea.setObjectName("polarsCoreScrollArea")

        self.polarsCoreScrollAreaContents = QWidget()
        self.polarsCoreScrollAreaContents.setGeometry(QRect(0, 0, 461, 331))
        self.polarsCoreScrollAreaContents.setObjectName("polarsCoreScrollAreaContents")

        self.gridLayout_7 = QGridLayout(self.polarsCoreScrollAreaContents)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.polarsCoreLayout = QVBoxLayout()
        self.polarsCoreLayout.setObjectName("polarsCoreLayout")

        self.gridLayout_7.addLayout(self.polarsCoreLayout, 0, 0, 1, 1)
        self.polarsCoreLayout = QVBoxLayout()
        self.polarsCoreLayout.setObjectName("polarsCoreLayout")

        self.gridLayout_7.addLayout(self.polarsCoreLayout, 0, 0, 1, 1)
        self.polarsCoreScrollArea.setWidget(self.polarsCoreScrollAreaContents)
        self.gridLayout_5.addWidget(self.polarsCoreScrollArea, 2, 2, 2, 2)
        self.polarsTypeLabel = SubtitleLabel(self.downloadWithPolarsAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polarsTypeLabel.sizePolicy().hasHeightForWidth())
        self.polarsTypeLabel.setSizePolicy(sizePolicy)
        self.polarsTypeLabel.setObjectName("polarsTypeLabel")

        self.gridLayout_5.addWidget(self.polarsTypeLabel, 0, 2, 1, 1)
        self.VerticalSeparator_2 = VerticalSeparator(self.downloadWithPolarsAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VerticalSeparator_2.sizePolicy().hasHeightForWidth())
        self.VerticalSeparator_2.setSizePolicy(sizePolicy)
        self.VerticalSeparator_2.setMinimumSize(QSize(3, 0))
        self.VerticalSeparator_2.setMaximumSize(QSize(3, 16777215))
        self.VerticalSeparator_2.setObjectName("VerticalSeparator_2")

        self.gridLayout_5.addWidget(self.VerticalSeparator_2, 0, 1, 4, 1)
        self.refreshPolarsAPIBtn = PushButton(
            icon=FIF.UPDATE, text="刷新", parent=self.downloadWithPolarsAPI
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshPolarsAPIBtn.sizePolicy().hasHeightForWidth())
        self.refreshPolarsAPIBtn.setSizePolicy(sizePolicy)
        self.refreshPolarsAPIBtn.setObjectName("refreshPolarsAPIBtn")
        self.gridLayout_5.addWidget(self.refreshPolarsAPIBtn, 0, 3, 1, 1)
        self.polarsDescriptionLabel = BodyLabel(self.downloadWithPolarsAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polarsDescriptionLabel.sizePolicy().hasHeightForWidth())
        self.polarsDescriptionLabel.setSizePolicy(sizePolicy)
        self.polarsDescriptionLabel.setObjectName("polarsDescriptionLabel")

        self.gridLayout_5.addWidget(self.polarsDescriptionLabel, 1, 2, 1, 2)
        self.polarsTypeScrollArea = MySmoothScrollArea(self.downloadWithPolarsAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polarsTypeScrollArea.sizePolicy().hasHeightForWidth())
        self.polarsTypeScrollArea.setSizePolicy(sizePolicy)
        self.polarsTypeScrollArea.setMinimumSize(QSize(170, 0))
        self.polarsTypeScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.polarsTypeScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.polarsTypeScrollArea.setWidgetResizable(True)
        self.polarsTypeScrollArea.setObjectName("polarsTypeScrollArea")

        self.polarsTypeScrollAreaContents = QWidget()
        self.polarsTypeScrollAreaContents.setGeometry(QRect(0, 0, 200, 356))
        self.polarsTypeScrollAreaContents.setObjectName("polarsTypeScrollAreaContents")

        self.gridLayout_6 = QGridLayout(self.polarsTypeScrollAreaContents)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.polarsTypeLayout = QVBoxLayout()
        self.polarsTypeLayout.setObjectName("polarsTypeLayout")

        self.gridLayout_6.addLayout(self.polarsTypeLayout, 0, 0, 1, 1)
        self.polarsTypeScrollArea.setWidget(self.polarsTypeScrollAreaContents)
        self.gridLayout_5.addWidget(self.polarsTypeScrollArea, 1, 0, 3, 1)
        self.polarsTitle = SubtitleLabel(self.downloadWithPolarsAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polarsTitle.sizePolicy().hasHeightForWidth())
        self.polarsTitle.setSizePolicy(sizePolicy)
        self.polarsTitle.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.polarsTitle.setObjectName("polarsTitle")

        self.gridLayout_5.addWidget(self.polarsTitle, 0, 0, 1, 1)
        self.downloadStackedWidget.addWidget(self.downloadWithPolarsAPI)
        self.gridLayout.addWidget(self.downloadStackedWidget, 3, 2, 1, 1)

        self.VerticalSeparator = VerticalSeparator(self)
        self.VerticalSeparator.setObjectName("VerticalSeparator")

        self.gridLayout.addWidget(self.VerticalSeparator, 3, 3, 1, 1)

        self.downloadingItemWidget = MySmoothScrollArea(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadingItemWidget.sizePolicy().hasHeightForWidth())
        self.downloadingItemWidget.setSizePolicy(sizePolicy)
        self.downloadingItemWidget.setMinimumSize(QSize(310, 0))
        self.downloadingItemWidget.setMaximumSize(QSize(310, 16777215))
        self.downloadingItemWidget.setFrameShape(QFrame.NoFrame)
        self.downloadingItemWidget.setWidgetResizable(True)
        self.downloadingItemWidget.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.downloadingItemWidget.setObjectName("downloadingItemWidget")

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 310, 407))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.downloadingItemLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.downloadingItemLayout.setContentsMargins(0, 0, 0, 0)
        self.downloadingItemLayout.setObjectName("downloadingItemLayout")

        self.downloadingItemWidget.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.downloadingItemWidget, 3, 4, 1, 1)
        self.dsList = [
            self.downloadWithFastMirror,
            self.downloadWithMCSLSync,
            self.downloadWithPolarsAPI,
        ]
        self.downloadStackedWidget.setCurrentWidget(
            self.dsList[settingsVariables.get_download_source_index()]
        )

        self.setObjectName("DownloadInterface")

        self.titleLabel.setText(self.tr("下载"))
        self.subTitleLabel.setText(self.tr("多线程高速下载引擎！"))
        self.coreListSubtitleLabel.setText(self.tr("核心列表"))
        self.versionSubtitleLabel.setText(self.tr("游戏版本"))
        self.buildSubtitleLabel.setText(self.tr("构建列表"))
        self.refreshFastMirrorAPIBtn.setText(self.tr("刷新"))
        self.mcsLSyncCoreListSubtitleLabel.setText(self.tr("核心列表"))
        self.mcsLSyncVersionSubtitleLabel.setText(self.tr("游戏版本"))
        self.mcsLSyncBuildSubtitleLabel.setText(self.tr("构建列表"))
        self.refreshMCSLSyncBtn.setText(self.tr("刷新"))
        self.polarsTitle.setText("核心类型")

        self.refreshMCSLSyncBtn.clicked.connect(self.refreshMCSLSyncData)
        self.refreshPolarsAPIBtn.clicked.connect(self.getPolarsAPI)
        self.refreshFastMirrorAPIBtn.clicked.connect(self.getFastMirrorAPI)
        self.refreshMCSLSyncBtn.setEnabled(False)
        self.scrollAreaSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.createCustomDownloadBtn.clicked.connect(self.downloadCustomURLFile)
        self.openDownloadFolderBtn.clicked.connect(lambda: openLocalFile("./MCSL2/Downloads/"))
        self.openDownloadEntriesBtn.clicked.connect(
            lambda: {
                (box := DownloadEntryBox(self)),
                box.show(),
                box.raise_(),
                box.asyncGetEntries(),
            }
        )
        self.downloadingItemWidget.setFixedWidth(0)
        self.VerticalSeparator.setVisible(False)
        self.showDownloadingItemBtn.toggled.connect(self.switchDownloadingItemWidget)

    @pyqtSlot(int)
    def onPageChangedRefresh(self, currentChanged):
        if currentChanged == 3:
            index = settingsVariables.get_download_source_index()
            self.subTitleLabel.setText(
                self.tr("一键高速下载！\n当前下载源: {downloadSource}").format(
                    downloadSource=settingsVariables.downloadSourceTextList[index]
                )
            )
            self.downloadStackedWidget.setCurrentWidget(self.dsList[index])
            self.refreshDownloads()

    def refreshDownloads(self):
        """刷新下载页面主逻辑"""
        # FastMirror
        if self.downloadStackedWidget.currentIndex() == 0:
            if downloadVariables.FastMirrorAPIDict:
                if downloadVariables.FastMirrorAPIDict["name"] != -1:
                    self.initFastMirrorCoreListWidget()
                else:
                    self.showFastMirrorFailedTip()
            else:
                self.getFastMirrorAPI()
        # PolarsAPI
        elif self.downloadStackedWidget.currentIndex() == 2:
            if downloadVariables.PolarTypeDict:
                if downloadVariables.PolarTypeDict["name"] != -1:
                    self.initPolarsTypeListWidget()
                else:
                    self.showPolarsAPIFailedTip()
            else:
                self.getPolarsAPI()
        # MCSL-Sync
        elif self.downloadStackedWidget.currentIndex() == 1:
            # 如果存在列表且不为空,则不再重新获取
            if downloadVariables.MCSLSyncCoreList:
                self.initMCSLSyncCoreListWidget()
            else:
                self.getMCSLSync()
                self.refreshMCSLSyncBtn.setEnabled(False)

    ##############
    # MCSL-Sync  #
    ##############

    def releaseMCSLSyncMemory(self, id=0):
        """释放MCSL-Sync相关内存"""
        if not id:  # 核心列表
            try:
                self.mcsLSyncCoreListLayout.removeItem(self.scrollAreaSpacer)
            except AttributeError:
                pass
            for i in reversed(range(self.mcsLSyncCoreListLayout.count())):
                try:
                    self.mcsLSyncCoreListLayout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    self.mcsLSyncCoreListLayout.itemAt(i).widget().deleteLater()
                    del self.mcsLSyncCoreListLayout.itemAt(i).widget
                except AttributeError:
                    pass
        elif id == 1:  # 版本列表
            try:
                self.mcsLSyncVersionLayout.removeItem(self.scrollAreaSpacer)
            except AttributeError:
                pass
            for i in reversed(range(self.mcsLSyncVersionLayout.count())):
                try:
                    self.mcsLSyncVersionLayout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    self.mcsLSyncVersionLayout.itemAt(i).widget().deleteLater()
                    del self.mcsLSyncVersionLayout.itemAt(i).widget
                except AttributeError:
                    pass
        elif id == 2:  # 构建列表
            try:
                self.mcsLSyncBuildLayout.removeItem(self.scrollAreaSpacer)
            except AttributeError:
                pass
            for i in reversed(range(self.mcsLSyncBuildLayout.count())):
                try:
                    self.mcsLSyncBuildLayout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    self.mcsLSyncBuildLayout.itemAt(i).widget().deleteLater()
                    del self.mcsLSyncBuildLayout.itemAt(i).widget
                except AttributeError:
                    pass

    def getMCSLSync(self):
        """请求MCSL-Sync核心列表"""
        workThread = self.fetchMCSLSyncCoreListThreadFactory.create(
            _singleton=True, finishSlot=self.updateMCSLSyncCoreList
        )
        if workThread.isRunning():
            self.refreshMCSLSyncBtn.setEnabled(False)
            return
        else:
            self.getMCSLSyncStateToolTip = StateToolTip(
                self.tr("正在请求 MCSL-Sync API"), self.tr("加载中，请稍后..."), self
            )
            self.getMCSLSyncStateToolTip.move(self.getMCSLSyncStateToolTip.getSuitablePos())
            self.getMCSLSyncStateToolTip.show()
            workThread.start()
            self.refreshMCSLSyncBtn.setEnabled(False)

    @pyqtSlot(dict)
    def updateMCSLSyncCoreList(self, _coreListDict: dict):
        """更新MCSL-Sync核心列表"""
        downloadVariables.MCSLSyncCoreList = _coreListDict.get("cores", [])
        if downloadVariables.MCSLSyncCoreList:
            self.getMCSLSyncStateToolTip.setContent(self.tr("请求 MCSL-Sync API 完毕！"))
            self.getMCSLSyncStateToolTip.setState(True)
            self.getMCSLSyncStateToolTip = None
            self.initMCSLSyncCoreListWidget()
        else:
            self.getMCSLSyncStateToolTip.setContent(self.tr("请求 MCSL-Sync API 失败！"))
            self.getMCSLSyncStateToolTip.setState(True)
            self.getMCSLSyncStateToolTip = None
            self.showMCSLSyncFailedTip()
        self.refreshMCSLSyncBtn.setEnabled(True)

    def showMCSLSyncFailedTip(self):
        """显示MCSL-Sync API失败提示"""
        InfoBar.error(
            title=self.tr("错误"),
            content=self.tr("获取 MCSL-Sync API 失败！\n尝试检查网络后，请再尝试刷新。"),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self,
        )

    def initMCSLSyncCoreListWidget(self):
        """初始化MCSL-Sync核心列表"""
        self.releaseMCSLSyncMemory()
        self.releaseMCSLSyncMemory(1)
        self.releaseMCSLSyncMemory(2)
        self.mcsLSyncCoreBtnGroup.deleteLater()
        self.mcsLSyncCoreBtnGroup = QButtonGroup(self)

        for core_name in downloadVariables.MCSLSyncCoreList:
            widget = MCSLSyncCorePushButton(
                core_name=core_name,
                slot=self.mcsLSyncCoreProcessor,
                parent=self,
            )
            self.mcsLSyncCoreListLayout.addWidget(widget)
            self.mcsLSyncCoreBtnGroup.addButton(widget)
        self.mcsLSyncCoreListLayout.addSpacerItem(self.scrollAreaSpacer)

    def mcsLSyncCoreProcessor(self):
        """处理MCSL-Sync核心选择"""
        downloadVariables.MCSLSyncSelectedCore = self.sender().property("core_name")
        self.getMCSLSyncCoreVersions(downloadVariables.MCSLSyncSelectedCore)
        # 清空构建列表
        self.releaseMCSLSyncMemory(2)

    def getMCSLSyncCoreVersions(self, core_type):
        """获取MCSL-Sync核心版本列表"""
        workThread = self.fetchMCSLSyncCoreVersionsThreadFactory.create(
            core_type=core_type,
            _singleton=True,
            finishSlot=self.updateMCSLSyncCoreVersions,
        )
        if workThread.isRunning():
            return
        else:
            self.getMCSLSyncVersionsStateToolTip = StateToolTip(
                self.tr("正在进一步请求 MCSL-Sync API"),
                self.tr("加载中，请稍后..."),
                self,
            )
            self.getMCSLSyncVersionsStateToolTip.move(
                self.getMCSLSyncVersionsStateToolTip.getSuitablePos()
            )
            self.getMCSLSyncVersionsStateToolTip.show()
            workThread.start()

    @pyqtSlot(dict)
    def updateMCSLSyncCoreVersions(self, _versionsDict: dict):
        """更新MCSL-Sync核心版本列表"""
        downloadVariables.MCSLSyncCoreVersions = _versionsDict
        if downloadVariables.MCSLSyncCoreVersions.get("versions"):
            self.getMCSLSyncVersionsStateToolTip.setContent(self.tr("请求 MCSL-Sync API 完毕！"))
            self.getMCSLSyncVersionsStateToolTip.setState(True)
            self.getMCSLSyncVersionsStateToolTip = None
            self.initMCSLSyncVersionListWidget()
        else:
            self.getMCSLSyncVersionsStateToolTip.setContent(self.tr("请求 MCSL-Sync API 失败！"))
            self.getMCSLSyncVersionsStateToolTip.setState(True)
            self.getMCSLSyncVersionsStateToolTip = None

    def initMCSLSyncVersionListWidget(self):
        """初始化MCSL-Sync版本列表"""
        self.releaseMCSLSyncMemory(1)
        self.releaseMCSLSyncMemory(2)
        self.mcsLSyncVersionBtnGroup.deleteLater()
        self.mcsLSyncVersionBtnGroup = QButtonGroup(self)

        versions = downloadVariables.MCSLSyncCoreVersions.get("versions", [])
        for version in versions:
            widget = MCSLSyncVersionButton(
                version=version,
                slot=self.mcsLSyncVersionProcessor,
                parent=self,
            )
            self.mcsLSyncVersionLayout.addWidget(widget)
            self.mcsLSyncVersionBtnGroup.addButton(widget)
        self.mcsLSyncVersionLayout.addSpacerItem(self.scrollAreaSpacer)

    def mcsLSyncVersionProcessor(self):
        """处理MCSL-Sync版本选择"""
        downloadVariables.MCSLSyncSelectedVersion = self.sender().property("version")
        self.getMCSLSyncCoreBuilds(
            downloadVariables.MCSLSyncSelectedCore, downloadVariables.MCSLSyncSelectedVersion
        )

    def getMCSLSyncCoreBuilds(self, core_type, mc_version):
        """获取MCSL-Sync核心构建列表"""
        # 检查参数有效性
        if not core_type or not mc_version:
            InfoBar.warning(
                title=self.tr("参数错误"),
                content=self.tr("核心类型或版本信息无效"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            return

        # 请求前先清空当前构建列表，保持 UI 与 FastMirror 行为一致
        self.releaseMCSLSyncMemory(2)

        workThread = self.fetchMCSLSyncCoreBuildsThreadFactory.create(
            core_type=core_type,
            mc_version=mc_version,
            _singleton=True,
            finishSlot=self.updateMCSLSyncCoreBuilds,
        )

        if workThread.isRunning():
            InfoBar.info(
                title=self.tr("请稍等"),
                content=self.tr("正在获取构建列表，请稍后..."),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )
            return

        # 显示加载状态
        self.getMCSLSyncBuildsStateToolTip = StateToolTip(
            self.tr("正在获取构建列表"),
            self.tr("正在从 MCSL-Sync API 获取数据..."),
            self,
        )
        self.getMCSLSyncBuildsStateToolTip.move(self.getMCSLSyncBuildsStateToolTip.getSuitablePos())
        self.getMCSLSyncBuildsStateToolTip.show()

        # 跟踪线程
        self.active_threads.append(workThread)
        workThread.finished.connect(self._handleMCSLSyncBuildThreadFinished)

        # 禁用刷新按钮，待请求完成后再恢复
        self.refreshMCSLSyncBtn.setEnabled(False)

        workThread.start()

    @pyqtSlot(dict)
    def updateMCSLSyncCoreBuilds(self, _buildsDict: dict):
        """更新MCSL-Sync核心构建列表"""
        downloadVariables.MCSLSyncCoreBuilds = _buildsDict
        if downloadVariables.MCSLSyncCoreBuilds.get("builds"):
            self.getMCSLSyncBuildsStateToolTip.setContent(self.tr("请求 MCSL-Sync API 完毕！"))
            self.getMCSLSyncBuildsStateToolTip.setState(True)
            self.getMCSLSyncBuildsStateToolTip = None
            self.initMCSLSyncBuildListWidget()
        else:
            self.getMCSLSyncBuildsStateToolTip.setContent(self.tr("请求 MCSL-Sync API 失败！"))
            self.getMCSLSyncBuildsStateToolTip.setState(True)
            self.getMCSLSyncBuildsStateToolTip = None

        # 请求完成后恢复刷新按钮
        self.refreshMCSLSyncBtn.setEnabled(True)

    def initMCSLSyncBuildListWidget(self):
        """初始化MCSL-Sync构建列表"""
        self.releaseMCSLSyncMemory(2)

        builds = downloadVariables.MCSLSyncCoreBuilds.get("builds", [])

        if not builds:
            self._showMCSLSyncNoBuildMessage()
            return

        # 使用 FastMirrorBuildListWidget 构建列表项
        for idx, build_response in enumerate(builds):
            build_info = {}

            if isinstance(build_response, dict):
                build_info = build_response.get("build", {}) if isinstance(
                    build_response.get("build", {}), dict
                ) else build_response
                core_version = (
                    build_info.get("version")
                    or build_info.get("core_version")
                    or build_response.get("build")
                    or build_response.get("core_version")
                    or "未知版本"
                )
            else:
                core_version = str(build_response)

            selected_core = downloadVariables.MCSLSyncSelectedCore
            selected_version = downloadVariables.MCSLSyncSelectedVersion
            cache_key = None
            if selected_core and selected_version and core_version:
                cache_key = (selected_core, selected_version, core_version)
            cached_detail = (
                downloadVariables.MCSLSyncBuildDetailsCache.get(cache_key, {})
                if cache_key
                else {}
            )
            cached_download_url = (
                cached_detail.get("download_url") if isinstance(cached_detail, dict) else ""
            )
            if not isinstance(cached_download_url, str):
                cached_download_url = ""
            else:
                cached_download_url = cached_download_url.strip()

            widget = FastMirrorBuildListWidget(
                buildVer=core_version,
                syncTime="",
                coreVersion=core_version,
                btnSlot=self.downloadMCSLSyncFile,
                parent=self,
            )

            # 为下载按钮附加必要的属性
            widget.downloadBtn.setProperty("download_url", cached_download_url)
            widget.downloadBtn.setProperty("build_name", core_version)
            widget.downloadBtn.setProperty("build_info", build_info)
            widget.downloadBtn.setProperty("build_index", idx)
            widget.syncTimeLabel.setParent(None)

            self.mcsLSyncBuildLayout.addWidget(widget)

        # 添加底部间隔器
        self.mcsLSyncBuildLayout.addSpacerItem(self.scrollAreaSpacer)

    def _handleMCSLSyncBuildThreadFinished(self):
        """在构建线程完成时进行清理，避免访问已删除的对象"""
        thread = self.sender()
        if thread is None or sip.isdeleted(thread):
            return
        self._cleanupFinishedThread(thread)

    def _cleanupFinishedThread(self, thread):
        """清理已完成的线程"""
        try:
            if sip.isdeleted(thread):
                return
            if thread in self.active_threads:
                self.active_threads.remove(thread)
            thread.deleteLater()
        except (ValueError, RuntimeError):
            # 线程可能已经被移除或删除
            pass

    def _showMCSLSyncNoBuildMessage(self):
        """显示无构建信息的提示"""
        from qfluentwidgets import InfoBar, InfoBarPosition

        InfoBar.warning(
            title=self.tr("无构建信息"),
            content=self.tr("该版本暂无可用构建"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self,
        )

    def downloadMCSLSyncFile(self):
        """下载MCSL-Sync文件"""
        button = self.sender()
        if button is None or sip.isdeleted(button):
            return

        build_name = button.property("build_name") or button.property("core_version")
        if not self._validateMCSLSyncDownloadParams(build_name):
            return

        core_name = downloadVariables.MCSLSyncSelectedCore
        mc_version = downloadVariables.MCSLSyncSelectedVersion
        cache_key = (
            (core_name, mc_version, build_name)
            if core_name and mc_version and build_name
            else None
        )
        cached_detail = (
            downloadVariables.MCSLSyncBuildDetailsCache.get(cache_key, {})
            if cache_key
            else {}
        )
        cached_url = cached_detail.get("download_url") if isinstance(cached_detail, dict) else ""

        if isinstance(cached_url, str) and cached_url:
            sanitized_cached_url = cached_url
            button.setProperty("download_url", sanitized_cached_url)
            self._startMCSLSyncFileDownload(sanitized_cached_url, button)
            return

        raw_download_url = button.property("download_url")
        download_url = (
            raw_download_url.strip()
            if isinstance(raw_download_url, str) and raw_download_url.strip()
            else None
        )

        if download_url:
            self._startMCSLSyncFileDownload(download_url, button)
            return

        self._setMCSLSyncBuildFetchingState(button)

        detail_thread = self.fetchMCSLSyncBuildDetailsThreadFactory.create(
            core_type=downloadVariables.MCSLSyncSelectedCore,
            mc_version=downloadVariables.MCSLSyncSelectedVersion,
            core_version=build_name,
            finishSlot=lambda data, btn=button: self._onMCSLSyncBuildDetailsFetched(data, btn),
        )

        self.active_threads.append(detail_thread)
        detail_thread.finished.connect(self._handleMCSLSyncBuildThreadFinished)
        detail_thread.start()

        InfoBar.info(
            title=self.tr("请稍候"),
            content=self.tr("正在获取下载链接..."),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self,
        )

    def _setMCSLSyncBuildFetchingState(self, button):
        """在获取下载链接时更新界面状态"""
        if button is None or sip.isdeleted(button):
            return

        button.setEnabled(False)

    def _validateMCSLSyncDownloadParams(self, build_name, download_url=None):
        """验证下载参数"""
        if not build_name or not str(build_name).strip():
            InfoBar.error(
                title=self.tr("下载错误"),
                content=self.tr("构建名称无效！"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            return False

        if download_url is not None:
            if not isinstance(download_url, str) or not download_url.strip():
                InfoBar.error(
                    title=self.tr("下载错误"),
                    content=self.tr("下载链接无效！"),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
                return False

        if (
            not downloadVariables.MCSLSyncSelectedCore
            or not downloadVariables.MCSLSyncSelectedVersion
        ):
            InfoBar.error(
                title=self.tr("下载错误"),
                content=self.tr("请先选择核心类型和版本！"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            return False

        return True

    def _onMCSLSyncBuildDetailsFetched(self, details: dict, button):
        """处理构建详情请求结果"""
        if button is None or sip.isdeleted(button):
            return

        button.setEnabled(True)

        build_name = button.property("build_name") or button.property("core_version")

        if isinstance(details, dict) and isinstance(details.get("build"), dict):
            build_data = details.get("build", {})
        elif isinstance(details, dict):
            build_data = details
        else:
            build_data = {}

        download_url = build_data.get("download_url", "")

        core_name = build_data.get("core_type") or downloadVariables.MCSLSyncSelectedCore
        mc_version = build_data.get("mc_version") or downloadVariables.MCSLSyncSelectedVersion
        build_version = build_data.get("core_version") or build_name

        sanitized_url = download_url.strip() if isinstance(download_url, str) else ""

        if core_name and mc_version and build_version:
            cache_key = (core_name, mc_version, build_version)
            if isinstance(build_data, dict):
                cache_payload = dict(build_data)
            else:
                cache_payload = {"core_version": build_version}
            if sanitized_url:
                cache_payload["download_url"] = sanitized_url
            elif "download_url" in cache_payload:
                cache_payload.pop("download_url")
            downloadVariables.MCSLSyncBuildDetailsCache[cache_key] = cache_payload

        if sanitized_url:
            button.setProperty("download_url", sanitized_url)
            self._startMCSLSyncFileDownload(sanitized_url, button)
        else:
            button.setProperty("download_url", "")
            self._handleMCSLSyncDownloadError(
                button, self.tr("未能从 MCSL-Sync API 获取到下载链接，请稍后重试。")
            )

    def _handleMCSLSyncDownloadError(self, button, message):
        """处理下载错误并恢复界面"""
        InfoBar.error(
            title=self.tr("下载错误"),
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self,
        )

        if button and not sip.isdeleted(button):
            button.setEnabled(True)
            self._updateMCSLSyncDownloadButtonState(button, "available")

    def _startMCSLSyncFileDownload(self, download_url: str, button):
        """使用获取的下载链接启动下载"""
        if button is None or sip.isdeleted(button):
            return

        build_name = button.property("build_name") or button.property("core_version")
        if not self._validateMCSLSyncDownloadParams(build_name, download_url):
            button.setEnabled(True)
            return

        core_name = downloadVariables.MCSLSyncSelectedCore
        mc_version = downloadVariables.MCSLSyncSelectedVersion
        file_name = f"{core_name}-{mc_version}-{build_name}"
        file_format = "jar"

        button.setProperty("download_url", download_url)

        self.checkDownloadFileExists(
            file_name,
            file_format,
            download_url,
            (
                f"{file_name}.jar",
                core_name,
                mc_version,
                build_name,
                "",
                "",
            ),
        )

        self._updateMCSLSyncDownloadButtonState(button, "downloading")
        button.setEnabled(False)

        file_info = self._prepareMCSLSyncDownloadInfo(build_name)

        self._startMCSLSyncDownload(download_url, file_info, button)

    def _updateMCSLSyncDownloadButtonState(self, button, state):
        """更新下载按钮状态"""
        try:
            # 找到对应的Widget并更新状态
            widget = button.parent()
            if hasattr(widget, "setDownloadStatus"):
                widget.setDownloadStatus(state)
        except Exception as e:
            print(f"Failed to update button state: {e}")

    def _prepareMCSLSyncDownloadInfo(self, build_name):
        """准备下载信息"""
        core_name = downloadVariables.MCSLSyncSelectedCore
        mc_version = downloadVariables.MCSLSyncSelectedVersion

        # 生成更友好的文件名
        fileName = f"{core_name}-{mc_version}-{build_name}"
        fileFormat = "jar"

        return {
            "fileName": fileName,
            "fileFormat": fileFormat,
            "fullFileName": f"{fileName}.{fileFormat}",
            "metadata": (
                f"{fileName}.{fileFormat}",
                core_name,
                mc_version,
                build_name,
            ),
        }

    def _startMCSLSyncDownload(self, download_url, file_info, sender_button):
        """开始MCSL-Sync文件下载"""
        try:
            # 显示下载开始提示
            InfoBar.success(
                title=self.tr("开始下载"),
                content=self.tr(f"正在下载 {file_info['fullFileName']}"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )
        except Exception as e:
            print(f"Error starting download: {e}")

    def refreshMCSLSyncData(self):
        """刷新MCSL-Sync数据"""
        # 如果已经选择了核心和版本，刷新构建列表
        if downloadVariables.MCSLSyncSelectedCore and downloadVariables.MCSLSyncSelectedVersion:
            self.getMCSLSyncCoreBuilds(
                downloadVariables.MCSLSyncSelectedCore, downloadVariables.MCSLSyncSelectedVersion
            )
        else:
            # 否则刷新核心列表
            self.getMCSLSync()

    ##############
    # Polars API #
    ##############

    def releasePolarsAPIMemory(self, id=0):
        layout = self.polarsTypeLayout if not id else self.polarsCoreLayout
        if layout == self.polarsCoreLayout:
            try:
                layout.removeItem(self.scrollAreaSpacer)
            except AttributeError:
                pass
        for i in reversed(range(layout.count())):
            try:
                layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass
            try:
                layout.itemAt(i).widget().deleteLater()
                del layout.itemAt(i).widget
            except AttributeError:
                pass

    def getPolarsAPI(self):
        """请求Polars API"""
        workThread = self.fetchPolarsAPITypeThreadFactory.create(
            _singleton=True, finishSlot=self.updatePolarsAPIDict
        )
        if workThread.isRunning():
            self.refreshPolarsAPIBtn.setEnabled(False)
            return
        else:
            self.getPolarsStateToolTip = StateToolTip(
                self.tr("正在请求 极星镜像 API"), self.tr("加载中，请稍后..."), self
            )
            self.getPolarsStateToolTip.move(self.getPolarsStateToolTip.getSuitablePos())
            self.getPolarsStateToolTip.show()
            workThread.start()
            self.refreshPolarsAPIBtn.setEnabled(False)

    @pyqtSlot(dict)
    def updatePolarsAPIDict(self, _APIDict: dict):
        """更新Polars API"""
        downloadVariables.PolarTypeDict.clear()
        downloadVariables.PolarTypeDict.update(_APIDict)
        if downloadVariables.PolarTypeDict["name"] != -1:
            self.getPolarsStateToolTip.setContent(self.tr("请求 极星镜像 API 完毕！"))
            self.getPolarsStateToolTip.setState(True)
            self.getPolarsStateToolTip = None
            self.initPolarsTypeListWidget()
        else:
            self.getPolarsStateToolTip.setContent(self.tr("请求 极星镜像 API 失败！"))
            self.getPolarsStateToolTip.setState(True)
            self.getPolarsStateToolTip = None
            self.showPolarsAPIFailedTip()
        self.refreshPolarsAPIBtn.setEnabled(True)

    def showPolarsAPIFailedTip(self):
        InfoBar.error(
            title=self.tr("错误"),
            content=self.tr("获取 极星镜像 API 失败！\n尝试检查网络后，请再尝试刷新。"),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self,
        )

    def initPolarsTypeListWidget(self):
        self.releasePolarsAPIMemory()
        self.polarsBtnGroup.deleteLater()
        self.polarsBtnGroup = QButtonGroup(self)
        for i in range(len(downloadVariables.PolarTypeDict["name"])):
            k = PolarsTypeWidget(
                name=downloadVariables.PolarTypeDict["name"][i],
                idx=downloadVariables.PolarTypeDict["id"][i],
                description=downloadVariables.PolarTypeDict["description"][i],
                slot=self.polarsTypeProcessor,
                parent=self,
            )
            self.polarsTypeLayout.addWidget(k)
            self.polarsBtnGroup.addButton(k)

    def polarsTypeProcessor(self):
        self.polarsTypeLabel.setText(self.sender().property("name"))
        self.polarsDescriptionLabel.setText(self.sender().property("description"))
        self.getPolarsCoreAPI(idx=self.sender().property("id"))

    def getPolarsCoreAPI(self, idx):
        workThread = self.fetchPolarsAPICoreThreadFactory.create(
            _singleton=True, idx=idx, finishSlot=self.updatePolarsAPICoreDict
        )
        if workThread.isRunning():
            self.refreshPolarsAPIBtn.setEnabled(False)
            return
        else:
            self.getPolarsCoreStateToolTip = StateToolTip(
                self.tr("正在进一步请求 极星镜像 API"),
                self.tr("加载中，请稍后..."),
                self,
            )
            self.getPolarsCoreStateToolTip.move(self.getPolarsCoreStateToolTip.getSuitablePos())
            self.getPolarsCoreStateToolTip.show()
            workThread.start()
            self.refreshPolarsAPIBtn.setEnabled(False)

    @pyqtSlot(dict)
    def updatePolarsAPICoreDict(self, _APIDict: dict):
        downloadVariables.PolarCoreDict.clear()
        downloadVariables.PolarCoreDict.update(_APIDict)
        if downloadVariables.PolarCoreDict["name"] != -1:
            self.getPolarsCoreStateToolTip.setContent(self.tr("请求 极星镜像 API 完毕！"))
            self.getPolarsCoreStateToolTip.setState(True)
            self.getPolarsCoreStateToolTip = None
            self.initPolarsCoreListWidget()
        else:
            self.getPolarsCoreStateToolTip.setContent(self.tr("请求 极星镜像 API 失败！"))
            self.getPolarsCoreStateToolTip.setState(True)
            self.getPolarsCoreStateToolTip = None
            self.showPolarsAPIFailedTip()
        self.refreshPolarsAPIBtn.setEnabled(True)

    def initPolarsCoreListWidget(self):
        self.releasePolarsAPIMemory(1)
        for i in range(len(downloadVariables.PolarCoreDict["name"])):
            self.polarsCoreLayout.addWidget(
                FastMirrorBuildListWidget(
                    buildVer=downloadVariables.PolarCoreDict["name"][i],
                    syncTime=downloadVariables.PolarCoreDict["downloadUrl"][i],
                    coreVersion=downloadVariables.PolarCoreDict["downloadUrl"][i],
                    btnSlot=self.downloadPolarsAPIFile,
                    parent=self,
                )
            )
        self.polarsCoreLayout.addItem(self.scrollAreaSpacer)

    def downloadPolarsAPIFile(self):
        """下载极星镜像API文件"""
        # 多线程下载引擎总是可用，直接开始下载
        uri = self.sender().property("core_version")
        fileFormat = self.sender().parent().buildVerLabel.text().split(".")[-1]
        fileName = self.sender().parent().buildVerLabel.text().replace("." + fileFormat, "")
        # 判断文件是否存在
        self.checkDownloadFileExists(
            fileName,
            fileFormat,
            uri,
            (fileName + "." + fileFormat, "coreName", "MCVer", "buildVer"),
        )

    ##################
    # FastMirror API #
    ##################

    def releaseFMMemory(self, id=0):
        if not id:
            self.coreListLayout.removeItem(self.scrollAreaSpacer)
            for i in reversed(range(self.coreListLayout.count())):
                try:
                    self.coreListLayout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    self.coreListLayout.itemAt(i).widget().deleteLater()
                    del self.coreListLayout.itemAt(i).widget
                except AttributeError:
                    pass
        elif id == 1:
            self.versionLayout.removeItem(self.scrollAreaSpacer)
            for i in reversed(range(self.versionLayout.count())):
                try:
                    self.versionLayout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    self.versionLayout.itemAt(i).widget().deleteLater()
                    del self.versionLayout.itemAt(i).widget
                except AttributeError:
                    pass
        elif id == 2:
            self.buildLayout.removeItem(self.scrollAreaSpacer)
            for i in reversed(range(self.buildLayout.count())):
                try:
                    self.buildLayout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    self.buildLayout.itemAt(i).widget().deleteLater()
                    del self.buildLayout.itemAt(i).widget
                except AttributeError:
                    pass
        else:
            pass

    def getFastMirrorAPI(self):
        """请求FastMirror API"""
        self.releasePolarsAPIMemory()
        self.releasePolarsAPIMemory(1)
        workThread = self.fetchFMAPIThreadFactory.create(
            _singleton=True, finishSlot=self.updateFastMirrorAPIDict
        )
        if workThread.isRunning():
            self.refreshFastMirrorAPIBtn.setEnabled(False)
            return
        else:
            self.getFastMirrorStateToolTip = StateToolTip(
                self.tr("正在请求 FastMirror API"), self.tr("加载中，请稍后..."), self
            )
            self.getFastMirrorStateToolTip.move(self.getFastMirrorStateToolTip.getSuitablePos())
            self.getFastMirrorStateToolTip.show()
            workThread.start()
            self.refreshFastMirrorAPIBtn.setEnabled(False)

    def getFastMirrorAPICoreVersion(self, name, mcVersion):
        """请求FastMirror API 核心的版本"""
        workThread = self.fetchFMAPICoreVersionThreadFactory.create(
            name=name,
            mcVersion=mcVersion,
            _singleton=True,
            finishSlot=self.updateFastMirrorAPICoreVersionDict,
        )
        if workThread.isRunning():
            return
        else:
            self.getFastMirrorStateToolTip = StateToolTip(
                self.tr("正在进一步请求 FastMirror API"),
                self.tr("加载中，请稍后..."),
                self,
            )
            self.getFastMirrorStateToolTip.move(self.getFastMirrorStateToolTip.getSuitablePos())
            self.getFastMirrorStateToolTip.show()
            workThread.start()

    @pyqtSlot(dict)
    def updateFastMirrorAPIDict(self, _APIDict: dict):
        """更新获取FastMirrorAPI结果"""
        downloadVariables.FastMirrorAPIDict.clear()
        downloadVariables.FastMirrorAPIDict.update(_APIDict)
        if downloadVariables.FastMirrorAPIDict["name"] != -1:
            self.getFastMirrorStateToolTip.setContent(self.tr("请求 FastMirror API 完毕！"))
            self.getFastMirrorStateToolTip.setState(True)
            self.getFastMirrorStateToolTip = None
            self.initFastMirrorCoreListWidget()
        else:
            self.getFastMirrorStateToolTip.setContent(self.tr("请求FastMirror API失败！"))
            self.getFastMirrorStateToolTip.setState(True)
            self.getFastMirrorStateToolTip = None
            self.showFastMirrorFailedTip()
        self.refreshFastMirrorAPIBtn.setEnabled(True)

    @pyqtSlot(dict)
    def updateFastMirrorAPICoreVersionDict(self, _APICoreVersionDict: dict):
        """更新获取FastMirrorAPI结果"""
        downloadVariables.FastMirrorAPICoreVersionDict.clear()
        downloadVariables.FastMirrorAPICoreVersionDict.update(_APICoreVersionDict)
        if downloadVariables.FastMirrorAPICoreVersionDict["name"] != -1:
            self.getFastMirrorStateToolTip.setContent(self.tr("请求 FastMirror API 完毕！"))
            self.getFastMirrorStateToolTip.setState(True)
            self.getFastMirrorStateToolTip = None
            self.initFastMirrorCoreVersionListWidget()
        else:
            self.getFastMirrorStateToolTip.setContent(self.tr("请求 FastMirror API 失败！"))
            self.getFastMirrorStateToolTip.setState(True)
            self.getFastMirrorStateToolTip = None

    def showFastMirrorFailedTip(self):
        i = InfoBar.error(
            title=self.tr("错误"),
            content=self.tr(
                "获取 FastMirror API 失败！\n \
                    尝试检查网络后，请再尝试刷新。\n \
                        或者，点击旁边的按钮看看你是不是暂时达到请求限制了。"
            ),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self,
        )
        errTestBtn = HyperlinkButton("https://download.fastmirror.net/api/v3", "测试", i, FIF.LINK)
        i.addWidget(errTestBtn)

    def initFastMirrorCoreListWidget(self):
        """FastMirror核心列表"""
        self.releaseFMMemory()
        self.releaseFMMemory(1)
        self.releaseFMMemory(2)
        self.fmBtnGroup.deleteLater()
        self.fmBtnGroup = QButtonGroup(self)
        for i in range(len(downloadVariables.FastMirrorAPIDict["name"])):
            k = FastMirrorCorePushButton(
                tag=downloadVariables.FastMirrorReplaceTagDict[
                    downloadVariables.FastMirrorAPIDict["tag"][i]
                ],
                name=downloadVariables.FastMirrorAPIDict["name"][i],
                slot=self.fastMirrorCoreNameProcessor,
                parent=self,
            )
            self.coreListLayout.addWidget(k)
            self.fmBtnGroup.addButton(k)
        self.coreListLayout.addSpacerItem(self.scrollAreaSpacer)

    def fastMirrorCoreNameProcessor(self):
        downloadVariables.selectedName = self.sender().property("name")
        self.initFastMirrorMCVersionsListWidget()
        try:
            self.buildLayout.removeItem(self.scrollAreaSpacer)
        except AttributeError:
            pass
        try:
            for i in reversed(range(self.buildLayout.count())):
                self.buildLayout.itemAt(i).widget().setParent(None)
                self.buildLayout.itemAt(i).widget().deleteLater()
                del self.buildLayout.itemAt(i).widget
        except AttributeError:
            pass

    def initFastMirrorMCVersionsListWidget(self):
        self.releaseFMMemory(1)
        self.releaseFMMemory(2)
        MCVersionList = downloadVariables.FastMirrorAPIDict["mc_versions"][
            list(downloadVariables.FastMirrorAPIDict["name"]).index(downloadVariables.selectedName)
        ]
        self.fmVersionBtnGroup.deleteLater()
        self.fmVersionBtnGroup = QButtonGroup(self)
        for i in range(len(MCVersionList)):
            MCVersion = MCVersionList[i]
            k = FastMirrorVersionButton(
                version=MCVersion,
                slot=self.fastMirrorMCVersionProcessor,
                parent=self,
            )
            self.versionLayout.addWidget(k)
            self.fmVersionBtnGroup.addButton(k)
        self.versionLayout.addSpacerItem(self.scrollAreaSpacer)

    def fastMirrorMCVersionProcessor(self):
        downloadVariables.selectedMCVersion = self.sender().property("version")
        self.getFastMirrorAPICoreVersion(
            name=downloadVariables.selectedName,
            mcVersion=downloadVariables.selectedMCVersion,
        )

    def initFastMirrorCoreVersionListWidget(self):
        self.releaseFMMemory(2)
        for i in range(len(downloadVariables.FastMirrorAPICoreVersionDict["name"])):
            self.buildLayout.addWidget(
                FastMirrorBuildListWidget(
                    buildVer=downloadVariables.FastMirrorAPICoreVersionDict["core_version"][i],
                    syncTime=downloadVariables.FastMirrorAPICoreVersionDict["update_time"][
                        i
                    ].replace("T", " "),
                    coreVersion=downloadVariables.FastMirrorAPICoreVersionDict["core_version"][i],
                    btnSlot=self.downloadFastMirrorAPIFile,
                    parent=self,
                )
            )
        self.buildLayout.addSpacerItem(self.scrollAreaSpacer)

    def downloadFastMirrorAPIFile(self):
        """下载FastMirror API文件"""
        # 多线程下载引擎总是可用，直接开始下载
        buildVer = self.sender().property("core_version")
        fileName = (
            f"{downloadVariables.selectedName}-{downloadVariables.selectedMCVersion}-{buildVer}"
        )
        fileFormat = "jar"
        uri = f"https://download.fastmirror.net/download/{downloadVariables.selectedName}/{downloadVariables.selectedMCVersion}/{buildVer}"
        # 判断文件是否存在
        self.checkDownloadFileExists(
            fileName,
            fileFormat,
            uri,
            (
                f"{fileName}.jar",
                downloadVariables.selectedName,
                downloadVariables.selectedMCVersion,
                buildVer,
            ),
        )

    def downloadCustomURLFile(self):
        """下载自定义URL文件"""
        # 多线程下载引擎总是可用，直接开始下载
        urlLineEdit = LineEdit()
        urlLineEdit.setPlaceholderText(self.tr("URL"))
        w = MessageBox(
            self.tr("创建下载任务"),
            self.tr(
                "使用 MCSL2 自带的多线程高速下载引擎下载文件。\n请注意，部分网站可能会禁止 (403)，无法正常下载。"  # noqa: E501
            ),
            self,
        )
        w.textLayout.addWidget(urlLineEdit)
        w.yesButton.setText(self.tr("下载"))
        w.yesSignal.connect(
            lambda: self.checkDownloadFileExists(
                fileName := urlLineEdit.text().replace("\\", "/").split("/")[-1].split(".")[0],
                fileFormat := urlLineEdit.text()
                .replace("\\", "/")
                .split("/")[-1]
                .replace(fileName, "")
                .replace(".", ""),
                urlLineEdit.text(),
                (fileName + "." + fileFormat, "custom", "custom", "custom"),
            )
        )
        w.show()

    def checkDownloadFileExists(self, fileName, fileFormat, uri, extraData: tuple) -> bool:
        if osp.exists(osp.join("MCSL2", "Downloads", f"{fileName}.{fileFormat}")):
            if cfg.get(cfg.saveSameFileException) == "ask":
                w = MessageBox(self.tr("提示"), self.tr("您要下载的文件已存在。请选择操作。"), self)
                w.yesButton.setText(self.tr("停止下载"))
                w.cancelButton.setText(self.tr("覆盖文件"))
                w.cancelSignal.connect(lambda: remove(f"MCSL2/Downloads/{fileName}.{fileFormat}"))
                w.cancelSignal.connect(
                    lambda: self.downloadFile(fileName, fileFormat, uri, extraData)
                )
                w.exec()
            elif cfg.get(cfg.saveSameFileException) == "overwrite":
                InfoBar.warning(
                    title=self.tr("警告"),
                    content=self.tr(
                        "MCSL2/Downloads 文件夹存在同名文件。\n根据设置，已删除原文件并继续下载。"
                    ),
                    orient=Qt.Horizontal,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                    duration=2222,
                    parent=self,
                )
                remove(f"MCSL2/Downloads/{fileName}.{fileFormat}")
                self.downloadFile(fileName, fileFormat, uri, extraData)
            elif cfg.get(cfg.saveSameFileException) == "stop":
                InfoBar.warning(
                    title=self.tr("警告"),
                    content=self.tr("MCSL2/Downloads 文件夹存在同名文件。\n根据设置，已停止下载。"),
                    orient=Qt.Horizontal,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                    duration=2222,
                    parent=self,
                )
        else:
            self.downloadFile(fileName, fileFormat, uri, extraData)

    def downloadFile(self, fileName, fileFormat, uri, extraData: tuple):
        InfoBar.info(
            title=self.tr("开始下载"),
            content=self.tr("{fileName}.{fileFormat}").format(
                fileName=fileName, fileFormat=fileFormat
            ),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=1500,
            parent=self,
        )
        downloadingInfoWidget = DownloadCard(
            fileName=f"{fileName}.{fileFormat}", url=uri, parent=self
        )

        # 使用多线程下载引擎
        gid = MultiThreadDownloadController.download(
            uri=uri,
            watch=True,
            info_get=downloadingInfoWidget.onInfoGet,
            stopped=downloadingInfoWidget.onDownloadFinished,
            filename=f"{fileName}.{fileFormat}",
            interval=0.2,
            extraData=extraData,
        )

        downloadingInfoWidget.canceled.connect(
            lambda: MultiThreadDownloadController.cancelDownloadTask(gid)
        )
        downloadingInfoWidget.paused.connect(
            lambda x: (
                MultiThreadDownloadController.pauseDownloadTask(gid)
                if x
                else MultiThreadDownloadController.resumeDownloadTask(gid)
            )
        )
        self.downloadingItemLayout.addWidget(downloadingInfoWidget)

    def switchDownloadingItemWidget(self):
        if self.showDownloadingItemBtn.isChecked():
            self.downloadingItemWidget.setFixedWidth(310)
            self.VerticalSeparator.setVisible(True)
            self.showDownloadingItemBtn.setText(self.tr("收起下载中列表"))
        else:
            self.downloadingItemWidget.setFixedWidth(0)
            self.VerticalSeparator.setVisible(False)
            self.showDownloadingItemBtn.setText(self.tr("展开下载中列表"))

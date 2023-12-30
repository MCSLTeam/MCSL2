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
Download page with FastMirror and MCSLAPI.
"""

from os import path as osp, remove

from PyQt5.QtCore import Qt, QSize, QRect, pyqtSlot
from PyQt5.QtGui import QPixmap
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
    BreadcrumbBar,
    HyperlinkButton,
    LineEdit,
    PrimaryPushButton,
)

from MCSL2Lib.Widgets.DownloadEntryViewerWidget import DownloadEntryBox
from MCSL2Lib.Widgets.DownloadProgressWidget import DownloadCard
from MCSL2Lib.DownloadAPIs.FastMirrorAPI import (
    FetchFastMirrorAPIThreadFactory,
    FetchFastMirrorAPICoreVersionThreadFactory,
)
from MCSL2Lib.Widgets.PolarsWidgets import PolarsTypeWidget
from MCSL2Lib.Widgets.FastMirrorWidgets import (
    FastMirrorBuildListWidget,
    FastMirrorCorePushButton,
    FastMirrorVersionButton,
)
from MCSL2Lib.DownloadAPIs.MCSLAPI import FetchMCSLAPIDownloadURLThreadFactory
from MCSL2Lib.DownloadAPIs.PolarsAPI import (
    FetchPolarsAPICoreThreadFactory,
    FetchPolarsAPITypeThreadFactory,
)
from MCSL2Lib.DownloadAPIs.AkiraCloud import (
    FetchAkiraTypeThreadFactory,
    FetchAkiraCoreThreadFactory,
)
from MCSL2Lib.Controllers.aria2ClientController import Aria2Controller
from MCSL2Lib.Controllers.interfaceController import (
    MySmoothScrollArea,
)
from MCSL2Lib.Widgets.loadingTipWidget import (
    MCSLAPILoadingErrorWidget,
    MCSLAPILoadingWidget,
)
from MCSL2Lib.Controllers.settingsController import cfg
from MCSL2Lib.Widgets.singleMCSLAPIDownloadWidget import MCSLAPIDownloadWidget
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

        self.fetchMCSLAPIDownloadURLThreadFactory = FetchMCSLAPIDownloadURLThreadFactory()

        self.fetchPolarsAPITypeThreadFactory = FetchPolarsAPITypeThreadFactory()
        self.fetchPolarsAPICoreThreadFactory = FetchPolarsAPICoreThreadFactory()

        self.fetchAkiraTypeThreadFactory = FetchAkiraTypeThreadFactory()
        self.fetchAkiraCoreThreadFactory = FetchAkiraCoreThreadFactory()
        # fmt: on

        self.fmBtnGroup = QButtonGroup(self)
        self.fmVersionBtnGroup = QButtonGroup(self)
        self.polarsBtnGroup = QButtonGroup(self)
        self.akiraBtnGroup = QButtonGroup(self)

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
            text=self.tr("打开下载文件夹"), parent=self.titleLimitWidget, icon=FIF.FOLDER
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

        self.downloadWithMCSLAPI = QWidget()
        self.downloadWithMCSLAPI.setObjectName("downloadWithMCSLAPI")
        self.gridLayout_3 = QGridLayout(self.downloadWithMCSLAPI)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.refreshMCSLAPIBtn = PushButton(
            icon=FIF.UPDATE, text=self.tr("刷新"), parent=self.downloadWithMCSLAPI
        )
        self.gridLayout_3.addWidget(self.refreshMCSLAPIBtn, 0, 1, 1, 1)
        self.MCSLAPIScrollArea = MySmoothScrollArea(self.downloadWithMCSLAPI)
        self.MCSLAPIScrollArea.setFrameShape(QFrame.NoFrame)
        self.MCSLAPIScrollArea.setWidgetResizable(True)
        self.MCSLAPIScrollArea.setObjectName("MCSLAPIScrollArea")
        self.MCSLAPIScrollAreaWidgetContents = QWidget()
        self.MCSLAPIScrollAreaWidgetContents.setGeometry(QRect(0, 0, 676, 351))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLAPIScrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.MCSLAPIScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.MCSLAPIScrollAreaWidgetContents.setObjectName("MCSLAPIScrollAreaWidgetContents")
        self.verticalLayout_9 = QVBoxLayout(self.MCSLAPIScrollAreaWidgetContents)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.MCSLAPIScrollAreaLayout = QVBoxLayout()
        self.MCSLAPIScrollAreaLayout.setObjectName("MCSLAPIScrollAreaLayout")
        self.verticalLayout_9.addLayout(self.MCSLAPIScrollAreaLayout)
        self.MCSLAPIScrollArea.setWidget(self.MCSLAPIScrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.MCSLAPIScrollArea, 1, 0, 1, 2)
        self.MCSLAPIBreadcrumbBar = BreadcrumbBar(self.downloadWithMCSLAPI)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLAPIBreadcrumbBar.sizePolicy().hasHeightForWidth())
        self.MCSLAPIBreadcrumbBar.setSizePolicy(sizePolicy)
        self.MCSLAPIBreadcrumbBar.setObjectName("MCSLAPIBreadcrumbBar")
        self.gridLayout_3.addWidget(self.MCSLAPIBreadcrumbBar, 0, 0, 1, 1)
        self.downloadStackedWidget.addWidget(self.downloadWithMCSLAPI)

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
        self.downloadWithAkiraCloud = QWidget()
        self.downloadWithAkiraCloud.setObjectName("downloadWithAkiraCloud")

        self.gridLayout_10 = QGridLayout(self.downloadWithAkiraCloud)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.akiraTitle = SubtitleLabel(self.downloadWithAkiraCloud)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.akiraTitle.sizePolicy().hasHeightForWidth())
        self.akiraTitle.setSizePolicy(sizePolicy)
        self.akiraTitle.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.akiraTitle.setObjectName("akiraTitle")

        self.gridLayout_10.addWidget(self.akiraTitle, 0, 0, 1, 1)
        self.VerticalSeparator_3 = VerticalSeparator(self.downloadWithAkiraCloud)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VerticalSeparator_3.sizePolicy().hasHeightForWidth())
        self.VerticalSeparator_3.setSizePolicy(sizePolicy)
        self.VerticalSeparator_3.setMinimumSize(QSize(3, 0))
        self.VerticalSeparator_3.setMaximumSize(QSize(3, 16777215))
        self.VerticalSeparator_3.setObjectName("VerticalSeparator_3")

        self.gridLayout_10.addWidget(self.VerticalSeparator_3, 0, 1, 3, 1)
        self.akiraTypeLabel = SubtitleLabel(self.downloadWithAkiraCloud)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.akiraTypeLabel.sizePolicy().hasHeightForWidth())
        self.akiraTypeLabel.setSizePolicy(sizePolicy)
        self.akiraTypeLabel.setObjectName("akiraTypeLabel")

        self.gridLayout_10.addWidget(self.akiraTypeLabel, 0, 2, 1, 1)
        self.refreshAkiraCloudBtn = PushButton(
            icon=FIF.UPDATE, text=self.tr("刷新"), parent=self.downloadWithAkiraCloud
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshAkiraCloudBtn.sizePolicy().hasHeightForWidth())
        self.refreshAkiraCloudBtn.setSizePolicy(sizePolicy)
        self.refreshAkiraCloudBtn.setObjectName("refreshAkiraCloudBtn")

        self.gridLayout_10.addWidget(self.refreshAkiraCloudBtn, 0, 3, 1, 1)
        self.akiraTypeScrollArea = MySmoothScrollArea(self.downloadWithAkiraCloud)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.akiraTypeScrollArea.sizePolicy().hasHeightForWidth())
        self.akiraTypeScrollArea.setSizePolicy(sizePolicy)
        self.akiraTypeScrollArea.setMinimumSize(QSize(170, 0))
        self.akiraTypeScrollArea.setMaximumSize(QSize(170, 16777215))
        self.akiraTypeScrollArea.setFrameShape(QFrame.NoFrame)
        self.akiraTypeScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.akiraTypeScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.akiraTypeScrollArea.setWidgetResizable(True)
        self.akiraTypeScrollArea.setObjectName("akiraTypeScrollArea")

        self.akiraTypeScrollAreaContents = QWidget()
        self.akiraTypeScrollAreaContents.setGeometry(QRect(0, 0, 170, 351))
        self.akiraTypeScrollAreaContents.setObjectName("akiraTypeScrollAreaContents")

        self.gridLayout_9 = QGridLayout(self.akiraTypeScrollAreaContents)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setObjectName("gridLayout_9")

        self.akiraTypeLayout = QVBoxLayout()
        self.akiraTypeLayout.setObjectName("akiraTypeLayout")

        self.gridLayout_9.addLayout(self.akiraTypeLayout, 0, 0, 1, 1)
        self.akiraTypeScrollArea.setWidget(self.akiraTypeScrollAreaContents)
        self.gridLayout_10.addWidget(self.akiraTypeScrollArea, 1, 0, 2, 1)
        self.akiraCoreScrollArea = MySmoothScrollArea(self.downloadWithAkiraCloud)
        self.akiraCoreScrollArea.setFrameShape(QFrame.NoFrame)
        self.akiraCoreScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.akiraCoreScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.akiraCoreScrollArea.setWidgetResizable(True)
        self.akiraCoreScrollArea.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.akiraCoreScrollArea.setObjectName("akiraCoreScrollArea")

        self.akiraCoreScrollAreaContents = QWidget()
        self.akiraCoreScrollAreaContents.setGeometry(QRect(0, 0, 491, 345))
        self.akiraCoreScrollAreaContents.setObjectName("akiraCoreScrollAreaContents")

        self.gridLayout_8 = QGridLayout(self.akiraCoreScrollAreaContents)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")

        self.akiraCoreLayout = QVBoxLayout()
        self.akiraCoreLayout.setObjectName("akiraCoreLayout")

        self.gridLayout_8.addLayout(self.akiraCoreLayout, 0, 0, 1, 1)
        self.akiraCoreScrollArea.setWidget(self.akiraCoreScrollAreaContents)
        self.gridLayout_10.addWidget(self.akiraCoreScrollArea, 2, 2, 1, 2)
        self.downloadStackedWidget.addWidget(self.downloadWithAkiraCloud)
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
            self.downloadWithMCSLAPI,
            self.downloadWithPolarsAPI,
            self.downloadWithAkiraCloud,
        ]
        self.downloadStackedWidget.setCurrentWidget(
            self.dsList[settingsVariables.downloadSourceList.index(cfg.get(cfg.downloadSource))]
        )

        self.setObjectName("DownloadInterface")

        self.titleLabel.setText(self.tr("下载"))
        self.subTitleLabel.setText(self.tr("Aria2引擎高速驱动！"))
        self.coreListSubtitleLabel.setText(self.tr("核心列表"))
        self.versionSubtitleLabel.setText(self.tr("游戏版本"))
        self.buildSubtitleLabel.setText(self.tr("构建列表"))
        self.refreshFastMirrorAPIBtn.setText(self.tr("刷新"))
        self.polarsTitle.setText("核心类型")
        self.akiraTitle.setText("核心类型")

        self.MCSLAPIBreadcrumbBar.addItem("MCSLAPI", "MCSLAPI")
        self.refreshMCSLAPIBtn.clicked.connect(
            lambda: self.getMCSLAPI(f"/{self.MCSLAPIBreadcrumbBar.currentItem().routeKey}")
        )
        self.refreshPolarsAPIBtn.clicked.connect(self.getPolarsAPI)
        self.refreshFastMirrorAPIBtn.clicked.connect(self.getFastMirrorAPI)
        self.refreshMCSLAPIBtn.setEnabled(False)
        self.scrollAreaSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.createCustomDownloadBtn.clicked.connect(self.downloadCustomURLFile)
        self.openDownloadFolderBtn.clicked.connect(lambda: openLocalFile(".\\MCSL2\\Downloads\\"))
        self.MCSLAPIBreadcrumbBar.currentIndexChanged.connect(self.getMCSLAPI)
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
            self.subTitleLabel.setText(
                self.tr(
                    f"Aria2引擎高速驱动！ - 当前下载源：{settingsVariables.downloadSourceTextList[settingsVariables.downloadSourceList.index(cfg.get(cfg.downloadSource))]}"  # noqa: E501
                )
            )
            self.downloadStackedWidget.setCurrentWidget(
                self.dsList[settingsVariables.downloadSourceList.index(cfg.get(cfg.downloadSource))]
            )
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
        # Akira Cloud
        elif self.downloadStackedWidget.currentIndex() == 3:
            if downloadVariables.AkiraTypeList:
                if len(downloadVariables.AkiraTypeList):
                    self.initAkiraTypeListWidget()
                else:
                    self.showAkiraFailedTip()
            else:
                self.getAkiraInfo()
        # MCSLAPI
        elif self.downloadStackedWidget.currentIndex() == 1:
            # 如果存在列表且不为空,则不再重新获取
            if downloadVariables.MCSLAPIDownloadUrlDict:
                if (
                    str(downloadVariables.MCSLAPIDownloadUrlDict["name"]) != "-2"
                    or str(downloadVariables.MCSLAPIDownloadUrlDict["name"]) != "-1"
                ):
                    self.initMCSLAPIDownloadWidget()
                else:
                    self.showMCSLAPIFailedWidget()
            else:
                self.getMCSLAPI()
                self.refreshMCSLAPIBtn.setEnabled(False)

    ###########
    # MCSLAPI #
    ###########

    def releaseMCSLAPIMemory(self):
        self.MCSLAPIScrollAreaLayout.removeItem(self.scrollAreaSpacer)
        for i in reversed(range(self.MCSLAPIScrollAreaLayout.count())):
            try:
                self.MCSLAPIScrollAreaLayout.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass
            try:
                self.MCSLAPIScrollAreaLayout.itemAt(i).widget().deleteLater()
                del self.MCSLAPIScrollAreaLayout.itemAt(i).widget
            except AttributeError:
                pass

    def getMCSLAPI(self, path: str = ""):
        """请求MCSLAPI"""
        if type(path) is int:
            if path == 0:
                self.refreshMCSLAPIBtn.click()
            return
        if path == "MCSLAPI" or path == "/MCSLAPI":
            path = ""
        workThread = self.fetchMCSLAPIDownloadURLThreadFactory.create(
            _singleton=True, finishSlot=self.updateMCSLAPIDownloadUrlDict, path=path
        )
        if path != "" and type(self.sender()) is not PrimaryPushButton:
            path = path.replace("/", "")
            self.MCSLAPIBreadcrumbBar.addItem(path, path)
        if workThread.isRunning():
            self.refreshMCSLAPIBtn.setEnabled(False)
            return
        else:
            self.releaseMCSLAPIMemory()
            self.MCSLAPIScrollAreaLayout.addWidget(MCSLAPILoadingWidget())
            workThread.start()
            self.refreshMCSLAPIBtn.setEnabled(False)

    @pyqtSlot(dict)
    def updateMCSLAPIDownloadUrlDict(self, _downloadUrlDict: dict):
        """更新获取MCSLAPI结果"""
        downloadVariables.MCSLAPIDownloadUrlDict.update(_downloadUrlDict)
        if (
            str(downloadVariables.MCSLAPIDownloadUrlDict["name"]) != "-2"
            or str(downloadVariables.MCSLAPIDownloadUrlDict["name"]) != "-1"
        ):
            self.initMCSLAPIDownloadWidget()
        else:
            self.showMCSLAPIFailedWidget()

    def showMCSLAPIFailedWidget(self):
        self.releaseMCSLAPIMemory()
        self.MCSLAPIScrollAreaLayout.addWidget(MCSLAPILoadingErrorWidget())
        self.refreshMCSLAPIBtn.setEnabled(True)

    @staticmethod
    def getMCSLAPIDownloadIcon(isDir):
        """设置MCSLAPI源图标"""
        return (
            QPixmap(":/built-InIcons/file.svg")
            if not isDir
            else QPixmap(":/built-InIcons/folder.svg")
        )

    def initMCSLAPIDownloadWidget(self):
        """初始化MCSLAPI模式下的UI"""
        self.releaseMCSLAPIMemory()
        self.refreshMCSLAPIBtn.setEnabled(True)
        downloadDict = downloadVariables.MCSLAPIDownloadUrlDict
        # try:
        for i in range(downloadDict["total"]):
            self.MCSLAPIScrollAreaLayout.addWidget(
                MCSLAPIDownloadWidget(
                    link=f"/{downloadDict['name'][i]}"
                    if downloadDict["is_dir"][i]
                    else f"/{self.MCSLAPIBreadcrumbBar.currentItem().routeKey}",
                    name=f"/{downloadDict['name'][i]}"
                    if not downloadDict["is_dir"][i]
                    else downloadDict["name"][i],
                    size=downloadDict["size"][i] if not downloadDict["is_dir"][i] else "-",
                    pixmap=self.getMCSLAPIDownloadIcon(downloadDict["is_dir"][i]),
                    downloadSlot=self.downloadMCSLAPIFile
                    if not downloadDict["is_dir"][i]
                    else self.getMCSLAPI,
                )
            )
        self.MCSLAPIScrollAreaLayout.addSpacerItem(self.scrollAreaSpacer)
        # except TypeError:
        #     self.showMCSLAPIFailedWidget()

    def downloadMCSLAPIFile(self):
        """下载MCSLAPI文件"""
        if not self.checkAria2Service():
            return
        sender = self.sender()
        uri = sender.property("link")
        print(uri)
        fileFormat = sender.property("name").split(".")[-1]
        fileName = sender.property("name").replace(f".{fileFormat}", "").replace("/", "")
        # 判断文件是否存在
        # TODO 完善MCSLAPI的extraData : "coreName", "MCVer", "buildVer"
        self.checkDownloadFileExists(
            fileName,
            fileFormat,
            uri,
            (fileName + "." + fileFormat, "coreName", "MCVer", "buildVer"),
        )

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
                self.tr("正在请求极星镜像API"), self.tr("加载中，请稍后..."), self
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
            self.getPolarsStateToolTip.setContent(self.tr("请求极星镜像API完毕！"))
            self.getPolarsStateToolTip.setState(True)
            self.getPolarsStateToolTip = None
            self.initPolarsTypeListWidget()
        else:
            self.getPolarsStateToolTip.setContent(self.tr("请求极星镜像API失败！"))
            self.getPolarsStateToolTip.setState(True)
            self.getPolarsStateToolTip = None
            self.showPolarsAPIFailedTip()
        self.refreshPolarsAPIBtn.setEnabled(True)

    def showPolarsAPIFailedTip(self):
        InfoBar.error(
            title=self.tr("错误"),
            content=self.tr("获取极星镜像API失败！\n尝试检查网络后，请再尝试刷新。"),
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
                self.tr("正在进一步请求极星镜像API"), self.tr("加载中，请稍后..."), self
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
            self.getPolarsCoreStateToolTip.setContent(self.tr("请求极星镜像API完毕！"))
            self.getPolarsCoreStateToolTip.setState(True)
            self.getPolarsCoreStateToolTip = None
            self.initPolarsCoreListWidget()
        else:
            self.getPolarsCoreStateToolTip.setContent(self.tr("请求极星镜像API失败！"))
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
        if not self.checkAria2Service():
            return
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

    ###############
    # Akira Cloud #
    ###############

    def releaseAkiraMemory(self, id=0):
        layout = self.akiraTypeLayout if not id else self.akiraCoreLayout
        if layout == self.akiraCoreLayout:
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

    def getAkiraInfo(self):
        """请求Polars API"""
        workThread = self.fetchAkiraTypeThreadFactory.create(
            _singleton=True, finishSlot=self.updateAkiraTypeList
        )
        if workThread.isRunning():
            self.refreshAkiraCloudBtn.setEnabled(False)
            return
        else:
            self.getAkiraStateToolTip = StateToolTip(
                self.tr("正在请求Akira Cloud镜像站"), self.tr("加载中，请稍后..."), self
            )
            self.getAkiraStateToolTip.move(self.getAkiraStateToolTip.getSuitablePos())
            self.getAkiraStateToolTip.show()
            workThread.start()
            self.refreshAkiraCloudBtn.setEnabled(False)

    @pyqtSlot(list)
    def updateAkiraTypeList(self, _APIList):
        downloadVariables.AkiraTypeList = _APIList
        if len(downloadVariables.AkiraTypeList):
            self.getAkiraStateToolTip.setContent(self.tr("请求Akira Cloud镜像站完毕！"))
            self.getAkiraStateToolTip.setState(True)
            self.getAkiraStateToolTip = None
            self.initAkiraTypeListWidget()
        else:
            self.getAkiraStateToolTip.setContent(self.tr("请求Akira Cloud镜像站失败！"))
            self.getAkiraStateToolTip.setState(True)
            self.getAkiraStateToolTip = None
            self.showAkiraFailedTip()
        self.refreshAkiraCloudBtn.setEnabled(True)

    def showAkiraFailedTip(self):
        InfoBar.error(
            title=self.tr("错误"),
            content=self.tr("获取Akira Cloud镜像站信息失败！\n尝试检查网络后，请再尝试刷新。"),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self,
        )

    def initAkiraTypeListWidget(self):
        self.releaseAkiraMemory()
        self.akiraBtnGroup.deleteLater()
        self.akiraBtnGroup = QButtonGroup(self)
        for i in range(len(downloadVariables.AkiraTypeList)):
            k = PolarsTypeWidget(
                name=downloadVariables.AkiraTypeList[i],
                idx=1,
                description="",
                slot=self.akiraTypeProcessor,
                parent=self,
            )
            self.akiraTypeLayout.addWidget(k)
            self.akiraBtnGroup.addButton(k)

    def akiraTypeProcessor(self):
        self.akiraTypeLabel.setText(self.sender().property("name"))
        self.getAkiraCore(coreType=self.sender().property("name"))

    def getAkiraCore(self, coreType):
        workThread = self.fetchAkiraCoreThreadFactory.create(
            _singleton=True, coreType=coreType, finishSlot=self.updateAkiraAPICoreDict
        )
        if workThread.isRunning():
            self.refreshAkiraCloudBtn.setEnabled(False)
            return
        else:
            self.getAkiraCoreStateToolTip = StateToolTip(
                self.tr("正在进一步请求Akira Cloud镜像站"), self.tr("加载中，请稍后..."), self
            )
            self.getAkiraCoreStateToolTip.move(self.getAkiraCoreStateToolTip.getSuitablePos())
            self.getAkiraCoreStateToolTip.show()
            workThread.start()
            self.refreshAkiraCloudBtn.setEnabled(False)

    @pyqtSlot(dict)
    def updateAkiraAPICoreDict(self, _APIDict: dict):
        downloadVariables.AkiraCoreDict.clear()
        downloadVariables.AkiraCoreDict.update(_APIDict)
        if downloadVariables.AkiraCoreDict["name"] != "-1":
            self.getAkiraCoreStateToolTip.setContent(self.tr("请求Akira Cloud镜像站完毕！"))
            self.getAkiraCoreStateToolTip.setState(True)
            self.getAkiraCoreStateToolTip = None
            self.initAkiraCoreListWidget()
        else:
            self.getAkiraCoreStateToolTip.setContent(self.tr("请求Akira Cloud镜像站失败！"))
            self.getAkiraCoreStateToolTip.setState(True)
            self.getAkiraCoreStateToolTip = None
            self.showAkiraFailedTip()
        self.refreshAkiraCloudBtn.setEnabled(True)

    def initAkiraCoreListWidget(self):
        self.releaseAkiraMemory(1)
        for i in range(len(downloadVariables.AkiraCoreDict["list"])):
            w = FastMirrorBuildListWidget(
                buildVer=downloadVariables.AkiraCoreDict["list"][i],
                syncTime="",
                coreVersion=downloadVariables.AkiraCoreDict["name"],
                btnSlot=self.downloadAkiraFile,
                parent=self,
            )
            w.syncTimeLabel.setParent(None)
            self.akiraCoreLayout.addWidget(w)
        self.akiraCoreLayout.addItem(self.scrollAreaSpacer)

    def downloadAkiraFile(self):
        """下载Akira Cloud镜像站文件"""
        if not self.checkAria2Service():
            return
        uri = f"https://mirror.akiracloud.net/{self.sender().property('core_version')}/{self.sender().parent().buildVerLabel.text()}"
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
                self.tr("正在请求FastMirror API"), self.tr("加载中，请稍后..."), self
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
                self.tr("正在进一步请求FastMirror API"), self.tr("加载中，请稍后..."), self
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
            self.getFastMirrorStateToolTip.setContent(self.tr("请求FastMirror API完毕！"))
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
            self.getFastMirrorStateToolTip.setContent(self.tr("请求FastMirror API完毕！"))
            self.getFastMirrorStateToolTip.setState(True)
            self.getFastMirrorStateToolTip = None
            self.initFastMirrorCoreVersionListWidget()
        else:
            self.getFastMirrorStateToolTip.setContent(self.tr("请求FastMirror API失败！"))
            self.getFastMirrorStateToolTip.setState(True)
            self.getFastMirrorStateToolTip = None

    def showFastMirrorFailedTip(self):
        i = InfoBar.error(
            title=self.tr("错误"),
            content=self.tr(
                "获取FastMirror API失败！\n \
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
        if not self.checkAria2Service():
            return
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
        if not self.checkAria2Service():
            return
        urlLineEdit = LineEdit()
        urlLineEdit.setPlaceholderText(self.tr("URL"))
        w = MessageBox(
            "创建下载任务",
            "使用MCSL2自带的高速Aria2下载引擎下载文件。\n请注意，部分网站可能会禁止(403)，无法正常下载。",
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

    def checkAria2Service(self):
        if not Aria2Controller.testAria2Service():
            if not Aria2Controller.startAria2():
                box = MessageBox(
                    title=self.tr("无法下载"),
                    content=self.tr("Aria2可能未安装或启动失败。\n已尝试重新启动Aria2。"),
                    parent=self,
                )
                box.yesSignal.connect(box.deleteLater)
                box.cancelButton.setParent(None)
                box.cancelButton.deleteLater()
                del box.cancelButton
                box.exec()
                return False
            else:
                return True
        else:
            return True

    def checkDownloadFileExists(self, fileName, fileFormat, uri, extraData: tuple) -> bool:
        if osp.exists(
            osp.join("MCSL2", "Downloads", f"{fileName}.{fileFormat}")
        ) and not osp.exists(osp.join("MCSL2", "Downloads", f"{fileName}.{fileFormat}.aria2")):
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
                        "MCSL2/Downloads文件夹存在同名文件。\n根据设置，已删除原文件并继续下载。"
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
                    content=self.tr("MCSL2/Downloads文件夹存在同名文件。\n根据设置，已停止下载。"),
                    orient=Qt.Horizontal,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                    duration=2222,
                    parent=self,
                )
        else:
            self.downloadFile(fileName, fileFormat, uri, extraData)

    def downloadFile(self, fileName, fileFormat, uri, extraData: tuple):
        downloadingInfoWidget = DownloadCard(
            fileName=f"{fileName}.{fileFormat}", url=uri, parent=self
        )
        gid = Aria2Controller.download(
            uri=uri,
            watch=True,
            info_get=downloadingInfoWidget.onInfoGet,
            stopped=downloadingInfoWidget.onDownloadFinished,
            interval=0.2,
            extraData=extraData,
        )
        downloadingInfoWidget.canceled.connect(lambda: Aria2Controller.cancelDownloadTask(gid))
        downloadingInfoWidget.paused.connect(
            lambda x: Aria2Controller.pauseDownloadTask(gid)
            if x
            else Aria2Controller.resumeDownloadTask(gid)
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

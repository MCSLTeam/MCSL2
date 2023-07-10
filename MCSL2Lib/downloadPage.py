from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtWidgets import (
    QSizePolicy,
    QWidget,
    QFrame,
    QGridLayout,
    QVBoxLayout,
    QSpacerItem
)
from qfluentwidgets import (
    SmoothScrollArea,
    StrongBodyLabel,
    SubtitleLabel,
    TitleLabel
)
from MCSL2Lib.variables import scrollAreaViewportQss


class _DownloadPage(QWidget):
    def __init__(self):

        super().__init__()

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
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.verticalLayout.addWidget(self.subTitleLabel)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 2, 3)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.coreListSubtitleLabel = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coreListSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.coreListSubtitleLabel.setSizePolicy(sizePolicy)
        self.coreListSubtitleLabel.setObjectName("coreListSubtitleLabel")

        self.gridLayout.addWidget(self.coreListSubtitleLabel, 4, 2, 1, 1)
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.versionSubtitleLabel = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.versionSubtitleLabel.setSizePolicy(sizePolicy)
        self.versionSubtitleLabel.setObjectName("versionSubtitleLabel")

        self.gridLayout.addWidget(self.versionSubtitleLabel, 4, 3, 1, 1)
        self.buildSubtitleLabel = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buildSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.buildSubtitleLabel.setSizePolicy(sizePolicy)
        self.buildSubtitleLabel.setObjectName("buildSubtitleLabel")

        self.gridLayout.addWidget(self.buildSubtitleLabel, 4, 4, 1, 1)
        self.coreListSmoothScrollArea = SmoothScrollArea(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coreListSmoothScrollArea.sizePolicy().hasHeightForWidth())
        self.coreListSmoothScrollArea.setSizePolicy(sizePolicy)
        self.coreListSmoothScrollArea.setMinimumSize(QSize(200, 0))
        self.coreListSmoothScrollArea.setMaximumSize(QSize(200, 16777215))
        self.coreListSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.coreListSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.coreListSmoothScrollArea.setWidgetResizable(True)
        self.coreListSmoothScrollArea.setObjectName("coreListSmoothScrollArea")

        self.coreListScrollAreaWidgetContents = QWidget()
        self.coreListScrollAreaWidgetContents.setGeometry(QRect(0, 0, 200, 392))
        self.coreListScrollAreaWidgetContents.setObjectName("coreListScrollAreaWidgetContents")

        self.coreListSmoothScrollArea.setWidget(self.coreListScrollAreaWidgetContents)
        self.gridLayout.addWidget(self.coreListSmoothScrollArea, 5, 2, 1, 1)
        self.versionSmoothScrollArea = SmoothScrollArea(self)
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
        self.versionScrollAreaWidgetContents.setGeometry(QRect(0, 0, 160, 392))
        self.versionScrollAreaWidgetContents.setObjectName("versionScrollAreaWidgetContents")

        self.versionSmoothScrollArea.setWidget(self.versionScrollAreaWidgetContents)
        self.gridLayout.addWidget(self.versionSmoothScrollArea, 5, 3, 1, 1)
        self.buildScrollArea = SmoothScrollArea(self)
        self.buildScrollArea.setMinimumSize(QSize(304, 0))
        self.buildScrollArea.setFrameShape(QFrame.NoFrame)
        self.buildScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.buildScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.buildScrollArea.setWidgetResizable(True)
        self.buildScrollArea.setObjectName("buildScrollArea")

        self.buildScrollAreaWidgetContents = QWidget()
        self.buildScrollAreaWidgetContents.setGeometry(QRect(0, 0, 304, 392))
        self.buildScrollAreaWidgetContents.setObjectName("buildScrollAreaWidgetContents")

        self.buildScrollArea.setWidget(self.buildScrollAreaWidgetContents)
        self.gridLayout.addWidget(self.buildScrollArea, 5, 4, 1, 1)
        
        self.setObjectName("DownloadInterface")

        self.titleLabel.setText("下载")
        self.subTitleLabel.setText("由FastMirror提供支持。")
        self.coreListSubtitleLabel.setText("核心列表")
        self.versionSubtitleLabel.setText("游戏版本")
        self.buildSubtitleLabel.setText("构建列表")

        self.coreListSmoothScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.coreListSmoothScrollArea.viewport().setStyleSheet(scrollAreaViewportQss)
        self.versionSmoothScrollArea.viewport().setStyleSheet(scrollAreaViewportQss)
        self.buildScrollArea.viewport().setStyleSheet(scrollAreaViewportQss)

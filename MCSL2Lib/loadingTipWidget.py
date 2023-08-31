from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QSizePolicy,
    QWidget,
    QGridLayout,
    QSpacerItem,
    QHBoxLayout,
    QVBoxLayout,
)
from qfluentwidgets import (
    IndeterminateProgressRing,
    SubtitleLabel,
    PixmapLabel,
    PrimaryPushButton,
)


class LoadingTip(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("LoadingTip")
        self.resize(120, 135)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(120, 135))
        self.setMaximumSize(QSize(120, 135))
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.IndeterminateProgressRing = IndeterminateProgressRing(self)
        self.IndeterminateProgressRing.setAlignment(Qt.AlignCenter)
        self.IndeterminateProgressRing.setObjectName("IndeterminateProgressRing")

        self.gridLayout.addWidget(self.IndeterminateProgressRing, 0, 1, 1, 1)
        self.loadingText = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadingText.sizePolicy().hasHeightForWidth())
        self.loadingText.setSizePolicy(sizePolicy)
        self.loadingText.setAlignment(Qt.AlignCenter)
        self.loadingText.setObjectName("loadingText")

        self.gridLayout.addWidget(self.loadingText, 1, 1, 1, 1)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 2, 1)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 2, 1)
        self.loadingText.setText("加载中...")


class LoadFailedTip(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("LoadFailedTip")
        self.resize(120, 170)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(120, 170))
        self.setMaximumSize(QSize(120, 170))
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 2, 1)
        self.errPixmap = PixmapLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.errPixmap.sizePolicy().hasHeightForWidth())
        self.errPixmap.setSizePolicy(sizePolicy)
        self.errPixmap.setMinimumSize(QSize(80, 80))
        self.errPixmap.setMaximumSize(QSize(80, 80))
        self.errPixmap.setObjectName("errPixmap")

        self.gridLayout.addWidget(self.errPixmap, 0, 1, 1, 1)
        self.loadFailedText = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.loadFailedText.sizePolicy().hasHeightForWidth()
        )
        self.loadFailedText.setSizePolicy(sizePolicy)
        self.loadFailedText.setAlignment(Qt.AlignCenter)
        self.loadFailedText.setObjectName("loadFailedText")

        self.gridLayout.addWidget(self.loadFailedText, 1, 1, 1, 1)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 2, 1)
        self.refreshBtn = PrimaryPushButton(self)
        self.refreshBtn.setObjectName("refreshBtn")
        
        self.gridLayout.addWidget(self.refreshBtn, 2, 1, 1, 1)

        self.loadFailedText.setText("加载失败")
        self.refreshBtn.setText("刷新")


class MCSLAPILoadingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("MCSLAPILoading")

        self.resize(656, 135)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(656, 135))
        self.setMaximumSize(QSize(16777215, 135))
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.IndeterminateProgressRing = IndeterminateProgressRing(self)
        self.IndeterminateProgressRing.setAlignment(Qt.AlignCenter)
        self.IndeterminateProgressRing.setObjectName("IndeterminateProgressRing")

        self.gridLayout.addWidget(self.IndeterminateProgressRing, 0, 1, 1, 1)
        self.loadingText = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadingText.sizePolicy().hasHeightForWidth())
        self.loadingText.setSizePolicy(sizePolicy)
        self.loadingText.setAlignment(Qt.AlignCenter)
        self.loadingText.setObjectName("loadingText")

        self.gridLayout.addWidget(self.loadingText, 1, 1, 1, 1)
        spacerItem = QSpacerItem(270, 114, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 2, 1)
        spacerItem1 = QSpacerItem(270, 114, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 2, 1)
        self.loadingText.setText("加载中...")


class MCSLAPILoadingErrorWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("MCSLAPILoadingError")

        self.resize(656, 160)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(656, 160))
        self.setMaximumSize(QSize(16777215, 160))
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.errPixmapWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.errPixmapWidget.sizePolicy().hasHeightForWidth()
        )
        self.errPixmapWidget.setSizePolicy(sizePolicy)
        self.errPixmapWidget.setObjectName("errPixmapWidget")

        self.horizontalLayout_2 = QHBoxLayout(self.errPixmapWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        spacerItem = QSpacerItem(261, 69, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.errPixmap = PixmapLabel(self.errPixmapWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.errPixmap.sizePolicy().hasHeightForWidth())
        self.errPixmap.setSizePolicy(sizePolicy)
        self.errPixmap.setObjectName("errPixmap")

        self.horizontalLayout_2.addWidget(self.errPixmap)
        spacerItem1 = QSpacerItem(270, 114, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.errPixmapWidget)
        self.errTextWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.errTextWidget.sizePolicy().hasHeightForWidth()
        )
        self.errTextWidget.setSizePolicy(sizePolicy)
        self.errTextWidget.setObjectName("errTextWidget")

        self.horizontalLayout = QHBoxLayout(self.errTextWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem2 = QSpacerItem(69, 15, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.errText = SubtitleLabel(self.errTextWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.errText.sizePolicy().hasHeightForWidth())
        self.errText.setSizePolicy(sizePolicy)
        self.errText.setAlignment(Qt.AlignCenter)
        self.errText.setObjectName("errText")

        self.horizontalLayout.addWidget(self.errText)
        spacerItem3 = QSpacerItem(40, 15, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.errTextWidget)
        self.errText.setText("加载失败。请尝试刷新，如果仍然失败，请汇报此Bug。")
        self.errPixmap.setPixmap(QPixmap(":/built-InIcons/Error.svg"))
        self.errPixmap.setFixedSize(QSize(80, 80))

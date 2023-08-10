from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout, QSpacerItem
from qfluentwidgets import IndeterminateProgressRing, SubtitleLabel


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
        self.setWindowTitle("")
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

from PyQt5.QtWidgets import (
    QSizePolicy,
    QFrame,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QSpacerItem
)
from PyQt5.QtCore import Qt, QRect
from qfluentwidgets import SmoothScrollArea, StrongBodyLabel, TitleLabel
from MCSL2Lib.variables import scrollAreaViewportQss

class _ServerManagerPage(QWidget):
    def __init__(self):

        super().__init__()

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle("")
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
        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")
        self.gridLayout_2.addWidget(self.subTitleLabel, 1, 0, 1, 1)
        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout_2.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.serversSmoothScrollArea = SmoothScrollArea(self.titleLimitWidget)
        self.serversSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.serversSmoothScrollArea.setFrameShadow(QFrame.Plain)
        self.serversSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.serversSmoothScrollArea.setWidgetResizable(True)
        self.serversSmoothScrollArea.setObjectName("serversSmoothScrollArea")
        self.serversScrollAreaWidgetContents = QWidget()
        self.serversScrollAreaWidgetContents.setGeometry(QRect(0, 0, 658, 469))
        self.serversScrollAreaWidgetContents.setObjectName("serversScrollAreaWidgetContents")
        self.verticalLayout = QVBoxLayout(self.serversScrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.serversSmoothScrollArea.setWidget(self.serversScrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.serversSmoothScrollArea, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 2, 2)

        self.setObjectName("ManagerInterface")

        self.subTitleLabel.setText("在此处，管理你所有的服务器。")
        self.titleLabel.setText("管理")

        self.serversSmoothScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.serversSmoothScrollArea.viewport().setStyleSheet(scrollAreaViewportQss)
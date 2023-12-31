from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QGridLayout, QSizePolicy, QWidget, QSpacerItem, QFrame

from qfluentwidgets import StrongBodyLabel, TitleLabel

from MCSL2Lib.ProgramControllers.interfaceController import MySmoothScrollArea


class ConsoleCenterPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ConsoleInterface")

        self.gridLayout = QGridLayout(self)
        self.titleLimitWidget = QWidget(self)
        self.titleLayout = QGridLayout(self.titleLimitWidget)
        self.subTitleLabel = StrongBodyLabel(
            text="查看所有正在运行中的服务器。", parent=self.titleLimitWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.titleLayout.addWidget(self.subTitleLabel, 1, 0, 1, 1)
        self.titleLabel = TitleLabel(text="监控", parent=self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 2, 2)
        spacerItem = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.runningServersScrollArea = MySmoothScrollArea(self)
        self.runningServersScrollArea.setFrameShape(QFrame.NoFrame)
        self.runningServersScrollArea.setFrameShadow(QFrame.Plain)
        self.runningServersScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.runningServersScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.runningServersScrollArea.setWidgetResizable(True)
        self.runningServersScrollArea.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.runningServersScrollAreaWidgetContents = QWidget()
        self.runningServersScrollAreaWidgetContents.setGeometry(QRect(0, 0, 670, 512))
        self.runningServersScrollArea.setWidget(self.runningServersScrollAreaWidgetContents)
        self.gridLayout.addWidget(self.runningServersScrollArea, 3, 2, 1, 1)

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
from PyQt5.QtCore import QRect, Qt, pyqtSlot
from PyQt5.QtWidgets import QGridLayout, QSizePolicy, QWidget, QSpacerItem, QFrame

from qfluentwidgets import StrongBodyLabel, TitleLabel, FlowLayout

from MCSL2Lib.ProgramControllers.interfaceController import MySmoothScrollArea
from MCSL2Lib.Widgets.singleRunningServerWidget import RunningServerHeaderCardWidget


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
        self.flowLayout = FlowLayout(self.runningServersScrollAreaWidgetContents)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)

    @pyqtSlot(RunningServerHeaderCardWidget)
    def addRunningCard(self, card: RunningServerHeaderCardWidget):
        card.setParent(self.runningServersScrollAreaWidgetContents)
        self.flowLayout.addWidget(card)

    def isAnyServerRunning(self) -> bool:
        return bool(self.flowLayout.count() > 0)

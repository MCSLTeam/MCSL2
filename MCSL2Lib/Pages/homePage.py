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
Home page.
"""

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QGridLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy,
)
from qfluentwidgets import (
    PrimaryPushButton,
    PushButton,
    TitleLabel,
    FluentIcon as FIF,
)

from MCSL2Lib.singleton import Singleton


@Singleton
class HomePage(QWidget):
    """主页"""

    def __init__(self, parent=None):
        super().__init__(parent)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle("")
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.gridLayout_3 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayout_3.addWidget(self.titleLabel, 0, 0, 1, 1)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 2, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 1, 1)
        self.home_btnWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.home_btnWidget.sizePolicy().hasHeightForWidth())
        self.home_btnWidget.setSizePolicy(sizePolicy)
        self.home_btnWidget.setMinimumSize(QSize(200, 135))
        self.home_btnWidget.setMaximumSize(QSize(200, 135))
        self.home_btnWidget.setObjectName("home_btnWidget")
        self.gridLayout_2 = QGridLayout(self.home_btnWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.newServerBtn = PushButton(self.home_btnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newServerBtn.sizePolicy().hasHeightForWidth())
        self.newServerBtn.setSizePolicy(sizePolicy)
        self.newServerBtn.setFocusPolicy(Qt.NoFocus)
        self.newServerBtn.setObjectName("newServerBtn")
        self.newServerBtn.setIcon(FIF.ADD_TO)
        self.gridLayout_2.addWidget(self.newServerBtn, 1, 0, 1, 1)
        self.downloadBtn = PushButton(self.home_btnWidget)
        self.downloadBtn.setIcon(FIF.CLOUD_DOWNLOAD)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadBtn.sizePolicy().hasHeightForWidth())
        self.downloadBtn.setSizePolicy(sizePolicy)
        self.downloadBtn.setObjectName("downloadBtn")
        self.gridLayout_2.addWidget(self.downloadBtn, 1, 1, 1, 1)
        self.selectServerBtn = PrimaryPushButton(self.home_btnWidget)
        self.selectServerBtn.setIcon(FIF.LIBRARY_FILL)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectServerBtn.sizePolicy().hasHeightForWidth())
        self.selectServerBtn.setSizePolicy(sizePolicy)
        self.selectServerBtn.setFixedSize(QSize(180, 65))
        self.selectServerBtn.setObjectName("selectServerBtn")
        self.gridLayout_2.addWidget(self.selectServerBtn, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.home_btnWidget, 4, 3, 1, 1)
        spacerItem1 = QSpacerItem(400, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        spacerItem2 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 0, 2, 1, 1)
        spacerItem4 = QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 3, 2, 1, 1)
        self.newServerBtn.setText(self.tr("新建"))
        self.downloadBtn.setText(self.tr("下载"))
        self.selectServerBtn.setText(self.tr("选择服务器"))
        self.titleLabel.setText(self.tr("主页"))

        self.setObjectName("homeInterface")

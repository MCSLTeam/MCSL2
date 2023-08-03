#     Copyright 2023, MCSL Team, mailto:lxhtz.dl@qq.com
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
Plugin page.
"""

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtWidgets import (
    QSizePolicy,
    QSpacerItem,
    QGridLayout,
    QWidget,
    QFrame,
    QVBoxLayout,
)
from qfluentwidgets import (
    PrimaryPushButton,
    PushButton,
    SmoothScrollArea,
    StrongBodyLabel,
    TitleLabel,
)
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import GlobalMCSL2Variables


@Singleton
class PluginPage(QWidget):
    """插件页"""

    def __init__(self):
        super().__init__()

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.PrimaryPushButton = PrimaryPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PrimaryPushButton.sizePolicy().hasHeightForWidth()
        )
        self.PrimaryPushButton.setSizePolicy(sizePolicy)
        self.PrimaryPushButton.setMinimumSize(QSize(82, 32))
        self.PrimaryPushButton.setMaximumSize(QSize(82, 32))
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")

        self.gridLayout.addWidget(self.PrimaryPushButton, 3, 4, 1, 1)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 2, 4, 1, 1)
        self.PushButton = PushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PushButton.sizePolicy().hasHeightForWidth())
        self.PushButton.setSizePolicy(sizePolicy)
        self.PushButton.setMinimumSize(QSize(82, 32))
        self.PushButton.setMaximumSize(QSize(82, 32))
        self.PushButton.setObjectName("PushButton")

        self.gridLayout.addWidget(self.PushButton, 4, 4, 1, 1)
        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.gridLayout_2 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

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

        self.gridLayout_2.addWidget(self.subTitleLabel, 1, 0, 1, 1)
        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayout_2.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.pluginsSmoothScrollArea = SmoothScrollArea(self.titleLimitWidget)
        self.pluginsSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.pluginsSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.pluginsSmoothScrollArea.setWidgetResizable(True)
        self.pluginsSmoothScrollArea.setObjectName("pluginsSmoothScrollArea")

        self.pluginsScrollAreaWidgetContents = QWidget()
        self.pluginsScrollAreaWidgetContents.setGeometry(QRect(0, 0, 544, 470))
        self.pluginsScrollAreaWidgetContents.setObjectName(
            "pluginsScrollAreaWidgetContents"
        )

        self.gridLayout_3 = QGridLayout(self.pluginsScrollAreaWidgetContents)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.pluginsVerticalLayout = QVBoxLayout()
        self.pluginsVerticalLayout.setObjectName("pluginsVerticalLayout")

        self.gridLayout_3.addLayout(self.pluginsVerticalLayout, 0, 0, 1, 1)
        self.pluginsSmoothScrollArea.setWidget(self.pluginsScrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.pluginsSmoothScrollArea, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 5, 2)
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 4, 1, 1)
        spacerItem3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 0, 2, 1, 1)
        spacerItem4 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 3, 5, 1, 1)

        self.setObjectName("PluginsInterface")

        self.pluginsSmoothScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.subTitleLabel.setText("添加属于你的插件，让你的MCSL2更加强大！")
        self.titleLabel.setText("插件")
        self.PushButton.setText("插件设置")
        self.PrimaryPushButton.setText("安装插件")

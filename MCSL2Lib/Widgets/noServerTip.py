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
A Widget for showing that there's no Minecraft Servers in MCSL2.
"""
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QSizePolicy,
    QWidget,
    QSpacerItem,
    QHBoxLayout,
    QVBoxLayout,
)
from qfluentwidgets import (
    SubtitleLabel,
    PixmapLabel,
)
from MCSL2Lib.Resources.icons import *  # noqa: F401

class NoServerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("noServerWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(656, 160))
        self.setMaximumSize(QSize(16777215, 202))
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
        spacerItem2 = QSpacerItem(50, 15, QSizePolicy.Fixed, QSizePolicy.Minimum)
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
        spacerItem3 = QSpacerItem(50, 15, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.errTextWidget)

        self.errText.setText("好像还没有添加过的服务器欸。先去“新建”页新建一个？")
        self.errPixmap.setPixmap(QPixmap(":/built-InIcons/Error.svg"))
        self.errPixmap.setFixedSize(QSize(80, 80))
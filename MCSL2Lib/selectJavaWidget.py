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
'''
A single widget template for selecting Java.
'''

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QSizePolicy,
    QWidget,
    QGridLayout,
    QFrame,
    QLayout,
    QHBoxLayout,
    QSpacerItem,
)
from qfluentwidgets import (
    CardWidget,
    LineEdit,
    PixmapLabel,
    PrimaryPushButton,
    BodyLabel,
    TextEdit,
)


class singleSelectJavaWidget(CardWidget):
    """单独的选择Java的Widget模板"""

    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(640, 160))
        self.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.finishSelectJavaBtn = PrimaryPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.finishSelectJavaBtn.sizePolicy().hasHeightForWidth()
        )
        self.finishSelectJavaBtn.setSizePolicy(sizePolicy)
        self.finishSelectJavaBtn.setMinimumSize(QSize(0, 50))
        self.finishSelectJavaBtn.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.finishSelectJavaBtn, 0, 3, 3, 1)
        self.javaPixmapLabel = PixmapLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.javaPixmapLabel.sizePolicy().hasHeightForWidth()
        )
        self.javaPixmapLabel.setSizePolicy(sizePolicy)
        self.javaPixmapLabel.setObjectName("javaPixmapLabel")

        self.gridLayout.addWidget(self.javaPixmapLabel, 0, 1, 4, 1)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 4, 1)
        self.javaVerWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.javaVerWidget.sizePolicy().hasHeightForWidth()
        )
        self.javaVerWidget.setSizePolicy(sizePolicy)
        self.javaVerWidget.setMinimumSize(QSize(480, 50))
        self.javaVerWidget.setMaximumSize(QSize(16777215, 50))
        self.javaVerWidget.setObjectName("javaVerWidget")

        self.horizontalLayout = QHBoxLayout(self.javaVerWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.javaVerTitle = BodyLabel(self.javaVerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.javaVerTitle.sizePolicy().hasHeightForWidth())
        self.javaVerTitle.setSizePolicy(sizePolicy)
        self.javaVerTitle.setObjectName("javaVerTitle")

        self.horizontalLayout.addWidget(self.javaVerTitle)
        self.javaVer = LineEdit(self.javaVerWidget)
        self.javaVer.setReadOnly(True)
        self.javaVer.setReadOnly(True)
        self.javaVer.setReadOnly(True)
        self.javaVer.setReadOnly(True)
        self.javaVer.setReadOnly(True)
        self.javaVer.setReadOnly(True)
        self.javaVer.setReadOnly(True)
        self.javaVer.setReadOnly(True)
        self.javaVer.setObjectName("javaVer")

        self.horizontalLayout.addWidget(self.javaVer)
        self.gridLayout.addWidget(self.javaVerWidget, 0, 2, 1, 1)
        self.javaPathWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.javaPathWidget.sizePolicy().hasHeightForWidth()
        )
        self.javaPathWidget.setSizePolicy(sizePolicy)
        self.javaPathWidget.setMinimumSize(QSize(480, 82))
        self.javaPathWidget.setObjectName("javaPathWidget")

        self.gridLayout_2 = QGridLayout(self.javaPathWidget)
        self.gridLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.javaPathTitle = BodyLabel(self.javaPathWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.javaPathTitle.sizePolicy().hasHeightForWidth()
        )
        self.javaPathTitle.setSizePolicy(sizePolicy)
        self.javaPathTitle.setObjectName("javaPathTitle")

        self.gridLayout_2.addWidget(self.javaPathTitle, 1, 0, 1, 1)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.javaPath = TextEdit(self.javaPathWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.javaPath.sizePolicy().hasHeightForWidth())
        self.javaPath.setSizePolicy(sizePolicy)
        self.javaPath.setMinimumSize(QSize(0, 33))
        self.javaPath.setFrameShape(QFrame.StyledPanel)
        self.javaPath.setFrameShadow(QFrame.Sunken)
        self.javaPath.setReadOnly(True)
        self.javaPath.setReadOnly(True)
        self.javaPath.setReadOnly(True)
        self.javaPath.setReadOnly(True)
        self.javaPath.setReadOnly(True)
        self.javaPath.setReadOnly(True)
        self.javaPath.setReadOnly(True)
        self.javaPath.setReadOnly(True)
        self.javaPath.setObjectName("javaPath")

        self.gridLayout_2.addWidget(self.javaPath, 1, 1, 2, 1)
        self.gridLayout.addWidget(self.javaPathWidget, 1, 2, 1, 1)
        self.finishSelectJavaBtn.setText("选择")
        self.javaVerTitle.setText("Java版本:")
        self.javaPathTitle.setText("Java路径:")
        self.javaPixmapLabel.setPixmap(QPixmap(":/built-InIcons/Java.svg"))
        self.javaPixmapLabel.setFixedSize(QSize(50, 50))

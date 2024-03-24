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
A single widget template for selecting Java.
"""

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QSizePolicy,
    QWidget,
    QGridLayout,
    QLayout,
    QHBoxLayout,
)
from qfluentwidgets import (
    SimpleCardWidget,
    LineEdit,
    PixmapLabel,
    PrimaryPushButton,
    BodyLabel,
    TextEdit,
)
from MCSL2Lib.Resources.icons import *  # noqa: F401 F403


class SingleSelectJavaWidget(SimpleCardWidget):
    """单独的选择Java的Widget模板"""

    def __init__(self, btnName: str, selectBtnSlot, backBtnSlot, path, ver):
        super().__init__()

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(550, 150))
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.javaVerWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.javaVerWidget.sizePolicy().hasHeightForWidth()
        )
        self.javaVerWidget.setSizePolicy(sizePolicy)
        self.javaVerWidget.setMinimumSize(QSize(280, 50))
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
        self.javaVer.setObjectName("javaVer")
        self.horizontalLayout.addWidget(self.javaVer)
        self.gridLayout.addWidget(self.javaVerWidget, 0, 1, 1, 1)
        self.finishSelectJavaBtn = PrimaryPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.finishSelectJavaBtn.sizePolicy().hasHeightForWidth()
        )
        self.finishSelectJavaBtn.setSizePolicy(sizePolicy)
        self.finishSelectJavaBtn.setMinimumSize(QSize(0, 0))
        self.finishSelectJavaBtn.setMaximumSize(QSize(16777215, 16777215))
        self.finishSelectJavaBtn.setObjectName("finishSelectJavaBtn")
        self.gridLayout.addWidget(self.finishSelectJavaBtn, 0, 2, 3, 1)
        self.javaPixmapLabel = PixmapLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.javaPixmapLabel.sizePolicy().hasHeightForWidth()
        )
        self.javaPixmapLabel.setSizePolicy(sizePolicy)
        self.javaPixmapLabel.setFixedSize(QSize(50, 50))
        self.javaPixmapLabel.setObjectName("javaPixmapLabel")
        self.gridLayout.addWidget(self.javaPixmapLabel, 0, 0, 4, 1)
        self.javaPathWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.javaPathWidget.sizePolicy().hasHeightForWidth()
        )
        self.javaPathWidget.setSizePolicy(sizePolicy)
        self.javaPathWidget.setMinimumSize(QSize(280, 50))
        self.javaPathWidget.setMaximumSize(QSize(16777215, 50))
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
        self.javaPath = TextEdit(self.javaPathWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.javaPath.sizePolicy().hasHeightForWidth())
        self.javaPath.setSizePolicy(sizePolicy)
        self.javaPath.setFixedHeight(50)
        self.javaPath.setReadOnly(True)
        self.javaPath.setObjectName("javaPath")
        self.gridLayout_2.addWidget(self.javaPath, 1, 1, 2, 1)
        self.gridLayout.addWidget(self.javaPathWidget, 1, 1, 1, 1)

        self.finishSelectJavaBtn.setText(self.tr("选择"))
        self.javaVerTitle.setText(self.tr("版本: "))
        self.javaPathTitle.setText(self.tr("路径: "))
        self.javaPixmapLabel.setPixmap(QPixmap(":/built-InIcons/Java.svg"))
        self.javaPixmapLabel.setFixedSize(QSize(50, 50))

        self.finishSelectJavaBtn.setObjectName(btnName)
        self.finishSelectJavaBtn.clicked.connect(selectBtnSlot)
        self.finishSelectJavaBtn.clicked.connect(backBtnSlot)
        self.javaPath.setText(str(path))
        self.javaVer.setText(str(ver))

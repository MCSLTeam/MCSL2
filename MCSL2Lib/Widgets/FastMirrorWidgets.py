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
FastMirror Download Widgets.
"""
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QSizePolicy, QGridLayout, QHBoxLayout, QWidget, QVBoxLayout
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    StrongBodyLabel,
    PrimaryToolButton,
    FluentIcon as FIF,
    InfoBadge,
)


class FastMirrorVersionListWidget(CardWidget):
    def __init__(self, version, slot, parent=None):
        super().__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(140, 48))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.versionLabel = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionLabel.sizePolicy().hasHeightForWidth())
        self.versionLabel.setSizePolicy(sizePolicy)
        self.versionLabel.setAlignment(Qt.AlignCenter)
        self.versionLabel.setObjectName("versionLabel")
        self.horizontalLayout.addWidget(self.versionLabel)
        # self.versionLabel.setObjectName("versionLabel")
        self.versionLabel.setText(version)
        self.clicked.connect(slot)
        self.setProperty("version", version)


class FastMirrorCoreListWidget(CardWidget):
    def __init__(self, tag, name, slot, parent=None):
        super().__init__(parent)
        # self.setObjectName("coreListWidget")

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(180, 48))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.coreTagWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.coreTagWidget.sizePolicy().hasHeightForWidth()
        )
        self.coreTagWidget.setSizePolicy(sizePolicy)
        self.coreTagWidget.setMinimumSize(QSize(0, 35))
        self.coreTagWidget.setMaximumSize(QSize(16777215, 35))
        self.coreTagWidget.setObjectName("coreTagWidget")
        self.gridLayout = QGridLayout(self.coreTagWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.coreTag = InfoBadge.attension("", self.coreTagWidget)
        self.gridLayout.addWidget(self.coreTag, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.coreTagWidget)
        self.coreName = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coreName.sizePolicy().hasHeightForWidth())
        self.coreName.setSizePolicy(sizePolicy)
        self.coreName.setAlignment(Qt.AlignCenter)
        self.coreName.setObjectName("coreName")
        self.horizontalLayout.addWidget(self.coreName)

        self.horizontalLayout.addWidget(self.coreName)

        self.coreTag.setText(tag)
        self.coreName.setText(name)
        self.setProperty("name", name)
        self.clicked.connect(slot)


class FastMirrorBuildListWidget(CardWidget):
    def __init__(self, buildVer, syncTime, coreVersion, btnSlot, parent=None):
        super().__init__(parent)

        self.setObjectName("buildListWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(284, 72))
        self.setMaximumSize(QSize(16777215, 72))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TextWidget = QWidget(self)
        self.TextWidget.setObjectName("TextWidget")
        self.verticalLayout = QVBoxLayout(self.TextWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buildVerLabel = StrongBodyLabel(self.TextWidget)
        self.buildVerLabel.setObjectName("buildVerLabel")
        self.verticalLayout.addWidget(self.buildVerLabel)
        self.syncTimeLabel = StrongBodyLabel(self.TextWidget)
        self.syncTimeLabel.setObjectName("syncTimeLabel")
        self.verticalLayout.addWidget(self.syncTimeLabel)
        self.horizontalLayout.addWidget(self.TextWidget)
        self.downloadBtn = PrimaryToolButton(FIF.DOWNLOAD, self)
        self.downloadBtn.setFixedSize(QSize(40, 40))
        self.downloadBtn.setObjectName("downloadBtn")
        self.horizontalLayout.addWidget(self.downloadBtn)

        self.buildVerLabel.setText(buildVer)
        self.syncTimeLabel.setText(syncTime)
        self.downloadBtn.clicked.connect(btnSlot)
        self.downloadBtn.setProperty("core_version", coreVersion)

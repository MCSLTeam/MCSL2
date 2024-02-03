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
FastMirror Download Widgets.
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QWidget, QVBoxLayout
from qfluentwidgets import (
    CardWidget,
    StrongBodyLabel,
    PrimaryToolButton,
    FluentIcon as FIF,
    ToggleButton,
)


class FastMirrorVersionButton(ToggleButton):
    def __init__(self, version, slot, parent=None):
        super().__init__(parent)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(140, 45))
        self.setText(version)
        self.clicked.connect(slot)
        self.setProperty("version", version)


class FastMirrorCorePushButton(ToggleButton):
    def __init__(self, tag, name, slot, parent=None):
        super().__init__(parent)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(150, 45))
        self.setText(f"{tag} | {name}")
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
        self.setMinimumSize(QSize(284, 75))
        self.setMaximumSize(QSize(16777215, 75))
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
        self.downloadBtn = PrimaryToolButton(FIF.CLOUD_DOWNLOAD, self)
        self.downloadBtn.setFixedSize(QSize(45, 45))
        self.downloadBtn.setObjectName("downloadBtn")
        self.horizontalLayout.addWidget(self.downloadBtn)

        self.buildVerLabel.setText(buildVer)
        self.syncTimeLabel.setText(syncTime)
        self.downloadBtn.clicked.connect(btnSlot)
        self.downloadBtn.setProperty("core_version", coreVersion)

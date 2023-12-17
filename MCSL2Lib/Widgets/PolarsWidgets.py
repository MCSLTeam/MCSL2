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
Polars Download Widgets.
"""

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
)


class PolarsTypeWidget(CardWidget):
    def __init__(self, name, idx, description, slot, parent=None):
        super().__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(140, 48))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.nameLabel = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLabel.sizePolicy().hasHeightForWidth())
        self.nameLabel.setSizePolicy(sizePolicy)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setObjectName("versionLabel")
        self.horizontalLayout.addWidget(self.nameLabel)
        # self.versionLabel.setObjectName("versionLabel")
        self.nameLabel.setText(name)
        self.clicked.connect(slot)
        self.setProperty("name", name)
        self.setProperty("id", idx)
        self.setProperty("description", description)

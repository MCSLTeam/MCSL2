#     Copyright 2024, MCSL Team, mailto:lxhtt@vip.qq.com
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

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QSizePolicy
from qfluentwidgets import ToggleButton


class PolarsTypeWidget(ToggleButton):
    def __init__(self, name, idx, description, slot, parent=None):
        super().__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(140, 48))
        self.setText(name)
        self.clicked.connect(slot)
        self.setProperty("name", name)
        self.setProperty("id", idx)
        self.setProperty("description", description)

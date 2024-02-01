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
Download Item Widget for MCSLAPI.
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QHBoxLayout
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    PixmapLabel,
    StrongBodyLabel,
)


class MCSLAPIDownloadWidget(CardWidget):
    def __init__(self, link, name, size, pixmap, downloadSlot):
        super().__init__()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(656, 55))
        self.setMaximumSize(QSize(16777215, 55))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.MCSLAPIPixmapLabel = PixmapLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLAPIPixmapLabel.sizePolicy().hasHeightForWidth())
        self.MCSLAPIPixmapLabel.setSizePolicy(sizePolicy)
        self.MCSLAPIPixmapLabel.setFixedSize(QSize(40, 40))
        self.MCSLAPIPixmapLabel.setObjectName("MCSLAPIPixmapLabel")
        self.horizontalLayout.addWidget(self.MCSLAPIPixmapLabel)
        self.fileName = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileName.sizePolicy().hasHeightForWidth())
        self.fileName.setSizePolicy(sizePolicy)
        self.fileName.setObjectName("fileName")
        self.horizontalLayout.addWidget(self.fileName)
        self.fileSizeTitle = StrongBodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileSizeTitle.sizePolicy().hasHeightForWidth())
        self.fileSizeTitle.setSizePolicy(sizePolicy)
        self.fileSizeTitle.setObjectName("fileSizeTitle")
        self.horizontalLayout.addWidget(self.fileSizeTitle)
        self.fileSize = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileSize.sizePolicy().hasHeightForWidth())
        self.fileSize.setSizePolicy(sizePolicy)
        self.fileSize.setMinimumSize(QSize(70, 0))
        self.fileSize.setMaximumSize(QSize(70, 16777215))
        self.fileSize.setObjectName("fileSize")
        self.horizontalLayout.addWidget(self.fileSize)
        self.fileSizeTitle.setText("大小:")
        self.fileSize.setText(size if type(size) is str else str(f"{size / 1024 / 1024:.2f}MB"))
        self.fileName.setText(name.replace("/", ""))
        self.setProperty("link", f"https://file.mcsl.com.cn/d/alistfile/MCSL2/MCSLAPI{link}{name}")
        self.setProperty("name", name)
        self.MCSLAPIPixmapLabel.setPixmap(pixmap)
        self.MCSLAPIPixmapLabel.setFixedSize(QSize(40, 40))
        if size != "-":
            self.clicked.connect(downloadSlot)
        else:
            self.clicked.connect(lambda: downloadSlot(f"/{name}"))

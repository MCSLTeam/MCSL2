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
A single widget template for managing exist Minecraft servers.
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QSizePolicy, QGridLayout, QSpacerItem, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (
    BodyLabel,
    SimpleCardWidget,
    PixmapLabel,
    PrimaryPushButton,
    PushButton,
    StrongBodyLabel,
    SubtitleLabel,
    isDarkTheme,
)

from MCSL2Lib.variables import GlobalMCSL2Variables


class SingleServerManager(SimpleCardWidget):
    """单独的服务器管理Widget模板"""

    def __init__(self, mem, coreFileName, javaPath, serverName, icon, btnSlot, i, parent=None):
        super().__init__(parent)

        self.setObjectName("singleServerManagerWidget")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(550, 215))
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.serverName = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverName.sizePolicy().hasHeightForWidth())
        self.serverName.setSizePolicy(sizePolicy)
        self.serverName.setWordWrap(True)
        self.serverName.setObjectName("serverName")
        self.gridLayout.addWidget(self.serverName, 0, 1, 1, 1)
        self.btnWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnWidget.sizePolicy().hasHeightForWidth())
        self.btnWidget.setSizePolicy(sizePolicy)
        self.btnWidget.setObjectName("btnWidget")
        self.horizontalLayout = QHBoxLayout(self.btnWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.runBtn = PrimaryPushButton(self.btnWidget)
        self.runBtn.setObjectName("selectBtn")
        self.horizontalLayout.addWidget(self.runBtn)
        self.editBtn = PushButton(self.btnWidget)
        self.editBtn.setObjectName("editBtn")
        self.horizontalLayout.addWidget(self.editBtn)
        self.backupBtn = PushButton(self.btnWidget)
        self.backupBtn.setObjectName("backupBtn")
        self.horizontalLayout.addWidget(self.backupBtn)
        self.openDataFolderBtn = PushButton(self.btnWidget)
        self.openDataFolderBtn.setObjectName("openDataFolderBtn")
        self.horizontalLayout.addWidget(self.openDataFolderBtn)
        self.deleteBtn = PushButton(self.btnWidget)

        self.deleteBtn.setStyleSheet(
            GlobalMCSL2Variables.darkWarnBtnStyleSheet
            if isDarkTheme()
            else GlobalMCSL2Variables.lightWarnBtnStyleSheet
        )
        self.deleteBtn.setObjectName("deleteBtn")
        self.horizontalLayout.addWidget(self.deleteBtn)
        self.gridLayout.addWidget(self.btnWidget, 2, 1, 1, 2)
        self.serverInfoWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverInfoWidget.sizePolicy().hasHeightForWidth())
        self.serverInfoWidget.setSizePolicy(sizePolicy)
        self.serverInfoWidget.setMinimumSize(QSize(100, 70))
        self.serverInfoWidget.setObjectName("serverInfoWidget")
        self.gridLayout_2 = QGridLayout(self.serverInfoWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.coreFileNameTitle = StrongBodyLabel(self.serverInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coreFileNameTitle.sizePolicy().hasHeightForWidth())
        self.coreFileNameTitle.setSizePolicy(sizePolicy)
        self.coreFileNameTitle.setObjectName("coreFileNameTitle")
        self.gridLayout_2.addWidget(self.coreFileNameTitle, 0, 0, 1, 1)
        self.memTitle = StrongBodyLabel(self.serverInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.memTitle.sizePolicy().hasHeightForWidth())
        self.memTitle.setSizePolicy(sizePolicy)
        self.memTitle.setObjectName("memTitle")
        self.gridLayout_2.addWidget(self.memTitle, 2, 0, 1, 1)
        self.mem = BodyLabel(self.serverInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mem.sizePolicy().hasHeightForWidth())
        self.mem.setSizePolicy(sizePolicy)
        self.mem.setObjectName("mem")
        self.gridLayout_2.addWidget(self.mem, 2, 1, 1, 1)
        self.coreFileName = BodyLabel(self.serverInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coreFileName.sizePolicy().hasHeightForWidth())
        self.coreFileName.setSizePolicy(sizePolicy)
        self.coreFileName.setObjectName("coreFileName")
        self.gridLayout_2.addWidget(self.coreFileName, 0, 1, 1, 1)
        self.javaPathTitle = StrongBodyLabel(self.serverInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.javaPathTitle.sizePolicy().hasHeightForWidth())
        self.javaPathTitle.setSizePolicy(sizePolicy)
        self.javaPathTitle.setObjectName("javaPathTitle")
        self.gridLayout_2.addWidget(self.javaPathTitle, 1, 0, 1, 1)
        self.javaPath = BodyLabel(self.serverInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.javaPath.sizePolicy().hasHeightForWidth())
        self.javaPath.setSizePolicy(sizePolicy)
        self.javaPath.setObjectName("javaPath")
        self.gridLayout_2.addWidget(self.javaPath, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.serverInfoWidget, 1, 1, 1, 1)
        self.widget = QWidget(self)
        self.widget.setObjectName("widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Icon = PixmapLabel(self.widget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Icon.sizePolicy().hasHeightForWidth())
        self.Icon.setSizePolicy(sizePolicy)
        self.Icon.setFixedSize(QSize(70, 70))
        self.Icon.setObjectName("Icon")
        self.verticalLayout.addWidget(self.Icon)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.widget, 0, 0, 3, 1)

        self.runBtn.setText(self.tr("启动"))
        self.editBtn.setText(self.tr("编辑"))
        self.backupBtn.setText(self.tr("备份"))
        self.openDataFolderBtn.setText(self.tr("打开文件夹"))
        self.deleteBtn.setText(self.tr("删除"))
        self.coreFileNameTitle.setText(self.tr("核心："))
        self.memTitle.setText(self.tr("内存设置："))
        self.javaPathTitle.setText(self.tr("Java："))

        self.serverName.setWordWrap(True)
        self.mem.setText(mem)
        self.coreFileName.setText(coreFileName)
        self.javaPath.setText(javaPath)
        self.serverName.setText(serverName)
        self.Icon.setPixmap(icon)
        self.Icon.setFixedSize(QSize(70, 70))

        self.runBtn.clicked.connect(btnSlot)
        self.editBtn.clicked.connect(btnSlot)
        self.deleteBtn.clicked.connect(btnSlot)
        self.backupBtn.clicked.connect(btnSlot)
        self.openDataFolderBtn.clicked.connect(btnSlot)

        self.runBtn.setObjectName(f"runBtn{str(i)}")
        self.editBtn.setObjectName(f"editBtn{str(i)}")
        self.deleteBtn.setObjectName(f"deleteBtn{str(i)}")
        self.backupBtn.setObjectName(f"backupBtn{str(i)}")
        self.openDataFolderBtn.setObjectName(f"openDataFolderBtn{str(i)}")

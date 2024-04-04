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

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QWidget,
    QSizePolicy,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
)
from qfluentwidgets import (
    BodyLabel,
    SimpleCardWidget,
    PixmapLabel,
    PrimaryPushButton,
    StrongBodyLabel,
    SubtitleLabel,
    CommandBar,
    Action,
    FluentIcon as FIF,
)


class SingleServerManager(SimpleCardWidget):
    """单独的服务器管理Widget模板"""

    def __init__(self, mem, coreFileName, javaPath, serverName, icon, btnSlot, i, parent=None):
        super().__init__(parent)

        self.btnSlot = btnSlot
        self.setObjectName("singleServerManagerWidget")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(500, 215))
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.serverName = SubtitleLabel(self)
        self.serverName.setAlignment(Qt.AlignBottom | Qt.AlignLeading | Qt.AlignLeft)
        self.serverName.setFixedHeight(40)
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
        spacerItem = QSpacerItem(20, 30, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.horizontalLayout.addItem(spacerItem)
        self.runBtn = PrimaryPushButton(self.btnWidget)
        self.runBtn.setObjectName("selectBtn")
        self.horizontalLayout.addWidget(self.runBtn)
        self.actionsCommandBar = SingleServerManageCommandBar(i, self)
        self.actionsCommandBar.setObjectName("commandBar")
        self.horizontalLayout.addWidget(self.actionsCommandBar)
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
        self.coreFileNameTitle.setText(self.tr("核心: "))
        self.memTitle.setText(self.tr("内存设置: "))
        self.javaPathTitle.setText(self.tr("Java: "))

        self.serverName.setWordWrap(True)
        self.mem.setText(mem)
        self.coreFileName.setText(coreFileName)
        self.javaPath.setText(javaPath)
        self.serverName.setText(" " + serverName)
        self.Icon.setPixmap(icon)
        self.Icon.setFixedSize(QSize(70, 70))
        self.runBtn.clicked.connect(btnSlot)
        self.runBtn.setObjectName(f"startServer!{i}")
        self.runBtn.setIcon(FIF.PLAY_SOLID)


class SingleServerManageCommandBar(CommandBar):
    def __init__(self, i: str, parent=None):
        super().__init__(parent)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.editServer = Action(
            icon=FIF.EDIT.icon(), text=self.tr("编辑MCSL2服务器配置"), parent=self
        )
        self.editServerConfig = Action(
            icon=FIF.EDIT.icon(), text=self.tr("编辑服务器配置文件"), parent=self
        )
        self.backupFullServer = Action(
            icon=FIF.SAVE_COPY.icon(), text=self.tr("备份服务器"), parent=self
        )
        self.backupServerSaves = Action(
            icon=FIF.SAVE_COPY.icon(), text=self.tr("备份存档"), parent=self
        )
        self.openDataFolder = Action(
            icon=FIF.LINK.icon(), text=self.tr("打开服务器文件夹"), parent=self
        )
        self.deleteServer = Action(icon=FIF.DELETE.icon(), text=self.tr("删除服务器"), parent=self)

        self.editServer.setObjectName(f"editServer!{i}")
        self.editServerConfig.setObjectName(f"editServerConfig!{i}")
        self.backupFullServer.setObjectName(f"backupFullServer!{i}")
        self.backupServerSaves.setObjectName(f"backupServerSaves!{i}")
        self.openDataFolder.setObjectName(f"openDataFolder!{i}")
        self.deleteServer.setObjectName(f"deleteServer!{i}")
        self.actionsList = [
            self.editServer,
            self.editServerConfig,
            self.backupFullServer,
            self.backupServerSaves,
            self.openDataFolder,
            self.deleteServer,
        ]
        self.backupActionsList = [
            self.editServerConfig,
            self.backupFullServer,
            self.backupServerSaves,
        ]
        self.completeActions()

    def parent(self) -> SingleServerManager:
        return super().parent()

    def completeActions(self):
        for action in self.actionsList:
            action.triggered.connect(self.parent().btnSlot)
        self.addHiddenActions(self.actionsList)

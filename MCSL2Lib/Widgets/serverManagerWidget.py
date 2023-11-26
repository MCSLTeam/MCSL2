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
A single widget template for managing exist Minecraft servers.
'''

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QSizePolicy, QGridLayout, QSpacerItem, QVBoxLayout
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    PixmapLabel,
    PrimaryPushButton,
    PushButton,
    StrongBodyLabel,
    SubtitleLabel,
    isDarkTheme,
)


class singleServerManager(CardWidget):
    """单独的服务器管理Widget模板"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("singleServerManager")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(640, 200))
        self.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 11, 5, 1)
        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 4, 1)
        self.serverInfoWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverInfoWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverInfoWidget.setSizePolicy(sizePolicy)
        self.serverInfoWidget.setMinimumSize(QSize(100, 70))
        self.serverInfoWidget.setObjectName("serverInfoWidget")

        self.gridLayout_2 = QGridLayout(self.serverInfoWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.coreFileNameTitle = StrongBodyLabel(self.serverInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.coreFileNameTitle.sizePolicy().hasHeightForWidth()
        )
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
        sizePolicy.setHeightForWidth(
            self.javaPathTitle.sizePolicy().hasHeightForWidth()
        )
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
        self.gridLayout.addWidget(self.serverInfoWidget, 2, 8, 1, 1)
        spacerItem2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 0, 4, 1, 9)
        self.btnWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnWidget.sizePolicy().hasHeightForWidth())
        self.btnWidget.setSizePolicy(sizePolicy)
        self.btnWidget.setObjectName("btnWidget")

        self.verticalLayout = QVBoxLayout(self.btnWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.selectBtn = PrimaryPushButton(self.btnWidget)

        self.verticalLayout.addWidget(self.selectBtn)
        self.editBtn = PushButton(self.btnWidget)

        self.verticalLayout.addWidget(self.editBtn)
        self.deleteBtn = PushButton(self.btnWidget)
        if isDarkTheme():
            self.deleteBtn.setStyleSheet(
                "PushButton {\n"
                "    color: black;\n"
                "    background: rgba(255, 255, 255, 0.7);\n"
                "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                "    border-radius: 5px;\n"
                "    /* font: 14px 'Segoe UI', 'Microsoft YaHei'; */\n"
                "    padding: 5px 12px 6px 12px;\n"
                "    outline: none;\n"
                "}\n"
                "QPushButton {\n"
                "    background-color: rgba(255, 117, 117, 30%);\n"
                "    color: rgb(245, 0, 0)\n"
                "}\n"
                "QPushButton:hover {\n"
                "    background-color: rgba(255, 122, 122, 50%);\n"
                "    color: rgb(245, 0, 0)\n"
                "}"
            )
        else:
            self.deleteBtn.setStyleSheet(
                "PushButton {\n"
                "    color: black;\n"
                "    background: rgba(255, 255, 255, 0.7);\n"
                "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                "    border-radius: 5px;\n"
                "    /* font: 14px 'Segoe UI', 'Microsoft YaHei'; */\n"
                "    padding: 5px 12px 6px 12px;\n"
                "    outline: none;\n"
                "}\n"
                "QPushButton {\n"
                "    background-color: rgba(255, 117, 117, 30%);\n"
                "    color: rgb(255, 0, 0)\n"
                "}\n"
                "QPushButton:hover {\n"
                "    background-color: rgba(255, 122, 122, 50%);\n"
                "    color: rgb(255, 0, 0)\n"
                "}"
            )

        self.verticalLayout.addWidget(self.deleteBtn)
        self.gridLayout.addWidget(self.btnWidget, 1, 12, 6, 1)
        spacerItem3 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 7, 6, 1)
        spacerItem4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem4, 7, 4, 1, 9)
        self.serverName = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverName.sizePolicy().hasHeightForWidth())
        self.serverName.setSizePolicy(sizePolicy)
        self.serverName.setObjectName("serverName")

        self.gridLayout.addWidget(self.serverName, 1, 8, 1, 1)
        self.widget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setFixedSize(QSize(80, 80))
        self.widget.setObjectName("widget")

        self.gridLayout_3 = QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.Icon = PixmapLabel(self.widget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Icon.sizePolicy().hasHeightForWidth())
        self.Icon.setSizePolicy(sizePolicy)
        self.Icon.setObjectName("Icon")

        self.gridLayout_3.addWidget(self.Icon, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 1, 1, 2, 1)

        self.coreFileNameTitle.setText(self.tr("核心："))
        self.memTitle.setText(self.tr("内存设置："))
        self.javaPathTitle.setText(self.tr("Java："))
        self.selectBtn.setText(self.tr("选择"))
        self.editBtn.setText(self.tr("编辑"))
        self.deleteBtn.setText(self.tr("删除"))

        self.serverName.setWordWrap(True)

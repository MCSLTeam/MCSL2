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
Plugin page.
"""
from os import getcwd, remove, path as ospath
from shutil import copy
from zipfile import ZipFile

from PyQt5.QtCore import Qt, QSize, QRect, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QSizePolicy,
    QSpacerItem,
    QGridLayout,
    QWidget,
    QFrame,
    QVBoxLayout,
    QFileDialog,
)
from qfluentwidgets import (
    PrimaryPushButton,
    PushButton,
    SmoothScrollArea,
    StrongBodyLabel,
    TitleLabel,
    InfoBarPosition,
    InfoBar,
    FluentIcon as FIF
)

from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import GlobalMCSL2Variables


@Singleton
class PluginPage(QWidget):
    """插件页"""

    def __init__(self, parent=None):
        super().__init__(parent)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.installPluginBtn = PrimaryPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.installPluginBtn.sizePolicy().hasHeightForWidth()
        )
        self.installPluginBtn.setSizePolicy(sizePolicy)
        self.installPluginBtn.setMinimumSize(QSize(82, 32))
        self.installPluginBtn.setMaximumSize(QSize(82, 32))
        self.installPluginBtn.setObjectName("installPluginBtn")

        self.gridLayout.addWidget(self.installPluginBtn, 3, 4, 1, 1)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 2, 4, 1, 1)
        self.refreshPluginListBtn = PushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.refreshPluginListBtn.sizePolicy().hasHeightForWidth()
        )
        self.refreshPluginListBtn.setSizePolicy(sizePolicy)
        self.refreshPluginListBtn.setMinimumSize(QSize(82, 32))
        self.refreshPluginListBtn.setMaximumSize(QSize(82, 32))
        self.refreshPluginListBtn.setObjectName("refreshPluginListBtn")

        self.gridLayout.addWidget(self.refreshPluginListBtn, 4, 4, 1, 1)
        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.gridLayout_2 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.subTitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.gridLayout_2.addWidget(self.subTitleLabel, 1, 0, 1, 1)
        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayout_2.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.pluginsSmoothScrollArea = SmoothScrollArea(self.titleLimitWidget)
        self.pluginsSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.pluginsSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.pluginsSmoothScrollArea.setWidgetResizable(True)
        self.pluginsSmoothScrollArea.setObjectName("pluginsSmoothScrollArea")

        self.pluginsScrollAreaWidgetContents = QWidget()
        self.pluginsScrollAreaWidgetContents.setGeometry(QRect(0, 0, 544, 470))
        self.pluginsScrollAreaWidgetContents.setObjectName(
            "pluginsScrollAreaWidgetContents"
        )

        self.gridLayout_3 = QGridLayout(self.pluginsScrollAreaWidgetContents)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.pluginsVerticalLayout = QVBoxLayout()
        self.pluginsVerticalLayout.setObjectName("pluginsVerticalLayout")

        self.gridLayout_3.addLayout(self.pluginsVerticalLayout, 0, 0, 1, 1)
        self.pluginsSmoothScrollArea.setWidget(self.pluginsScrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.pluginsSmoothScrollArea, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 5, 2)
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 4, 1, 1)
        spacerItem3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 0, 2, 1, 1)
        spacerItem4 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 3, 5, 1, 1)

        self.setObjectName("PluginsInterface")

        self.pluginsSmoothScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )

        self.subTitleLabel.setText("添加属于你的插件，让你的MCSL2更加强大！")
        self.titleLabel.setText("插件")
        self.refreshPluginListBtn.setText("刷新")
        self.installPluginBtn.setText("安装")
        self.refreshPluginListBtn.setIcon(FIF.UPDATE)
        self.installPluginBtn.setIcon(FIF.ZIP_FOLDER)
        self.refreshPluginListBtn.clicked.connect(
            lambda: InfoBar.success(
                title="成功",
                content="刷新完毕",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM_LEFT,
                duration=2222,
                parent=self,
            )
        )
        self.installPluginBtn.clicked.connect(self.installPlugin)

    def installPlugin(self):
        GlobalMCSL2Variables.installingPluginArchiveDirectory = (
            str(QFileDialog.getOpenFileName(self, "选择.zip形式的插件", getcwd(), "*.zip")[
                0
            ]).replace("/", "\\")
        )
        if GlobalMCSL2Variables.installingPluginArchiveDirectory != "":
            self.installPluginThread = InstallPluginThread(self)
            self.installPluginThread.success.connect(
                lambda: InfoBar.success(
                    title="成功安装",
                    content=f"可能需要重启以生效",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_LEFT,
                    duration=3000,
                    parent=PluginPage(),
                )
            )
            self.installPluginThread.failed.connect(
                lambda: InfoBar.error(
                    title="安装失败",
                    content="",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_LEFT,
                    duration=3000,
                    parent=PluginPage(),
                )
            )
            self.installPluginThread.start()
            self.installPluginThread.finished.connect(self.refreshPluginListBtn.click)


class InstallPluginThread(QThread):
    success = pyqtSignal()
    failed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("InstallPluginThread")

    def run(self):
        try:
            pluginArchive = ZipFile(GlobalMCSL2Variables.installingPluginArchiveDirectory, "r")
            pluginArchive.extractall("./Plugins")
            pluginArchive.close()
            self.success.emit()
        except Exception as e:
            print(Exception().with_traceback())
            self.failed.emit()

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
Config Editor Widget
"""
from os import path as osp
from typing import Tuple, Dict, Optional

from PyQt5.QtCore import Qt, QSize, pyqtSlot
from PyQt5.QtWidgets import QWidget, QGridLayout, QSizePolicy, QFrame, QFileSystemModel
from qfluentwidgets import (
    TreeView,
    TabBar,
    PlainTextEdit,
    FluentIcon as FIF,
    InfoBarPosition,
    InfoBar,
    TabCloseButtonDisplayMode,
)

from MCSL2Lib.ProgramControllers.interfaceController import EraseStackedWidget

from MCSL2Lib.variables import ServerVariables


class ConfigEditorPage(QWidget):
    """
    Config Editor Page
    """

    def __init__(self, serverConfig: ServerVariables, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.serverConfig = serverConfig
        self.containerDict: Dict[str, QWidget] = dict()
        self.editorDict: Dict[str, PlainTextEdit] = dict()
        self.layout = QGridLayout(self)
        self.stackedWidget = EraseStackedWidget(self)
        self.tabBar = TabBar(self)
        self.treeView = TreeView(self)
        self.treeModel = QFileSystemModel()

        self.__initWidget()

    def __initWidget(self):
        self.tabBar.setAddButtonVisible(False)
        self.tabBar.setMovable(False)
        self.tabBar.setScrollable(True)
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        self.tabBar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabBar.hScrollBar.rangeChanged.connect(self.hScrollBarRangeChanged)

        self.treeModel.setRootPath("")
        self.treeModel.setNameFilters([
            "*.yml",
            "*.json",
            "*.conf",
            "*.ini",
            "*.properties",
            "*.xml",
            "*.yaml",
            "*.tmlp",
            "*.toml",
            "*.txt",
            "*.log",
            "*.sh",
            "*.bat",
            "*.cmd",
            "*.ps1",
            "*.psm1",
            "*.psd1",
            "*.ps1xml",
            "*.dsc",
            "*.dscx",
            "*.dscx12",
            "*.*.ps1xml",
        ])
        self.treeModel.setNameFilterDisables(False)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setMinimumSize(QSize(200, 0))
        self.treeView.setFrameShape(QFrame.NoFrame)
        self.treeView.setFrameShadow(QFrame.Plain)
        self.treeView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.treeView.setModel(self.treeModel)
        self.treeView.setRootIndex(
            self.treeModel.index(osp.abspath(f"Servers/{self.serverConfig.serverName}"))
        )
        self.treeView.setHeaderHidden(True)
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)
        self.treeView.selectionModel().selectionChanged.connect(self.createConfigEditor)
        self.tabBar.tabCloseRequested.connect(self.removeConfigEditor)

        self.__initLayout()

    def __initLayout(self):
        self.layout.addWidget(self.stackedWidget, 1, 1, 1, 1)
        self.layout.addWidget(self.tabBar, 0, 1, 1, 1)
        self.layout.addWidget(self.treeView, 0, 0, 2, 1)

    @pyqtSlot(tuple)
    def hScrollBarRangeChanged(self, range: Tuple[int, int]):
        """
        Only run When ScrollBar Range Changed(TabBar AddItem/RemoveItem over Focus Width)
        """
        scrollBar = self.tabBar.hScrollBar
        tab = self.tabBar.currentTab()
        if tab.pos().x() + tab.width() / 2 - scrollBar.value() > self.tabBar.width():
            scrollBar.scrollTo(scrollBar.maximum(), useAni=False)

    def createConfigEditor(self, selected, deselected):
        filePath = self.treeModel.filePath(selected.indexes()[0]).replace("\\", "/")  # type: str
        if osp.isdir(filePath):
            return
        if filePath in self.tabBar.itemMap:  # Select Existing Tab
            tab = self.tabBar.tab(filePath)
            tab.pressed.emit()  # Select Tab
            self.tabBar.hScrollBar.scrollTo(tab.pos().x(), useAni=False)  # Auto Scroll To The Select Tab
            return
        else:  # Add New Tab
            try:
                with open(filePath, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception as e:
                InfoBar.info(
                    title="抱歉",
                    content=f"MCSL2无法打开此文件，原因：\n{e.with_traceback(None)}",
                    orient=Qt.Horizontal,
                    parent=self,
                    duration=1500,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                )
                return

            fileName = osp.basename(filePath)
            container = QWidget()
            containerLayout = QGridLayout(container)
            containerLayout.addWidget((p := PlainTextEdit(container)), 0, 0)
            p.setPlainText(text)
            self.stackedWidget.addWidget(container)
            self.tabBar.addTab(
                routeKey=filePath,
                text=fileName,
                icon=FIF.LABEL,
                onClick=lambda: self.stackedWidget.setCurrentWidget(container),
            )
            self.tabBar.setCurrentTab(filePath)
            self.stackedWidget.setCurrentWidget(container)
            self.containerDict[filePath] = container
            self.editorDict[filePath] = p

    @pyqtSlot(int)
    def removeConfigEditor(self, i: int):
        routeKey = self.tabBar.items[i].routeKey()  # type: str
        with open(routeKey, "r", encoding="utf-8") as f:
            tmpText = f.read()
        if (newText := self.editorDict[routeKey].toPlainText()) != tmpText:
            with open(routeKey, "w+", encoding="utf-8") as nf:
                nf.write(newText)

            InfoBar.info(
                title="提示",
                content=f"已自动保存{routeKey}",
                orient=Qt.Horizontal,
                parent=self,
                duration=1500,
                isClosable=False,
                position=InfoBarPosition.TOP,
            )

        self.stackedWidget.removeWidget(self.containerDict[routeKey])
        self.editorDict.pop(routeKey)
        self.containerDict.pop(routeKey)
        self.tabBar.removeTab(i)

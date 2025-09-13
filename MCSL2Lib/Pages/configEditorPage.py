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

from PyQt5.QtCore import Qt, QSize, pyqtSlot, QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSizePolicy,
    QFrame,
    QFileSystemModel,
    QApplication,
)
from qfluentwidgets import (
    TreeView,
    TabBar,
    PlainTextEdit,
    FluentIcon as FIF,
    InfoBarPosition,
    InfoBar,
    TabCloseButtonDisplayMode,
    TabItem,
)

from MCSL2Lib.ProgramControllers.interfaceController import EraseStackedWidget
from MCSL2Lib.utils import readFile, writeFile
from MCSL2Lib.variables import ServerVariables


class CtrlSPlainTextEdit(PlainTextEdit):
    ctrlSPressed = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.ctrlSPressed.emit()
                return
        super().keyPressEvent(event)


def addFileChange(tab: TabItem):
    if tab.text()[-1:] != "*":
        tab.setText(tab.text() + "*")


def clearFileChange(tab: TabItem):
    if tab.text()[-1:] == "*":
        tab.setText(tab.text()[:-1])


class ConfigEditorPage(QWidget):
    """
    `编辑配置文件` 页面
    """

    def __init__(self, serverConfig: ServerVariables, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.serverConfig = serverConfig
        self.containerDict: Dict[str, QWidget] = dict()
        """标签页中的编辑控件存储器"""
        self.editorDict: Dict[str, CtrlSPlainTextEdit] = dict()
        """标签页中的编辑框存储器"""
        self.layout = QGridLayout(self)
        self.stackedWidget = EraseStackedWidget(self)
        self.tabBar = TabBar(self)
        """标签页"""
        self.treeView = TreeView(self)
        """文件树"""
        self.treeModel = QFileSystemModel()
        """文件树Model"""
        self.autoSaveTimer = QTimer(self)
        """自动保存计时器"""
        self.autoSaveInterval = 60
        """自动保存间隔时间,单位:秒"""

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
        self.tabBar.currentChanged.connect(self.configTabSelectChanged)
        self.autoSaveTimer.setSingleShot(False)
        self.autoSaveTimer.timeout.connect(self.autoSaveConfig)

        self.__initLayout()

    def __initLayout(self):
        self.layout.addWidget(self.stackedWidget, 1, 1, 1, 1)
        self.layout.addWidget(self.tabBar, 0, 1, 1, 1)
        self.layout.addWidget(self.treeView, 0, 0, 2, 1)

    @pyqtSlot(int)
    def configTabSelectChanged(self, index: int):
        self.reloadTimer()

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
        if not selected.indexes():
            return
        filePath = (
            self.treeView.selectionModel()
            .model()
            .filePath(selected.indexes()[0])
            .replace("\\", "/")
        )  # type: str
        self.treeView.selectionModel().clearSelection()
        if osp.isdir(filePath):
            return
        if filePath in self.tabBar.itemMap:  # Select Existing Tab
            tab = self.tabBar.tab(filePath)
            tab.pressed.emit()  # Select Tab
            self.tabBar.hScrollBar.scrollTo(
                tab.pos().x(), useAni=False
            )  # Auto Scroll To The Select Tab
            return
        else:  # Add New Tab
            try:
                text = readFile(filePath)
            except Exception as e:
                InfoBar.info(
                    title=self.tr("抱歉"),
                    content=self.tr("MCSL2 无法打开此文件，原因：\n") + str(e.with_traceback(None)),
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
            containerLayout.addWidget((p := CtrlSPlainTextEdit(container)), 0, 0)
            p.setPlainText(text)
            p.ctrlSPressed.connect(lambda: self.autoSaveConfig(False))
            self.stackedWidget.addWidget(container)
            tab = self.tabBar.addTab(
                routeKey=filePath,
                text=fileName,
                icon=FIF.LABEL,
                onClick=lambda: self.stackedWidget.setCurrentWidget(container),
            )
            p.textChanged.connect(lambda: addFileChange(tab))
            self.tabBar.setCurrentTab(filePath)
            self.stackedWidget.setCurrentWidget(container)
            self.containerDict[filePath] = container
            self.editorDict[filePath] = p
            self.tabBar.currentChanged.emit(
                self.tabBar.currentIndex()
            )  # 新建标签页不触发currentChanged,这里手动触发

    def saveConfig(self, filePath: str, auto: bool = True):
        tmpText = readFile(filePath)
        if (newText := self.editorDict[filePath].toPlainText()) != tmpText:
            writeFile(filePath, newText)
            InfoBar.info(
                title=self.tr("提示"),
                content=self.tr("已保存 ") + osp.basename(filePath),
                orient=Qt.Horizontal,
                parent=self,
                duration=1500,
                isClosable=False,
                position=InfoBarPosition.TOP,
            )
        # else:
        #     MCSL2Logger.debug(f"{filePath}未修改,无需保存")

    def autoSaveConfig(self, auto: bool = True):
        if tab := self.tabBar.currentTab():
            self.saveConfig(tab.routeKey(), auto)
            clearFileChange(tab)

    @pyqtSlot(int)
    def removeConfigEditor(self, i: int):
        routeKey = self.tabBar.items[i].routeKey()  # type: str
        self.saveConfig(routeKey)

        self.stackedWidget.removeWidget(self.containerDict[routeKey])
        self.editorDict.pop(routeKey)
        self.containerDict.pop(routeKey)
        self.tabBar.removeTab(i)

    def reloadTimer(self):
        self.autoSaveTimer.stop()
        self.autoSaveTimer.start(self.autoSaveInterval * 1000)

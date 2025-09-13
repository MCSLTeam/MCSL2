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
Download Entry Viewer Widget
"""

import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QSizePolicy
from qfluentwidgets import MessageBoxBase, SubtitleLabel, TableWidget

from MCSL2Lib.ProgramControllers.aria2ClientController import DL_EntryController


class DownloadEntryModel(QAbstractListModel):
    def __init__(self):
        super().__init__()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        pass


class DownloadEntryBox(MessageBoxBase):
    onClosed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setMinimumSize(QSize(600, 0))
        self.setMaximumSize(QSize(16777215, 16777215))
        self.titleLabel = SubtitleLabel(self.tr("下载项 (正在加载...)"), self)
        self.entryView = TableWidget(self)
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.entryView)

        self.widget.setMinimumSize(QSize(620, 300))
        self.widget.setMaximumSize(QSize(16777215, 16777215))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)

        self.entryView.itemSelectionChanged.connect(self.onItemSelectionChanged)
        self.entryView.doubleClicked.connect(self.yesButton.click)
        self.entryView.setColumnCount(4)
        self.columnSortOrder = [True] * 5

        self.entryView.setHorizontalHeaderLabels([
            self.tr("名称"),
            self.tr("类型"),
            self.tr("MC 版本"),
            self.tr("构建版本"),
        ])
        self.entryView.verticalHeader().hide()
        self.entryView.setWordWrap(False)
        self.entryView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.entryView.setMinimumSize(QSize(620, 300))
        self.entryView.setMaximumSize(QSize(16777215, 16777215))
        self.entryView.setEditTriggers(self.entryView.NoEditTriggers)
        self.entryView.setSelectionBehavior(self.entryView.SelectRows)
        self.entryView.setSelectionMode(self.entryView.SingleSelection)
        self.entryView.horizontalHeader().sectionClicked.connect(self.onSectionClicked)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entryView.sizePolicy().hasHeightForWidth())
        self.entryView.setSizePolicy(sizePolicy)
        self.entryView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.yesButton.setText(self.tr("选择"))
        self.cancelButton.setText(self.tr("取消"))

        self.__lastSelection = []

        self.yesButton.setDisabled(True)

    def asyncGetEntries(self):
        (controller := DL_EntryController()).resultReady.connect(self.updateEntries)
        controller.work.emit(("getEntriesList", {"check": True, "autoDelete": False}))

    def getSelectedEntry(self):
        return self.__lastSelection.copy()

    def onItemSelectionChanged(self):
        self.yesButton.setEnabled(True)
        self.__lastSelection = [e.text() for e in self.entryView.selectedItems()]

    def closeEvent(self, e):
        self.onClosed.emit(self.__lastSelection)
        return super().closeEvent(e)

    def updateEntries(self, entries: typing.List[typing.Dict]):
        entries.sort(key=lambda x: x.get("mc_version"), reverse=True)
        self.entryView.setRowCount(len(entries))
        for i, coreInfo in enumerate(entries):
            name = QTableWidgetItem(coreInfo.get("name"))
            type_ = QTableWidgetItem(coreInfo.get("type"))
            mcVersion = QTableWidgetItem(coreInfo.get("mc_version"))
            buildVersion = QTableWidgetItem(coreInfo.get("build_version"))

            self.entryView.setItem(i, 0, name)
            self.entryView.setItem(i, 1, type_)
            self.entryView.setItem(i, 2, mcVersion)
            self.entryView.setItem(i, 3, buildVersion)
        self.entryView.resizeRowsToContents()
        self.yesButton.setDisabled(True)
        self.titleLabel.setText(self.tr("下载项 (共 ") + str(len(entries)) + self.tr(" 项)"))

    def onSectionClicked(self, index: int):
        self.entryView.horizontalHeader().setSortIndicatorShown(True)
        if self.columnSortOrder[index]:
            self.entryView.horizontalHeader().setSortIndicator(index, Qt.DescendingOrder)
            self.entryView.sortItems(index, Qt.DescendingOrder)
            self.columnSortOrder[index] = not self.columnSortOrder[index]
        else:
            self.entryView.horizontalHeader().setSortIndicator(index, Qt.AscendingOrder)
            self.entryView.sortItems(index, Qt.AscendingOrder)
            self.columnSortOrder[index] = not self.columnSortOrder[index]

    @property
    def lastSelection(self):
        return self.__lastSelection.copy()

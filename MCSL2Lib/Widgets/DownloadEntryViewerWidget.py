import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QSize
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QSizePolicy
from qfluentwidgets import MessageBoxBase, SubtitleLabel, TableWidget

from MCSL2Lib.Controllers.aria2ClientController import DL_EntryController


class DownloadEntryModel(QAbstractListModel):
    def __init__(self):
        super().__init__()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        pass


class DownloadEntryBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(QSize(600, 0))
        self.setMaximumSize(QSize(16777215, 16777215))
        self.titleLabel = SubtitleLabel("下载项(正在加载...)", self)
        self.entryView = TableWidget(self)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.entryView)

        self.entryView.setWordWrap(False)
        self.entryView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.widget.setMinimumSize(QSize(620, 300))
        self.widget.setMaximumSize(QSize(16777215, 16777215))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)

        self.entryView.setMinimumSize(QSize(620, 300))
        self.entryView.setMaximumSize(QSize(16777215, 16777215))

        (controller := DL_EntryController()).resultReady.connect(self.updateEntries)
        controller.work.emit(("getEntriesList", {"check": True, "autoDelete": False}))

        self.entryView.setEditTriggers(self.entryView.NoEditTriggers)
        self.entryView.setSelectionBehavior(self.entryView.SelectRows)
        self.entryView.setSelectionMode(self.entryView.SingleSelection)
        self.entryView.horizontalHeader().sectionClicked.connect(self.onSectionClicked)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entryView.sizePolicy().hasHeightForWidth())
        self.entryView.setSizePolicy(sizePolicy)

        self.entryView.itemSelectionChanged.connect(
            lambda: self.yesButton.setEnabled(True)
        )
        self.entryView.doubleClicked.connect(lambda: self.accept())
        self.entryView.setColumnCount(4)
        self.columnSortOrder = [True] * 5

        self.entryView.setHorizontalHeaderLabels(["名称", "类型", "MC版本", "构建版本"])
        self.entryView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.yesButton.setText("选择")
        self.cancelButton.setText("取消")

        self.yesButton.setDisabled(True)

    def getSelectedEntry(self):
        return list(map(lambda x: x.text(), self.entryView.selectedItems()))

    def updateEntries(self, entries: typing.List[typing.Dict]):
        entries.sort(key=lambda x: x.get("mc_version"), reverse=True)

        self.entryView.setRowCount(len(entries))

        for i, coreInfo in enumerate(entries):
            self.entryView.setItem(i, 0, QTableWidgetItem(coreInfo.get("name")))
            self.entryView.setItem(i, 1, QTableWidgetItem(coreInfo.get("type")))
            self.entryView.setItem(i, 2, QTableWidgetItem(coreInfo.get("mc_version")))
            self.entryView.setItem(
                i, 3, QTableWidgetItem(coreInfo.get("build_version"))
            )
        self.entryView.verticalHeader().hide()
        self.entryView.setHorizontalHeaderLabels(["名称", "类型", "MC版本", "构建版本"])

        if self.entryView.rowCount() != 0:  # resize header view
            self.entryView.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.ResizeToContents
            )
            self.entryView.resizeRowsToContents()
        self.yesButton.setDisabled(True)
        self.titleLabel.setText(f"下载项(共{len(entries)}项)")

    def onSectionClicked(self, index: int):
        self.entryView.horizontalHeader().setSortIndicatorShown(True)
        if self.columnSortOrder[index]:
            self.entryView.horizontalHeader().setSortIndicator(
                index, Qt.DescendingOrder
            )
            self.entryView.sortItems(index, Qt.DescendingOrder)
            self.columnSortOrder[index] = not self.columnSortOrder[index]
        else:
            self.entryView.horizontalHeader().setSortIndicator(index, Qt.AscendingOrder)
            self.entryView.sortItems(index, Qt.AscendingOrder)
            self.columnSortOrder[index] = not self.columnSortOrder[index]

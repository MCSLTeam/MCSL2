import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex
from PyQt5.QtWidgets import QTableWidgetItem
from qfluentwidgets import MessageBoxBase, SubtitleLabel, TableWidget

from MCSL2Lib.Controllers.aria2ClientController import DL_EntryManager


class DownloadEntryModel(QAbstractListModel):
    def __init__(self):
        super().__init__()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        pass


class DownloadEntryBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('下载项', self)
        self.entryView = TableWidget(self)

        self.entryView.setWordWrap(False)
        self.updateEntries()

        self.entryView.verticalHeader().hide()
        self.entryView.setHorizontalHeaderLabels(['名称', '类型', 'MC版本', '构建版本'])
        self.entryView.resizeColumnsToContents()

        self.entryView.setEditTriggers(self.entryView.NoEditTriggers)
        self.entryView.setSelectionBehavior(self.entryView.SelectRows)
        self.entryView.setSelectionMode(self.entryView.SingleSelection)

        self.entryView.itemSelectionChanged.connect(lambda: self.yesButton.setEnabled(True))

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.entryView)

        self.yesButton.setText('选择')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(600)
        self.widget.setMinimumHeight(600)
        self.widget.setContentsMargins(0, 0, 0, 0)
        # self.widget.setStyleSheet('MessageBoxBase{background:rgb(32,32,32)}')

    def getSelectedEntry(self):
        return list(map(lambda x: x.text(), self.entryView.selectedItems()))

    def updateEntries(self):
        entries = DL_EntryManager.getEntriesList()
        self.entryView.setRowCount(len(entries))
        self.entryView.setColumnCount(4)

        for i, coreInfo in enumerate(entries):
            self.entryView.setItem(i, 0, QTableWidgetItem(coreInfo.get('name')))
            self.entryView.setItem(i, 1, QTableWidgetItem(coreInfo.get('type')))
            self.entryView.setItem(i, 2, QTableWidgetItem(coreInfo.get('mc_version')))
            self.entryView.setItem(i, 3, QTableWidgetItem(coreInfo.get('build_version')))

        self.yesButton.setDisabled(True)

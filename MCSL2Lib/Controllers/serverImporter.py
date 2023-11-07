from typing import List
from PyQt5.QtCore import QObject
from MCSL2Lib.Widgets.importServerWidgets import (
    ImportPageWidget,
    ConfirmArgumentsWidget,
    ImportFileFolderWidget,
    ImportSingleWidget,
    ListWidget,
    SaveWidget,
)
from PyQt5.QtWidgets import QStackedWidget


class ServerImporter(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pageWidget = ImportPageWidget(parent)
        self.totalStep = 0

    def initStep(self):
        raise NotImplementedError

    def setTypeName(self, name: str):
        self.pageWidget.__setTypeName(name)

    def addThisImportType(self):
        parent = self.parent()  # type: QStackedWidget
        parent.addWidget(self.pageWidget)

    def addTypeWidget(self, w):
        self.pageWidget.typeWidgetLayout.addWidget(w)

    def initImportFileFolderWidget(self) -> ImportFileFolderWidget:
        self.totalStep += 1
        return ImportFileFolderWidget(self.totalStep)

    def initImportSingleWidget(
        self,
        title: str = "",
        btnText: str = "",
    ) -> ImportSingleWidget:
        self.totalStep += 1
        return ImportSingleWidget(self.totalStep, title, btnText)

    def initListWidget(self, title: str = "选择") -> ListWidget:
        self.totalStep += 1
        return ListWidget(self.totalStep, title)

    def initConfirmArgumentsWidget(self) -> ConfirmArgumentsWidget:
        self.totalStep += 1
        return ConfirmArgumentsWidget(self.totalStep)

    def initSaveWidget(self) -> SaveWidget:
        self.totalStep += 1
        return SaveWidget(self.totalStep)


class NoShellArchivesImporter(ServerImporter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTypeName("导入不含开服脚本的完整服务器压缩包")

    def initStep(self):
        self.importWidget = self.initImportSingleWidget("导入服务器压缩包")
        self.addTypeWidget(self.importWidget)
        self.selectWidget = self.initListWidget("选择核心")
        self.addTypeWidget(self.selectWidget)
        self.confirmWidget = self.initConfirmArgumentsWidget()
        self.addTypeWidget(self.confirmWidget)
        self.saveWidget = self.initSaveWidget()
        self.addTypeWidget(self.saveWidget)

    def connectSlot(self):
        self.pageWidget.connectBackSlot(lambda: self.parent().setCurrentIndex(0))


class ShellArchivesImporter(ServerImporter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTypeName("导入含开服脚本的完整服务器压缩包")

    def initStep(self):
        self.importWidget = self.initImportSingleWidget("导入服务器压缩包")
        self.addTypeWidget(self.importWidget)
        self.selectWidget = self.initListWidget("选择开服脚本")
        self.addTypeWidget(self.selectWidget)
        self.confirmWidget = self.initConfirmArgumentsWidget()
        self.addTypeWidget(self.confirmWidget)
        self.saveWidget = self.initSaveWidget()
        self.addTypeWidget(self.saveWidget)

    def connectSlot(self):
        self.pageWidget.connectBackSlot(lambda: self.parent().setCurrentIndex(0))
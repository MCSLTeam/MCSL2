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

    def addThisImportType(self):
        parent = self.parent() # type: QStackedWidget
        parent.addWidget(self.pageWidget)

    def addTypeWidget(self, w):
        self.pageWidget.typeWidgetLayout.addWidget(w)

    def initImportFileFolderWidget(self, stepCount: int = 0) -> ImportFileFolderWidget:
        return ImportFileFolderWidget(stepCount)

    def initImportSingleWidget(
        self,
        stepCount: int = 0,
        title: str = "",
        btnText: str = "",
    ) -> ImportSingleWidget:
        return ImportSingleWidget(stepCount, title, btnText)

    def initListWidget(self, stepCount: int=0) -> ListWidget:
        return ListWidget(stepCount)

    def initConfirmArgumentsWidget(
        self,
        stepCount: int = 0,
        javaPath: str = "",
        minMem=0,
        maxMem=0,
        outputCoding: str = "",
        inputCoding: str = "",
        jvmArg: List[str] = [],
    ) -> ConfirmArgumentsWidget:
        return ConfirmArgumentsWidget(
            stepCount,
            javaPath,
            minMem,
            maxMem,
            outputCoding,
            inputCoding,
            jvmArg,
        )

    def initSaveWidget(self, stepCount: int=0) -> SaveWidget:
        return SaveWidget(stepCount)
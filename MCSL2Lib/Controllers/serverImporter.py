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
Server Importer
"""

from zipfile import ZipFile
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QStackedWidget  # noqa: F401
from MCSL2Lib.Widgets.importServerWidgets import (
    ImportPageWidget,
    ConfirmArgumentsWidget,
    ImportFileFolderWidget,
    ImportSingleWidget,
    MyListWidget,
    MyTreeWidget,
    SaveWidget,
)
from qfluentwidgets import CardWidget


class BaseServerImporter(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pageWidget = ImportPageWidget(parent)
        self.totalStep = 0

    def initStep(self):
        raise NotImplementedError

    def setTypeName(self, name: str):
        self.pageWidget._setTypeName(name)

    def addThisImportType(self):
        parent = self.parent()  # type: QStackedWidget
        parent.addWidget(self.pageWidget)

    def addTypeWidget(self, w: CardWidget):
        if self.totalStep > 1:
            w.setEnabled(False)
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

    def initMyListWidget(self, title: str = "选择") -> MyListWidget:
        self.totalStep += 1
        return MyListWidget(self.totalStep, title)

    def initMyTreeWidget(self, title: str = "选择") -> MyTreeWidget:
        self.totalStep += 1
        return MyTreeWidget(self.totalStep, title)

    def initConfirmArgumentsWidget(self, title: str = "设置参数") -> ConfirmArgumentsWidget:
        self.totalStep += 1
        return ConfirmArgumentsWidget(self.totalStep, title)

    def initSaveWidget(self) -> SaveWidget:
        self.totalStep += 1
        return SaveWidget(self.totalStep)


class NoShellArchivesImporter(BaseServerImporter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTypeName("导入不含开服脚本的完整服务器压缩包")
        self.initStep()
        self.connectSlot()
        self.addThisImportType()

    def initStep(self):
        self.importWidget = self.initImportSingleWidget("导入服务器压缩包", "选择文件")
        self.addTypeWidget(self.importWidget)
        self.selectWidget = self.initMyTreeWidget("选择核心")
        self.addTypeWidget(self.selectWidget)
        self.confirmWidget = self.initConfirmArgumentsWidget("设置更多参数")
        self.addTypeWidget(self.confirmWidget)
        self.saveWidget = self.initSaveWidget()
        self.addTypeWidget(self.saveWidget)

    def connectSlot(self):
        # fmt: off
        self.pageWidget.connectBackSlot(lambda: self.parent().setCurrentIndex(0))

        self.importWidget.fileImportedSignal.connect(self.initFileListView)

        self.importWidget.finishSignal.connect(self.selectWidget.setEnabled)
        self.selectWidget.finishSignal.connect(self.confirmWidget.setEnabled)
        self.confirmWidget.finishSignal.connect(self.saveWidget.setEnabled)
        # fmt: on

    @pyqtSlot(str)
    def initFileListView(self, file: str):
        self.selectWidget.createZipTree(zipFile=ZipFile(file, mode="r"), supportExt="jar")


# class ShellArchivesImporter(ServerImporter):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setTypeName("导入含开服脚本的完整服务器压缩包")
#         self.initStep()
#         self.connectSlot()
#         self.addThisImportType()

#     def initStep(self):
#         self.importWidget = self.initImportSingleWidget("导入服务器压缩包", "选择文件")
#         self.addTypeWidget(self.importWidget)
#         self.selectWidget = self.initListWidget("选择开服脚本")
#         self.addTypeWidget(self.selectWidget)
#         self.confirmWidget = self.initConfirmArgumentsWidget()
#         self.addTypeWidget(self.confirmWidget)
#         self.saveWidget = self.initSaveWidget()
#         self.addTypeWidget(self.saveWidget)

#     def connectSlot(self):
#         self.pageWidget.connectBackSlot(lambda: self.parent().setCurrentIndex(0))

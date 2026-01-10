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
Forge Install Progress Widget
"""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy
from qfluentwidgets import MessageBoxBase, SubtitleLabel, SmoothScrollArea

from .DownloadEntryWidget import DownloadEntryWidget


class EntryScrollArea(SmoothScrollArea):
    empty = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self settings
        self.viewport().setStyleSheet("background-color: transparent;")
        self.resize(DownloadEntryWidget.WIDTH + 10, self.height())
        self.setFrameShape(QFrame.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setWidgetResizable(True)

        self.area = QWidget(self)
        self.area.setLayout(QVBoxLayout(self.area))

        self.areaContent = QWidget(self.area)

        self.area.layout().addWidget(self.areaContent)
        # vertical spacer
        self.area.layout().addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        widgetLayout = QVBoxLayout(self.areaContent)
        self.areaContent.setLayout(widgetLayout)

        self.setWidget(self.area)

    def append(self, widget):
        self.areaContent.layout().addWidget(widget)
        self.update()

    def remove(self, widget):
        self.areaContent.layout().removeWidget(widget)
        self.update()
        if self.areaContent.layout().count() == 0:
            self.empty.emit()


class ForgeInstallerDownloadView(MessageBoxBase):
    allDone = pyqtSignal()

    def __init__(self, parent=None, title: str = None):
        super().__init__(parent)
        # 使用传入的 title，如果没有则默认为 "Forge Installer"
        if title is None:
            title = self.tr("Forge Installer")
        self.titleLabel = SubtitleLabel(title, self)
        self.scrollArea = EntryScrollArea(self)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.scrollArea)

        self.cancelButton.setText(self.tr("取消安装"))
        self.yesButton.setText(self.tr("隐藏"))

        self.widget.setMinimumWidth(500)
        self.widget.setMinimumHeight(600)
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.yesButton.clicked.connect(self.hide)

        self.widgetMap = {}

    def onProgress(self, filename, progress, speed, done, allDone):
        if filename not in self.widgetMap:
            w = DownloadEntryWidget.getWidget(filename, self)
            self.widgetMap[filename] = w

            # add to scroll area
            self.scrollArea.append(w)
        else:
            w = self.widgetMap[filename]

        w.setSpeed(speed)
        w.setProgress(progress)

        if done:
            # remove from scroll area
            self.scrollArea.remove(w)
            del self.widgetMap[filename]
            w.deleteLater()

        if allDone:
            self.allDone.emit()

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
Forge Install Progress Widget
"""
from PyQt5.QtCore import pyqtSignal
from qfluentwidgets import MessageBoxBase, SubtitleLabel, PlainTextEdit


class ForgeInstallerProgressBox(MessageBoxBase):
    def __init__(self, textSignal: pyqtSignal, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr("Forge安装器(正在安装...)"), self)
        self.forgeLogViewer = PlainTextEdit(self)
        self.forgeLogViewer.setMaximumBlockCount(1000)
        self.textSignal = textSignal
        self.textSignal.connect(self.forgeLogViewer.appendPlainText)
        self.forgeLogViewer.setReadOnly(True)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.forgeLogViewer)

        self.cancelButton.setText(self.tr("取消安装"))
        self.yesButton.setText(self.tr("隐藏"))

        self.widget.setMinimumWidth(550)
        self.widget.setMinimumHeight(600)
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.yesButton.clicked.connect(self.hide)
        # self.yesButton.setDisabled(True)

    def __del__(self):
        self.textSignal.disconnect(self.forgeLogViewer.appendPlainText)

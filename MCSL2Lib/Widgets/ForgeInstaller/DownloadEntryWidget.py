# -*- coding: utf-8 -*-
from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QWidget

from qfluentwidgets import (CardWidget, ProgressBar, StrongBodyLabel)


class DownloadEntryWidget(CardWidget):
    WIDTH = 300

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(DownloadEntryWidget.WIDTH, 50)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.CardWidget = self

        self.CardWidget.setObjectName(u"CardWidget")
        self.verticalLayout = QVBoxLayout(self.CardWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.name = StrongBodyLabel(self.CardWidget)
        self.name.setObjectName(u"name")

        self.horizontalLayout_2.addWidget(self.name)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.speed = StrongBodyLabel(self.CardWidget)
        self.speed.setObjectName(u"progressText")

        self.horizontalLayout_2.addWidget(self.speed)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.bar = ProgressBar(self.CardWidget)
        self.bar.setObjectName(u"bar")

        self.horizontalLayout_3.addWidget(self.bar)

        self.percent = StrongBodyLabel(self.CardWidget)
        self.percent.setObjectName(u"StrongBodyLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.percent.sizePolicy().hasHeightForWidth())
        self.percent.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.percent)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.translateUi(self)

    def translateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.name.setText(QCoreApplication.translate("Frame", u"\u6587\u4ef6\u540d", None))
        self.speed.setText(QCoreApplication.translate("Frame", u"100KB/s", None))
        self.percent.setText(QCoreApplication.translate("Frame", u"100%", None))

    def setSpeed(self, speed: int) -> None:
        """
        speed: xxx KB/s
        """

        self.speed.setText(f"{speed} KB/s")

    def setProgress(self, progress: int) -> None:
        """
        progress ∈ [0,100]
        """
        self.bar.setValue(progress)
        self.bar.update()
        self.percent.setText(f"{progress}%")

    @staticmethod
    def getWidget(name: str, parent=None) -> 'DownloadEntryWidget':
        widget = DownloadEntryWidget(parent)
        widget.name.setText(name)
        widget.setSpeed(0)
        widget.setProgress(0)
        return widget

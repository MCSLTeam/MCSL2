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
A single widget template of plugin.
"""

from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QSpacerItem
from qfluentwidgets import (
    BodyLabel,
    SimpleCardWidget,
    PixmapLabel,
    StrongBodyLabel,
    SwitchButton,
    TransparentToolButton,
    FluentIcon as FIF,
    IconWidget,
)
from PyQt5.QtGui import QPixmap


class PluginSwitchButton(SwitchButton):
    selfCheckedChanged = pyqtSignal(SwitchButton, bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checkedChanged.connect(self.onCheckedChanged)

    def onCheckedChanged(self, checked):
        self.selfCheckedChanged.emit(self, checked)


class PluginOperationButton(TransparentToolButton):
    selfClicked = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.onClicked)

    def onClicked(self):
        self.selfClicked.emit(self.objectName().split("Btn_")[1])


class singlePluginWidget(SimpleCardWidget):
    """单独的插件Widget模板"""

    def __init__(self, icon: str = None):
        super().__init__()

        self.setObjectName("singlePluginWidget")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(524, 150))
        self.setMaximumSize(QSize(16777215, 150))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        isFIF = icon.startswith("FIF.") or icon.startswith("FluentIcon.")
        self.pluginIcon = PixmapLabel(self) if not isFIF else IconWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pluginIcon.sizePolicy().hasHeightForWidth())
        self.pluginIcon.setSizePolicy(sizePolicy)
        self.pluginIcon.setMinimumSize(QSize(60, 60))
        self.pluginIcon.setMaximumSize(QSize(60, 60))
        self.pluginIcon.setObjectName("pluginIcon")

        self.horizontalLayout.addWidget(self.pluginIcon)
        spacerItem1 = QSpacerItem(15, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pluginInfoWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pluginInfoWidget.sizePolicy().hasHeightForWidth())
        self.pluginInfoWidget.setSizePolicy(sizePolicy)
        self.pluginInfoWidget.setMinimumSize(QSize(0, 120))
        self.pluginInfoWidget.setMaximumSize(QSize(16777215, 120))
        self.pluginInfoWidget.setObjectName("pluginInfoWidget")

        self.verticalLayout = QVBoxLayout(self.pluginInfoWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.pluginName = StrongBodyLabel(self.pluginInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pluginName.sizePolicy().hasHeightForWidth())
        self.pluginName.setSizePolicy(sizePolicy)
        self.pluginName.setObjectName("pluginName")

        self.verticalLayout.addWidget(self.pluginName)
        self.pluginVer = BodyLabel(self.pluginInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pluginVer.sizePolicy().hasHeightForWidth())
        self.pluginVer.setSizePolicy(sizePolicy)
        self.pluginVer.setObjectName("pluginVer")

        self.verticalLayout.addWidget(self.pluginVer)
        self.pluginAuthor = BodyLabel(self.pluginInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pluginAuthor.sizePolicy().hasHeightForWidth())
        self.pluginAuthor.setSizePolicy(sizePolicy)
        self.pluginAuthor.setObjectName("pluginAuthor")

        self.verticalLayout.addWidget(self.pluginAuthor)
        self.pluginTip = BodyLabel(self.pluginInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pluginTip.sizePolicy().hasHeightForWidth())
        self.pluginTip.setSizePolicy(sizePolicy)
        self.pluginTip.setObjectName("pluginTip")

        self.verticalLayout.addWidget(self.pluginTip)
        self.horizontalLayout.addWidget(self.pluginInfoWidget)
        self.SwitchButton = PluginSwitchButton(self)
        self.horizontalLayout.addWidget(self.SwitchButton)
        self.openFolderButton = PluginOperationButton(FIF.FOLDER, self)
        self.openFolderButton.setObjectName("openFolderButton")

        self.horizontalLayout.addWidget(self.openFolderButton)
        self.deleteBtn = PluginOperationButton(FIF.DELETE, self)
        self.deleteBtn.setObjectName("deleteBtn")
        self.SwitchButton.setOffText("")
        self.SwitchButton.setOnText("")
        self.SwitchButton.setText("")
        self.horizontalLayout.addWidget(self.deleteBtn)

    def setPluginIcon(self, icon):
        if type(self.pluginIcon) is PixmapLabel:
            self.pluginIcon.setPixmap(QPixmap(icon))
        else:
            self.pluginIcon.setIcon(icon)

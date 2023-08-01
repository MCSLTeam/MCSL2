#     Copyright 2023, MCSL Team, mailto:lxhtz.dl@qq.com
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
'''
A single widget template of plugin.
'''

from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QSpacerItem
from PyQt5.QtCore import QSize

from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    PixmapLabel,
    StrongBodyLabel,
    SwitchButton,
    TransparentToolButton,
)


class singlePluginWidget(CardWidget):
    """单独的插件Widget模板"""

    def __init__(self):
        super().__init__()

        self.setObjectName("singlePluginWidget")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(524, 100))
        self.setMaximumSize(QSize(16777215, 100))
        self.setWindowTitle("")
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pluginIcon = PixmapLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pluginIcon.sizePolicy().hasHeightForWidth())
        self.pluginIcon.setSizePolicy(sizePolicy)
        self.pluginIcon.setMinimumSize(QSize(50, 50))
        self.pluginIcon.setMaximumSize(QSize(50, 50))
        self.pluginIcon.setObjectName("pluginIcon")

        self.horizontalLayout.addWidget(self.pluginIcon)
        self.pluginInfoWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pluginInfoWidget.sizePolicy().hasHeightForWidth()
        )
        self.pluginInfoWidget.setSizePolicy(sizePolicy)
        self.pluginInfoWidget.setMinimumSize(QSize(0, 75))
        self.pluginInfoWidget.setMaximumSize(QSize(16777215, 75))
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
        self.pluginMoreInfo = BodyLabel(self.pluginInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pluginMoreInfo.sizePolicy().hasHeightForWidth()
        )
        self.pluginMoreInfo.setSizePolicy(sizePolicy)
        self.pluginMoreInfo.setObjectName("pluginMoreInfo")

        self.verticalLayout.addWidget(self.pluginMoreInfo)
        self.horizontalLayout.addWidget(self.pluginInfoWidget)
        self.SwitchButton = SwitchButton(self)
        self.SwitchButton.setChecked(False)
        self.SwitchButton.setObjectName("SwitchButton")

        self.horizontalLayout.addWidget(self.SwitchButton)
        self.shareButton = TransparentToolButton(self)
        self.shareButton.setObjectName("shareButton")

        self.horizontalLayout.addWidget(self.shareButton)
        self.deleteIcon = TransparentToolButton(self)
        self.deleteIcon.setObjectName("deleteIcon")

        self.horizontalLayout.addWidget(self.deleteIcon)

        # self.pluginName.setText("[插件名称]")
        # self.pluginMoreInfo.setText("[插件详细信息]")
        self.SwitchButton.setText("已禁用")
        self.SwitchButton.setOnText("已启用")
        self.SwitchButton.setOffText("已禁用")

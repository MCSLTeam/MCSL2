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
Widget Template for Quick Menu.
"""
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy, QGridLayout, QVBoxLayout
from qfluentwidgets import (
    BodyLabel,
    ComboBox,
    LineEdit,
    StrongBodyLabel,
    SmoothScrollArea,
)

from MCSL2Lib.variables import GlobalMCSL2Variables


class playersController(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("playersController")

        self.playersControllerMainWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.playersControllerMainWidget.sizePolicy().hasHeightForWidth()
        )
        self.playersControllerMainWidget.setSizePolicy(sizePolicy)
        self.playersControllerMainWidget.setMinimumSize(QSize(350, 241))
        self.playersControllerMainWidget.setMaximumSize(QSize(16777215, 16777215))
        self.playersControllerMainWidget.setObjectName("playersControllerMainWidget")

        self.gridLayout = QGridLayout(self.playersControllerMainWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.who = LineEdit(self.playersControllerMainWidget)
        self.who.setObjectName("who")

        self.gridLayout.addWidget(self.who, 0, 0, 1, 1)
        self.mode = ComboBox(self.playersControllerMainWidget)
        self.mode.setObjectName("mode")

        self.gridLayout.addWidget(self.mode, 0, 1, 1, 1)
        self.tipSmoothScrollArea = SmoothScrollArea(self.playersControllerMainWidget)
        self.tipSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tipSmoothScrollArea.setWidgetResizable(True)
        self.tipSmoothScrollArea.setObjectName("tipSmoothScrollArea")

        self.tipScrollAreaWidgetContents = QWidget()
        self.tipScrollAreaWidgetContents.setGeometry(QRect(0, -6, 313, 188))
        self.tipScrollAreaWidgetContents.setObjectName("tipScrollAreaWidgetContents")

        self.verticalLayout = QVBoxLayout(self.tipScrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.targetSelectorTipTitle = StrongBodyLabel(self.tipScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.targetSelectorTipTitle.sizePolicy().hasHeightForWidth()
        )
        self.targetSelectorTipTitle.setSizePolicy(sizePolicy)
        self.targetSelectorTipTitle.setObjectName("targetSelectorTipTitle")

        self.verticalLayout.addWidget(self.targetSelectorTipTitle)
        self.targetSelectorTip = BodyLabel(self.tipScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.targetSelectorTip.sizePolicy().hasHeightForWidth()
        )
        self.targetSelectorTip.setSizePolicy(sizePolicy)
        self.targetSelectorTip.setObjectName("targetSelectorTip")

        self.verticalLayout.addWidget(self.targetSelectorTip)
        self.playersTipTitle = StrongBodyLabel(self.tipScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.playersTipTitle.sizePolicy().hasHeightForWidth()
        )
        self.playersTipTitle.setSizePolicy(sizePolicy)
        self.playersTipTitle.setObjectName("playersTipTitle")

        self.verticalLayout.addWidget(self.playersTipTitle)
        self.playersTip = BodyLabel(self.tipScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersTip.sizePolicy().hasHeightForWidth())
        self.playersTip.setSizePolicy(sizePolicy)
        self.playersTip.setObjectName("playersTip")

        self.verticalLayout.addWidget(self.playersTip)
        self.tipSmoothScrollArea.setWidget(self.tipScrollAreaWidgetContents)
        self.gridLayout.addWidget(self.tipSmoothScrollArea, 1, 0, 1, 2)

        self.tipSmoothScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )

        self.who.setPlaceholderText("填写玩家名或目标选择器")
        self.targetSelectorTip.setText(
            "@p - 最近的玩家(在控制台可能无法使用)\n"
            "@r - 随机玩家\n"
            "@a - 所有玩家\n"
            "@e - 所有实体(不包括死亡实体)\n"
            "@s - 命令执行者(控制台不可用)"
        )
        self.playersTipTitle.setText("当前在线玩家：(可能不准确)")
        self.targetSelectorTipTitle.setText("目标选择器提示:")

#     Copyright 2024, MCSL Team, mailto:lxhtt@vip.qq.com
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
Select Java page, for adding new Minecraft servers.
"""

from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QSizePolicy,
    QGridLayout,
    QSpacerItem,
    QFrame,
    QVBoxLayout,
)
from qfluentwidgets import (
    StrongBodyLabel,
    BodyLabel,
    TitleLabel,
    TransparentToolButton,
    FluentIcon as FIF,
    FlowLayout,
)
from MCSL2Lib.ProgramControllers.interfaceController import MySmoothScrollArea

from MCSL2Lib.Widgets.selectJavaWidget import SingleSelectJavaWidget


class SelectJavaPage(QWidget):
    """适用于新建服务器时的选择Java页面"""

    setJavaVer = pyqtSignal(str)
    setJavaPath = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("selectJavaInterface")

        self.gridLayout = QGridLayout(self)
        spacerItem = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.javaSmoothScrollArea = MySmoothScrollArea(self)
        self.javaSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.javaSmoothScrollArea.setWidgetResizable(True)

        self.javaScrollAreaWidgetContents = QWidget()
        self.javaScrollAreaWidgetContents.setGeometry(QRect(0, 0, 778, 472))

        self.verticalLayout = QVBoxLayout(self.javaScrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.javaItemFlowLayout = FlowLayout()

        self.verticalLayout.addLayout(self.javaItemFlowLayout)
        self.javaSmoothScrollArea.setWidget(self.javaScrollAreaWidgetContents)
        self.gridLayout.addWidget(self.javaSmoothScrollArea, 3, 2, 1, 1)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.titleLimitWidget = QWidget(self)

        self.gridLayout_2 = QGridLayout(self.titleLimitWidget)

        self.backBtn = TransparentToolButton(FIF.PAGE_LEFT, self.titleLimitWidget)

        self.gridLayout_2.addWidget(self.backBtn, 0, 0, 1, 1)
        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.PlainText)

        self.gridLayout_2.addWidget(self.subTitleLabel, 2, 1, 1, 1)
        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.titleLabel, 0, 1, 1, 1)
        self.selectJavaTip = BodyLabel(self.titleLimitWidget)

        self.gridLayout_2.addWidget(self.selectJavaTip, 0, 3, 3, 1)
        titleLimitLayout = QSpacerItem(5, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(titleLimitLayout, 0, 2, 3, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 2, 2)
        self.subTitleLabel.setText(
            self.tr("以下是所有已知的Java，包括你自己添加的，和程序扫描到的。请选择。\n")
        )
        self.selectJavaTip.setText(
            self.tr(
                "请注意，如果您选择的Java版本不符合服务器的要求，可能会导致服务器无法启动。\n游戏版本1.16.5及以下的请使用Java 8\n游戏版本1.17~1.17.1的建议Java 17-18\n1.18及以上则使用Java 18-20"  # noqa: E501
            )
        )
        self.titleLabel.setText("Java")
        self.javaSmoothScrollArea.setAttribute(Qt.WA_StyledBackground)

    def refreshPage(self, JavaPath):
        """刷新Java列表"""
        self.javaItemFlowLayout.takeAllWidgets()
        for i in range(len(JavaPath)):
            self.javaItemFlowLayout.addWidget(
                SingleSelectJavaWidget(
                    btnName=f"finishSelectJavaBtn{str(i)}",
                    selectBtnSlot=lambda: self.scrollAreaProcessor(JavaPath),
                    backBtnSlot=self.backBtn.click,
                    path=JavaPath[i].path,
                    ver=JavaPath[i].version,
                )
            )

    def scrollAreaProcessor(self, JavaPath):
        """判断索引"""
        index = int(str(self.sender().objectName()).split("Btn")[1])
        selectedJavaPath = str(JavaPath[index].path)
        selectedJavaVer = str(str(JavaPath[index].version))
        self.setJavaPath.emit(selectedJavaPath)
        self.setJavaVer.emit(selectedJavaVer)

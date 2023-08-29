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
    SmoothScrollArea,
    StrongBodyLabel,
    TitleLabel,
    TransparentToolButton,
    FluentIcon as FIF,
)
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import GlobalMCSL2Variables
from MCSL2Lib.selectJavaWidget import singleSelectJavaWidget
from MCSL2Lib import icons as _  # noqa: F401


@Singleton
class SelectJavaPage(QWidget):
    """适用于新建服务器时的选择Java页面"""

    setJavaVer = pyqtSignal(str)
    setJavaPath = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("selectJavaInterface")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle("")
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.gridLayout_2 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.subTitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.gridLayout_2.addWidget(self.subTitleLabel, 1, 1, 1, 1)
        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayout_2.addWidget(self.titleLabel, 0, 1, 1, 1)
        self.javaSmoothScrollArea = SmoothScrollArea(self.titleLimitWidget)
        self.javaSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.javaSmoothScrollArea.setWidgetResizable(True)
        self.javaSmoothScrollArea.setObjectName("javaSmoothScrollArea")

        self.javaScrollAreaWidgetContents = QWidget()
        self.javaScrollAreaWidgetContents.setGeometry(QRect(0, 0, 658, 469))
        self.javaScrollAreaWidgetContents.setObjectName("javaScrollAreaWidgetContents")

        self.verticalLayout = QVBoxLayout(self.javaScrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.javaItemVerticalLayout = QVBoxLayout()
        self.javaItemVerticalLayout.setObjectName("javaItemVerticalLayout")

        self.verticalLayout.addLayout(self.javaItemVerticalLayout)
        self.javaSmoothScrollArea.setWidget(self.javaScrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.javaSmoothScrollArea, 2, 0, 1, 2)
        self.backBtn = TransparentToolButton(FIF.PAGE_LEFT, self.titleLimitWidget)
        self.backBtn.setObjectName("backBtn")

        self.gridLayout_2.addWidget(self.backBtn, 0, 0, 2, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 2, 2)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.subTitleLabel.setText("以下是所有已知的Java，包括你自己添加的，和程序扫描到的。请选择。")
        self.titleLabel.setText("Java")
        self.javaSmoothScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.javaSmoothScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )

    def refreshPage(self, JavaPath):
        """刷新Java列表"""

        # 删除旧的
        for i in reversed(range(self.javaItemVerticalLayout.count())):
            self.javaItemVerticalLayout.itemAt(i).widget().deleteLater()
        # 添加新的
        for i in range(len(JavaPath)):
            self.tmpSingleJavaWidget = singleSelectJavaWidget()
            self.tmpSingleJavaWidget.finishSelectJavaBtn.setObjectName(
                f"finishSelectJavaBtn{str(i)}"
            )
            self.tmpSingleJavaWidget.finishSelectJavaBtn.clicked.connect(
                lambda: self.scrollAreaProcessor(JavaPath)
            )
            self.tmpSingleJavaWidget.finishSelectJavaBtn.clicked.connect(self.backBtn.click)
            self.tmpSingleJavaWidget.javaPath.setText(str(JavaPath[i].path))
            self.tmpSingleJavaWidget.javaVer.setText(str(JavaPath[i].version))
            self.tmpSingleJavaWidget.javaVer.setReadOnly(True)
            self.tmpSingleJavaWidget.javaVer.setReadOnly(True)
            self.tmpSingleJavaWidget.javaVer.setReadOnly(True)
            self.tmpSingleJavaWidget.javaVer.setReadOnly(True)
            self.tmpSingleJavaWidget.javaVer.setReadOnly(True)
            self.tmpSingleJavaWidget.javaVer.setReadOnly(True)
            self.tmpSingleJavaWidget.javaVer.setReadOnly(True)
            self.tmpSingleJavaWidget.javaVer.setReadOnly(True)
            self.javaItemVerticalLayout.addWidget(self.tmpSingleJavaWidget)

    def scrollAreaProcessor(self, JavaPath):
        """判断索引"""
        index = int(str(self.sender().objectName()).split("Btn")[1])
        selectedJavaPath = str(JavaPath[index].path)
        selectedJavaVer = str(str(JavaPath[index].version))
        self.setJavaPath.emit(selectedJavaPath)
        self.setJavaVer.emit(selectedJavaVer)

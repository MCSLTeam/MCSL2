from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (
    QWidget,
    QSizePolicy,
    QGridLayout,
    QSpacerItem,
    QFrame,
    QVBoxLayout
)
from qfluentwidgets import (
    SmoothScrollArea,
    StrongBodyLabel,
    TitleLabel,
    TransparentToolButton,
    FluentIcon as FIF
)
from MCSL2Lib.variables import scrollAreaViewportQss


class _SelectJavaPage(QWidget):
    def __init__(self):

        super().__init__()

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
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
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
        self.javaSmoothScrollArea.viewport().setStyleSheet(scrollAreaViewportQss)
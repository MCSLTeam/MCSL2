from PyQt5.QtWidgets import QSizePolicy, QGridLayout, QHBoxLayout, QWidget, QVBoxLayout
from PyQt5.QtCore import QSize, Qt
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    PushButton,
    StrongBodyLabel,
    PrimaryToolButton,
    FluentIcon as FIF
)
from MCSL2Lib.variables import GlobalMCSL2Variables
from MCSL2Lib.publicFunctions import isDarkTheme


class FastMirrorVersionListWidget(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setObjectName("versionListWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(160, 50))
        self.setMaximumSize(QSize(160, 50))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.versionBtn = PushButton(self)
        self.versionBtn.setStyleSheet(
            GlobalMCSL2Variables.darkFastMirrorDownloadBtnStyleSheet
            if isDarkTheme()
            else GlobalMCSL2Variables.lightFastMirrorDownloadBtnStyleSheet
        )
        self.horizontalLayout.addWidget(self.versionBtn)
        # self.versionBtn.setObjectName("versionBtn")
        # self.versionBtn.setText("[版本]")


class FastMirrorCoreListWidget(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("coreListWidget")

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(180, 57))
        self.setMaximumSize(QSize(180, 57))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.coreTagWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.coreTagWidget.sizePolicy().hasHeightForWidth()
        )
        self.coreTagWidget.setSizePolicy(sizePolicy)
        self.coreTagWidget.setMinimumSize(QSize(0, 35))
        self.coreTagWidget.setMaximumSize(QSize(16777215, 35))
        self.coreTagWidget.setStyleSheet(
            "QWidget {\n"
            "    color: white;\n"
            "    background-color: #009faa;\n"
            "    border-radius: 17px;\n"
            "}"
        )
        self.coreTagWidget.setObjectName("coreTagWidget")

        self.gridLayout = QGridLayout(self.coreTagWidget)
        self.gridLayout.setObjectName("gridLayout")

        self.coreTag = BodyLabel(self.coreTagWidget)
        self.coreTag.setAlignment(Qt.AlignCenter)
        self.coreTag.setObjectName("coreTag")

        self.gridLayout.addWidget(self.coreTag, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.coreTagWidget)
        self.coreName = PushButton(self)
        self.coreName.setStyleSheet(
            GlobalMCSL2Variables.darkFastMirrorDownloadBtnStyleSheet
            if isDarkTheme()
            else GlobalMCSL2Variables.lightFastMirrorDownloadBtnStyleSheet
        )
        # self.coreName.setObjectName("coreName")

        self.horizontalLayout.addWidget(self.coreName)

        # self.coreTag.setText("[标签]")
        # self.coreName.setText("[名称]")


class FastMirrorBuildListWidget(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("buildListWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(284, 80))
        self.setMaximumSize(QSize(16777215, 80))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TextWidget = QWidget(self)
        self.TextWidget.setObjectName("TextWidget")
        self.verticalLayout = QVBoxLayout(self.TextWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buildVerLabel = StrongBodyLabel(self.TextWidget)
        self.buildVerLabel.setObjectName("buildVerLabel")
        self.verticalLayout.addWidget(self.buildVerLabel)
        self.syncTimeLabel = StrongBodyLabel(self.TextWidget)
        self.syncTimeLabel.setObjectName("syncTimeLabel")
        self.verticalLayout.addWidget(self.syncTimeLabel)
        self.horizontalLayout.addWidget(self.TextWidget)
        self.downloadBtn = PrimaryToolButton(FIF.DOWNLOAD, self)
        self.downloadBtn.setMinimumSize(QSize(50, 50))
        self.downloadBtn.setMaximumSize(QSize(50, 50))
        self.downloadBtn.setObjectName("downloadBtn")
        self.horizontalLayout.addWidget(self.downloadBtn)

        # self.coreNameLabel.setText("[版本号]")
        # self.syncTimeLabel.setText("[同步时间]")

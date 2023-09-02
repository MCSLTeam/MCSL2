from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QHBoxLayout, QVBoxLayout
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    PixmapLabel,
    PrimaryPushButton,
    SubtitleLabel,
)


class singleMCSLAPIDownloadWidget(CardWidget):
    def __init__(self):

        super().__init__()

        # self.setObjectName("singleMCSLAPIDownloadWidget")

        self.resize(656, 120)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(656, 120))
        self.setMaximumSize(QSize(16777215, 120))
        self.setWindowTitle("")
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.MCSLAPIPixmapLabel = PixmapLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLAPIPixmapLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLAPIPixmapLabel.setSizePolicy(sizePolicy)
        self.MCSLAPIPixmapLabel.setObjectName("MCSLAPIPixmapLabel")

        self.horizontalLayout.addWidget(self.MCSLAPIPixmapLabel)
        self.MCSLAPIDownloadInfoWidget = QWidget(self)
        self.MCSLAPIDownloadInfoWidget.setObjectName("MCSLAPIDownloadInfoWidget")

        self.verticalLayout = QVBoxLayout(self.MCSLAPIDownloadInfoWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.fileTitle = SubtitleLabel(self.MCSLAPIDownloadInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileTitle.sizePolicy().hasHeightForWidth())
        self.fileTitle.setSizePolicy(sizePolicy)
        self.fileTitle.setObjectName("fileTitle")

        self.verticalLayout.addWidget(self.fileTitle)
        self.fileName = BodyLabel(self.MCSLAPIDownloadInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileName.sizePolicy().hasHeightForWidth())
        self.fileName.setSizePolicy(sizePolicy)
        self.fileName.setObjectName("fileName")

        self.verticalLayout.addWidget(self.fileName)
        self.horizontalLayout.addWidget(self.MCSLAPIDownloadInfoWidget)
        self.MCSLAPIDownloadBtn = PrimaryPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLAPIDownloadBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLAPIDownloadBtn.setSizePolicy(sizePolicy)
        self.MCSLAPIDownloadBtn.setMinimumSize(QSize(0, 50))
        self.MCSLAPIDownloadBtn.setMaximumSize(QSize(16777215, 16777215))
        # self.MCSLAPIDownloadBtn.setObjectName("MCSLAPIDownloadBtn")

        self.horizontalLayout.addWidget(self.MCSLAPIDownloadBtn)
        # self.fileTitle.setText("[文件标题]")
        # self.fileName.setText("[文件名]")
        self.MCSLAPIDownloadBtn.setText("下载")

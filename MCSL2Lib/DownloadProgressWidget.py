from PyQt5.QtCore import QSize, QRect, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPaintEvent, QResizeEvent
from qfluentwidgets import (
    BodyLabel,
    PrimaryPushButton,
    ProgressBar,
    PushButton,
    StrongBodyLabel,
    SubtitleLabel, MessageBox,
)
from PyQt5.QtWidgets import (
    QSizePolicy,
    QGridLayout,
    QWidget,
    QStackedWidget,
    QSpacerItem,
    QHBoxLayout, QApplication,
)


class DownloadProgressWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("downloadProgress")

        self.downloadProgressMainWidget = QStackedWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.downloadProgressMainWidget.sizePolicy().hasHeightForWidth()
        )
        self.downloadProgressMainWidget.setSizePolicy(sizePolicy)
        self.downloadProgressMainWidget.setMinimumSize(QSize(321, 241))
        self.downloadProgressMainWidget.setMaximumSize(QSize(16777215, 16777215))
        self.downloadProgressMainWidget.setObjectName("downloadProgressMainWidget")

        self.downloading = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloading.sizePolicy().hasHeightForWidth())
        self.downloading.setSizePolicy(sizePolicy)
        self.downloading.setMinimumSize(QSize(321, 241))
        self.downloading.setObjectName("downloading")

        self.gridLayout_4 = QGridLayout(self.downloading)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.fileSizeTitle = StrongBodyLabel(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fileSizeTitle.sizePolicy().hasHeightForWidth()
        )
        self.fileSizeTitle.setSizePolicy(sizePolicy)
        self.fileSizeTitle.setObjectName("fileSizeTitle")

        self.gridLayout_4.addWidget(self.fileSizeTitle, 3, 0, 1, 1)
        self.downloadingLabel = SubtitleLabel(self.downloading)
        self.downloadingLabel.setObjectName("downloadingLabel")

        self.gridLayout_4.addWidget(self.downloadingLabel, 0, 0, 1, 2)
        self.ProgressWidget = QWidget(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ProgressWidget.sizePolicy().hasHeightForWidth()
        )
        self.ProgressWidget.setSizePolicy(sizePolicy)
        self.ProgressWidget.setMinimumSize(QSize(315, 40))
        self.ProgressWidget.setMaximumSize(QSize(16777215, 40))
        self.ProgressWidget.setObjectName("ProgressWidget")

        self.horizontalLayout = QHBoxLayout(self.ProgressWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.ProgressBar = ProgressBar(self.ProgressWidget)
        self.ProgressBar.setProperty("value", 0)
        self.ProgressBar.setObjectName("ProgressBar")

        self.horizontalLayout.addWidget(self.ProgressBar)
        self.ProgressNum = BodyLabel(self.ProgressWidget)
        self.ProgressNum.setObjectName("ProgressNum")

        self.horizontalLayout.addWidget(self.ProgressNum)
        self.gridLayout_4.addWidget(self.ProgressWidget, 9, 0, 1, 2)
        self.ETATitle = StrongBodyLabel(self.downloading)
        self.ETATitle.setObjectName("ETATitle")

        self.gridLayout_4.addWidget(self.ETATitle, 4, 0, 1, 1)
        self.cancelBtn = PushButton(self.downloading)
        self.cancelBtn.setObjectName("cancelBtn")

        self.gridLayout_4.addWidget(self.cancelBtn, 13, 0, 1, 1)
        self.fileSize = BodyLabel(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileSize.sizePolicy().hasHeightForWidth())
        self.fileSize.setSizePolicy(sizePolicy)
        self.fileSize.setObjectName("fileSize")

        self.gridLayout_4.addWidget(self.fileSize, 3, 1, 1, 1)
        self.speed = BodyLabel(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speed.sizePolicy().hasHeightForWidth())
        self.speed.setSizePolicy(sizePolicy)
        self.speed.setObjectName("speed")

        self.gridLayout_4.addWidget(self.speed, 5, 1, 1, 1)
        self.ETA = BodyLabel(self.downloading)
        self.ETA.setObjectName("ETA")

        self.gridLayout_4.addWidget(self.ETA, 4, 1, 1, 1)
        self.speedTitle = StrongBodyLabel(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speedTitle.sizePolicy().hasHeightForWidth())
        self.speedTitle.setSizePolicy(sizePolicy)
        self.speedTitle.setObjectName("speedTitle")

        self.gridLayout_4.addWidget(self.speedTitle, 5, 0, 1, 1)
        self.pauseBtn = PushButton(self.downloading)
        self.pauseBtn.setObjectName("pauseBtn")

        self.gridLayout_4.addWidget(self.pauseBtn, 13, 1, 1, 1)
        self.fileName = BodyLabel(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileName.sizePolicy().hasHeightForWidth())
        self.fileName.setSizePolicy(sizePolicy)
        self.fileName.setObjectName("fileName")

        self.gridLayout_4.addWidget(self.fileName, 2, 1, 1, 1)
        self.fileNameTitle = StrongBodyLabel(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fileNameTitle.sizePolicy().hasHeightForWidth()
        )
        self.fileNameTitle.setSizePolicy(sizePolicy)
        self.fileNameTitle.setObjectName("fileNameTitle")

        self.gridLayout_4.addWidget(self.fileNameTitle, 2, 0, 1, 1)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_4.addItem(spacerItem, 12, 0, 1, 2)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 8, 0, 1, 2)
        self.PrimaryPushButton = PrimaryPushButton(self.downloading)
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")

        self.gridLayout_4.addWidget(self.PrimaryPushButton, 13, 2, 1, 1)
        self.downloadProgressMainWidget.addWidget(self.downloading)
        self.downloadFinished = QWidget()
        self.downloadFinished.setObjectName("downloadFinished")

        self.gridLayout_2 = QGridLayout(self.downloadFinished)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.closeBoxBtnFinished = PrimaryPushButton(self.downloadFinished)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.closeBoxBtnFinished.sizePolicy().hasHeightForWidth()
        )
        self.closeBoxBtnFinished.setSizePolicy(sizePolicy)
        self.closeBoxBtnFinished.setMinimumSize(QSize(60, 0))
        self.closeBoxBtnFinished.setMaximumSize(QSize(60, 16777215))
        self.closeBoxBtnFinished.setObjectName("closeBoxBtnFinished")

        self.gridLayout_2.addWidget(self.closeBoxBtnFinished, 1, 1, 1, 1)
        self.downloadedLabel = SubtitleLabel(self.downloadFinished)
        self.downloadedLabel.setObjectName("downloadedLabel")

        self.gridLayout_2.addWidget(self.downloadedLabel, 0, 0, 1, 2)
        self.downloadProgressMainWidget.addWidget(self.downloadFinished)
        self.downloadFailed = QWidget()
        self.downloadFailed.setObjectName("downloadFailed")

        self.gridLayout_3 = QGridLayout(self.downloadFailed)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.closeBoxBtnFailed = PrimaryPushButton(self.downloadFailed)
        self.closeBoxBtnFailed.setMinimumSize(QSize(60, 0))
        self.closeBoxBtnFailed.setMaximumSize(QSize(60, 16777215))
        self.closeBoxBtnFailed.setObjectName("closeBoxBtnFailed")

        self.gridLayout_3.addWidget(self.closeBoxBtnFailed, 1, 1, 1, 1)
        self.downloadFailedLabel = SubtitleLabel(self.downloadFailed)
        self.downloadFailedLabel.setObjectName("downloadFailedLabel")

        self.gridLayout_3.addWidget(self.downloadFailedLabel, 0, 0, 1, 2)
        self.downloadProgressMainWidget.addWidget(self.downloadFailed)

        self.fileSizeTitle.setText("文件大小：")
        self.downloadingLabel.setText("正在下载：")
        self.ETATitle.setText("预计剩余时间：")
        self.cancelBtn.setText("取消")
        self.speedTitle.setText("当前速度：")
        self.pauseBtn.setText("暂停")
        self.fileNameTitle.setText("文件名：")
        self.PrimaryPushButton.setText("隐藏")
        self.closeBoxBtnFinished.setText("关闭")
        self.downloadedLabel.setText("下载完毕。")
        self.closeBoxBtnFailed.setText("关闭")
        self.downloadFailedLabel.setText("下载失败或取消！")

        self.downloading = False


class DL_MessageBox(MessageBox):
    canceled = pyqtSignal()
    paused = pyqtSignal(bool)

    def __init__(self, fileName, parent=None):
        super().__init__("", "", parent)
        self.pauseSwitch = False
        self.fileName = fileName
        self.downloadProgressWidget = DownloadProgressWidget()
        self.titleLabel.setParent(None)
        self.contentLabel.setParent(None)
        self.buttonGroup.setParent(None)
        self.downloadProgressWidget.fileName.setText(self.fileName)
        self.textLayout.addWidget(self.downloadProgressWidget.downloadProgressMainWidget)

        widget = self.downloadProgressWidget
        widget.cancelBtn.clicked.connect(self.canceled.emit)
        widget.pauseBtn.clicked.connect(self.onPauseBtnClicked)
        widget.PrimaryPushButton.clicked.connect(self.hide)

    def DL_Widget(self):
        return self.downloadProgressWidget

    def onPauseBtnClicked(self):
        self.pauseSwitch = not self.pauseSwitch
        if self.pauseSwitch:
            self.downloadProgressWidget.pauseBtn.setText("继续")
        else:
            self.downloadProgressWidget.pauseBtn.setText("暂停")
        self.paused.emit(self.pauseSwitch)

    @pyqtSlot(dict)
    def onInfoGet(self, info):
        self.downloadProgressWidget.fileSize.setText(info["totalLength"])
        self.downloadProgressWidget.ETA.setText(info["eta"])
        self.downloadProgressWidget.speed.setText(info["speed"])
        self.downloadProgressWidget.ProgressNum.setText(info["progress"])
        self.downloadProgressWidget.ProgressBar.setValue(info["bar"])
        self.downloadProgressWidget.downloading = True

    @pyqtSlot(int)
    def onDownloadFinished(self, status):
        self.hide()
        self.show()

        if status == 0:
            self.downloadProgressWidget.downloadProgressMainWidget.setCurrentIndex(1)
        elif status == 1:
            self.downloadProgressWidget.downloadProgressMainWidget.setCurrentIndex(2)
        elif status == 2:
            self.downloadProgressWidget.downloadProgressMainWidget.setCurrentIndex(2)
        elif status == 3:
            self.downloadProgressWidget.downloadProgressMainWidget.setCurrentIndex(1)
        self.downloadProgressWidget.downloading = False

    def setFileName(self, name):
        self.downloadProgressWidget.fileName.setText(name)

    def isDownloading(self):
        return self.downloadProgressWidget.downloading

    def flush(self):
        self.downloadProgressWidget.fileSize.setText("[文件大小]")
        self.downloadProgressWidget.speed.setText("[速度]")
        self.downloadProgressWidget.ETA.setText("[ETA]")
        self.downloadProgressWidget.ProgressNum.setText("NaN%")
        self.downloadProgressWidget.ProgressBar.setValue(0)
        self.downloadProgressWidget.fileName.setText("[文件名]")
        self.downloadProgressWidget.downloadProgressMainWidget.setCurrentIndex(0)
        self.downloadProgressWidget.downloading = False


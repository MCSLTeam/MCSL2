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
Download Progress Widget.
"""

from os import path
from typing import Optional

from PyQt5.QtCore import QSize, QRect, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QSizePolicy,
    QGridLayout,
    QWidget,
    QStackedWidget,
    QSpacerItem,
    QHBoxLayout,
)
from aria2p import Download
from qfluentwidgets import (
    BodyLabel,
    PrimaryPushButton,
    ProgressBar,
    PushButton,
    StrongBodyLabel,
    SubtitleLabel,
    MessageBox,
    SimpleCardWidget,
    InfoBarPosition,
    CaptionLabel,
    InfoBar,
)

from MCSL2Lib.ProgramControllers.aria2ClientController import (
    Aria2Controller,
    DL_EntryController,
)
from MCSL2Lib.utils import MCSL2Logger


class DownloadProgressWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("downloadProgress")

        self.downloadProgressMainWidget = QStackedWidget(self)
        self.downloadProgressMainWidget.setGeometry(QRect(20, 20, 321, 241))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.downloadProgressMainWidget.sizePolicy().hasHeightForWidth()
        )
        self.downloadProgressMainWidget.setSizePolicy(sizePolicy)
        self.downloadProgressMainWidget.setMinimumSize(QSize(321, 241))
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
        sizePolicy.setHeightForWidth(self.fileSizeTitle.sizePolicy().hasHeightForWidth())
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
        sizePolicy.setHeightForWidth(self.ProgressWidget.sizePolicy().hasHeightForWidth())
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
        self.fileNameTitle = StrongBodyLabel(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileNameTitle.sizePolicy().hasHeightForWidth())
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
        self.fileName = BodyLabel(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileName.sizePolicy().hasHeightForWidth())
        self.fileName.setSizePolicy(sizePolicy)
        self.fileName.setObjectName("fileName")

        self.gridLayout_4.addWidget(self.fileName, 2, 1, 1, 2)
        self.fileSize = BodyLabel(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileSize.sizePolicy().hasHeightForWidth())
        self.fileSize.setSizePolicy(sizePolicy)
        self.fileSize.setObjectName("fileSize")

        self.gridLayout_4.addWidget(self.fileSize, 3, 1, 1, 2)
        self.ETA = BodyLabel(self.downloading)
        self.ETA.setObjectName("ETA")

        self.gridLayout_4.addWidget(self.ETA, 4, 1, 1, 2)
        self.speed = BodyLabel(self.downloading)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speed.sizePolicy().hasHeightForWidth())
        self.speed.setSizePolicy(sizePolicy)
        self.speed.setObjectName("speed")

        self.gridLayout_4.addWidget(self.speed, 5, 1, 1, 2)
        self.downloadProgressMainWidget.addWidget(self.downloading)
        self.downloadFinished = QWidget()
        self.downloadFinished.setObjectName("downloadFinished")

        self.gridLayout_2 = QGridLayout(self.downloadFinished)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.closeBoxBtnFinished = PrimaryPushButton(self.downloadFinished)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closeBoxBtnFinished.sizePolicy().hasHeightForWidth())
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

        self.fileSizeTitle.setText(self.tr("文件大小："))
        self.downloadingLabel.setText(self.tr("正在下载："))
        self.ETATitle.setText(self.tr("预计剩余时间："))
        self.cancelBtn.setText(self.tr("取消"))
        self.speedTitle.setText(self.tr("当前速度："))
        self.pauseBtn.setText(self.tr("暂停"))
        self.fileNameTitle.setText(self.tr("文件名："))
        self.PrimaryPushButton.setText(self.tr("隐藏"))
        self.closeBoxBtnFinished.setText(self.tr("关闭"))
        self.downloadedLabel.setText(self.tr("下载完毕。"))
        self.closeBoxBtnFailed.setText(self.tr("关闭"))
        self.downloadFailedLabel.setText(self.tr("下载失败或取消！"))

        self.downloading = False


class DownloadMessageBox(MessageBox):
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
        self.titleLabel.deleteLater()
        self.contentLabel.deleteLater()
        self.buttonGroup.deleteLater()
        self.downloadProgressWidget.fileName.setText(self.fileName)
        self.textLayout.addWidget(self.downloadProgressWidget.downloadProgressMainWidget)

        widget = self.downloadProgressWidget
        widget.cancelBtn.clicked.connect(self.canceled.emit)
        widget.pauseBtn.clicked.connect(self.onPauseBtnClicked)
        widget.PrimaryPushButton.clicked.connect(self.hide)
        self.DownloadWidget().closeBoxBtnFinished.clicked.connect(self.close)
        self.DownloadWidget().closeBoxBtnFailed.clicked.connect(self.close)

    def DownloadWidget(self):
        return self.downloadProgressWidget

    def onPauseBtnClicked(self):
        self.pauseSwitch = not self.pauseSwitch
        if self.pauseSwitch:
            self.downloadProgressWidget.pauseBtn.setText(self.tr("继续"))
        else:
            self.downloadProgressWidget.pauseBtn.setText(self.tr("暂停"))
        self.paused.emit(self.pauseSwitch)

    @pyqtSlot(dict)
    def onInfoGet(self, info):
        self.downloadProgressWidget.fileSize.setText(info["totalLength"])
        self.downloadProgressWidget.ETA.setText(info["eta"])
        self.downloadProgressWidget.speed.setText(info["speed"])
        self.downloadProgressWidget.ProgressNum.setText(info["progress"])
        self.downloadProgressWidget.ProgressBar.setValue(info["bar"])
        self.downloadProgressWidget.downloading = True

    @pyqtSlot(list)
    def onDownloadFinished(self, _: list):
        [dl, extraData] = _
        dl: Optional[Download]
        self.hide()
        self.show()
        filename = extraData[0]
        data = {
            "type": extraData[1],
            "mc_version": extraData[2],
            "build_version": extraData[3],
        }

        if dl is not None:
            if dl.status == "complete":
                self.downloadProgressWidget.downloadProgressMainWidget.setCurrentIndex(1)
                if path.exists(path.join("MCSL2", "Downloads", filename)):  # 防止有时候aria2抽风...
                    DL_EntryController().work.emit((
                        "addCoreEntry",
                        {"coreName": filename, "extraData": data},
                    ))
            elif dl.status == "error":
                self.downloadProgressWidget.downloadProgressMainWidget.setCurrentIndex(2)
                MCSL2Logger.error(msg=f"{dl.error_code}{dl.error_message}{dl.files}")
            elif dl.status == "removed":
                self.downloadProgressWidget.downloadProgressMainWidget.setCurrentIndex(2)
        else:
            self.downloadProgressWidget.downloadProgressMainWidget.setCurrentIndex(2)
        self.downloadProgressWidget.downloading = False
        try:
            self.parent().downloadFinishedHelper()
        except Exception:
            pass

    def setFileName(self, name):
        self.downloadProgressWidget.fileName.setText(name)

    def isDownloading(self):
        return self.downloadProgressWidget.downloading

    def flush(self):
        self.downloadProgressWidget.fileSize.setText(self.tr("[文件大小]"))
        self.downloadProgressWidget.speed.setText(self.tr("[速度]"))
        self.downloadProgressWidget.ETA.setText(self.tr("[ETA]"))
        self.downloadProgressWidget.ProgressNum.setText(self.tr("NaN%"))
        self.downloadProgressWidget.ProgressBar.setValue(0)
        self.downloadProgressWidget.fileName.setText(self.tr("[文件名]"))
        self.downloadProgressWidget.downloadProgressMainWidget.setCurrentIndex(0)
        self.downloadProgressWidget.downloading = False


class DownloadCard(SimpleCardWidget):
    canceled = pyqtSignal()
    paused = pyqtSignal(bool)

    def __init__(self, fileName, url, parent=None):
        super().__init__(parent)
        self.setObjectName("downloadingProgressWidget")
        self.resize(300, 100)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(300, 100))
        self.setMaximumSize(QSize(300, 120))
        self.gridLayout_2 = QGridLayout(self)
        self.infoWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoWidget.sizePolicy().hasHeightForWidth())
        self.infoWidget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.infoWidget)
        self.fileNameLabel = BodyLabel(self.infoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileNameLabel.sizePolicy().hasHeightForWidth())
        self.fileNameLabel.setSizePolicy(sizePolicy)
        self.fileNameLabel.setFixedSize(QSize(196, 18))
        self.gridLayout.addWidget(self.fileNameLabel, 0, 0, 1, 2)
        self.progressNum = CaptionLabel(self.infoWidget)
        self.gridLayout.addWidget(self.progressNum, 2, 1, 1, 1)
        self.ProgressBar = ProgressBar(self.infoWidget)
        self.gridLayout.addWidget(self.ProgressBar, 2, 0, 1, 1)
        self.downloadExtraInfoLabel = BodyLabel(self.infoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadExtraInfoLabel.sizePolicy().hasHeightForWidth())
        self.downloadExtraInfoLabel.setSizePolicy(sizePolicy)
        self.downloadExtraInfoLabel.setFixedSize(QSize(196, 18))
        self.gridLayout.addWidget(self.downloadExtraInfoLabel, 1, 0, 1, 2)
        self.gridLayout_2.addWidget(self.infoWidget, 0, 0, 2, 1)
        self.cancelBtn = PushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelBtn.sizePolicy().hasHeightForWidth())
        self.cancelBtn.setSizePolicy(sizePolicy)
        self.cancelBtn.setFixedSize(QSize(61, 32))
        self.gridLayout_2.addWidget(self.cancelBtn, 0, 1, 1, 1)
        self.pauseBtn = PushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pauseBtn.sizePolicy().hasHeightForWidth())
        self.pauseBtn.setSizePolicy(sizePolicy)
        self.pauseBtn.setFixedSize(QSize(61, 32))
        self.gridLayout_2.addWidget(self.pauseBtn, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.pauseBtn, 1, 1, 1, 1)
        self.progressNum.setText("NaN%")
        self.fileNameLabel.setText(fileName)
        self.cancelBtn.setText("取消")
        self.pauseBtn.setText("暂停")
        self.downloadExtraInfoLabel.setText("[大小]  [速度]  [ETA]")
        self.downloading = False
        self.pauseSwitch = False
        self.uri = url
        self.cancelBtn.clicked.connect(self.close)
        self.cancelBtn.clicked.connect(self.canceled.emit)
        self.pauseBtn.clicked.connect(self.onPauseBtnClicked)

    def retryDownloadFile(self, extraData: tuple):
        gid = Aria2Controller.download(
            uri=self.uri,
            watch=True,
            info_get=self.onInfoGet,
            stopped=self.onDownloadFinished,
            interval=0.2,
            extraData=extraData,
        )
        self.canceled.disconnect()
        self.paused.disconnect()
        self.canceled.connect(lambda: Aria2Controller.cancelDownloadTask(gid))
        self.paused.connect(
            lambda x: Aria2Controller.pauseDownloadTask(gid)
            if x
            else Aria2Controller.resumeDownloadTask(gid)
        )

    def onPauseBtnClicked(self):
        self.pauseSwitch = not self.pauseSwitch
        if self.pauseSwitch:
            self.pauseBtn.setText(self.tr("继续"))
            self.ProgressBar.pause()
        else:
            self.pauseBtn.setText(self.tr("暂停"))
            self.ProgressBar.resume()
        self.paused.emit(self.pauseSwitch)

    @pyqtSlot(dict)
    def onInfoGet(self, info):
        self.downloadExtraInfoLabel.setText(
            f"{info['totalLength']} | {info['speed']} | {info['eta']}"
        )
        self.progressNum.setText(info["progress"])
        self.ProgressBar.setValue(info["bar"])
        self.downloading = True

    @pyqtSlot(list)
    def onDownloadFinished(self, _: list):
        [dl, extraData] = _
        dl: Optional[Download]
        filename = extraData[0]
        data = {
            "type": extraData[1],
            "mc_version": extraData[2],
            "build_version": extraData[3],
        }

        if dl is not None:
            if dl.status == "complete":
                InfoBar.success(
                    title=self.tr(f"{filename} 下载完成"),
                    content="",
                    duration=1500,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    parent=self.parent().parent().parent().parent(),
                )
                if path.exists(path.join("MCSL2", "Downloads", filename)):  # 防止有时候aria2抽风...
                    DL_EntryController().work.emit((
                        "addCoreEntry",
                        {"coreName": filename, "extraData": data},
                    ))
                self.setParent(None)
                self.deleteLater()
            elif dl.status == "error":
                errInfoBar = InfoBar.error(
                    title=self.tr(f"{filename} 下载失败"),
                    content="",
                    duration=-1,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    parent=self.parent().parent().parent().parent(),
                )
                retryBtn = PushButton(self.tr("重试"), parent=errInfoBar)
                retryBtn.clicked.connect(lambda: self.retryDownloadFile(extraData))
                retryBtn.clicked.connect(errInfoBar.close)
                errInfoBar.addWidget(retryBtn)
                self.ProgressBar.setValue(100)
                self.ProgressBar.error()
                MCSL2Logger.error(msg=f"{dl.error_code}{dl.error_message}{dl.files}")
            elif dl.status == "removed":
                try:
                    self.flush()
                    self.setParent(None)
                    self.deleteLater()
                except Exception:
                    pass
        else:
            errInfoBar = InfoBar.error(
                title=self.tr(f"{filename} 下载失败"),
                content="",
                duration=-1,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                parent=self.parent().parent().parent().parent(),
            )
            retryBtn = PushButton(self.tr("重试"), parent=errInfoBar)
            retryBtn.clicked.connect(lambda: self.retryDownloadFile(extraData))
            retryBtn.clicked.connect(errInfoBar.close)
            errInfoBar.addWidget(retryBtn)
            self.ProgressBar.setValue(100)
            self.ProgressBar.error()
        self.downloading = False
        try:
            self.parent().downloadFinishedHelper()
        except Exception:
            pass

    def isDownloading(self):
        return self.downloading

    def flush(self):
        self.fileNameLabel.setText(self.tr("[文件名]"))
        self.downloadExtraInfoLabel.setText(self.tr("[大小]  [速度]  [ETA]"))
        self.progressNum.setText(self.tr("NaN%"))
        self.ProgressBar.setValue(0)
        self.downloading = False

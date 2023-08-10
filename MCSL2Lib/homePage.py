#     Copyright 2023, MCSL Team, mailto:lxhtt@mcsl.com.cn
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
Home page.
"""

from qfluentwidgets import (
    PrimaryPushButton,
    PushButton,
    StrongBodyLabel,
    TitleLabel,
    IndeterminateProgressRing,
)
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGridLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from MCSL2Lib.networkController import Session
from MCSL2Lib.singleton import Singleton


@Singleton
class HomePage(QWidget):
    """主页"""

    def __init__(self):
        super().__init__()

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle("")
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.gridLayout_3 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayout_3.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.noticeWidget = QWidget(self.titleLimitWidget)
        self.noticeWidget.setObjectName("noticeWidget")

        self.horizontalLayout = QHBoxLayout(self.noticeWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.subTitleLabel = StrongBodyLabel(self.noticeWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.subTitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.horizontalLayout.addWidget(self.subTitleLabel)
        self.IndeterminateProgressRing = IndeterminateProgressRing(self.noticeWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.IndeterminateProgressRing.sizePolicy().hasHeightForWidth()
        )
        self.IndeterminateProgressRing.setSizePolicy(sizePolicy)
        self.IndeterminateProgressRing.setMinimumSize(QSize(20, 20))
        self.IndeterminateProgressRing.setMaximumSize(QSize(20, 20))
        self.IndeterminateProgressRing.setObjectName("IndeterminateProgressRing")

        self.horizontalLayout.addWidget(self.IndeterminateProgressRing)
        self.gridLayout_3.addWidget(self.noticeWidget, 1, 0, 1, 1)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 2, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 1, 1)
        self.home_btnWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.home_btnWidget.sizePolicy().hasHeightForWidth()
        )
        self.home_btnWidget.setSizePolicy(sizePolicy)
        self.home_btnWidget.setMinimumSize(QSize(244, 140))
        self.home_btnWidget.setMaximumSize(QSize(244, 140))
        self.home_btnWidget.setObjectName("home_btnWidget")

        self.gridLayout_2 = QGridLayout(self.home_btnWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.newServerBtn = PushButton(self.home_btnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newServerBtn.sizePolicy().hasHeightForWidth())
        self.newServerBtn.setSizePolicy(sizePolicy)
        self.newServerBtn.setFocusPolicy(Qt.NoFocus)
        self.newServerBtn.setObjectName("newServerBtn")

        self.gridLayout_2.addWidget(self.newServerBtn, 0, 2, 1, 1)
        self.startServerBtn = PrimaryPushButton(self.home_btnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.startServerBtn.sizePolicy().hasHeightForWidth()
        )
        self.startServerBtn.setSizePolicy(sizePolicy)
        self.startServerBtn.setMinimumSize(QSize(0, 70))
        self.startServerBtn.setFocusPolicy(Qt.NoFocus)
        self.startServerBtn.setObjectName("startServerBtn")

        self.gridLayout_2.addWidget(self.startServerBtn, 1, 1, 1, 2)
        self.selectServerBtn = PushButton(self.home_btnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.selectServerBtn.sizePolicy().hasHeightForWidth()
        )
        self.selectServerBtn.setSizePolicy(sizePolicy)
        self.selectServerBtn.setFocusPolicy(Qt.NoFocus)
        self.selectServerBtn.setObjectName("selectServerBtn")

        self.gridLayout_2.addWidget(self.selectServerBtn, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.home_btnWidget, 4, 3, 1, 1)
        spacerItem1 = QSpacerItem(400, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        spacerItem2 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 0, 2, 1, 1)
        spacerItem4 = QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 3, 2, 1, 1)
        self.newServerBtn.setText("新建")
        self.startServerBtn.setText("启动服务器：")
        self.selectServerBtn.setText("选择")
        self.titleLabel.setText("主页")
        self.subTitleLabel.setText("获取公告中...")

        self.setObjectName("homeInterface")

        self.startServerBtn.setEnabled(False)

        self.thread = GetNoticeThread(self)
        self.thread.notice.connect(self.subTitleLabel.setText)
        self.thread.ringVisible.connect(self.IndeterminateProgressRing.setVisible)
        self.thread.start()

    @pyqtSlot(str)
    def afterSelectedServer(self, serverName):
        """选择服务器后的处理"""
        self.startServerBtn.setText(f"启动服务器：{serverName}")


class GetNoticeThread(QThread):
    """
    获取公告的线程\n
    使用多线程防止拖慢启动速度
    """

    notice = pyqtSignal(str)
    ringVisible = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("NoticeThread")

    def run(self):
        getNoticeUrl = "http://api.2018k.cn/getExample?id=BCF5D58B4AE6471E98CFD5A56604560B&data=notice"
        try:
            notice = f"公告: \n{Session.get(getNoticeUrl).text}"
            self.notice.emit(notice)
        except Exception as e:
            self.notice.emit("网络连接失败，无法获取公告。")
        self.ringVisible.emit(False)

from qfluentwidgets import PrimaryPushButton, PushButton, StrongBodyLabel, TitleLabel
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QGridLayout, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from traceback import format_exception as FormatException
from MCSL2Lib.networkController import Session


class _HomePage(QWidget):

    def __init__(self):
        
        super().__init__()

        # 全局GridLayout
        self.gridLayout = QGridLayout(self)

        self.titleLimitWidget = QWidget(self)

        self.verticalLayout = QVBoxLayout(self.titleLimitWidget)

        # 标题
        self.titleLabel = TitleLabel(self.titleLimitWidget)

        self.verticalLayout.addWidget(self.titleLabel)

        # 公告
        self.NoticeLabel = StrongBodyLabel(self.titleLimitWidget)
        self.NoticeLabel.setTextFormat(Qt.MarkdownText)

        self.verticalLayout.addWidget(self.NoticeLabel)

        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 1, 1)

        self.home_btnWidget = QWidget(self)
        self.home_btnWidget.setMinimumSize(QSize(244, 140))
        self.home_btnWidget.setMaximumSize(QSize(244, 140))

        self.btnWidgetGridLayout = QGridLayout(self.home_btnWidget)

        self.newServerBtn = PushButton(self.home_btnWidget)

        self.btnWidgetGridLayout.addWidget(self.newServerBtn, 0, 2, 1, 1)

        self.startServerBtn = PrimaryPushButton(self.home_btnWidget)
        self.startServerBtn.setMinimumSize(QSize(0, 70))
        self.btnWidgetGridLayout.addWidget(self.startServerBtn, 1, 1, 1, 2)

        self.selectServerBtn = PushButton(self.home_btnWidget)
        self.btnWidgetGridLayout.addWidget(self.selectServerBtn, 0, 1, 1, 1)

        self.gridLayout.addWidget(self.home_btnWidget, 4, 3, 1, 1)
        spacerItem = QSpacerItem(
            400, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 2, 1, 1)
        spacerItem1 = QSpacerItem(
            10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QSpacerItem(
            20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QSpacerItem(
            20, 300, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 3, 2, 1, 1)

        self.newServerBtn.setText("新建")
        self.startServerBtn.setText("启动服务器：")
        self.selectServerBtn.setText("选择")
        self.titleLabel.setText("主页")
        self.NoticeLabel.setText(self.GetNotice())
        self.setObjectName("homeInterface")

        # self.newServerBtn.clicked.connect()
        # self.startServerBtn.clicked.connect()
        # self.selectServerBtn.clicked.connect()

    def GetNotice(self):
        GetNoticeUrl = "http://api.2018k.cn/getExample?id=BCF5D58B4AE6471E98CFD5A56604560B&data=notice"
        try:
            Notice = f"公告: {Session.get(GetNoticeUrl).text}"
            return Notice
        except Exception as e:
            ExceptionString = "".join(FormatException(type(e), e, e.__traceback__))
            return f"{ExceptionString}网络连接失败，无法获取公告。"

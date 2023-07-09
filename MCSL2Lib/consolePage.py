from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QSpacerItem,
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QFrame
)
from qfluentwidgets import (
    CardWidget,
    ComboBox,
    LineEdit,
    PlainTextEdit,
    PrimaryToolButton,
    ProgressRing,
    StrongBodyLabel,
    TitleLabel,
    TransparentPushButton
)

class _ConsolePage(QWidget):
    def __init__(self):
        super().__init__()
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.serverMemCardWidget = CardWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverMemCardWidget.sizePolicy().hasHeightForWidth())
        self.serverMemCardWidget.setSizePolicy(sizePolicy)
        self.serverMemCardWidget.setMinimumSize(QSize(130, 120))
        self.serverMemCardWidget.setMaximumSize(QSize(130, 120))
        self.serverMemCardWidget.setObjectName("serverMemCardWidget")

        self.gridLayout_3 = QGridLayout(self.serverMemCardWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.serverMemProgressRing = ProgressRing(self.serverMemCardWidget)
        self.serverMemProgressRing.setMinimumSize(QSize(80, 80))
        self.serverMemProgressRing.setMaximumSize(QSize(80, 80))
        self.serverMemProgressRing.setObjectName("serverMemProgressRing")

        self.gridLayout_3.addWidget(self.serverMemProgressRing, 1, 0, 1, 1)
        self.serverMemLabel = StrongBodyLabel(self.serverMemCardWidget)
        self.serverMemLabel.setObjectName("serverMemLabel")

        self.gridLayout_3.addWidget(self.serverMemLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.serverMemCardWidget, 1, 4, 1, 1)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.serverCPUCardWidget = CardWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverCPUCardWidget.sizePolicy().hasHeightForWidth())
        self.serverCPUCardWidget.setSizePolicy(sizePolicy)
        self.serverCPUCardWidget.setMinimumSize(QSize(130, 120))
        self.serverCPUCardWidget.setMaximumSize(QSize(130, 120))
        self.serverCPUCardWidget.setObjectName("serverCPUCardWidget")

        self.gridLayout_4 = QGridLayout(self.serverCPUCardWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.serverCPUProgressRing = ProgressRing(self.serverCPUCardWidget)
        self.serverCPUProgressRing.setMinimumSize(QSize(80, 80))
        self.serverCPUProgressRing.setMaximumSize(QSize(80, 80))
        self.serverCPUProgressRing.setObjectName("serverCPUProgressRing")

        self.gridLayout_4.addWidget(self.serverCPUProgressRing, 1, 0, 1, 1)
        self.serverCPULabel = StrongBodyLabel(self.serverCPUCardWidget)
        self.serverCPULabel.setObjectName("serverCPULabel")

        self.gridLayout_4.addWidget(self.serverCPULabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.serverCPUCardWidget, 2, 4, 1, 1)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 4, 1, 1)
        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.gridLayout_2 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.sendCommandButton = PrimaryToolButton(self.titleLimitWidget)
        self.sendCommandButton.setText("")
        self.sendCommandButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sendCommandButton.setObjectName("sendCommandButton")

        self.gridLayout_2.addWidget(self.sendCommandButton, 4, 1, 1, 1)
        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.gridLayout_2.addWidget(self.subTitleLabel, 1, 0, 1, 1)
        self.commandLineEdit = LineEdit(self.titleLimitWidget)
        self.commandLineEdit.setObjectName("commandLineEdit")

        self.gridLayout_2.addWidget(self.commandLineEdit, 4, 0, 1, 1)
        self.serverOutput = PlainTextEdit(self.titleLimitWidget)
        self.serverOutput.setFrameShape(QFrame.NoFrame)
        self.serverOutput.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.serverOutput.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setPlainText("")
        self.serverOutput.setObjectName("serverOutput")

        self.gridLayout_2.addWidget(self.serverOutput, 3, 0, 1, 2)
        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayout_2.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 4, 2)
        self.quickMenu = CardWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quickMenu.sizePolicy().hasHeightForWidth())
        self.quickMenu.setSizePolicy(sizePolicy)
        self.quickMenu.setMinimumSize(QSize(100, 300))
        self.quickMenu.setMaximumSize(QSize(130, 16777215))
        self.quickMenu.setObjectName("quickMenu")

        self.verticalLayout = QVBoxLayout(self.quickMenu)
        self.verticalLayout.setObjectName("verticalLayout")

        self.quickMenuTitleLabel = StrongBodyLabel(self.quickMenu)
        self.quickMenuTitleLabel.setObjectName("quickMenuTitleLabel")

        self.verticalLayout.addWidget(self.quickMenuTitleLabel)
        self.gameMode = ComboBox(self.quickMenu)
        self.gameMode.setMinimumSize(QSize(0, 30))
        self.gameMode.setObjectName("gameMode")

        self.verticalLayout.addWidget(self.gameMode)
        self.whiteList = TransparentPushButton(self.quickMenu)
        self.whiteList.setMinimumSize(QSize(0, 30))
        self.whiteList.setObjectName("whiteList")

        self.verticalLayout.addWidget(self.whiteList)
        self.op = TransparentPushButton(self.quickMenu)
        self.op.setMinimumSize(QSize(0, 30))
        self.op.setObjectName("op")

        self.verticalLayout.addWidget(self.op)
        self.kickPlayers = TransparentPushButton(self.quickMenu)
        self.kickPlayers.setMinimumSize(QSize(0, 30))
        self.kickPlayers.setObjectName("kickPlayers")

        self.verticalLayout.addWidget(self.kickPlayers)
        self.banPlayers = TransparentPushButton(self.quickMenu)
        self.banPlayers.setMinimumSize(QSize(0, 30))
        self.banPlayers.setObjectName("banPlayers")

        self.verticalLayout.addWidget(self.banPlayers)
        self.saveServer = TransparentPushButton(self.quickMenu)
        self.saveServer.setMinimumSize(QSize(0, 30))
        self.saveServer.setObjectName("saveServer")

        self.verticalLayout.addWidget(self.saveServer)
        self.exitServer = TransparentPushButton(self.quickMenu)
        self.exitServer.setMinimumSize(QSize(0, 30))
        self.exitServer.setObjectName("exitServer")

        self.verticalLayout.addWidget(self.exitServer)
        self.killServer = TransparentPushButton(self.quickMenu)
        self.killServer.setMinimumSize(QSize(0, 30))
        self.killServer.setObjectName("killServer")

        self.verticalLayout.addWidget(self.killServer)
        self.gridLayout.addWidget(self.quickMenu, 3, 4, 1, 1)

        self.setObjectName("DownloadInterface")

        self.serverMemLabel.setText("内存占用：")
        self.serverCPULabel.setText("CPU占用：")
        self.subTitleLabel.setText("直观地观察你的服务器的输出，资源占用等。")
        self.titleLabel.setText("终端")
        self.quickMenuTitleLabel.setText("快捷菜单：")
        self.gameMode.setText("游戏模式")
        self.whiteList.setText("白名单")
        self.op.setText("管理员")
        self.kickPlayers.setText("踢人")
        self.banPlayers.setText("封禁")
        self.saveServer.setText("保存存档")
        self.exitServer.setText("关闭服务器")
        self.killServer.setText("强制关闭")

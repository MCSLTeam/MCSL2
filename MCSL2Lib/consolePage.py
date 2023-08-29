# -*- coding: utf-8 -*-
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
Minecraft server console page.
"""

from PyQt5.QtCore import QSize, Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QTextCharFormat, QColor, QBrush
from PyQt5.QtWidgets import (
    QSpacerItem,
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QFrame,
    QCompleter,
    QStackedWidget
)
from qfluentwidgets import (
    CardWidget,
    ComboBox,
    ProgressRing,
    StrongBodyLabel,
    TitleLabel,
    TransparentPushButton,
    MessageBox,
    InfoBar,
    InfoBarPosition,
    TabBar,
)
from MCSL2Lib.serverController import ServerHandler, readServerProperties

from MCSL2Lib.singleton import Singleton

from MCSL2Lib.playersControllerMainWidget import playersController
from MCSL2Lib.variables import ServerVariables, GlobalMCSL2Variables

serverVariables = ServerVariables()


@Singleton
class ConsolePage(QWidget):
    """终端页"""

    playersControllerBtnEnabled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.playersList = []
        self.playersControllerBtnEnabled.emit(False)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
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

        self.gridLayout_3.addWidget(self.serverMemProgressRing, 1, 1, 1, 1)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 2, 1, 1)
        self.serverMemLabel = StrongBodyLabel(self.serverMemCardWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverMemLabel.sizePolicy().hasHeightForWidth())
        self.serverMemLabel.setSizePolicy(sizePolicy)
        self.serverMemLabel.setObjectName("serverMemLabel")
        
        self.gridLayout_3.addWidget(self.serverMemLabel, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.serverMemCardWidget, 1, 4, 1, 1)
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 0, 1, 1)
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

        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem4, 1, 0, 1, 1)
        self.serverCPUProgressRing = ProgressRing(self.serverCPUCardWidget)
        self.serverCPUProgressRing.setMinimumSize(QSize(80, 80))
        self.serverCPUProgressRing.setMaximumSize(QSize(80, 80))
        self.serverCPUProgressRing.setObjectName("serverCPUProgressRing")

        self.gridLayout_4.addWidget(self.serverCPUProgressRing, 1, 1, 1, 1)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem5, 1, 2, 1, 1)
        self.serverCPULabel = StrongBodyLabel(self.serverCPUCardWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverCPULabel.sizePolicy().hasHeightForWidth())
        self.serverCPULabel.setSizePolicy(sizePolicy)
        self.serverCPULabel.setObjectName("serverCPULabel")

        self.gridLayout_4.addWidget(self.serverCPULabel, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.serverCPUCardWidget, 2, 4, 1, 1)
        spacerItem6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 4, 4, 1, 1)
        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.gridLayout_2 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayout_2.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.serversStackedWidget = QStackedWidget(self.titleLimitWidget)
        self.serversStackedWidget.setObjectName("serversStackedWidget")

        self.noServer = QWidget()
        self.noServer.setObjectName("noServer")

        self.gridLayout_5 = QGridLayout(self.noServer)
        self.gridLayout_5.setObjectName("gridLayout_5")

        self.TitleLabel = TitleLabel(self.noServer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setObjectName("TitleLabel")

        self.gridLayout_5.addWidget(self.TitleLabel, 0, 0, 1, 1)
        self.serversStackedWidget.addWidget(self.noServer)
        # self.sampleServerPage = QWidget()
        # self.sampleServerPage.setObjectName("sampleServerPage")

        # self.serversStackedWidget.addWidget(self.sampleServerPage)
        self.gridLayout_2.addWidget(self.serversStackedWidget, 3, 0, 1, 1)
        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.gridLayout_2.addWidget(self.subTitleLabel, 1, 0, 1, 1)
        self.serversTabBar = TabBar(self.titleLimitWidget)
        self.serversTabBar.setFrameShape(QFrame.NoFrame)
        self.serversTabBar.setObjectName("serversTabBar")

        self.gridLayout_2.addWidget(self.serversTabBar, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 4, 2)
        self.quickMenu = CardWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quickMenu.sizePolicy().hasHeightForWidth())
        self.quickMenu.setSizePolicy(sizePolicy)
        self.quickMenu.setMinimumSize(QSize(100, 340))
        self.quickMenu.setMaximumSize(QSize(130, 16777215))
        self.quickMenu.setObjectName("quickMenu")

        self.verticalLayout = QVBoxLayout(self.quickMenu)
        self.verticalLayout.setObjectName("verticalLayout")

        self.quickMenuTitleLabel = StrongBodyLabel(self.quickMenu)
        self.quickMenuTitleLabel.setObjectName("quickMenuTitleLabel")

        self.verticalLayout.addWidget(self.quickMenuTitleLabel)
        self.difficulty = ComboBox(self.quickMenu)
        self.difficulty.setMinimumSize(QSize(0, 30))
        self.difficulty.setObjectName("difficulty")

        self.verticalLayout.addWidget(self.difficulty)
        self.gamemode = TransparentPushButton(self.quickMenu)
        self.gamemode.setMinimumSize(QSize(0, 30))
        self.gamemode.setObjectName("gamemode")

        self.verticalLayout.addWidget(self.gamemode)
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

        self.serversStackedWidget.setCurrentIndex(0)
        self.serversTabBar.setAddButtonVisible(False)

        self.setObjectName("ConsoleInterface")

        self.serverMemLabel.setText("内存： NaN")
        self.serverCPULabel.setText("CPU占用：")
        self.subTitleLabel.setText("直观地观察你的服务器的输出，资源占用等。")
        self.titleLabel.setText("终端")
        self.quickMenuTitleLabel.setText("快捷菜单：")
        self.difficulty.addItems(["和平", "简单", "普通", "困难"])
        self.gamemode.setText("游戏模式")
        self.whiteList.setText("白名单")
        self.op.setText("管理员")
        self.kickPlayers.setText("踢人")
        self.banPlayers.setText("封禁/解封")
        self.saveServer.setText("保存存档")
        self.exitServer.setText("关闭服务器")
        self.TitleLabel.setText("请先开启服务器。")
        self.killServer.setText("强制关闭")
        self.gamemode.clicked.connect(self.initQuickMenu_GameMode)
        self.difficulty.currentIndexChanged.connect(self.runQuickMenu_Difficulty)
        self.whiteList.clicked.connect(self.initQuickMenu_WhiteList)
        self.op.clicked.connect(self.initQuickMenu_Operator)
        self.kickPlayers.clicked.connect(self.initQuickMenu_Kick)
        self.banPlayers.clicked.connect(self.initQuickMenu_BanOrPardon)
        self.saveServer.clicked.connect(lambda: self.sendCommand("save-all"))
        self.killServer.clicked.connect(self.runQuickMenu_KillServer)
        # intellisense = QCompleter(GlobalMCSL2Variables.MinecraftBuiltInCommand, self.commandLineEdit)
        # intellisense.setCaseSensitivity(Qt.CaseInsensitive)
        # self.commandLineEdit.setCompleter(intellisense)
        # self.commandLineEdit.setClearButtonEnabled(True)
        self.serverMemProgressRing.setTextVisible(True)
        self.serverCPUProgressRing.setTextVisible(True)

    @pyqtSlot(float)
    def setMemView(self, mem):
        self.serverMemLabel.setText(f"内存：{round(mem, 2)}{serverVariables.memUnit[-1]}")
        self.serverMemProgressRing.setValue(int(int(mem) / serverVariables.maxMem[-1] * 100))

    @pyqtSlot(float)
    def setCPUView(self, cpuPercent):
        self.serverCPUProgressRing.setValue(int(cpuPercent))

    @pyqtSlot(str)
    def colorConsoleText(self, serverOutput):
        fmt = QTextCharFormat()
        greenText = ["INFO", "Info", "info", "tip", "tips", "hint", "提示"]
        orangeText = [
            "WARN",
            "Warning",
            "warn",
            "alert",
            "ALERT",
            "Alert",
            "CAUTION",
            "Caution",
            "警告",
        ]
        redText = [
            "ERR",
            "Err",
            "Fatal",
            "FATAL",
            "Critical",
            "Danger",
            "DANGER",
            "错",
            "at java",
            "at net",
            "at oolloo",
            "Caused by",
            "at sun",
        ]
        blueText = [
            "DEBUG",
            "Debug",
            "debug",
            "调试",
            "TEST",
            "Test",
            "Unknown command",
            "MCSL2",
        ]
        color = [
            QColor(52, 185, 96),
            QColor(196, 139, 33),
            QColor(214, 39, 21),
            QColor(22, 122, 232),
        ]
        for keyword in greenText:
            if keyword in serverOutput:
                fmt.setForeground(QBrush(color[0]))
        for keyword in orangeText:
            if keyword in serverOutput:
                fmt.setForeground(QBrush(color[1]))
        for keyword in redText:
            if keyword in serverOutput:
                fmt.setForeground(QBrush(color[2]))
        for keyword in blueText:
            if keyword in serverOutput:
                fmt.setForeground(QBrush(color[3]))
        self.serverOutput.mergeCurrentCharFormat(fmt)
        serverOutput = serverOutput[:-1].replace("[38;2;170;170;170m", "").replace("[38;2;255;170;0m", "").replace("[38;2;255;255;255m", "").replace("[0m", "").replace("[38;2;255;255;85m", "").replace("[38;2;255;255;255m", "").replace("[3m", "")
        if "Loading libraries, please wait..." in serverOutput:
            self.playersList.clear()
            serverOutput = "[MCSL2 | 提示]：服务器正在启动，请稍后...\n" + serverOutput
            InfoBar.info(
                title="提示",
                content="服务器正在启动，请稍后...",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=2222,
                parent=self,
            )
        self.serverOutput.appendPlainText(serverOutput)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        if " INFO]: Done" in serverOutput:
            fmt.setForeground(QBrush(color[3]))
            self.serverOutput.mergeCurrentCharFormat(fmt)
            self.serverOutput.appendPlainText("[MCSL2 | 提示]：服务器启动完毕！")
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            InfoBar.success(
                title="提示",
                content="服务器启动完毕！",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=2222,
                parent=self,
            )
            readServerProperties()
            self.initQuickMenu_Difficulty()
        if "�" in serverOutput:
            fmt.setForeground(QBrush(color[1]))
            self.serverOutput.mergeCurrentCharFormat(fmt)
            self.serverOutput.appendPlainText(
                "[MCSL2 | 警告]：服务器疑似输出非法字符，也有可能是无法被当前编码解析的字符。请尝试更换编码。"
            )
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            self.serverOutput.setReadOnly(True)
            InfoBar.warning(
                title="警告",
                content="服务器疑似输出非法字符，也有可能是无法被当前编码解析的字符。\n请尝试更换编码。",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=2222,
                parent=self,
            )
        if (
            "logged in with entity id" in serverOutput
            or " left the game" in serverOutput
        ):
            self.recordPlayers(serverOutput)

    def recordPlayers(self, serverOutput: str):
        if "logged in with entity id" in serverOutput:
            self.playersList.append(str(str(serverOutput).split("INFO]: ")[1].split("[/")[0]))
        elif " left the game" in serverOutput:
            try:
                self.playersList.pop(
                    self.playersList.index(str(str(serverOutput).split("INFO]: ")[1].split(" left the game")[0]))
                )
            except Exception:
                pass

    def showServerNotOpenMsg(self):
        """弹出服务器未开启提示"""
        w = MessageBox(
            title="失败",
            content="服务器并未开启，请先开启服务器。",
            parent=self,
        )
        w.yesButton.setText("好")
        w.cancelButton.setParent(None)
        w.exec()

    def sendCommand(self, command):
        if ServerHandler().isServerRunning():
            if command != "":
                ServerHandler().sendCommand(command=command)
                self.commandLineEdit.clear()
                GlobalMCSL2Variables.userCommandHistory.append(command)
                GlobalMCSL2Variables.upT = 0
            else:
                pass
        else:
            w = MessageBox(
                title="失败",
                content="服务器并未开启，请先开启服务器。",
                parent=self,
            )
            w.yesButton.setText("好")
            w.cancelButton.setParent(None)
            w.exec()

    def lineEditChecker(self, text):
        if text != "":
            self.playersControllerBtnEnabled.emit(True)
        else:
            self.playersControllerBtnEnabled.emit(False)

    def getKnownServerPlayers(self) -> str:
        players = "无玩家加入"
        if len(self.playersList):
            players = ""
            for player in self.playersList:
                players += f"{player}\n"
        else:
            pass
        return players

    def initQuickMenu_Difficulty(self):
        """快捷菜单-服务器游戏难度"""
        textDiffiultyList = ["peaceful", "easy", "normal", "hard"]
        if ServerHandler().isServerRunning():
            try:
                self.difficulty.setCurrentIndex(
                    int(serverVariables.serverProperties["difficulty"])
                )
            except ValueError:
                self.difficulty.setCurrentIndex(
                    int(textDiffiultyList.index(serverVariables.serverProperties["difficulty"]))
                )
            except Exception:
                pass
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_Difficulty(self):
        textDiffiultyList = ["peaceful", "easy", "normal", "hard"]
        self.sendCommand(f"difficulty {textDiffiultyList[self.difficulty.currentIndex()]}")

    def initQuickMenu_GameMode(self):
        """快捷菜单-游戏模式"""
        if ServerHandler().isServerRunning():
            gamemodeWidget = playersController()
            gamemodeWidget.mode.addItems(["生存", "创造", "冒险", "旁观"])
            gamemodeWidget.mode.setCurrentIndex(0)
            gamemodeWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=gamemodeWidget.who.text())
            )
            gamemodeWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox("服务器游戏模式", "设置服务器游戏模式", self)
            w.yesButton.setText("确定")
            w.cancelButton.setText("取消")
            w.textLayout.addWidget(gamemodeWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(
                lambda: self.runQuickMenu_GameMode(
                    gamemode=gamemodeWidget.mode.currentIndex(),
                    player=gamemodeWidget.who.text(),
                )
            )
            w.exec()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_GameMode(self, gamemode: int, player: str):
        gameModeList = ["survival", "creative", "adventure", "spectator"]
        ServerHandler().sendCommand(command=f"gamemode {gameModeList[gamemode]} {player}")

    def initQuickMenu_WhiteList(self):
        """快捷菜单-白名单"""
        if ServerHandler().isServerRunning():
            whiteListWidget = playersController()
            whiteListWidget.mode.addItems(["添加(add)", "删除(remove)"])
            whiteListWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=whiteListWidget.who.text())
            )
            whiteListWidget.playersTip.setText(self.getKnownServerPlayers())
            content = (
                "请确保服务器的白名单功能处于启用状态。\n"
                "启用：/whitelist on\n"
                "关闭：/whitelist off\n"
                "列出当前白名单：/whitelist list\n"
                "重新加载白名单：/whitelist reload"
            )
            w = MessageBox("白名单", content, self)
            w.yesButton.setText("确定")
            w.cancelButton.setText("取消")
            w.textLayout.addWidget(whiteListWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(
                lambda: self.runQuickMenu_WhiteList(
                    mode=whiteListWidget.mode.currentIndex(),
                    player=whiteListWidget.who.text(),
                )
            )
            w.exec()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_WhiteList(self, mode: int, player: str):
        whiteListMode = ["add", "remove"]
        ServerHandler().sendCommand(command=f"whitelist {whiteListMode[mode]} {player}")

    def initQuickMenu_Operator(self):
        """快捷菜单-服务器管理员"""
        if ServerHandler().isServerRunning():
            opWidget = playersController()
            opWidget.mode.addItems(["添加", "删除"])
            opWidget.mode.setCurrentIndex(0)
            opWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=opWidget.who.text())
            )
            opWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox("服务器管理员", "添加或删除管理员", self)
            w.yesButton.setText("确定")
            w.cancelButton.setText("取消")
            w.textLayout.addWidget(opWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(
                lambda: self.runQuickMenu_Operator(
                    mode=opWidget.mode.currentIndex(), player=opWidget.who.text()
                )
            )
            w.exec()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_Operator(self, mode: int, player: str):
        commandPrefixList = ["op", "deop"]
        ServerHandler().sendCommand(command=f"{commandPrefixList[mode]} {player}")

    def initQuickMenu_Kick(self):
        """快捷菜单-踢人"""
        if ServerHandler().isServerRunning():
            kickWidget = playersController()
            kickWidget.mode.setParent(None)
            kickWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=kickWidget.who.text())
            )
            kickWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox("踢出玩家", "踢出服务器中的玩家", self)
            w.yesButton.setText("确定")
            w.cancelButton.setText("取消")
            w.textLayout.addWidget(kickWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(
                lambda: self.runQuickMenu_Kick(player=kickWidget.who.text())
            )
            w.exec()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_Kick(self, player: str):
        ServerHandler().sendCommand(command=f"kick {player}")

    def initQuickMenu_BanOrPardon(self):
        """快捷菜单-封禁或解禁玩家"""
        if ServerHandler().isServerRunning():
            banOrPardonWidget = playersController()
            banOrPardonWidget.mode.addItems(["封禁", "解禁"])
            banOrPardonWidget.mode.setCurrentIndex(0)
            banOrPardonWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=banOrPardonWidget.who.text())
            )
            banOrPardonWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox("封禁或解禁玩家", "ban/pardon", self)
            w.yesButton.setText("确定")
            w.cancelButton.setText("取消")
            w.textLayout.addWidget(banOrPardonWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(
                lambda: self.runQuickMenu_BanOrPardon(
                    mode=banOrPardonWidget.mode.currentIndex(),
                    player=banOrPardonWidget.who.text(),
                )
            )
            w.exec()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_BanOrPardon(self, mode: int, player: str):
        commandPrefixList = ["ban", "pardon"]
        ServerHandler().sendCommand(command=f"{commandPrefixList[mode]} {player}")

    def runQuickMenu_StopServer(self):
        if ServerHandler().isServerRunning():
            box = MessageBox("正常关闭服务器", "你确定要关闭服务器吗？", self)
            box.yesSignal.connect(ServerHandler().stopServer)
            box.exec()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_KillServer(self):
        """快捷菜单-强制关闭服务器"""
        if ServerHandler().isServerRunning():
            w = MessageBox("强制关闭服务器", "确定要强制关闭服务器吗？\n有可能导致数据丢失！\n请确保存档已经保存！", self)
            w.yesButton.setText("算了")
            w.cancelButton.setText("强制关闭")
            w.cancelSignal.connect(lambda: ServerHandler().haltServer())
            w.cancelSignal.connect(
                lambda: InfoBar.warning(
                    title="警告",
                    content="正在结束服务器...",
                    orient=Qt.Horizontal,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                    duration=800,
                    parent=self,
                )
            )
            w.exec()
        else:
            self.showServerNotOpenMsg()

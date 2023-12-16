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

from PyQt5.QtCore import QSize, Qt, pyqtSlot, pyqtSignal, QObject, QEvent
from PyQt5.QtGui import QTextCharFormat, QColor, QBrush, QCursor
from PyQt5.QtWidgets import (
    QSpacerItem,
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QFrame,
    QCompleter,
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
    TransparentPushButton,
    FluentIcon as FIF,
    MessageBox,
    InfoBar,
    InfoBarPosition,
    ToggleButton,
    ToolTip,
)
from re import search
from MCSL2Lib.Controllers.serverController import ServerHandler, readServerProperties
from MCSL2Lib.Controllers.serverErrorHandler import ServerErrorHandler
from MCSL2Lib.Widgets.playersControllerMainWidget import playersController
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import ServerVariables, GlobalMCSL2Variables
from MCSL2Lib.utils import MCSL2Logger


serverVariables = ServerVariables()


class ErrorHandlerToggleButton(ToggleButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        self.tip = ToolTip("已开启")
        self.toggled.connect(self.toggleToolTip)

    def toggleToolTip(self):
        if self.isChecked():
            self.tip = ToolTip("已开启")
        else:
            self.tip = ToolTip("已关闭")

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a1.type() == QEvent.ToolTip:
            self.tip.move(QCursor.pos())
            self.tip.show()
            return True
        if a1.type() == QEvent.Leave:
            self.tip.hide()
            return True
        return super().eventFilter(a0, a1)


@Singleton
class ConsolePage(QWidget):
    """终端页"""

    playersControllerBtnEnabled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.errMsg = ""
        self.playersList = []
        self.playersControllerBtnEnabled.emit(False)
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

        self.sendCommandButton = PrimaryToolButton(FIF.SEND, self.titleLimitWidget)
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
        self.errorHandler = ErrorHandlerToggleButton(self.quickMenu)
        self.errorHandler.setMinimumSize(QSize(0, 30))
        self.errorHandler.setObjectName("errorHandler")

        self.verticalLayout.addWidget(self.errorHandler)
        self.gridLayout.addWidget(self.quickMenu, 3, 4, 1, 1)

        self.setObjectName("ConsoleInterface")

        self.serverMemLabel.setText(self.tr("内存： NaN"))
        self.serverCPULabel.setText(self.tr("CPU占用："))
        self.subTitleLabel.setText(self.tr("直观地观察你的服务器的输出，资源占用等。"))
        self.titleLabel.setText(self.tr("终端"))
        self.quickMenuTitleLabel.setText(self.tr("快捷菜单："))
        self.difficulty.addItems([
            self.tr("和平"),
            self.tr("简单"),
            self.tr("普通"),
            self.tr("困难"),
        ])
        self.gamemode.setText(self.tr("游戏模式"))
        self.whiteList.setText(self.tr("白名单"))
        self.op.setText(self.tr("管理员"))
        self.kickPlayers.setText(self.tr("踢人"))
        self.banPlayers.setText(self.tr("封禁/解封"))
        self.saveServer.setText(self.tr("保存存档"))
        self.exitServer.setText(self.tr("关闭服务器"))
        self.killServer.setText(self.tr("强制关闭"))
        self.errorHandler.setText(self.tr("报错分析"))
        self.commandLineEdit.setPlaceholderText(
            self.tr("在此输入指令，回车或点击右边按钮发送，不需要加/")
        )
        self.serverOutput.setPlaceholderText(self.tr("请先开启服务器！不开服务器没有日志的喂"))
        self.sendCommandButton.setEnabled(False)
        self.commandLineEdit.textChanged.connect(
            lambda: self.sendCommandButton.setEnabled(self.commandLineEdit.text() != "")
        )
        self.serverOutput.setReadOnly(True)
        self.sendCommandButton.clicked.connect(
            lambda: self.sendCommand(command=self.commandLineEdit.text())
        )
        self.commandLineEdit.returnPressed.connect(
            lambda: self.sendCommand(command=self.commandLineEdit.text())
        )
        self.gamemode.clicked.connect(self.initQuickMenu_GameMode)
        self.difficulty.currentIndexChanged.connect(self.runQuickMenu_Difficulty)
        self.whiteList.clicked.connect(self.initQuickMenu_WhiteList)
        self.op.clicked.connect(self.initQuickMenu_Operator)
        self.kickPlayers.clicked.connect(self.initQuickMenu_Kick)
        self.banPlayers.clicked.connect(self.initQuickMenu_BanOrPardon)
        self.saveServer.clicked.connect(lambda: self.sendCommand("save-all"))
        self.killServer.clicked.connect(self.runQuickMenu_KillServer)
        intellisense = QCompleter(
            GlobalMCSL2Variables.MinecraftBuiltInCommand, self.commandLineEdit
        )
        intellisense.setCaseSensitivity(Qt.CaseInsensitive)
        self.commandLineEdit.setCompleter(intellisense)
        self.commandLineEdit.setClearButtonEnabled(True)
        self.serverMemProgressRing.setTextVisible(True)
        self.serverCPUProgressRing.setTextVisible(True)
        self.errorHandler.setChecked(False)

    @pyqtSlot(float)
    def setMemView(self, mem):
        self.serverMemLabel.setText(
            self.tr("内存：") + str(round(mem, 2)) + serverVariables.memUnit
        )
        self.serverMemProgressRing.setValue(int(int(mem) / serverVariables.maxMem * 100))

    @pyqtSlot(float)
    def setCPUView(self, cpuPercent):
        self.serverCPUProgressRing.setValue(int(cpuPercent))

    @pyqtSlot(str)
    def colorConsoleText(self, serverOutput):
        readServerProperties()
        fmt = QTextCharFormat()
        # fmt: off
        greenText = ["INFO", "Info", "info", "tip", "tips", "hint", "HINT", "提示"]
        orangeText = ["WARN", "Warning", "warn", "alert", "ALERT", "Alert", "CAUTION", "Caution", "警告"]  # noqa: E501
        redText = ["ERR", "Err", "Fatal", "FATAL", "Critical", "Danger", "DANGER", "错", "at java", "at net", "at oolloo", "Caused by", "at sun"]  # noqa: E501
        blueText = ["DEBUG", "Debug", "debug", "调试", "TEST", "Test", "Unknown command", "MCSL2"]
        color = [QColor(52, 185, 96), QColor(196, 139, 33), QColor(214, 39, 21), QColor(22, 122, 232)]  # noqa: E501
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
        serverOutput = (
            serverOutput.replace("[38;2;170;170;170m", "")
            .replace("[38;2;255;170;0m", "")
            .replace("[38;2;255;255;255m", "")
            .replace("[0m", "")
            .replace("[38;2;255;255;85m", "")
            .replace("[38;2;255;255;0m", "")
            .replace("[38;2;255;85;85m", "")
            .replace("[38;2;255;255;255m", "")
            .replace("[3m", "")
            .replace("[m[", "[")
            .replace("[32m", "")
            .replace("Preparing spawn area", self.tr("准备生成点区域中"))
            .replace("main/INFO", self.tr("主类/信息"))
            .replace("main/WARN", self.tr("主类/警告"))
            .replace("main/ERROR", self.tr("主类/错误"))
            .replace("main/FATAL", self.tr("主类/致命错误"))
            .replace("main/DEBUG", self.tr("主类/调试信息"))
            .replace("INFO", self.tr("信息"))
            .replace("WARN", self.tr("警告"))
            .replace("ERROR", self.tr("错误"))
            .replace("FATAL", self.tr("致命错误"))
            .replace("DEBUG", self.tr("调试信息"))
            .replace("Server thread", self.tr("服务器线程"))
            .replace("Server-Worker", self.tr("服务器工作进程"))
            .replace("DEBUG", self.tr("调试信息"))
            .replace("Forge Version Check", self.tr("Forge版本检查"))
            .replace("ModLauncher running: args", self.tr("ModLauncher运行中: 参数"))
            .replace("All chunks are saved", self.tr("所有区块已保存"))
            .replace("Saving the game (this may take a moment!)", self.tr("保存游戏存档中（可能需要一些时间）"))  # noqa: E501
            .replace("Saved the game", self.tr("已保存游戏存档"))
        )
        if "Disabling terminal, you're running in an unsupported environment." in serverOutput:
            return
        if "Advanced terminal features are not available in this environment" in serverOutput:
            return
        if "Unable to instantiate org.fusesource.jansi.WindowsAnsiOutputStream" in serverOutput:
            return
        if "Loading libraries, please wait..." in serverOutput:
            self.playersList.clear()
            serverOutput = self.tr("[MCSL2 | 提示]：服务器正在启动，请稍后...\n") + serverOutput
            InfoBar.info(
                title=self.tr("提示"),
                content=self.tr("服务器正在启动，请稍后..."),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=2222,
                parent=self,
            )
        self.serverOutput.appendPlainText(serverOutput)
        if search(r"(?=.*Done)(?=.*!)", serverOutput):
            fmt.setForeground(QBrush(color[3]))
            self.serverOutput.mergeCurrentCharFormat(fmt)
            try:
                ip = serverVariables.serverProperties["server-ip"]
                ip = "127.0.0.1" if ip == "" else ip
            except KeyError:
                ip = "127.0.0.1"
            port = serverVariables.serverProperties.get("server-port", 25565)
            self.serverOutput.appendPlainText(
                self.tr("[MCSL2 | 提示]：服务器启动完毕！\n[MCSL2 | 提示]：如果本机开服，IP 地址为") + ip + self.tr("，端口为") + port + self.tr("。\n[MCSL2 | 提示]：如果外网开服,或使用了内网穿透等服务，连接地址为你的相关服务地址。")  # noqa: E501
            )
            InfoBar.success(
                title=self.tr("提示"),
                content=self.tr("服务器启动完毕！\n如果本机开服，IP 地址为") + ip + self.tr("，端口为") + port + self.tr("。\n如果外网开服,或使用了内网穿透等服务，连接地址为你的相关服务地址。"),  # noqa: E501
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self,
            )
            self.initQuickMenu_Difficulty()
        if "�" in serverOutput:
            fmt.setForeground(QBrush(color[1]))
            self.serverOutput.mergeCurrentCharFormat(fmt)
            self.serverOutput.appendPlainText(
                self.tr("[MCSL2 | 警告]：服务器疑似输出非法字符，也有可能是无法被当前编码解析的字符。请尝试更换编码。")  # noqa: E501
            )
            InfoBar.warning(
                title=self.tr("警告"),
                content=self.tr("服务器疑似输出非法字符，也有可能是无法被当前编码解析的字符。\n请尝试更换编码。"),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=2222,
                parent=self,
            )
        if self.errorHandler.isChecked():
            self.errMsg += ServerErrorHandler.detect(serverOutput)
        if (
            "logged in with entity id" in serverOutput
            or " left the game" in serverOutput
        ):
            self.recordPlayers(serverOutput)

    def showErrorHandlerReport(self):
        if self.errorHandler.isChecked():
            if self.errMsg != "":
                w = MessageBox("错误分析器日志", self.errMsg, self)
                w.cancelButton.setParent(None)
                w.show()
            else:
                w = MessageBox(
                    "错误分析器日志", "本次没有检测到任何MCSL2内置错误分析可用解决方案。", self
                )
                w.cancelButton.setParent(None)
                w.show()

    def recordPlayers(self, serverOutput: str):
        if "logged in with entity id" in serverOutput:
            try:
                self.playersList.append(str(str(serverOutput).split("INFO]: ")[1].split("[/")[0]))
                return
            except Exception:
                pass

            try:
                # 若不成功，尝试提取玩家名字
                # [11:49:05] [Server thread/INFO] [minecraft/PlayerList]: Ares_Connor[/127.0.0.1:63854] logged in with entity id 229 at (7.258252218995321, 65.0, 11.09627995098097)  # noqa: E501
                # 提取玩家名字
                name = serverOutput
                name = name.split("]: ")[1].split("[/")[0]
                self.playersList.append(name)
            except Exception as e:
                MCSL2Logger.error(
                    msg=f"extract player name failed\nonRecordPlayers::login {serverOutput}",
                    exc=e,
                )

        elif " left the game" in serverOutput:
            try:
                # fmt: off
                self.playersList.pop(self.playersList.index(str(str(serverOutput).split("INFO]: ")[1].split(" left the game")[0])))  # noqa: E501
                return
            except Exception:
                pass

            try:  # 若不成功，尝试提取玩家名字
                # [11:53:52] [Server thread/INFO] [minecraft/DedicatedServer]: Ares_Connor left the game  # noqa: E501
                name = serverOutput
                name = name.split("]: ")[1].split(" left the game")[0].strip()
                self.playersList.pop(self.playersList.index(name))
            except Exception as e:
                MCSL2Logger.error(
                    msg=f"extract player name failed\nonRecordPlayers::logout {serverOutput}",
                    exc=e,
                )

    def showServerNotOpenMsg(self):
        """弹出服务器未开启提示"""
        w = MessageBox(
            title=self.tr("失败"),
            content=self.tr("服务器并未开启，请先开启服务器。"),
            parent=self,
        )
        w.yesButton.setText(self.tr("好"))
        w.cancelButton.setParent(None)
        w.cancelButton.deleteLater()
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
                title=self.tr("失败"),
                content=self.tr("服务器并未开启，请先开启服务器。"),
                parent=self,
            )
            w.yesButton.setText(self.tr("好"))
            w.cancelButton.deleteLater()
            w.exec()

    def lineEditChecker(self, text):
        if text != "":
            self.playersControllerBtnEnabled.emit(True)
        else:
            self.playersControllerBtnEnabled.emit(False)

    def getKnownServerPlayers(self) -> str:
        players = self.tr("无玩家加入")
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
                self.difficulty.setCurrentIndex(int(serverVariables.serverProperties["difficulty"]))
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
            gamemodeWidget.mode.addItems([
                self.tr("生存"),
                self.tr("创造"),
                self.tr("冒险"),
                self.tr("旁观"),
            ])
            gamemodeWidget.mode.setCurrentIndex(0)
            gamemodeWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=gamemodeWidget.who.text())
            )
            gamemodeWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox(self.tr("服务器游戏模式"), self.tr("设置服务器游戏模式"), self)
            w.yesButton.setText(self.tr("确定"))
            w.cancelButton.setText(self.tr("取消"))
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
            whiteListWidget.mode.addItems([self.tr("添加(add)"), self.tr("删除(remove)")])
            whiteListWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=whiteListWidget.who.text())
            )
            whiteListWidget.playersTip.setText(self.getKnownServerPlayers())
            content = (
                self.tr("请确保服务器的白名单功能处于启用状态。\n")
                + self.tr("启用：/whitelist on\n")
                + self.tr("关闭：/whitelist off\n")
                + self.tr("列出当前白名单：/whitelist list\n")
                + self.tr("重新加载白名单：/whitelist reload")
            )
            w = MessageBox(self.tr("白名单"), content, self)
            w.yesButton.setText(self.tr("确定"))
            w.cancelButton.setText(self.tr("取消"))
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
            opWidget.mode.addItems([self.tr("添加"), self.tr("删除")])
            opWidget.mode.setCurrentIndex(0)
            opWidget.who.textChanged.connect(lambda: self.lineEditChecker(text=opWidget.who.text()))
            opWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox(self.tr("服务器管理员"), self.tr("添加或删除管理员"), self)
            w.yesButton.setText(self.tr("确定"))
            w.cancelButton.setText(self.tr("取消"))
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
            kickWidget.mode.deleteLater()
            kickWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=kickWidget.who.text())
            )
            kickWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox(self.tr("踢出玩家"), self.tr("踢出服务器中的玩家"), self)
            w.yesButton.setText(self.tr("确定"))
            w.cancelButton.setText(self.tr("取消"))
            w.textLayout.addWidget(kickWidget.playersControllerMainWidget)
            self.playersControllerBtnEnabled.connect(w.yesButton.setEnabled)
            w.yesSignal.connect(lambda: self.runQuickMenu_Kick(player=kickWidget.who.text()))
            w.exec()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_Kick(self, player: str):
        ServerHandler().sendCommand(command=f"kick {player}")

    def initQuickMenu_BanOrPardon(self):
        """快捷菜单-封禁或解禁玩家"""
        if ServerHandler().isServerRunning():
            banOrPardonWidget = playersController()
            banOrPardonWidget.mode.addItems([self.tr("封禁"), self.tr("解禁")])
            banOrPardonWidget.mode.setCurrentIndex(0)
            banOrPardonWidget.who.textChanged.connect(
                lambda: self.lineEditChecker(text=banOrPardonWidget.who.text())
            )
            banOrPardonWidget.playersTip.setText(self.getKnownServerPlayers())
            w = MessageBox(self.tr("封禁或解禁玩家"), "ban/pardon", self)
            w.yesButton.setText(self.tr("确定"))
            w.cancelButton.setText(self.tr("取消"))
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
            box = MessageBox(self.tr("正常关闭服务器"), self.tr("你确定要关闭服务器吗？"), self)
            box.yesSignal.connect(ServerHandler().stopServer)
            box.exec()
        else:
            self.showServerNotOpenMsg()

    def runQuickMenu_KillServer(self):
        """快捷菜单-强制关闭服务器"""
        if ServerHandler().isServerRunning():
            w = MessageBox(
                self.tr("强制关闭服务器"),
                self.tr("确定要强制关闭服务器吗？\n有可能导致数据丢失！\n请确保存档已经保存！"),
                self,
            )
            w.yesButton.setText(self.tr("算了"))
            w.cancelButton.setText(self.tr("强制关闭"))
            w.cancelSignal.connect(lambda: ServerHandler().haltServer())
            w.cancelSignal.connect(
                lambda: InfoBar.warning(
                    title=self.tr("警告"),
                    content=self.tr("正在结束服务器..."),
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

# -*- coding: utf-8 -*-
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
Communicate with Minecraft servers.
"""

from datetime import datetime
from os import path as osp
from typing import Optional

from PyQt5.QtCore import QProcess, QObject, pyqtSignal
from MCSL2Lib.variables import ServerVariables
from MCSL2Lib.utils import MCSL2Logger, readFile, writeFile


class _Server:
    """服务器进程"""

    def __init__(self):
        self.process: Optional[QProcess] = None
        self.lastOutputSize = 0


class ServerConfigConstructor:
    @classmethod
    def loadServerConfig(cls, index) -> ServerVariables:
        return ServerVariables().initialize(index=index)


class _ServerProcessBridge(QObject):
    """服务器进程操控器"""

    # 当服务器输出日志时发出的信号(发送一个字符串)
    serverLogOutput = pyqtSignal(str)

    # 当服务器关闭时发出的信号(发送一个整数exit code)
    serverClosed = pyqtSignal(int)

    # 当服务器重启时发出的信号
    serverRestarted = pyqtSignal()

    def __init__(self, v, arg):
        """
        初始化一个服务器处理器
        """
        super().__init__()
        self.config: ServerVariables = v
        self.javaPath: str = self.config.javaPath
        self.processArgs = arg
        self.workingDirectory: str = str(osp.realpath(f"Servers//{self.config.serverName}"))
        self.partialData: str = b""
        self.handledServer = None
        self.serverProcess = self.createServerProcess()

    def createServerProcess(self) -> _Server:
        """
        创建了一个服务器进程对象
        """
        self.handledServer = _Server()
        self.handledServer.process = QProcess()
        self.handledServer.process.setProgram(self.javaPath)
        self.handledServer.process.setArguments(self.processArgs)
        self.handledServer.process.setWorkingDirectory(self.workingDirectory)
        self.handledServer.process.readyReadStandardOutput.connect(self.serverLogOutputHandler)
        self.handledServer.process.finished.connect(
            lambda: self.serverClosed.emit(self.handledServer.process.exitCode())
        )
        # self.handledServer.process.finished.connect(
        #     lambda: self.serverCrashed(self.handledServer.process.exitCode())
        # )
        return self.handledServer

    def serverLogOutputHandler(self):
        """
        When the server outputs change, emit a signal with the updated output.
        """
        newData = self.serverProcess.process.readAllStandardOutput().data()
        self.partialData += newData  # Append the incoming data to the buffer
        lines = self.partialData.split(b"\n")  # Split the buffer into lines
        self.partialData = (
            lines.pop()
        )  # The last element might be incomplete, so keep it in the buffer

        for line in lines:
            newOutput = line.decode(self.config.outputDecoding, errors="replace")
            self.serverLogOutput.emit(newOutput[:-1])

    def startServer(self):
        """
        运行服务器\n
        processArgs: 服务器参数,列表形式，形如["-jar","server.jar","nogui","-Xms1G","-Xmx1G"]\n
        """
        self.serverProcess = self.createServerProcess()
        self.serverProcess.process.start()

    def stopServer(self):
        """
        停止服务器
        """
        if self.isServerRunning():
            self.serverProcess.process.write(b"stop\n")

    def restartServer(self):
        """
        重启服务器
        """
        self.serverProcess.process.write(b"stop\n")
        self.serverProcess.process.waitForFinished()
        self.serverProcess.process.start()
        self.serverRestarted.emit()

    def haltServer(self):
        """
        强制停止服务器
        """
        if self.isServerRunning():
            self.serverProcess.process.kill()
            self.serverProcess.process.waitForFinished()

    def sendCommand(self, command: str):
        """
        用户向服务器发送命令
        """
        self.serverProcess.process.write(f"{command}\n".encode(self.config.inputEncoding))

    def isServerRunning(self):
        if self.serverProcess.process is None:
            return False
        return self.serverProcess.process.state() == QProcess.Running


class _MinecraftEULA:
    """有关Mojang Eula的部分。"""

    def __init__(self, name):
        self.serverDir = f"Servers/{name}"
        self.name = name

    def checkEula(self) -> bool:
        """检查Eula"""
        self.__init__(self.name)
        try:
            # with open(f"{self.serverDir}/eula.txt", "r", encoding="utf-8") as Eula:
            #     EulaText = Eula.readlines()
            # for line in EulaText:
            #     line = line.strip()
            #     if line.startswith("eula"):
            #         if "true" in line:
            #             return True
            #         else:
            #             return False
            #     else:
            #         continue
            t = readFile(f"{self.serverDir}/eula.txt")
            if "eula=true" in t:
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    def acceptEula(self):
        """同意Eula"""
        writeFile(
            f"{self.serverDir}/eula.txt",
            f"# By changing the setting below to TRUE you are indicating your agreement to Mojang EULA (https://aka.ms/MinecraftEULA).\n# Generated by MCSL2. Time: {str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\neula=true",  # noqa: E501
        )


class ServerLauncher:
    """
    启动服务器的调用部分。
    """

    def __init__(self, v: ServerVariables):
        self.config = v

    def start(self):
        """
        供调用的方法。\n
        1.检查Minecraft EULA\n
        2.生成开服命令参数\n
        3.启动进程
        """
        if not (validator := _MinecraftEULA(self.config.serverName)).checkEula():
            return validator
        else:
            self._setJVMArg()
            return self._launch()

    def _setJVMArg(self):
        """生成开服命令参数"""
        self.jvmArg = [
            f"-Xms{self.config.minMem}{self.config.memUnit}",
            f"-Xmx{self.config.maxMem}{self.config.memUnit}",
        ]
        # add jvm args
        if isinstance(self.config.jvmArg, list):
            self.jvmArg.extend(self.config.jvmArg)
        else:
            if self.config.jvmArg:
                self.jvmArg.append(self.config.jvmArg)

        # adjust to different server type
        if self.config.serverType == "forge":
            pass
        else:
            self.jvmArg.append("-jar")
            self.jvmArg.append(f"{self.config.coreFileName}")

        # add "nogui" arg
        self.jvmArg.append("nogui")
        MCSL2Logger.info(f"生成 JVM 参数: \n{self.jvmArg}")

    def _launch(self) -> _ServerProcessBridge:
        """启动进程"""
        (bridge := _ServerProcessBridge(self.config, self.jvmArg)).startServer()
        return bridge

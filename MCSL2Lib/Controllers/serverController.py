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
Communicate with Minecraft servers.
"""

from datetime import datetime
from os import path as osp
from typing import List, Optional

from PyQt5.QtCore import QProcess, QObject, pyqtSignal, QThread, QTimer, pyqtSlot
from psutil import NoSuchProcess, Process, AccessDenied

from MCSL2Lib.Controllers.settingsController import cfg
from MCSL2Lib.utils import readGlobalServerConfig
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import ServerVariables
from MCSL2Lib.utils import MCSL2Logger

serverVariables = ServerVariables()


@Singleton
class ServerHelper(QObject):
    """用以确定开启哪个服务器"""

    serverName = pyqtSignal(str)
    backToHomePage = pyqtSignal(int)
    startBtnStat = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def loadAtLaunch(self):
        """
        读取上次启动的服务器，同时操作获取index。\n
        本方法按理来说不需要被再次调用，一次即可。
        """
        self.readLastServerConfigThread = readLastServerConfigThread(self)
        self.readLastServerConfigThread.start()

    def loadServerConfig(self, index):
        """将选定的服务器的配置加载到变量中"""
        serverVariables.initialize(index=index)

    def selectedServer(self, index):
        """选择了服务器"""
        self.loadServerConfig(index=index)
        self.serverName.emit(readGlobalServerConfig()[index]["name"])
        self.startBtnStat.emit(True)
        # 防止和设置页冲突导致设置无效，得这样写，立刻保存变量以及文件
        cfg.set(cfg.lastServer, readGlobalServerConfig()[index]["name"], save=True)
        self.backToHomePage.emit(0)


class Server:
    """服务器进程，理论不用再改动"""

    def __init__(self):
        self.serverProcess: Optional[QProcess] = None
        self.LastOutputSize = 0


@Singleton
class ServerHandler(QObject):
    """服务器进程操控器"""

    # 当服务器输出日志时发出的信号(发送一个字符串)
    serverLogOutput = pyqtSignal(str)

    # 当服务器关闭时发出的信号(发送一个整数exit code)
    serverClosed = pyqtSignal(int)

    # 当服务器重启时发出的信号
    serverRestarted = pyqtSignal()

    def __init__(self):
        """
        初始化一个服务器处理器
        """
        super().__init__()
        self.javaPath: str = ""
        self.processArgs = [""]
        self.workingDirectory: str = ""
        self.partialData: str = b""
        self.AServer = None
        self.serverLogOutput.connect(MCSL2Logger.info)
        self.Server = self.getServerProcess()

    def getServerProcess(self) -> Server:
        """
        获取一个服务器进程，但是并没有运行，只是创建了一个QProcess对象
        """
        self.AServer = Server()
        self.AServer.serverProcess = QProcess()
        self.AServer.serverProcess.setProgram(self.javaPath)
        self.AServer.serverProcess.setArguments(self.processArgs)
        self.AServer.serverProcess.setWorkingDirectory(self.workingDirectory)
        self.AServer.serverProcess.started.connect(
            lambda: self.serverLogOutput.emit(self.tr("[MCSL2 | 提示]：服务器正在启动，请稍后..."))
        )
        self.AServer.serverProcess.readyReadStandardOutput.connect(
            self.serverLogOutputHandler
        )
        self.AServer.serverProcess.finished.connect(
            lambda: self.serverClosed.emit(self.AServer.serverProcess.exitCode())
        )
        self.AServer.serverProcess.finished.connect(
            lambda: self.serverCrashed(self.AServer.serverProcess.exitCode())
        )
        return self.AServer

    def serverCrashed(self, exitCode):
        if exitCode:
            if exitCode != 62097:
                self.serverLogOutput.emit(self.tr("[MCSL2 | 提示]：服务器崩溃！"))
                if cfg.get(cfg.restartServerWhenCrashed):
                    self.Server.serverProcess.waitForFinished()
                    self.serverLogOutput.emit(self.tr("[MCSL2 | 提示]：正在重新启动服务器..."))
                    self.Server.serverProcess.start()
            else:
                self.serverLogOutput.emit(self.tr("[MCSL2 | 提示]：服务器崩溃，但可能是被强制结束进程。"))
        else:
            self.serverLogOutput.emit(self.tr("[MCSL2 | 提示]：服务器已关闭！"))

    def serverLogOutputHandler(self):
        """
        When the server outputs change, emit a signal with the updated output.
        """
        newData = self.Server.serverProcess.readAllStandardOutput().data()
        self.partialData += newData  # Append the incoming data to the buffer
        lines = self.partialData.split(b"\n")  # Split the buffer into lines
        self.partialData = (
            lines.pop()
        )  # The last element might be incomplete, so keep it in the buffer

        for line in lines:
            newOutput = line.decode(serverVariables.outputDecoding, errors="replace")
            self.serverLogOutput.emit(newOutput[:-1])

    def startServer(self, javaPath: str, processArgs: List[str], workingDirectory: str):
        """
        运行服务器\n
        javaPath: Java路径\n
        processArgs: 服务器参数,列表形式，形如["-jar","server.jar","nogui","-Xms1G","-Xmx1G"]\n
        """
        self.javaPath = javaPath
        self.processArgs = processArgs
        self.workingDirectory = workingDirectory
        self.Server = self.getServerProcess()
        self.Server.serverProcess.start()

    def stopServer(self):
        """
        停止服务器
        """
        if self.isServerRunning():
            if cfg.get(cfg.sendStopInsteadOfKill):
                self.Server.serverProcess.write(b"stop\n")
                # self.Server.serverProcess.waitForFinished()
            else:
                self.haltServer()

    def restartServer(self):
        """
        重启服务器
        """
        self.Server.serverProcess.write(b"stop\n")
        self.Server.serverProcess.waitForFinished()
        self.Server.serverProcess.start()
        self.serverRestarted.emit()

    def haltServer(self):
        """
        强制停止服务器
        """
        if self.isServerRunning():
            self.Server.serverProcess.kill()
            self.Server.serverProcess.waitForFinished()

    def sendCommand(self, command: str):
        """
        用户向服务器发送命令
        """
        self.Server.serverProcess.write(
            f"{command}\n".encode(serverVariables.inputEncoding)
        )

    def isServerRunning(self):
        if self.Server.serverProcess is None:
            return False
        return self.Server.serverProcess.state() == QProcess.Running


@Singleton
class MojangEula:
    """有关Mojang Eula的部分。"""

    def __init__(self):
        self.serverDir = f".//Servers//{serverVariables.serverName}"

    def checkEula(self) -> bool:
        """检查Eula"""
        self.__init__()
        try:
            with open(f"{self.serverDir}/eula.txt", "r", encoding="utf-8") as Eula:
                EulaText = Eula.readlines()
            for line in EulaText:
                line = line.strip()
                if line.startswith("eula"):
                    if "true" in line:
                        return True
                    else:
                        return False
                else:
                    continue
        except FileNotFoundError:
            return False

    def acceptEula(self):
        """同意Eula"""
        with open(f"{self.serverDir}//eula.txt", "w+", encoding="utf-8") as Eula:
            Eula.write(
                f"#By changing the setting below to TRUE you are indicating your agreement to Mojang EULA (https://aka.ms/MinecraftEULA).\n#Generated by MCSL2. Time: {str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\neula=true"
            )


@Singleton
class ServerLauncher:
    """
    启动服务器的调用部分。
    """

    def __init__(self):
        self.jvmArg: List[str] = [""]
        self.javaPath: str = ""

    def startServer(self) -> bool:
        """
        供调用的方法。\n
        1.检查Mojang Eula\n
        2.生成开服命令参数\n
        3.启动进程
        """
        if not MojangEula().checkEula():
            return False
        else:
            self.reGetNewJava()
            self.setjvmArg()
            self.launch()
            return True

    def reGetNewJava(self):
        self.javaPath = serverVariables.javaPath

    def setjvmArg(self):
        """生成开服命令参数"""
        self.jvmArg = [
            f"-Xms{serverVariables.minMem}{serverVariables.memUnit}",
            f"-Xmx{serverVariables.maxMem}{serverVariables.memUnit}",
        ]
        # add jvm args
        if isinstance(serverVariables.jvmArg, list):
            self.jvmArg.extend(serverVariables.jvmArg)
        else:
            if serverVariables.jvmArg:
                self.jvmArg.append(serverVariables.jvmArg)

        # adjust to different server type
        if serverVariables.serverType == "forge":
            pass
        else:
            self.jvmArg.append("-jar")
            self.jvmArg.append(f"{serverVariables.coreFileName}")

        # add "nogui" arg
        self.jvmArg.append("nogui")
        MCSL2Logger.info(f"生成JVM参数：\n{self.jvmArg}")

    def launch(self):
        """启动进程"""
        ServerHandler().startServer(
            javaPath=self.javaPath,
            processArgs=self.jvmArg,
            workingDirectory=str(
                osp.realpath(f"Servers//{serverVariables.serverName}")
            ),
        )


class readLastServerConfigThread(QThread):
    """读取上次运行的服务器，考虑到可能服务器比较多导致读取拖慢程序启动所以使用多线程"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        # 不应该在这里直接启用启动服务器按钮，应先获取index补全服务器配置。
        lastServerName = cfg.get(cfg.lastServer)
        if lastServerName != "":
            # 不加try小心服务器删了又得boom
            try:
                globalServerList = readGlobalServerConfig()
                serverNameList: list = []
                for i in range(len(globalServerList)):
                    serverNameList.append(globalServerList[i]["name"])
                ServerHelper().loadServerConfig(
                    index=serverNameList.index(lastServerName)
                )
                ServerHelper().startBtnStat.emit(True)
                ServerHelper().serverName.emit(lastServerName)
            except Exception:
                ServerHelper().startBtnStat.emit(False)
        else:
            ServerHelper().startBtnStat.emit(False)


class MinecraftServerResMonitorUtil(QObject):
    """
    获取服务器资源占用的线程
    """

    memPercent = pyqtSignal(float)
    cpuPercent = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MinecraftServerResMonitorThread")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getServerMem)
        self.timer.timeout.connect(self.getServerCPU)
        self.timer.start(1000)  # 每隔1秒获取一次

    def getServerMem(self):
        divisionNumList = {"G": 1073741824, "M": 1048576}
        divisionNum = divisionNumList[serverVariables.memUnit]
        try:
            if ServerHandler().isServerRunning():
                serverMem = (
                    Process(ServerHandler().AServer.serverProcess.processId())
                    .memory_full_info()
                    .uss
                    / divisionNum
                )
                self.memPercent.emit(float("{:.4f}".format(serverMem)))
            else:
                self.memPercent.emit(0.0000)
        except NoSuchProcess:
            pass
        except PermissionError:
            pass
        except AccessDenied:
            pass

    def getServerCPU(self):
        try:
            if ServerHandler().isServerRunning():
                serverCPU = Process(
                    ServerHandler().AServer.serverProcess.processId()
                ).cpu_percent(interval=0.01)
                self.cpuPercent.emit(float("{:.4f}".format(serverCPU / 10)))
            else:
                self.cpuPercent.emit(0.0000)
        except NoSuchProcess:
            pass
        except PermissionError:
            pass
        except AccessDenied:
            pass

    @pyqtSlot(int)
    def onServerClosedHandler(self, _):
        self.cpuPercent.emit(0.0)
        self.memPercent.emit(0.0)
        self.timer.stop()


def readServerProperties():
    serverVariables.serverProperties.clear()
    try:
        with open(
            f"./Servers/{serverVariables.serverName}/server.properties", "r"
        ) as serverPropertiesFile:
            lines = serverPropertiesFile.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    serverVariables.serverProperties[key.strip()] = value.strip()
    except FileNotFoundError:
        serverVariables.serverProperties.update({"msg": "File not found"})

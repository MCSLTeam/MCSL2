#     Copyright 2023, MCSL Team, mailto:lxhtz.dl@qq.com
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
'''
Communicate with Minecraft servers.
'''

from json import dumps, loads
from os.path import realpath
from typing import List, Optional
from MCSL2Lib.singleton import Singleton
from PyQt5.QtCore import QProcess, QObject, pyqtSignal
from MCSL2Lib.settingsController import SettingsController
settingsController = SettingsController()

def readGlobalServerConfig():
    '''读取全局服务器配置'''
    with open(r'MCSL2/MCSL2_ServerList.json', "r", encoding='utf-8') as globalServerConfigFile:
        globalServerList = loads(globalServerConfigFile.read())[
            'MCSLServerList']
        globalServerConfigFile.close()
    return globalServerList

@Singleton
class ServerHelper(QObject):
    '''用以确定开启哪个服务器'''
    serverName = pyqtSignal(str)
    backToHomePage = pyqtSignal(int)
    startBtnStat = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def loadAtLaunch(self):
        '''读取上次启动的服务器'''
        lastServerName = settingsController.fileSettings['lastServer']
        if lastServerName != "":
            self.serverName.emit(lastServerName)
            self.startBtnStat.emit(True)
        else:
            self.startBtnStat.emit(False)

    def selectedServer(self, index):
        '''选择了服务器'''
        self.serverName.emit(readGlobalServerConfig()[index]['name'])
        self.backToHomePage.emit(0)
        self.startBtnStat.emit(True)
        # 防止和设置页冲突导致设置无效，得这样写
        settingsController.unSavedSettings.update({"lastServer": readGlobalServerConfig()[index]['name']})
        settingsController.fileSettings.update(settingsController.unSavedSettings)
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as writeConfig:
            writeConfig.write(dumps(settingsController.fileSettings, indent=4))
            writeConfig.close()


class Server:
    '''服务器进程'''
    def __init__(self):
        self.serverProcess: Optional[QProcess] = None
        self.LastOutputSize = 0

class ServerHandler(QObject):
    '''服务器进程操控器'''

    # 当服务器输出日志时发出的信号(发送一个字符串)
    serverLogOutput = pyqtSignal(str)

    # 当服务器关闭时发出的信号(发送一个整数exit code)
    serverClosed = pyqtSignal(int)

    # 当服务器重启时发出的信号
    serverRestarted = pyqtSignal()

    def __init__(self, javaPath: str, processArgs: List[str], workingDirectory: str):
        """
        初始化一个服务器处理器
        JavaPath:Java路径
        Args:服务器参数,列表形式，形如["-jar","server.jar","nogui","-Xms1G","-Xmx1G"]
        """
        super().__init__()
        self.javaPath = javaPath
        self.processArgs = processArgs
        self.workingDirectory = workingDirectory
        self.Server = self.getServerProcess()


    def getServerProcess(self) -> Server:
        """
        获取一个服务器进程，但是并没有运行，只是创建了一个QProcess对象
        """
        server = Server()
        server.serverProcess = QProcess()
        server.serverProcess.setProgram(self.javaPath)
        server.serverProcess.setArguments(self.processArgs)
        server.serverProcess.setWorkingDirectory(self.workingDirectory)
        server.serverProcess.readyReadStandardOutput.connect(
            self.serverLogOutputHandler)
        server.serverProcess.finished.connect(
            lambda: self.serverClosed.emit(server.serverProcess.exitCode()))

        return server

    def serverLogOutputHandler(self):
        """
        当服务器输出有变化时，发射信号，发送新的输出(更新的部分)
        """
        NewData = self.Server.serverProcess.readAllStandardOutput()
        DataSize = NewData.size()
        if DataSize > self.Server.LastOutputSize:
            # 截取新的输出,由于data可能会达到MB级别，所以使用memoryview来对付QByteArray
            NewOutput = memoryview(NewData)[self.Server.LastOutputSize:DataSize].tobytes(
            ).decode(MCSL2Settings.ConsoleOutputEncoding)
            self.serverLogOutput.emit(NewOutput)
            self.Server.LastOutputSize = DataSize

    def startServer(self):
        """
        运行服务器
        """
        self.Server.serverProcess.start()

    def stopServer(self):
        """
        停止服务器
        """
        if MCSL2Settings.SendStopInsteadOfKill == True:
            self.Server.serverProcess.write(b"stop\n")
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
        self.Server.serverProcess.kill()
        self.Server.serverProcess.waitForFinished()

    def sendCommand(self, Command: str):
        """
        用户向服务器发送命令
        """
        self.Server.serverProcess.write(f"{Command}\n".encode(
            MCSL2Settings.ConsoleInputDecoding))

    def isServerRunning(self):
        return self.Server.serverProcess.state() == QProcess.Running

class ServerLauncher:
    def __init__(self):
        self.GetMonitor = None
        self.Monitor = None
        self.MaxMemory = None
        self.MinMemory = None
        self.MemoryUnit = None
        self.ServerName = None
        self.JavaPath = None
        self.CoreName = None
        self.CoreFolder = None
        self.JVMArg = None
        self.EnableJVMArg = False

    def getGlobalServerConfig(self, ServerIndexNum):
        with open(r"MCSL2/MCSL2_ServerList.json", "r", encoding="utf-8") as ReadGlobalConfig:
            GlobalJson = loads(ReadGlobalConfig.read())
            ServerConfig = GlobalJson['MCSLServerList'][int(ServerIndexNum)]
            self.ServerName = ServerConfig['name']
            self.CoreName = ServerConfig['core_file_name']
            self.CoreFolder = realpath(f"./Servers/{self.ServerName}/")
            self.MinMemory = ServerConfig['min_memory']
            self.MaxMemory = ServerConfig['max_memory']
            self.MemoryUnit = ServerConfig['memory_unit']
            self.JavaPath = ServerConfig['java_path']
            if ServerConfig['jvm_arg'] != "":
                self.EnableJVMArg = True
                self.JVMArg = ServerConfig['jvm_arg']
            else:
                self.EnableJVMArg = False
            ReadGlobalConfig.close()
        self.setLaunchCommand()

    def setLaunchCommand(self):
        if self.EnableJVMArg == True:
            LaunchArg = [f"-Xms{self.MinMemory}{self.MemoryUnit}", f"-Xmx{self.MaxMemory}{self.MemoryUnit}",
                         f"{self.JVMArg}", "-jar", f"{self.CoreFolder}\\{self.CoreName}"]
        else:
            LaunchArg = [f"-Xms{self.MinMemory}{self.MemoryUnit}",
                         f"-Xmx{self.MaxMemory}{self.MemoryUnit}", "-jar", f"{self.CoreFolder}\\{self.CoreName}"]
        if self.checkEulaAcceptStatus(self.CoreFolder) == True:
            self.launch(LaunchArg)
        else:
            ReturnStatus = CallMCSL2Dialog(
                Tip="ServerControllerNoAcceptedMojangEula",
                OtherTextArg=None,
                isNeededTwoButtons=1, ButtonArg="确定|取消")
            if ReturnStatus == 1:
                self.acceptEula(self.CoreFolder)
                self.launch(LaunchArg)
            else:
                pass

    def checkEulaAcceptStatus(self, CoreFolder):
        try:
            with open(f"{CoreFolder}/eula.txt", "r", encoding="utf-8") as Eula:
                EulaText = str(Eula.read())
                print(EulaText)
                if "eula=true" in EulaText:
                    return True
                else:
                    return False
        except:
            return False

    def acceptEula(self, CoreFolder):
        with open(f"{CoreFolder}/eula.txt", "w+", encoding="utf-8") as AcceptEula:
            AcceptEula.write("eula=true")
            AcceptEula.close()

    def launch(self, LaunchArg):
        print(self.JavaPath)
        ServerHandler(processArgs=LaunchArg, javaPath=self.JavaPath,
                      workingDirectory=str(realpath(f"{self.CoreFolder}"))).startServer()

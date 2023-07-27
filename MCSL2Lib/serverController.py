from json import loads, dumps
from os import mkdir
from os.path import realpath
from shutil import copy
from typing import List, Optional

from PyQt5.QtCore import QProcess, QObject, pyqtSignal


def readGlobalServerConfig():
    with open(r'MCSL2/MCSL2_ServerList.json', "r", encoding='utf-8') as globalServerConfigFile:
        globalServerList = loads(globalServerConfigFile.read())[
            'MCSLServerList']
        globalServerConfigFile.close()
    return globalServerList


class Server:
    def __init__(self):
        self.Process: Optional[QProcess] = None
        self.LastOutputSize = 0


class ServerHandler(QObject):
    # 当服务器输出日志时发出的信号(发送一个字符串)
    ServerLogOutput = pyqtSignal(str)

    # 当服务器关闭时发出的信号(发送一个整数exit code)
    ServerClosed = pyqtSignal(int)

    # 当服务器重启时发出的信号
    ServerRestarted = pyqtSignal()

    def __init__(self, JavaPath: str, Args: List[str], WorkingDirectory: str):
        """
        初始化一个服务器处理器
        JavaPath:Java路径
        Args:服务器参数,列表形式，形如["-jar","server.jar","nogui","-Xms1G","-Xmx1G"]
        """
        super().__init__()
        self.JavaPath = JavaPath
        self.Args = Args
        self.WorkingDirectory = WorkingDirectory
        self.Server = self.GetServerProcess()

    def GetServerProcess(self) -> Server:
        """
        获取一个服务器进程，但是并没有运行，只是创建了一个QProcess对象
        """
        server = Server()
        server.Process = QProcess()
        server.Process.setProgram(self.JavaPath)
        server.Process.setArguments(self.Args)
        server.Process.setWorkingDirectory(self.WorkingDirectory)
        server.Process.readyReadStandardOutput.connect(
            self.ServerLogOutputHandler)
        server.Process.finished.connect(
            lambda: self.ServerClosed.emit(server.Process.exitCode()))

        return server

    def ServerLogOutputHandler(self):
        """
        当服务器输出有变化时，发射信号，发送新的输出(更新的部分)
        """
        NewData = self.Server.Process.readAllStandardOutput()
        DataSize = NewData.size()
        if DataSize > self.Server.LastOutputSize:
            # 截取新的输出,由于data可能会达到MB级别，所以使用memoryview来对付QByteArray
            NewOutput = memoryview(NewData)[self.Server.LastOutputSize:DataSize].tobytes(
            ).decode(MCSL2Settings.ConsoleOutputEncoding)
            self.ServerLogOutput.emit(NewOutput)
            self.Server.LastOutputSize = DataSize

    def StartServer(self):
        """
        运行服务器
        """
        self.Server.Process.start()

    def StopServer(self):
        """
        停止服务器
        """
        if MCSL2Settings.SendStopInsteadOfKill == True:
            self.Server.Process.write(b"stop\n")
        else:
            self.HaltServer()

    def RestartServer(self):
        """
        重启服务器
        """
        self.Server.Process.write(b"stop\n")
        self.Server.Process.waitForFinished()
        self.Server.Process.start()
        self.ServerRestarted.emit()

    def HaltServer(self):
        """
        强制停止服务器
        """
        self.Server.Process.kill()
        self.Server.Process.waitForFinished()

    def SendCommand(self, Command: str):
        """
        用户向服务器发送命令
        """
        self.Server.Process.write(f"{Command}\n".encode(
            MCSL2Settings.ConsoleInputDecoding))

    def IsServerRunning(self):
        return self.Server.Process.state() == QProcess.Running


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

    def GetGlobalServerConfig(self, ServerIndexNum):
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
        self.SetLaunchCommand()

    def SetLaunchCommand(self):
        if self.EnableJVMArg == True:
            LaunchArg = [f"-Xms{self.MinMemory}{self.MemoryUnit}", f"-Xmx{self.MaxMemory}{self.MemoryUnit}",
                         f"{self.JVMArg}", "-jar", f"{self.CoreFolder}\\{self.CoreName}"]
        else:
            LaunchArg = [f"-Xms{self.MinMemory}{self.MemoryUnit}",
                         f"-Xmx{self.MaxMemory}{self.MemoryUnit}", "-jar", f"{self.CoreFolder}\\{self.CoreName}"]
        if self.CheckEulaAcceptStatus(self.CoreFolder) == True:
            self.Launch(LaunchArg)
        else:
            ReturnStatus = CallMCSL2Dialog(
                Tip="ServerControllerNoAcceptedMojangEula",
                OtherTextArg=None,
                isNeededTwoButtons=1, ButtonArg="确定|取消")
            if ReturnStatus == 1:
                self.AcceptEula(self.CoreFolder)
                self.Launch(LaunchArg)
            else:
                pass

    def CheckEulaAcceptStatus(self, CoreFolder):
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

    def AcceptEula(self, CoreFolder):
        with open(f"{CoreFolder}/eula.txt", "w+", encoding="utf-8") as AcceptEula:
            AcceptEula.write("eula=true")
            AcceptEula.close()

    def Launch(self, LaunchArg):
        print(self.JavaPath)
        ServerHandler(Args=LaunchArg, JavaPath=self.JavaPath,
                      WorkingDirectory=str(realpath(f"{self.CoreFolder}"))).StartServer()

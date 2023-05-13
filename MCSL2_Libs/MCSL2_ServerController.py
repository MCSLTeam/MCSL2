from json import loads, dumps
from os import mkdir
from os.path import realpath
from shutil import copy

from PyQt5.QtCore import QProcess

from MCSL2_Libs.MCSL2_Dialog import CallMCSL2Dialog
from MCSL2_Libs.MCSL2_Settings import MCSL2Settings


def CheckAvailableSaveServer(ChkVal):
    if ChkVal[0] == 1:
        if ChkVal[1] == 1:
            if ChkVal[2] == 1:
                if ChkVal[3] == 1:
                    if ChkVal[4] == 1:
                        CanCreate = 1
                        Tip = "ConfigPageBeginToSetUpServer"
                        Log = "AllConfigIsOK"
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerCore"
                        Log = Tip
                else:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoJava"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNoJavaAndServerCore"
                        Log = Tip
            else:
                if ChkVal[3] == 1:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerName"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerNameAndServerCore"
                        Log = Tip
                else:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerNameAndJava"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageOnlyMinMemoryAndMaxMemory"
                        Log = Tip
        else:
            if ChkVal[2] == 1:
                if ChkVal[3] == 1:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoMaxMemory"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNoMaxMemoryAndServerCore"
                        Log = Tip
                else:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoMaxMemoryAndJava"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerCoreAndJavaAndMaxMemory"
                        Log = Tip
            else:
                if ChkVal[3] == 1:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerNameAndMaxMemory"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerCodeAndServerNameAndMaxMemory"
                        Log = Tip
                else:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoJavaAndServerNameAndMaxMemory"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageOnlyMinMemory"
                        Log = Tip
    else:
        if ChkVal[1] == 1:
            if ChkVal[2] == 1:
                if ChkVal[3] == 1:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoMinMemory"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerCoreAndMinMemory"
                        Log = Tip
                else:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoJavaAndMinMemory"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerCoreAndJavaAndMinMemory"
                        Log = Tip
            else:
                if ChkVal[3] == 1:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerNameAndMinMemory"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerCoreAndServerNameAndMinMemory"
                        Log = Tip
                else:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoJavaAndServerNameAndMinMemory"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageOnlyMaxMemory"
                        Log = Tip
        else:
            if ChkVal[2] == 1:
                if ChkVal[3] == 1:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoMinMemoryAndMaxMemory"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerCoreAndMinMemoryAndMaxMemory"
                        Log = Tip
                else:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoJavaAndMinMemoryAndMaxMemory"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageOnlyServerName"
                        Log = Tip
            else:
                if ChkVal[3] == 1:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageNoServerNameAndMinMemoryAndMaxMemory"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageOnlyJava"
                        Log = Tip
                else:
                    if ChkVal[4] == 1:
                        CanCreate = 0
                        Tip = "ConfigPageOnlyServerCore"
                        Log = Tip
                    else:
                        CanCreate = 0
                        Tip = "ConfigPageNothing"
                        Log = Tip
                        # 终于写完了.jpg
                        # 终于改完了.png
    return CanCreate, Tip, Log


def SaveServer(ServerName, CorePath, JavaPath, MinMemory, MaxMemory, CoreFileName, AddServerType):
    global GlobalServerList
    MemoryUnits = ["M", "G"]
    MemoryUnit = None
    if AddServerType == "noob":
        MemoryUnit = MemoryUnits[0]
    elif AddServerType == "extended_m":
        MemoryUnit = MemoryUnits[0]
    elif AddServerType == "extended_g":
        MemoryUnit = MemoryUnits[1]
    ServerFolderPath = "./Servers/" + ServerName
    mkdir(ServerFolderPath)
    copy(CorePath, ServerFolderPath)
    ServerConfigDict = {
        "name": str(ServerName),
        "core_file_name": str(CoreFileName),
        "java_path": str(JavaPath),
        "min_memory": int(MinMemory),
        "max_memory": int(MaxMemory),
        "memory_unit": str(MemoryUnit),
        "jvm_arg": ""
    }
    with open(r'MCSL2/MCSL2_ServerList.json', "r", encoding='utf-8') as ReadGlobalServerListFile:
        GlobalServerList = loads(ReadGlobalServerListFile.read())
        GlobalServerList['MCSLServerList'].append(ServerConfigDict)
        ReadGlobalServerListFile.close()
    with open(r'MCSL2/MCSL2_ServerList.json', "w", encoding='utf-8') as WriteGlobalServerListFile:
        WriteGlobalServerListFile.write(dumps(GlobalServerList))
        WriteGlobalServerListFile.close()

    ConfigPath = f"Servers//{ServerName}//MCSL2ServerConfig.json"
    with open(ConfigPath, "w+") as SaveConfig:
        SaveConfig.write(str(dumps(ServerConfigDict)))
        SaveConfig.close()
    Tip = "服务器部署完毕！"

    CallMCSL2Dialog(Tip, OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)


def ReadGlobalServerConfig():
    with open(r'MCSL2/MCSL2_ServerList.json', "r", encoding='utf-8') as ReadGlobalServerConfigFile:
        GlobalServerList = loads(ReadGlobalServerConfigFile.read())['MCSLServerList']
        ServerCount = len(GlobalServerList)
        ReadGlobalServerConfigFile.close()
    return ServerCount, GlobalServerList


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
            LaunchCommand = f"\"{self.JavaPath}\" -Xms{self.MinMemory}{self.MemoryUnit} -Xmx{self.MaxMemory}{self.MemoryUnit} {self.JVMArg} -jar {self.CoreFolder}\\{self.CoreName}"
        else:
            LaunchCommand = f"\"{self.JavaPath}\" -Xms{self.MinMemory}{self.MemoryUnit} -Xmx{self.MaxMemory}{self.MemoryUnit} -jar {self.CoreFolder}\\{self.CoreName}"
        if self.CheckEulaAcceptStatus(self.CoreFolder) == True:
            self.Launch(LaunchCommand)
        else:
            ReturnStatus = CallMCSL2Dialog(
                Tip="ServerControllerNoAcceptedMojangEula",
                OtherTextArg=None,
                isNeededTwoButtons=1, ButtonArg="确定|取消")
            if ReturnStatus == 1:
                self.AcceptEula(self.CoreFolder)
                self.Launch(LaunchCommand)
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

    def Launch(self, LaunchCommand):
        RealServerWorkingDirectory = realpath(f"{self.CoreFolder}")
        StartGetServerOutput(LaunchCommand, cwd=str(RealServerWorkingDirectory))


class StartGetServerOutput(QProcess):
    def __init__(self, LaunchCommand, cwd):
        super().__init__()
        self.setWorkingDirectory(cwd)
        self.setProcessChannelMode(QProcess.MergedChannels)
        self.readyReadStandardOutput.connect(self.on_readyReadStandardOutput)
        self.start(LaunchCommand)

    def on_readyReadStandardOutput(self):
        DecodeType = MCSL2Settings().GetConfig("ConsoleOutputEncoding")
        output = self.readAllStandardOutput().data().decode(DecodeType)
        print(output.strip('\r\n'))
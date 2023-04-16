from json import loads, dumps
from os import mkdir
from os.path import realpath
from shutil import copy
from subprocess import Popen, PIPE

from MCSL2_Libs.MCSL2_Dialog import CallMCSL2Dialog


class ServerSaver:
    def __init__(self):
        pass

    def CheckAvailableSaveServer(ChkVal):
        if (ChkVal[0] == 1):
            if (ChkVal[1] == 1):
                if (ChkVal[2] == 1):
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 1
                            Tip = "关闭此窗口后，\n\n服务器将会开始部署。"
                        else:
                            CanCreate = 0
                            Tip = "只剩服务器核心没设置好力\n\n（喜"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩Java没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "只剩Java和服务器核心没设置好力\n\n（喜"
                else:
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩服务器名称没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "只剩服务器名称和服务器核心没设置好力\n\n（喜"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩服务器名称和Java没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "你只设置好了内存\n\n（恼"
            else:
                if (ChkVal[2] == 1):
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩最大内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "只剩最大内存和服务器核心没设置好力\n\n（喜"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩最大内存和Java没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "服务器核心、Java和最大内存还没设置好呢\n\n（恼"
                else:
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩服务器名称和最大内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "服务器核心、服务器名称和最大内存还没设置好呢\n\n（恼"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "Java、服务器名称和最大内存还没设置好呢\n\n（恼"
                        else:
                            CanCreate = 0
                            Tip = "你只设置好了最小内存\n\n（恼"
        else:
            if (ChkVal[1] == 1):
                if (ChkVal[2] == 1):
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩最小内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "只剩服务器核心和最小内存没设置好力\n\n（喜"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩Java和最小内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "服务器核心、Java和最小内存还没设置好呢\n\n（恼"
                else:
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩服务器名称和最小内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "服务器核心、服务器名称和最小内存还没设置好呢\n\n（恼"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "Java、服务器名称和最小内存还没设置好呢\n\n（恼"
                        else:
                            CanCreate = 0
                            Tip = "你只设置好了最大内存\n\n（恼"
            else:
                if (ChkVal[2] == 1):
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "服务器核心和内存还没设置好呢\n\n（恼"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "Java和内存还没设置好呢\n\n（恼"
                        else:
                            CanCreate = 0
                            Tip = "你只设置好了服务器名称\n\n（恼"
                else:
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "服务器名称和内存还没设置好呢\n\n（恼"
                        else:
                            CanCreate = 0
                            Tip = "你只设置好了Java\n\n（恼"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "你只设置好了服务器核心\n\n（恼"
                        else:
                            CanCreate = 0
                            Tip = "你什么都没设置好呢\n\n（恼"
                            # 终于写完了.jpg
        return CanCreate, Tip

    def SaveServer(self, Tip, ServerName, CorePath, JavaPath, MinMemory, MaxMemory, CoreFileName):
        global GlobalServerList
        CallMCSL2Dialog(Tip, isNeededTwoButtons=0, ButtonArg=None)
        ServerFolderPath = "./Servers/" + ServerName
        mkdir(ServerFolderPath)
        copy(CorePath, ServerFolderPath)
        ServerConfigDict = {
            "name": ServerName,
            "core_file_name": CoreFileName,
            "java_path": JavaPath,
            "min_memory": MinMemory,
            "max_memory": MaxMemory,
            "jvm_arg": ""
        }
        ServerConfigJson = dumps(ServerConfigDict, ensure_ascii=False)
        with open(r'MCSL2/MCSL2_ServerList.json', "r", encoding='utf-8') as ReadGlobalServerListFile:
            GlobalServerList = loads(ReadGlobalServerListFile.read())
            print(GlobalServerList)
            print(type(GlobalServerList))
            ServerCount = len(GlobalServerList)
            print(ServerCount)
            GlobalServerList['MCSLServerList'].append(ServerConfigDict)
            ReadGlobalServerListFile.close()
        with open(r'MCSL2/MCSL2_ServerList.json', "w", encoding='utf-8') as WriteGlobalServerListFile:
            WriteGlobalServerListFile.write(dumps(GlobalServerList))
            WriteGlobalServerListFile.close()

        print(ServerConfigJson)
        ConfigPath = "Servers//" + ServerName + "//" + "MCSL2ServerConfig.json"
        with open(ConfigPath, "w+") as SaveConfig:
            SaveConfig.write(ServerConfigJson)
            SaveConfig.close()
        SaveConfig = open(ConfigPath, "w+")
        SaveConfig.write(ServerConfigJson)
        SaveConfig.close()
        Tip = "服务器部署完毕！"

        CallMCSL2Dialog(Tip, isNeededTwoButtons=0, ButtonArg=None)


class ServerLauncher:
    def __init__(self, ServerGlobalIndex):
        self.ServerGlobalIndex = ServerGlobalIndex
        self.MaxMemory = None
        self.MinMemory = None
        self.ServerName = None
        self.JavaPath = None
        self.CoreName = None
        self.CoreFolder = None
        self.JVMArg = None
        self.EnableJVMArg = False
        self.GetGlobalServerConfig()

    def GetGlobalServerConfig(self):
        with open(r"MCSL2/MCSL2_ServerList.json", "r", encoding="utf-8") as ReadGlobalConfig:
            GlobalJson = loads(ReadGlobalConfig.read())
            ServerConfig = GlobalJson['MCSLServerList'][self.ServerGlobalIndex]
            self.ServerName = ServerConfig['name']
            self.CoreName = ServerConfig['core_file_name']
            self.CoreFolder = realpath(f"./Servers/{self.ServerName}/")
            self.MinMemory = ServerConfig['min_memory']
            self.JavaPath = ServerConfig['java_path']
            if ServerConfig['jvm_arg'] != "":
                self.EnableJVMArg = True
                self.JVMArg = ServerConfig['jvm_arg']
            else:
                self.EnableJVMArg = False
            ReadGlobalConfig.close()

    def SetLaunchCommand(self):
        if self.EnableJVMArg == True:
            LaunchCommand = f"\"{self.JavaPath}\" -Xms{self.MinMemory}M -Xmx{self.MaxMemory}M {self.JVMArg} -jar {self.CoreFolder}"
        else:
            LaunchCommand = f"\"{self.JavaPath}\" -Xms{self.MinMemory}M -Xmx{self.MaxMemory}M -jar {self.CoreFolder}{self.CoreName}"
        if self.CheckEulaAcceptStatus(self.CoreFolder) == True:
            self.Launch(LaunchCommand)
        else:
            ReturnStatus = CallMCSL2Dialog(Tip="您所启动的服务器\n并未同意Mojang EULA。\n按下\"确定\"来同意，\n或点击\"取消\"以拒绝。", isNeededTwoButtons=1, ButtonArg="确定|取消")
            if ReturnStatus == 1:
                self.AcceptEula(self.CoreFolder)
            else:
                pass

    def CheckEulaAcceptStatus(self, CoreFolder):
        try:
            with open(f"{CoreFolder}/eula.txt", "r", encoding="utf-8") as Eula:
                EulaText = Eula.read()
                if "eula=true" in EulaText:
                    return True
                else:
                    return False
        except:
            return False

    def AcceptEula(self, CoreFolder):
        with open(f"{CoreFolder}/eula.txt", "w+", encoding="utf-8") as AcceptEula:
            AcceptEula.write("#Accepted by MCSL2\neula=true")
            AcceptEula.close()

    def Launch(self, LaunchCommand):
        Monitor = Popen(LaunchCommand, shell=True, stdout=PIPE, stderr=PIPE)
        # while True:
        #     result = Monitor.stdout.readline()
        #     if result != b'':
        #         try:
        #             print(result.decode('gbk').strip('\r\n'))
        #         except:
        #             print(result.decode('utf-8').strip('\r\n'))
        #     else:
        #         break
from json import loads, dumps
from os import mkdir
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
        CallMCSL2Dialog(Tip, isNeededTwoButtons=0)
        ServerFolderPath = "./Servers/" + ServerName
        mkdir(ServerFolderPath)
        copy(CorePath, ServerFolderPath)
        ServerConfigDict = {
            "name": ServerName,
            "java_path": JavaPath,
            "min_memory": MinMemory,
            "max_memory": MaxMemory,
        }
        ServerConfigJson = dumps(ServerConfigDict, ensure_ascii=False)
        with open(r'MCSL2/MCSL2_ServerList.json', "r", encoding='utf-8') as ReadGlobalServerListFile:
            GlobalServerList = loads(ReadGlobalServerListFile.read())
            print(GlobalServerList)
            print(type(GlobalServerList))
            ServerCount = len(GlobalServerList)
            print(ServerCount)
            GlobalServerList['MCSLServerList'].append({
                "name": ServerName,
                "core_file_name": CoreFileName,
                "java_path": JavaPath,
                "min_memory": MinMemory,
                "max_memory": MaxMemory,
            })
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

        CallMCSL2Dialog(Tip, isNeededTwoButtons=0)




# class ServerLauncher:
#     def __init__(self, ServerGlobalIndex):
#         self.ServerGlobalIndex = ServerGlobalIndex
#         self.MaxMemory = None
#         self.MinMemory = None
#         self.ServerName = None
#         self.JavaPath = None
#         self.CoreName = None
#         self.JVMArg = None
#         self.EnableJVMArg = False
#         self.GetGlobalServerConfig()
#
#     def GetGlobalServerConfig(self):
#
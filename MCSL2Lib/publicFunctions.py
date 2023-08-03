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
"""
These are the built-in functions of MCSL2. They are just for solving the circular import.
"""


from json import loads, dumps
from os import mkdir, path as ospath, remove


def readGlobalServerConfig() -> list:
    """读取全局服务器配置, 返回的是一个list"""
    with open(
        r"MCSL2/MCSL2_ServerList.json", "r", encoding="utf-8"
    ) as globalServerConfigFile:
        globalServerList = loads(globalServerConfigFile.read())["MCSLServerList"]
        globalServerConfigFile.close()
    return globalServerList


def initializeMCSL2():
    """
    初始化程序
    各位开发者请注意，这块是屎山if集中地 --- LxHTT
    """

    # 最外层文件夹
    if not ospath.exists(r"Servers"):
        mkdir(r"./Servers")
    if not ospath.exists(r"Plugins"):
        mkdir(r"./Plugins")
    if not ospath.exists(r"MCSL2"):
        # 如果没有，如下文件夹肯定也没有
        mkdir(r"MCSL2")
        mkdir(r"MCSL2/Logs")
        mkdir(r"MCSL2/Aria2")
        mkdir(r"MCSL2/Downloads")

    # 如果有MCSL2目录，是否有Aria2目录
    elif not ospath.exists(r"MCSL2/Aria2"):
        mkdir(r"MCSL2/Aria2")
        # 如果有Aria2目录，是否有Downloads目录
        if not ospath.exists(r"MCSL2/Downloads"):
            mkdir(r"MCSL2/Downloads")
    else:
        pass
    if not ospath.exists(r"./MCSL2/MCSL2_Config.json"):
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as InitConfig:
            ConfigTemplate = {
                "autoRunLastServer": False,
                "acceptAllMojangEula": False,
                "sendStopInsteadOfKill": True,
                "newServerType": "Default",
                "onlySaveGlobalServerConfig": False,
                "downloadSource": "FastMirror",
                "alwaysAskSaveDirectory": False,
                "aria2Thread": 8,
                "saveSameFileException": "ask",
                "outputDeEncoding": "utf-8",
                "inputDeEncoding": "follow",
                "quickMenu": True,
                "theme": "auto",
                "themeColor": "#0078d4",
                "alwaysRunAsAdministrator": False,
                "startOnStartup": False,
                "checkUpdateOnStart": False,
                "lastServer": "",
            }
            InitConfig.write(dumps(ConfigTemplate, indent=4))
            InitConfig.close()
    if ospath.getsize(r"./MCSL2/MCSL2_Config.json") == 0:
        remove(r"./MCSL2/MCSL2_Config.json")
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as FixConfig:
            ConfigTemplate = {
                "autoRunLastServer": False,
                "acceptAllMojangEula": False,
                "sendStopInsteadOfKill": True,
                "newServerType": "Default",
                "onlySaveGlobalServerConfig": False,
                "downloadSource": "FastMirror",
                "alwaysAskSaveDirectory": False,
                "aria2Thread": 8,
                "saveSameFileException": "ask",
                "outputDeEncoding": "utf-8",
                "inputDeEncoding": "follow",
                "quickMenu": True,
                "theme": "auto",
                "themeColor": "#0078d4",
                "alwaysRunAsAdministrator": False,
                "startOnStartup": False,
                "checkUpdateOnStart": False,
                "lastServer": "",
            }
            FixConfig.write(dumps(ConfigTemplate, indent=4))
            FixConfig.close()
    if not ospath.exists(r"./MCSL2/MCSL2_ServerList.json"):
        with open(
            r"./MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
        ) as InitServerList:
            ServerListTemplate = '{\n  "MCSLServerList": [\n\n  ]\n}'
            InitServerList.write(ServerListTemplate)
            InitServerList.close()

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

from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from json import loads, dumps
from os import makedirs, path as ospath


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
    """

    folders = ["Servers", "Plugins", "MCSL2", "MCSL2/Aria2", "MCSL2/Downloads"]
    for folder in folders:
        if not ospath.exists(folder):
            makedirs(folder)

    if not ospath.exists(r"./MCSL2/MCSL2_Config.json"):
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as config:
            configTemplate = {
                "autoRunLastServer": False,
                "acceptAllMojangEula": False,
                "sendStopInsteadOfKill": True,
                "newServerType": "Default",
                "onlySaveGlobalServerConfig": False,
                "clearAllNewServerConfigInProgram": False,
                "downloadSource": "FastMirror",
                "alwaysAskSaveDirectory": False,
                "aria2Thread": 8,
                "saveSameFileException": "ask",
                "outputDeEncoding": "utf-8",
                "inputDeEncoding": "follow",
                "quickMenu": True,
                "clearConsoleWhenStopServer": False,
                "theme": "auto",
                "themeColor": "#0078d4",
                "alwaysRunAsAdministrator": False,
                "startOnStartup": False,
                "checkUpdateOnStart": False,
                "lastServer": "",
            }
            config.write(dumps(configTemplate, indent=4))
            config.close()
    if ospath.getsize(r"./MCSL2/MCSL2_Config.json") == 0:
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as config:
            configTemplate = {
                "autoRunLastServer": False,
                "acceptAllMojangEula": False,
                "sendStopInsteadOfKill": True,
                "newServerType": "Default",
                "onlySaveGlobalServerConfig": False,
                "clearAllNewServerConfigInProgram": False,
                "downloadSource": "FastMirror",
                "alwaysAskSaveDirectory": False,
                "aria2Thread": 8,
                "saveSameFileException": "ask",
                "outputDeEncoding": "utf-8",
                "inputDeEncoding": "follow",
                "quickMenu": True,
                "clearConsoleWhenStopServer": False,
                "theme": "auto",
                "themeColor": "#0078d4",
                "alwaysRunAsAdministrator": False,
                "startOnStartup": False,
                "checkUpdateOnStart": False,
                "lastServer": "",
            }
            config.write(dumps(configTemplate, indent=4))
            config.close()
    if not ospath.exists(r"./MCSL2/MCSL2_ServerList.json"):
        with open(
            r"./MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
        ) as serverList:
            serverListTemplate = '{\n  "MCSLServerList": [\n\n  ]\n}'
            serverList.write(serverListTemplate)
            serverList.close()


def openWebUrl(Url):
    """打开网址"""
    QDesktopServices.openUrl(QUrl(Url))

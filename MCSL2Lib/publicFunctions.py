#     Copyright 2023, MCSL Team, mailto:lxhtt@mcsl.com.cn
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
import enum
import functools
from json import loads, dumps
from os import makedirs, path as ospath
from types import TracebackType
from typing import Type

import aria2p
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from darkdetect import theme as currentTheme

from MCSL2Lib.settingsController import SettingsController

settingsController = SettingsController()


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
                "outputDeEncoding": "ansi",
                "inputDeEncoding": "follow",
                "quickMenu": True,
                "clearConsoleWhenStopServer": False,
                "theme": "auto",
                "themeColor": "#0078d4",
                "alwaysRunAsAdministrator": False,
                "startOnStartup": False,
                "checkUpdateOnStart": False,
                "lastServer": "",
                "nodeMCSLAPI": "https://hardbin.com",
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
                "outputDeEncoding": "ansi",
                "inputDeEncoding": "follow",
                "quickMenu": True,
                "clearConsoleWhenStopServer": False,
                "theme": "auto",
                "themeColor": "#0078d4",
                "alwaysRunAsAdministrator": False,
                "startOnStartup": False,
                "checkUpdateOnStart": False,
                "lastServer": "",
                "nodeMCSLAPI": "https://hardbin.com",
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


# 带有text的warning装饰器
def warning(text: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(">>> 警告:", func.__name__, text)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def obsolete(text: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(">>> 此函数已过时: ", func.__name__, text)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def isDarkTheme():
    if settingsController.fileSettings["theme"] == "auto":
        return currentTheme() == "Dark"
    elif settingsController.fileSettings["theme"] == "light":
        return False
    elif settingsController.fileSettings["theme"] == "dark":
        return True


def openWebUrl(Url):
    """打开网址"""
    QDesktopServices.openUrl(QUrl(Url))


class ExceptionFilterMode(enum.Enum):
    RAISE_AND_PRINT = enum.auto()  # 过滤：弹框提示，也会抛出异常
    RAISE = enum.auto()  # 过滤：不弹框提示，但是会抛出异常
    PASS = enum.auto()  # 过滤：不弹框提示，也不抛出异常，就当做什么都没发生


def exceptionFilter(ty: Type[BaseException], value: BaseException, _traceback: TracebackType) -> ExceptionFilterMode:
    """
    过滤异常
    """
    if isinstance(value, AttributeError) and "MessageBox" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, aria2p.client.ClientException) and "Active Download not found for GID" in str(value):
        return ExceptionFilterMode.RAISE
    if isinstance(value, RuntimeError) and "wrapped C/C++ object of type" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, Exception) and "raise test" in str(value):
        return ExceptionFilterMode.RAISE
    if isinstance(value, Exception) and "pass test" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, Exception) and "print test" in str(value):
        return ExceptionFilterMode.RAISE_AND_PRINT

    return ExceptionFilterMode.RAISE_AND_PRINT

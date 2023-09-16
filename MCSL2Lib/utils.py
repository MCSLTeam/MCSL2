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
These are the built-in functions of MCSL2. They are just for solving the circular import.
"""
import enum
import functools
import hashlib
import inspect
from json import loads, dumps
from os import makedirs, path as osp
from types import TracebackType
from typing import Type, Optional, Iterable, Callable, Dict, List

import aria2p
from PyQt5.QtCore import QUrl, QThread
from PyQt5.QtGui import QDesktopServices

from subprocess import Popen 
from platform import system as sysinfo

from darkdetect import theme as currentTheme

from MCSL2Lib.Controllers.settingsController import SettingsController

from MCSL2Lib.Controllers.logController import MCSL2Logger

MCSLLogger = MCSL2Logger()

settingsController = SettingsController()

configTemplate = {
    "autoRunLastServer": False,
    "acceptAllMojangEula": False,
    "sendStopInsteadOfKill": True,
    "restartServerWhenCrashed": False,
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
    "enableExperimentalFeatures": False,
}


class ServerUrl:

    @staticmethod
    def getBmclapiUrl(mcVersion: str) -> str:
        return QUrl(f"https://bmclapi2.bangbang93.com/version/{mcVersion}/server")


def readGlobalServerConfig() -> list:
    """读取全局服务器配置, 返回的是一个list"""
    with open(
            r"MCSL2/MCSL2_ServerList.json", "r", encoding="utf-8"
    ) as globalServerConfigFile:
        globalServerList = loads(globalServerConfigFile.read())["MCSLServerList"]
    return globalServerList


def initializeMCSL2():
    """
    初始化程序
    """

    folders = ["Servers", "Plugins", "MCSL2", "MCSL2/Aria2", "MCSL2/Downloads", "MCSL2/Logs"]
    for folder in folders:
        if not osp.exists(folder):
            makedirs(folder, exist_ok=True)

    if not osp.exists(r"./MCSL2/MCSL2_Config.json"):
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as config:
            config.write(dumps(configTemplate, indent=4))
    if osp.getsize(r"./MCSL2/MCSL2_Config.json") == 0:
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as config:
            config.write(dumps(configTemplate, indent=4))
    if not osp.exists(r"./MCSL2/MCSL2_ServerList.json"):
        with open(
                r"./MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
        ) as serverList:
            serverListTemplate = '{\n  "MCSLServerList": [\n\n  ]\n}'
            serverList.write(serverListTemplate)
    configurationCompleter()


def configurationCompleter():
    with open(r"./MCSL2/MCSL2_Config.json", "r", encoding="utf-8") as config:
        configContent = loads(config.read())
        if set(configContent.keys()) == set(configTemplate.keys()):
            pass
        else:
            missingKeys = set(configTemplate.keys()) - set(configContent.keys())
            MCSLLogger.warning(f"缺失配置{missingKeys}，正在使用默认配置补全。")
            for key in missingKeys:
                configContent[key] = configTemplate[key]
    with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as config:
        config.write(dumps(configContent, indent=4))


# 带有text的warning装饰器
def warning(text: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            MCSLLogger.warning(f"警告: {func.__name__} {text}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def obsolete(text: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            MCSLLogger.warning(f"此函数已过时: {func.__name__} {text}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def private(func):
    # 获取函数所属的类名
    class_name = func.__qualname__.split('.')[0]

    # 定义一个包装函数
    def wrapper(*args, **kwargs):
        # 获取调用函数的栈帧
        frame = inspect.currentframe().f_back
        # 获取调用函数的类名
        caller_class = frame.f_locals.get('self', None).__class__.__name__
        # 如果调用函数的类名和函数所属的类名相同，说明是在类的内部调用
        if caller_class == class_name:
            # 调用原始函数
            return func(*args, **kwargs)
        else:
            # 抛出异常
            raise PermissionError(f"{func.__name__} is a private method of {class_name}")

    # 返回包装函数
    return wrapper


def isDarkTheme():
    if settingsController.fileSettings["theme"] == "auto":
        return currentTheme() == "Dark"
    else:
        return settingsController.fileSettings["theme"] == "dark"


def openWebUrl(Url):
    """打开网址"""
    QDesktopServices.openUrl(QUrl(Url))


class ExceptionFilterMode(enum.Enum):
    RAISE_AND_PRINT = enum.auto()  # 过滤：弹框提示，也会抛出异常
    RAISE = enum.auto()  # 过滤：不弹框提示，但是会抛出异常
    PASS = enum.auto()  # 过滤：不弹框提示，也不抛出异常，就当做什么都没发生


def exceptionFilter(
        ty: Type[BaseException], value: BaseException, _traceback: TracebackType
) -> ExceptionFilterMode:
    """
    过滤异常
    """
    if isinstance(value, AttributeError) and "MessageBox" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(
            value, aria2p.ClientException
    ) and "Active Download not found for GID" in str(value):
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


def checkSHA1(fileAndSha1: Iterable, _filter: Callable[[str, str], bool] = None) -> List[Dict]:
    """
    检查文件的SHA1值是否正确
    """
    rv = []
    if _filter is None:
        _filter = lambda a, b: True
    for file, sha1 in fileAndSha1:
        if not osp.exists(file):
            rv.append({"file": file, "result": False})
            continue
        if _filter(file, sha1):
            # check sha1
            with open(file, "rb") as f:
                fileSha1 = hashlib.sha1(f.read()).hexdigest()
            rv.append({"file": file, "result": fileSha1 == sha1})
        else:
            rv.append({"file": file, "result": True})
    return rv


class workingThreads:
    threads = {}

    @classmethod
    def register(cls, name) -> None:
        """
        注册一个线程,并启动它
        """
        if cls.hasThread(name):
            raise RuntimeError("This thread has already been registered.")
        thread = QThread()
        thread.start()
        cls.threads[name] = thread

    @classmethod
    def getThread(cls, name) -> Optional[QThread]:
        """
        获取一个正在运行的线程
        """
        if cls.hasThread(name):
            return cls.threads[name]
        else:
            raise RuntimeError("This thread is not running or not exists.")

    @classmethod
    def closeThread(cls, name) -> bool:
        """
        关闭一个正在运行的线程
        """
        if cls.hasThread(name):
            th = cls.threads.pop(name)
            th.quit()
            th.wait()
            th.deleteLater()
            return True
        else:
            return False

    @classmethod
    def closeAllThreads(cls) -> None:
        """
        关闭所有正在运行的线程
        """
        for th in cls.threads.values():
            th.quit()
            th.wait()
            th.deleteLater()
        cls.threads.clear()

    @classmethod
    def hasThread(cls, name) -> bool:
        rv = cls.threads.get(name, None)
        if rv is None:
            return False
        if not rv.isRunning():
            return False
        return True

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("This class is not allowed to be instantiated.")

    def __call__(self, *args, **kwargs):
        raise RuntimeError("This class is not allowed to be instantiated.")

class FileOpener:

    def openFileChecker(self, filePath):
        if not self.isOpenedFolder:
            self._openFileFolder(filePath)
            self.isOpenedFolder = 1
        else:
            self.isOpenedFolder = 0

    def _openFileFolder(_filePath):
        system = sysinfo()
        if system == "Windows":
            Popen(["start", _filePath], shell=True)
        elif system == "Darwin":
            Popen(["open", _filePath])
        elif system == "Linux":
            Popen(["xdg-open", _filePath])
        else:
            pass
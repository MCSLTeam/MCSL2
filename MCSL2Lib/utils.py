#     Copyright 2024, MCSL Team, mailto:services@mcsl.com.cn
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
from json import dumps, loads
from os import makedirs, path as osp
import os
from types import TracebackType
from typing import Type, Optional, Iterable, Callable, Dict, List, Any, Set, Tuple

import psutil
import requests
from PyQt5.QtCore import QUrl, QThread, QThreadPool, QFile
from PyQt5.QtGui import QDesktopServices

from MCSL2Lib.ProgramControllers.logController import _MCSL2Logger

MCSL2Logger = _MCSL2Logger()
AUTHOR_SERVERS = ["18.65.216.60", "13.35.58.36", "18.65.216.14", "13.35.58.102", "18.65.216.5"]


class ServicesUrl:
    @staticmethod
    def getBmclapiUrl(mcVersion: str) -> QUrl:
        return QUrl(f"https://bmclapi2.bangbang93.com/version/{mcVersion}/server")


def readGlobalServerConfig() -> list:
    """读取全局服务器配置, 返回的是一个list"""
    return loads(readFile(r"MCSL2/MCSL2_ServerList.json"))["MCSLServerList"]


def _normalize_server_config(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _normalize_server_config(value[k]) for k in sorted(value.keys())}
    if isinstance(value, list):
        return [_normalize_server_config(item) for item in value]
    return value


def deep_compare_server_config(left: Dict, right: Dict) -> bool:
    return _normalize_server_config(left) == _normalize_server_config(right)


def find_server_config_index(server_list: List[Dict], candidate: Dict) -> Optional[int]:
    name = candidate.get("name")
    core_file_name = candidate.get("core_file_name")
    for idx, existing in enumerate(server_list):
        if existing.get("name") == name and existing.get("core_file_name") == core_file_name:
            return idx
    return None


def initializeMCSL2():
    """
    初始化程序
    """

    folders = [
        "Servers",
        "Plugins",
        "MCSL2",
        "MCSL2/Downloads",
        "MCSL2/Logs",
    ]
    for folder in folders:
        if not osp.exists(folder):
            makedirs(folder, exist_ok=True)
    del folders

    if not osp.exists(r"./MCSL2/MCSL2_ServerList.json"):
        globalServerList = {"MCSLServerList": []}
        writeFile(r"./MCSL2/MCSL2_ServerList.json", '{\n  "MCSLServerList": [\n\n  ]\n}')
    else:
        globalServerList = loads(readFile(r"MCSL2/MCSL2_ServerList.json"))

    needs_save = False

    # scan Server folder to add missing server configs or update changed ones
    serverFolder = r"./Servers"
    existing_keys: Set[Tuple[Optional[str], Optional[str]]] = set()
    for root, _, files in os.walk(serverFolder):
        for file in files:
            if file == "MCSL2ServerConfig.json":
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    try:
                        singleConfig = loads(f.read())
                    except Exception:
                        MCSL2Logger.error(
                            f"读取服务器配置文件失败: {os.path.join(root, file)}，请检查文件格式是否正确。"  # noqa: E501
                        )
                        continue

                key = (singleConfig.get("name"), singleConfig.get("core_file_name"))
                existing_keys.add(key)
                index = find_server_config_index(globalServerList["MCSLServerList"], singleConfig)
                if index is None:
                    globalServerList["MCSLServerList"].append(singleConfig)
                    needs_save = True
                    MCSL2Logger.warning(
                        "扫描到不在全局配置中的服务器，已自动添加： {"
                        + (
                            f'"name": "{singleConfig["name"]}", '
                            f'"core_file_name": "{singleConfig["core_file_name"]}"'
                        )
                        + "}"
                    )
                else:
                    existing = globalServerList["MCSLServerList"][index]
                    if not deep_compare_server_config(existing, singleConfig):
                        globalServerList["MCSLServerList"][index] = singleConfig
                        needs_save = True
                        MCSL2Logger.info(
                            "检测到服务器配置变更，已使用最新配置覆盖： {"
                            + (
                                f'"name": "{singleConfig["name"]}", '
                                f'"core_file_name": "{singleConfig["core_file_name"]}"'
                            )
                            + "}"
                        )
    # remove missing configs from global list
    filtered_configs: List[Dict] = []
    for singleConfig in globalServerList.get("MCSLServerList", []):
        key = (singleConfig.get("name"), singleConfig.get("core_file_name"))
        if key in existing_keys:
            filtered_configs.append(singleConfig)
            continue
        needs_save = True
        MCSL2Logger.warning(
            "检测到全局配置中存在未找到的服务器，已自动移除： {"
            + (
                f'"name": "{singleConfig.get("name")}", '
                f'"core_file_name": "{singleConfig.get("core_file_name")}"'
            )
            + "}"
        )

    if len(filtered_configs) != len(globalServerList.get("MCSLServerList", [])):
        globalServerList["MCSLServerList"] = filtered_configs
    # set global thread pool
    QThreadPool.globalInstance().setMaxThreadCount(
        psutil.cpu_count(logical=True)
    )  # IO-Bound = 2*N, CPU-Bound = N + 1

    # fix changed icon
    for singleConfig in globalServerList.get("MCSLServerList", []):
        if singleConfig.get("icon") == "Spigot.svg":
            singleConfig["icon"] = "Spigot.png"
            needs_save = True
            MCSL2Logger.warning(
                "检测到过时配置文件，已自动更新: {"
                + (f'"name": "{singleConfig["name"]}", "icon": "{singleConfig["icon"]}"')
                + "}"
            )

    if needs_save:
        writeFile(
            r"MCSL2/MCSL2_ServerList.json",
            dumps(globalServerList, indent=4, ensure_ascii=False),
        )


# 带有text的warning装饰器
def warning(text: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            MCSL2Logger.warning(f"警告: {func.__name__} {text}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def obsolete(text: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            MCSL2Logger.warning(f"此函数已过时: {func.__name__} {text}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def private(func):
    # 获取函数所属的类名
    class_name = func.__qualname__.split(".")[0]

    # 定义一个包装函数
    def wrapper(*args, **kwargs):
        # 获取调用函数的栈帧
        frame = inspect.currentframe().f_back
        # 获取调用函数的类名
        caller_class = frame.f_locals.get("self", None).__class__.__name__
        # 如果调用函数的类名和函数所属的类名相同，说明是在类的内部调用
        if caller_class == class_name:
            # 调用原始函数
            return func(*args, **kwargs)
        else:
            # 抛出异常
            raise PermissionError(f"{func.__name__} is a private method of {class_name}")

    # 返回包装函数
    return wrapper


def openWebUrl(Url):
    """打开网址"""
    QDesktopServices.openUrl(QUrl(Url))


def openLocalFile(FilePath):
    """打开本地文件(夹)"""
    QDesktopServices.openUrl(QUrl.fromLocalFile(FilePath))


def writeFile(file: str, content: str):
    f = QFile(file)
    f.open(QFile.WriteOnly)
    f.write(content.encode("utf-8"))
    f.close()


def readFile(file: str) -> str:
    f = QFile(file)
    if not f.exists():
        return ""
    f.open(QFile.ReadOnly)
    content = f.readAll()
    f.close()
    return bytes(content).decode("utf-8")


def readBytesFile(file: str):
    f = QFile(file)
    f.open(QFile.ReadOnly)
    content = f.readAll()
    f.close()
    return content


def writeBytesFile(file: str, content: bytes):
    f = QFile(file)
    f.open(QFile.WriteOnly)
    f.write(content)
    f.close()


class ExceptionFilterMode(enum.Enum):
    RAISE_AND_PRINT = enum.auto()  # 过滤：弹框提示，也会抛出异常
    RAISE = enum.auto()  # 过滤：不弹框提示，但是会抛出异常
    PASS = enum.auto()  # 过滤：不弹框提示，也不抛出异常，就当做什么都没发生
    SILENT = enum.auto()  # 过滤：不弹框提示，也不抛出异常，就当做什么都没发生


def exceptionFilter(
    ty: Type[BaseException], value: BaseException, _traceback: TracebackType
) -> ExceptionFilterMode:
    """
    过滤异常
    """
    if isinstance(value, AttributeError) and "MessageBox" in str(value):
        return ExceptionFilterMode.SILENT
    if isinstance(value, RuntimeError) and "wrapped C/C++ object of type" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, Exception) and "raise test" in str(value):
        return ExceptionFilterMode.RAISE
    if isinstance(value, Exception) and "pass test" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, Exception) and "print test" in str(value):
        return ExceptionFilterMode.RAISE_AND_PRINT
    if isinstance(
        value, Exception
    ) and "RunningServerHeaderCardWidget cannot be converted to PyQt5.QtWidgets.QLayoutItem" in str(
        value
    ):
        return ExceptionFilterMode.SILENT
    if isinstance(value, Exception) and "sipBadCatcherResult" in str(value):
        return ExceptionFilterMode.SILENT

    return ExceptionFilterMode.RAISE_AND_PRINT


def checkSHA1(fileAndSha1: Iterable, _filter: Callable[[str, str], bool] = None) -> List[Dict]:
    """
    检查文件的SHA1值是否正确
    """
    rv = []
    if _filter is None:

        def _filter(a, b):
            return True

    for file, sha1 in fileAndSha1:
        if not osp.exists(file):
            rv.append({"file": file, "result": False})
            continue
        if _filter(file, sha1):
            # check sha1
            fileSha1 = hashlib.sha1(readBytesFile(file)).hexdigest()
            rv.append({"file": file, "result": fileSha1 == sha1})
        else:
            rv.append({"file": file, "result": True})
    return rv


class WorkingThreads:
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


def getAvailableAuthorServer() -> Optional[str]:
    for e in AUTHOR_SERVERS:
        try:
            requests.get(e, timeout=1)
            return e
        except ConnectionError:
            continue
    return None

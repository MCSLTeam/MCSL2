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
An auto-detect Java function.
"""

import json
from os import environ as env
from os import path as osp
from os import pathsep, remove, listdir
from platform import system
from re import search

if "windows" in system().lower():
    import winreg

from PyQt5.QtCore import QThread, pyqtSignal, QProcess

from MCSL2Lib.utils import MCSL2Logger, readFile, writeFile

foundJava = []
fSearch = True
# fmt: off
matchKeywords = {
    '1.', 'bin', 'cache', 'client', 'corretto', 'craft', 'data', 'download', 'eclipse',
    'env', 'ext', 'file', 'forge', 'fabric', 'game', 'hmcl', 'hotspot', 'java', 'jdk', 'jre',
    'zulu', 'dragonwell', 'jvm', 'launch', 'mc', 'microsoft', 'mod', 'mojang', 'net', 'netease',
    'optifine', 'oracle', 'path', 'program', 'roaming', 'run', 'runtime', 'server', 'software',
    'temp', 'users', 'users', 'x64', 'x86', 'lib', 'usr',
    '世界', '前置', '原版', '启动', '启动', '国服', '官启', '官方', '客户', '应用', '整合',
    '新建文件夹', '服务', '游戏', '环境', '程序', '网易', '软件', '运行', '高清'
}
excludedKeywords = {
    "$", "{", "}", "__"
}


# fmt: on
class Java:
    def __init__(self, path, ver):
        self._path = path
        self._version = ver

    @property
    def path(self):
        return self._path

    @property
    def version(self):
        return self._version

    @property
    def json(self):
        return {"Path": self.path, "Version": self.version}

    def __hash__(self):
        return hash((self._path, self._version))

    def __str__(self):
        return json.dumps(self.json)

    def __eq__(self, other):
        if isinstance(other, Java):
            return self._path == other._path and self._version == other._version


def getJavaVersion(File):
    """
    获取Java版本，三端通用\n
    为什么不Win32API读取文件：无法跨平台\n
    为什么不读取Java安装目录下的release文件：万一没有呢
    """
    process = QProcess()
    process.start(File, ["-version"])
    process.waitForFinished()
    output = process.readAllStandardError().data().decode("utf-8")

    # 从输出中提取版本信息
    version_pattern = r"(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[._](\d+))?(?:-(.+))?"
    version_match = search(version_pattern, output)

    # 输出版本信息
    if version_match:
        version = ".".join(filter(None, version_match.groups()))
        return version
    else:
        return ""


def javaVersionMatcher(s):
    pattern = r"(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[._](\d+))?(?:-(.+))?"
    match = search(pattern, s)
    if match is not None:
        match = ".".join(filter(None, match.groups()))
    else:
        match = "unknown"
    return match


def detectJava(fSearch=True):
    """
    检测所有已安装的Java路径，三端通用
    """
    javaList = []
    javaPathList = []
    foundJava.clear()
    # 检测环境变量中的Java（不是Java的PATH会在最后筛选时过滤）
    javaPathList.extend(env.get("PATH").split(pathsep))

    # 针对不同系统的寻找
    if "windows" in system().lower():  # windows
        # 检测JAVA_HOME环境变量
        javaPathList.extend(env.get("JAVA_HOME").split(pathsep))

        # 检测默认安装路径
        javaInstallationPaths = [
            r"C:\Program Files\Java",
            r"C:\Program Files (x86)\Java",
            r"C:\Program Files\Eclipse Adoptium",
            r"C:\Program Files (x86)\Eclipse Adoptium",
        ]

        for path in javaInstallationPaths:
            for subPath in listdir(path):
                javaPathList.extend(osp.join(subPath, r"bin"))

        # 检测注册表
        javaRegKeyPaths = [
            r"SOFTWARE\JavaSoft\Java Runtime Environment",
            r"SOFTWARE\JavaSoft\Java Development Kit",
            r"SOFTWARE\\JavaSoft\\JRE",
            r"SOFTWARE\\JavaSoft\\JDK",
            r"SOFTWARE\\Eclipse Foundation\\JDK",
            r"SOFTWARE\\Eclipse Adoptium\\JRE",
            r"SOFTWARE\\Eclipse Foundation\\JDK",
            r"SOFTWARE\\Microsoft\\JDK",
        ]

        accessFlags = winreg.KEY_READ
        for keyPath in javaRegKeyPaths:
            try:
                # 32位注册表视图
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyPath, 0,
                                    accessFlags | winreg.KEY_WOW64_32KEY) as java_key_32:
                    javaPaths = getJavaInRegistryKey(java_key_32)
                    javaPathList.extend(javaPaths)

                # 64位注册表视图（如果可用）
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyPath, 0,
                                    accessFlags | winreg.KEY_WOW64_64KEY) as java_key_64:
                    javaPaths = getJavaVersion(java_key_64)
                    javaPathList.extend(javaPaths)
            except WindowsError:
                # 如果键不存在，则忽略错误并继续
                pass
    elif "darwin" in system().lower():  # macOS
        # 检测第三方App内置Java路径
        javaInstallationPaths = [
            r"/Applications/Xcode.app/Contents/Applications/Application Loader.app/Contents/MacOS/itms/java",
            r"/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home",
            r"/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands",
        ]
        javaPathList.extend(javaInstallationPaths)
        # 检测默认安装路径
        basePath = "/Library/Java/JavaVirtualMachines/"
        if osp.isdir(basePath):
            for entry in listdir(basePath):
                if osp.isdir(entry):
                    javaPathList.append(osp.join(entry, "Contents/Home/bin"))
    else:  # linux
        # 检测默认安装路径
        javaInstallationPaths = [
            r"/usr",
            r"/usr/java",
            r"/usr/lib/jvm",
            r"/usr/lib64/jvm",
            r"/opt/jdk",
            r"/opt/jdks",
        ]

        for path in javaInstallationPaths:
            # 尝试插入jre/bin和bin目录
            javaPathList.append(osp.join(path, "/jre/bin"))
            javaPathList.append(osp.join(path, "/bin"))

            # 如果目录存在，则遍历其内容
            if osp.isdir(path):
                for entry in listdir(path):
                    if osp.isdir(path):
                        # 尝试插入每个子目录的jre/bin和bin目录
                        javaPathList.append(osp.join(entry, "/jre/bin"))
                        javaPathList.append(osp.join(entry, "/bin"))

    # 筛选Java路径
    for path in javaPathList:
        path = osp.join(path, "javaw.exe") if "windows" in system().lower() else osp.join(path, "java")
        if osp.exists(path):
            version = getJavaVersion(path)
            if version != "":
                java = Java(path, version)
                if not java in javaList:
                    javaList.append(Java(path, version))

    return javaList


def getJavaInRegistryKey(keyPath):
    """
    检测注册表中的Java路径，仅windows
    """
    javaPathList = []
    # 打开注册表键
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keyPath)
    except FileNotFoundError:
        return javaPathList

    # 遍历子键
    i = 0
    while True:
        try:
            subKeyName, _, _ = winreg.EnumValue(key, i)
            subKey = winreg.OpenKey(key, subKeyName)

            # 检查特定的值
            subKeyValueNames = ["JavaHome", "InstallationPath", "\\\\hotspot\\\\MSI"]
            for subKeyValue in subKeyValueNames:
                try:
                    javaPath, _ = winreg.QueryValueEx(subKey, subKeyValue)
                    javaPathList.extend(osp.join(javaPath, r"bin\javaw.exe"))
                except FileNotFoundError:
                    continue

            i += 1
        except OSError:
            break  # 如果没有更多子键，则跳出循环

    winreg.CloseKey(key)
    return javaPathList


def checkJavaAvailability(java: Java):
    if osp.exists(java.path):
        process = QProcess()
        process.start(java.path, ["-version"])
        process.waitForFinished()
        output = process.readAllStandardError().data().decode("utf-8")
        process.deleteLater()
        matcher = javaVersionMatcher(output)
        if matcher == java.version:
            return True
    return False


def loadJavaList():
    """
    从配置文件中读取Java
    """

    # 兼容
    if osp.exists("MCSL2/AutoDetectJavaHistory.txt"):
        remove("MCSL2/AutoDetectJavaHistory.txt")
    if osp.exists("MCSL2/AutoDetectJavaHistory.json"):
        remove("MCSL2/AutoDetectJavaHistory.json")

    if not osp.exists("MCSL2/MCSL2_DetectedJava.json"):
        return []
    foundedJava = json.loads(readFile("MCSL2/MCSL2_DetectedJava.json"))
    return [Java(e["Path"], e["Version"]) for e in foundedJava["java"]]


def saveJavaList(list_: list):
    writeFile(
        "MCSL2/MCSL2_DetectedJava.json",
        json.dumps(
            {"java": [j.json for j in list_]},
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
        ),
    )


def sortJavaList(list_: list, reverse=False):
    """
    为List[Java]排序
    """
    list_.sort(key=lambda x: x.version, reverse=reverse)


def sortedJavaList(list_: list, reverse=False):
    """
    为List[Java]排序，并返回新列表
    """
    return sorted(list_, key=lambda x: x.version, reverse=reverse)


def combineJavaList(original: list, list_: list, invaild: ..., check=True):
    """
    合并两个List[Java]
    invaild为引用输出(list)
    """
    s1 = set(original)
    s2 = set(list_)
    s = s1.union(s2)
    if check:
        for e in s1 - s2:
            if not checkJavaAvailability(e):
                s.remove(e)
                MCSL2Logger.warning(f"{e} 已失效")
                if isinstance(invaild, list):
                    invaild.append(e)
    return list(s)


class JavaFindWorkThread(QThread):
    foundJavaSignal = pyqtSignal(list)
    finishSignal = pyqtSignal(int)

    def __init__(self, fSearch=True, parent=None):
        super().__init__(parent)
        self._f = fSearch
        self._sequenceNumber = 0

    @property
    def sequenceNumber(self):
        return self._sequenceNumber

    @sequenceNumber.setter
    def sequenceNumber(self, value):
        self._sequenceNumber = value

    def run(self):
        self.foundJavaSignal.emit(detectJava(self._f))
        self.finishSignal.emit(self._sequenceNumber)


class JavaFindWorkThreadFactory:
    def __init__(self, fSearch=True, parent=None):
        self._finishConnect = None
        self._connect = None
        self._f = fSearch
        self._parent = parent
        self._instanceCounter = 0
        self._thread = None

    @property
    def fSearch(self):
        return self._f

    @fSearch.setter
    def fSearch(self, value):
        self._f = value

    @property
    def signalConnect(self):
        return self._connect

    @signalConnect.setter
    def signalConnect(self, value):
        self._connect = value

    @property
    def finishSignalConnect(self):
        return self._finishConnect

    @finishSignalConnect.setter
    def finishSignalConnect(self, value):
        self._finishConnect = value

    def create(self):
        self._instanceCounter += 1
        thread = JavaFindWorkThread(self._f, self._parent)
        thread.foundJavaSignal.connect(self._connect)
        thread.sequenceNumber = self._instanceCounter
        thread.finishSignal.connect(self._finishConnect)
        self._thread = thread
        return thread

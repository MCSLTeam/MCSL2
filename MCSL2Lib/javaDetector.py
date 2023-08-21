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
'''
An auto-detect Java function.
'''

import json
from os import listdir, remove
from os import path as ospath
from platform import system
from re import search

from PyQt5.QtCore import QThread, pyqtSignal, QProcess

foundJava = []
isNeedFuzzySearch = True
# fmt: off
MatchKeywords = {
    '1.', 'bin', 'cache', 'client', 'corretto', 'craft', 'data', 'download', 'eclipse',
    'env', 'ext', 'file', 'forge', 'game', 'hmcl', 'hotspot', 'java', 'jdk', 'jre',
    'jvm', 'launch', 'mc', 'microsoft', 'mod', 'mojang', 'net', 'netease', 'optifine',
    'oracle', 'path', 'program', 'roaming', 'run', 'runtime', 'server', 'software',
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
        return {
            "Path": self.path,
            "Version": self.version
        }

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
    有人问，为什么不Win32API读取文件：无法跨平台\n
    有人问，为什么不读取Java安装目录下的release文件：万一没有呢\n
    急死我了。 --LxHTT
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


def findStr(s):
    for _s in excludedKeywords:
        if _s in s:
            return False
    for _s in MatchKeywords:
        if _s in s:
            return True
    return False


def searchFile(Path, FileKeyword, FileExtended, FuzzySearch, _Match):
    # construct _Match function
    if "windows" in system().lower():
        def Match(P, F):
            return ospath.join(P, F).endswith(r"bin\java.exe")
    else:
        def Match(P, F):
            return ospath.join(P, F).endswith(r"bin/java")

    processes = searchingFile(Path, FileKeyword, FileExtended, FuzzySearch, Match)
    rv = []
    for process in processes:
        process.waitForFinished()
        try:
            if match := _Match(process.readAllStandardError().data().decode("utf-8")):
                rv.append(Java(process.program(), match))
        except UnicodeDecodeError:
            if match := _Match(process.readAllStandardError().data().decode("gbk")):
                rv.append(Java(process.program(), match))
    return rv


def searchingFile(Path, FileKeyword, FileExtended, FuzzySearch, _Match):
    processes = []
    if FuzzySearch:
        if ospath.isfile(Path) or "x86_64-linux-gnu" in Path:
            return processes
        try:
            for File in listdir(Path):
                _Path = ospath.join(Path, File)
                if ospath.isfile(_Path):
                    if _Match(Path, File):
                        process = QProcess()
                        process.start(_Path, ["-version"])
                        processes.append(process)
                elif findStr(File.lower()):
                    processes.extend(
                        searchingFile(
                            _Path, FileKeyword, FileExtended, FuzzySearch, _Match
                        )
                    )
        except PermissionError:
            pass
        except FileNotFoundError as e:
            pass
    return processes


def JavaVersionMatcher(s):
    pattern = r"(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[._](\d+))?(?:-(.+))?"
    match = search(pattern, s)
    if match is not None:
        match = ".".join(filter(None, match.groups()))
    else:
        match = "unknown"
    return match


def detectJava(FuzzySearch=True):
    JavaPathList = []
    foundJava.clear()
    if "windows" in system().lower():
        for i in range(65, 91):
            Path = chr(i) + ":\\"
            if ospath.exists(Path):
                JavaPathList.extend(
                    searchFile(Path, "java", "exe", FuzzySearch, JavaVersionMatcher)
                )
    else:
        JavaPathList.extend(
            searchFile("/usr/lib", "java", "", FuzzySearch, JavaVersionMatcher)
        )
    return JavaPathList


def checkJavaAvailability(java: Java):
    if ospath.exists(java.path):
        process = QProcess()
        process.start(java.path, ["-version"])
        process.waitForFinished()
        output = process.readAllStandardError().data().decode("utf-8")
        process.deleteLater()
        matcher = JavaVersionMatcher(output)
        if matcher == java.version:
            return True
    return False


def loadJavaList():
    """
    从配置文件中读取Java
    """

    # 兼容
    if ospath.exists("MCSL2/AutoDetectJavaHistory.txt"):
        remove("MCSL2/AutoDetectJavaHistory.txt")
    if ospath.exists("MCSL2/AutoDetectJavaHistory.json"):
        remove("MCSL2/AutoDetectJavaHistory.json")

    if not ospath.exists("MCSL2/MCSL2_DetectedJava.json"):
        return []
    with open(
            "MCSL2/MCSL2_DetectedJava.json", "r", encoding="utf-8"
    ) as f:
        foundedJava = json.load(f)
        l = [Java(e["Path"], e["Version"]) for e in foundedJava["java"]]
        return l


def saveJavaList(l: list):
    with open(
            "MCSL2/MCSL2_DetectedJava.json", "w", encoding="utf-8"
    ) as f:
        json.dump(
            {"java": [j.json for j in l]},
            f,
            ensure_ascii=False,
            sort_keys=True,
            indent=4
        )


def sortJavaList(l: list, reverse=False):
    """
    为List[Java]排序
    """
    l.sort(key=lambda x: x.version, reverse=reverse)


def sortedJavaList(l: list, reverse=False):
    """
    为List[Java]排序，并返回新列表
    """
    return sorted(l, key=lambda x: x.version, reverse=reverse)


def combineJavaList(original: list, l: list,invaild:...,check=True):
    """
    合并两个List[Java]
    invaild为引用输出(list)
    """
    s1 = set(original)
    s2 = set(l)
    s = s1.union(s2)
    if check:
        for e in s1 - s2:
            if not checkJavaAvailability(e):
                s.remove(e)
                print(e, "已失效")
                if isinstance(invaild,list):
                    invaild.append(e)
    return list(s)


class JavaFindWorkThread(QThread):
    foundJavaSignal = pyqtSignal(list)
    finishSignal = pyqtSignal(int)

    def __init__(self, fuzzySearch=True, parent=None):
        super().__init__(parent)
        self._fuzzy = fuzzySearch
        self._sequenceNumber = 0

    @property
    def sequenceNumber(self):
        return self._sequenceNumber

    @sequenceNumber.setter
    def sequenceNumber(self, value):
        self._sequenceNumber = value

    def run(self):
        self.foundJavaSignal.emit(detectJava(self._fuzzy))
        self.finishSignal.emit(self._sequenceNumber)


class JavaFindWorkThreadFactory:
    def __init__(self, fuzzySearch=True, parent=None):
        self._finishConnect = None
        self._connect = None
        self._fuzzy = fuzzySearch
        self._parent = parent
        self._instanceCounter = 0
        self._thread = None

    @property
    def fuzzySearch(self):
        return self._fuzzy

    @fuzzySearch.setter
    def fuzzySearch(self, value):
        self._fuzzy = value

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
        thread = JavaFindWorkThread(self._fuzzy, self._parent)
        thread.foundJavaSignal.connect(self._connect)
        thread.sequenceNumber = self._instanceCounter
        thread.finishSignal.connect(self._finishConnect)
        self._thread = thread
        return thread

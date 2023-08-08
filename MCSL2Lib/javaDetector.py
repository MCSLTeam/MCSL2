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
'''
An auto-detect Java function.
'''

from os import listdir
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

    def __hash__(self):
        return hash((self._path, self._version))

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
    # construct _Math function
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
        if match := _Match(process.readAllStandardError().data().decode("utf-8")):
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
            print(f"扫描路径时出错: {e}")
    return processes


def detectJava(FuzzySearch=True):
    def JavaVersionMatcher(s):
        pattern = r"(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[._](\d+))?(?:-(.+))?"
        match = search(pattern, s)
        if match is not None:
            match = ".".join(filter(None, match.groups()))
        else:
            match = "unknown"
        return match
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

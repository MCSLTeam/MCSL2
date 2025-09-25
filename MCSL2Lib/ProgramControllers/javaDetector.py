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
An auto-detect Java module.
"""

import json
from os import environ as env
from os import path as osp
from os import getlogin
from os import pathsep, remove, listdir
from platform import system
from re import search

from PyQt5.QtCore import QThread, pyqtSignal, QProcess

from MCSL2Lib.utils import MCSL2Logger, readFile, writeFile

foundJava = []
fSearch = True
# fmt: off
matchKeywords = [
    '1.', 'bin', 'cache', 'client', 'craft', 'data', 'download', 'eclipse', 'mine', 'mc', 'launch',
    'hotspot', 'java', 'jdk', 'jre', 'zulu', 'dragonwell', 'jvm', 'microsoft', 'corretto', 'sigma',
    'mod', 'mojang', 'net', 'netease', 'forge', 'liteloader', 'fabric', 'game', 'vanilla', 'server',
    'optifine', 'oracle', 'path', 'program', 'roaming', 'local', 'run', 'runtime', 'software', 'daemon',  # noqa: E501
    'temp', 'users', 'users', 'x64', 'x86', 'lib', 'usr', 'env', 'ext', 'file', 'data', 'green', 'vape',  # noqa: E501
    '我的', '世界', '前置', '原版', '启动', '启动', '国服', '官启', '官方', '客户', '应用', '整合',
    getlogin(), '新建文件夹', '服务', '游戏', '环境', '程序', '网易', '软件', '运行', '高清', '组件',  # noqa: E501
    'badlion', 'blc', 'lunar', 'tlauncher', 'soar', 'cheatbreaker', 'hmcl', 'pcl', 'bakaxl', 'fsm',
    'jetbrains', 'intellij', 'idea', 'pycharm', 'webstorm', 'clion', 'goland', 'rider', 'datagrip',
    'rider', 'appcode', 'phpstorm', 'rubymine', 'jbr', 'android', 'mcsm', 'msl', 'mcsl', '3dmark', 'arctime',  # noqa: E501
]
excludedKeywords = ['$', '{', '}', '__']


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


def findStr(s):
    for _s in excludedKeywords:
        if _s in s:
            return False
    for _s in matchKeywords:
        if _s in s:
            return True
    return False


def searchFile(path, keyword, ext, fSearch, _match):
    # construct _match function
    if "windows" in system().lower():

        def match(P, F):
            return osp.join(P, F).endswith(r"bin\java.exe")

    else:

        def match(P, F):
            return osp.join(P, F).endswith(r"bin/java")

    processes = searchingFile(path, keyword, ext, fSearch, match)
    rv = []
    for process in processes:
        process.waitForFinished()
        try:
            if match := _match(process.readAllStandardError().data().decode("utf-8")):
                rv.append(Java(process.program(), match))
        except UnicodeDecodeError:
            if match := _match(process.readAllStandardError().data().decode("gbk")):
                rv.append(Java(process.program(), match))
    return rv


def searchingFile(path, keyword, ext, fSearch, _match):
    processes = []
    if fSearch:
        if osp.isfile(path):
            return processes
        try:
            for File in listdir(path):
                _Path = osp.join(path, File)
                if osp.isfile(_Path):
                    if _match(path, File):
                        process = QProcess()
                        process.start(_Path, ["-version"])
                        processes.append(process)
                elif findStr(File.lower()):
                    processes.extend(searchingFile(_Path, keyword, ext, fSearch, _match))
        except PermissionError:
            pass
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        except Exception as error:
            MCSL2Logger.error(f"[Java Detector] error occurred when access {path=}, {error=}")
    return processes


def javaVersionMatcher(s):
    pattern = r"(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[._](\d+))?(?:-(.+))?"
    match = search(pattern, s)
    if match is not None:
        match = ".".join(filter(None, match.groups()))
    else:
        match = None
    return match


def detectJava(fSearch=True):
    """
    检测所有已安装的Java路径，三端通用
    """
    javaPathList = []
    foundJava.clear()

    # Windows
    if "windows" in system().lower():
        for i in range(65, 91):
            path = chr(i) + ":\\"
            if osp.exists(path):
                javaPathList.extend(searchFile(path, "java", "exe", fSearch, javaVersionMatcher))
        return javaPathList

    # macOS & linux
    javaList = []
    candidate_paths = set()
    visited_dirs = set()

    def push_candidate(*parts):
        if not parts:
            return
        path = osp.expanduser(osp.join(*parts))
        if not path:
            return
        if osp.isdir(path):
            java_binary = osp.join(path, "java")
            if osp.isfile(java_binary):
                candidate_paths.add(osp.realpath(java_binary))
        elif osp.isfile(path):
            candidate_paths.add(osp.realpath(path))

    def scan_runtime_dir(root, max_depth=4):
        root = osp.expanduser(root)
        if not osp.isdir(root):
            return
        stack = [(root, 0)]
        while stack:
            current, depth = stack.pop()
            real_current = osp.realpath(current)
            if real_current in visited_dirs:
                continue
            visited_dirs.add(real_current)
            if depth > max_depth:
                continue
            java_path = osp.join(real_current, "java")
            if osp.isfile(java_path):
                candidate_paths.add(java_path)
            bin_java = osp.join(real_current, "bin", "java")
            if osp.isfile(bin_java):
                candidate_paths.add(bin_java)
            try:
                entries = listdir(real_current)
            except (PermissionError, FileNotFoundError, NotADirectoryError):
                continue
            for entry in entries:
                child = osp.join(real_current, entry)
                if osp.isdir(child):
                    stack.append((child, depth + 1))

    # 环境变量中的路径
    for raw_path in env.get("PATH", "").split(pathsep):
        cleaned = raw_path.strip()
        if not cleaned:
            continue
        if cleaned.endswith("java") and osp.isfile(cleaned):
            push_candidate(cleaned)
        else:
            push_candidate(cleaned)

    system_name = system().lower()
    if "darwin" in system_name:  # macOS
        # 常见预装或内置位置
        mac_specific_paths = [
            (
                "/Applications/Xcode.app/Contents/Applications/Application"
                " Loader.app/Contents/MacOS/itms/java"
            ),
            "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java",
            "/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/java",
        ]
        for path in mac_specific_paths:
            push_candidate(path)

        base_path = "/Library/Java/JavaVirtualMachines"
        if osp.isdir(base_path):
            for entry in listdir(base_path):
                entry_path = osp.join(base_path, entry)
                if not osp.isdir(entry_path):
                    continue
                push_candidate(entry_path, "Contents", "Home", "bin")

        # 常见第三方启动器内置运行时
        mac_runtime_roots = [
            "~/Library/Application Support/Badlion Client/Data",
            "~/Library/Application Support/Lunar Client",
            "~/Library/Application Support/piston-meta",
        ]
        for root in mac_runtime_roots:
            scan_runtime_dir(root)
    else:  # linux、BSD 等类 Unix 系统
        java_installation_paths = [
            "/usr",
            "/usr/java",
            "/usr/lib/jvm",
            "/usr/lib64/jvm",
            "/opt/jdk",
            "/opt/jdks",
        ]

        for base in java_installation_paths:
            if not base:
                continue
            push_candidate(base, "bin")
            push_candidate(base, "jre", "bin")

            if osp.isdir(base):
                for entry in listdir(base):
                    entry_path = osp.join(base, entry)
                    if not osp.isdir(entry_path):
                        continue
                    push_candidate(entry_path, "bin")
                    push_candidate(entry_path, "jre", "bin")

    # 整理候选 Java 二进制
    for candidate in sorted(candidate_paths):
        if not osp.isfile(candidate) or not osp.exists(candidate):
            continue
        version = getJavaVersion(candidate)
        if version:
            java = Java(candidate, version)
            if java not in javaList:
                javaList.append(java)

    return javaList


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

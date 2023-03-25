from os import listdir
from os import path as ospath
from re import match

from PyQt5.QtCore import QThread, pyqtSignal

FoundJava = []
isNeedFuzzySearch = True
# fmt: off
MatchKeywords = {
    '1.', 'bin', 'cache', 'client', 'corretto', 'craft', 'data', 'download', 'eclipse',
    'env', 'ext', 'file', 'forge', 'game', 'hmcl', 'hotspot', 'java', 'jdk', 'jre',
    'jvm', 'launch', 'mc', 'microsoft', 'mod', 'mojang', 'net', 'netease', 'optifine',
    'oracle', 'path', 'program', 'roaming', 'run', 'runtime', 'server', 'software',
    'temp', 'users', 'users', 'x64', 'x86',
    '世界', '前置', '原版', '启动', '启动', '国服', '官启', '官方', '客户', '应用', '整合',
    '新建文件夹', '服务', '游戏', '环境', '程序', '网易', '软件', '运行', '高清'
}


# fmt: on


def FindStr(s):
    for _s in MatchKeywords:
        if _s in s:
            return True
    return False


def SearchFile(Path, FileKeyword, FileExtended, FuzzySearch):
    JavaPathList = []
    if FuzzySearch:
        if ospath.isfile(Path):
            return JavaPathList
        for File in listdir(Path):
            try:
                if ospath.isfile(Path + "/" + File):
                    if match(f".*?bin/{FileKeyword}.{FileExtended}", Path + "/" + File):
                        JavaPathList.append(Path + "/" + File)
                elif FindStr(File.lower()):
                    JavaPathList.extend(SearchFile(Path + "/" + File, FileKeyword, FileExtended, FuzzySearch))
            except PermissionError:
                pass
    return JavaPathList


def FindJava(FuzzySearch=True):
    JavaPathList = []
    FoundJava.clear()
    for i in range(65, 91):
        Path = chr(i) + ":/"
        if ospath.exists(Path):
            JavaPathList.extend(SearchFile(Path, "java", "exe", FuzzySearch))
    return JavaPathList


class JavaFindWorkThread(QThread):
    foundJavaSignal = pyqtSignal(list)
    finishSignal = pyqtSignal(int)

    def __init__(self, fuzzySearch=True, parent=None):
        super().__init__(parent)
        self._fuzzy = fuzzySearch
        self._sequenceNumber = 0

    @property
    def SequenceNumber(self):
        return self._sequenceNumber

    @SequenceNumber.setter
    def SequenceNumber(self, value):
        self._sequenceNumber = value

    def run(self):
        self.foundJavaSignal.emit(FindJava(self._fuzzy))
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
    def FuzzySearch(self):
        return self._fuzzy

    @FuzzySearch.setter
    def FuzzySearch(self, value):
        self._fuzzy = value

    @property
    def SignalConnect(self):
        return self._connect

    @SignalConnect.setter
    def SignalConnect(self, value):
        self._connect = value

    @property
    def FinishSignalConnect(self):
        return self._finishConnect

    @FinishSignalConnect.setter
    def FinishSignalConnect(self, value):
        self._finishConnect = value

    def Create(self):
        self._instanceCounter += 1
        thread = JavaFindWorkThread(self._fuzzy, self._parent)
        thread.foundJavaSignal.connect(self._connect)
        thread.SequenceNumber = self._instanceCounter
        thread.finishSignal.connect(self._finishConnect)
        self._thread = thread
        return thread

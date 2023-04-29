import platform
from os import listdir
from os import path as ospath
from re import match, search
from subprocess import check_output, STDOUT, CalledProcessError

from PyQt5.QtCore import QThread, pyqtSignal

FoundJava = []
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


# fmt: on

class Java:
    def __init__(self, path, ver):
        self._path = path
        self._version = ver

    @property
    def Path(self):
        return self._path

    @property
    def Version(self):
        return self._version

    def __hash__(self):
        return hash((self._path, self._version))

    def __eq__(self, other):
        if isinstance(other, Java):
            return self._path == other._path and self._version == other._version


def GetJavaVersion(File):
    # 运行java.exe并捕获输出
    try:
        output = check_output([File, '-version'], stderr=STDOUT)
    except CalledProcessError as e:
        print(f"获取Java信息时出错:{e.cmd} | {e.output}")
        return e
    # 从输出中提取版本信息
    version_pattern = r'(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[._](\d+))?(?:-(.+))?'
    version_match = search(version_pattern, output.decode('utf-8'))

    # 输出版本信息
    if version_match:
        version = '.'.join(filter(None, version_match.groups()))
        return version
    else:
        return "Failed to retrieve Java version information."


def FindStr(s):
    for _s in MatchKeywords:
        if _s in s:
            return True
    return False


def SearchFile(Path, FileKeyword, FileExtended, FuzzySearch):
    # construct _Math function
    if 'windows' in platform.system().lower():
        def Match(FileKw, FileExt, P, F):
            return match(f".*?bin/{FileKw}.{FileExt}", ospath.join(P, F))
    else:
        def Match(FileKw, FileExt, P, F):
            return match(f".*?bin/{FileKw}$", ospath.join(P, F))

    return SearchingFile(Path, FileKeyword, FileExtended, FuzzySearch, Match)


def SearchingFile(Path, FileKeyword, FileExtended, FuzzySearch, _Match):
    JavaPathList = []
    if FuzzySearch:
        if ospath.isfile(Path) or 'x86_64-linux-gnu' in Path:
            return JavaPathList
        try:
            for File in listdir(Path):
                try:
                    _Path = ospath.join(Path, File)
                    if ospath.isfile(_Path):
                        if _Match(FileKeyword,FileExtended,Path, File):
                            v = GetJavaVersion(_Path)
                            if not isinstance(v, CalledProcessError):
                                JavaPathList.append(Java(_Path, v))
                    elif FindStr(File.lower()):
                        JavaPathList.extend(
                            SearchingFile(_Path, FileKeyword, FileExtended, FuzzySearch, _Match))
                except PermissionError:
                    pass
        except FileNotFoundError as e:
            print(f'扫描路径时出错: {e}')
    return JavaPathList


def FindJava(FuzzySearch=True):
    JavaPathList = []
    FoundJava.clear()
    if "windows" in platform.system().lower():
        for i in range(65, 91):
            Path = chr(i) + ":/"
            if ospath.exists(Path):
                JavaPathList.extend(SearchFile(Path, "java", "exe", FuzzySearch))
    else:
        JavaPathList.extend(SearchFile("/usr/lib", "java", "", FuzzySearch))
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

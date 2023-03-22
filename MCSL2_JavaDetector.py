from os import listdir
from os import path as ospath
from re import match

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


def SearchFile(Path, FileKeyword, FileExtended):
    if isNeedFuzzySearch:
        for File in listdir(Path):
            try:
                if ospath.isfile(Path + "/" + File):
                    Name, Extended = ospath.splitext(File)
                    if match(f".*?bin/{FileKeyword}.{FileExtended}", Path + "/" + File):
                        FoundJava.append(Path + "/" + File)
                elif FindStr(File.lower()):
                    SearchFile(Path + "/" + File, FileKeyword, FileExtended)
            except PermissionError:
                pass


def FindJava():
    FoundJava.clear()
    for i in range(65, 91):
        Path = chr(i) + ":/"
        if ospath.exists(Path):
            SearchFile(Path, "java", "exe")

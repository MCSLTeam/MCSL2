from re import match
from os import path as ospath, listdir

FoundJava = []
isNeedFuzzySearch = True
MatchKeywords = {"users", "java", "jdk", "env", "环境", "run", "软件", "jre", "bin", "mc", "software", "cache", "temp",
                 "corretto", "roaming", "users", "craft", "program", "世界", "net", "游戏", "oracle", "game", "file",
                 "data", "jvm", "服务", "server", "客户", "client", "整合", "应用", "运行", "前置", "mojang", "官启",
                 "新建文件夹", "eclipse", "microsoft", "hotspot", "runtime", "x86", "x64", "forge", "原版", "optifine",
                 "官方", "启动", "hmcl", "mod", "高清", "download", "launch", "程序", "path", "国服", "网易", "ext",
                 "netease", "1.", "启动"}


def FindStr(s):
    for _s in MatchKeywords:
        if _s in s:
            return True
    return False


def SearchFile(Path, FileKeyword, FileExtended):
    if isNeedFuzzySearch:
        for File in listdir(Path):
            try:
                if ospath.isfile(Path + '/' + File):
                    Name, Extended = ospath.splitext(File)
                    if match(f".*?bin/{FileKeyword}.{FileExtended}", Path + "/" + File):
                        FoundJava.append(Path + "/" + File)
                elif FindStr(File.lower()):
                    SearchFile(Path + '/' + File, FileKeyword, FileExtended)
            except PermissionError:
                pass


def FindJava():
    FoundJava.clear()
    for i in range(65, 91):
        Path = chr(i) + ':/'
        if ospath.exists(Path):
            SearchFile(Path, "java", "exe")

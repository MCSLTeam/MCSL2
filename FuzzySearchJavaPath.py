import os

SearchSet = {"users", "java", "jdk", "env", "环境", "run", "软件", "jre", "bin", "mc", "software", "cache", "temp",
             "corretto", "roaming", "users", "craft", "program", "世界", "net", "游戏", "oracle", "game", "file",
             "data", "jvm", "服务", "server", "客户", "client", "整合", "应用", "运行", "前置", "mojang", "官启",
             "新建文件夹", "eclipse", "microsoft", "hotspot", "runtime", "x86", "x64", "forge", "原版", "optifine",
             "官方", "启动", "hmcl", "mod", "高清", "download", "launch", "程序", "path", "国服", "网易", "ext",
             "netease", "1.", "启动"}


def FindStr(s):
    for _s in SearchSet:
        if _s in s:
            return True
    return False


# 递归遍历
def SearchFile(path, FuzzySearch):
    JavaPathList = []
    if FuzzySearch:
        for File in os.listdir(path):
            try:
                if os.path.isfile(path + '/' + File):
                    Name, Ext = os.path.splitext(File)
                    if Name == "java" and "exe" in Ext:
                        JavaPathList.append(path + '/' + File)
                elif FindStr(File.lower()):
                    JavaPathList.extend(SearchFile(path + '/' + File, FuzzySearch))
            except PermissionError:
                pass
    return JavaPathList


def FindJavaPath(FuzzySearch=True):
    """
    :param FuzzySearch: 是否开启模糊搜索，默认开启，填了false你会发现什么也不返回。/狗头
    :return: 包含java.exe的路径
    """
    JavaPathList = []
    # 检查A-Z:/下的所有文件夹
    for i in range(65, 91):
        Path = chr(i) + ':/'
        if os.path.exists(Path):
            JavaPathList.extend(SearchFile(Path, FuzzySearch))
    return JavaPathList


def FindJavaPathTestCase():
    import time
    begin = time.time()
    print(FindJavaPath())
    print('耗时：', time.time() - begin, 's')
    del time


if __name__ == '__main__':
    FindJavaPathTestCase()

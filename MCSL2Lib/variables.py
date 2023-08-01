from Adapters.Plugin import PluginManager


def Singleton(cls):
    """单例化装饰器"""
    Instances = {}

    def GetInstance(*args, **kwargs):
        if cls not in Instances:
            Instances[cls] = cls(*args, **kwargs)
        return Instances[cls]

    return GetInstance


@Singleton
class ConfigureServerVariables:
    """新建服务器所需变量"""

    def __init__(self):
        self.javaPath: list = []
        self.minMem: int
        self.maxMem: int
        self.corePath: str = ""
        self.coreFileName: str = ""
        self.selectedJavaPath: str = ""
        self.selectedJavaVersion: str = ""
        self.memUnit: str = ""
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"
        self.consoleOutputDeEncodingList = ["follow", "utf-8", "gbk"]
        self.consoleInputDeEncodingList = ["follow", "utf-8", "gbk"]
        self.memUnitList = ["M", "G"]
        self.jvmArg: str = ""
        self.serverName: str = ""

    def resetToDefault(self):
        self.javaPath: list = []
        self.minMem: int
        self.maxMem: int
        self.corePath: str = ""
        self.coreFileName: str = ""
        self.selectedJavaPath: str = ""
        self.selectedJavaVersion: str = ""
        self.memUnit: str = ""
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"
        self.consoleOutputDeEncodingList = ["follow", "utf-8", "gbk"]
        self.consoleInputDeEncodingList = ["follow", "utf-8", "gbk"]
        self.memUnitList = ["M", "G"]
        self.jvmArg: str = ""
        self.serverName: str = ""
        self.icon: str = ""


@Singleton
class EditServerVariables:
    """修改服务器所需变量"""

    def __init__(self):
        self.javaPath: list = []
        self.corePath: str = ""
        self.selectedJavaVersion: str = ""

        self.oldMinMem: int
        self.oldMaxMem: int
        self.oldCoreFileName: str = ""
        self.oldSelectedJavaPath: str = ""
        self.oldMemUnit: str = ""
        self.oldJVMArg: str = ""
        self.oldServerName: str = ""
        self.oldConsoleOutputDeEncoding: str = "follow"
        self.oldConsoleInputDeEncoding: str = "follow"
        self.oldIcon: str = "Grass.png"

        self.minMem: int
        self.maxMem: int
        self.coreFileName: str = ""
        self.selectedJavaPath: str = ""
        self.memUnit: str = ""
        self.jvmArg: str = ""
        self.serverName: str = ""
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"
        self.icon: str = "Grass.png"

        self.consoleOutputDeEncodingList = ["follow", "utf-8", "gbk"]
        self.consoleInputDeEncodingList = ["follow", "utf-8", "gbk"]
        self.memUnitList = ["M", "G"]

    def resetToDefault(self):
        self.javaPath: list = []

        self.oldMinMem: int
        self.oldMaxMem: int
        self.oldCorePath: str = ""
        self.oldCoreFileName: str = ""
        self.oldSelectedJavaPath: str = ""
        self.oldSelectedJavaVersion: str = ""
        self.oldSemUnit: str = ""
        self.oldJVMArg: str = ""
        self.oldServerName: str = ""
        self.oldConsoleOutputDeEncoding: str = "follow"
        self.oldConsoleInputDeEncoding: str = "follow"
        self.oldIcon: str = "Grass.png"

        self.minMem: int
        self.maxMem: int
        self.corePath: str = ""
        self.coreFileName: str = ""
        self.selectedJavaPath: str = ""
        self.selectedJavaVersion: str = ""
        self.memUnit: str = ""
        self.jvmArg: str = ""
        self.serverName: str = ""
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"
        self.icon: str = "Grass.png"

        self.consoleOutputDeEncodingList = ["follow", "utf-8", "gbk"]
        self.consoleInputDeEncodingList = ["follow", "utf-8", "gbk"]
        self.memUnitList = ["M", "G"]


@Singleton
class PluginVariables:
    """插件系统所需变量"""

    def __init__(self):
        self.pluginManager: PluginManager = PluginManager()


class GlobalMCSL2Variables:
    """需要被全局使用的变量"""

    MCSL2Version = "2.1.4.0"
    scrollAreaViewportQss = "background-color: transparent;"


@Singleton
class DownloadVariables:
    """下载页需要的变量"""

    def __init__(self):
        self.MCSLAPIDownloadUrlDict = {}

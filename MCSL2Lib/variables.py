class _configureNewServerVariables:
    
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

class _globalMCSL2Variables:
    MCSL2Version = "2.1.4.0"
    scrollAreaViewportQss = "background-color: transparent;"
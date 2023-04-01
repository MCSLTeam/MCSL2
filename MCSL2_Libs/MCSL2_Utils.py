from json import load, loads, dump
from os import mkdir, listdir
from os import path as ospath
from typing import Callable, Any, Dict

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog
from requests import get

from MCSL2_Libs.MCSL2_AskDialog import Ui_MCSL2_AskDialog
from MCSL2_Libs.MCSL2_Dialog import Ui_MCSL2_Dialog


def Singleton(cls):
    Instances = {}

    def GetInstance(*args, **kwargs):
        if cls not in Instances:
            Instances[cls] = cls(*args, **kwargs)
        return Instances[cls]

    return GetInstance


def InitMCSL():
    global LogFilesCount
    if not ospath.exists(r"MCSL2"):
        LogFilesCount = 0
        mkdir(r"MCSL2")
        mkdir(r"MCSL2/Logs")
        CallMCSL2Dialog(Tip="请注意：\n\n本程序无法在125%的\n\nDPI缩放比下正常运行。\n(本提示仅在首次启动出现)",
                        isNeededTwoButtons=0)
        mkdir(r"MCSL2/Aria2")
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as InitConfig:
            ConfigTemplate = ""
            InitConfig.write(ConfigTemplate)
            InitConfig.close()
        with open(
                r"./MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
        ) as InitServerList:
            ServerListTemplate = '{\n  "MCSLServerList": [\n    {\n      "name": "MCSLReplacer",\n      ' \
                                 '"core_file_name": "MCSLReplacer",\n      "java_path": "MCSLReplacer",' \
                                 '\n      "min_memory": "MCSLReplacer",\n      "max_memory": "MCSLReplacer"\n    }\n  ' \
                                 ']\n} '
            InitServerList.write(ServerListTemplate)
            InitServerList.close()
        if not ospath.exists(r"Servers"):
            mkdir(r"./Servers")

        pass
    elif not ospath.exists(r"MCSL2/Logs"):
        mkdir(r"MCSL2/Logs")
    else:
        LogFilesCount = len(listdir(r"MCSL2/Logs"))
        if not ospath.exists(r"Servers"):
            mkdir(r"./Servers")
        pass


def ParseDownloaderAPIUrl(DownloadSource, DownloadType):
    UrlPrefix = "https://raw.iqiq.io/LxHTT/MCSLDownloaderAPI/master/"
    SourceSuffix = ["SharePoint", "Gitee", "luoxisCloud", "GHProxy", "GitHub"]
    TypeSuffix = [
        "/JavaDownloadInfo.json",
        "/SpigotDownloadInfo.json",
        "/PaperDownloadInfo.json",
        "/BungeeCordDownloadInfo.json",
        "/OfficialCoreDownloadInfo.json",
    ]
    DownloadAPIUrl = UrlPrefix + SourceSuffix[DownloadSource] + TypeSuffix[DownloadType]
    DecodeDownloadJsonsSS = DecodeDownloadJsons(DownloadAPIUrl)
    SubWidgetNames = DecodeDownloadJsonsSS[0]
    DownloadUrls = DecodeDownloadJsonsSS[1]
    FileNames = DecodeDownloadJsonsSS[2]
    FileFormats = DecodeDownloadJsonsSS[3]
    return SubWidgetNames, DownloadUrls, FileNames, FileFormats


def ParseDownloaderAPIUrl1(DownloadSource):
    UrlPrefix = "https://raw.iqiq.io/LxHTT/MCSLDownloaderAPI/master/"
    SourceSuffix = ["SharePoint", "Gitee", "luoxisCloud", "GHProxy", "GitHub"]
    TypeSuffix = [
        "/JavaDownloadInfo.json",
        "/SpigotDownloadInfo.json",
        "/PaperDownloadInfo.json",
        "/BungeeCordDownloadInfo.json",
        "/OfficialCoreDownloadInfo.json",
    ]
    rv = {}
    for i in range(len(TypeSuffix)):
        DownloadAPIUrl = UrlPrefix + SourceSuffix[DownloadSource] + TypeSuffix[i]
        SubWidgetNames, DownloadUrls, FileNames, FileFormats = DecodeDownloadJsons(DownloadAPIUrl)
        rv.update({
            i: dict(zip(("SubWidgetNames", "DownloadUrls", "FileNames", "FileFormats"),
                        (SubWidgetNames, DownloadUrls, FileNames, FileFormats)))
        })
    return {DownloadSource: rv}


def DecodeDownloadJsons(RefreshUrl):
    SubWidgetNames = []
    DownloadUrls = []
    FileFormats = []
    FileNames = []
    try:
        DownloadJson = get(RefreshUrl).text
    except:
        # Tip = "无法连接MCSLAPI，\n\n请检查网络或系统代理设置"
        # CallMCSL2Dialog(Tip, isNeededTwoButtons=0)
        return -2, -2, -2, -2
    try:
        PyDownloadList = loads(DownloadJson)["MCSLDownloadList"]
        for i in PyDownloadList:
            SubWidgetName = i["name"]
            SubWidgetNames.insert(0, SubWidgetName)
            DownloadUrl = i["url"]
            DownloadUrls.insert(0, DownloadUrl)
            FileFormat = i["format"]
            FileFormats.insert(0, FileFormat)
            FileName = i["filename"]
            FileNames.insert(0, FileName)
        return SubWidgetNames, DownloadUrls, FileNames, FileFormats
    except:
        # print(DownloadJson)
        # Tip = "可能解析api内容失败\n\n请检查网络或自己的节点设置"
        # CallMCSL2Dialog(Tip, isNeededTwoButtons=0)
        return -1, -1, -1, -1


def ReadJsonFile(FileName):
    FileName = 'MCSL2/' + FileName
    with open(FileName, 'r', encoding='utf-8') as RJsonFile:
        Data = load(RJsonFile)
    return Data


def SaveJsonFile(FileName, Data):
    FileName = 'MCSL2/' + FileName
    with open(FileName, 'w', encoding='utf-8') as SJsonFile:
        dump(Data, SJsonFile, ensure_ascii=False, indent=4, sort_keys=True)


# Customize dialogs
class MCSL2Dialog(QDialog, Ui_MCSL2_Dialog):
    def __init__(self, Tip, parent=None):
        super(MCSL2Dialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.Dialog_label.setText(Tip)


class MCSL2AskDialog(QDialog, Ui_MCSL2_AskDialog):
    def __init__(self, Tip, parent=None):
        super(MCSL2AskDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.Dialog_label.setText(Tip)


# The function of calling MCSL2 Dialog
def CallMCSL2Dialog(Tip, isNeededTwoButtons, parent=None):
    if isNeededTwoButtons == 0:
        Dialog = MCSL2Dialog(Tip, parent)
    elif isNeededTwoButtons == 1:
        Dialog = MCSL2AskDialog(Tip, parent)
    else:
        return
    Dialog.exec_()
    return Dialog


class JsonReadThread(QThread):
    readSignal = pyqtSignal(dict)

    def __init__(self, FileName, FinishSlot: Callable[[dict, ], Any] = ...):
        super().__init__()
        self.FileName = FileName
        self.Data = None
        if FinishSlot is not ...:
            self.readSignal.connect(FinishSlot)

    def GetFileName(self):
        return self.FileName

    def run(self):
        self.Data = ReadJsonFile(self.FileName)
        self.readSignal.emit(self.Data)

    def GetData(self):
        return self.Data


class JsonSaveThread(QThread):
    saveSignal = pyqtSignal(bool)

    def __init__(self, FileName, Data, FinishSlot: Callable[[], Any] = ...):
        super().__init__()
        self.FileName = FileName
        self.Data = Data
        if FinishSlot is not ...:
            self.saveSignal.connect(FinishSlot)

    def GetFileName(self):
        return self.FileName

    def run(self):
        try:
            SaveJsonFile(self.FileName, self.Data)
            self.saveSignal.emit(True)
        except Exception as e:
            # print(e)
            self.saveSignal.emit(False)


@Singleton
class JsonReadThreadFactory:
    """
        虽然我不会去实例化这个类，但我还是加了个singleton装饰器...
    """

    @classmethod
    def Create(cls, FileName, FinishSlot: Callable[[dict, ], Any] = ...) -> JsonReadThread:
        return JsonReadThread(FileName, FinishSlot)


@Singleton
class JsonSaveThreadFactory:
    """
        虽然我不会去实例化这个类，但我还是加了个singleton装饰器...
    """

    @classmethod
    def Create(cls, FileName, Data, FinishSlot: Callable[[], Any] = ...) -> JsonSaveThread:
        return JsonSaveThread(FileName, Data, FinishSlot)


class FetchDownloadURLThread(QThread):
    """
    用于获取网页内容的线程
    结束时发射fetchSignal信号，参数为url和data组成的元组
    """
    fetchSignal = pyqtSignal(dict)

    def __init__(self, DownloadSource, FinishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.DownloadSource = DownloadSource
        self.Data = None
        if FinishSlot is not ...:
            self.fetchSignal.connect(FinishSlot)

    def getURL(self):
        return self.url

    def run(self):
        self.fetchSignal.emit(ParseDownloaderAPIUrl1(self.DownloadSource))

    def getData(self):
        return self.Data


@Singleton
class FetchDownloadURLThreadFactory:
    singletonThread: Dict[int, FetchDownloadURLThread] = {}

    @classmethod
    def create(cls,
               downloadSrc: int,
               _singleton=False,
               finishSlot=...) -> FetchDownloadURLThread:

        # print({k: v.isRunning() for k, v in cls.singletonThread.items()})
        if _singleton:

            if downloadSrc in cls.singletonThread and cls.singletonThread[downloadSrc].isRunning():
                # print("线程已存在，返回已存在的线程")

                return cls.singletonThread[downloadSrc]
            else:
                thread = FetchDownloadURLThread(downloadSrc, finishSlot)
                cls.singletonThread[downloadSrc] = thread
                return thread
        else:
            return FetchDownloadURLThread(downloadSrc, finishSlot)

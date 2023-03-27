import json
from typing import Callable, Any

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog
from requests import get

from MCSL2_AskDialog import Ui_MCSL2_AskDialog
from MCSL2_Dialog import Ui_MCSL2_Dialog


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


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
        Tip = "无法连接MCSLAPI，\n\n请检查网络或系统代理设置"
        CallMCSL2Dialog(Tip, isNeededTwoButtons=0)
        return -1, -1, -1, -1
    try:
        PyDownloadList = json.loads(DownloadJson)["MCSLDownloadList"]
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
        print(DownloadJson)
        Tip = "可能解析api内容失败\n\n请检查网络或自己的节点设置"
        CallMCSL2Dialog(Tip, isNeededTwoButtons=0)
        return -1, -1, -1, -1


def readJsonFile(filename):
    filename = 'MCSL2/' + filename
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def saveJsonFile(filename, data):
    filename = 'MCSL2/' + filename
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)


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
        dialog = MCSL2Dialog(Tip, parent)
    elif isNeededTwoButtons == 1:
        dialog = MCSL2AskDialog(Tip, parent)
    else:
        return
    dialog.exec()
    return dialog


class JsonReadThread(QThread):
    readSignal = pyqtSignal(dict)

    def __init__(self, filename, finishSlot: Callable[[dict, ], Any] = ...):
        super().__init__()
        self.filename = filename
        self.data = None
        if finishSlot is not ...:
            self.readSignal.connect(finishSlot)

    def getFileName(self):
        return self.filename

    def run(self):
        self.data = readJsonFile(self.filename)
        self.readSignal.emit(self.data)

    def getData(self):
        return self.data


class JsonSaveThread(QThread):
    saveSignal = pyqtSignal(bool)

    def __init__(self, filename, data, finishSlot: Callable[[], Any] = ...):
        super().__init__()
        self.filename = filename
        self.data = data
        if finishSlot is not ...:
            self.saveSignal.connect(finishSlot)

    def getFileName(self):
        return self.filename

    def run(self):
        try:
            saveJsonFile(self.filename, self.data)
            self.saveSignal.emit(True)
        except Exception as e:
            print(e)
            self.saveSignal.emit(False)


@singleton
class JsonReadThreadFactory:
    """
        虽然我不会去实例化这个类，但我还是加了个singleton装饰器...
    """

    @classmethod
    def create(cls, filename, finishSlot: Callable[[dict, ], Any] = ...) -> JsonReadThread:
        return JsonReadThread(filename, finishSlot)


@singleton
class JsonSaveThreadFactory:
    """
        虽然我不会去实例化这个类，但我还是加了个singleton装饰器...
    """

    @classmethod
    def create(cls, filename, data, finishSlot: Callable[[], Any] = ...) -> JsonSaveThread:
        return JsonSaveThread(filename, data, finishSlot)


class FetchDownloadURLThread(QThread):
    """
    用于获取网页内容的线程
    结束时发射fetchSignal信号，参数为url和data组成的元组
    """
    fetchSignal = pyqtSignal(dict)

    def __init__(self, downloadSrc, finishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.downloadSrc = downloadSrc
        self.data = None
        if finishSlot is not ...:
            self.fetchSignal.connect(finishSlot)

    def getURL(self):
        return self.url

    def run(self):
        self.fetchSignal.emit(ParseDownloaderAPIUrl1(self.downloadSrc))

    def getData(self):
        return self.data


@singleton
class FetchDownloadURLThreadFactory:
    singletonThread:dict[int,FetchDownloadURLThread] = {}

    @classmethod
    def create(cls,
               downloadSrc: int,
               _singleton=False,
               finishSlot=...) -> FetchDownloadURLThread:

        print({k: v.isRunning() for k, v in cls.singletonThread.items()})
        if _singleton:

            if downloadSrc in cls.singletonThread and cls.singletonThread[downloadSrc].isRunning():
                print("线程已存在，返回已存在的线程")

                return cls.singletonThread[downloadSrc]
            else:
                thread = FetchDownloadURLThread(downloadSrc, finishSlot)
                cls.singletonThread[downloadSrc] = thread
                return thread
        else:
            return FetchDownloadURLThread(downloadSrc, finishSlot)

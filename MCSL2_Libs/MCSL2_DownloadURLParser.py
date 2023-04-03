from typing import Dict, Callable
from PyQt5.QtCore import pyqtSignal, QThread
from requests import get
from json import loads


def Singleton(cls):
    Instances = {}

    def GetInstance(*args, **kwargs):
        if cls not in Instances:
            Instances[cls] = cls(*args, **kwargs)
        return Instances[cls]

    return GetInstance


class DownloadURLParser:
    def __init__(self):
        pass

    def ParseDownloaderAPIUrl(DownloadSource):
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
            SubWidgetNames, DownloadUrls, FileNames, FileFormats = DownloadURLParser.DecodeDownloadJsons(DownloadAPIUrl)
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
            return -1, -1, -1, -1


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
        self.fetchSignal.emit(DownloadURLParser.ParseDownloaderAPIUrl(self.DownloadSource))

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

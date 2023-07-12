from json import loads
from typing import Dict, Callable

from PyQt5.QtCore import pyqtSignal, QThread

from MCSL2Lib.networkController import Session

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

    def ParseDownloaderAPIUrl():
        UrlArg = "http://mcsl_api.df100.ltd/json"
        TypeArg = [
            "/JavaDownloadInfo.json",
            "/SpigotDownloadInfo.json",
            "/PaperDownloadInfo.json",
            "/BungeeCordDownloadInfo.json",
            "/OfficialCoreDownloadInfo.json",
        ]
        rv = {}
        for i in range(len(TypeArg)):
            DownloadAPIUrl = UrlArg + TypeArg[i]
            downloadFileTitles, downloadFileURLs, downloadFileNames, downloadFileFormats = DownloadURLParser.DecodeDownloadJsons(
                DownloadAPIUrl)
            rv.update({
                i: dict(zip(("downloadFileTitles", "downloadFileURLs", "downloadFileNames", "downloadFileFormats"),
                            (downloadFileTitles, downloadFileURLs, downloadFileNames, downloadFileFormats)))
            })
        return rv

    def DecodeDownloadJsons(RefreshUrl):
        downloadFileTitles = []
        downloadFileURLs = []
        downloadFileFormats = []
        downloadFileNames = []
        try:
            DownloadJson = Session.get(RefreshUrl).text
        except Exception as e:
            return -2, -2, -2, -2
        try:
            PyDownloadList = loads(DownloadJson)["MCSLDownloadList"]
            for i in PyDownloadList:
                downloadFileTitle = i["name"]
                downloadFileTitles.insert(0, downloadFileTitle)
                downloadFileURL = i["url"]
                downloadFileURLs.insert(0, downloadFileURL)
                downloadFileFormat = i["format"]
                downloadFileFormats.insert(0, downloadFileFormat)
                downloadFileName = i["filename"]
                downloadFileNames.insert(0, downloadFileName)
            return downloadFileTitles, downloadFileURLs, downloadFileNames, downloadFileFormats
        except:
            return -1, -1, -1, -1


class FetchDownloadURLThread(QThread):
    """
    用于获取网页内容的线程
    结束时发射fetchSignal信号，参数为url和data组成的元组
    """
    fetchSignal = pyqtSignal(dict)

    def __init__(self, FinishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.Data = None
        if FinishSlot is not ...:
            self.fetchSignal.connect(FinishSlot)

    def getURL(self):
        return self.url

    def run(self):
        self.fetchSignal.emit(
            DownloadURLParser.ParseDownloaderAPIUrl())

    def getData(self):
        return self.Data


@Singleton
class FetchDownloadURLThreadFactory:
    singletonThread: FetchDownloadURLThread = {}

    @classmethod
    def create(cls,
               _singleton=False,
               finishSlot=...) -> FetchDownloadURLThread:

        if _singleton:

            if cls.singletonThread.isRunning():
                # print("线程已存在，返回已存在的线程")

                return cls.singletonThread
            else:
                thread = FetchDownloadURLThread(finishSlot)
                cls.singletonThread = thread
                return thread
        else:
            return FetchDownloadURLThread(finishSlot)

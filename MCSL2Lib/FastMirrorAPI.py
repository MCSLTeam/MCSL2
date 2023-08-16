#     Copyright 2023, MCSL Team, mailto:lxhtt@mcsl.com.cn
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
'''
A function for communicatng with FastMirrorAPI.
'''

from json import loads
from typing import Callable

from PyQt5.QtCore import pyqtSignal, QThread

from MCSL2Lib.networkController import Session


class FMAPIDownloadURLParser:
    """URL设定器"""

    def __init__(self):
        pass

    @staticmethod
    def parseDownloaderAPIUrl():
        UrlArg = "https://download.fastmirror.net/api/v3"
        
        rv = {}
        DownloadAPIUrl = UrlArg
        (
            downloadServerData,
            downloadCode,
            downloadSuccess,
            downloadMsg,
        ) = FMAPIDownloadURLParser.decodeDownloadJsons(DownloadAPIUrl)
        rv.update(
            {
                dict(
                    zip(
                        (
                            "downloadServerData",
                            "downloadCode",
                            "downloadSuccess",
                            "downloadMsg",
                        ),
                        (
                            downloadServerData,
                            downloadCode,
                            downloadSuccess,
                            downloadMsg,
                        ),
                    )
                )
            }
        )
        return rv

    @staticmethod
    def decodeDownloadJsons(RefreshUrl):
        downloadServerDatas = []
        try:
            DownloadJson = Session.get(RefreshUrl).text
        except Exception as e:
            return -2, -2, -2, -2
        try:
            PyDownloadList = loads(DownloadJson)["MCSLDownloadList"]
            for i in PyDownloadList:
                downloadServerData = i["name"]
                downloadServerDatas.insert(0, downloadServerData)
                downloadCode = i["url"]
                downloadSucces = i["format"]
                downloadMsg = i["filename"]
            return (
                downloadServerDatas,
                downloadCodes,
                downloadSuccess,
                downloadMsgs,
            )
        except:
            return -1, -1, -1, -1


class FetchFMAPIDownloadURLThread(QThread):
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
        self.fetchSignal.emit(FMAPIDownloadURLParser.parseDownloaderAPIUrl())

    def getData(self):
        return self.Data


class FetchFMAPIDownloadURLThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(self, _singleton=False, finishSlot=...) -> FetchFMAPIDownloadURLThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchFMAPIDownloadURLThread(finishSlot)
                self.singletonThread = thread
                return thread
        else:
            return FetchFMAPIDownloadURLThread(finishSlot)

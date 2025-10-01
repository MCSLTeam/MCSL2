#     Copyright 2024, MCSL Team, mailto:services@mcsl.com.cn
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
"""
A function for communicatng with AList.
"""

from typing import Callable

from PyQt5.QtCore import pyqtSignal, QThread

from MCSL2Lib.ProgramControllers.networkController import MCSLNetworkSession



class AListDownloadURLParser:
    """URL设定器，可派生"""

    def __init__(self, endPoint: str = None):
        self.endPoint = endPoint

    def parseDownloaderAPIUrl(self, path):
        """可重写：解析下载API URL，返回信息字典"""
        rv = {}
        r = self.decodeDownloadJsons(
            f"{self.endPoint}/api/fs/list", path
        )
        rv["name"] = r[0]
        rv["size"] = r[1]
        rv["is_dir"] = r[2]
        rv["total"] = r[3]
        return rv

    def decodeDownloadJsons(self, APIUrl, path: str, pathPrefix: str = "/"):
        """
        :param APIUrl: API地址
        :param path: 目标路径
        :param pathPrefix: 路径前缀，默认"/"
        """
        name = []
        size = []
        isDir = []
        try:
            s = MCSLNetworkSession()
            downloadJson = s.post(
                url=APIUrl,
                json={
                    "path": f"{pathPrefix}{path}",
                    "password": "",
                    "page": 1,
                    "per_page": 0,
                    "refresh": False,
                },
                headers=s.MCSLNetworkHeaders,
            )
            del s
        except Exception:
            return -2, -2, -2, -2
        try:
            for i in range(downloadJson.json()["data"]["total"]):
                name.append(downloadJson.json()["data"]["content"][i]["name"])
                size.append(downloadJson.json()["data"]["content"][i]["size"])
                isDir.append(downloadJson.json()["data"]["content"][i]["is_dir"])
            return name, size, isDir, downloadJson.json()["data"]["total"]
        except Exception:
            return -1, -1, -1, -1



class FetchAListDownloadURLThread(QThread):
    """
    用于获取网页内容的线程，可派生
    结束时发射fetchSignal信号，参数为url和data组成的元组
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, finishSlot: Callable = None, path: str = "", parser: AListDownloadURLParser = None):
        super().__init__()
        self._id = None
        self.data = None
        self.path = path
        self._parser = parser or AListDownloadURLParser()
        if finishSlot is not None:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        self.data = self._parser.parseDownloaderAPIUrl(self.path)
        self.fetchSignal.emit(self.data)

    def getData(self):
        return self.data



class FetchAListDownloadURLThreadFactory:
    def __init__(self, parser: AListDownloadURLParser = None):
        self.singletonThread = None
        self._parser = parser or AListDownloadURLParser()

    def create(
        self, _singleton=False, finishSlot=None, path: str = ""
    ) -> FetchAListDownloadURLThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchAListDownloadURLThread(finishSlot, path, parser=self._parser)
                self.singletonThread = thread
                return thread
        else:
            return FetchAListDownloadURLThread(finishSlot, path, parser=self._parser)

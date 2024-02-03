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
A function for communicatng with MCSLAPI.
"""

from typing import Callable

from PyQt5.QtCore import pyqtSignal, QThread

from MCSL2Lib.ProgramControllers.networkController import MCSLNetworkSession


class MCSLAPIDownloadURLParser:
    """URL设定器"""

    def __init__(self):
        pass

    @staticmethod
    def parseDownloaderAPIUrl(path):
        rv = {}
        r = MCSLAPIDownloadURLParser.decodeDownloadJsons(
            "https://file.mcsl.com.cn/api/fs/list", path
        )
        rv["name"] = r[0]
        rv["size"] = r[1]
        rv["is_dir"] = r[2]
        rv["total"] = r[3]
        return rv

    @staticmethod
    def decodeDownloadJsons(APIUrl, path: str):
        name = []
        size = []
        isDir = []
        try:
            downloadJson = (s := MCSLNetworkSession()).post(
                url=APIUrl,
                json={
                    "path": f"/MCSL2/MCSLAPI{path}",
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


class FetchMCSLAPIDownloadURLThread(QThread):
    """
    用于获取网页内容的线程
    结束时发射fetchSignal信号，参数为url和data组成的元组
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, finishSlot: Callable = None, path: str = ""):
        super().__init__()
        self._id = None
        self.data = None
        self.path = path
        if finishSlot is not None:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        self.fetchSignal.emit(MCSLAPIDownloadURLParser.parseDownloaderAPIUrl(self.path))

    def getData(self):
        return self.data


class FetchMCSLAPIDownloadURLThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(
        self, _singleton=False, finishSlot=None, path: str = ""
    ) -> FetchMCSLAPIDownloadURLThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchMCSLAPIDownloadURLThread(finishSlot, path)
                self.singletonThread = thread
                return thread
        else:
            return FetchMCSLAPIDownloadURLThread(finishSlot, path)

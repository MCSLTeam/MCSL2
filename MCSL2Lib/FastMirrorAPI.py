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
"""
A function for communicatng with FastMirrorAPI.
"""

from json import loads
from typing import Callable

from PyQt5.QtCore import pyqtSignal, QThread

from MCSL2Lib.networkController import Session


class FMAPIDownloadURLParser:
    """URL设定器"""

    def __init__(self):
        pass

    @staticmethod
    def parseFMAPIUrl():
        fmAPI = "https://download.fastmirror.net/api/v3"

        rv = {}
        downloadAPIUrl = fmAPI
        (
            data,
            code,
            success,
            message,
        ) = FMAPIDownloadURLParser.decodeDownloadJsons(downloadAPIUrl)
        rv.update(
            {
                dict(
                    zip(
                        (
                            "data",
                            "code",
                            "success",
                            "message",
                        ),
                        (
                            data,
                            code,
                            success,
                            message,
                        ),
                    )
                )
            }
        )
        return rv

    @staticmethod
    def parseFMAPIUrl():
        fmAPI = "https://download.fastmirror.net/api/v3"

        rv = {}
        downloadAPIUrl = fmAPI
        (
            data,
            code,
            success,
            message,
        ) = FMAPIDownloadURLParser.decodeDownloadJsons(downloadAPIUrl)
        rv.update(
            {
                dict(
                    zip(
                        (
                            "data",
                            "code",
                            "success",
                            "message",
                        ),
                        (
                            data,
                            code,
                            success,
                            message,
                        ),
                    )
                )
            }
        )
        return rv


    @staticmethod
    def decodeDownloadJsons(downloadAPIUrl):
        data = []
        try:
            apiData = loads(Session.get(downloadAPIUrl).text)
        except Exception as e:
            return -2
        try:
            if apiData["success"]:
                for i in apiData["data"]:
                    data.insert(0, i)
                return data
        except:
            return -1


class FetchFMAPIThread(QThread):
    """
    用于获取/api/v3
    即核心类型+游戏版本列表
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
        self.fetchSignal.emit(FMAPIDownloadURLParser.parseFMAPIUrl())

    def getData(self):
        return self.Data


class FetchFMAPICoreVersionThread(QThread):
    """
    用于获取/api/v3/{name}/{mc_version}
    即服务端版本列表
    需加上?offset=0&limit=25参数
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
        self.fetchSignal.emit(FMAPIDownloadURLParser.parseFMAPIUrl())

    def getData(self):
        return self.Data


class FetchFMAPIDownloadURLThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(self, _singleton=False, finishSlot=...) -> FetchFMAPIThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchFMAPIThread(finishSlot)
                self.singletonThread = thread
                return thread
        else:
            return FetchFMAPIThread(finishSlot)

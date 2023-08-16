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


class FastMirrorAPIDownloadURLParser:
    """URL设定器"""

    def __init__(self):
        pass

    @staticmethod
    def parseFastMirrorAPIUrl():
        fastMirrorAPI = "https://download.fastmirror.net/api/v3"
        rv = {}
        downloadAPIUrl = fastMirrorAPI
        (
            data,
            code,
            success,
            message,
        ) = FastMirrorAPIDownloadURLParser.decodeFastMirrorJsons(downloadAPIUrl)
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
    def decodeFastMirrorJsons(downloadAPIUrl):
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

    @staticmethod
    def parseFastMirrorAPICoreVersionUrl(name, mcVersion):
        fastMirrorAPI = f"https://download.fastmirror.net/api/v3/{name}/{mcVersion}?offset=0&limit=25"
        rv = {}
        downloadAPIUrl = fastMirrorAPI
        (
            data,
            code,
            success,
            message,
        ) = FastMirrorAPIDownloadURLParser.decodeFastMirrorCoreVersionJsons(
            downloadAPIUrl
        )
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
    def decodeFastMirrorCoreVersionJsons(downloadAPIUrl):
        builds = []
        try:
            apiData = loads(Session.get(downloadAPIUrl).text)
        except Exception as e:
            return -2
        try:
            if apiData["success"]:
                for i in apiData["data"]["builds"]:
                    builds.insert(0, i)
                return builds
        except:
            return -1

    @staticmethod
    def parseFastMirrorAPICoreDownloadUrl(name, mcVersion, coreVersion):
        fastMirrorAPI = f"https://download.fastmirror.net/api/v3/{name}/{mcVersion}/{coreVersion}"
        rv = {}
        downloadAPIUrl = fastMirrorAPI
        (
            data,
            code,
            success,
            message,
        ) = FastMirrorAPIDownloadURLParser.decodeFastMirrorCoreVersionJsons(
            downloadAPIUrl
        )
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
    def decodeFastMirrorCoreDownloadJsons(downloadAPIUrl):
        data = []
        try:
            apiData = loads(Session.get(downloadAPIUrl).text)
        except Exception as e:
            return -2
        try:
            if apiData["success"]:
                data = apiData["data"]
                return data
        except:
            return -1


class FetchFastMirrorAPIThread(QThread):
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
        self.fetchSignal.emit(FastMirrorAPIDownloadURLParser.parseFastMirrorAPIUrl())

    def getData(self):
        return self.Data


class FetchFastMirrorAPICoreVersionThread(QThread):
    """
    用于获取/api/v3/{name}/{mc_version}
    即服务端版本列表
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, name, mcVersion, FinishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.Data = None
        self.name = name
        self.mcVersion = mcVersion
        if FinishSlot is not ...:
            self.fetchSignal.connect(FinishSlot)

    def getURL(self):
        return self.url

    def run(self):
        self.fetchSignal.emit(FastMirrorAPIDownloadURLParser.parseFastMirrorAPICoreVersionUrl(name=self.name, mcVersion=self.mcVersion))

    def getData(self):
        return self.Data


class FetchFastMirrorAPIDownloadURLThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(self, _singleton=False, finishSlot=...) -> FetchFastMirrorAPIThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchFastMirrorAPIThread(finishSlot)
                self.singletonThread = thread
                return thread
        else:
            return FetchFastMirrorAPIThread(finishSlot)

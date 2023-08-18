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
from collections import defaultdict
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
        downloadAPIUrl = fastMirrorAPI
        rv = defaultdict(list)
        r = FastMirrorAPIDownloadURLParser.decodeFastMirrorJsons(downloadAPIUrl)

        if r not in [-1, -2]:
            for e in r:
                rv["name"].append(e["name"])
                rv["mc_versions"].append(e["mc_versions"])
                rv["tag"].append(e["tag"])
                rv["homepage"].append(e["homepage"])
                rv["recommend"].append(e["recommend"])
            return rv

    @staticmethod
    def decodeFastMirrorJsons(downloadAPIUrl):
        data = []
        try:
            apiData = loads(Session.get(downloadAPIUrl).text)
        except Exception:
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
            name,
            mc_version,
            core_version,
            update_time,
            sha1,
        ) = FastMirrorAPIDownloadURLParser.decodeFastMirrorCoreVersionJsons(
            downloadAPIUrl
        )
        rv.update(
            {
                dict(
                    zip(
                        (
                            "name",
                            "mc_version",
                            "core_version",
                            "update_time",
                            "sha1",
                        ),
                        (
                            name,
                            mc_version,
                            core_version,
                            update_time,
                            sha1,
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
        except Exception:
            return -2
        try:
            if apiData["success"]:
                for i in apiData["data"]["builds"]:
                    builds.insert(0, i)
                return builds
        except:
            return -1

    @staticmethod
    def parseFastMirrorAPIRealCoreDownloadURL(name, mcVersion, coreVersion):
        fastMirrorAPI = (
            f"https://download.fastmirror.net/api/v3/{name}/{mcVersion}/{coreVersion}"
        )
        downloadAPIUrl = fastMirrorAPI
        downloadURL: str = (
            FastMirrorAPIDownloadURLParser.getFastMirrorAPIRealCoreDownloadURL(
                downloadAPIUrl
            )
        )
        return downloadURL

    @staticmethod
    def getFastMirrorAPIRealCoreDownloadURL(downloadAPIUrl):
        downloadURL = ""
        try:
            apiData = loads(Session.get(downloadAPIUrl).text)
        except Exception:
            return -2
        try:
            if apiData["success"]:
                downloadURL = apiData["data"]["download_url"]
                return downloadURL
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
        self.fetchSignal.emit(
            FastMirrorAPIDownloadURLParser.parseFastMirrorAPICoreVersionUrl(
                name=self.name, mcVersion=self.mcVersion
            )
        )

    def getData(self):
        return self.Data


class FetchFastMirrorAPICoreDownloadThread(QThread):
    """
    用于获取/api/v3/{name}/{mc_version}/{coreVersion}
    即真正的下载地址
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, name, mcVersion, coreVersion, FinishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.Data = None
        self.name = name
        self.mcVersion = mcVersion
        self.coreVersion = coreVersion
        if FinishSlot is not ...:
            self.fetchSignal.connect(FinishSlot)

    def getURL(self):
        return self.url

    def run(self):
        self.fetchSignal.emit(
            FastMirrorAPIDownloadURLParser.parseFastMirrorAPIRealCoreDownloadURL(
                name=self.name, mcVersion=self.mcVersion, coreVersion=self.coreVersion
            )
        )

    def getData(self):
        return self.Data


class FetchFastMirrorAPIThreadFactory:
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


class FetchFastMirrorAPICoreVersionThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(
            self, name, mcVersion, _singleton=False, finishSlot=...
    ) -> FetchFastMirrorAPICoreVersionThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchFastMirrorAPICoreVersionThread(
                    name=name,
                    mcVersion=mcVersion,
                    FinishSlot=finishSlot
                )
                self.singletonThread = thread
                return thread
        else:
            return FetchFastMirrorAPICoreVersionThread(finishSlot)


class FetchFastMirrorAPICoreDownloadThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(
            self, name, mcVersion, coreVersion, _singleton=False, finishSlot=...
    ) -> FetchFastMirrorAPICoreDownloadThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchFastMirrorAPICoreDownloadThread(
                    name=name,
                    mcVersion=mcVersion,
                    coreVersion=coreVersion,
                    FinishSlot=finishSlot
                )
                self.singletonThread = thread
                return thread
        else:
            return FetchFastMirrorAPICoreDownloadThread(finishSlot)

#     Copyright 2023, MCSL Team, mailto:lxhtt@vip.qq.com
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
from typing import Callable

from PyQt5.QtCore import pyqtSignal, QThread
from MCSL2Lib.Controllers.networkController import (
    MCSLNetworkSession,
    MCSLNetworkHeaders,
)


class FastMirrorAPIDownloadURLParser:
    """URL设定器"""

    def __init__(self):
        pass

    @staticmethod
    def parseFastMirrorAPIUrl():
        rv = defaultdict(list)
        r = FastMirrorAPIDownloadURLParser.decodeFastMirrorJsons(
            "https://download.fastmirror.net/api/v3"
        )
        if type(r) is list:
            for e in r:
                rv["name"].append(e["name"])
                rv["mc_versions"].append(e["mc_versions"])
                rv["tag"].append(e["tag"])
                rv["homepage"].append(e["homepage"])
                rv["recommend"].append(e["recommend"])
            return rv
        else:
            return {"name": -1}

    @staticmethod
    def decodeFastMirrorJsons(downloadAPIUrl):
        data = []
        try:
            apiData = (
                MCSLNetworkSession().get(url=downloadAPIUrl, headers=MCSLNetworkHeaders).json()
            )
        except Exception:
            return -2
        try:
            if apiData["success"]:
                for i in apiData["data"]:
                    data.append(i)
                return data
        except Exception:
            return -1

    @staticmethod
    def parseFastMirrorAPICoreVersionUrl(name, mcVersion):
        rv = defaultdict(list)
        r = FastMirrorAPIDownloadURLParser.decodeFastMirrorCoreVersionJsons(
            f"https://download.fastmirror.net/api/v3/{name}/{mcVersion}?offset=0&limit=25"
        )
        if type(r) is list:
            for e in r:
                rv["name"].append(e["name"])
                rv["mc_version"].append(e["mc_version"])
                rv["core_version"].append(e["core_version"])
                rv["update_time"].append(e["update_time"])
                rv["sha1"].append(e["sha1"])
            return rv
        else:
            return {"name": -1}

    @staticmethod
    def decodeFastMirrorCoreVersionJsons(downloadAPIUrl):
        builds = []
        try:
            apiData = (
                MCSLNetworkSession().get(url=downloadAPIUrl, headers=MCSLNetworkHeaders).json()
            )
        except Exception:
            return -2
        try:
            if apiData["success"]:
                for i in apiData["data"]["builds"]:
                    builds.append(i)
                return builds
        except Exception:
            return -1


class FetchFastMirrorAPIThread(QThread):
    """
    用于获取/api/v3
    即核心类型+游戏版本列表
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, finishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.data = None
        if finishSlot is not ...:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        self.fetchSignal.emit(FastMirrorAPIDownloadURLParser.parseFastMirrorAPIUrl())

    def getData(self):
        return self.data


class FetchFastMirrorAPICoreVersionThread(QThread):
    """
    用于获取/api/v3/{name}/{mc_version}
    即服务端版本列表
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, name, mcVersion, finishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.data = None
        self.name = name
        self.mcVersion = mcVersion
        if finishSlot is not ...:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        self.fetchSignal.emit(
            FastMirrorAPIDownloadURLParser.parseFastMirrorAPICoreVersionUrl(
                name=self.name, mcVersion=self.mcVersion
            )
        )

    def getData(self):
        return self.data


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
                    name=name, mcVersion=mcVersion, finishSlot=finishSlot
                )
                self.singletonThread = thread
                return thread
        else:
            return FetchFastMirrorAPICoreVersionThread(finishSlot)

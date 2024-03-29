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
A function for communicatng with PolarsAPI.
"""

from collections import defaultdict
from typing import Callable

from PyQt5.QtCore import pyqtSignal, QThread
from MCSL2Lib.ProgramControllers.networkController import (
    MCSLNetworkSession,
)


class PolarsAPIDownloadURLParser:
    """URL设定器"""

    def __init__(self):
        pass

    @staticmethod
    def parsePolarsAPIUrl():
        rv = defaultdict(list)
        r = PolarsAPIDownloadURLParser.decodePolarTypeJsons(
            "https://mirror.polars.cc/api/query/minecraft/core"
        )
        if type(r) is list:
            for e in r:
                rv["id"].append(e["id"])
                rv["name"].append(e["name"])
                rv["description"].append(e["description"])
            return rv
        else:
            return {"name": -1}

    @staticmethod
    def decodePolarTypeJsons(downloadAPIUrl):
        data = []
        try:
            apiData = (
                (s := MCSLNetworkSession())
                .get(url=downloadAPIUrl, headers=s.MCSLNetworkHeaders)
                .json()
            )
            del s
        except Exception:
            return -2
        try:
            for i in apiData:
                data.insert(0, i)
            return data
        except Exception:
            return -1

    @staticmethod
    def parsePolarsAPICoreUrl(coreType):
        rv = defaultdict(list)
        r = PolarsAPIDownloadURLParser.decodePolarsAPICoreJsons(
            f"https://mirror.polars.cc/api/query/minecraft/core/{coreType}"
        )
        if type(r) is list:
            for e in r:
                rv["name"].append(e["name"])
                rv["downloadUrl"].append(e["downloadUrl"])
            return rv
        else:
            return {"name": -1}

    @staticmethod
    def decodePolarsAPICoreJsons(downloadAPIUrl):
        cores = []
        try:
            apiData = (
                (s := MCSLNetworkSession())
                .get(url=downloadAPIUrl, headers=s.MCSLNetworkHeaders)
                .json()
            )
            del s
        except Exception:
            return -2
        try:
            for i in apiData:
                cores.insert(0, i)
            return cores
        except Exception:
            return -1


class FetchPolarsAPITypeThread(QThread):
    fetchSignal = pyqtSignal(dict)

    def __init__(self, finishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.data = None
        if finishSlot is not ...:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        self.fetchSignal.emit(PolarsAPIDownloadURLParser.parsePolarsAPIUrl())

    def getData(self):
        return self.data


class FetchPolarsAPICoreThread(QThread):
    fetchSignal = pyqtSignal(dict)

    def __init__(self, idx, FinishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.data = None
        self.idx = idx
        if FinishSlot is not ...:
            self.fetchSignal.connect(FinishSlot)

    def run(self):
        self.fetchSignal.emit(PolarsAPIDownloadURLParser.parsePolarsAPICoreUrl(coreType=self.idx))

    def getData(self):
        return self.data


class FetchPolarsAPITypeThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(self, _singleton=False, finishSlot=...) -> FetchPolarsAPITypeThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchPolarsAPITypeThread(finishSlot)
                self.singletonThread = thread
                return thread
        else:
            return FetchPolarsAPITypeThread(finishSlot)


class FetchPolarsAPICoreThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(self, idx, _singleton=False, finishSlot=...) -> FetchPolarsAPICoreThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchPolarsAPICoreThread(idx=idx, FinishSlot=finishSlot)
                self.singletonThread = thread
                return thread
        else:
            return FetchPolarsAPICoreThread(finishSlot)

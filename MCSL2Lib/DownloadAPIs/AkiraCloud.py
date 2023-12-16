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
A function for communicatng with AkiraCloud Mirror.
"""

from typing import Callable

from PyQt5.QtCore import pyqtSignal, QThread
from MCSL2Lib.Controllers.networkController import (
    MCSLNetworkSession,
    MCSLNetworkHeaders,
)

import re
from html.parser import HTMLParser


class AkiraHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inTable = False
        self.inTd = False
        self.currentData = []
        self.allList = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.inTable = True
        elif self.inTable and tag == "td":
            self.inTd = True

    def handle_data(self, data):
        if self.inTd:
            self.currentData.append(data.strip())

    def handle_endtag(self, tag):
        if tag == "table":
            self.inTable = False
        elif tag == "td":
            self.inTd = False
            if self.currentData:
                self.allList.append(self.currentData[-1])
                self.currentData = []

    def feed(self, data: str) -> list:
        super().feed(data)
        if "Parent Directory" in self.allList:
            self.allList.remove("Parent Directory")
        if "常用工具" in self.allList:
            self.allList.remove("常用工具")
        if "mirror.akiracloud.net" in self.allList:
            self.allList.remove("mirror.akiracloud.net")
        return self.allList


class AkiraCloudDownloadURLParser:
    def __init__(self) -> None:
        pass

    @classmethod
    def getDownloadTypeList(cls) -> list:
        try:
            return cls._parseHTML(cls._getAPI("/"))
        except Exception:
            return []

    @classmethod
    def getDownloadCoreList(cls, coreType: str) -> list:
        try:
            return {"name": coreType, "list": cls._parseHTML(cls._getAPI(f"/{coreType}"))}
        except Exception:
            return {"name": "-1"}

    @classmethod
    def _getAPI(cls, APIPath: str) -> str:
        return (
            MCSLNetworkSession()
            .get(
                url=f"https://mirror.akiracloud.net{APIPath}",
                headers=MCSLNetworkHeaders,
            )
            .text
        )

    @classmethod
    def _parseHTML(cls, htmlContent: str):
        parsedList = AkiraHTMLParser().feed(htmlContent)
        return list(
            [
                item
                for item in parsedList
                if not re.search(re.compile(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}|\d+\sKB"), item)
            ]
        )


class FetchAkiraTypeThread(QThread):
    fetchSignal = pyqtSignal(list)

    def __init__(self, finishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.data = None
        if finishSlot is not ...:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        self.fetchSignal.emit(AkiraCloudDownloadURLParser.getDownloadTypeList())

    def getData(self):
        return self.data


class FetchAkiraCoreThread(QThread):
    fetchSignal = pyqtSignal(dict)

    def __init__(self, coreType, finishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.data = None
        self.coreType = coreType
        if finishSlot is not ...:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        self.fetchSignal.emit(
            AkiraCloudDownloadURLParser.getDownloadCoreList(coreType=self.coreType)
        )

    def getData(self):
        return self.data


class FetchAkiraTypeThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(self, _singleton=False, finishSlot=...) -> FetchAkiraTypeThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchAkiraTypeThread(finishSlot)
                self.singletonThread = thread
                return thread
        else:
            return FetchAkiraTypeThread(finishSlot)


class FetchAkiraCoreThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(self, coreType, _singleton=False, finishSlot=...) -> FetchAkiraCoreThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchAkiraCoreThread(coreType=coreType, finishSlot=finishSlot)
                self.singletonThread = thread
                return thread
        else:
            return FetchAkiraCoreThread(finishSlot)

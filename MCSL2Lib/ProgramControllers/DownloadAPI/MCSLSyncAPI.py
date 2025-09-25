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
A function for communicating with MCSL-Sync API.
"""

from typing import Callable

from PyQt5 import sip
from PyQt5.QtCore import pyqtSignal, QThread
from MCSL2Lib.ProgramControllers.networkController import MCSLNetworkSession


class MCSLSyncAPIDownloadURLParser:
    """MCSL-Sync API URL解析器"""

    def __init__(self):
        pass

    @staticmethod
    def parseMCSLSyncCoreList():
        """获取核心列表"""
        r = MCSLSyncAPIDownloadURLParser.decodeMCSLSyncJsons("https://sync-api.mcsl.com.cn/core")
        if isinstance(r, list):
            return {"cores": r}
        elif r is None:
            return {"cores": []}
        else:
            return {"cores": []}

    @staticmethod
    def parseMCSLSyncCoreVersions(core_type):
        """获取特定核心支持的MC版本列表"""
        r = MCSLSyncAPIDownloadURLParser.decodeMCSLSyncJsons(
            f"https://sync-api.mcsl.com.cn/core/{core_type}"
        )
        if isinstance(r, dict) and "type" in r and "versions" in r:
            return {"type": r["type"], "versions": r["versions"]}
        elif r is None:
            return {"type": "", "versions": []}
        else:
            return {"type": "", "versions": []}

    @staticmethod
    def parseMCSLSyncCoreBuilds(core_type, mc_version):
        """获取特定核心特定MC版本的构建列表"""
        r = MCSLSyncAPIDownloadURLParser.decodeMCSLSyncJsons(
            f"https://sync-api.mcsl.com.cn/core/{core_type}/{mc_version}"
        )
        if isinstance(r, dict) and "type" in r and "builds" in r:
            return {"type": r["type"], "builds": r["builds"]}
        elif r is None:
            return {"type": "", "builds": []}
        else:
            return {"type": "", "builds": []}

    @staticmethod
    def parseMCSLSyncBuildDetails(core_type, mc_version, core_version):
        """获取特定构建的详细信息"""
        r = MCSLSyncAPIDownloadURLParser.decodeMCSLSyncJsons(
            f"https://sync-api.mcsl.com.cn/core/{core_type}/{mc_version}/{core_version}"
        )
        if isinstance(r, dict):
            if isinstance(r.get("build"), dict):
                return r.get("build")
            return r
        elif r is None:
            return {}
        else:
            return {}

    @staticmethod
    def decodeMCSLSyncJsons(downloadAPIUrl):
        """解析MCSL-Sync API响应"""
        s = MCSLNetworkSession()
        response = s.get(url=downloadAPIUrl, headers=s.MCSLNetworkHeaders)
        apiData = response.json()
        del s

        if apiData["code"] == 200:
            return apiData["data"]
        else:
            print(
                f"API returned error code: {apiData.get('code', 'unknown')}, "
                f"message: {apiData.get('msg', 'unknown')}"
            )
            return apiData["data"]  # 返回数据而不是错误码


class FetchMCSLSyncCoreListThread(QThread):
    """
    用于获取核心列表的线程
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, finishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.data = None
        if finishSlot is not ...:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        try:
            result = MCSLSyncAPIDownloadURLParser.parseMCSLSyncCoreList()
            self.fetchSignal.emit(result)
        except Exception as e:
            print(f"Error in FetchMCSLSyncCoreListThread: {e}")
            self.fetchSignal.emit({"cores": []})

    def getData(self):
        return self.data


class FetchMCSLSyncCoreVersionsThread(QThread):
    """
    用于获取特定核心版本列表的线程
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, core_type, finishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.data = None
        self.core_type = core_type
        if finishSlot is not ...:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        try:
            result = MCSLSyncAPIDownloadURLParser.parseMCSLSyncCoreVersions(self.core_type)
            self.fetchSignal.emit(result)
        except Exception as e:
            print(f"Error in FetchMCSLSyncCoreVersionsThread: {e}")
            self.fetchSignal.emit({"type": "", "versions": []})

    def getData(self):
        return self.data


class FetchMCSLSyncCoreBuildsThread(QThread):
    """
    用于获取特定核心特定MC版本构建列表的线程
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, core_type, mc_version, finishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.data = None
        self.core_type = core_type
        self.mc_version = mc_version
        if finishSlot is not ...:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        try:
            result = MCSLSyncAPIDownloadURLParser.parseMCSLSyncCoreBuilds(
                self.core_type, self.mc_version
            )
            self.fetchSignal.emit(result)
        except Exception as e:
            print(f"Error in FetchMCSLSyncCoreBuildsThread: {e}")
            self.fetchSignal.emit({"type": "", "builds": []})

    def getData(self):
        return self.data


class FetchMCSLSyncBuildDetailsThread(QThread):
    """
    用于获取构建详细信息的线程
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, core_type, mc_version, core_version, finishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.data = None
        self.core_type = core_type
        self.mc_version = mc_version
        self.core_version = core_version
        if finishSlot is not ...:
            self.fetchSignal.connect(finishSlot)

    def run(self):
        try:
            result = MCSLSyncAPIDownloadURLParser.parseMCSLSyncBuildDetails(
                self.core_type, self.mc_version, self.core_version
            )
            self.fetchSignal.emit(result)
        except Exception as e:
            print(f"Error in FetchMCSLSyncBuildDetailsThread: {e}")
            self.fetchSignal.emit({})

    def getData(self):
        return self.data


class FetchMCSLSyncCoreListThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(self, _singleton=False, finishSlot=...) -> FetchMCSLSyncCoreListThread:
        self._validate_singleton()
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchMCSLSyncCoreListThread(finishSlot)
                self.singletonThread = thread
                thread.finished.connect(
                    lambda thread_ref=thread: self._on_singleton_finished(thread_ref)
                )
                return thread
        else:
            return FetchMCSLSyncCoreListThread(finishSlot)

    def _validate_singleton(self):
        if self.singletonThread is not None:
            try:
                if sip.isdeleted(self.singletonThread):
                    self.singletonThread = None
            except RuntimeError:
                self.singletonThread = None

    def _on_singleton_finished(self, thread):
        if self.singletonThread is thread:
            self.singletonThread = None


class FetchMCSLSyncCoreVersionsThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(
        self, core_type, _singleton=False, finishSlot=...
    ) -> FetchMCSLSyncCoreVersionsThread:
        self._validate_singleton()
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchMCSLSyncCoreVersionsThread(
                    core_type=core_type, finishSlot=finishSlot
                )
                self.singletonThread = thread
                thread.finished.connect(
                    lambda thread_ref=thread: self._on_singleton_finished(thread_ref)
                )
                return thread
        else:
            return FetchMCSLSyncCoreVersionsThread(core_type, finishSlot)

    def _validate_singleton(self):
        if self.singletonThread is not None:
            try:
                if sip.isdeleted(self.singletonThread):
                    self.singletonThread = None
            except RuntimeError:
                self.singletonThread = None

    def _on_singleton_finished(self, thread):
        if self.singletonThread is thread:
            self.singletonThread = None


class FetchMCSLSyncCoreBuildsThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(
        self, core_type, mc_version, _singleton=False, finishSlot=...
    ) -> FetchMCSLSyncCoreBuildsThread:
        self._validate_singleton()
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchMCSLSyncCoreBuildsThread(
                    core_type=core_type, mc_version=mc_version, finishSlot=finishSlot
                )
                self.singletonThread = thread
                thread.finished.connect(
                    lambda thread_ref=thread: self._on_singleton_finished(thread_ref)
                )
                return thread
        else:
            return FetchMCSLSyncCoreBuildsThread(core_type, mc_version, finishSlot)

    def _validate_singleton(self):
        if self.singletonThread is not None:
            try:
                if sip.isdeleted(self.singletonThread):
                    self.singletonThread = None
            except RuntimeError:
                self.singletonThread = None

    def _on_singleton_finished(self, thread):
        if self.singletonThread is thread:
            self.singletonThread = None


class FetchMCSLSyncBuildDetailsThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(
        self, core_type, mc_version, core_version, _singleton=False, finishSlot=...
    ) -> FetchMCSLSyncBuildDetailsThread:
        self._validate_singleton()
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchMCSLSyncBuildDetailsThread(
                    core_type=core_type,
                    mc_version=mc_version,
                    core_version=core_version,
                    finishSlot=finishSlot,
                )
                self.singletonThread = thread
                thread.finished.connect(
                    lambda thread_ref=thread: self._on_singleton_finished(thread_ref)
                )
                return thread
        else:
            return FetchMCSLSyncBuildDetailsThread(core_type, mc_version, core_version, finishSlot)

    def _validate_singleton(self):
        if self.singletonThread is not None:
            try:
                if sip.isdeleted(self.singletonThread):
                    self.singletonThread = None
            except RuntimeError:
                self.singletonThread = None

    def _on_singleton_finished(self, thread):
        if self.singletonThread is thread:
            self.singletonThread = None

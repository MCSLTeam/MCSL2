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
Multi-thread download controller for MCSL2.
Using pypdl for high-performance parallel downloading.
"""

import hashlib
import json
import threading
from os import path as osp, mkdir, remove
import time
from typing import Optional, Callable, Dict
from pathlib import Path
from urllib.parse import unquote, urlsplit
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QMutex
from pypdl import Pypdl

from MCSL2Lib.ProgramControllers.settingsController import cfg
from MCSL2Lib.ProgramControllers.networkController import MCSLNetworkSession
from MCSL2Lib.utils import (
    readFile,
    WorkingThreads,
    MCSL2Logger,
    writeFile,
    readBytesFile,
)


entries = {}
entries_mutex = QMutex()


def getReadableSize(size_bytes):
    """将字节数转换为可读的大小格式"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"


def getReadableSpeed(speed_bytes_per_sec):
    """将字节/秒转换为可读的速度格式"""
    if speed_bytes_per_sec < 1024:
        # 小于 1KB/s 时显示为 0KB/s
        return "0KB/s"
    
    speed = speed_bytes_per_sec
    size_names = ["B/s", "KB/s", "MB/s", "GB/s"]
    i = 0
    
    while speed >= 1024 and i < len(size_names) - 1:
        speed /= 1024.0
        i += 1
    
    # 根据大小选择合适的小数位数
    if i == 0:  # B/s
        return f"{int(speed)}B/s"
    elif speed >= 100:  # >= 100 KB/s or MB/s
        return f"{speed:.0f}{size_names[i]}"
    elif speed >= 10:  # >= 10 KB/s or MB/s
        return f"{speed:.1f}{size_names[i]}"
    else:  # < 10 KB/s or MB/s
        return f"{speed:.2f}{size_names[i]}"


def formatETA(seconds):
    """将秒数转换为可读的时间格式"""
    if seconds <= 0 or seconds == float("inf"):
        return "-"

    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes}m"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        if minutes > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{hours}h"
    else:
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        if hours > 0:
            return f"{days}d {hours}h"
        else:
            return f"{days}d"


class DownloadTask(QObject):
    """
    基于 pypdl 的多线程下载任务管理器
    """

    taskInited = pyqtSignal(bool)  # 任务初始化完成
    workerInfoChanged = pyqtSignal(list)  # 下载进度信息
    speedChanged = pyqtSignal(int)  # 下载速度
    taskFinished = pyqtSignal()  # 下载完成
    gotWrong = pyqtSignal(str)  # 下载错误

    def __init__(
        self,
        url,
        headers=None,
        file_path: str = None,
        file_name: str = None,
        file_size: int = -1,
        extra_data: Optional[tuple] = None,
        parent=None,
    ):
        super().__init__(parent)

        self.url = url
        self.headers = headers or MCSLNetworkSession.MCSLNetworkHeaders
        self.file_name = file_name
        self.file_path = (
            Path(file_path).expanduser() if file_path else Path("MCSL2/Downloads").expanduser()
        )
        self.full_path = None
        self.thread_count = cfg.get(cfg.downloadThreads)
        self.file_size = file_size
        self.extra_data = extra_data

        self.is_cancelled = False
        self.is_finished = False

        # pypdl 下载器实例
        self.downloader = None

        # 进度监控
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._update_progress)

        self.last_progress = 0
        self.current_speed = 0

        # 确保下载路径
        self._ensure_download_path()

        # 发射初始化完成信号
        QTimer.singleShot(0, lambda: self.taskInited.emit(True))

    def _ensure_download_path(self):
        """确保文件名和保存路径已就绪"""
        import sys

        if not self.file_name:
            parsed = urlsplit(self.url or "")
            candidate = unquote(Path(parsed.path).name)
            if not candidate:
                candidate = "download.bin"
            self.file_name = candidate
        else:
            self.file_name = unquote(self.file_name)

        if sys.platform == "win32":
            self.file_name = "".join([i for i in self.file_name if i not in r'\\/:*?"<>|'])
        if len(self.file_name) > 255:
            self.file_name = self.file_name[:255]

        base_path = Path(self.file_path or Path("MCSL2/Downloads")).expanduser()
        if not base_path.exists():
            base_path.mkdir(parents=True, exist_ok=True)
        self.file_path = base_path.resolve()
        self.full_path = (self.file_path / self.file_name).resolve()
        return self.full_path

    def start_download(self):
        """开始下载 - 使用 pypdl"""
        if self.is_cancelled:
            return

        try:
            MCSL2Logger.info(f"开始下载任务: {self.url}")

            # 创建 pypdl 下载器
            self.downloader = Pypdl()

            # 设置参数
            self.downloader.headers = self.headers
            self.downloader.segments = max(1, self.thread_count)

            # 启动进度监控
            self.progress_timer.start(1000)

            # 开始下载（异步）
            def _download_thread():
                try:
                    self.downloader.start(
                        url=self.url,
                        file_path=str(self.full_path),
                        display=False,  # 不显示内置进度条
                        multisegment=True,
                        block=True,  # 阻塞直到完成
                    )
                    # 下载完成
                    QTimer.singleShot(0, self._on_download_finished)
                except Exception as e:
                    MCSL2Logger.error(f"下载失败: {e}")
                    QTimer.singleShot(0, lambda error=e: self.gotWrong.emit(str(error)))

            thread = threading.Thread(target=_download_thread, daemon=True)
            thread.start()

        except Exception as e:
            MCSL2Logger.error(f"启动下载失败: {e}")
            self.gotWrong.emit(str(e))

    def pause(self):
        """暂停下载"""
        if self.downloader:
            self.downloader.stop()

    def resume(self):
        """恢复下载 - pypdl 支持断点续传，重新start即可"""
        if self.downloader:
            self.start_download()

    def cancel(self):
        """取消下载"""
        if self.is_cancelled:
            return
        self.is_cancelled = True
        self.progress_timer.stop()
        if self.downloader:
            self.downloader.stop()
        self._cleanup_files()

    def _update_progress(self):
        """更新下载进度 - 从 pypdl 获取"""
        if self.is_cancelled or not self.downloader:
            self.progress_timer.stop()
            return

        try:
            # 获取当前进度
            current = self.downloader.progress
            total = self.downloader.size
            speed = self.downloader.speed

            # pypdl 提供的剩余时间（秒）
            time_left = self.downloader.time_left if hasattr(self.downloader, "time_left") else 0

            if total > 0:
                # pypdl 的 speed 单位是 MB/s，需要转换为 B/s
                speed_bytes = int(speed * 1024 * 1024) if speed else 0
                
                # 计算速度
                progress_delta = current - self.last_progress
                self.last_progress = current
                self.current_speed = speed_bytes if speed_bytes > 0 else progress_delta

                # 发射速度信号
                self.speedChanged.emit(self.current_speed)

                # 计算剩余时间（如果 pypdl 没有提供，手动计算）
                if time_left <= 0 and self.current_speed > 0:
                    time_left = (total - current) / self.current_speed

                # 发送进度信息
                worker_info = [
                    {
                        "downloaded": current,
                        "total": total,
                        "speed": self.current_speed,
                        "eta": time_left,
                        "eta_formatted": formatETA(time_left),
                    }
                ]
                self.workerInfoChanged.emit(worker_info)

        except Exception as e:
            MCSL2Logger.debug(f"更新进度失败: {e}")

    def _on_download_finished(self):
        """下载完成后的清理和信号触发"""
        if self.is_cancelled or self.is_finished:
            return

        self.is_finished = True
        self.progress_timer.stop()

        MCSL2Logger.success(f"下载完成: {self.full_path}")
        self.speedChanged.emit(0)
        self.taskFinished.emit()

    def _cleanup_files(self):
        """清理下载文件"""
        try:
            # 删除下载文件（如果存在且未完成）
            if hasattr(self, "full_path") and self.full_path and self.full_path.exists():
                self.full_path.unlink()
                MCSL2Logger.info(f"已删除未完成的下载文件: {self.full_path}")

        except Exception as e:
            MCSL2Logger.error(f"清理文件时发生错误: {e}")


class DownloadController:
    """
    多线程下载控制器
    """

    _download_tasks = {}

    @classmethod
    def download(
        cls,
        uri,
        info_get: Optional[Callable[[dict], None]] = None,
        stopped: Optional[Callable[[list], None]] = None,
        extraData: Optional[tuple] = None,
        watch=True,
        filename: Optional[str] = None,
        interval=0.1,
        file_size: Optional[int] = None,
    ) -> str:
        """
        下载文件

        :param uri: 下载链接
        :param info_get: 进度回调函数
        :param stopped: 完成回调函数
        :param extraData: 额外数据
        :param watch: 是否监视进度
        :param filename: 文件名
        :param interval: 监视间隔
        :param file_size: 已知文件大小（字节），可选
        :return: 任务ID
        """
        # 生成任务ID
        gid = hashlib.md5(f"{uri}{time.time()}".encode()).hexdigest()

        # 创建下载任务
        normalized_size = -1
        if file_size is not None:
            try:
                normalized_size = int(file_size)
            except (ValueError, TypeError):
                normalized_size = -1

        download_task = DownloadTask(
            url=uri,
            file_name=filename,
            file_size=normalized_size,
            extra_data=extraData,
        )

        # 设置回调
        if watch and info_get:
            download_task.workerInfoChanged.connect(
                lambda worker_info: cls._emit_download_info(gid, worker_info, info_get)
            )
            download_task.speedChanged.connect(
                lambda speed: cls._emit_speed_info(gid, speed, info_get)
            )

        if stopped:
            download_task.taskFinished.connect(lambda: stopped([None, extraData]))

        # 保存任务引用
        cls._download_tasks[gid] = download_task

        # 开始下载
        download_task.start_download()

        return gid

    @classmethod
    def _emit_download_info(cls, gid, worker_info, callback):
        """发射下载信息 (转换为 aria2 格式)"""
        try:
            if not worker_info:
                return

            info = worker_info[0]
            downloaded = info.get("downloaded", 0)
            total = info.get("total", 0)
            speed = info.get("speed", 0)
            eta = info.get("eta", 0)

            # 计算进度百分比和进度条值
            progress_percent = int((downloaded / total * 100)) if total > 0 else 0
            
            # 构造 aria2 格式的信息，并添加额外的显示字段
            aria2_format = {
                "gid": gid,
                "status": "active",
                "totalLength": getReadableSize(total),
                "completedLength": str(downloaded),
                "downloadSpeed": str(speed),
                "connections": "1",
                "files": [
                    {
                        "index": "1",
                        "length": str(total),
                        "completedLength": str(downloaded),
                    }
                ],
                # 添加 UI 需要的字段
                "speed": getReadableSpeed(speed),
                "eta": formatETA(eta),
                "progress": f"{progress_percent}%",
                "bar": progress_percent,
            }

            callback(aria2_format)

        except Exception as e:
            MCSL2Logger.error("发射下载信息失败", exc=e)

    @classmethod
    def _emit_speed_info(cls, gid, speed, callback):
        """发射速度信息"""
        try:
            task = cls._download_tasks.get(gid)
            if not task:
                return

            total = task.downloader.size if task.downloader else 0
            downloaded = task.downloader.progress if task.downloader else 0

            # 计算进度百分比
            progress_percent = int((downloaded / total * 100)) if total > 0 else 0
            
            # 计算剩余时间
            eta_seconds = (total - downloaded) / speed if speed > 0 and total > downloaded else 0

            aria2_format = {
                "gid": gid,
                "status": "active",
                "totalLength": getReadableSize(total),
                "completedLength": str(downloaded),
                "downloadSpeed": str(speed),
                "connections": "1",
                # 添加 UI 需要的字段
                "speed": getReadableSpeed(speed),
                "eta": formatETA(eta_seconds),
                "progress": f"{progress_percent}%",
                "bar": progress_percent,
            }

            callback(aria2_format)

        except Exception as e:
            MCSL2Logger.debug(f"发射速度信息失败: {e}")

    @classmethod
    def pauseDownloadTask(cls, gid: str):
        """暂停下载任务"""
        if gid in cls._download_tasks:
            cls._download_tasks[gid].pause()

    @classmethod
    def resumeDownloadTask(cls, gid: str):
        """恢复下载任务"""
        if gid in cls._download_tasks:
            cls._download_tasks[gid].resume()

    @classmethod
    def cancelDownloadTask(cls, gid: str):
        """取消下载任务"""
        if gid in cls._download_tasks:
            cls._download_tasks[gid].cancel()
            del cls._download_tasks[gid]


class DL_EntryManager(QObject):
    """
    下载记录管理器,用于管理下载记录:获取下载记录,检查记录完整性,删除不完整的记录,添加记录等
    # >>> 注意：请用DL_EntryController来调用此类中的方法!!(异步)<<<
    """

    onGetEntries = pyqtSignal(list)
    onReadEntries = pyqtSignal(dict)
    file = "./MCSL2/Downloads/download_entries.json"
    path = "./MCSL2/Downloads"

    def __init__(self, _entries, mutex: QMutex):
        super().__init__()
        self.entries = _entries
        self.mutex = mutex

    def fileExisted(self):
        """
        在对文件进行操作前检查文件是否存在，如果不存在则创建文件,确保文件操作不会出错
        """
        if not osp.exists(osp.join("MCSL2", "Downloads")):
            mkdir(osp.join("MCSL2", "Downloads"))
        if not osp.exists(DL_EntryManager.file):
            MCSL2Logger.info(f"创建下载记录文件: {DL_EntryManager.file}")
            writeFile(DL_EntryManager.file, "{}")

    def read(self, check=True, autoDelete=True):
        self.fileExisted()
        self.entries = json.loads(readFile(DL_EntryManager.file))
        for coreName, coreData in self.entries.copy().items():
            if check and not self.checkCoreEntry(coreName, coreData["md5"], autoDelete):
                self.entries.pop(coreName)
        self.flush()
        MCSL2Logger.info(f"读取下载记录: {len(self.entries)}条")
        self.onReadEntries.emit(self.entries)
        return self.entries

    def addEntry(self, entryName: str, entryData: dict):
        """
        向文件中添加一条记录
        """
        json.dumps({entryName: entryData}, indent=4, ensure_ascii=False, sort_keys=True)
        MCSL2Logger.success(f"新增记录: {entryName}: {entryData}")
        self.mutex.lock()
        self.entries.update({entryName: entryData})
        self.mutex.unlock()
        self.flush()

    def addCoreEntry(self, coreName: str, extraData: dict):
        """
        添加核心文件的记录
        """
        coreFileName = osp.join(self.path, coreName)
        # 计算md5
        md5 = hashlib.md5(readBytesFile(coreFileName)).hexdigest()
        extraData.update({"md5": md5})
        self.addEntry(coreName, extraData)

    def popCoreEntry(self, coreName: str, autoDelete=True) -> Dict:
        """
        删除核心文件的记录并返回删除的记录的原条目，如果autoDelete为True则同时删除核心文件
        """
        if coreName in self.entries.keys():
            self.mutex.lock()
            rv = self.entries.pop(coreName)
            self.mutex.unlock()
            if autoDelete:
                try:
                    remove(osp.join(self.path, coreName))
                except FileNotFoundError:
                    pass
            self.flush()
            return {coreName: rv}
        else:
            return {}

    def flush(self):
        """
        将文件中的数据写入文件
        """
        self.fileExisted()
        self.mutex.lock()
        writeFile(
            self.file,
            json.dumps(self.entries, indent=4, ensure_ascii=False, sort_keys=True),
        )
        self.mutex.unlock()

    def checkCoreEntry(self, coreName: str, originMd5: str, autoDelete=False):
        """
        检查核心文件的完整性
        :param coreName: 核心文件名
        :param originMd5: 原始md5
        :param autoDelete: 如果文件不完整是否自动删除核心文件
        """
        coreFileName = osp.join(self.path, coreName)
        if osp.exists(coreFileName):
            # 计算md5
            fileMd5 = hashlib.md5(readBytesFile(coreFileName)).hexdigest()
            if fileMd5 == originMd5:
                return True
            if autoDelete:
                self.popCoreEntry(coreName, True)
        else:
            if autoDelete:
                self.popCoreEntry(coreName, False)
        return False

    def check(self, autoDelete=False):
        """
        检查所有核心文件的完整性
        :param autoDelete: 如果文件不完整是否自动删除核心文件
        """
        self.mutex.lock()
        entries_snapshot = self.entries.copy()
        self.mutex.unlock()
        for coreName, coreData in entries_snapshot.items():
            if not self.checkCoreEntry(coreName, coreData["md5"], autoDelete):
                self.popCoreEntry(coreName, autoDelete)
        self.flush()
        return True

    def cleanUnavailable(self):
        """
        清理所有无效记录（包括本地文件）
        """
        self.check(True)

    def tryGetEntry(self, entryName: str, check=True, autoDelete=True):
        """
        尝试获取一条记录，如果记录不完整则返回None
        """
        if not check:
            return self.entries.get(entryName, None)
        # 检查记录完整性
        if self.checkCoreEntry(entryName, self.entries[entryName]["md5"], autoDelete):
            return self.entries[entryName]
        else:
            return None

    def GetEntries(self, check=True, autoDelete=True):
        """
        获取所有正确的记录
        """
        self.mutex.lock()
        entries_snapshot = self.entries.copy()
        self.mutex.unlock()
        rv = entries_snapshot.copy()

        for entryName in entries_snapshot.keys():
            if self.tryGetEntry(entryName, check, autoDelete) is None:
                rv.pop(entryName)
        self.flush()
        return rv

    def getEntriesList(self, check=True, autoDelete=True):
        """
        获取所有正确的记录的列表
        "name", "type", "mc_version", "build_version", ...
        """
        rv = []
        for entryName, entryData in self.GetEntries(check, autoDelete).items():
            e = entryData.copy()
            e.update({"name": entryName})
            rv.append(e)
        self.onGetEntries.emit(rv)
        return rv

    def asyncDispatcher(self, info):
        method, kwargs = info
        getattr(self, method)(**kwargs)


WorkingThreads.register("DL_Entry")


class DL_EntryController(QObject):
    """
    用于在线程中执行DL_EntryManager中的函数:
    1.controller = DL_EntryController()
    2.controller.resultReady.connect(...)
    3.controller.work.emit((<method:str>,<kwargs>:dict))
    """

    work = pyqtSignal(object)
    resultReady = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        global entries, entries_mutex
        self.mutex = entries_mutex
        self.entries = entries
        self.worker = DL_EntryManager(self.entries, self.mutex)
        self.worker.read()
        self.worker.moveToThread(WorkingThreads.getThread("DL_Entry"))

        self.resultReady.connect(lambda _: self.worker.deleteLater())
        self.work.connect(self.worker.asyncDispatcher)
        self.worker.onGetEntries.connect(lambda entries_: self.resultReady.emit(entries_))
        self.worker.onReadEntries.connect(lambda d: self.resultReady.emit(d))


def set_entries(_):
    global entries
    entries = _


# entries = DL_EntryManager(entries, entries_mutex).read()
(controller := DL_EntryController()).resultReady.connect(lambda d: set_entries(d))
controller.work.emit(("read", {}))

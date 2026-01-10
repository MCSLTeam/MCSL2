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
"""

import hashlib
import math
from os import path as osp, mkdir, remove
import json
import time
from typing import Optional, Callable, Dict
import sys
import struct
from pathlib import Path
from urllib.parse import unquote, urlsplit
from PyQt5.QtCore import (
    QObject,
    pyqtSignal,
    QTimer,
    QMutex,
    QUrl,
    QEventLoop,
)
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from pyqt5_concurrent.TaskExecutor import TaskExecutor

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

MIN_PARALLEL_CHUNK_SIZE = 1024 * 1024  # 1 MiB


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


def getLinkInfo(url, headers, fileName=None):
    """获取链接信息"""
    try:
        # 用QNetworkAccessManager同步HEAD请求
        manager = QNetworkAccessManager()
        req = QNetworkRequest(QUrl(url))
        for k, v in headers.items():
            req.setRawHeader(k.encode(), str(v).encode())
        req.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
        loop = QEventLoop()
        reply = manager.head(req)
        reply.finished.connect(loop.quit)
        loop.exec_()
        if reply.error() != QNetworkReply.NoError:
            raise Exception(reply.errorString())
        # 获取文件大小
        file_size = int(reply.rawHeader(b"Content-Length") or 0)
        # 获取文件名
        if not fileName:
            cd = bytes(reply.rawHeader(b"Content-Disposition")).decode(errors="ignore")
            if "filename=" in cd:
                fileName = cd.split("filename=")[1].strip('"')
            if not fileName:
                fileName = url.split("/")[-1]
                if "?" in fileName:
                    fileName = fileName.split("?")[0]
        # 检查最终URL（处理重定向）
        final_url = str(reply.url().toString())
        reply.deleteLater()
        return final_url, fileName, file_size
    except Exception as e:
        MCSL2Logger.error(msg=f"获取链接信息失败: {e}")
        return url, fileName or "unknown_file", 0


def createSparseFile(file_path, size=None):
    """创建稀疏文件"""
    try:
        if sys.platform == "win32":
            # Windows 系统的稀疏文件支持
            import ctypes

            GENERIC_WRITE = 0x40000000
            OPEN_ALWAYS = 4
            FILE_ATTRIBUTE_NORMAL = 0x80

            kernel32 = ctypes.windll.kernel32
            handle = kernel32.CreateFileW(
                str(file_path), GENERIC_WRITE, 0, None, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, None
            )

            if handle != -1:
                kernel32.CloseHandle(handle)
        else:
            # Unix 系统
            if size and size > 0:
                with open(file_path, "wb") as f:
                    f.seek(size - 1)
                    f.write(b"\0")
    except Exception as e:
        MCSL2Logger.warning(f"创建稀疏文件失败: {e}")


class DownloadWorker:
    """下载工作单元"""

    def __init__(self, start, end, downloaded=0):
        self.start = start
        self.end = end
        self.downloaded = downloaded
        self.progress = start + downloaded

    @property
    def remaining(self):
        return self.end - self.progress + 1

    def __repr__(self):
        return f"DownloadWorker({self.start}, {self.progress}, {self.end})"


class DownloadTask(QObject):
    """
    多线程下载任务管理器
    使用 pyqt5-concurrent 实现
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
        parent=None,
    ):
        super().__init__(parent)

        self.url = url
        self.headers = headers or MCSLNetworkSession.MCSLNetworkHeaders
        self.file_name = file_name
        self.file_path = (
            Path(file_path).expanduser()
            if file_path
            else Path("MCSL2/Downloads").expanduser()
        )
        self.full_path = None
        self.thread_count = cfg.get(cfg.downloadThreads)
        self.file_size = file_size
        self.workers = []
        self.supports_parallel = False

        self.total_downloaded = 0
        self.last_downloaded = 0
        self.speed_history = [0] * 10
        self.is_paused = False
        self.is_cancelled = False
        self.is_finished = False
        self.should_start_after_init = False  # 是否在初始化后开始下载

        # ETA 计算相关
        self.start_time = None
        self.eta_seconds = 0

        # 多线程任务管理
        self.pending_tasks = 0
        self.completed_tasks = 0

        # 进度监控定时器
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._update_progress)

        # 文件写入互斥锁
        self.file_write_mutex = QMutex()

        # 初始化任务
        self._init_future = TaskExecutor.run(self._init_task)
        self._init_future.finished.connect(self._on_init_finished)

    def _ensure_download_path(self):
        """确保文件名和保存路径已就绪"""
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

    def _init_task(self):
        """初始化下载任务"""
        try:
            # 获取文件信息（保持调用方指定的文件名，补全其他信息）
            final_url, inferred_name, inferred_size = getLinkInfo(
                self.url, self.headers, self.file_name
            )
            self.url = final_url
            if not self.file_name and inferred_name:
                self.file_name = inferred_name
            if inferred_size and (self.file_size is None or self.file_size <= 0):
                self.file_size = inferred_size

            # 确保路径信息
            self._ensure_download_path()
            MCSL2Logger.info(
                f"初始化下载文件: 路径={self.full_path}, 预期大小={self.file_size}"
            )

            progress_file = self.file_path / f"{self.file_name}.progress"

            # 默认视为不支持并行，在满足条件后再开启
            self.supports_parallel = False
            self.thread_count = max(1, self.thread_count)

            if self.file_size is None or self.file_size <= 0:
                self.file_size = 0

            if self.file_size > 0 and self.thread_count > 1:
                support_range = self._check_range_support()
            else:
                support_range = False

            if support_range and self.file_size > MIN_PARALLEL_CHUNK_SIZE:
                max_workers = max(1, self.file_size // MIN_PARALLEL_CHUNK_SIZE)
                self.thread_count = max(1, min(self.thread_count, max_workers))
                self.supports_parallel = self.thread_count > 1

            if self.supports_parallel:
                if not self.full_path.exists():
                    self.full_path.touch()
                    createSparseFile(self.full_path, self.file_size)
                else:
                    try:
                        existing_size = self.full_path.stat().st_size
                    except OSError:
                        existing_size = 0
                    if existing_size < self.file_size:
                        createSparseFile(self.full_path, self.file_size)
                self._load_workers()
                return True

            # 不支持并行时，使用单线程
            self.thread_count = 1
            self.workers.clear()
            if progress_file.exists():
                try:
                    progress_file.unlink()
                except Exception:
                    pass
            if not self.full_path.exists():
                self.full_path.touch()
            return False

        except Exception as e:
            MCSL2Logger.error(f"初始化下载任务失败: {e}")
            raise e

    def _check_range_support(self):
        """检查服务器是否支持分块下载（QNetwork实现）"""
        if "fastmirror.net" in self.url:
            return True
        try:
            manager = QNetworkAccessManager()
            req = QNetworkRequest(QUrl(self.url))
            for k, v in self.headers.items():
                req.setRawHeader(k.encode(), str(v).encode())
            req.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
            loop = QEventLoop()
            reply = manager.head(req)
            reply.finished.connect(loop.quit)
            loop.exec_()
            if reply.error() != QNetworkReply.NoError:
                return False
            accept_ranges = bytes(reply.rawHeader(b"Accept-Ranges")).decode(errors="ignore").lower()
            if accept_ranges == "none":
                MCSL2Logger.info("服务器明确表示不支持Range请求")
                reply.deleteLater()
                return False
            # 进一步用GET+Range头测试
            req2 = QNetworkRequest(QUrl(self.url))
            for k, v in self.headers.items():
                req2.setRawHeader(k.encode(), str(v).encode())
            req2.setRawHeader(b"Range", b"bytes=0-1023")
            req2.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
            reply2 = manager.get(req2)
            loop2 = QEventLoop()
            reply2.finished.connect(loop2.quit)
            loop2.exec_()
            code = reply2.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            reply.deleteLater()
            reply2.deleteLater()
            if code == 206:
                return True
            elif code == 200:
                return False
            else:
                MCSL2Logger.info(f"Range请求返回状态码: {code}")
                return False
        except Exception as e:
            MCSL2Logger.error(f"检查Range支持时发生错误: {e}")
            return False

    def _load_workers(self):
        """加载或创建工作单元"""
        if not self.supports_parallel or self.file_size <= 0:
            self.workers.clear()
            return

        progress_file = self.file_path / f"{self.file_name}.progress"

        if progress_file.exists():
            # 从进度文件加载
            try:
                with open(progress_file, "rb") as f:
                    while True:
                        data = f.read(24)  # 3个uint64
                        if not data:
                            break
                        start, progress, end = struct.unpack("<QQQ", data)
                        if end < start:
                            continue
                        progress = max(start, min(progress, end + 1))
                        self.workers.append(DownloadWorker(start, end, progress - start))
            except Exception as e:
                MCSL2Logger.error(f"加载进度失败: {e}")
                self._create_workers()
        else:
            self._create_workers()

    def _create_workers(self):
        """创建工作单元"""
        self.workers.clear()
        if self.file_size <= 0 or self.thread_count <= 0:
            return

        chunk_size = math.ceil(self.file_size / self.thread_count)
        start = 0

        while start < self.file_size:
            end = min(start + chunk_size - 1, self.file_size - 1)
            self.workers.append(DownloadWorker(start, end))
            start = end + 1

    def _save_progress(self):
        """保存下载进度"""
        try:
            progress_file = self.file_path / f"{self.file_name}.progress"
            with open(progress_file, "wb") as f:
                for worker in self.workers:
                    data = struct.pack("<QQQ", worker.start, worker.progress, worker.end)
                    f.write(data)
        except Exception as e:
            MCSL2Logger.error(f"保存进度失败: {e}")

    def _on_init_finished(self):
        """初始化完成"""
        try:
            MCSL2Logger.info(
                "初始化完成，{}并行下载".format("支持" if self.supports_parallel else "不支持")
            )
            # 发射信号表示是否支持并行下载
            self.taskInited.emit(self.supports_parallel)

            # 如果需要在初始化后开始下载
            if self.should_start_after_init and not self.is_cancelled:
                MCSL2Logger.info("初始化完成后自动开始下载")
                self._start_download_internal()
        except Exception as e:
            MCSL2Logger.error(e, f"初始化处理失败: {e}")
            self.gotWrong.emit(str(e))

    def start_download(self):
        """开始下载 - 公共接口"""
        if self.is_cancelled:
            return

        MCSL2Logger.info(f"开始下载任务: {self.url}")

        # 标记为需要在初始化后开始
        self.should_start_after_init = True

        # 检查初始化是否可能已经完成（通过检查workers是否已初始化）
        if hasattr(self, "workers") and len(self.workers) > 0:
            MCSL2Logger.info("检测到初始化可能已完成，直接开始下载")
            self._start_download_internal()

    def _start_download_internal(self):
        """内部下载实现"""
        if self.is_cancelled:
            return

        self._ensure_download_path()
        worker_count = len(self.workers) if hasattr(self, "workers") else 0
        MCSL2Logger.info(
            "开始内部下载，线程数: %s，工作单元数: %s，目标文件=%s"
            % (self.thread_count, worker_count, self.full_path)
        )

        # 记录开始时间用于ETA计算
        self.start_time = time.time()

        # 启动进度监控
        self.progress_timer.start(1000)  # 每秒更新一次

        if self.thread_count <= 1:
            # 单线程下载
            MCSL2Logger.info("使用单线程下载")
            future = TaskExecutor.run(self._download_single)
            future.finished.connect(self._on_download_finished)
        else:
            # 多线程下载
            MCSL2Logger.info("使用多线程下载")
            download_tasks = []
            for i, worker in enumerate(self.workers):
                if worker.remaining > 0:
                    task = TaskExecutor.createTask(self._download_worker, worker, i)
                    download_tasks.append(task)

            MCSL2Logger.info(f"创建了 {len(download_tasks)} 个下载任务")

            if download_tasks:
                # 记录待完成的任务数量
                self.pending_tasks = len(download_tasks)
                self.completed_tasks = 0

                # 为每个任务单独连接完成信号
                for task in download_tasks:
                    task.finished.connect(self._on_worker_finished)

                # 启动所有下载任务
                for task in download_tasks:
                    task.runTask()
            else:
                # 已经下载完成（所有工作单元都已完成）
                self.taskFinished.emit()

    def _download_single(self):
        """QNetwork单线程下载实现"""
        manager = QNetworkAccessManager()
        request = QNetworkRequest(QUrl(self.url))
        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
        for k, v in self.headers.items():
            request.setRawHeader(k.encode(), str(v).encode())

        reply = manager.get(request)
        loop = QEventLoop()
        error_message = None

        try:
            self._ensure_download_path()
            MCSL2Logger.info(f"单线程下载打开文件: {self.full_path}")
            with open(self.full_path, "wb") as f:
                def on_ready_read():
                    if self.is_cancelled:
                        reply.abort()
                        return
                    data = reply.readAll()
                    if not data.isEmpty():
                        chunk = bytes(data)
                        f.write(chunk)
                        self.total_downloaded += len(chunk)
                        MCSL2Logger.info(
                            f"写入 {len(chunk)} 字节 -> 总计 {self.total_downloaded}"
                        )

                def on_finished():
                    loop.quit()

                def on_error(_):
                    nonlocal error_message
                    error_message = reply.errorString()

                reply.readyRead.connect(on_ready_read)
                reply.finished.connect(on_finished)
                reply.error.connect(on_error)

                loop.exec_()
        finally:
            reply.deleteLater()
            manager.deleteLater()

        if self.is_cancelled:
            return False
        if error_message:
            raise Exception(error_message)
        return True

    def _download_worker(self, worker, worker_index):
        """QNetwork多线程分块下载实现"""
        if self.is_cancelled or worker.remaining <= 0:
            return False

        manager = QNetworkAccessManager()
        request = QNetworkRequest(QUrl(self.url))
        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
        request.setRawHeader(b"Range", f"bytes={worker.progress}-{worker.end}".encode())
        for k, v in self.headers.items():
            request.setRawHeader(k.encode(), str(v).encode())

        reply = manager.get(request)
        loop = QEventLoop()
        error_message = None
        bytes_written = worker.progress

        try:
            with open(self.full_path, "r+b") as f:
                def on_ready_read():
                    nonlocal bytes_written
                    if self.is_cancelled:
                        reply.abort()
                        return
                    data = reply.readAll()
                    if data.isEmpty():
                        return
                    chunk = bytes(data)
                    self.file_write_mutex.lock()
                    try:
                        f.seek(bytes_written)
                        f.write(chunk)
                    finally:
                        self.file_write_mutex.unlock()
                    bytes_written += len(chunk)
                    delta = len(chunk)
                    worker.downloaded = min(
                        worker.downloaded + delta,
                        worker.end - worker.start + 1,
                    )
                    worker.progress = worker.start + worker.downloaded

                def on_finished():
                    loop.quit()

                def on_error(_):
                    nonlocal error_message
                    error_message = reply.errorString()

                reply.readyRead.connect(on_ready_read)
                reply.finished.connect(on_finished)
                reply.error.connect(on_error)

                loop.exec_()
        finally:
            reply.deleteLater()
            manager.deleteLater()

        if self.is_cancelled:
            return False
        if error_message:
            raise Exception(error_message)
        return True

    def pause(self):
        """暂停下载"""
        self.is_paused = True

    def resume(self):
        """恢复下载"""
        self.is_paused = False

    def cancel(self):
        """取消下载"""
        if self.is_cancelled:
            return
        self.is_cancelled = True
        self.progress_timer.stop()
        self._cleanup_files()

    def _update_progress(self):
        """更新下载进度"""
        if self.is_cancelled:
            self.progress_timer.stop()
            return

        # 计算总下载量
        if self.supports_parallel:
            current_downloaded = sum(worker.downloaded for worker in self.workers)
        else:
            current_downloaded = self.total_downloaded

        # 计算速度
        speed = current_downloaded - self.last_downloaded
        self.last_downloaded = current_downloaded
        self.speed_history.pop(0)
        self.speed_history.append(speed)
        avg_speed = sum(self.speed_history) // 10

        # 计算ETA
        self._calculate_eta(current_downloaded, avg_speed)

        self.speedChanged.emit(avg_speed)

        # 发送工作单元信息
        if self.supports_parallel:
            worker_info = []
            for worker in self.workers:
                worker_info.append({
                    "start": worker.start,
                    "progress": worker.progress,
                    "end": worker.end,
                })
            self.workerInfoChanged.emit(worker_info)

        # 保存进度
        if self.supports_parallel:
            self._save_progress()

    def _calculate_eta(self, current_downloaded, avg_speed):
        """计算ETA（剩余时间估计）"""
        if not self.start_time or self.file_size <= 0:
            self.eta_seconds = 0
            return

        # 计算剩余字节数
        remaining_bytes = self.file_size - current_downloaded

        if remaining_bytes <= 0:
            self.eta_seconds = 0
            return

        # 如果平均速度太低，使用基于时间的速度计算
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0 and avg_speed <= 0:
            overall_speed = current_downloaded / elapsed_time
            if overall_speed > 0:
                self.eta_seconds = remaining_bytes / overall_speed
            else:
                self.eta_seconds = 0
        elif avg_speed > 0:
            # 使用平均速度计算ETA
            self.eta_seconds = remaining_bytes / avg_speed
        else:
            self.eta_seconds = 0

    def _on_download_finished(self):
        """下载完成后的清理和信号触发"""
        if self.is_cancelled or self.is_finished:
            return

        self.is_finished = True
        self.progress_timer.stop()
        self.pending_tasks = 0
        self.completed_tasks = 0
        self.should_start_after_init = False
        self.eta_seconds = 0
        self.total_downloaded = (
            self.file_size if self.file_size and self.file_size > 0 else self.total_downloaded
        )

        target_path = getattr(self, "full_path", None)
        MCSL2Logger.info(f"下载完成回调，target_path={target_path}")

        if self.supports_parallel:
            try:
                if getattr(self, "file_path", None) and getattr(self, "file_name", None):
                    progress_file = Path(self.file_path) / f"{self.file_name}.progress"
                    if progress_file.exists():
                        progress_file.unlink()
            except Exception as e:
                MCSL2Logger.error(f"清理进度文件失败: {e}")

        self.speedChanged.emit(0)
        path_str = str(target_path) if target_path else "<unknown>"
        MCSL2Logger.success(f"下载完成: {path_str}")
        self.taskFinished.emit()

    def _on_worker_finished(self):
        """单个工作单元完成"""
        self.completed_tasks += 1

        # 检查是否所有任务都完成了
        if self.completed_tasks >= self.pending_tasks:
            self._on_download_finished()

    def _cleanup_files(self):
        """清理下载和进度文件"""
        try:
            # 删除下载文件（如果存在且未完成）
            if hasattr(self, "full_path") and self.full_path and self.full_path.exists():
                self.full_path.unlink()
                MCSL2Logger.info(f"已删除下载文件: {self.full_path}")

            # 删除进度文件（如果存在）
            if (
                hasattr(self, "file_path")
                and hasattr(self, "file_name")
                and self.file_path
                and self.file_name
            ):
                progress_file = self.file_path / f"{self.file_name}.progress"
                if progress_file.exists():
                    progress_file.unlink()
                    MCSL2Logger.info(f"已删除进度文件: {progress_file}")

        except Exception as e:
            MCSL2Logger.error(f"清理文件时发生错误: {e}")


class DownloadController:
    """
    多线程下载控制器
    """

    _download_tasks = {}
    _download_watchers = {}

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
            except Exception:
                normalized_size = -1

        download_task = DownloadTask(
            url=uri,
            file_name=filename,
            file_size=normalized_size,
        )

        # 设置回调
        if watch and info_get:
            download_task.workerInfoChanged.connect(
                lambda info: cls._emit_download_info(gid, info, info_get)
            )
            download_task.speedChanged.connect(
                lambda speed: cls._emit_speed_info(gid, speed, info_get)
            )

        if stopped:
            download_task.taskFinished.connect(lambda: stopped([None, extraData]))
            download_task.gotWrong.connect(lambda error: stopped([error, extraData]))

        # 保存任务引用
        cls._download_tasks[gid] = download_task

        # 开始下载
        download_task.start_download()

        return gid

    @classmethod
    def _emit_download_info(cls, gid, worker_info, callback):
        """发射下载信息 (转换为 aria2 格式)"""
        try:
            if gid not in cls._download_tasks:
                return

            task = cls._download_tasks[gid]

            # 计算总进度 - 使用与speed_info相同的逻辑
            total_size = task.file_size
            total_downloaded = 0
            connections = 0

            if getattr(task, "supports_parallel", False):
                connections = task.thread_count
                # 直接从worker对象计算，确保与speed_info一致
                for worker in task.workers:
                    total_downloaded += worker.downloaded
            else:
                # 单线程下载
                connections = 1
                total_downloaded = task.total_downloaded

            # 计算进度百分比
            progress_percent = (total_downloaded / total_size * 100) if total_size > 0 else 0

            # 构造 aria2 格式的信息
            aria2_info = {
                "connections": connections,
                "speed": "0B/s",  # 速度会在 _emit_speed_info 中更新
                "progress": f"{progress_percent:.1f}%",
                "status": "active",
                "totalLength": getReadableSize(total_size),
                "completedLength": getReadableSize(total_downloaded),
                "files": [],
                "bar": int(progress_percent),
                "eta": formatETA(task.eta_seconds),
            }

            callback(aria2_info)

        except Exception as e:
            MCSL2Logger.error(e, f"发射下载信息失败: {e}")

    @classmethod
    def _emit_speed_info(cls, gid, speed, callback):
        """发射速度信息"""
        try:
            if gid not in cls._download_tasks:
                return

            task = cls._download_tasks[gid]

            # 计算总进度
            total_size = task.file_size
            total_downloaded = 0

            if getattr(task, "supports_parallel", False):
                for worker in task.workers:
                    total_downloaded += worker.downloaded
            else:
                total_downloaded = task.total_downloaded

            progress_percent = (total_downloaded / total_size * 100) if total_size > 0 else 0

            # 更新信息，包含速度和ETA
            aria2_info = {
                "connections": (
                    task.thread_count if getattr(task, "supports_parallel", False) else 1
                ),
                "speed": f"{getReadableSize(speed)}/s",
                "progress": f"{progress_percent:.1f}%",
                "status": "active",
                "totalLength": getReadableSize(total_size),
                "completedLength": getReadableSize(total_downloaded),
                "files": [],
                "bar": int(progress_percent),
                "eta": formatETA(task.eta_seconds),
            }

            callback(aria2_info)

        except Exception as e:
            MCSL2Logger.error(e, f"发射速度信息失败: {e}")

    @classmethod
    def pauseDownloadTask(cls, gid: str):
        """暂停下载任务"""
        if gid in cls._download_tasks:
            task = cls._download_tasks[gid]
            task.pause()
            MCSL2Logger.info(f"下载任务 {gid} 已暂停")

    @classmethod
    def resumeDownloadTask(cls, gid: str):
        """恢复下载任务"""
        if gid in cls._download_tasks:
            task = cls._download_tasks[gid]
            task.resume()
            MCSL2Logger.info(f"下载任务 {gid} 已恢复")

    @classmethod
    def cancelDownloadTask(cls, gid: str):
        """取消下载任务"""
        if gid in cls._download_tasks:
            task = cls._download_tasks[gid]
            task.cancel()
            del cls._download_tasks[gid]
            MCSL2Logger.info(f"下载任务 {gid} 已取消")


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
                MCSL2Logger.info(f"删除不完整的核心文件记录: {coreName}")
                try:
                    self.entries.pop(coreName)
                except KeyError:
                    pass
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

    # @pyqtSlot(str, dict)
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
                except Exception:
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
                try:  # 删除文件和记录
                    remove(coreFileName)
                    self.mutex.lock()
                    self.entries.pop(coreName)
                    self.mutex.unlock()
                except Exception:
                    pass
        else:
            if autoDelete:
                self.mutex.lock()
                self.entries.pop(coreName)
                self.mutex.unlock()
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
                return False
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

        # # 检查记录一致性
        # f = readFile(self.file)
        # fileRecordedEntries = json.load(f)
        #
        # if fileRecordedEntries != entries_snapshot:  # 如果数据不一致则重新读取,并更新记录.用于加速结果的生成  # noqa: E501
        #     print("记录不一致,重新计算各条目完整性,并更新本地记录")
        #     for entryName in entries_snapshot.keys():
        #         if self.tryGetEntry(entryName, check, autoDelete) is None:
        #             rv.pop(entryName)
        #     self.flush()
        for entryName in entries_snapshot.keys():
            if self.tryGetEntry(entryName, check, autoDelete) is None:
                rv.pop(entryName)
        self.flush()
        # else:
        #     print("记录一致,无需重新计算各条目完整性")
        return rv

    # @pyqtSlot(bool, bool)
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

    # def __new__(cls, *args, **kwargs):
    #     raise Exception("请勿实例化本类,请使用类方法!")


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

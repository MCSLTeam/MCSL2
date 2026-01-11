import asyncio
import traceback
import queue
import threading
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal

from .installer.actions.progress_callback import ProgressCallback
from .installer.simple_installer import SimpleInstaller


class InstallerControllerSignal(QObject):
    finished = pyqtSignal(bool, str)
    output = pyqtSignal(str)


class NeoForgeInstallThread(threading.Thread):
    """NeoForge Installer Thread"""
    def __init__(
        self,
        installer: str,
        targetDir: str,
        java: str,
        detailed: bool = False,
        dlInfoQueue: queue.Queue = None,
    ):
        super().__init__()
        # external signal
        self.signal = InstallerControllerSignal()
        self.finished = self.signal.finished
        self.output = self.signal.output

        self.installer = installer
        self.targetDir = targetDir
        self.java = java
        self.monitor = ProgressCallback.of(lambda self_, msg: self.output.emit(msg))  # type: ProgressCallback
        self.downloadInfoQueue = dlInfoQueue

        self.simpleInstaller = SimpleInstaller(detailed, self.downloadInfoQueue)

    async def installServer(self):
        target = Path(self.targetDir)
        try:
            if not await self.simpleInstaller.installServer(
                target / self.installer, target, self.monitor, Path(self.java)
            ):
                self.finished.emit(False, "安装失败或用户取消")
                return

            if self.monitor.cancelled:
                self.finished.emit(False, "用户取消")
            else:
                self.finished.emit(True, "安装成功")
        except Exception as e:
            traceback.print_exc()
            self.finished.emit(False, str(e))

    def cancel(self):
        self.monitor.setCancelled(True)

    def run(self):
        asyncio.run(self.installServer())

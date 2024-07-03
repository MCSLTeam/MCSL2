import asyncio
import queue
import threading
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal

from .installer.actions.progress_callback import ProgressCallback
from .installer.simple_installer import SimpleInstaller


class InstallerControllerSignal(QObject):
    finished = pyqtSignal(bool)
    output = pyqtSignal(str)


class ForgeInstallThread(threading.Thread):
    def __init__(self, installer: str, targetDir: str, java: str, detailed: bool = False,
                 dlInfoQueue: queue.Queue = None):
        super().__init__()
        # external signal
        self.signal = InstallerControllerSignal()
        self.finished = self.signal.finished
        self.output = self.signal.output

        self.installer = installer
        self.targetDir = targetDir
        self.java = java
        self.monitor = ProgressCallback.of(lambda self_, msg: self.output.emit(msg))
        self.downloadInfoQueue = dlInfoQueue

        self.simpleInstaller = SimpleInstaller(detailed, self.downloadInfoQueue)

    async def installServer(self):
        target = Path(self.targetDir)
        self.finished.emit(
            await self.simpleInstaller.installServer(
                target / self.installer, target, self.monitor, Path(self.java)
            )
        )

    def cancel(self):
        self.monitor.setCancelled(True)

    def run(self):
        asyncio.run(self.installServer())

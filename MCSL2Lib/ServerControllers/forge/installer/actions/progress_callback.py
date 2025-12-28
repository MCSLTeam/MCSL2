import abc
import queue

from ..java2python import FunctionalInterface
from ..utils import ActionCanceledException


@FunctionalInterface
class ProgressCallback(metaclass=abc.ABCMeta):
    lastProgress = 0

    def __init__(self):
        self.hasInfoQueue = False
        self.infoQueue: queue = None
        self.cancelled = False

    def start(self, label: str):
        self.message(label)

    def stage(self, message: str):
        self.message(message)

    @abc.abstractmethod
    def message(self, message: str):
        ...

    def progress(self, progress: float, total: float):
        try:
            percent = int(progress / total * 100 + 0.5)
        except ZeroDivisionError:
            percent = 0

        if percent > self.lastProgress:
            print("·" * (percent - self.lastProgress), end="")
            self.lastProgress = percent
        else:
            if self.lastProgress - percent > 0:
                print()
                print("·" * (self.lastProgress - percent), end="")
                self.lastProgress = percent

    def downloadProgress(
            self, filename: str, progress: float, total: float, speed: float, done: bool
    ):
        self.progress(progress, total)
        if self.infoQueue is None:
            return
        if total:
            self.onDownloadProgress(filename, speed, int(round(progress / total * 100)), done, False)

    def setInfoQueue(self, queue_: queue):
        self.hasInfoQueue = True
        self.infoQueue = queue_

    def onDownloadProgress(self, filename, speed, progress, done, allDone):
        self.infoQueue.put((filename, speed, progress, done, allDone))

    def setCancelled(self, cancelled: bool):
        self.cancelled = cancelled

    def isCancelled(self):
        return self.cancelled

    def allDownloadsDone(self):
        self.onDownloadProgress("", 0, 100, True, True)

    def checkCancelled(self):
        if self.cancelled:
            raise ActionCanceledException()

    def endInfoQueue(self):
        if self.infoQueue is None:
            return
        self.infoQueue.put(None)


TO_STD_OUT = ProgressCallback.of(lambda self, message: print(message))

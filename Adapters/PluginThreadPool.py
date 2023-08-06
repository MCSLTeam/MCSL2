from typing import List

from PyQt5.QtCore import QThread


class _PluginThread(QThread):

    def __init__(self):
        super().__init__()
        self.runFunc = None
        self.stopFunc = None
        self.isStop = False

    def registerStartFunc(self, func):
        self.runFunc = func

    def registerStopFunc(self, func):
        self.stopFunc = func

    def run(self) -> None:
        while True:
            if self.isStop:
                if self.stopFunc is not None:
                    self.stopFunc()
                break
            self.runFunc()


class _PluginThreadPool:
    def __init__(self):
        self.threadPool: List[_PluginThread] = []

    def registerThread(self, runFunc, stopFunc):
        pluginThread: _PluginThread = _PluginThread()
        pluginThread.registerStartFunc(runFunc)
        pluginThread.registerStopFunc(stopFunc)
        self.threadPool.append(pluginThread)
        pluginThread.start()

    def stopThreadAll(self):
        for thread in self.threadPool:
            thread.isStop = True

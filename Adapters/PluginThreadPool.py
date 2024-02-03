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

    def registerThread(self, runFunc, stopCallback):
        pluginThread: _PluginThread = _PluginThread()
        pluginThread.registerStartFunc(runFunc)
        pluginThread.registerStopFunc(stopCallback)
        self.threadPool.append(pluginThread)
        pluginThread.start()

    def stopThreadAll(self):
        for thread in self.threadPool:
            thread.isStop = True

# -*- coding: utf-8 -*-
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
Communicate with Minecraft servers.
"""

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, pyqtSlot
from psutil import NoSuchProcess, Process, AccessDenied
from MCSL2Lib.ServerController.processCreator import _ServerProcessHandler
from MCSL2Lib.variables import ServerVariables

serverVariables = ServerVariables()


class MinecraftServerResMonitorUtil(QObject):
    """
    获取服务器资源占用的线程
    """

    memPercent = pyqtSignal(float)
    cpuPercent = pyqtSignal(float)

    def __init__(self, handler: _ServerProcessHandler, parent=None):
        super().__init__(parent)
        self.handler = handler
        self.setObjectName("MinecraftServerResMonitorThread")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getServerMem)
        self.timer.timeout.connect(self.getServerCPU)
        self.timer.start(1000)
        self.divisionNumList = {"G": 1073741824, "M": 1048576}

    def getServerMem(self):
        divisionNum = self.divisionNumList[serverVariables.memUnit]
        try:
            if self.handler.isServerRunning():
                serverMem = (
                    Process(self.handler.handledServer.process.processId()).memory_full_info().uss
                    / divisionNum
                )
                self.memPercent.emit(float("{:.4f}".format(serverMem)))
            else:
                self.memPercent.emit(0.0000)
        except NoSuchProcess:
            pass
        except PermissionError:
            pass
        except AccessDenied:
            pass

    def getServerCPU(self):
        try:
            if self.handler.isServerRunning():
                serverCPU = Process(
                    self.handler.handledServer.process.processId().processId()
                ).cpu_percent(interval=0.01)
                self.cpuPercent.emit(float("{:.4f}".format(serverCPU / 10)))
            else:
                self.cpuPercent.emit(0.0000)
        except NoSuchProcess:
            pass
        except PermissionError:
            pass
        except AccessDenied:
            pass

    @pyqtSlot(int)
    def onServerClosedHandler(self, _):
        self.cpuPercent.emit(0.0)
        self.memPercent.emit(0.0)
        self.timer.stop()


def readServerProperties():
    serverVariables.serverProperties.clear()
    try:
        with open(
            f"./Servers/{serverVariables.serverName}/server.properties", "r"
        ) as serverPropertiesFile:
            lines = serverPropertiesFile.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    serverVariables.serverProperties[key.strip()] = value.strip()
    except FileNotFoundError:
        serverVariables.serverProperties.update({"msg": "File not found"})

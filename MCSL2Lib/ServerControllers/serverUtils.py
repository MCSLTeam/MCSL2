# -*- coding: utf-8 -*-
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
Communicate with Minecraft servers.
"""

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QFileDialog
from psutil import NoSuchProcess, Process, AccessDenied
from MCSL2Lib.ServerControllers.processCreator import _ServerProcessBridge
from MCSL2Lib.variables import ServerVariables
from os import path as osp, mkdir
from os.path import isdir, exists
from qfluentwidgets import InfoBar, InfoBarPosition
from shutil import make_archive, copytree, rmtree


class MinecraftServerResMonitorUtil(QObject):
    """
    获取服务器资源占用的线程
    """

    memPercent = pyqtSignal(float)
    cpuPercent = pyqtSignal(float)

    def __init__(self, serverConfig, bridge: _ServerProcessBridge, parent=None):
        super().__init__(parent)
        self.bridge = bridge
        self.setObjectName("MinecraftServerResMonitorThread")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getServerMem)
        self.timer.timeout.connect(self.getServerCPU)
        self.timer.start(1000)
        self.divisionNumList = {"G": 1073741824, "M": 1048576}
        self.serverConfig: ServerVariables = serverConfig

    def getServerMem(self):
        divisionNum = self.divisionNumList[self.serverConfig.memUnit]
        try:
            if self.bridge.isServerRunning():
                serverMem = (
                    Process(self.bridge.handledServer.process.processId()).memory_full_info().uss
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
            if self.bridge.isServerRunning():
                serverCPU = Process(self.bridge.handledServer.process.processId()).cpu_percent(
                    interval=0.01
                )
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
    def onServerClosedHandler(self):
        self.cpuPercent.emit(0.0)
        self.memPercent.emit(0.0)
        self.timer.stop()


def readServerProperties(serverConfig: ServerVariables):
    serverConfig.serverProperties.clear()
    try:
        with open(
            f"./Servers/{serverConfig.serverName}/server.properties", "r", encoding="utf-8"
        ) as serverPropertiesFile:
            lines = serverPropertiesFile.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    serverConfig.serverProperties[key.strip()] = value.strip()
    except FileNotFoundError:
        serverConfig.serverProperties.update({"msg": "File not found"})


class MakeArchiveThread(QThread):
    successSignal = pyqtSignal()
    errorSignal = pyqtSignal()

    def __init__(self, a, b, c, parent=None):
        super().__init__(parent)
        self.a = a
        self.b = b
        self.c = c

    def run(self):
        try:
            make_archive(
                self.a,
                self.b,
                self.c,
            )
            self.successSignal.emit()
        except Exception:
            self.errorSignal.emit()


def backupServer(serverName: str, parent):
    try:
        s = QFileDialog.getSaveFileName(
            parent,
            f"MCSL2 - 备份服务器“{serverName}”",
            f"{serverName}_backup.zip",
            "Zip压缩包(*.zip)",
        )[0]
        if s == "":
            return
        tmpArchiveThread = MakeArchiveThread(
            (s).replace(".zip", ""), "zip", osp.abspath(f"Servers/{serverName}"), parent
        )
        tmpArchiveThread.successSignal.connect(
            lambda: InfoBar.success(
                title="备份完毕",
                content=f"已保存至{s}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1500,
                parent=parent,
            )
        )
        tmpArchiveThread.start()
    except Exception:
        InfoBar.success(
            title="备份失败",
            content=str(Exception.args),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=4000,
            parent=parent,
        )


def isBedrockServer(serverName):
    directoryPath = f'./Servers/{serverName}/resource_packs'
    return exists(directoryPath) and isdir(directoryPath)


def backupSaves(serverConfig: ServerVariables, parent):
    try:
        readServerProperties(serverConfig)
        levelName = serverConfig.serverProperties.get("level-name")
        levelNameList = [f"worlds/{levelName}", "worlds/nether", "worlds/end"] if isBedrockServer(serverConfig.serverName) else [levelName, f"{levelName}_nether", f"{levelName}_the_end"]  # noqa: E501
        if osp.exists(f"MCSL2/BackupTemp_{serverConfig.serverName}/"):
            rmtree(f"MCSL2/BackupTemp_{serverConfig.serverName}/")
        s = QFileDialog.getSaveFileName(
            parent,
            f"MCSL2 - 备份服务器“{serverConfig.serverName}”的存档",
            f"{serverConfig.serverName}_{levelName}_backup.zip",
            "Zip压缩包(*.zip)",
        )[0]
        if s == "":
            return
        mkdir(f"MCSL2/BackupTemp_{serverConfig.serverName}/")
        for dir in levelNameList:
            try:
                copytree(
                    osp.abspath(f"Servers/{serverConfig.serverName}/{dir}/"),
                    osp.abspath(f"MCSL2/BackupTemp_{serverConfig.serverName}/{dir}/"),
                )
            except FileNotFoundError:
                levelNameList.remove(dir)
                continue
        existsDir = "\n".join(levelNameList)
        tmpArchiveThread = MakeArchiveThread(
            s.replace(".zip", ""),
            "zip",
            osp.abspath(f"MCSL2/BackupTemp_{serverConfig.serverName}/"),
            parent,
        )
        tmpArchiveThread.successSignal.connect(
            lambda: InfoBar.success(
                title="备份完毕",
                content=f"已保存至{s}。\n备份了以下文件夹：\n{existsDir}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1500,
                parent=parent,
            )
        )
        tmpArchiveThread.successSignal.connect(
            lambda: rmtree(osp.abspath(f"MCSL2/BackupTemp_{serverConfig.serverName}/"))
        )
        tmpArchiveThread.errorSignal.connect(
            lambda: rmtree(osp.abspath(f"MCSL2/BackupTemp_{serverConfig.serverName}/"))
        )
        tmpArchiveThread.start()
    except Exception as e:
        try:
            rmtree(osp.abspath(f"MCSL2/BackupTemp_{serverConfig.serverName}\\"))
        except Exception:
            pass
        raise e

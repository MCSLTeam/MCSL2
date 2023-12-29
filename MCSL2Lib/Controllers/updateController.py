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
Update Controller
"""

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from MCSL2Lib import MCSL2VERSION
from MCSL2Lib.Controllers.aria2ClientController import Aria2Controller
import sys
from os import remove, name as osname, rename, execl
from platform import architecture
from shutil import move
from qfluentwidgets import MessageBox, InfoBar, InfoBarPosition
from MCSL2Lib.Controllers.settingsController import cfg
from MCSL2Lib.variables import GlobalMCSL2Variables
try:
    from MCSL2Lib.verification import checkUpdate
except Exception:
    from MCSL2Lib.noVerification import checkUpdate


class CheckUpdateThread(QThread):
    """
    检查更新的网络连接线程\n
    使用多线程防止假死
    """

    isUpdate = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CheckUpdateThread")

    def run(self):
        try:
            latestVerInfo = checkUpdate()
            self.isUpdate.emit(latestVerInfo)
        except Exception:
            self.isUpdate.emit({"latest": "", "update-log": ""})


class MCSL2FileUpdater(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.updateOSPrefix = "Windows" if osname == "nt" else "Linux"
        self.updateExtSuffix = "." + cfg.get(cfg.oldExecuteable).split(".")[1]
        self.updateArchitecturePrefix: str = ""
        if "32" in architecture()[0]:
            self.updateArchitecturePrefix = f"{self.updateOSPrefix}-x86"
        elif "64" in architecture()[0]:
            self.updateArchitecturePrefix = f"{self.updateOSPrefix}-x64"
        else:
            self.updateArchitecturePrefix = f"{self.updateOSPrefix}-arm64"
        self.updateSite = f"http://update.mcsl.com.cn/Update/{self.updateArchitecturePrefix}/MCSL2{self.updateExtSuffix}"

    def downloadUpdate(self):
        """下载，首先调用"""
        if not GlobalMCSL2Variables.devMode:
            Aria2Controller.download(
                uri=self.updateSite, watch=True, interval=0.2, stopped=self.renameUpdate
            )
            if not Aria2Controller.testAria2Service():
                if not Aria2Controller.startAria2():
                    box = MessageBox(
                        title=self.tr("无法更新"),
                        content=self.tr(
                            "MCSL2的Aria2可能未安装或启动失败。\n已尝试重新启动Aria2。"
                        ),
                        parent=self.parent(),
                    )
                    box.exec()
                    return
            else:
                InfoBar.info(
                    title=self.tr("正在下载更新"),
                    content=self.tr("下载结束后将自动重启。"),
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=-1,
                    parent=self.parent().window(),
                )
        else:
            return

    def renameUpdate(self):
        """重命名，在下载后调用"""
        if not GlobalMCSL2Variables.devMode:
            rename(
                cfg.get(cfg.oldExecuteable),
                f"{cfg.get('oldExecuteable')}.old",
            )
            self.moveFile()
        else:
            return

    def moveFile(self):
        """移动下载后的文件，重命名后调用"""
        move(
            f"MCSL2/Downloads/MCSL2{self.updateExtSuffix}",
            f"MCSL2{self.updateExtSuffix}",
        )
        restart()


def cmpVersion(newVer: str) -> bool:
    """比较版本号"""
    return bool(int("".join(MCSL2VERSION.split("."))) < int("".join(newVer.split("."))))


def restart():
    """重启，在移动文件后调用(此代码在开发时不起作用)"""
    if not GlobalMCSL2Variables.devMode:
        execl(
            cfg.get(cfg.oldExecuteable),
            cfg.get(cfg.oldExecuteable),
            *sys.argv,
        )


def deleteOldMCSL2():
    """删除旧的，在更新重启后调用"""
    if not GlobalMCSL2Variables.devMode:
        try:
            remove(f"{sys.executable}.old")
        except Exception:
            pass
    else:
        return

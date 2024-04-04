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
Update Controller
"""

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from MCSL2Lib import MCSL2VERSION
from MCSL2Lib.ProgramControllers.aria2ClientController import Aria2Controller
import sys
from os import remove, name as osname, rename, execl, path as osp
from platform import architecture
from shutil import move
from qfluentwidgets import MessageBox, InfoBar, InfoBarPosition
from MCSL2Lib.ProgramControllers.settingsController import cfg
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
        self.updateOSName = "Windows" if osname == "nt" else "Linux"
        self.updateProcessExt = "." + cfg.get(cfg.oldExecuteable).split(".")[1]
        self.updateVerificationFileName = "verification." + (
            "pyd" if osname == "nt" else "so"
        )
        self.updateArchitecture: str = ""
        self.isUpdateAvailable = True
        if "64" in architecture()[0]:
            self.updateArchitecture = f"{self.updateOSName}-x64"
        else:
            InfoBar.error(
                title=self.tr("更新失败"),
                content=self.tr("你正在使用非官方构建的版本"),
                position=InfoBarPosition.TOP_RIGHT,
                duration=-1,
                parent=self.parent().window(),
            )
            self.isUpdateAvailable = False
        self.processUpdateLink = f"http://update.mcsl.com.cn/Update/{self.updateArchitecture}/MCSL2{self.updateProcessExt}"
        self.verificationUpdateLink = f"http://update.mcsl.com.cn/Update/{self.updateArchitecture}/MCSL2Lib/{self.updateVerificationFileName}"

    def downloadUpdate(self, showInfoBar: bool = True):
        """下载，首先调用"""
        if GlobalMCSL2Variables.devMode:
            return
        else:
            if not Aria2Controller.testAria2Service():
                if not Aria2Controller.startAria2():
                    box = MessageBox(
                        title=self.tr("无法更新"),
                        content=self.tr(
                            "MCSL2 的 Aria2 可能未安装或启动失败。\n已尝试重新启动 Aria2。"
                        ),
                        parent=self.parent(),
                    )
                    box.exec()
                    return
            else:
                if not self.isUpdateAvailable:
                    return
                if showInfoBar:
                    InfoBar.info(
                        title=self.tr("正在下载更新"),
                        content=self.tr("MCSL2 稍后将自动重启"),
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=-1,
                        parent=self.parent().window(),
                    )
            Aria2Controller.download(
                uri=self.processUpdateLink,
                watch=False,
                interval=0.2,
                stopped=self.downloadVerification,
            )

    def downloadVerification(self):
        """下载MCSL2验证模块，在下载主程序之后调用"""
        if GlobalMCSL2Variables.devMode:
            return
        if not osp.exists(f"MCSL2/Downloads/{self.updateVerificationFileName}"):
            self.downloadUpdate(showInfoBar=False)
            return
        else:
            Aria2Controller.download(
                uri=self.verificationUpdateLink,
                watch=False,
                interval=0.2,
                stopped=self.renameUpdate,
            )

    def renameUpdate(self):
        """重命名，在下载验证文件后调用"""
        if not GlobalMCSL2Variables.devMode:
            rename(
                cfg.get(cfg.oldExecuteable),
                f"{cfg.get(cfg.oldExecuteable)}.old",
            )
            rename(
                f"MCSL2Lib/{self.updateVerificationFileName}",
                f"MCSL2Lib/{self.updateVerificationFileName}.old",
            )
            self.moveFile()
        else:
            return

    def moveFile(self):
        """移动下载后的文件，在重命名后调用"""
        move(
            f"MCSL2/Downloads/MCSL2{self.updateProcessExt}",
            f"MCSL2{self.updateProcessExt}",
        )
        move(
            f"MCSL2/Downloads/{self.updateVerificationFileName}",
            f"MCSL2Lib/{self.updateVerificationFileName}",
        )
        restart()


def compareVersion(newVer: str) -> bool:
    """比较版本号"""
    return bool(int("".join(MCSL2VERSION.split("."))) < int("".join(newVer.split("."))))


def restart():
    """重启，在移动文件后调用(此代码在开发时不起作用)"""
    if GlobalMCSL2Variables.devMode:
        return
    else:
        execl(
            cfg.get(cfg.oldExecuteable),
            cfg.get(cfg.oldExecuteable),
            *sys.argv,
        )


def deleteOldMCSL2():
    """删除旧的，在更新重启后调用"""
    if GlobalMCSL2Variables.devMode:
        return
    else:
        try:
            remove(f"{sys.executable}.old")
        except Exception:
            pass
        try:
            remove("MCSL2Lib/verification.so.old")
        except Exception:
            pass
        try:
            remove("MCSL2Lib/verification.pyd.old")
        except Exception:
            pass

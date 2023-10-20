from PyQt5.QtCore import QThread, pyqtSignal, QObject
from MCSL2Lib import MCSL2VERSION
from MCSL2Lib.Controllers.aria2ClientController import Aria2Controller
from MCSL2Lib.Controllers.networkController import Session
import sys
from os import remove, name as osname, rename, execl
from platform import architecture
from shutil import move
from qfluentwidgets import MessageBox, InfoBar, InfoBarPosition
from MCSL2Lib.Controllers.settingsController import SettingsController
from MCSL2Lib.variables import GlobalMCSL2Variables

settingsController = SettingsController()


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
            latestVerInfo = Session().get(f"https://mcsl.com.cn/api/checkUpdate").json()
            self.isUpdate.emit(latestVerInfo)
        except Exception:
            self.isUpdate.emit({"latest": "", "update-log": ""})


class MCSL2FileUpdater(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.updateOSPrefix = "Windows" if osname == "nt" else "Linux"
        self.updateExtSuffix = (
            "." + settingsController.fileSettings["oldExecuteable"].split(".")[1]
        )
        self.updateArchitecturePrefix: str = ""
        if "32" in architecture()[0]:
            self.updateArchitecturePrefix = f"{self.updateOSPrefix}-x86"
        elif "64" in architecture()[0]:
            self.updateArchitecturePrefix = f"{self.updateOSPrefix}-x64"
        else:
            self.updateArchitecturePrefix = f"{self.updateOSPrefix}-arm64"
        self.updateSite = f"http://shenjack.top:5100/LxHTT/MCSL2_Update/media/branch/master/{self.updateArchitecturePrefix}/MCSL2{self.updateExtSuffix}"

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
                        content=self.tr("MCSL2的Aria2可能未安装或启动失败。\n已尝试重新启动Aria2。"),
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
                settingsController.fileSettings["oldExecuteable"],
                f"{settingsController.fileSettings['oldExecuteable']}.old",
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
    currentVer = MCSL2VERSION.split(".")
    newVer = newVer.split(".")
    isUpdate: bool = False
    for i in range(0, 4):
        if int(currentVer[i]) < int(newVer[i]):
            isUpdate = True
            break
        else:
            continue
    return isUpdate


def restart():
    """重启，在移动文件后调用(此代码在开发时不起作用)"""
    if not GlobalMCSL2Variables.devMode:
        execl(
            settingsController.fileSettings["oldExecuteable"],
            settingsController.fileSettings["oldExecuteable"],
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

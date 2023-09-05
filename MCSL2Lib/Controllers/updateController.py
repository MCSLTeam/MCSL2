from PyQt5.QtCore import QThread, pyqtSignal
from MCSL2Lib.Controllers.aria2ClientController import Aria2Controller
from MCSL2Lib.Controllers.networkController import Session
from MCSL2Lib.variables import GlobalMCSL2Variables
import sys
from os import remove, name as osname, rename, execl
from platform import architecture
from shutil import move


class CheckUpdateThread(QThread):
    """
    检查更新的网络连接线程\n
    使用多线程防止假死
    """

    isUpdate = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CheckUpdateThread")

    def run(self):
        try:
            latestVerInfo = (
                Session()
                .get(
                    f"http://api.2018k.cn/checkVersion?id=BCF5D58B4AE6471E98CFD5A56604560B&version={GlobalMCSL2Variables.MCSL2Version}"
                )
                .text.split("|")
            )
            self.isUpdate.emit(latestVerInfo)
        except Exception as e:
            self.isUpdate.emit(["Failed"])


class FetchUpdateIntroThread(QThread):
    """
    获取更新介绍的网络连接线程\n
    使用多线程防止假死
    """

    content = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("FetchUpdateIntroThread")

    def run(self):
        try:
            intro = f"""{Session().get("http://api.2018k.cn/getExample?id=BCF5D58B4AE6471E98CFD5A56604560B&data=remark").text}"""
            self.content.emit(intro)
        except Exception as e:
            self.content.emit(["奇怪，怎么获取信息失败了？\n检查一下网络，或者反馈给开发者？"])


class MCSL2FileUpdater:
    def __init__(self):
        self.oldExecutableFileName = sys.executable
        self.updateOSPrefix = "Windows" if osname == "nt" else "Linux"
        self.updateExtSuffix = ".exe" if osname == "nt" else ".bin"
        self.updateArchitecturePrefix: str = ""
        if "32" in architecture()[0]:
            self.updateArchitecturePrefix = f"{self.updateOSPrefix}-x86"
        elif "64" in architecture()[0]:
            self.updateArchitecturePrefix = f"{self.updateOSPrefix}-x64"
        elif "32" in architecture()[0]:
            self.updateArchitecturePrefix = f"{self.updateOSPrefix}-arm64"
        self.updateSite = f"http://shenjack.top:5100/LxHTT/MCSL2_Update/media/branch/master/{self.updateArchitecturePrefix}/MCSL2{self.updateExtSuffix}"
        self.devMode = (
            True
            if self.oldExecutableFileName.endswith("python")
            or self.oldExecutableFileName.endswith("python.exe")
            else False
        )

    def download(self):
        """下载，首先调用"""
        if not self.devMode:
            Aria2Controller.download(
                uri=self.updateSite,
                watch=True,
                interval=0.2,
            )
        else:
            return

    def rename(self):
        """重命名，在下载后调用"""
        if not self.devMode:
            rename(self.oldExecutableFileName, f"{self.oldExecutableFileName}.old")
        else:
            return

    def moveFile(self):
        """移动下载后的文件，重命名后调用"""
        move(
            f"MCSL2/Downloads/MCSL2{self.updateExtSuffix}",
            f"MCSL2{self.updateExtSuffix}",
        )

    def restart(self):
        """重启，在移动文件后调用(此代码在开发时不起作用)"""
        if not self.devMode:
            execl(self.oldExecutableFileName, self.oldExecutableFileName, *sys.argv)
            sys.exit()

    def deleteOldMCSL2(self):
        """删除旧的，在更新重启后调用"""
        if not self.devMode:
            try:
                remove(f"{self.oldExecutableFileName}.old")
            except Exception:
                pass
        else:
            return

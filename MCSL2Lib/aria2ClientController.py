#     Copyright 2023, MCSL Team, mailto:lxhtt@mcsl.com.cn
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
A controller for aria2 download engine.
"""

from os import getcwd
from os import path as ospath
from platform import system
from shutil import which
from subprocess import PIPE, STDOUT, CalledProcessError, check_output, Popen
from typing import Optional, Callable

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QProcess, QTimer
from PyQt5.QtWidgets import QProgressDialog
from aria2p import Client, API, Download

from MCSL2Lib.networkController import Session
from MCSL2Lib.settingsController import SettingsController

settingsController = SettingsController()


class Aria2Controller:
    """
    Aria2Controller is a singleton class that controls aria2c.
    """

    ########################
    #  private class vars  #
    ########################

    _port = 6800

    _osType = None

    _aria2 = None

    _downloadTasks = {}

    _downloadWatcher = {}

    systemType = ""

    aria2cStatus = False

    aria2Process = None

    def __init__(self):
        super().__init__()
        self.systemType: str
        self.aria2cStatus: bool
        self.checkPlatform()

    #################
    #  Check Aria2  #
    #################

    @classmethod
    def init(cls):
        cls.checkPlatform()

    @classmethod
    def checkPlatform(cls):
        CurrentSystem = system().lower()
        if "windows" in CurrentSystem:
            cls.systemType = "Windows"
            cls._osType = "Windows"
        elif "linux" in CurrentSystem:
            cls.systemType = "Linux"
            cls._osType = "Linux"
        elif "darwin" in CurrentSystem:
            cls.systemType = "macOS"
            cls._osType = "macOS"
        else:
            pass

    @classmethod
    def checkAria2(cls):
        cls.checkPlatform()
        if cls.systemType == "Windows":
            if not ospath.exists(r"MCSL2/Aria2/aria2c.exe"):
                cls.aria2cStatus = False
            else:
                cls.aria2cStatus = True
        elif cls.systemType == "macOS":
            if not ospath.exists(r"/usr/local/bin/aria2c"):
                cls.aria2cStatus = False
            else:
                cls.aria2cStatus = True
        elif cls.systemType == "Linux":
            cls.aria2cStatus = cls.checkPackageExistsOnLinux("aria2c")
        else:
            pass
        return cls.aria2cStatus

    @staticmethod
    def checkPackageExistsOnLinux(PackageName):
        try:
            check_output(["which", PackageName])
            return True
        except CalledProcessError:
            return False

    #########################
    #  If there's no Aria2  #
    #########################

    def ShowNoAria2Msg(self):
        pass
        # ReturnNum = CallMCSL2Dialog(
        #     Tip="NoAria2",
        #     OtherTextArg=None,
        #     isNeededTwoButtons=1,
        #     ButtonArg="安装|取消",
        # )
        # if ReturnNum == 1:
        #     if self.systemType == "Windows":
        #         openWebUrl(
        #             "https://www.github.com/LxHTT/MCSL2",
        #         )
        #         # self.WinInstallAria2(mainWindow)
        #     elif self.systemType == "macOS":
        #         self.macOSInstallAria2()
        #     elif self.systemType == "Linux":
        #         LinuxInstall = self.LinuxInstallAria2()
        #         if LinuxInstall:
        #             pass
        #         else:
        #             MCSLLogger.Log(
        #                 Msg="InstallAria2Failed",
        #                 MsgArg=f"平台：{self.systemType}",
        #                 MsgLevel=2,
        #             )
        #             CallMCSL2Dialog(
        #                 Tip="InstallAria2Failed",
        #                 OtherTextArg=None,
        #                 isNeededTwoButtons=0,
        #                 ButtonArg=None,
        #             )
        # else:
        #     pass

    ########################################
    #  Install Aria2 (No Windows support)  #
    ########################################

    def macOSInstallAria2(self):
        try:
            HomeBrewInstallCommand = '/bin/bash -c "$(curl -fsSL ' \
                                     'https://mecdn.mcserverx.com/gh/LxHTT/MCSLDownloaderAPI/master' \
                                     '/MCSL2NecessaryTools/Install_Homebrew.sh)"'
            InstallHomeBrew = Popen(HomeBrewInstallCommand, stdout=PIPE, shell=True)
            output, error = InstallHomeBrew.communicate()
            if InstallHomeBrew.returncode == 0:
                InstallAria2 = Popen("brew install aria2", stdout=PIPE, shell=True)
                self.aria2cStatus = True
            else:
                pass
        except Exception as e:
            print(e)

    def LinuxInstallAria2(self):
        if which("apt"):
            cmd = ["apt", "install", "-y", "aria2"]
        elif which("pacman"):
            cmd = ["pacman", "-Sy", "--noconfirm", "aria2"]
        elif which("yum"):
            cmd = ["yum", "install", "-y", "aria2"]
        else:
            return "No"
        try:
            Popen(cmd, check=True)
        except CalledProcessError as e:
            print(e)
            return False
        return True

    #################
    #  Start Aria2  #
    #################

    def Download(self, DownloadURL: str):
        if self.systemType == "Windows":
            Aria2Program = "MCSL2/Aria2/aria2c.exe"
        elif self.systemType == "macOS":
            Aria2Program = "/usr/local/bin/aria2c"
        elif self.systemType == "Linux":
            Aria2Program = "aria2c"
        else:
            Aria2Program = "aria2c"
        ConfigCommand = "--conf-path=/MCSL2/Aria2/aria2.conf --input-file=/MCSL2/Aria2/aria2.session " \
                        "--save-session=/MCSL2/Aria2/aria2.session"
        Aria2Thread = Aria2ProcessThread(
            Aria2Program=Aria2Program,
            ConfigCommand=ConfigCommand,
            DownloadURL=DownloadURL,
        )
        Aria2Thread.start()

    @classmethod
    def WinInstallAria2(cls, mainWindow):
        pass
        # todo
        # def onDownloadFinish(failed):
        #     """
        #     文件结构:aira2.zip
        #             |-aria2-xxxxxxxx
        #                 |-aria2c.exe
        #                 |-...
        #     将aria2c.exe移动到MCSL2/Aria2/aria2c.exe
        #     :return:
        #     """
        #     if failed:
        #         MCSLLogger.Log(
        #             Msg="InstallAria2Failed", MsgArg=f"平台：{cls._osType}", MsgLevel=0
        #         )
        #         CallMCSL2Dialog(
        #             Tip="InstallAria2Failed",
        #             OtherTextArg=None,
        #             isNeededTwoButtons=0,
        #             ButtonArg=None,
        #         )
        #     zipFile = ZipFile("MCSL2/Aria2/aria2.zip")
        #     zipFile.extractall("MCSL2/Aria2")
        #     zipFile.close()
        #     aria2Folder = [v for v in listdir("MCSL2/Aria2") if "aria2-" in v][0]
        #     move(f"MCSL2/Aria2/{aria2Folder}/aria2c.exe", "MCSL2/Aria2/aria2c.exe")
        #     rmtree(f"MCSL2/Aria2/{aria2Folder}")
        #
        #     remove("MCSL2/Aria2/aria2.zip")
        #     CallMCSL2Dialog(
        #         Tip="Aria2安装完成", OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None
        #     )
        #
        # url = "https://api.github.com/repos/aria2/aria2/releases/latest"
        # try:
        #     releaseInfo = Session.get(url=url).json()
        # except SSLError as e:
        #     MCSLLogger.ExceptionLog(e)
        #     print("获取Aria2仓库release失败:关闭代理后重试")
        #     CallMCSL2Dialog(
        #         Tip="获取Aria2仓库release失败:\n请关闭代理后重试",
        #         OtherTextArg=None,
        #         isNeededTwoButtons=0,
        #         ButtonArg=None,
        #     )
        #     return
        #
        # except Exception as e:
        #     MCSLLogger.ExceptionLog(e)
        #     print(f"获取Aria2仓库release失败:{e}")
        #     CallMCSL2Dialog(
        #         Tip=f"获取Aria2仓库release失败:\n{e}",
        #         OtherTextArg=None,
        #         isNeededTwoButtons=0,
        #         ButtonArg=None,
        #     )
        #     return
        #
        # try:
        #     winPackageInfo = [
        #         v for v in releaseInfo["assets"] if "win-32bit" in v["name"]
        #     ][0]
        # except KeyError as e:
        #     # 肯定存在32bit 但是可能是因为rest api的问题导致获取失败
        #     message = releaseInfo.get("message", "未知错误")
        #     CallMCSL2Dialog(
        #         Tip=f"获取Aria2仓库release失败:\n{message}",
        #         OtherTextArg=None,
        #         isNeededTwoButtons=0,
        #         ButtonArg=None,
        #     )
        #     MCSLLogger.ExceptionLog(e)
        #     print(f"获取Aria2仓库release失败:{message}")
        #     return
        #
        # winPackageUrl = winPackageInfo["browser_download_url"]
        # manager = NormalDownloadManager(
        #     winPackageUrl, "MCSL2/Aria2/aria2.zip", parent=mainWindow
        # )
        #
        # manager.downloadFinished.connect(onDownloadFinish)
        #
        # manager.download()

    @classmethod
    def download(
            cls,
            uri,
            info_get: Optional[Callable[[dict], None]] = None,
            stopped: Optional[Callable[[int], None]] = None,
            watch=True,
            interval=0.1
    ) -> str:
        """
        Download a file from uri

        param uri: the uri of the file to be downloaded
        param watch: whether to watch the download progress
        param info_get: the slot function to get the download progress
        param stopped: the slot function to be called when the download is stopped
            get integer:
                0: download finished
                1: download error
                2: download removed
        param interval: the interval of watching the download progress
        """
        gid = cls.addUri(uri)
        if watch:
            cls._downloadWatcher[gid] = DownloadWatcher(
                gid,
                info_get=info_get,
                stopped=stopped,
                interval=interval
            )
        return gid

    @classmethod
    def getWatcher(cls, gid) -> 'DownloadWatcher':
        """
        get the DownloadWatcher of the download task
        """
        return cls._downloadWatcher.get(gid, None)

    @classmethod
    def killWatcher(cls, gid):
        """
        kill the DownloadWatcher of the download task
        """
        watcher = cls._downloadWatcher.get(gid, None)
        if watcher:
            watcher.kill()
            del cls._downloadWatcher[gid]

    @classmethod
    def addUri(cls, uri: str) -> str:
        """
        Add a download task to Aria2,and return the gid of the task
        * normally, this function is only used by Class:DownloadWatcher

        param uri: the uri of the file to be downloaded
        """
        if not cls.testAria2Service():
            if not cls.aria2Process.isOpen():
                cls.startAria2()
            else:
                raise Exception("Aria2 service is not running")

        gid = cls._aria2.add_uris([uri]).gid
        if gid in cls._downloadTasks.keys():
            download = cls._aria2.get_download(gid)

            if download.status not in ["complete", "error", "removed"]:
                raise Exception("Download task already exists")

        cls._downloadTasks.update({gid: [uri]})
        return gid

    @classmethod
    def addUris(cls, uris: list):
        """
        Add a download task to Aria2,and return the gid of the task
        * normally, this function is only used by Class:DownloadWatcher

        param uris: the uris of the files to be downloaded
        """
        if not cls.testAria2Service():
            cls.startAria2()

        gid = cls._aria2.add_uris(uris).gid
        if gid in cls._downloadTasks.keys():
            download = cls._aria2.get_download(gid)
            if download.status not in ["complete", "error", "removed"]:
                raise Exception("Download task already exists")
        cls._downloadTasks.update({gid: uris})
        return gid

    @classmethod
    def getDownloadsStatus(cls, gid: str) -> dict:
        """
        Get the state of a download task by gid
        * normally, this function is only used by Class:DownloadWatcher
        """
        try:
            download = cls._aria2.get_download(gid)
        except:
            cls.killWatcher(gid)
            return {
                "connections": 0,
                "speed": "0.0B/s",
                "progress": "0.0%",
                "status": "removed",
                "totalLength": "0.0B",
                "completedLength": "0.0B",
                "files": [],
                "bar": 0,
                "eta": "-",
            }
        download: Download
        rv = {
            "connections": download.connections,
            "speed": download.download_speed_string() if download.status == 'active' else download.status,
            "progress": download.progress_string(),
            "status": download.status,
            "totalLength": download.total_length_string(),
            "completedLength": download.completed_length_string(),
            "files": [f.path for f in download.files],
            "bar": int(download.progress),
            "eta": download.eta_string(),
        }
        return rv

    @classmethod
    def pauseDownloadTask(cls, gid: str):
        """
        Halt a download task by gid
        * normally, this function is only used by Class:DownloadWatcher
        """
        try:
            print("已暂停:", cls._aria2.client.pause(gid))
            cls._downloadTasks.pop(gid)
        except:
            pass

    @classmethod
    def resumeDownloadTask(cls, gid: str):
        """
        Resume a download task by gid
        * normally, this function is only used by Class:DownloadWatcher
        """
        print("已恢复:", cls._aria2.client.unpause(gid))
        cls._downloadTasks.update({gid: cls._aria2.get_download(gid).files})

    @classmethod
    def cancelDownloadTask(cls, gid: str):
        """
        Cancel a download task by gid
        * normally, this function is only used by Class:DownloadWatcher
        """
        try:
            print("已取消:", cls._aria2.client.remove(gid))
        finally:
            if gid in cls._downloadTasks.keys():
                cls._downloadTasks.pop(gid)

    @classmethod
    def applySettings(cls, Settings: dict):
        """
        Apply settings to Aria2,current not used
        """
        cls._aria2.port = Settings.get("port", cls._port)
        cls._port = cls._aria2.port

    @classmethod
    def testAria2Service(cls):
        """
        测试Aria2服务是否正常
        :return:
        """
        try:
            cls._aria2.client.get_version()
        except:
            return False
        return True

    @classmethod
    def startAria2(cls) -> bool:
        """
        启动Aria2服务,如果启动失败则返回False，否则返回True
        """
        if rv := cls.checkAria2():
            if cls._osType == "Windows":
                Aria2Program = "MCSL2/Aria2/aria2c.exe"
            elif cls._osType == "macOS":
                Aria2Program = "/usr/local/bin/aria2c"
            elif cls._osType == "Linux":
                Aria2Program = "aria2c"
            else:
                Aria2Program = "aria2c"
            path = ospath.join(getcwd(), "MCSL2", "Downloads")
            ConfigCommand = [
                "--conf-path=MCSL2/Aria2/aria2.conf",
                "--input-file=MCSL2/Aria2/aria2.session",
                "--save-session=MCSL2/Aria2/aria2.session",
                f"--dir={path}",
            ]
            cls.aria2Process = QProcess()
            cls.aria2Process.startDetached(Aria2Program, ConfigCommand)
            cls.aria2Process.waitForStarted()
            cls._aria2 = API(Client(host="http://localhost", port=cls._port, secret="", timeout=0.1))
            if cls.testAria2Service():
                return True
            else:
                cls._aria2 = None
                return False
        return rv

    @classmethod
    def downloadCompletedHandler(cls, gid, stopFlag):
        cls._aria2: API
        try:
            download = cls._aria2.get_download(gid)
        except:
            cls.killWatcher(gid)
            return None
        if stopFlag:
            try:
                cls._aria2.client.remove(gid)  # 删除下载任务
            except:
                pass
        if download.status == "complete" and gid in cls._downloadTasks.keys():
            cls._downloadTasks.pop(gid)
            if gid in cls._downloadWatcher.keys():
                cls._downloadWatcher.pop(gid)
        return download

    @classmethod
    def shutDown(cls):
        try:
            if cls._aria2 is not None:
                cls._aria2: API
                # 清理aria2中被取消和暂停的任务，以及其对应的下载文件
                cls._aria2.pause_all()
                cls._aria2.client.shutdown()
            if cls.aria2Process is not None:
                if cls.aria2Process.isOpen():
                    cls.aria2Process.kill()
            return True
        except Exception:
            try:
                cls.aria2Process.kill()
            except Exception:
                pass
            return True


class NormalDownloadManager(QObject):
    downloadFinished = pyqtSignal(bool)

    def __init__(self, uri, savePath, retryCount=3, parent=None):
        super().__init__()
        self.uri = uri
        self.setParent(parent)
        self.savePath = savePath
        self.retryCount = retryCount
        self.downloadThread = None
        self.dialog: Optional[QProgressDialog] = None
        self.downloadProgress = 0

    def download(self):
        self.downloadThread = NormalDownloadThread(
            self.uri, self.savePath, self.retryCount, parent=self.parent()
        )

        self.downloadThread.finished.connect(self.downloadFinish)
        self.downloadThread.start()

    @pyqtSlot(int)
    def getFileSize(self, fileSize):
        self.dialog.setRange(0, fileSize)

    def showDialog(self):
        self.dialog = QProgressDialog(labelText="正在下载", parent=self.parent())
        # 阻塞主窗口
        self.dialog.setModal(True)
        self.dialog.show()

    @pyqtSlot(int)
    def updateProgress(self, progress):
        self.downloadProgress += progress
        print(self.downloadProgress)
        self.dialog.setValue(self.downloadProgress)

    @pyqtSlot(bool)
    def downloadFinish(self, failed):
        if self.needDialog:
            self.dialog.close()
        self.downloadFinished.emit(failed)


class NormalDownloadThread(QThread):
    fileSize = pyqtSignal(int)
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self, uri, savePath, retryCount=3, parent=None):
        super().__init__()
        self.setParent(parent)
        self.uri = uri
        self.savePath = savePath
        self.retryCount = retryCount
        self.failed = False

    def run(self):
        print("开始下载")
        flag = False
        # 普通下载
        with open(self.savePath, "wb") as f:
            for r in range(self.retryCount):
                response = Session.get(self.uri, timeout=10, stream=True)
                fileSize = response.headers.get("Content-Length", 0)
                self.progress.emit(int(fileSize))

                for data in response.iter_content(chunk_size=4096):
                    self.progress.emit(len(data))
                    f.write(data)
                flag = True
                break
        if flag:
            print("下载完成")
        else:
            print("下载失败")
            self.failed = True
        self.finished.emit(self.failed)


###################
#   Aria2 Thread  #
###################


class Aria2ProcessThread(QThread):
    started = pyqtSignal()
    finished = pyqtSignal(bool)

    def __init__(self, Aria2Program, ConfigCommand, DownloadURL):
        super().__init__()
        self.Aria2Program = Aria2Program
        self.ConfigCommand = ConfigCommand
        self.DownloadURL = DownloadURL

    def run(self):
        MCSL2_Aria2Client = API(Client(host="http://localhost", port=6800))
        MCSL2_Aria2Client.add_uris(self.DownloadURL)
        process = Popen(
            [self.Aria2Program, self.ConfigCommand], stdout=PIPE, stderr=STDOUT
        )
        process.wait()


class DownloadWatcher(QObject):
    """
    DownloadWatcher is a QThread that watches the download progress of a download task.
    download task started and download information emitted every interval.
    """

    # 每隔一段时间获取一次下载信息(self.Interval)，并发射下载信息OnDownloadInfoGet(dict)
    onDownloadInfoGet = pyqtSignal(dict)
    downloadStop = pyqtSignal(list)

    def __init__(
            self,
            gid,
            info_get: Optional[Callable[[dict], None]],
            stopped: Optional[Callable[[int], None]],
            interval=0.1,
            parent: Optional[QObject] = None
    ) -> None:
        """
        uris: a list of download urls
        interval can be a float or int (xxx seconds)
        """
        super().__init__(parent)
        self._gid = gid
        self._interval = interval
        self._files = None

        if info_get is not None:
            self.onDownloadInfoGet.connect(info_get)
        if stopped is not None:
            self.downloadStop.connect(stopped)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDownloadInfo)
        self.timer.singleShot(int(1000 * self._interval), lambda: self.timer.start(int(self._interval * 1000)))

    def updateDownloadInfo(self):
        if (status := Aria2Controller.getDownloadsStatus(self._gid))[
            "status"
        ] not in ["complete", "error", "removed"]:
            self.onDownloadInfoGet.emit(status)
            # print(
            #     f'下载进度：{status["progress"]},'
            #     f'下载速度：{status["speed"]},'
            #     f'连接数量:{status["connections"]},'
            #     f'文件大小：{status["totalLength"]},'
            #     f'eta：{status["eta"]}')
        elif status["status"] == "complete":
            self.timer.stop()
            self.onDownloadInfoGet.emit(status)
            dl = Aria2Controller.downloadCompletedHandler(self._gid, False)
            self.downloadStop.emit([dl])
            print("下载完成")
        elif status["status"] == "error":
            self.timer.stop()
            self.onDownloadInfoGet.emit(status)
            dl = Aria2Controller.downloadCompletedHandler(self._gid, True)
            self.downloadStop.emit([dl])
            print("下载失败")
        elif status["status"] == "removed":
            self.timer.stop()
            self.onDownloadInfoGet.emit(status)
            dl = Aria2Controller.downloadCompletedHandler(self._gid, True)
            self.downloadStop.emit([dl])
            print("下载被取消")

    def stopDownload(self):
        Aria2Controller.pauseDownloadTask(self._gid)
        Aria2Controller.downloadCompletedHandler(self._gid, True)

    def resumeDownload(self):
        Aria2Controller.resumeDownloadTask(self._gid)

    def pauseDownload(self):
        Aria2Controller.pauseDownloadTask(self._gid)

    def kill(self):
        self.timer.stop()

    @property
    def gid(self):
        return self._gid

    @property
    def interval(self):
        return self._interval

    @property
    def files(self):
        return self._files


def initializeAria2Configuration():
    Aria2Thread = str(settingsController.fileSettings['aria2Thread'])
    with open(
            r"MCSL2/Aria2/aria2.conf", "w+", encoding="utf-8"
    ) as Aria2ConfigFile:
        Aria2ConfigFile.write(
            "file-allocation=falloc\n"
            "continue=true\n"
            "max-concurrent-downloads=5\n"
            "min-split-size=5M\n"
            "split=64\n"
            "disable-ipv6=false\n"
            "enable-http-pipelining=false\n"
            f"max-connection-per-server={Aria2Thread}\n"
            "enable-rpc=true\n"
            "rpc-allow-origin-all=true\n"
            "rpc-listen-all=true\n"
            "event-poll=select\n"
            "rpc-listen-port=6800\n"
            "force-save=false"
        )
        Aria2ConfigFile.close()
    with open(
            r"MCSL2/Aria2/aria2.session", "w+", encoding="utf-8"
    ) as Aria2SessionFile:
        Aria2SessionFile.write("")
        Aria2SessionFile.close()

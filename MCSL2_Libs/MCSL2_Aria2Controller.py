from os import path as ospath
from os import remove, listdir, getcwd
from platform import system
from shutil import which, rmtree, move
from subprocess import PIPE, STDOUT, CalledProcessError, check_output, Popen
from typing import Optional
from zipfile import ZipFile

import requests
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QProcess
from PyQt5.QtWidgets import QProgressDialog
from aria2p import Client, API
from requests.exceptions import SSLError

from MCSL2_Libs.MCSL2_Dialog import CallMCSL2Dialog
from MCSL2_Libs.MCSL2_Logger import MCSL2Logger
from MCSL2_Libs.MCSL2_Settings import MCSL2Settings, OpenWebUrl

MCSLLogger = MCSL2Logger()


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

    def __init__(self):
        try:
            super().__init__()
            self.Aria2Status = None
            self.OSType: str
            self.Aria2Status: bool
            self.CheckPlatform()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    #################
    #  Check Aria2  #
    #################

    @classmethod
    def CheckPlatform(cls):
        try:
            CurrentSystem = system().lower()
            if 'windows' in CurrentSystem:
                cls.OSType = "Windows"
                cls._osType = "Windows"
            elif 'linux' in CurrentSystem:
                cls.OSType = "Linux"
                cls._osType = "Linux"
            elif 'darwin' in CurrentSystem:
                cls.OSType = "macOS"
                cls._osType = "macOS"
            else:
                pass
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def CheckAria2(self):
        try:
            self.CheckPlatform()
            if self.OSType == "Windows":
                if not ospath.exists(r"MCSL2/Aria2/aria2c.exe"):
                    self.Aria2Status = False
                else:
                    self.Aria2Status = True
            elif self.OSType == "macOS":
                if not ospath.exists(r"/usr/local/bin/aria2c"):
                    self.Aria2Status = False
                else:
                    self.Aria2Status = True
            elif self.OSType == "Linux":
                self.Aria2Status = self.LinuxCheckPackageExists('aria2c')
            else:
                pass
        except Exception as e:
            MCSLLogger.ExceptionLog(e)
        return self.Aria2Status

    def LinuxCheckPackageExists(self, PackageName):
        try:
            check_output(["which", PackageName])
            return True
        except CalledProcessError:
            return False

    #########################
    #  If there's no Aria2  #
    #########################

    def ShowNoAria2Msg(self, mainWindow):
        try:
            ReturnNum = CallMCSL2Dialog(
                Tip="NoAria2",
                OtherTextArg=None,
                isNeededTwoButtons=1, ButtonArg="安装|取消")
            if ReturnNum == 1:
                if self.OSType == "Windows":

                    OpenWebUrl(
                        "https://www.github.com/LxHTT/MCSL2", )
                    # self.WinInstallAria2(mainWindow)
                elif self.OSType == "macOS":
                    self.macOSInstallAria2()
                elif self.OSType == "Linux":
                    LinuxInstall = self.LinuxInstallAria2()
                    if LinuxInstall:
                        pass
                    else:
                        MCSLLogger.Log(Msg=
                                       "InstallAria2Failed", MsgArg=f"平台：{self.OSType}", MsgLevel=2
                                       )
                        CallMCSL2Dialog(
                            Tip="InstallAria2Failed",
                            OtherTextArg=None,
                            isNeededTwoButtons=0, ButtonArg=None)
            else:
                pass
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    ########################################
    #  Install Aria2 (No Windows support)  #
    ########################################

    def macOSInstallAria2(self):
        try:
            HomeBrewInstallCommand = '/bin/bash -c "$(curl -fsSL https://mecdn.mcserverx.com/gh/LxHTT/MCSLDownloaderAPI/master/MCSL2NecessaryTools/Install_Homebrew.sh)"'
            InstallHomeBrew = Popen(HomeBrewInstallCommand,
                                    stdout=PIPE, shell=True)
            output, error = InstallHomeBrew.communicate()
            if InstallHomeBrew.returncode == 0:
                InstallAria2 = Popen("brew install aria2", stdout=PIPE, shell=True)
                self.Aria2Status = True
            else:
                MCSLLogger.Log(Msg=
                               "InstallAria2Failed", MsgArg=f"平台：{self.OSType}", MsgLevel=2)
                CallMCSL2Dialog(
                    Tip="InstallAria2Failed",
                    OtherTextArg=None,
                    isNeededTwoButtons=0, ButtonArg=None)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

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
            MCSLLogger.ExceptionLog(e)
            return False
        return True

    #################
    #  Start Aria2  #
    #################

    def InitAria2Configuration(self):
        try:
            Aria2Thread = str(MCSL2Settings().Aria2Thread)
            with open(r"MCSL2/Aria2/aria2.conf", "w+", encoding="utf-8") as Aria2ConfigFile:
                Aria2ConfigFile.write("file-allocation=falloc\n"
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
                                      "force-save=false")
                Aria2ConfigFile.close()
            with open(r"MCSL2/Aria2/aria2.session", "w+", encoding="utf-8") as Aria2SessionFile:
                Aria2SessionFile.write("")
                Aria2SessionFile.close()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def Download(self, DownloadURL: str):
        try:
            if self.OSType == "Windows":
                Aria2Program = "MCSL2/Aria2/aria2c.exe"
            elif self.OSType == "macOS":
                Aria2Program = "/usr/local/bin/aria2c"
            elif self.OSType == "Linux":
                Aria2Program = "aria2c"
            else:
                Aria2Program = "aria2c"
            ConfigCommand = "--conf-path=/MCSL2/Aria2/aria2.conf --input-file=/MCSL2/Aria2/aria2.session --save-session=/MCSL2/Aria2/aria2.session"
            Aria2Thread = Aria2ProcessThread(
                Aria2Program=Aria2Program, ConfigCommand=ConfigCommand, DownloadURL=DownloadURL,
            )
            Aria2Thread.start()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @classmethod
    def WinInstallAria2(cls, mainWindow):
        def onDownloadFinish(failed):
            """
            文件结构:aira2.zip
                    |-aria2-xxxxxxxx
                        |-aria2c.exe
                        |-...
            将aria2c.exe移动到MCSL2/Aria2/aria2c.exe
            :return:
            """
            if failed:
                MCSLLogger.Log(Msg=
                               "InstallAria2Failed", MsgArg=f"平台：{cls._osType}", MsgLevel=0)
                CallMCSL2Dialog(
                    Tip="InstallAria2Failed",
                    OtherTextArg=None,
                    isNeededTwoButtons=0, ButtonArg=None)
            zipFile = ZipFile("MCSL2/Aria2/aria2.zip")
            zipFile.extractall("MCSL2/Aria2")
            zipFile.close()
            aria2Folder = [v for v in listdir("MCSL2/Aria2") if "aria2-" in v][0]
            move(f"MCSL2/Aria2/{aria2Folder}/aria2c.exe", "MCSL2/Aria2/aria2c.exe")
            rmtree(f"MCSL2/Aria2/{aria2Folder}")

            remove("MCSL2/Aria2/aria2.zip")
            CallMCSL2Dialog(Tip="Aria2安装完成", OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)

        url = 'https://api.github.com/repos/aria2/aria2/releases/latest'
        try:
            releaseInfo = requests.get(
                url=url
            ).json()
        except SSLError as e:
            MCSLLogger.ExceptionLog(e)
            print("获取Aria2仓库release失败:关闭代理后重试")
            CallMCSL2Dialog(Tip="获取Aria2仓库release失败:\n请关闭代理后重试", OtherTextArg=None, isNeededTwoButtons=0,
                            ButtonArg=None)
            return

        except Exception as e:
            MCSLLogger.ExceptionLog(e)
            print(f"获取Aria2仓库release失败:{e}")
            CallMCSL2Dialog(Tip=f"获取Aria2仓库release失败:\n{e}", OtherTextArg=None, isNeededTwoButtons=0,
                            ButtonArg=None)
            return

        try:
            winPackageInfo = [v for v in releaseInfo["assets"] if 'win-32bit' in v["name"]][0]
        except KeyError as e:
            # 肯定存在32bit 但是可能是因为rest api的问题导致获取失败
            message = releaseInfo.get("message", "未知错误")
            CallMCSL2Dialog(Tip=f"获取Aria2仓库release失败:\n{message}", OtherTextArg=None, isNeededTwoButtons=0,
                            ButtonArg=None)
            MCSLLogger.ExceptionLog(e)
            print(f"获取Aria2仓库release失败:{message}")
            return

        winPackageUrl = winPackageInfo["browser_download_url"]
        manager = NormalDownloadManager(winPackageUrl, "MCSL2/Aria2/aria2.zip",
                                        parent=mainWindow)

        manager.downloadFinished.connect(onDownloadFinish)

        manager.download()

    @classmethod
    def AddUri(cls, uri: str) -> str:
        try:
            """
            Add a download task to Aria2,and return the gid of the task
            * normally, this function is only used by Class:DownloadWatcher
            """
            if not cls.TestAria2Service():
                cls.StartAria2()

            gid = cls._aria2.add_uris([uri]).gid
            if gid in cls._downloadTasks.keys():
                download = cls._aria2.get_download(gid)
                if download.status not in ["complete", "error", "removed"]:
                    raise Exception("Download task already exists")
            cls._downloadTasks.update({gid: [uri]})

        except Exception as e:
            MCSLLogger.ExceptionLog(e)
        return gid

    @classmethod
    def AddUris(cls, uris: list):
        try:
            """
            Add a download task to Aria2,and return the gid of the task
            * normally, this function is only used by Class:DownloadWatcher
            """
            if not cls.TestAria2Service():
                cls.StartAria2()

            gid = cls._aria2.add_uris(uris).gid
            if gid in cls._downloadTasks.keys():
                download = cls._aria2.get_download(gid)
                if download.status not in ["complete", "error", "removed"]:
                    raise Exception("Download task already exists")
            cls._downloadTasks.update({gid: uris})
        except Exception as e:
            MCSLLogger.ExceptionLog(e)
        return gid

    @classmethod
    def GetDownloadsStatus(cls, gid: str) -> dict:
        try:
            """
            Get the state of a download task by gid
            * normally, this function is only used by Class:DownloadWatcher
            """
            download = cls._aria2.get_download(gid)
            rv = {
                "speed": download.download_speed_string(),
                "progress": download.progress_string(),
                "status": download.status,
                "totalLength": download.total_length_string(),
                "completedLength": download.completed_length_string(),
                "files": [f.path for f in download.files],
                "bar": int(download.progress),
                "eta": download.eta_string(),
            }
            if download.status == "complete":
                cls._downloadTasks.pop(gid)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)
        return rv

    @classmethod
    def PauseDownloadTask(cls, gid: str):
        try:
            """
            Halt a download task by gid
            * normally, this function is only used by Class:DownloadWatcher
            """
            print("已暂停:", cls._aria2.client.pause(gid))
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @classmethod
    def ApplySettings(cls, Settings: dict):
        try:
            """
            Apply settings to Aria2,current not used
            """
            cls._aria2.port = Settings.get("port", cls._port)
            cls._port = cls._aria2.port
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @classmethod
    def TestAria2Service(cls):
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
    def StartAria2(cls):
        try:
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
                f"--dir={path}"
            ]
            QProcess.startDetached(Aria2Program, ConfigCommand)
            cls._aria2 = API(
                Client(
                    host="http://localhost",
                    port=cls._port,
                    secret=""
                )
            )
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @classmethod
    def DownloadCompletedHandler(cls, gid, stopFlag):
        try:
            cls._aria2: API
            download = cls._aria2.get_download(gid)
            if stopFlag:
                cls._aria2.client.force_remove(gid)
            else:
                if download.status == "complete" and gid in cls._downloadTasks.keys():
                    cls._downloadTasks.pop(gid)
                    cls._aria2.client.remove(gid)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @classmethod
    def Shutdown(cls):
        try:
            if cls._aria2 is not None:
                cls._aria2: API
                cls._aria2.remove_all(True)
                cls._aria2.client.shutdown()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)


class NormalDownloadManager(QObject):
    downloadFinished = pyqtSignal(bool)

    def __init__(self, uri, savePath, retryCount=3, parent=None):
        try:
            super().__init__()
            self.uri = uri
            self.setParent(parent)
            self.savePath = savePath
            self.retryCount = retryCount
            self.downloadThread = None
            self.dialog: Optional[QProgressDialog] = None
            self.downloadProgress = 0
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def download(self):
        try:
            self.downloadThread = NormalDownloadThread(self.uri, self.savePath, self.retryCount,
                                                       parent=self.parent())

            self.downloadThread.finished.connect(self.downloadFinish)
            self.downloadThread.start()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @pyqtSlot(int)
    def getFileSize(self, fileSize):
        try:
            self.dialog.setRange(0, fileSize)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def showDialog(self):
        try:
            self.dialog = QProgressDialog(labelText='正在下载', parent=self.parent())
            # 阻塞主窗口
            self.dialog.setModal(True)
            self.dialog.show()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @pyqtSlot(int)
    def updateProgress(self, progress):
        try:
            self.downloadProgress += progress
            print(self.downloadProgress)
            self.dialog.setValue(self.downloadProgress)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @pyqtSlot(bool)
    def downloadFinish(self, failed):
        try:
            if self.needDialog:
                self.dialog.close()
            self.downloadFinished.emit(failed)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)


class NormalDownloadThread(QThread):
    fileSize = pyqtSignal(int)
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self, uri, savePath, retryCount=3, parent=None):
        try:
            super().__init__()
            self.setParent(parent)
            self.uri = uri
            self.savePath = savePath
            self.retryCount = retryCount
            self.failed = False
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def run(self):
        try:
            MCSLLogger.Log(Msg="StartDownload", MsgArg=f"\n链接：{self.uri}", MsgLevel=0, )
            flag = False
            # 普通下载
            with open(self.savePath, "wb") as f:
                for r in range(self.retryCount):
                    try:
                        response = requests.get(
                            self.uri,
                            timeout=10,
                            stream=True
                        )
                        fileSize = response.headers.get("Content-Length", 0)
                        self.progress.emit(int(fileSize))
                        i = 0
                        for data in response.iter_content(chunk_size=4096):
                            self.progress.emit(len(data))
                            f.write(data)
                        flag = True
                        break
                    except Exception as e:
                        print(e)
                        MCSLLogger.Log(Msg=f"DownloadError retry:{r + 1}/{self.retryCount}",
                                       MsgArg=f"\n链接：{self.uri}",
                                       MsgLevel=1)
            if flag:
                MCSLLogger.Log(Msg="DownloadCompleted", MsgArg=f"\n链接：{self.uri}", MsgLevel=0
                               )
            else:
                MCSLLogger.Log(Msg="DownloadFailed", MsgArg=f"\n链接：{self.uri}", MsgLevel=2
                               )
                self.failed = True
            self.finished.emit(self.failed)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)


###################
#   Aria2 Thread  #
###################


class Aria2ProcessThread(QThread):
    started = pyqtSignal()
    finished = pyqtSignal(bool)

    def __init__(self, Aria2Program, ConfigCommand, DownloadURL):
        try:
            super().__init__()
            self.Aria2Program = Aria2Program
            self.ConfigCommand = ConfigCommand
            self.DownloadURL = DownloadURL
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def run(self):
        MCSL2_Aria2Client = API(
            Client(host="http://localhost", port=6800))
        MCSL2_Aria2Client.add_uris(self.DownloadURL)
        MCSLLogger.Log(Msg=
                       "StartDownload", MsgArg=f"\n链接：{self.DownloadURL}", MsgLevel=0)
        try:
            process = Popen(
                [self.Aria2Program, self.ConfigCommand], stdout=PIPE, stderr=STDOUT)
            process.wait()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)


class DownloadWatcher(QThread):
    """
    DownloadWatcher is a QThread that watches the download progress of a download task.
    download task started and download information emitted every interval.
    """

    # 每隔一段时间获取一次下载信息(self.Interval)，并发射下载信息OnDownloadInfoGet(dict)
    OnDownloadInfoGet = pyqtSignal(dict)
    DownloadStop = pyqtSignal(bool)

    def __init__(self, uris: list, interval=1, parent: Optional[QObject] = None) -> None:
        try:
            """
            uris: a list of download urls
            interval can be a float or int (xxx seconds)
            """
            super().__init__(parent)
            self._uris = uris
            self._gid = Aria2Controller.AddUris(self._uris)
            self._stopFlag = False
            self._interval = interval
            self._downloadStatus = Aria2Controller.GetDownloadsStatus(self._gid)
            self._e = None
            self._files = None
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def run(self) -> None:
        try:

            MCSLLogger.Log(Msg=
                           "StartDownload", MsgArg=f"\n链接：{self._uris}", MsgLevel=0, )
            while (status := Aria2Controller.GetDownloadsStatus(self._gid))["status"] not in ["complete", "error",
                                                                                              "removed"]:
                if self._stopFlag:
                    break
                # update download status
                self._downloadStatus = status

                self.OnDownloadInfoGet.emit(
                    Aria2Controller.GetDownloadsStatus(self._gid))

                MCSLLogger.Log(Msg=
                               "Downloading...",
                               MsgArg=f'下载进度：{status["progress"]},下载速度：{status["speed"]},文件大小：{status["totalLength"]},eta：{status["eta"]}',
                               MsgLevel=0)
                self._files = status.get("files", None)
                if isinstance(self._interval, int):
                    self.sleep(self._interval)
                elif isinstance(self._interval, float):
                    self.msleep(max(100, int(self._interval * 1000)))
            if not self._stopFlag:
                print("下载完成")

        except Exception as e:
            MCSLLogger.ExceptionLog(e)
            self._e = e
        Aria2Controller.DownloadCompletedHandler(self._gid, self.StopOrCancel)

    @pyqtSlot()
    def StopWatch(self):
        try:
            Aria2Controller.PauseDownloadTask(self._gid)
            self._stopFlag = True
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @property
    def Gid(self):
        return self._gid

    @property
    def StopOrCancel(self):
        return self._stopFlag or self._e is not None

    @property
    def Interval(self):
        return self._interval

    @property
    def DownloadStatus(self):
        return self._downloadStatus

    @property
    def Files(self):
        return self._files

    @Interval.setter
    def Interval(self, interval: float or int):
        try:
            self._interval = interval
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

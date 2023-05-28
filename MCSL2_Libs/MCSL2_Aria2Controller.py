from shutil import which
from subprocess import PIPE, STDOUT, SW_HIDE, CalledProcessError, check_output, Popen
from typing import Optional

from aria2p import Client, API
from platform import system
from os import path as ospath
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
from MCSL2_Libs.MCSL2_Dialog import CallMCSL2Dialog
from MCSL2_Libs.MCSL2_Logger import MCSL2Logger
from MCSL2_Libs.MCSL2_Settings import MCSL2Settings, OpenWebUrl


class Aria2Controller:
    """
    Aria2Controller is a singleton class that controls aria2c.
    """

    ########################
    #  private class vars  #
    ########################

    _port = 6800

    _aria2 = API(
        Client(
            host="http://localhost",
            port=_port,
            secret=""
        )
    )
    _downloadTasks = {}

    def __init__(self, LogFilesCount):
        super().__init__()
        self.Aria2Status = None
        self.OSType: str
        self.Aria2Status: bool
        self.LogFilesCount = LogFilesCount
        self.CheckPlatform()

    #################
    #  Check Aria2  #
    #################

    def CheckPlatform(self):
        CurrentSystem = system().lower()
        if 'windows' in CurrentSystem:
            self.OSType = "Windows"

        elif 'linux' in CurrentSystem:
            self.OSType = "Linux"
        elif 'darwin' in CurrentSystem:
            self.OSType = "macOS"
        else:
            pass

    def CheckAria2(self):
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
            self.Aria2Status = self.LinuxCheckPackageExists('aria2')
        else:
            pass
        return self.Aria2Status

    def LinuxCheckPackageExists(self, PackageName):
        try:
            check_output(["which", PackageName], creationflags=SW_HIDE)
            return True
        except CalledProcessError:
            return False

    #########################
    #  If there's no Aria2  #
    #########################

    def ShowNoAria2Msg(self):
        ReturnNum = CallMCSL2Dialog(
            Tip="NoAria2",
            OtherTextArg=None,
            isNeededTwoButtons=1, ButtonArg="安装|取消")
        if ReturnNum == 1:
            if self.OSType == "Windows":
                OpenWebUrl(
                    "https://www.github.com/LxHTT/MCSL2", LogFilesCount=self.LogFilesCount)
            elif self.OSType == "macOS":
                self.macOSInstallAria2()
            elif self.OSType == "Linux":
                LinuxInstall = self.LinuxInstallAria2()
                if LinuxInstall:
                    pass
                else:
                    MCSL2Logger(
                        "InstallAria2Failed", MsgArg=f"平台：{self.OSType}", MsgLevel=2,
                        LogFilesCount=self.LogFilesCount).Log()
                    CallMCSL2Dialog(
                        Tip="InstallAria2Failed",
                        OtherTextArg=None,
                        isNeededTwoButtons=0, ButtonArg=None)
        else:
            pass

    ########################################
    #  Install Aria2 (No Windows support)  #
    ########################################

    def macOSInstallAria2(self):
        HomeBrewInstallCommand = '/bin/bash -c "$(curl -fsSL https://mecdn.mcserverx.com/gh/LxHTT/MCSLDownloaderAPI/master/MCSL2NecessaryTools/Install_Homebrew.sh)"'
        InstallHomeBrew = Popen(HomeBrewInstallCommand,
                                stdout=PIPE, shell=True)
        output, error = InstallHomeBrew.communicate()
        if InstallHomeBrew.returncode == 0:
            InstallAria2 = Popen("brew install aria2", stdout=PIPE, shell=True)
            self.Aria2Status = True
        else:
            MCSL2Logger(
                "InstallAria2Failed", MsgArg=f"平台：{self.OSType}", MsgLevel=0, LogFilesCount=self.LogFilesCount).Log()
            CallMCSL2Dialog(
                Tip="InstallAria2Failed",
                OtherTextArg=None,
                isNeededTwoButtons=0, ButtonArg=None)

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
        except CalledProcessError:
            return False
        return True

    #################
    #  Start Aria2  #
    #################

    def InitAria2Configuration(self):
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

    def Download(self, DownloadURL: str):
        if self.OSType == "Windows":
            Aria2Program = "MCSL2/Aria2/aria2c.exe"
        elif self.OSType == "macOS":
            Aria2Program = "/usr/local/bin/aria2c"
        elif self.OSType == "Linux":
            Aria2Program = "aria2c"
        else:
            Aria2Program = "aria2c"
        ConfigCommand = "--conf-path=/MCSL2/Aria2/aria2.conf --input-file=/MCSL2/Aria2/aria2.session --save-session=/MCSL2/Aria2/aria2.session "
        Aria2Thread = Aria2ProcessThread(
            Aria2Program=Aria2Program, ConfigCommand=ConfigCommand, DownloadURL=DownloadURL,
            LogFilesCount=self.LogFilesCount)
        Aria2Thread.start()

    @classmethod
    def AddUri(cls, uri: str) -> str:
        """
        Add a download task to Aria2,and return the gid of the task
        * normally, this function is only used by Class:DownloadWatcher
        """
        gid = cls._aria2.add_uris([uri]).gid
        if gid in cls._downloadTasks.keys():
            download = cls._aria2.get_download(gid)
            if download.status not in ["complete", "error", "removed"]:
                raise Exception("Download task already exists")
        cls._downloadTasks.update({gid: [uri]})

        return gid

    @classmethod
    def AddUris(cls, uris: list):
        """
        Add a download task to Aria2,and return the gid of the task
        * normally, this function is only used by Class:DownloadWatcher
        """
        gid = cls._aria2.add_uris(uris).gid
        if gid in cls._downloadTasks.keys():
            download = cls._aria2.get_download(gid)
            if download.status not in ["complete", "error", "removed"]:
                raise Exception("Download task already exists")
        cls._downloadTasks.update({gid: uris})
        return gid

    @classmethod
    def GetDownloadsStatus(cls, gid: str) -> dict:
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
            "files": download.files,
        }
        if download.status == "complete":
            cls._downloadTasks.pop(gid)
        return rv

    @classmethod
    def ApplySettings(cls, Settings: dict):
        """
        Apply settings to Aria2,current not used
        """
        cls._aria2.port = Settings.get("port", cls._port)
        cls._port = cls._aria2.port


###################
#   Aria2 Thread  #
###################


class Aria2ProcessThread(QThread):
    started = pyqtSignal()
    finished = pyqtSignal(bool)

    def __init__(self, Aria2Program, ConfigCommand, DownloadURL, LogFilesCount):
        super().__init__()
        self.Aria2Program = Aria2Program
        self.ConfigCommand = ConfigCommand
        self.DownloadURL = DownloadURL
        self.LogFilesCount = LogFilesCount

    def run(self):
        MCSL2_Aria2Client = API(
            Client(host="http://localhost", port=6800))
        MCSL2_Aria2Client.add_uris(self.DownloadURL)
        MCSL2Logger(
            "StartDownload", MsgArg=f"\n链接：{self.DownloadURL}", MsgLevel=0, LogFilesCount=self.LogFilesCount).Log()
        try:
            process = Popen(
                [self.Aria2Program, self.ConfigCommand], stdout=PIPE, stderr=STDOUT)
            process.wait()
        except Exception as e:
            print('Error:', e)


class DownloadWatcher(QThread):
    """
    DownloadWatcher is a QThread that watches the download progress of a download task.
    download task started and download information emitted every interval.
    """

    # 每隔一段时间获取一次下载信息(self.Interval)，并发射下载信息OnDownloadInfoGet(dict)
    OnDownloadInfoGet = pyqtSignal(dict)

    def __init__(self, uris: list, interval=1, parent: Optional[QObject] = ...) -> None:
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

    def run(self) -> None:
        while (status := Aria2Controller.GetDownloadsStatus(self._gid))["status"] not in ["complete", "error",
                                                                                          "removed"]:
            if self._stopFlag:
                break
            # update download status
            self._downloadStatus = status

            self.OnDownloadInfoGet.emit(
                Aria2Controller.GetDownloadsStatus(self._gid))

            if self._interval is int:
                self.sleep(self._interval)
            else:
                self.msleep(min(1, int(self._interval * 1000)))

    @pyqtSlot()
    def StopWatch(self):
        self._stopFlag = True

    @property
    def Gid(self):
        return self._gid

    @property
    def Interval(self):
        return self._interval

    @property
    def DownloadStatus(self):
        return self._downloadStatus

    @Interval.setter
    def Interval(self, interval: float or int):
        self._interval = interval

from shutil import which
from subprocess import PIPE, STDOUT, SW_HIDE, CalledProcessError, check_output, Popen
from aria2p import Client, API
from platform import system
from os import path as ospath
from PyQt5.QtCore import QThread, pyqtSignal
from MCSL2_Libs.MCSL2_Dialog import CallMCSL2Dialog
from MCSL2_Libs.MCSL2_Logger import MCSL2Logger
from MCSL2_Libs.MCSL2_Settings import MCSL2Settings, OpenWebUrl


class Aria2Controller():
    def __init__(self, LogFilesCount):
        super().__init__()
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

    def LinuxCheckPackageExists(PackageName):
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
                if LinuxInstall == True:
                    pass
                else:
                    MCSL2Logger(
                        "InstallAria2Failed", MsgArg=f"平台：{self.OSType}", MsgLevel=2, LogFilesCount=self.LogFilesCount).Log()
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
            Aria2Program=Aria2Program, ConfigCommand=ConfigCommand, DownloadURL=DownloadURL, LogFilesCount=self.LogFilesCount)
        Aria2Thread.start()

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

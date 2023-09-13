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
A controller for aria2 download engine.
"""
import hashlib
import json
import subprocess
import time
from os import getcwd, mkdir, remove
from os import path as osp
from platform import system
from shutil import which
from subprocess import PIPE, STDOUT, CalledProcessError, check_output, Popen
from typing import Optional, Callable, Dict

from PyQt5.QtCore import QThread, pyqtSignal, QObject, QProcess, QTimer, QMutex
from aria2p import Client, API, Download

from MCSL2Lib.Controllers.settingsController import SettingsController
from MCSL2Lib.utils import workingThreads

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
            if not osp.exists(r"MCSL2/Aria2/aria2c.exe"):
                cls.aria2cStatus = False
            else:
                cls.aria2cStatus = True
        elif cls.systemType == "macOS":
            if not osp.exists(r"/usr/local/bin/aria2c"):
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

    ########################################
    #  Install Aria2 (No Windows support)  #
    ########################################

    def macOSInstallAria2(self):
        try:
            HomeBrewInstallCommand = '/bin/bash -c "$(curl -fsSL https://mecdn.mcserverx.com/gh/LxHTT/MCSLDownloaderAPI/master/MCSL2NecessaryTools/Install_Homebrew.sh)"'
            InstallHomeBrew = Popen(HomeBrewInstallCommand, stdout=PIPE, shell=True)
            output, error = InstallHomeBrew.communicate()
            if InstallHomeBrew.returncode == 0:
                InstallAria2 = Popen("brew install aria2", stdout=PIPE, shell=True)
                self.aria2cStatus = True
            else:
                # CallMCSL2Dialog(
                #     Tip="InstallAria2Failed",
                #     OtherTextArg=None,
                #     isNeededTwoButtons=0,
                #     ButtonArg=None,
                # )
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
        ConfigCommand = "--conf-path=/MCSL2/Aria2/aria2.conf --input-file=/MCSL2/Aria2/aria2.session --save-session=/MCSL2/Aria2/aria2.session"
        Aria2Thread = Aria2ProcessThread(
            Aria2Program=Aria2Program,
            ConfigCommand=ConfigCommand,
            DownloadURL=DownloadURL,
        )
        Aria2Thread.start()

    @classmethod
    def download(
            cls,
            uri,
            info_get: Optional[Callable[[dict], None]] = None,
            stopped: Optional[Callable[[int], None]] = None,
            extraData: Optional[tuple] = None,
            watch=True,
            interval=0.1,
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
                interval=interval,
                extraData=extraData,
            )
        return gid

    @classmethod
    def getWatcher(cls, gid) -> "DownloadWatcher":
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
            "speed": download.download_speed_string()
            if download.status == "active"
            else download.status,
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
            path = osp.join(getcwd(), "MCSL2", "Downloads")
            ConfigCommand = [
                "--conf-path=MCSL2/Aria2/aria2.conf",
                "--input-file=MCSL2/Aria2/aria2.session",
                "--save-session=MCSL2/Aria2/aria2.session",
                f"--dir={path}",
            ]
            cls.aria2Process = QProcess()
            cls.aria2Process.startDetached(Aria2Program, ConfigCommand)
            cls.aria2Process.waitForStarted()
            cls._aria2 = API(
                Client(host="http://localhost", port=cls._port, secret="", timeout=0.1)
            )
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
    def killAria2(cls):
        # 如果是Windows系统，强制关闭aria2进程
        if cls._osType == "Windows":
            # command = 'tasklist | findstr "aria2c"'
            # result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
            # if result.stdout != "":
            #     print("已杀死aria2进程")
            subprocess.run("taskkill /f /im aria2c.exe", text=True, shell=True)
        elif cls._osType == "macOS":
            subprocess.run("killall aria2c", text=True, shell=True)
        elif cls._osType == "Linux":
            subprocess.run("killall aria2c", text=True, shell=True)
        else:
            subprocess.run("killall aria2c", text=True, shell=True)

    @classmethod
    def shutDown(cls):
        try:
            if cls._aria2 is not None:
                cls._aria2: API
                # 清理aria2中被取消和暂停的任务，以及其对应的下载文件
                cls._aria2.pause_all()
                cls._aria2.client.shutdown()
            if cls.aria2Process is not None:
                cls.killAria2()
            return True
        except Exception:
            try:
                cls.killAria2()
            except Exception:
                pass
            return True


class Aria2BootThread(QThread):
    """
    Aria2启动线程
    """

    loaded = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        try:
            time_time = time.time()
            if Aria2Controller.startAria2():
                if Aria2Controller.testAria2Service():
                    self.loaded.emit(True)
                else:
                    self.loaded.emit(False)

        except Exception:
            self.loaded.emit(False)
        finally:
            print(f"启动Aria2服务耗时:{time.time() - time_time}")


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
            stopped: Optional[Callable[[list], None]],
            interval=0.1,
            extraData: Optional[tuple] = None,
            parent: Optional[QObject] = None,
    ) -> None:
        """
        uris: a list of download urls
        interval can be a float or int (xxx seconds)
        """
        super().__init__(parent)
        self._gid = gid
        self._interval = interval
        self._files = None
        self._extraData = extraData

        if info_get is not None:
            self.onDownloadInfoGet.connect(info_get)
        if stopped is not None:
            self.downloadStop.connect(stopped)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDownloadInfo)
        self.timer.singleShot(
            int(1000 * self._interval),
            lambda: self.timer.start(int(self._interval * 1000)),
        )

    def updateDownloadInfo(self):
        if (status := Aria2Controller.getDownloadsStatus(self._gid))["status"] not in [
            "complete",
            "error",
            "removed",
        ]:
            self.onDownloadInfoGet.emit(status)
        elif status["status"] == "complete":
            self.timer.stop()
            self.onDownloadInfoGet.emit(status)
            dl = Aria2Controller.downloadCompletedHandler(self._gid, False)
            self.downloadStop.emit([dl, self._extraData])
            print("下载完成")
        elif status["status"] == "error":
            self.timer.stop()
            self.onDownloadInfoGet.emit(status)
            dl = Aria2Controller.downloadCompletedHandler(self._gid, True)
            self.downloadStop.emit([dl, self._extraData])
            print("下载失败")
        elif status["status"] == "removed":
            self.timer.stop()
            self.onDownloadInfoGet.emit(status)
            dl = Aria2Controller.downloadCompletedHandler(self._gid, True)
            self.downloadStop.emit([dl, self._extraData])
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
    Aria2Thread = str(settingsController.fileSettings["aria2Thread"])
    with open(r"MCSL2/Aria2/aria2.conf", "w+", encoding="utf-8") as Aria2ConfigFile:
        Aria2ConfigFile.write(
            "file-allocation=none\n"
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
    with open(r"MCSL2/Aria2/aria2.session", "w+", encoding="utf-8") as Aria2SessionFile:
        Aria2SessionFile.write("")


entries = {}
entries_mutex = QMutex()


# class DL_EntryManager(QObject):
#     """
#     下载记录管理器,用于管理下载记录:获取下载记录,检查记录完整性,删除不完整的记录,添加记录等
#     # >>> 注意：本类方法全部是类方法,请勿将本类实例化!<<<
#     """
#
#     file = "MCSL2//Downloads//download_entries.json"
#     path = "MCSL2//Downloads"
#
#     @staticmethod
#     def fileExisted():
#         """
#         在对文件进行操作前检查文件是否存在，如果不存在则创建文件,确保文件操作不会出错
#         """
#         if not osp.exists(osp.join("MCSL2", "Downloads")):
#             mkdir(osp.join("MCSL2", "Downloads"))
#         if not osp.exists(DL_EntryManager.file):
#             with open(DL_EntryManager.file, "w", encoding="utf-8") as f:
#                 f.write("{}")
#
#     @staticmethod
#     def read(check=True, autoDelete=True):
#         DL_EntryManager.fileExisted()
#         with open(DL_EntryManager.file) as f:
#             rv = json.load(f)
#         for coreName, coreData in rv.copy().items():
#             if check and not DL_EntryManager.checkCoreEntry(coreName, coreData["md5"], autoDelete):
#                 print("删除不完整的核心文件记录:", coreName)
#                 rv.pop(coreName)
#         return rv
#
#     entries = {}
#
#     @classmethod
#     def addEntry(cls, entryName: str, entryData: dict):
#         """
#         向文件中添加一条记录
#         """
#         print(
#             "新增记录:",
#             json.dumps(
#                 {entryName: entryData}, indent=4, ensure_ascii=False, sort_keys=True
#             ),
#         )
#         cls.entries.update({entryName: entryData})
#         cls.flush()
#
#     @classmethod
#     def addCoreEntry(cls, coreName: str, extraData: dict):
#         """
#         添加核心文件的记录
#         """
#         coreFileName = osp.join(cls.path, coreName)
#         # 计算md5
#         with open(coreFileName, "rb") as f:
#             md5 = hashlib.md5(f.read()).hexdigest()
#         extraData.update({"md5": md5})
#         cls.addEntry(coreName, extraData)
#
#     @classmethod
#     def popCoreEntry(cls, coreName: str, autoDelete=True) -> Dict:
#         """
#         删除核心文件的记录并返回删除的记录的原条目，如果autoDelete为True则同时删除核心文件
#         """
#         if coreName in cls.entries.keys():
#             rv = cls.entries.pop(coreName)
#             if autoDelete:
#                 try:
#                     remove(osp.join(cls.path, coreName))
#                 except:
#                     pass
#             cls.flush()
#             return {coreName: rv}
#         else:
#             return {}
#
#     @classmethod
#     def flush(cls):
#         """
#         将文件中的数据写入文件
#         """
#         cls.fileExisted()
#         with open(cls.file, "w", encoding="utf-8") as f:
#             json.dump(cls.entries, f, indent=4, ensure_ascii=False, sort_keys=True)
#
#     @classmethod
#     def checkCoreEntry(cls, coreName: str, originMd5: str, autoDelete=False):
#         """
#         检查核心文件的完整性
#         :param coreName: 核心文件名
#         :param originMd5: 原始md5
#         :param autoDelete: 如果文件不完整是否自动删除核心文件
#         """
#         coreFileName = osp.join(cls.path, coreName)
#         if osp.exists(coreFileName):
#             # 计算md5
#             with open(coreFileName, "rb") as f:
#                 fileMd5 = hashlib.md5(f.read()).hexdigest()
#             if fileMd5 == originMd5:
#                 return True
#             if autoDelete:
#                 try:  # 删除文件和记录
#                     remove(coreFileName)
#                     cls.entries.pop(coreName)
#                 except:
#                     pass
#         else:
#             if autoDelete:
#                 cls.entries.pop(coreName)
#         return False
#
#     @classmethod
#     def check(cls, autoDelete=False):
#         """
#         检查所有核心文件的完整性
#         :param autoDelete: 如果文件不完整是否自动删除核心文件
#         """
#         for coreName, coreData in cls.entries.items():
#             if not cls.checkCoreEntry(coreName, coreData["md5"], autoDelete):
#                 return False
#         cls.flush()
#         return True
#
#     @classmethod
#     def cleanUnavailable(cls):
#         """
#         清理所有无效记录（包括本地文件）
#         """
#         cls.check(True)
#
#     @classmethod
#     def tryGetEntry(cls, entryName: str, check=True, autoDelete=True):
#         """
#         尝试获取一条记录，如果记录不完整则返回None
#         """
#         if not check:
#             return cls.entries.get(entryName, None)
#         # 检查记录完整性
#         if cls.checkCoreEntry(entryName, cls.entries[entryName]["md5"], autoDelete):
#             return cls.entries[entryName]
#         else:
#             return None
#
#     @classmethod
#     def GetEntries(cls, check=True, autoDelete=True):
#         """
#         获取所有正确的记录
#         """
#         rv = cls.entries.copy()
#         for entryName in cls.entries.keys():
#             if cls.tryGetEntry(entryName, check, autoDelete) is None:
#                 rv.pop(entryName)
#         return rv
#
#     @classmethod
#     def getEntriesList(cls, check=True, autoDelete=True):
#         """
#         获取所有正确的记录的列表
#         "name", "type", "mc_version", "build_version", ...
#         """
#         rv = []
#         for entryName, entryData in cls.GetEntries(check, autoDelete).items():
#             e = entryData.copy()
#             e.update({"name": entryName})
#             rv.append(e)
#         return rv
#
#     def __new__(cls, *args, **kwargs):
#         raise Exception("请勿实例化本类,请使用类方法!")
#
# time.perf_counter()
# DL_EntryManager.entries = DL_EntryManager.read(check=False)
# DL_EntryManager.flush()


class DL_EntryManager(QObject):
    """
    下载记录管理器,用于管理下载记录:获取下载记录,检查记录完整性,删除不完整的记录,添加记录等
    # >>> 注意：请用DL_EntryController来调用此类中的方法!!(异步)<<<
    """
    onGetEntries = pyqtSignal(list)
    onReadEntries = pyqtSignal(dict)
    file = "MCSL2//Downloads//download_entries.json"
    path = "MCSL2//Downloads"

    def __init__(self, _entries, mutex: QMutex):
        super().__init__()
        self.entries = _entries
        self.mutex = mutex

    def fileExisted(self):
        """
        在对文件进行操作前检查文件是否存在，如果不存在则创建文件,确保文件操作不会出错
        """
        if not osp.exists(osp.join("MCSL2", "Downloads")):
            mkdir(osp.join("MCSL2", "Downloads"))
        if not osp.exists(DL_EntryManager.file):
            print("创建下载记录文件:", DL_EntryManager.file)
            with open(DL_EntryManager.file, "w", encoding="utf-8") as f:
                f.write("{}")

    def read(self, check=True, autoDelete=True):
        self.fileExisted()
        with open(DL_EntryManager.file, "r") as f:
            self.entries = json.load(f)
        for coreName, coreData in self.entries.copy().items():
            if check and not self.checkCoreEntry(coreName, coreData["md5"], autoDelete):
                print("删除不完整的核心文件记录:", coreName)
                try:
                    self.entries.pop(coreName)
                except KeyError:
                    pass
        self.flush()
        print("读取记录:", len(self.entries), "条")
        self.onReadEntries.emit(self.entries)
        return self.entries

    def addEntry(self, entryName: str, entryData: dict):
        """
        向文件中添加一条记录
        """
        print(
            "新增记录:",
            json.dumps(
                {entryName: entryData}, indent=4, ensure_ascii=False, sort_keys=True
            ),
        )
        self.mutex.lock()
        self.entries.update({entryName: entryData})
        self.mutex.unlock()
        self.flush()

    # @pyqtSlot(str, dict)
    def addCoreEntry(self, coreName: str, extraData: dict):
        """
        添加核心文件的记录
        """
        coreFileName = osp.join(self.path, coreName)
        # 计算md5
        with open(coreFileName, "rb") as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        extraData.update({"md5": md5})
        self.addEntry(coreName, extraData)

    def popCoreEntry(self, coreName: str, autoDelete=True) -> Dict:
        """
        删除核心文件的记录并返回删除的记录的原条目，如果autoDelete为True则同时删除核心文件
        """
        if coreName in self.entries.keys():
            self.mutex.lock()
            rv = self.entries.pop(coreName)
            self.mutex.unlock()
            if autoDelete:
                try:
                    remove(osp.join(self.path, coreName))
                except:
                    pass
            self.flush()
            return {coreName: rv}
        else:
            return {}

    def flush(self):
        """
        将文件中的数据写入文件
        """
        self.fileExisted()
        self.mutex.lock()
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=4, ensure_ascii=False, sort_keys=True)
        self.mutex.unlock()

    def checkCoreEntry(self, coreName: str, originMd5: str, autoDelete=False):
        """
        检查核心文件的完整性
        :param coreName: 核心文件名
        :param originMd5: 原始md5
        :param autoDelete: 如果文件不完整是否自动删除核心文件
        """
        coreFileName = osp.join(self.path, coreName)
        if osp.exists(coreFileName):
            # 计算md5
            with open(coreFileName, "rb") as f:
                fileMd5 = hashlib.md5(f.read()).hexdigest()
            if fileMd5 == originMd5:
                return True
            if autoDelete:
                try:  # 删除文件和记录
                    remove(coreFileName)
                    self.mutex.lock()
                    self.entries.pop(coreName)
                    self.mutex.unlock()
                except:
                    pass
        else:
            if autoDelete:
                self.mutex.lock()
                self.entries.pop(coreName)
                self.mutex.unlock()
        return False

    def check(self, autoDelete=False):
        """
        检查所有核心文件的完整性
        :param autoDelete: 如果文件不完整是否自动删除核心文件
        """
        self.mutex.lock()
        entries_snapshot = self.entries.copy()
        self.mutex.unlock()
        for coreName, coreData in entries_snapshot.items():
            if not self.checkCoreEntry(coreName, coreData["md5"], autoDelete):
                return False
        self.flush()
        return True

    def cleanUnavailable(self):
        """
        清理所有无效记录（包括本地文件）
        """
        self.check(True)

    def tryGetEntry(self, entryName: str, check=True, autoDelete=True):
        """
        尝试获取一条记录，如果记录不完整则返回None
        """
        if not check:
            return self.entries.get(entryName, None)
        # 检查记录完整性
        if self.checkCoreEntry(entryName, self.entries[entryName]["md5"], autoDelete):
            return self.entries[entryName]
        else:
            return None

    def GetEntries(self, check=True, autoDelete=True):
        """
        获取所有正确的记录
        """
        self.mutex.lock()
        entries_snapshot = self.entries.copy()
        self.mutex.unlock()
        rv = entries_snapshot.copy()

        # # 检查记录一致性
        # with open(self.file, "r") as f:
        #     fileRecordedEntries = json.load(f)
        #
        # if fileRecordedEntries != entries_snapshot:  # 如果数据不一致则重新读取,并更新记录.用于加速结果的生成
        #     print("记录不一致,重新计算各条目完整性,并更新本地记录")
        #     for entryName in entries_snapshot.keys():
        #         if self.tryGetEntry(entryName, check, autoDelete) is None:
        #             rv.pop(entryName)
        #     self.flush()
        for entryName in entries_snapshot.keys():
            if self.tryGetEntry(entryName, check, autoDelete) is None:
                rv.pop(entryName)
        self.flush()
        # else:
        #     print("记录一致,无需重新计算各条目完整性")
        return rv

    # @pyqtSlot(bool, bool)
    def getEntriesList(self, check=True, autoDelete=True):
        """
        获取所有正确的记录的列表
        "name", "type", "mc_version", "build_version", ...
        """
        rv = []
        for entryName, entryData in self.GetEntries(check, autoDelete).items():
            e = entryData.copy()
            e.update({"name": entryName})
            rv.append(e)
        self.onGetEntries.emit(rv)
        return rv

    def asyncDispatcher(self, info):
        method, kwargs = info
        getattr(self, method)(**kwargs)

    # def __new__(cls, *args, **kwargs):
    #     raise Exception("请勿实例化本类,请使用类方法!")


workingThreads.register("DL_Entry")


class DL_EntryController(QObject):
    """
    用于在线程中执行DL_EntryManager中的函数:
    1.controller = DL_EntryController()
    2.controller.resultReady.connect(...)
    3.controller.work.emit((<method:str>,<kwargs>:dict))
    """
    work = pyqtSignal(object)
    resultReady = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        global entries, entries_mutex
        self.mutex = entries_mutex
        self.entries = entries
        self.worker = DL_EntryManager(self.entries, self.mutex)
        self.worker.moveToThread(workingThreads.getThread("DL_Entry"))

        self.resultReady.connect(lambda _: self.worker.deleteLater())
        self.work.connect(self.worker.asyncDispatcher)
        self.worker.onGetEntries.connect(lambda l: self.resultReady.emit(l))
        self.worker.onReadEntries.connect(lambda d: self.resultReady.emit(d))


def set_entries(_):
    global entries
    entries = _


# entries = DL_EntryManager(entries, entries_mutex).read()
(controller := DL_EntryController()).resultReady.connect(
    lambda d: set_entries(d)
)
controller.work.emit(("read", {}))

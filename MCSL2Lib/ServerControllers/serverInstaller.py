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
Minecraft Forge Servers Installer.
"""

import json
import queue
from enum import Enum
from json import loads, dumps
from os import path as osp, name as osname
from queue import Queue
from typing import Optional, Tuple, Any
from zipfile import BadZipFile, ZipFile

from PyQt5.QtCore import (
    QProcess,
    QObject,
    pyqtSignal,
    QTimer,
    QFile,
    QIODevice,
    QThread,
)
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager

from .forge.install_thread import ForgeInstallThread
from ..ProgramControllers.settingsController import cfg
from ..utils import MCSL2Logger, ServicesUrl, readFile, writeFile
from ..variables import ConfigureServerVariables, EditServerVariables

configureServerVariables = ConfigureServerVariables()
editServerVariables = EditServerVariables()


class InstallerError(Exception):
    pass


class InstallerDownloadsMonitor(QThread):
    progressed = pyqtSignal(
        str, float, int, bool, bool
    )  # filename, dl_percent, speed, done, all_done

    def __init__(self, infoQueue: Queue, parent: QObject = None):
        super().__init__(parent)
        self.infoQueue = infoQueue

    def run(self):
        while True:
            rv = self.infoQueue.get()
            if rv is None:
                return  # cancel when installer is downloading sth.
            filename, speed, progress, done, allDone = rv
            self.progressed.emit(filename, progress, speed, done, allDone)
            if allDone:
                return  # all downloads finished


class McVersion:
    def __init__(self, version: str):
        vs = [int(i) for i in version.split(".")]
        if len(vs) == 2:
            self.v1, self.v2, self.v3 = vs[0], vs[1], 0
        elif len(vs) == 3:
            self.v1, self.v2, self.v3 = vs[0], vs[1], vs[2]
        else:
            raise ValueError("Invalid version string")

    def __str__(self):
        return f"{self.v1}.{self.v2}.{self.v3}"

    def __gt__(self, other):
        if self.v1 > other.v1:
            return True
        elif self.v1 == other.v1:
            if self.v2 > other.v2:
                return True
            elif self.v2 == other.v2:
                if self.v3 > other.v3:
                    return True
        return False

    def __lt__(self, other):
        if self.v1 < other.v1:
            return True
        elif self.v1 == other.v1:
            if self.v2 < other.v2:
                return True
            elif self.v2 == other.v2:
                if self.v3 < other.v3:
                    return True
        return False

    def __eq__(self, other):
        return self.v1 == other.v1 and self.v2 == other.v2 and self.v3 == other.v3

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)


class Installer(QObject):
    """
    安装器的基类,包含installerLogOutput信号,用于输出安装器的日志
    支持with语句
    """

    installFinished = pyqtSignal(bool, str)
    installerLogOutput = pyqtSignal(str)

    def __init__(self, cwd: str, file: str, logDecode="utf-8"):
        """
        :param cwd: The current working directory of the installer
        :param file: The name of the installer
        """
        super().__init__()
        self._cancelTimer = QTimer()
        self.cwd = cwd
        self.file = file
        self.logDecode = logDecode
        self.workingProcess: Optional[QProcess] = None
        self.logPartialData = b""
        self.installerLogOutput.connect(MCSL2Logger.info)
        self.cancelled = False
        # self.workThread = QThread()
        # self.workThread.start()

    def asyncInstall(self):
        raise NotImplementedError

    def cancelInstall(self, cancelled=False):
        self.cancelled = True
        if not cancelled:
            MCSL2Logger.warning("试图关闭 ForgeInstaller...")
            if self.workingProcess is not None:
                self.workingProcess.kill()
                self._cancelTimer.setSingleShot(True)
                self._cancelTimer.timeout.connect(lambda: self.cancelInstall(True))  # 设置超时时间
        else:
            MCSL2Logger.error(msg="关闭 ForgeInstaller 超时,正在强制关闭...")
            self.workingProcess.kill()
            self._cancelTimer.stop()
            self._cancelTimer.deleteLater()

    def _installerLogHandler(self, prefix: str = ""):
        newData = self.workingProcess.readAllStandardOutput().data()
        self.logPartialData += newData  # Append the incoming data to the buffer
        lines = self.logPartialData.split(b"\n")  # Split the buffer into lines
        self.partialData = (
            lines.pop()
        )  # The last element might be incomplete, so keep it in the buffer

        _ = []
        for line in lines:
            newOutput = line.decode(self.logDecode, errors="replace")
            _.append(">>".join([prefix, newOutput]))

        self.installerLogOutput.emit("\n".join(_))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.workingProcess is not None:
            self.workingProcess.kill()
            self.workingProcess = None


class BMCLAPIDownloader(QObject):
    downloadProgress = pyqtSignal(int, int)
    downloadFinished = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._manager = QNetworkAccessManager()
        self._reply = None
        self._url = None
        self._targetPath = None
        self._fileName = None

    def download(self, mcVersion, targetPath, fileName):
        self._url = ServicesUrl.getBmclapiUrl(str(mcVersion))
        self._targetPath = targetPath
        self._fileName = fileName
        self._download()

    def _download(self):
        self._manager.finished.connect(self.onDownloadFinished)
        request = QNetworkRequest(self._url)
        request.setHeader(
            QNetworkRequest.UserAgentHeader,
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0",
            # noqa: E501
        )
        # 设置自动跟随重定向
        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
        self._reply = self._manager.get(request)
        self._reply.downloadProgress.connect(self.onDownloadProgress)
        # 连接重定向信号，打印重定向后的URL
        self._reply.redirected.connect(lambda url: MCSL2Logger.info(f"Redirected to {url}"))

    def onDownloadProgress(self, bytesReceived, bytesTotal):
        self.downloadProgress.emit(bytesReceived, bytesTotal)

    def onDownloadFinished(self):
        data = self._reply.readAll()
        file = QFile(osp.join(self._targetPath, self._fileName))
        if file.open(QIODevice.WriteOnly):
            file.write(data)
            file.close()
        self.downloadFinished.emit(True)
        self._reply.deleteLater()
        self._manager.deleteLater()

    def cancelCurrentDownload(self):
        if self._reply is not None and self._reply.isRunning():
            self._reply.abort()
            self._reply.deleteLater()
        if self._manager is not None:
            self._manager.deleteLater()


class ForgeInstaller(Installer):
    downloadInfo = pyqtSignal(
        str, float, int, bool, bool
    )  # filename, dl_percent, speed, done, allDone

    class InstallPlan(Enum):
        PlanA = 0
        PlanB = 1

    def __init__(
        self,
        serverPath,
        file,
        isEditing: Optional[str] = "",
        java=None,
        installerPath=None,
        logDecode="utf-8",
    ):
        super().__init__(serverPath, file, logDecode)
        self.java = java
        self.serverPath = serverPath
        self.isEditing = int(isEditing) if isEditing != "" else None

        self._mcVersion = None
        self._profile = None
        self._forgeVersion = None
        self._bmclapiDownloader = None
        self._serverJarTargetPath = ""
        self._serverJarFileName = ""
        self._needHost = False
        self._dlInfoMonitor = None
        self._dlInfoQueue = None

        self.getInstallerData(
            osp.join(serverPath, file) if installerPath is None else installerPath
        )
        if self._mcVersion >= McVersion("1.17"):
            self.installPlan = ForgeInstaller.InstallPlan.PlanB
        elif self._mcVersion >= McVersion("1.8"):
            self.installPlan = ForgeInstaller.InstallPlan.PlanA
        else:
            raise InstallerError(
                self.tr(
                    "不支持的自动安装版本: {mcVersion}\nMCSL2 的 Forge 自动安装仅支持 Minecraft 1.8+"  # noqa: E501
                ).format(mcVersion=self._mcVersion)  # noqa: E501
            )

    def getInstallerData(self, jarFile):
        # 打开Installer压缩包
        # 读取version.json

        with ZipFile(
            jarFile,
            mode="r",
        ) as zipfile:
            try:
                _ = zipfile.read("install_profile.json")
            except KeyError:
                _ = zipfile.read("version.json")
            self._profile = loads(_)  # type: dict
            if not self.checkInstaller():
                raise InstallerError("Invalid Forge installer")

    def checkInstaller(self) -> bool:
        if (
            (versionInfo := self._profile.get("versionInfo", {}))
            .get("id", "")
            .lower()
            .startswith("forge")
        ):
            self._mcVersion = McVersion(versionInfo["id"].split("-")[0])
            self._forgeVersion = versionInfo["id"].replace((self._mcVersion), "").replace("-", "")
            return True
        elif "forge" in (version := self._profile.get("version", "")).lower():
            self._mcVersion = McVersion(version.split("-")[0])
            self._forgeVersion = version.replace(str(self._mcVersion), "").replace("-", "")
            return True
        elif "forge" in (version := self._profile.get("id", "")).lower():
            self._mcVersion = McVersion(version.split("-")[0])
            self._forgeVersion = version.replace(str(self._mcVersion), "").replace("-", "")
            return True
        else:
            return False

    def asyncInstall(self):
        """
        安装Forge
        若为1.17以上版本,则使用PlanB
        若为1.17以下版本,则使用PlanA

        若安装过程中出现错误,则抛出InstallerError
        """
        MCSL2Logger.debug(f"Forge 安装: {self.__class__.__name__}{self._mcVersion}")
        MCSL2Logger.debug(f"Forge 安装: {self.__class__.__name__}, {self._forgeVersion}")
        MCSL2Logger.debug(f"Forge 安装: {self.thread().currentThreadId()=}")
        if self.cancelled:
            self.installFinished.emit(False, "用户取消")
            return
        self.__asyncInstallRoutine()

    def __asyncInstallRoutine(self):
        self.__BeginInstallAsync()

    def __BeginInstallAsync(self):
        # set forge runtime java path
        if self.java is None:
            try:
                self.java = (
                    configureServerVariables.selectedJavaPath
                    if self.isEditing is None
                    else editServerVariables.selectedJavaPath
                )
            except IndexError:
                raise InstallerError("No Java path found")

        if self.cancelled:  # 如果取消了安装,则不创建QProcess安装进程
            self.installFinished.emit(False, "用户取消")
            return

        self._dlInfoQueue = queue.Queue()
        self.worker = ForgeInstallThread(
            self.file, self.cwd, self.java, detailed=True, dlInfoQueue=self._dlInfoQueue
        )
        self._dlInfoMonitor = InstallerDownloadsMonitor(self._dlInfoQueue)
        self._dlInfoMonitor.progressed.connect(self.downloadInfo.emit)

        self.worker.output.connect(
            lambda msg: self.installerLogOutput.emit(
                (
                    "ForgeInstaller::PlanB"
                    if self.installPlan == ForgeInstaller.InstallPlan.PlanB
                    else "ForgeInstaller::PlanA"
                )
                + ": "
                + msg
            )
        )

        self.worker.finished.connect(self.__EndInstallAsync)

        self._dlInfoMonitor.start()
        self.worker.start()

    def __EndInstallAsync(self, success: bool, message: str):
        self._cancelTimer: QTimer
        self._cancelTimer.stop()

        # safely quit dlInfoMonitor
        self._dlInfoQueue.put(None)
        self._dlInfoMonitor.quit()
        self._dlInfoMonitor.wait()
        self._dlInfoMonitor = None
        self._dlInfoQueue = None

        if success:
            # 1.17以上版本: PlanB
            if self.installPlan == ForgeInstaller.InstallPlan.PlanB:
                # 判断系统，分别读取run.bat和run.sh
                if osname == "nt":
                    with open(osp.join(self.cwd, "run.bat"), mode="r") as f:
                        run = f.readlines()
                else:
                    with open(osp.join(self.cwd, "run.sh"), mode="r") as f:
                        run = f.readlines()
                # 找到java命令
                try:
                    command = list(filter(lambda x: x.startswith("java"), run)).pop()
                except IndexError:
                    raise InstallerError("No java command found")

                # 构造forge启动参数
                try:
                    forgeArgs = list(
                        filter(lambda x: x.startswith("@libraries"), command.split(" "))
                    ).pop()
                except IndexError:
                    raise InstallerError("bad forge run script")

                forgeArgs = [forgeArgs]  # 转成列表，与下面相一致

            # 1.17以下版本: PlanA
            else:
                for entry in self._profile["libraries"]:
                    if entry["name"].startswith("net.minecraftforge:forge:"):
                        coreFile = entry["downloads"]["artifact"]["path"].replace("-universal", "")
                        forgeArgs = ["-jar", osp.basename(coreFile).strip()]
                        break
                if self.isEditing is None:
                    configureServerVariables.jvmArg.extend(forgeArgs)
                else:
                    editServerVariables.jvmArg.extend(forgeArgs)
            # 写入全局配置
            try:
                globalServerList = loads(readFile(r"MCSL2/MCSL2_ServerList.json"))
                d = globalServerList["MCSLServerList"][
                    (
                        len(globalServerList["MCSLServerList"]) - 1
                        if self.isEditing is None
                        else self.isEditing
                    )
                ]
                d["jvm_arg"].extend(forgeArgs)
                d.update({
                    "icon": "Anvil.png",
                    "server_type": "forge",
                })
                globalServerList["MCSLServerList"].pop(
                    -1 if self.isEditing is None else self.isEditing
                )
                globalServerList["MCSLServerList"].append(d)
                writeFile(
                    r"MCSL2/MCSL2_ServerList.json",
                    dumps(globalServerList, indent=4),
                )
            except Exception as e:
                raise e

            # 写入单独配置
            try:
                if not cfg.get(cfg.onlySaveGlobalServerConfig):
                    writeFile(
                        osp.join(self.cwd, "MCSL2ServerConfig.json"),
                        dumps(d, indent=4),
                    )
            except Exception as e:
                raise e

        self.installFinished.emit(success, message)
        self.worker.join()
        self.worker = None

    @classmethod
    def isPossibleForgeInstaller(cls, fileName: str) -> Optional[Tuple[McVersion, Any]]:
        """
        判断是否可能为Forge安装器
        若是,则返回一个元组,包含mcVersion和forgeVersion : # type:McVersion, str
        若不是,则返回None
        """
        if osp.getsize(fileName) > 10_000 * 1024:  # 若文件大于10MB,则几乎不可能是Forge安装器
            return None
        try:
            fileFile = ZipFile(fileName, mode="r")
        except BadZipFile:
            return None
        try:
            _profile = json.loads(fileFile.read("install_profile.json"))
        except Exception:
            return None

        # fmt: off
        if (versionInfo := _profile.get("versionInfo", {})).get("id", "").lower():
            _mcVersion = McVersion(versionInfo["id"].split("-")[0])
            _forgeVersion = versionInfo["id"].replace(str(_mcVersion), "").replace("-", "")
            return _mcVersion, _forgeVersion

        elif "forge" in (version := _profile.get("version", "")).lower():
            _mcVersion = McVersion(version.split("-")[0])
            _forgeVersion = version.replace(str(_mcVersion), "").replace("-", "")
            return _mcVersion, _forgeVersion

        elif "forge" in (version := _profile.get("id", "")).lower():
            _mcVersion = McVersion(version.split("-")[0])
            _forgeVersion = version.replace(str(_mcVersion), "").replace("-", "")
            return _mcVersion, _forgeVersion

        else:
            return None
        # fmt: on

    def cancelInstall(self, cancelled=False):
        super().cancelInstall(cancelled)
        if self.worker is not None:
            self.worker.cancel()

    @property
    def forgeVersion(self):
        return self._forgeVersion

    @property
    def mcVersion(self):
        return self._mcVersion


class FabricInstaller(Installer):
    downloadServerProgress = pyqtSignal(str)
    downloadServerFinished = pyqtSignal(bool)

    class InstallPlan(Enum):
        PlanA = 0
        PlanB = 1

    def __init__(
        self,
        serverPath,
        file,
        java=None,
        installerPath=None,
        logDecode="utf-8",
    ):
        super().__init__(serverPath, file, logDecode)
        self.java = java
        self.serverPath = serverPath

        self._properties = {}
        self._McVersion = None
        self._fabricVersion = None
        self._bmclapiDownloader = None
        self._serverJarTargetPath = ""
        self._serverJarFileName = ""

        self.getInstallerData(
            osp.join(serverPath, file) if installerPath is None else installerPath
        )

    def getInstallerData(self, jarFile):
        # 打开Installer压缩包

        with ZipFile(
            jarFile,
            mode="r",
        ) as zipfile:
            try:
                props = str(zipfile.read("install.properties")).split("\n")
            except KeyError:
                raise InstallerError("Invalid Fabric installer")
        for prop in props:
            k, v = prop.split("=")
            self._properties[k] = v
        self._McVersion = McVersion(self._properties.get("game-version", "0.0.0"))
        self._fabricVersion = self._properties.get("fabric-loader-version", "UNKNOWN")

    def asyncInstall(self):
        # 预下载核心并安装...
        self._bmclapiDownloader = BMCLAPIDownloader()
        self._bmclapiDownloader.downloadProgress.connect(self.onServerDownloadProgress)
        self._bmclapiDownloader.downloadFinished.connect(self.onServerDownloadFinished)
        self._bmclapiDownloader.download(
            self._McVersion,
            osp.join(self.cwd, ".fabric", "server"),
            self._McVersion + "-server.jar",
        )

    def onServerDownloadProgress(self, bytesReceived, bytesTotal):
        percent = bytesReceived * 100 / bytesTotal
        MCSL2Logger.info(f"(正在下载核心... {percent:.0f}%) 使用 BMCLAPI 下载")
        self.downloadServerProgress.emit(
            self.tr("(正在下载核心... {:.0f}%) 使用 BMCLAPI 下载").format(percent)
        )

    def onServerDownloadFinished(self, success: bool):
        self.downloadServerFinished.emit(success)
        self._bmclapiDownloader.deleteLater()
        self._bmclapiDownloader = None
        self.installFinished.emit(success, "" if success else "下载核心失败")

    @classmethod
    def isPossibleFabricInstaller(cls, fileName: str) -> Optional[Tuple[McVersion, Any]]:
        """
        判断是否可能为Fabric安装器
        若是,则返回一个元组,包含mcVersion和fabricVersion : # type:McVersion, str
        若不是,则返回None
        """
        with ZipFile(fileName, mode="r") as fileFile:
            try:
                props = str(fileFile.read("install.properties")).split("\n")
            except KeyError:
                return None
        properties = {}
        for prop in props:
            k, v = prop.split("=")
            properties[k] = v
        if properties.get("game-version", "").lower():
            _mcVersion = McVersion(properties["game-version"])
            _fabricVersion = properties["fabric-loader-version"]
            return _mcVersion, _fabricVersion

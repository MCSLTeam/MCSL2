from json import loads, dumps
from os import path as ospath, name as osname
from typing import Optional
from zipfile import ZipFile
from PyQt5.QtCore import QProcess, QObject, pyqtSignal
from MCSL2Lib.publicFunctions import warning
from MCSL2Lib.variables import ConfigureServerVariables
from MCSL2Lib.Controllers.settingsController import SettingsController

configureServerVariables = ConfigureServerVariables()
settingsController = SettingsController()


class InstallerError(Exception):
    pass


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

    installFinished = pyqtSignal(bool)
    installerLogOutput = pyqtSignal(str)

    def __init__(self, cwd: str, file: str, logDecode="utf-8"):
        """
        :param cwd: The current working directory of the installer
        :param file: The name of the installer
        """
        super().__init__()
        self.cwd = cwd
        self.file = file
        self.logDecode = logDecode
        self.workingProcess: Optional[QProcess] = None
        self.logPartialData = b""
        self.installerLogOutput.connect(print)

    def install(self):
        raise NotImplementedError

    def _installerLogHandler(self, prefix: str = ""):
        newData = self.workingProcess.readAllStandardOutput().data()
        self.logPartialData += newData  # Append the incoming data to the buffer
        lines = self.logPartialData.split(b"\n")  # Split the buffer into lines
        self.partialData = (
            lines.pop()
        )  # The last element might be incomplete, so keep it in the buffer

        for line in lines:
            newOutput = line.decode(self.logDecode, errors="replace")
            self.installerLogOutput.emit(">>".join([prefix, newOutput]))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.workingProcess is not None:
            self.workingProcess.kill()
            self.workingProcess = None


class ForgeInstaller(Installer):
    def __init__(self, cwd, file, java=None, logDecode="utf-8"):
        super().__init__(cwd, file, logDecode)
        self.version = None
        self.mcVersion = None
        # self.forgeVersion = None
        self.java = java
        # copyfile(
        #     configureServerVariables.corePath,
        #     f"./Servers/{configureServerVariables.serverName}/{configureServerVariables.coreFileName}",
        # )
        # self.checkCopyThread = CopyCheckThread(
        #     f1=configureServerVariables.corePath,
        #     f2=f"./Servers/{configureServerVariables.serverName}/{configureServerVariables.coreFileName}",
        #     parent=self,
        # )
        # self.checkCopyThread.fileFinished.connect(self.getInstallerData)
        # self.checkCopyThread.start()

    #     self.getInstallerData()

    # def getInstallerData(self):
    #     # 打开Installer压缩包
    #     # 读取version.json
    #     zipfile = ZipFile(
    #         f"./Servers/{configureServerVariables.serverName}/{configureServerVariables.coreFileName}",
    #         mode="r",
    #     )
    #     _ = zipfile.read("install_profile.json")
    #     self._profile = loads(_)
    #     zipfile.close()

    # def checkInstaller(self):
    #     if (
    #         (versionInfo := self._profile.get("versionInfo", {}))
    #         .get("id", "")
    #         .startswith("forge")
    #     ):
    #         self.mcVersion = McVersion(versionInfo["id"].split("-")[0])
    #         self.forgeVersion = (
    #             versionInfo["id"].replace((self.mcVersion), "").replace("-", "")
    #         )
    #         canInstall = 1
    #     elif "forge" in (version := self._profile.get("version", "")):
    #         self.mcVersion = McVersion(version.split("-")[0])
    #         self.forgeVersion = version.replace(str(self.mcVersion), "").replace(
    #             "-", ""
    #         )
    #         canInstall = 1
    #     else:
    #         canInstall = 0
    #         raise InstallerError("Invalid forge installer")
    #     if canInstall:
    #         self.install()

    @warning("该方法还未完善,目前仅支持1.12以上的Forge安装,且还未测试")
    def install(self):
        """
        安装Forge
        若为1.12以上版本,则使用PlanB
        若为1.12以下版本,则使用PlanA

        若安装过程中出现错误,则抛出InstallerError
        """
        self.mcVersion = McVersion(configureServerVariables.extraData["forge_version"])
        if self.mcVersion >= McVersion("1.12"):
            self._installPlanB()
        else:
            self._installPlanA()

    def _installPlanB(self, installed=False):
        """
        安装1.12版本及以上的Forge
        """
        if not installed:
            # set forge runtime java path
            if self.java is None:
                try:
                    self.java = configureServerVariables.javaPath[0]
                except IndexError:
                    raise InstallerError("No Java path found")

            process = QProcess()
            process.setWorkingDirectory(self.cwd)
            process.setProgram(self.java)
            process.setArguments(["-jar", self.file, "--installServer"])
            process.readyReadStandardOutput.connect(
                lambda: self._installerLogHandler("ForgeInstaller::PlanB")
            )
            process.finished.connect(lambda a, b: self._installPlanB(True))
            self.workingProcess = process
            self.workingProcess.start()
        else:
            if self.workingProcess.exitCode() == 0:
                # 判断系统，分别读取run.bat和run.sh
                if osname == "nt":
                    with open(ospath.join(self.cwd, "run.bat"), mode="r") as f:
                        run = f.readlines()
                else:
                    with open(ospath.join(self.cwd, "run.sh"), mode="r") as f:
                        run = f.readlines()
                # 找到java命令
                try:
                    command = list(filter(lambda x: x.startswith("java"), run)).pop()
                except IndexError:
                    raise InstallerError("No java command found")

                try:
                    forgeArgs = list(
                        filter(lambda x: x.startswith("@libraries"), command.split(" "))
                    ).pop()
                except IndexError:
                    raise InstallerError("bad forge run script")

                configureServerVariables.jvmArg.append(forgeArgs)
                # configureServerVariables.extraData["forge_version"] = self.forgeVersion
                # 写入全局配置
                try:
                    with open(
                        r"MCSL2/MCSL2_ServerList.json", "r", encoding="utf-8"
                    ) as globalServerListFile:
                        # old
                        globalServerList = loads(globalServerListFile.read())
                    d = globalServerList["MCSLServerList"][
                        len(globalServerList["MCSLServerList"]) - 1
                    ]
                    print(d)
                    d["jvmArg"].append(forgeArgs)
                    d.update(
                        {
                            "server_type": "forge",
                            # "extra_data": {
                            #     "forge_version": self.forgeVersion,
                            # },
                        }
                    )
                    globalServerList["MCSLServerList"].pop(-1)
                    globalServerList["MCSLServerList"].append(d)
                    with open(
                        r"MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
                    ) as newGlobalServerListFile:
                        newGlobalServerListFile.write(dumps(globalServerList, indent=4))
                except Exception as e:
                    raise e

                # 写入单独配置
                try:
                    if not settingsController.fileSettings[
                        "onlySaveGlobalServerConfig"
                    ]:
                        with open(
                            ospath.join(self.cwd, "MCSL2ServerConfig.json"),
                            mode="w+",
                            encoding="utf-8",
                        ) as f:
                            f.write(dumps(d, indent=4))
                except Exception as e:
                    raise e

                self.installFinished.emit(True)
            else:
                self.installFinished.emit(False)
                raise InstallerError(
                    f"Forge installer exited with code {self.workingProcess.exitCode()}"
                )

    def _installPlanA(self):
        """
        安装1.12版本以下的Forge
        """
        pass

    @classmethod
    def isPossibleForgeInstaller(cls, fileName: str) -> bool:
        """
        判断是否可能为Forge安装器
        """
        fileFile = ZipFile(fileName, mode="r")
        try:
            _profile = fileFile.read("install_profile.json")
        except:
            return False
        if "forge" not in loads(_profile).get("versionInfo", {}).get("id"):
            return False
        return True


# class CopyCheckThread(QThread):
#     fileFinished = pyqtSignal()

#     def __init__(self, f1, f2, parent=None):
#         super().__init__(parent)
#         self.f1 = f1
#         self.f2 = f2
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.checkFile)
#         self.timer.start(800)

#     def checkFile(self):
#         print(self.f1, ospath.getsize(self.f1), self.f2, ospath.getsize(self.f2))
#         if ospath.getsize(self.f1) == ospath.getsize(self.f2):
#             self.timer.timeout.disconnect()
#             self.fileFinished.emit()
#             self.terminate()

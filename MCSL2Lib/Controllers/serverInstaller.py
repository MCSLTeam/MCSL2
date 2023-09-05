import os.path
import shutil
import sys
from json import loads, dumps
from os import path as ospath, name as osname
from typing import Optional
from zipfile import ZipFile

from PyQt5.QtCore import QProcess, QObject, pyqtSignal

from MCSL2Lib.Controllers.settingsController import SettingsController
from MCSL2Lib.variables import ConfigureServerVariables

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

    def asyncInstall(self):
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
    def __init__(self, serverPath, file, java=None, installerPath=None, logDecode="utf-8"):
        super().__init__(serverPath, file, logDecode)
        self._profile = None
        self.version = None
        self._mcVersion = None
        self._forgeVersion = None
        self.java = java
        self.serverPath = serverPath
        self.installPlan = 0

        self.getInstallerData(os.path.join(serverPath, file) if installerPath is None else installerPath)
        if self._mcVersion >= McVersion("1.17"):
            self.installPlan = 1
        elif self._mcVersion >= McVersion("1.8"):
            self.installPlan = 0
        else:
            raise InstallerError(f"不支持的自动安装版本:{self._mcVersion}的forge\nMCSL2支持1.8往后的所有forge安装")

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
        if (versionInfo := self._profile.get("versionInfo", {})).get("id", "").lower().startswith("forge"):
            self._mcVersion = McVersion(versionInfo["id"].split("-")[0])
            self._forgeVersion = (
                versionInfo["id"].replace((self._mcVersion), "").replace("-", "")
            )
            return True
        elif "forge" in (version := self._profile.get("version", "")).lower():
            self._mcVersion = McVersion(version.split("-")[0])
            self._forgeVersion = version.replace(str(self._mcVersion), "").replace(
                "-", ""
            )
            return True
        elif "forge" in (version := self._profile.get("id", "")).lower():
            self._mcVersion = McVersion(version.split("-")[0])
            self._forgeVersion = version.replace(str(self._mcVersion), "").replace(
                "-", ""
            )
            return True
        else:
            return False

    def asyncInstall(self, installed=False):
        """
        安装Forge
        若为1.17以上版本,则使用PlanB
        若为1.17以下版本,则使用PlanA

        若安装过程中出现错误,则抛出InstallerError
        """
        print(self.__class__.__name__, self._mcVersion)
        print(self.__class__.__name__, self._forgeVersion)

        if not installed:
            # set forge runtime java path
            if self.java is None:
                try:
                    self.java = configureServerVariables.javaPath[0]
                except IndexError:
                    raise InstallerError("No Java path found")
            # copy tmp file of forge installer
            shutil.copyfile(
                ospath.join(self.cwd, self.file),
                ospath.join(self.cwd, self.file + ".tmp"),
            )

            process = QProcess()
            process.setWorkingDirectory(self.cwd)
            process.setProgram(self.java)
            process.setArguments(["-jar", self.file + ".tmp", "--installServer"])
            process.readyReadStandardOutput.connect(
                lambda: self._installerLogHandler(
                    "ForgeInstaller::PlanB" if self.installPlan == 1 else "ForgeInstaller::PlanA"
                )
            )
            process.finished.connect(lambda a, b: self.asyncInstall(True))
            self.workingProcess = process
            self.workingProcess.start()

        else:
            print("PlanB::forge installed callback entered")
            # 删除tmp
            os.remove(ospath.join(self.cwd, self.file + ".tmp"))

            if self.workingProcess.exitCode() == 0:

                if self.installPlan == 1:  # 1.17以上版本: PlanB

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

                    # 构造forge启动参数
                    try:
                        forgeArgs = list(
                            filter(lambda x: x.startswith("@libraries"), command.split(" "))
                        ).pop()
                    except IndexError:
                        raise InstallerError("bad forge run script")
                    
                    forgeArgs = [forgeArgs] # 转成列表，与下面相一致

                else:  # 1.17以下版本: PlanA
                    for entry in self._profile["libraries"]:
                        if entry["name"].startswith("net.minecraftforge:forge:"):
                            coreFile = entry["downloads"]["artifact"]["path"].replace("-universal", "")
                            forgeArgs = ["-jar", ospath.basename(coreFile).strip()]
                            break
                    configureServerVariables.jvmArg.extend(forgeArgs)
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
                    d["jvm_arg"].extend(forgeArgs)
                    d.update(
                        {
                            "server_type": "forge",
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
                sys.setprofile(lambda *args, **kwargs: None)
                raise InstallerError(
                    f"Forge installer exited with code {self.workingProcess.exitCode()}"
                )

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

    @property
    def forgeVersion(self):
        return self._forgeVersion

    @property
    def mcVersion(self):
        return self._mcVersion

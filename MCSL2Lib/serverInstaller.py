import json
import os.path
from typing import Optional
from zipfile import ZipFile

from PyQt5.QtCore import QProcess, QObject, pyqtSignal

from MCSL2Lib.publicFunctions import warning
from MCSL2Lib.variables import ConfigureServerVariables, ServerVariables


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
    """
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

    def install(self):
        raise NotImplementedError

    def _installerLogHandler(self):
        newData = self.workingProcess.readAllStandardOutput().data()
        self.logPartialData += newData  # Append the incoming data to the buffer
        lines = self.logPartialData.split(b"\n")  # Split the buffer into lines
        self.partialData = (
            lines.pop()
        )  # The last element might be incomplete, so keep it in the buffer

        for line in lines:
            newOutput = line.decode(self.logDecode, errors="replace")
            self.installerLogOutput.emit(newOutput)


class ForgeInstaller(Installer):
    def __init__(self, cwd, file, java=None, logDecode="utf-8"):
        super().__init__(cwd, file, logDecode)
        self.version = None
        self.mcVersion = None
        self.forgeVersion = None
        self.java = java
        self.getInstallerData()

    def getInstallerData(self):
        # 打开Installer压缩包
        # 读取version.json
        zipfile = ZipFile(os.path.join(self.cwd,self.file), mode="r")
        versionJson = zipfile.read("version.json")
        versionInfo = json.loads(versionJson)
        self.mcVersion = McVersion(versionInfo["inheritsFrom"])
        self.forgeVersion = versionInfo["id"]

    @warning("该方法还未完善,目前仅支持1.13以上的Forge安装,且还未测试")
    def install(self):
        """
        安装Forge
        若为1.13以上版本,则使用PlanB
        若为1.13以下版本,则使用PlanA
        
        若安装过程中出现错误,则抛出InstallerError
        """
        if self.mcVersion >= McVersion("1.13"):
            self._installPlanB()
        else:
            self._installPlanA()

    def _installPlanB(self, installed=False):
        """
        安装1.13版本以上的Forge
        """
        if not installed:
            var = ConfigureServerVariables()

            # set forge runtime java path
            if self.java is None:
                try:
                    self.java = var.javaPath[0]
                except IndexError:
                    raise InstallerError("No Java path found")

            process = QProcess()
            process.setWorkingDirectory(self.cwd)
            process.setProgram(self.java)
            process.setArguments(["-jar", self.file, "--installServer"])
            process.readyReadStandardOutput.connect(self._installerLogHandler)
            process.finished.connect(lambda a, b: self._installPlanB(True))
            self.workingProcess = process
            self.workingProcess.start()
        else:
            if self.workingProcess.exitCode() == 0:
                # 生成eula.txt
                with open(os.path.join(self.cwd, "eula.txt"), mode="w") as f:
                    f.write("eula=true")

                # 判断系统，分别读取run.bat和run.sh
                if os.name == "nt":
                    with open(os.path.join(self.cwd, "run.bat"), mode="r") as f:
                        run = f.readlines()
                else:
                    with open(os.path.join(self.cwd, "run.sh"), mode="r") as f:
                        run = f.readlines()
                # 找到java命令
                try:
                    command = list(filter(lambda x: x.startswith("java"), run)).pop()
                except IndexError:
                    raise InstallerError("No java command found")

                try:
                    forgeArgs = list(filter(lambda x: x.startswith("@libraries"), command.split(" "))).pop()
                except IndexError:
                    raise InstallerError("bad forge run script")

                # 更新serverVariables的信息
                var = ServerVariables()
                var.jvmArg.append(forgeArgs)
                var.serverType = "forge"
                var.extraData["forge_version"] = self.forgeVersion
                # 保存json
                if p := os.path.exists(os.path.join(self.cwd, "MCSL2ServerConfig.json")):
                    with open(p, mode="r", encoding="utf-8") as f:
                        d = json.load(f)
                        d["jvmArg"].append(forgeArgs)
                    d.update({
                        "server_type": "forge",
                        "extra_data": {
                            "forge_version": self.forgeVersion,
                        }
                    })
                    with open(p, mode="w", encoding="utf-8") as f:
                        json.dump(d, f, ensure_ascii=False, indent=4, sort_keys=True)
                else:
                    raise InstallerError("MCSL2ServerConfig.json not found,failed to save forge launch args")
            else:
                raise InstallerError(f"Forge installer exited with code {self.workingProcess.exitCode()}")

    def _installPlanA(self):
        """
        安装1.13版本以下的Forge
        """
        pass

import tempfile
import traceback
from pathlib import Path
from typing import List, Set, Dict, Optional

from .progress_callback import ProgressCallback
from ..download_utils import DownloadUtils
from ..java2python import Supplier
from ..json.artifact import Artifact
from ..json.install import Processor
from ..json.installV1 import InstallV1
from ..json.util import Util
from ..json.version import Library


class PostProcessors:
    profile: InstallV1
    isClient: bool
    monitor: ProgressCallback
    hasTasks: bool = False
    processors: List[Processor]

    class __DataEntry(Supplier[str]):
        value: str

        def __init__(self, value: str):
            super().__init__(self)
            self.value = value

        def __str__(self):
            return self.value

        def get(self):
            return self.value

    class __ArtifactEntry(__DataEntry):
        artifact: Artifact

        def __init__(self, artifact: Artifact, root: Path):
            super().__init__(str(artifact.getLocalPath(root).absolute()))
            self.artifact = artifact

    class __FileEntry(__DataEntry):
        file: Path

        def __init__(self, file: Path):
            super().__init__(str(file.absolute()))
            self.file = file

    class __Output:
        file: Path
        sha1: str

        def __init__(self, file: Path, sha1: str):
            self.file = file
            self.sha1 = sha1

    def __init__(self, profile: InstallV1, isClient: bool, monitor: ProgressCallback):
        self.profile = profile
        self.isClient = isClient
        self.monitor = monitor
        self.processors = profile.getProcessors("client" if isClient else "server")
        self.hasTasks = len(self.processors) > 0

    def getLibraries(self) -> List[Library]:
        return self.profile.getLibraries() if self.hasTasks else []

    def getTaskCount(self) -> int:
        return (
            0
            if self.hasTasks
            else len(self.profile.getLibraries())
            + len(self.processors)
            + len(self.profile.getData(self.isClient))
        )

    def process(
        self, librariesDir: Path, minecraft: Path, root: Path, installer: Path
    ) -> Optional[Set[Path]]:
        data = self.__loadData(librariesDir)
        if data is None:
            return None
        data.update({
            "SIDE": PostProcessors.__DataEntry("client" if self.isClient else "server"),
            "MINECRAFT_JAR": PostProcessors.__FileEntry(minecraft),
            "MINECRAFT_VERSION": PostProcessors.__DataEntry(self.profile.getMinecraft()),
            "ROOT": PostProcessors.__FileEntry(root),
            "INSTALLER": PostProcessors.__FileEntry(installer),
            "LIBRARY_DIR": PostProcessors.__FileEntry(librariesDir),
        })

        if len(self.processors) == 1:
            self.monitor.stage("Building Processor")
        else:
            self.monitor.stage("Building Processors")

        allOutputs = self.buildOutputs(librariesDir, data)
        if allOutputs is None:
            return None

        libPrefix = librariesDir.absolute()

        rv = set()
        for x in range(len(self.processors)):
            self.monitor.progress((x + 1), len(self.processors))
            self.monitor.message("")
            self.log(
                "==============================================================================="
            )
            proc = self.processors[x]
            outputs = allOutputs[x]

            if len(outputs) > 0:
                miss = True
                self.log("  Cache: ")
                for output in outputs:
                    if not output.file.exists():
                        self.log(f"    {output.file} Missing")
                        miss = False

                        if not (outputFile := str(output.file.absolute())).startswith(
                            str(libPrefix)
                        ):
                            miss = True
                        else:
                            suffix = outputFile[len(str(libPrefix)) :].replace("\\", "/")
                            if suffix.startswith("/"):
                                suffix = suffix[1:]

                            relative = f"./cache/{suffix}"

                            inputPath = Path(relative)
                            if not inputPath.exists():
                                miss = True
                            else:
                                try:
                                    input_ = inputPath.read_bytes()

                                    self.log("    Extracting output from " + relative)
                                    if not (parent := output.file.parent).exists():
                                        parent.mkdir(parents=True)

                                    with open(str(output.file.absolute()), "wb") as fileOutput:
                                        fileOutput.write(input_)
                                    sha1 = DownloadUtils.getSha1(output.file)
                                    if sha1 == output.sha1:
                                        self.log("      Extraction completed: Checksum validated.")
                                        rv.add(output.file)
                                    else:
                                        self.log(f"    {output.file}")
                                        self.log("      Expected: " + output.sha1)
                                        self.log("      Actual:   " + sha1)
                                        miss = True
                                        output.file.unlink(missing_ok=True)
                                except IOError:
                                    traceback.print_exc()
                                    return None

                    else:
                        sha_ = DownloadUtils.getSha1(output.file)
                        if sha_ == output.sha1:
                            self.log(f"    {output.file} Validated: {output.sha1}")
                            rv.add(output.file)
                        else:
                            self.log(f"    {output.file}")
                            self.log("      Expected: " + output.sha1)
                            self.log("      Actual:   " + sha_)
                            miss = True
                            output.file.unlink(missing_ok=True)

                if not miss:
                    self.log("  Cache Hit!")
                    continue

            jar = proc.getJar().getLocalPath(librariesDir)
            if not jar.exists() or not jar.is_file():
                self.error(f"  Missing Jar for processor: {jar.absolute()}")
                return None

            # Locate main class in jar file
            mainClass = DownloadUtils.getMainClass(jar)
            if not mainClass:  # mainClass is not None or !=""
                self.error(f"  Jar does not have main class: {jar.absolute()}")
                return None
            self.monitor.message(f"  MainClass: {mainClass}")

            classpath: List[Path] = []
            err = ""
            self.monitor.message("  Classpath:")
            self.monitor.message(f"    {jar.absolute()}")
            classpath.append(jar)
            for dep in proc.getClasspath():
                lib = dep.getLocalPath(librariesDir)
                if not lib.exists() and lib.is_file():
                    err += f"\n  {dep.getDescriptor()}"
                    classpath.append(lib)
                self.monitor.message(f"    {lib.absolute()}")

            if err:
                self.error(f"  Missing Processor Dependencies: {err}")
                return

            args = []
            for arg in proc.getArgs():
                if arg.startswith("[") and arg.endswith("]"):  # Library
                    artifact = Artifact.from_(arg[1:-1])
                    args.append(artifact.getLocalPath(librariesDir).absolute())
                else:
                    args.append(Util.replaceTokens(data, arg))
            if err:
                self.error(f"  Missing Processor data values: {err}")
                return None
            # monitor.message("  Args: " + args.stream().map(a -> a.indexOf(' ') != -1 || a.indexOf(',') != -1 ? '"' + a + '"' : a).collect(Collectors.joining(", ")));  # noqa: E501
            self.monitor.message(
                "  Args: "
                + str([
                    a if a.indexOf(" ") != -1 or a.indexOf(",") != -1 else f'"{a}"' for a in args
                ])
            )
            # TODO: continue translate PostProcessors.java:210

    def __loadData(self, librariesDir: Path) -> Optional[Dict[str, __DataEntry]]:
        """
        :raise IOError
        """

        cfg = self.profile.getData(self.isClient)
        if len(cfg) == 0:
            return {}

        rv = {}
        err = ""

        # Path temp  = Files.createTempDirectory("forge_installer");
        temp = Path(tempfile.mkdtemp("forge_installer"))
        self.monitor.start(f"Created Temporary Directory: {temp}")

        steps = len(cfg)
        progress = 1

        for key, value in cfg.items():
            self.monitor.progress(progress / steps)
            progress += 1

            if value.startswith("[") and value.endswith("]"):  # Artifact
                artifact = Artifact.from_(value[1:-1])
                entry = PostProcessors.__ArtifactEntry(artifact, librariesDir)
            elif value.startswith("'") and value.endswith("'"):  # Literal
                entry = PostProcessors.__DataEntry(value[1:-1])
            else:
                target = temp / value
                self.monitor.message(f"Extracting {value} to {target}")
                if not DownloadUtils.extractFile(value, target):
                    err += "\n  "
                    err += value
                entry = PostProcessors.__FileEntry(target)

            rv[key] = entry

        if err:
            self.error(f"Failed to extract files from archive: {err}")
            return None

        return rv

    def buildOutputs(self, librariesDir, data):
        rv: List[List[PostProcessors.__Output]] = []

        for proc in self.processors:
            outputs = proc.getOutputs()
            if len(outputs) == 0:
                rv.append([])
                continue

            pout: List[PostProcessors.__Output] = []
            for key in outputs.keys():
                file: str
                if key.startswith("[") and key.endswith("]"):  # Artifact
                    file = str(Artifact.from_(key[1:-1]).getLocalPath(librariesDir).absolute())
                else:
                    file = Util.replaceTokens(data, key)

                value = outputs.get(key)
                if value is not None:
                    value = Util.replaceTokens(data, value)

                if key is None or value is None:
                    self.error(f"  Invalid configuration, bad output config: [{key}: {value}]")
                    return None

                pout.append(PostProcessors.__Output(Path(file), value))

            rv.append(pout)

        return rv

    def log(self, msg: str): ...

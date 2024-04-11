import subprocess
import traceback
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Dict, List

from .action import Action, ActionCanceledException
from .progress_callback import ProgressCallback
from ..download_utils import DownloadUtils
from ..java2python import Supplier
from ..json.installV1 import InstallV1
from ..json.util import Util
from ..json.version import Version


class ServerInstall(Action):
    def __init__(self, profile: InstallV1, installer: Path, monitor: ProgressCallback):
        super().__init__(profile, monitor, installer, False)
        self.grabbed = []

    def run(self, target: Path) -> bool:
        try:

            if target.exists() and not target.is_dir():
                self.monitor.error("There is a file at this location, the server cannot be installed here!")
                return False

            librariesDir = Path(target).joinpath("libraries")
            if not target.exists():
                target.mkdir(parents=True, exist_ok=True)
            librariesDir.mkdir(parents=True, exist_ok=True)
            # self.checkCancel()

            # Extract main executable jar
            contained = self.profile.getPath()
            if contained is not None:
                self.monitor.stage("Extracting main jar:")
                if not DownloadUtils.extractFile(contained, self.installerDataBuf, target / contained.getFilename()):
                    self.monitor.error(f"  Failed to extract main jar: {contained.getFilename()}")
                    return False
                else:
                    self.monitor.stage("  Extracted successfully")
            # self.checkCancel()

            # Download MC Server jar
            self.monitor.stage("Considering minecraft server jar")
            tokens: Dict[str, Supplier[str]] = {
                "ROOT": Supplier.of(lambda: str(target.absolute())),
                "MINECRAFT_VERSION": Supplier.of(self.profile.getMinecraft),
                "LIBRARY_DIR": Supplier.of(lambda: str(librariesDir.absolute()))
            }

            path = Util.replaceTokens(tokens, self.profile.getServerJarPath())
            serverTarget = Path(path)

            if not self.downloadVanilla(serverTarget, self.installerDataBuf, "server"):
                self.error("Failed to download minecraft server jar")
                return False

            # self.checkCancel()

            # Download Libraries
            libDirs = []
            mcLibDir = self.installer.parent / "libraries"
            if mcLibDir.exists():
                libDirs.append(mcLibDir)

            if not self.downloadLibraries(librariesDir, self.installerDataBuf, libDirs):
                return False
        except ActionCanceledException:
            self.monitor.stage("Cancelled")
            return False

        ret = self.offlineInstall(self.installer)
        if ret != 0:
            self.error(f"Failed to install server: installer return code: {ret}")
            return False
        return True

    def offlineInstall(self, installer: Path, java: Path = None) -> int:
        javaPath = java or "java"
        return subprocess.run(
            f"{javaPath} -jar {installer.absolute()} --offline --installServer",
            cwd=str(self.installer.parent),
            shell=True
        ).returncode

    def downloadVanilla(self, target: Path, installerDataBuf: BytesIO, side: str):
        if not target.exists():
            parent = target.parent
            if not parent.exists():
                parent.mkdir(parents=True)

            res = "cache/vanilla/" + side + ".jar"
            with zipfile.ZipFile(installerDataBuf, "r") as installer:
                try:
                    target.write_bytes(installer.read(res))
                except KeyError:
                    pass
                except Exception as e:
                    traceback.print_exc()
                    self.error("Failed to download version manifest, can not find " + side + " jar URL.")
                    return False

            vanilla = Util.getVanillaVersion(self.profile.getMinecraft())
            if vanilla is None:
                self.error("Failed to download version manifest, can not find " + side + " jar URL.")
                return False

            dl = vanilla.getDownload(side)
            if dl is None:
                self.error("Failed to download minecraft " + side + " jar, info missing from manifest")
                return False

            if not DownloadUtils.download(self.monitor, self.profile.getMirror(), dl, target):
                target.unlink(missing_ok=True)
                self.error(
                    "Downloading minecraft " + side + " failed, invalid checksum.\n" + \
                    "Try again, or manually place server jar to skip download."
                )
                return False

        return True

    def downloadLibraries(self, librariesDir: Path, installerDataBuf: BytesIO, additionalLibDirs: List[Path]):
        self.monitor.start("Downloading libraries")
        self.monitor.message(f"Found {len(additionalLibDirs)} additional library directories")

        libraries = self.getLibraries()
        bad = ""
        for lib in libraries:  # TODO:Async Download
            # self.checkCancel()
            if not DownloadUtils.downloadLibrary(
                    self.monitor,
                    self.profile.getMirror(),
                    lib,
                    librariesDir,
                    installerDataBuf,
                    self.grabbed,
                    additionalLibDirs
            ):
                download = None if lib.getDownloads() is None else lib.getDownloads().getArtifact()
                if download is not None and download.url != '':
                    bad += f"\n{lib.getName()}"
        if bad != '':
            self.error(f"Failed to download libraries:\n{bad}")
            return False
        return True

    def getLibraries(self) -> List[Version.Library]:
        libraries = []
        for lib in self.version.getLibraries():
            libraries.append(lib)
        for lib in self.processors.getLibraries():
            libraries.append(lib)
        return libraries

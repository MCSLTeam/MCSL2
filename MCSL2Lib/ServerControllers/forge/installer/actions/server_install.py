import asyncio
import functools
import subprocess
import traceback
import zipfile
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Deque, Optional, Sequence

import requests

from .action import Action, ActionCanceledException
from .progress_callback import ProgressCallback
from .. import bmclapi
from ..download_utils import DownloadUtils
from ..java2python import Supplier
from ..json.artifact import Artifact
from ..json.installV1 import InstallV1
from ..json.mirror import Mirror
from ..json.util import Util
from ..json.version import Version


class ServerInstall(Action):
    def __init__(self, profile: InstallV1, installer: Path, monitor: ProgressCallback):
        super().__init__(profile, monitor, installer, False)
        self.grabbed = deque()  # thread-safe

    async def run(self, target: Path, java: Path = None) -> bool:
        try:
            if target.exists() and not target.is_dir():
                self.monitor.error(
                    "There is a file at this location, the server cannot be installed here!"
                )
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
                if not DownloadUtils.extractFile(
                        contained, self.installerDataBuf, target / contained.getFilename()
                ):
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
                "LIBRARY_DIR": Supplier.of(lambda: str(librariesDir.absolute())),
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

            if not await self.downloadLibraries(librariesDir, self.installerDataBuf, libDirs):
                return False
        except ActionCanceledException:
            self.monitor.stage("Cancelled")
            return False

        self.monitor.stage("Installing server, please wait ...")
        ret = self.offlineInstall(self.installer, java)
        if ret != 0:
            self.error(f"Failed to install server: installer return code: {ret}")
            return False
        return True

    def offlineInstall(self, installer: Path, java: Path = None) -> int:
        javaPath = java or "java"
        jvmArgs = f"{javaPath} -jar {installer.absolute()} --offline --installServer"
        print(jvmArgs, self.installer.parent)
        return subprocess.run(
            jvmArgs,
            cwd=str(self.installer.parent),
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
                except Exception:
                    traceback.print_exc()
                    self.error(
                        "Failed to download version manifest, can not find " + side + " jar URL."
                    )
                    return False

            vanilla = Util.getVanillaVersion(self.profile.getMinecraft())
            if vanilla is None:
                self.error(
                    "Failed to download version manifest, can not find " + side + " jar URL."
                )
                return False

            # dl = vanilla.getDownload(side)
            dl = bmclapi.getMinecraftDownload(vanilla, side)
            if dl is None:
                self.error(
                    "Failed to download minecraft " + side + " jar, info missing from manifest"
                )
                return False

            if not DownloadUtils.download(self.monitor, self.profile.getMirror(), dl, target):
                target.unlink(missing_ok=True)
                self.error(
                    "Downloading minecraft "
                    + side
                    + " failed, invalid checksum.\n"
                    + "Try again, or manually place server jar to skip download."
                )
                return False

        return True

    async def downloadLibraries(
            self, librariesDir: Path, installerDataBuf: BytesIO, additionalLibDirs: List[Path], retry: int = 3
    ):
        from ..simple_installer import SimpleInstaller
        self.monitor.start("Downloading libraries")
        bad = await self._downloadLibraries(
            librariesDir,
            installerDataBuf,
            additionalLibDirs,
            self.getLibraries(),
            SimpleInstaller.LIBRARIES_MAX_CONCURRENT
        )

        if not bad:
            self.monitor.message("All libraries downloaded successfully")
            return True

        for i in range(1, retry + 1):
            print("\n /////////////////////////////////////////////////////////////////// \n")
            self.monitor.message(f"Retrying {i} of {retry}")
            bad = await self._downloadLibraries(
                    librariesDir,
                    installerDataBuf,
                    additionalLibDirs,
                    bad,
                    SimpleInstaller.LIBRARIES_MAX_CONCURRENT
            )
            if not bad:
                return True

        if bad:
            _bad = '\n'.join(bad)
            self.error(f"Failed to download libraries:\n{_bad}")
        return False

    async def _downloadLibraries(
            self,
            librariesDir: Path,
            installerDataBuf: BytesIO,
            additionalLibDirs: List[Path],
            libraries: Sequence[Version.Library],
            max_concurrent: int
    ):
        self.monitor.message(f"Found {len(additionalLibDirs)} additional library directories")

        bad = deque()

        def task(
                monitor: ProgressCallback,
                mirror: Mirror,
                library: Version.Library,
                root: Path,
                installerBuf: BytesIO,
                grabbed: Deque[Artifact],
                additionalLibraryDirs: List[Path],
                session_: Optional[requests.Session] = None
        ):
            nonlocal bad
            success = DownloadUtils.downloadLibrary(
                monitor,
                mirror,
                library,
                root,
                installerBuf,
                grabbed,
                additionalLibraryDirs,
                session_
            )
            if not success:
                _download = None if library.getDownloads() is None else library.getDownloads().getArtifact()
                if _download is not None and _download.url != "":
                    bad.append(lib)

        session = requests.Session()
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = []
            for lib in libraries:
                futures.append(
                    loop.run_in_executor(
                        executor,
                        functools.partial(
                            task,
                            self.monitor,
                            self.profile.getMirror(),
                            lib,
                            librariesDir,
                            installerDataBuf,
                            self.grabbed,
                            additionalLibDirs,
                            session
                        )))
            await asyncio.gather(*futures)
        session.close()

        if bad:
            self.monitor.message(f"\nFound {len(bad)} bad libraries.\n >>> {[lib.name for lib in bad]}")
        return bad

    def getLibraries(self) -> List[Version.Library]:
        libraries = []
        for lib in self.version.getLibraries():
            libraries.append(lib)
        for lib in self.processors.getLibraries():
            libraries.append(lib)
        return libraries

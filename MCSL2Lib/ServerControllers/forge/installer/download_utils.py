import hashlib
import re
import time
import traceback
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Callable, List, Optional, TypeVar, Deque

import requests

from .actions.progress_callback import ProgressCallback
from .bmclapi import getLibraryUrl as getBmclapiLibUrl
from .json.artifact import Artifact
from .json.manifest import Manifest
from .json.mirror import Mirror
from .json.version import Download, Library, LibraryDownload

T = TypeVar("T")

DOWNLOAD_CHUNK_SIZE = 64  # KB


class SpeedCounter:
    def __init__(self, buffer_size):
        self.buffer = [0.0] * buffer_size
        self.buffer_size = buffer_size
        self.ptr = 0

        self.full = False

    def append(self, speed):
        if self.ptr == self.buffer_size - 1:
            self.full = True

        self.buffer[self.ptr] = speed
        self.ptr = (self.ptr + 1) % self.buffer_size

    def average(self):
        if not self.full and self.ptr == 0:
            return round(sum(self.buffer) / self.buffer_size, 2)
        elif not self.full:
            return round(sum(self.buffer[:self.ptr]) / self.ptr, 2)
        else:
            return round(sum(self.buffer) / self.buffer_size, 2)


class DownloadUtils:
    MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    LIBRARIES_URL = "https://libraries.minecraft.net/"
    OFFLINE_MODE = True

    @staticmethod
    def downloadMirrors(url: str) -> Optional[List[Mirror]]:
        from .json.util import Util

        return DownloadUtils.downloadString(url, Util.loadMirrorList)

    @staticmethod
    def downloadString(url: str, reader: Callable[[str], T]) -> Optional[T]:
        try:
            with requests.get(url) as response:
                return reader(response.text)
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def getSha1(target: Path) -> Optional[str]:
        try:
            return hashlib.sha1(target.read_bytes()).hexdigest()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getMainClass(jar: Path) -> Optional[str]:
        from .json.util import Util

        jarDataBuffer = BytesIO(jar.read_bytes())
        try:
            with zipfile.ZipFile(jarDataBuffer, "r") as jarAsArchive:
                # try get /META-INF/MANIFEST.MF
                lines = jarAsArchive.read("META-INF/MANIFEST.MF")
                rv = re.findall(Util.mainClassPattern, lines.decode("utf-8"))
                if rv:
                    return rv[0]
                return None
        except (KeyError, zipfile.BadZipfile):
            return None
        except Exception:
            traceback.print_exc()
            return None

    @staticmethod
    def extractFile(
            art: Artifact, buf: BytesIO, target: Path, checksum: Optional[str] = None
    ) -> bool:
        location = Path("maven") / art.getPath()
        try:
            data = DownloadUtils.readFileInZip(buf, location)
            if not target.parent.exists():
                target.parent.mkdir(parents=True)
            try:
                target.write_bytes(data)
                return DownloadUtils.checksumValid(target, checksum)
            except IOError:
                traceback.print_exc()
                return False
        except KeyError:
            print(f"File not found in installer archive: /maven/{art.getPath()}")
            return False

    @staticmethod
    def readFileInZip(archiveBuf: BytesIO, relative: Path) -> Optional[bytes]:
        """
        :raise KeyError | IOError
        """
        with zipfile.ZipFile(archiveBuf, "r") as archive:
            location = str(relative).replace("\\", "/")
            if location.startswith("/"):
                location = location[1:]
            return archive.read(location)

    @staticmethod
    def checksumValid(target: Path, checksum: Optional[str]) -> bool:
        if checksum is None or checksum == "":
            return True
        else:
            return checksum is not None and DownloadUtils.getSha1(target) == checksum

    @staticmethod
    def downloadManifest() -> Manifest:
        from .json.util import Util

        return DownloadUtils.downloadString(DownloadUtils.MANIFEST_URL, Util.loadManifest)

    @staticmethod
    def download(
            monitor: ProgressCallback,
            mirror: Mirror,
            download: Download,
            target: Path,
            session: Optional[requests.Session] = None,
            detailed: bool = False,
    ) -> bool:
        return DownloadUtils._download(monitor, mirror, download, target, download.url, session or requests.Session(),
                                       detailed)

    @staticmethod
    def _download(
            monitor: ProgressCallback,
            mirror: Mirror,
            download: Download,
            target: Path,
            url: str,
            session: requests.Session,
            detailed: bool,
    ) -> bool:
        # TODO
        monitor.message(f"  Downloading library from {url}")
        try:
            with session.get(url, stream=True) as response:
                total = int(response.headers.get("content-length", 0))
                downloaded = 0
                speedCounter = SpeedCounter(10)
                timer = time.time_ns()
                with target.open("wb") as f:
                    for data in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE * 1024):

                        if monitor.isCancelled():
                            return False

                        data_len = len(data)
                        downloaded += data_len
                        f.write(data)

                        try:
                            speedCounter.append(
                                round(data_len / ((new_timer := time.time_ns()) - timer) * 1_000_000, 2)
                            )
                            monitor.downloadProgress(
                                target.name,
                                downloaded,
                                total,
                                speedCounter.average(),
                                False
                            )
                        except ZeroDivisionError:
                            pass
                        timer = new_timer
                    monitor.downloadProgress(target.name, total, total, 0, True)
                    monitor.message("")

                if download.url is not None:
                    sha1 = DownloadUtils.getSha1(target)
                    if sha1 == download.sha1:
                        monitor.message("    Download completed: Checksum validated.")
                        return True
                    monitor.message("    Download failed: Checksum invalid, deleting file:")
                    monitor.message("      Expected: " + download.sha1)
                    monitor.message("      Actual:   " + sha1)
                    try:
                        target.unlink(missing_ok=False)
                    except IOError:
                        monitor.stage("      Failed to delete file, aborting.")
                        return False
                monitor.message("    Download completed: No checksum, Assuming valid.")
        except Exception:
            target.unlink(missing_ok=True)
            traceback.print_exc()
        return False

    @staticmethod
    def downloadLibrary(
            monitor: ProgressCallback,
            mirror: Mirror,
            library: Library,
            root: Path,
            installerBuf: BytesIO,
            grabbed: Deque[Artifact],
            additionalLibraryDirs: List[Path],
            session: Optional[requests.Session] = None,
            detailed: bool = False
    ) -> bool:
        artifact = library.getName()
        target = artifact.getLocalPath(root)
        download = None if library.getDownloads() is None else library.getDownloads().getArtifact()
        if download is None:
            download = LibraryDownload.of({"path": artifact.getPath()})

        monitor.message(f"Considering library {artifact.getDescriptor()}")

        if target.exists():
            if download.getSha1() is not None:
                sha1 = DownloadUtils.getSha1(target)
                if download.getSha1() == sha1:
                    monitor.message("  File exists: Checksum validated.")
                    return True
                monitor.message("  File exists: Checksum invalid, deleting file:")
                monitor.message(f"    Expected: {download.getSha1()}")
                monitor.message(f"    Actual:   {sha1}")
                target.unlink(missing_ok=True)

            else:
                monitor.message("  File exists: No checksum, Assuming valid.")
                return True

        target.parent.mkdir(exist_ok=True, parents=True)

        # try extract first
        try:
            data = DownloadUtils.readFileInZip(installerBuf, Path("maven") / artifact.getPath())

            monitor.message(f"  Extracting library from /maven/{artifact.getPath()}")
            target.write_bytes(data)
            if download.sha1 is not None:
                sha1 = DownloadUtils.getSha1(target)
                if sha1 == download.sha1:
                    monitor.message("  Extraction completed: Checksum validated.")
                    grabbed.append(artifact)
                    return True
                monitor.message("  Extraction failed: Checksum invalid, deleting file:")
                monitor.message(f"    Expected: {download.sha1}")
                monitor.message(f"    Actual:   {sha1}")
                target.unlink(missing_ok=True)
                return False
            else:
                monitor.message("  Extraction completed: No checksum, Assuming valid.")
                grabbed.append(artifact)
                return True
        except zipfile.BadZipFile:
            traceback.print_exc()
            return False
        except KeyError:
            # Try searching local installs if the file can be validated
            if (providedSha1 := download.sha1) is not None:
                for libDir in additionalLibraryDirs:
                    inLibDir = Path(libDir) / artifact.getPath()
                    if inLibDir.exists():
                        monitor.message(f"  Found artifact in local folder {libDir}")
                        sha1 = DownloadUtils.getSha1(inLibDir)
                        if providedSha1 == sha1:
                            monitor.message("    Checksum validated")
                        else:
                            # Do not fail immediately. We may have other sources
                            monitor.message("    Invalid checksum. Not using.")
                            continue
                        # Valid checksum,copy the lib
                        try:
                            target.write_bytes(inLibDir.read_bytes())
                            monitor.message("    Successfully copied local file")
                            grabbed.append(artifact)
                            return True
                        except Exception as e:
                            # The copy may have failed when the file is in use.
                            # Don't abort, we may have other sources
                            traceback.print_exc()
                            monitor.message(f"    Failed to copy from local folder: {e}")
                            # Clean up the file that may have been created if the copy failed
                            if target.exists():
                                target.unlink(missing_ok=True)
                                return False

        url = download.url
        if url is None or url == "":
            monitor.message("  Invalid library, missing url")
            return False
        # replace url with bmclapi
        download.url = getBmclapiLibUrl(url)
        print(f"{url} -> {download.url}")
        if DownloadUtils.download(monitor, mirror, download, target, session, detailed):
            grabbed.append(artifact)
            return True

        return False

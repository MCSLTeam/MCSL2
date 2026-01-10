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
from .json.artifact import Artifact
from .json.manifest import Manifest
from .json.mirror import Mirror
from .json.version import Download, Library, LibraryDownload

T = TypeVar("T")

DOWNLOAD_CHUNK_SIZE = 64  # KB
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
)
HEADERS = {"User-Agent": USER_AGENT}
DOWNLOAD_TIMEOUT = (10, 30)  # (connect timeout, read timeout) in seconds
MAX_RETRIES = 3  # Maximum number of retry attempts per URL
RETRY_DELAY = 2  # Delay between retries in seconds


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
            return round(sum(self.buffer[: self.ptr]) / self.ptr, 2)
        else:
            return round(sum(self.buffer) / self.buffer_size, 2)


class DownloadUtils:
    MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    LIBRARIES_URL = "https://libraries.minecraft.net/"
    MANIFEST_URL_MIRROR = "https://bmclapi2.bangbang93.com/mc/game/version_manifest.json"
    LIBRARIES_URL_MIRROR = "https://bmclapi2.bangbang93.com/maven"
    OFFLINE_MODE = True

    @staticmethod
    def downloadMirrors(url: str) -> Optional[List[Mirror]]:
        from .json.util import Util

        return DownloadUtils.downloadString(url, Util.loadMirrorList)

    @staticmethod
    def downloadString(url: str, reader: Callable[[str], T]) -> Optional[T]:
        for attempt in range(MAX_RETRIES):
            try:
                with requests.get(
                    url,
                    allow_redirects=True,
                    timeout=DOWNLOAD_TIMEOUT,
                    headers=HEADERS
                ) as response:
                    response.raise_for_status()
                    return reader(response.text)
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                    requests.exceptions.HTTPError) as e:
                if attempt < MAX_RETRIES - 1:
                    print(
                        f"Failed to download from {url} "
                        f"(attempt {attempt + 1}/{MAX_RETRIES}): {type(e).__name__}"
                    )
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                else:
                    print(
                        f"Failed to download from {url} "
                        f"after {MAX_RETRIES} attempts: {e}"
                    )
                    traceback.print_exc()
            except Exception:
                print(f"Failed to download from {url}")
                traceback.print_exc()
                break
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
        session = session or requests.Session()
        original_url = download.url

        if not original_url:
            return False

        # Try with mirror first if available
        from .bmclapi import getLibraryUrl, _isUseBMCLAPIForNeoForge

        # Collect unique URLs to try
        urls_to_try = []

        if _isUseBMCLAPIForNeoForge():
            mirror_url = getLibraryUrl(original_url)
            # If mirror URL is different, try it first
            if mirror_url != original_url:
                urls_to_try.append(("mirror", mirror_url))
                urls_to_try.append(("original", original_url))
            else:
                # Mirror URL is same as original, only try once
                urls_to_try.append(("original", original_url))
        else:
            # BMCLAPI disabled, only try original
            urls_to_try.append(("original", original_url))

        last_exception = None
        for idx, (source_type, url) in enumerate(urls_to_try):
            try:
                monitor.message(f"  Trying {source_type} source...")
                download.url = url
                result = DownloadUtils._download(
                    monitor, mirror, download, target, url, session, detailed
                )
                if result:
                    return True
            except Exception as e:
                last_exception = e
                monitor.message(f"    {source_type.capitalize()} source failed: {type(e).__name__}")
                # Show fallback message if there are more sources to try
                if idx < len(urls_to_try) - 1:
                    next_source = urls_to_try[idx + 1][0]
                    monitor.message(f"    Falling back to {next_source} source...")
                continue

        # All attempts failed
        if last_exception:
            raise last_exception
        return False

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
        monitor.message(f"  Downloading library from {url}")

        for attempt in range(MAX_RETRIES):
            try:
                with session.get(
                    url,
                    stream=True,
                    headers=HEADERS,
                    allow_redirects=True,
                    timeout=DOWNLOAD_TIMEOUT
                ) as response:
                    response.raise_for_status()
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
                                speed = (
                                    data_len
                                    / ((new_timer := time.time_ns()) - timer)
                                    * 1_000_000
                                )
                                speedCounter.append(round(speed, 2))
                                monitor.downloadProgress(
                                    target.name, downloaded, total, speedCounter.average(), False
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
                    else:
                        monitor.message("    Download completed: No checksum, Assuming valid.")
                        return True

            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                    requests.exceptions.ChunkedEncodingError) as e:
                target.unlink(missing_ok=True)
                if attempt < MAX_RETRIES - 1:
                    monitor.message(
                        f"    Download failed (attempt {attempt + 1}/{MAX_RETRIES}): "
                        f"{type(e).__name__}"
                    )
                    monitor.message(f"    Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                else:
                    monitor.message(f"    Download failed after {MAX_RETRIES} attempts: {e}")
                    raise
            except requests.exceptions.HTTPError as e:
                target.unlink(missing_ok=True)
                monitor.message(f"    HTTP error: {e}")
                raise
            except Exception:
                target.unlink(missing_ok=True)
                traceback.print_exc()
                raise

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
        detailed: bool = False,
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

        # The download method will handle mirror fallback automatically
        if DownloadUtils.download(monitor, mirror, download, target, session, detailed):
            grabbed.append(artifact)
            return True

        return False

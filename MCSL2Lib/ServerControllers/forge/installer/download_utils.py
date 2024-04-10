import hashlib
import re
import traceback
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Callable, List, Optional, TypeVar

import requests

from .actions.progress_callback import ProgressCallback
from .json.artifact import Artifact
from .json.manifest import Manifest
from .json.mirror import Mirror
from .json.version import Version

T = TypeVar("T")


class DownloadUtils:
    MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    LIBRARIES_URL = "https://libraries.minecraft.net/"

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
        except Exception as e:
            traceback.print_exception(e)
            return None

    @staticmethod
    def extractFile(art: Artifact, target: Path, checksum: Optional[str] = None) -> bool:
        buf = BytesIO(target.read_bytes())

        location = Path("maven") / art.getPath()
        try:
            data = DownloadUtils.readFileInZip(buf, location)
            buf.close()
            if not target.parent.exists():
                target.parent.mkdir(parents=True)
            try:
                target.write_bytes(data)
                return DownloadUtils.checksumValid(target, checksum)
            except IOError as e:
                traceback.print_exception(e)
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
            return archive.read(str(relative).replace("\\", "/"))

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
    def download(monitor: ProgressCallback, mirror: Mirror, download: Version.Download, target: Path):
        DownloadUtils._download(monitor, mirror, download, target, download.url)

    @staticmethod
    def _download(monitor: ProgressCallback, mirror: Mirror, download: Version.Download, target: Path, url: str):
        # TODO
        ...

    @staticmethod
    def downloadLibrary(
            monitor: ProgressCallback,
            mirror: Mirror,
            library: Version.Library,
            root: Path,
            installerBuf: BytesIO,
            grabbed: List[Artifact],
            additionalLibraryDirs: List[Path]
    ):
        """
         public static boolean downloadLibrary(ProgressCallback monitor, Mirror mirror, Library library, File root, List<Artifact> grabbed, List<File> additionalLibraryDirs) {
        Artifact artifact = library.getName();
        File target = artifact.getLocalPath(root);
        LibraryDownload download = library.getDownloads() == null ? null :  library.getDownloads().getArtifact();
        if (download == null) {
            download = new LibraryDownload();
            download.setPath(artifact.getPath());
        }

        monitor.message(String.format("Considering library %s", artifact.getDescriptor()));

        if (target.exists()) {
            if (download.getSha1() != null) {
                String sha1 = getSha1(target);
                if (download.getSha1().equals(sha1)) {
                    monitor.message("  File exists: Checksum validated.");
                    return true;
                }
                monitor.message("  File exists: Checksum invalid, deleting file:");
                monitor.message("    Expected: " + download.getSha1());
                monitor.message("    Actual:   " + sha1);
                if (!target.delete()) {
                    monitor.stage("    Failed to delete file, aborting.");
                    return false;
                }
            } else {
                monitor.message("  File exists: No checksum, Assuming valid.");
                return true;
            }
        }

        target.getParentFile().mkdirs();

        // Try extracting first
        try (final InputStream input = DownloadUtils.class.getResourceAsStream("/maven/" + artifact.getPath())) {
            if (input != null) {
                monitor.message("  Extracting library from /maven/" + artifact.getPath());
                Files.copy(input, target.toPath(), StandardCopyOption.REPLACE_EXISTING);
                if (download.getSha1() != null) {
                    String sha1 = getSha1(target);
                    if (download.getSha1().equals(sha1)) {
                        monitor.message("    Extraction completed: Checksum validated.");
                        grabbed.add(artifact);
                        return true;
                    }
                    monitor.message("    Extraction failed: Checksum invalid, deleting file:");
                    monitor.message("      Expected: " + download.getSha1());
                    monitor.message("      Actual:   " + sha1);
                    if (!target.delete()) {
                        monitor.stage("      Failed to delete file, aborting.");
                        return false;
                    }
                    return false;
                } else {
                    monitor.message("    Extraction completed: No checksum, Assuming valid.");
                }
                grabbed.add(artifact);
                return true;
            }
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }

        // Try searching local installs if the file can be validated
        if (download.getSha1() != null) {
            String providedSha1 = download.getSha1();
            for (File libDir : additionalLibraryDirs) {
                File inLibDir = new File(libDir, artifact.getPath());
                if (inLibDir.exists()) {
                    monitor.message(String.format("  Found artifact in local folder %s", libDir.toString()));
                    String sha1 = DownloadUtils.getSha1(inLibDir);
                    if (providedSha1.equals(sha1)) {
                        monitor.message("    Checksum validated");
                    } else {
                        // Do not fail immediately. We may have other sources
                        monitor.message("    Invalid checksum. Not using.");
                        continue;
                    }
                    // Valid checksum, copy the lib
                    try {
                        Files.copy(inLibDir.toPath(), target.toPath());
                        monitor.message("    Successfully copied local file");
                        grabbed.add(artifact);
                        return true;
                    } catch (IOException e) {
                        // The copy may have failed when the file is in use. Don't abort, we may have other sources
                        e.printStackTrace();
                        monitor.message(String.format("    Failed to copy from local folder: %s", e.toString()));
                        // Clean up the file that may have been created if the copy failed
                        if (target.exists()) {
                            if (!target.delete()) {
                                monitor.message("    Failed to delete failed copy, aborting");
                                return false;
                            }
                        }
                    }
                }
            }
        }

        String url = download.getUrl();
        if (url == null || url.isEmpty()) {
            monitor.message("  Invalid library, missing url");
            return false;
        }

        if (download(monitor, mirror, download, target)) {
            grabbed.add(artifact);
            return true;
        }
        return false;
    }
        """

        artifact = library.getName()
        target = artifact.getLocalPath(root)
        download = None if library.getDownloads() else library.getDownloads().getArtifact()
        if download is None:
            download = Version.LibraryDownload.of({
                "path": artifact.getPath()
            })

        monitor.message(f"Considering library {artifact.getDescriptor()}")

        if target.exists():
            if download.getSha1() is not None:
                sha1 = DownloadUtils.getSha1(target)
                if download.getSha1() == sha1:
                    monitor.message("  File exists: Checksum validated.")
                    return True
                monitor.message(f"  File exists: Checksum invalid, deleting file:")
                monitor.message(f"    Expected: {download.getSha1()}")
                monitor.message(f"    Actual:   {sha1}")
                target.unlink(missing_ok=True)

            else:
                monitor.message("  File exists: No checksum, Assuming valid.")
                return True

        target.parent.mkdir(exist_ok=True)

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
                monitor.message(f"  Extraction failed: Checksum invalid, deleting file:")
                monitor.message(f"    Expected: {download.sha1}")
                monitor.message(f"    Actual:   {sha1}")
                target.unlink(missing_ok=True)
                return False
            else:
                monitor.message("  Extraction completed: No checksum, Assuming valid.")
                grabbed.append(artifact)
                return True
        except zipfile.BadZipFile as e:
            traceback.print_exception(e)
            return False
        except KeyError:

            # Try searching local installs if the file can be validated
            if (providedSha1 := download.getSha1()) is not None:
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
                            # The copy may have failed when the file is in use. Don't abort, we may have other sources
                            traceback.print_exception(e)
                            monitor.message(f"    Failed to copy from local folder: {e}")
                            # Clean up the file that may have been created if the copy failed
                            if target.exists():
                                target.unlink(missing_ok=True)
                                return False

        url = download.url
        if url is None or url != "":
            monitor.message("  Invalid library, missing url")
            return False

        if (download(monitor,mirror,download,target)):
            grabbed.append(artifact)
            return True

        return False

import hashlib
import re
import traceback
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Callable, List, Optional, TypeVar, Dict

import requests

from .json.artifact import Artifact
from .json.manifest import Manifest
from .json.mirror import Mirror


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
        with zipfile.ZipFile(buf, "r") as archive:
            location = str(Path("maven") / art.getPath()).replace("\\", "/")
            try:
                data = archive.read(location)
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
    def checksumValid(target: Path, checksum: Optional[str]) -> bool:
        if checksum is None or checksum == "":
            return True
        else:
            return checksum is not None and DownloadUtils.getSha1(target) == checksum

    @staticmethod
    def downloadManifest() -> Manifest:
        return DownloadUtils.downloadString(DownloadUtils.MANIFEST_URL, DownloadUtils.loadManifest)

    @staticmethod
    def loadManifest(data: Dict) -> Manifest:
        return Manifest.from_dict(data)

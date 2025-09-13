from typing import Dict, Optional

import requests

from .json.version import Version, Download

BMCLAPI_ROOT = "https://bmclapi2.bangbang93.com"

SESSION = requests.Session()


def getDownloadInfo(version) -> Download:
    from .download_utils import DownloadUtils
    from .json.util import Util

    url = BMCLAPI_ROOT + f"/version/{version}/json"
    versions = DownloadUtils.downloadString(url, Util.loadVersion)
    dl = versions.getDownload("server")  # type: ignore
    return dl  # type: ignore


def getMinecraftDownload(version: str, side: str) -> Optional[Download]:
    url = BMCLAPI_ROOT + f"/version/{version}/{side}"
    dl = getDownloadInfo(version)
    if dl is not None:
        dl.url = url
    return dl


def getLibraryUrl(url: str):
    return "https://bmclapi2.bangbang93.com/maven" + url[url.find("/", 8) :]

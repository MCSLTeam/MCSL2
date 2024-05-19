from typing import Dict, Optional

import requests

from .json.version import Version

BMCLAPI_ROOT = "https://bmclapi2.bangbang93.com"


class Utils:
    @staticmethod
    def getDownloadInfo(url) -> Optional[Dict[str, str]]:
        with requests.head(url, allow_redirects=True) as resp:
            if resp.ok:
                headers = resp.headers
                return {
                    "sha1": headers.get("x-bmclapi-hash"),
                    "size": int(headers.get("Content-Length")),
                }


def getMinecraftDownload(version: Version, side: str) -> Optional[Version.Download]:
    url = BMCLAPI_ROOT + f"/version/{version.id}/{side}"
    info = Utils.getDownloadInfo(url)
    if info is None:
        return None
    return Version.Download.of(
        {"sha1": info.get("sha1"), "size": info.get("size"), "url": url, "provided": False}
    )


def getLibraryUrl(url: str):
    return "https://bmclapi2.bangbang93.com/maven" + url[32:]

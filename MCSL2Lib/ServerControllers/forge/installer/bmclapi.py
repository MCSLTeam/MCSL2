from typing import Dict, Optional

import requests

from .json.version import Version, Download

BMCLAPI_ROOT = "https://bmclapi2.bangbang93.com"

SESSION = requests.Session()


def getDownloadInfo(url) -> Optional[Dict[str, str]]:
    with SESSION.head(url, allow_redirects=True) as resp:
        if resp.ok:
            headers = resp.headers
            return {
                "sha1": headers.get("x-bmclapi-hash"),
                "size": int(headers.get("Content-Length")),
            }


def getMinecraftDownload(version: Version, side: str) -> Optional[Download]:
    url = BMCLAPI_ROOT + f"/version/{version.id}/{side}"
    info = getDownloadInfo(url)
    if info is None:
        return None
    return Download.of(
        {"sha1": info.get("sha1"), "size": info.get("size"), "url": url, "provided": False}
    )


def getLibraryUrl(url: str):
    return "https://bmclapi2.bangbang93.com/maven" + url[url.find("/", 8):]

from typing import Dict, Optional

import requests

from .json.version import Version, Download

BMCLAPI_ROOT = "https://bmclapi2.bangbang93.com"

SESSION = requests.Session()


def _isUseBMCLAPI() -> bool:
    """Check if BMCLAPI should be used"""
    try:
        from MCSL2Lib.ProgramControllers.settingsController import cfg
        return cfg.get(cfg.useBMCLAPI)
    except Exception:
        return True  # Default to True if config is not available


def getDownloadInfo(version) -> Optional[Download]:
    from .download_utils import DownloadUtils
    from .json.util import Util

    if not _isUseBMCLAPI():
        return None
    
    url = BMCLAPI_ROOT + f"/version/{version}/json"
    versions = DownloadUtils.downloadString(url, Util.loadVersion)
    if versions is None:
        print(f"Failed to download version info for {version} from {url}")
        return None
    
    # Check if versions object has getDownload method
    if not hasattr(versions, 'getDownload'):
        print(f"Invalid version object returned for {version}")
        return None
    
    dl = versions.getDownload("server")  # type: ignore
    return dl  # type: ignore


def getMinecraftDownload(version: str, side: str) -> Optional[Download]:
    if not _isUseBMCLAPI():
        print(f"BMCLAPI is disabled, skipping mirror download for {version}")
        return None
    
    url = BMCLAPI_ROOT + f"/version/{version}/{side}"
    dl = getDownloadInfo(version)
    if dl is not None:
        dl.url = url
    return dl


def getLibraryUrl(url: str):
    if not _isUseBMCLAPI():
        return url
    return "https://bmclapi2.bangbang93.com/maven" + url[url.find("/", 8) :]

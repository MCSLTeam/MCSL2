from typing import Callable, List, Optional, TypeVar

import requests

from .json.mirror import Mirror
from .json.util import Util

T = TypeVar("T")

class DownloadUtils:
    @staticmethod
    def downloadMirrors(url:str) -> Optional[List[Mirror]]:
        return DownloadUtils.downloadString(url, Util.loadMirrorList)
    
    def downloadString(url:str,reader:Callable[[str],T]) -> Optional[T]:
        try:
            with requests.get(url) as response:
                return reader(response.text)
        except Exception as e:
            print(e)
        return None

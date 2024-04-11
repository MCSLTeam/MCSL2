import json
import re
import traceback
from typing import List, Dict, Optional

from .manifest import Manifest
from .mirror import Mirror
from .version import Version
from ..download_utils import DownloadUtils
from ..java2python import Supplier


class Util:
    mainClassPattern = re.compile(r"Main-Class:\s(\S+)\n")

    @staticmethod
    def loadMirrorList(text: str) -> List[Mirror]:
        return [Mirror(**mirror) for mirror in json.loads(text)]

    @staticmethod
    def loadInstallProfile(text: str):
        from .install import Install
        from .installV1 import InstallV1

        profile = json.loads(text)
        spec = profile.get("spec", 0)

        if spec == 0:
            return InstallV1.from_installV0(Install.of(profile))
        elif spec == 1:
            return InstallV1.of(profile)

    @staticmethod
    def loadVersion(text: str):
        from .version import Version
        return Version.of(json.loads(text))

    @staticmethod
    def replaceTokens(tokens: Dict[str, Supplier[str]], value: str):
        """
        :raise ValueError
        """

        buf = ""

        x = 0  # for (int x = 0; x < value.length(); x++)
        while x < len(value):  # for (int x = 0; x < value.length(); x++)

            c = value[x]
            if c == "\\":
                if x == len(value) - 1:
                    raise ValueError("Illegal pattern (Bad escape): " + value)
                buf += value[x + 1]
                x += 1
            elif c == "{" or c == "'":
                key = ""

                y = x + 1  # for (int y = x + 1; y <= value.length(); y++)
                while y < len(value):  # for (int y = x + 1; y <= value.length(); y++)
                    if y == len(value) - 1:
                        raise ValueError("Illegal pattern (Unclosed " + c + "): " + value)

                    d = value[y]
                    if d == '\\':
                        if y == len(value) - 1:
                            raise ValueError("Illegal pattern (Bad escape): " + value)
                        key += value[y + 1]
                        y += 1
                    elif c == '{' and d == '}':
                        x = y
                        break
                    elif c == "'" and d == "'":
                        x = y
                        break
                    else:
                        key += d

                    y += 1  # # for (int y = x + 1; y <= value.length(); y++)

                if c == "'":
                    buf += key
                else:
                    token = tokens.get(key).get()
                    if token is None:
                        raise ValueError("Illegal pattern: " + value + " Missing Key: " + key)
                    buf += token
            else:
                buf += c

            x += 1  # for (int x = 0; x < value.length(); x++)
        return buf

    @staticmethod
    def getVanillaVersion(version: str) -> Optional[Version]:
        manifest = DownloadUtils.downloadManifest()
        if manifest is None:
            return None
        url = manifest.getUrl(version)
        if url is None:
            return None
        return DownloadUtils.downloadString(url, Util.loadVersionFromText)

    @staticmethod
    def loadManifest(text: str) -> Optional[Manifest]:
        try:
            data = json.loads(text)
            return Manifest.of(data)
        except Exception as e:
            traceback.print_exc()
            return None

    @staticmethod
    def loadVersionFromText(text: str) -> Optional[Version]:
        try:
            data = json.loads(text)
            return Version.of(data)
        except Exception as e:
            traceback.print_exc()
            return None

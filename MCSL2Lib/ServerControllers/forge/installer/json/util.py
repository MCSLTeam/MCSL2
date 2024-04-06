import json
from typing import List
from .mirror import Mirror


class Util:
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
            return InstallV1.from_installV0(Install.from_dict(profile))
        elif spec == 1:
            return InstallV1.from_dict(profile)
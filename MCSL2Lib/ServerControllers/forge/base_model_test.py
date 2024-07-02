import json
from pathlib import Path
from typing import List

from MCSL2Lib.ServerControllers.forge.installer.json.util import Util
from installer.json.base_model import BaseModel

# # dataclasses.dataclass()
# #
text = Path("./install_profile.json").read_text()
install = Util.loadInstallProfile(text)
print(json.dumps(install.to_dict(), indent=4, sort_keys=True))


print('====================================================================')


text = Path("./version.json").read_text()
version = Util.loadVersionFromText(text)
print(json.dumps(version.to_dict(), indent=4, sort_keys=True))



class D(BaseModel):
    a: int


class A(BaseModel):
    class B(BaseModel):
        o: int
        p: List[int]

    class C(BaseModel):
        o: int
        p: List[int]

    a: int
    b: List[str]
    c: List[List[int]]
    d: str
    dd: D


print(6)

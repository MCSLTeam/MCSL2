from pathlib import Path

import installer
from installer.json.util import Util
from typing import List

from installer.json.base_model import BaseModel


# dataclasses.dataclass()
#
text = Path("./install_profile.json").read_text()
install = Util.loadInstallProfile(text)
print(6)

text = Path("./version.json").read_text()
version = Util.loadVersionFromText(text)
print(6)


class A(BaseModel):
    a: int
    b: List[str]
    c: List[List[int]]


A
print(6)

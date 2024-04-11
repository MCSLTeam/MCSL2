from dataclasses import dataclass
from typing import List, Optional

from .base_model import BaseModel


@dataclass
class Manifest(BaseModel):
    @dataclass
    class Info(BaseModel):
        id: str
        url: str

        def getId(self) -> str:
            return self.id

        def getUrl(self) -> str:
            return self.url

    versions: List[Info]

    def getUrl(self, version) -> Optional[str]:
        # return versions == null ? null : versions.stream().filter(v -> version.equals(v.getId())).map(Info::getUrl).findFirst().orElse(null);
        try:
            return None if self.versions is None else next(v.getUrl() for v in self.versions if version == v.getId())
        except StopIteration:
            return None

    @classmethod
    def version_factory(cls, item) -> List[Info]:
        return [Manifest.Info.of(i) for i in item]

from dataclasses import dataclass

from .base_model import BaseModel


@dataclass
class Spec(BaseModel):
    spec: int

    def getSpec(self) -> int:
        return self.spec

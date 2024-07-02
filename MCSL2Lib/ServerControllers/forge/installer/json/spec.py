from dataclasses import dataclass

from .base_model import BaseModel


class Spec(BaseModel):
    spec: int

    def getSpec(self) -> int:
        return self.spec

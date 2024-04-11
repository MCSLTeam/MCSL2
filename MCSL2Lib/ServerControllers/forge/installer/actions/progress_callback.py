import abc

from ..java2python import FunctionalInterface


@FunctionalInterface
class ProgressCallback(metaclass=abc.ABCMeta):
    def start(self, label: str):
        self.message(label)

    def stage(self, message: str):
        self.message(message)

    @abc.abstractmethod
    def message(self, message: str):
        ...

    def progress(self, progress: float):
        pass


TO_SDT_OUT = ProgressCallback.of(lambda self, message: print(message))

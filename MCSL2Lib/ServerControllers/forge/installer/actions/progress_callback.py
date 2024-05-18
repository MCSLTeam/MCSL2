import abc

from ..java2python import FunctionalInterface


@FunctionalInterface
class ProgressCallback(metaclass=abc.ABCMeta):
    lastProgress = 0

    def start(self, label: str):
        self.message(label)

    def stage(self, message: str):
        self.message(message)

    @abc.abstractmethod
    def message(self, message: str):
        ...

    def progress(self, progress: float, total: float):
        percent = int(progress / total * 100 + 0.5)
        if percent > self.lastProgress:
            print("·" * (percent - self.lastProgress), end="")
            self.lastProgress = percent
        else:
            if self.lastProgress - percent > 0:
                print()
                print("·" * (self.lastProgress - percent), end='')
                self.lastProgress = percent


TO_STD_OUT = ProgressCallback.of(lambda self, message: print(message))

from json import load, dump
from typing import Callable, Any
from PyQt5.QtCore import QThread, pyqtSignal


def Singleton(cls):
    Instances = {}

    def GetInstance(*args, **kwargs):
        if cls not in Instances:
            Instances[cls] = cls(*args, **kwargs)
        return Instances[cls]

    return GetInstance

def ReadJsonFile(FileName):
    FileName = 'MCSL2/' + FileName
    with open(FileName, 'r', encoding='utf-8') as RJsonFile:
        Data = load(RJsonFile)
    return Data


def SaveJsonFile(FileName, Data):
    FileName = 'MCSL2/' + FileName
    with open(FileName, 'w', encoding='utf-8') as SJsonFile:
        dump(Data, SJsonFile, ensure_ascii=False, indent=4, sort_keys=True)

class JsonReadThread(QThread):
    readSignal = pyqtSignal(dict)

    def __init__(self, FileName, FinishSlot: Callable[[dict, ], Any] = ...):
        super().__init__()
        self.FileName = FileName
        self.Data = None
        if FinishSlot is not ...:
            self.readSignal.connect(FinishSlot)

    def GetFileName(self):
        return self.FileName

    def run(self):
        self.Data = ReadJsonFile(self.FileName)
        self.readSignal.emit(self.Data)

    def GetData(self):
        return self.Data


class JsonSaveThread(QThread):
    saveSignal = pyqtSignal(bool)

    def __init__(self, FileName, Data, FinishSlot: Callable[[], Any] = ...):
        super().__init__()
        self.FileName = FileName
        self.Data = Data
        if FinishSlot is not ...:
            self.saveSignal.connect(FinishSlot)

    def GetFileName(self):
        return self.FileName

    def run(self):
        try:
            SaveJsonFile(self.FileName, self.Data)
            self.saveSignal.emit(True)
        except Exception as e:
            # print(e)
            self.saveSignal.emit(False)


@Singleton
class JsonReadThreadFactory:
    """
        虽然我不会去实例化这个类，但我还是加了个singleton装饰器...
    """

    @classmethod
    def Create(cls, FileName, FinishSlot: Callable[[dict, ], Any] = ...) -> JsonReadThread:
        return JsonReadThread(FileName, FinishSlot)


@Singleton
class JsonSaveThreadFactory:
    """
        虽然我不会去实例化这个类，但我还是加了个singleton装饰器...
    """

    @classmethod
    def Create(cls, FileName, Data, FinishSlot: Callable[[], Any] = ...) -> JsonSaveThread:
        return JsonSaveThread(FileName, Data, FinishSlot)



from json import load, dump
from os import mkdir, listdir
from os import path as ospath
from typing import Callable, Any

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog

from MCSL2_Libs.MCSL2_Dialog import Ui_MCSL2_Dialog, Ui_MCSL2_AskDialog


def Singleton(cls):
    Instances = {}

    def GetInstance(*args, **kwargs):
        if cls not in Instances:
            Instances[cls] = cls(*args, **kwargs)
        return Instances[cls]

    return GetInstance


def InitMCSL():
    global LogFilesCount
    if not ospath.exists(r"MCSL2"):
        LogFilesCount = 0
        mkdir(r"MCSL2")
        mkdir(r"MCSL2/Logs")
        mkdir(r"MCSL2/Aria2")
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as InitConfig:
            ConfigTemplate = ""
            InitConfig.write(ConfigTemplate)
            InitConfig.close()
        with open(
                r"./MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
        ) as InitServerList:
            ServerListTemplate = '{\n  "MCSLServerList": [\n    {\n      "name": "MCSLReplacer",\n      ' \
                                 '"core_file_name": "MCSLReplacer",\n      "java_path": "MCSLReplacer",' \
                                 '\n      "min_memory": "MCSLReplacer",\n      "max_memory": "MCSLReplacer"\n    }\n  ' \
                                 ']\n} '
            InitServerList.write(ServerListTemplate)
            InitServerList.close()
        if not ospath.exists(r"Servers"):
            mkdir(r"./Servers")
        if not ospath.exists(r"MCSL2/Logs"):
            mkdir(r"MCSL2/Logs")
        pass
    else:
        LogFilesCount = len(listdir(r"MCSL2/Logs"))
        if not ospath.exists(r"Servers"):
            mkdir(r"./Servers")
        if not ospath.exists(r"MCSL2/Logs"):
            mkdir(r"MCSL2/Logs")
        pass











def ReadJsonFile(FileName):
    FileName = 'MCSL2/' + FileName
    with open(FileName, 'r', encoding='utf-8') as RJsonFile:
        Data = load(RJsonFile)
    return Data


def SaveJsonFile(FileName, Data):
    FileName = 'MCSL2/' + FileName
    with open(FileName, 'w', encoding='utf-8') as SJsonFile:
        dump(Data, SJsonFile, ensure_ascii=False, indent=4, sort_keys=True)


# Customize dialogs
class MCSL2Dialog(QDialog, Ui_MCSL2_Dialog):
    def __init__(self, Tip, parent=None):
        super(MCSL2Dialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.Dialog_label.setText(Tip)


class MCSL2AskDialog(QDialog, Ui_MCSL2_AskDialog):
    def __init__(self, Tip, parent=None):
        super(MCSL2AskDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.Dialog_label.setText(Tip)


# The function of calling MCSL2 Dialog
def CallMCSL2Dialog(Tip, isNeededTwoButtons, parent=None):
    if isNeededTwoButtons == 0:
        Dialog = MCSL2Dialog(Tip, parent)
    elif isNeededTwoButtons == 1:
        Dialog = MCSL2AskDialog(Tip, parent)
    else:
        return
    Dialog.exec_()
    return Dialog


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



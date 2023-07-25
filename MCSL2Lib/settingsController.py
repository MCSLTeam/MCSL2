from os import path as ospath
from json import loads

class _settingsController:
    _judge = None
    def __new__(cls):
        if cls._judge==None:
            cls._judge=object.__new__(cls)
            return  cls._judge
        else:
            return cls._judge

    def __init__(self):
        self.fileSettings = {}
        self.unSavedSettings = {}

    def _readSettings(self, firstLoad):
        if ospath.exists(r"./MCSL2/MCSL2_Config.json"):
            if ospath.getsize(r"./MCSL2/MCSL2_Config.json") != 0:
                with open(r"./MCSL2/MCSL2_Config.json", "r", encoding="utf-8") as readConfig:
                    # 从文件读取的配置
                    self.fileSettings = loads(readConfig.read())
                    # 多声明一份给修改设置的时候用
                    if firstLoad:
                        self.unSavedSettings = self.fileSettings
                    else:
                        pass
                    readConfig.close()
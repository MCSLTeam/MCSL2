#     Copyright 2023, MCSL Team, mailto:lxhtz.dl@qq.com
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
'''
Settings controller, for editing MCSL2's configurations.
'''

from os import path as ospath
from json import loads

class SettingsController:
    _judge = None
    def __new__(cls):
        if cls._judge==None:
            cls._judge=object.__new__(cls)
            return  cls._judge
        else:
            return cls._judge

    def __init__(self):
        self.fileSettings = {} # 文件中的原始配置
        self.unSavedSettings = {} # 更改后的配置

    def _readSettings(self, firstLoad):
        '''重新将文件中的配置强制覆盖到程序中，不管是否保存了'''
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
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
"""
These are the built-in variables of MCSL2.
"""

from MCSL2Lib.publicFunctions import readGlobalServerConfig
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.settingsController import SettingsController

settingsController = SettingsController()

@Singleton
class ConfigureServerVariables:
    """新建服务器所需变量"""

    def __init__(self):
        self.javaPath: list = []
        self.minMem: int
        self.maxMem: int
        self.corePath: str = ""
        self.coreFileName: str = ""
        self.selectedJavaPath: str = ""
        self.selectedJavaVersion: str = ""
        self.memUnit: str = ""
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"
        self.consoleDeEncodingList = ["follow", "utf-8", "gbk"]
        self.memUnitList = ["M", "G"]
        self.jvmArg: list[str] = [""]
        self.serverName: str = ""

    def resetToDefault(self):
        self.minMem: int
        self.maxMem: int
        self.corePath: str = ""
        self.coreFileName: str = ""
        self.selectedJavaPath: str = ""
        self.selectedJavaVersion: str = ""
        self.memUnit: str = ""
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"
        self.jvmArg: list[str] = [""]
        self.serverName: str = ""
        self.icon: str = ""


@Singleton
class EditServerVariables:
    """修改服务器所需变量"""

    def __init__(self):
        self.javaPath: list = []
        self.corePath: str = ""
        self.selectedJavaVersion: str = ""

        self.oldMinMem: int
        self.oldMaxMem: int
        self.oldCoreFileName: str = ""
        self.oldSelectedJavaPath: str = ""
        self.oldMemUnit: str = ""
        self.oldJVMArg: list[str] = [""]
        self.oldServerName: str = ""
        self.oldConsoleOutputDeEncoding: str = "follow"
        self.oldConsoleInputDeEncoding: str = "follow"
        self.oldIcon: str = "Grass.png"

        self.minMem: int
        self.maxMem: int
        self.coreFileName: str = ""
        self.selectedJavaPath: str = ""
        self.memUnit: str = ""
        self.jvmArg: list[str] = [""]
        self.serverName: str = ""
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"
        self.icon: str = "Grass.png"

        self.consoleDeEncodingList = ["follow", "utf-8", "gbk"]
        self.memUnitList = ["M", "G"]
        self.iconsFileNameList = [
            "Anvil.png",
            "Cloth.png",
            "CobbleStone.png",
            "CommandBlock.png",
            "CraftingTable.png",
            "Egg.png",
            "Glass.png",
            "GoldBlock.png",
            "Grass.png",
            "GrassPath.png",
            "Java.svg",
            "MCSL2.png",
            "Paper.png",
            "RedstoneBlock.png",
            "RedstoneLampOff.png",
            "RedstoneLampOn.png",
            "Spigot.svg",
        ]

    def resetToDefault(self):
        self.oldMinMem: int
        self.oldMaxMem: int
        self.oldCorePath: str = ""
        self.oldCoreFileName: str = ""
        self.oldSelectedJavaPath: str = ""
        self.oldSelectedJavaVersion: str = ""
        self.oldSemUnit: str = ""
        self.oldJVMArg: list[str] = [""]
        self.oldServerName: str = ""
        self.oldConsoleOutputDeEncoding: str = "follow"
        self.oldConsoleInputDeEncoding: str = "follow"
        self.oldIcon: str = "Grass.png"

        self.minMem: int
        self.maxMem: int
        self.corePath: str = ""
        self.coreFileName: str = ""
        self.selectedJavaPath: str = ""
        self.selectedJavaVersion: str = ""
        self.memUnit: str = ""
        self.jvmArg: list[str] = [""]
        self.serverName: str = ""
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"
        self.icon: str = "Grass.png"


@Singleton
class PluginVariables:
    """插件系统所需变量"""

    def __init__(self):
        self.pluginSwitchBtnDict = {}


class GlobalMCSL2Variables:
    """需要被全局使用的变量"""

    MCSL2Version = "2.1.4.0"
    scrollAreaViewportQss = "background-color: transparent;"


@Singleton
class DownloadVariables:
    """下载页需要的变量"""

    def __init__(self):
        self.MCSLAPIDownloadUrlDict = {}


@Singleton
class ServerVariables:
    """需要开启的服务器的变量"""

    def __init__(self):
        self.serverName: str = ""
        self.coreFileName: str = ""
        self.javaPath: str = ""
        self.minMem: int = 0
        self.maxMem: int = 0
        self.memUnit: str = "M"
        self.jvmArg: list[str] = [""]
        self.outputDecoding: str = "utf-8"
        self.inputEncoding: str = "utf-8"
        # self.icon = serverConfig['icon']  不需要。

    def initialize(self, index: int):
        serverConfig: dict = readGlobalServerConfig()[index]
        self.serverName = serverConfig["name"]
        self.coreFileName = serverConfig["core_file_name"]
        self.javaPath = serverConfig["java_path"]
        self.minMem = serverConfig["min_memory"]
        self.maxMem = serverConfig["max_memory"]
        self.memUnit = serverConfig["memory_unit"]
        self.jvmArg = serverConfig["jvm_arg"]
        self.outputDecoding = serverConfig["output_decoding"]
        self.inputEncoding = serverConfig["input_encoding"]
        self.translateCoding()
    
    def translateCoding(self):
        if self.outputDecoding == "follow":
            self.outputDecoding = settingsController.fileSettings['outputDeEncoding']
        if self.inputEncoding == "follow":  # 跟随全局
            self.inputEncoding = settingsController.fileSettings['inputDeEncoding']
            if self.inputEncoding == "follow":  # 跟随输出
                self.inputEncoding = self.outputDecoding
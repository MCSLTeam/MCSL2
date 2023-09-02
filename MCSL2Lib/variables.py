#     Copyright 2023, MCSL Team, mailto:lxhtt@vip.qq.com
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

from MCSL2Lib.Controllers.settingsController import SettingsController
from MCSL2Lib.publicFunctions import readGlobalServerConfig, warning
from MCSL2Lib.singleton import Singleton

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
        self.consoleDeEncodingList = ["follow", "utf-8", "GB18030", "ansi"]
        self.memUnitList = ["M", "G"]
        self.jvmArg: list[str] = [""]
        self.serverName: str = ""
        self.serverType = ""
        self.extraData = {}

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
        self.serverType = ""
        self.extraData = {}


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

        self.consoleDeEncodingList = ["follow", "utf-8", "GB18030", "ansi"]
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

        self.oldServerType = ""
        self.serverType = ""
        self.oldExtraData = {}
        self.extraData = {}

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

        self.serverType = ""
        self.extraData.clear()


class GlobalMCSL2Variables:
    """需要被全局使用的变量"""

    MCSL2Version = "2.2.2.0"
    scrollAreaViewportQss = "background-color: transparent;"
    MinecraftBuiltInCommand = [
        "advancement",
        "attribute",
        "ban",
        "ban-ip",
        "banlist",
        "bossbar",
        "clear",
        "clone",
        "damage",
        "data",
        "datapack",
        "debug",
        "defaultgamemode",
        "deop",
        "difficulty",
        "effect",
        "enchant",
        "execute",
        "experience",
        "fill",
        "fillbiome",
        "forceload",
        "function",
        "gamemode",
        "gamerule",
        "give",
        "item",
        "jfr",
        "kick",
        "kill",
        "list",
        "locate",
        "loot",
        "me",
        "minecraft:help",
        "minecraft:reload",
        "msg",
        "op",
        "pardon",
        "pardon-ip",
        "particle",
        "perf",
        "place",
        "playsound",
        "recipe",
        "return",
        "ride",
        "save-all",
        "save-off",
        "save-on",
        "say",
        "schedule",
        "scoreboard",
        "seed",
        "setblock",
        "setidletimeout",
        "setworldspawn",
        "spawnpoint",
        "spectate",
        "spreadplayers",
        "stop",
        "stopsound",
        "summon",
        "tag",
        "team",
        "teammsg",
        "teleport",
        "tell",
        "tellraw",
        "time",
        "title",
        "tm",
        "tp",
        "trigger",
        "w",
        "weather",
        "whitelist",
        "worldborder",
        "xp",
    ]
    userCommandHistory = []
    upT = 0
    darkWarnBtnStyleSheet = (
        "PushButton {\n"
        "    color: black;\n"
        "    background: rgba(255, 255, 255, 0.7);\n"
        "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
        "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
        "    border-radius: 5px;\n"
        "    /* font: 14px 'Segoe UI', 'Microsoft YaHei'; */\n"
        "    padding: 5px 12px 6px 12px;\n"
        "    outline: none;\n"
        "}\n"
        "QPushButton {\n"
        "    background-color: rgba(255, 117, 117, 30%);\n"
        "    color: rgb(245, 0, 0)\n"
        "}\n"
        "QPushButton:hover {\n"
        "    background-color: rgba(255, 122, 122, 50%);\n"
        "    color: rgb(245, 0, 0)\n"
        "}\n"
        "QPushButton:disabled {\n"
        "    background-color: transparent\n"
        "}"
    )
    lightWarnBtnStyleSheet = (
        "PushButton {\n"
        "    color: black;\n"
        "    background: rgba(255, 255, 255, 0.7);\n"
        "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
        "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
        "    border-radius: 5px;\n"
        "    /* font: 14px 'Segoe UI', 'Microsoft YaHei'; */\n"
        "    padding: 5px 12px 6px 12px;\n"
        "    outline: none;\n"
        "}\n"
        "QPushButton {\n"
        "    background-color: rgba(255, 117, 117, 30%);\n"
        "    color: rgb(255, 0, 0)\n"
        "}\n"
        "QPushButton:hover {\n"
        "    background-color: rgba(255, 122, 122, 50%);\n"
        "    color: rgb(255, 0, 0)\n"
        "}\n"
        "QPushButton:disabled {\n"
        "    background-color: transparent\n"
        "}"
    )
    isLoadFinished: bool = False
    installingPluginArchiveDirectory: str = ""


@Singleton
class DownloadVariables:
    """下载页需要的变量"""

    def __init__(self):
        self.MCSLAPIDownloadUrlDict = {}
        self.FastMirrorAPIDict = {}
        self.FastMirrorAPICoreVersionDict = {}
        self.selectedName: str = ""
        self.selectedMCVersion: str = ""
        self.FastMirrorReplaceTagDict = {
            "proxy": "代理",
            "vanilla": "原版",
            "pure": "纯净",
            "mod": "模组",
            "bedrock": "基岩",
        }


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
        self.serverProperties = {}
        self.serverType: str = ""
        self.extraData = {}

    @warning("要为所有ServerVariables添加serverType和extraData属性")
    def initialize(self, index: int):
        self.serverConfig: dict = readGlobalServerConfig()[index]
        self.serverName = self.serverConfig["name"]
        self.coreFileName = self.serverConfig["core_file_name"]
        self.javaPath = self.serverConfig["java_path"]
        self.minMem = self.serverConfig["min_memory"]
        self.maxMem = self.serverConfig["max_memory"]
        self.memUnit = self.serverConfig["memory_unit"]
        self.jvmArg = self.serverConfig["jvm_arg"]
        self.outputDecoding = self.serverConfig["output_decoding"]
        self.inputEncoding = self.serverConfig["input_encoding"]
        self.translateCoding()
        try:
            self.serverType = self.serverConfig["server_type"]
            self.extraData = self.serverConfig["extra_data"]
        except KeyError:
            self.serverType = ""
            self.extraData = {}
            pass

    def translateCoding(self):
        if self.outputDecoding == "follow":
            self.outputDecoding = settingsController.fileSettings["outputDeEncoding"]
        if self.inputEncoding == "follow":  # 跟随全局
            self.inputEncoding = settingsController.fileSettings["inputDeEncoding"]
            if self.inputEncoding == "follow":  # 跟随输出
                self.inputEncoding = self.outputDecoding


@Singleton
class SettingsVariables:
    """设置相关"""

    def __init__(self):
        self.newServerTypeList = ["Default", "Noob", "Extended", "Import"]
        self.downloadSourceList = ["FastMirror", "MCSLAPI"]
        self.saveSameFileExceptionList = ["ask", "overwrite", "stop"]
        self.outputDeEncodingList = ["utf-8", "GB18030", "ansi"]
        self.inputDeEncodingList = ["follow", "utf-8", "GB18030", "ansi"]
        self.themeList = ["auto", "dark", "light"]

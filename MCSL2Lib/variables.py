#     Copyright 2024, MCSL Team, mailto:services@mcsl.com.cn
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

from MCSL2Lib.ProgramControllers.settingsController import cfg
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.utils import readGlobalServerConfig


class BaseServerVariables:
    """服务器变量基类"""

    def __init__(self):
        self.javaPath: list = []
        self.minMem: int
        self.maxMem: int
        self.memUnit: str = ""
        self.corePath: str = ""
        self.coreFileName: str = ""
        self.selectedJavaPath: str = ""
        self.selectedJavaVersion: str = ""
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"
        self.consoleDeEncodingList = ["follow", "utf-8", "GB18030", "ansi"]
        self.memUnitList = ["M", "G"]
        self.jvmArg: list[str] = [""]
        self.serverName: str = ""
        self.serverType = ""
        self.extraData = {}
        """
        self.extraData maybe like this:

        self.extraData = {
            'mc_version' : ...,
            'build_version' : ...,
            ...
        }
        """

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
class ConfigureServerVariables(BaseServerVariables):
    """新建服务器所需变量"""

    pass


@Singleton
class EditServerVariables(BaseServerVariables):
    """修改服务器所需变量"""

    def __init__(self):
        super().__init__()
        self.oldMinMem: int
        self.oldMaxMem: int
        self.oldCoreFileName: str = ""
        self.oldSelectedJavaPath: str = ""
        self.oldMemUnit: str = ""
        self.oldJVMArg: list[str] = [""]
        self.oldServerName: str = ""
        self.oldConsoleOutputDeEncoding: str = "follow"
        self.oldConsoleInputDeEncoding: str = "follow"
        self.oldServerType = ""
        self.oldExtraData = {}
        self.oldIcon: str = "Grass.png"

        self.icon: str = "Grass.png"

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
            "Spigot.png",
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
        self.icon: str = "Grass.png"
        super().resetToDefault()


class GlobalMCSL2Variables:
    """需要被全局使用的变量"""

    devMode = False
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
        self.PolarTypeDict = {}
        self.PolarCoreDict = {}
        self.AkiraTypeList = []
        self.AkiraCoreDict = {}


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
        self.serverIconName: str = "Grass.png"
        self.serverType: str = ""
        self.extraData = {}

    def initialize(self, index: int) -> "ServerVariables":
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
        self.serverIconName = serverConfig["icon"]
        self.translateCoding()
        try:
            self.serverType = serverConfig["server_type"]
            self.extraData = serverConfig["extra_data"]
        except KeyError:
            self.serverType = ""
            self.extraData = {}
            pass
        return self

    def translateCoding(self):
        if self.outputDecoding == "follow":
            self.outputDecoding = cfg.get(cfg.outputDeEncoding)
        if self.inputEncoding == "follow":  # 跟随全局
            self.inputEncoding = cfg.get(cfg.inputDeEncoding)
            if self.inputEncoding == "follow":  # 跟随输出
                self.inputEncoding = self.outputDecoding


@Singleton
class SettingsVariables:
    """设置相关"""

    def __init__(self):
        self.newServerTypeList = ["Default", "Noob", "Extended", "Import"]
        self.downloadSourceList = ["FastMirror", "MCSLAPI", "PolarsAPI", "AkiraCloud"]
        self.downloadSourceTextList = [
            "FastMirror 镜像站",
            "MCSLAPI",
            "极星·镜像站",
            "Akira Cloud 镜像站",
        ]
        self.saveSameFileExceptionList = ["ask", "overwrite", "stop"]
        self.outputDeEncodingList = ["utf-8", "GB18030", "ansi"]
        self.inputDeEncodingList = ["follow", "utf-8", "GB18030", "ansi"]
        self.themeList = ["auto", "dark", "light"]


class ImportVariables:
    codingList = ["utf-8", "GB18030", "ansi"]


@Singleton
class MCSLv1ImportVariables:
    """MCSL 1 导入"""

    def __init__(self):
        self.executableFilePath: str = ""
        self.executableFileDir: str = ""
        self.commandStr: str = ""
        self.java: str = ""
        self.minMem: int = 0
        self.maxMem: int = 0
        self.coreFileName: str = "server.jar"
        self.serverName: str = ""
        self.memUnit: str = ""
        self.jvmArg: list[str] = [
            "-XX:+UnlockExperimentalVMOptions",
            "-XX:+DisableExplicitGC",
            "-XX:+AlwaysPreTouch",
            "-XX:+ParallelRefProcEnabled",
        ]
        self.consoleDeEncodingList = ["follow", "utf-8", "GB18030", "ansi"]
        self.memUnitList = ["M", "G"]
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"

    def resetToDefault(self):
        self.executableFilePath: str = ""
        self.executableFileDir: str = ""
        self.commandStr: str = ""
        self.java: str = ""
        self.minMem: int = 0
        self.maxMem: int = 0
        self.serverName: str = ""
        self.memUnit: str = ""
        self.consoleOutputDeEncoding: str = "follow"
        self.consoleInputDeEncoding: str = "follow"

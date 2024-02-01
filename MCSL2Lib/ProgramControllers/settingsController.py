#     Copyright 2024, MCSL Team, mailto:lxhtt@vip.qq.com
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
Settings controller, for editing MCSL2's configurations.
"""

from qfluentwidgets import (
    QConfig,
    ConfigItem,
    OptionsConfigItem,
    OptionsValidator,
    RangeConfigItem,
    RangeValidator,
    BoolValidator,
)


class Aria2Range(RangeConfigItem):
    @property
    def range(self):
        """get the available range of config"""
        return [1, 128]


class Config(QConfig):
    """MCSL2 Configuration"""

    # Server
    autoRunLastServer = ConfigItem("Server", "autoRunLastServer", False, BoolValidator())
    acceptAllMojangEula = ConfigItem("Server", "acceptAllMojangEula", False, BoolValidator())
    sendStopInsteadOfKill = ConfigItem("Server", "sendStopInsteadOfKill", True, BoolValidator())
    restartServerWhenCrashed = ConfigItem(
        "Server", "restartServerWhenCrashed", False, BoolValidator()
    )
    # Configure server

    newServerType = OptionsConfigItem(
        "ConfigureServer",
        "newServerType",
        "Default",
        OptionsValidator(["Default", "Noob", "Extended", "Import"]),
    )
    onlySaveGlobalServerConfig = ConfigItem(
        "ConfigureServer", "onlySaveGlobalServerConfig", False, BoolValidator()
    )
    clearAllNewServerConfigInProgram = ConfigItem(
        "ConfigureServer", "clearAllNewServerConfigInProgram", False, BoolValidator()
    )

    # Download
    downloadSource = OptionsConfigItem(
        "Download",
        "downloadSource",
        "FastMirror",
        OptionsValidator(["FastMirror", "MCSLAPI", "PolarsAPI", "AkiraCloud"]),
    )
    alwaysAskSaveDirectory = ConfigItem(
        "Download", "alwaysAskSaveDirectory", False, BoolValidator()
    )
    aria2Thread = Aria2Range(
        "Download",
        "aria2Thread",
        8,
        validator=RangeValidator(min=1, max=128),
    )
    saveSameFileException = OptionsConfigItem(
        "Download",
        "saveSameFileException",
        "ask",
        OptionsValidator(["ask", "overwrite", "stop"]),
    )

    # Console
    outputDeEncoding = OptionsConfigItem(
        "Console",
        "outputDeEncoding",
        "ansi",
        OptionsValidator(["utf-8", "GB18030", "ansi"]),
    )
    inputDeEncoding = OptionsConfigItem(
        "Console",
        "inputDeEncoding",
        "follow",
        OptionsValidator(["follow", "utf-8", "GB18030", "ansi"]),
    )
    quickMenu = ConfigItem("Console", "quickMenu", True, BoolValidator())
    clearConsoleWhenStopServer = ConfigItem(
        "Console", "clearConsoleWhenStopServer", False, BoolValidator()
    )
    # Software
    # themeMode = OptionsConfigItem(
    # "QFluentWidgets", "ThemeMode", Theme.LIGHT, OptionsValidator(Theme), EnumSerializer(Theme))
    # themeColor = ColorConfigItem("QFluentWidgets", "ThemeColor", '#009faa')
    alwaysRunAsAdministrator = ConfigItem(
        "Software", "alwaysRunAsAdministrator", False, BoolValidator()
    )
    startOnStartup = ConfigItem("Software", "startOnStartup", False, BoolValidator())
    # Update
    checkUpdateOnStart = ConfigItem("Update", "checkUpdateOnStart", False, BoolValidator())
    # Other
    enableExperimentalFeatures = ConfigItem(
        "Other", "enableExperimentalFeatures", False, BoolValidator()
    )
    lastServer = ConfigItem("Other", "lastServer", "", "")
    oldExecuteable = ConfigItem("Other", "oldExecuteable", "", "")
    # lastWindowSize = ConfigItem(
    #     "Other", "lastWindowSize", [None, None]
    # )


cfg = Config()

if cfg.get(cfg.autoRunLastServer):
    cfg.set(cfg.autoRunLastServer, False)
if cfg.get(cfg.sendStopInsteadOfKill):
    cfg.set(cfg.sendStopInsteadOfKill, True)
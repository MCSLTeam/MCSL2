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
Settings controller, for editing MCSL2's configurations.
"""

import platform
from qfluentwidgets import (
    QConfig,
    ConfigItem,
    OptionsConfigItem,
    OptionsValidator,
    RangeConfigItem,
    RangeValidator,
    BoolValidator,
    ColorConfigItem,
    Theme,
    EnumSerializer,
)


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
        OptionsValidator(["FastMirror", "MCSLSync", "PolarsAPI", "RainYun"]),
    )
    alwaysAskSaveDirectory = ConfigItem(
        "Download", "alwaysAskSaveDirectory", False, BoolValidator()
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
        "ansi" if platform.system() == "Windows" else "utf-8",
        OptionsValidator(
            ["utf-8", "GB18030", "ansi"]
            if platform.system().lower() == "windows"
            else ["utf-8", "GB18030"]
        ),
    )
    inputDeEncoding = OptionsConfigItem(
        "Console",
        "inputDeEncoding",
        "follow",
        OptionsValidator(
            ["utf-8", "GB18030", "ansi"]
            if platform.system().lower() == "windows"
            else ["utf-8", "GB18030"]
        ),
    )
    quickMenu = ConfigItem("Console", "quickMenu", True, BoolValidator())
    clearConsoleWhenStopServer = ConfigItem(
        "Console", "clearConsoleWhenStopServer", False, BoolValidator()
    )

    # Software
    themeMode = OptionsConfigItem(
    "QFluentWidgets", "ThemeMode", Theme.AUTO, OptionsValidator(Theme), EnumSerializer(Theme))
    themeColor = ColorConfigItem("QFluentWidgets", "ThemeColor", '#19e8a2')
    alwaysRunAsAdministrator = ConfigItem(
        "Software", "alwaysRunAsAdministrator", False, BoolValidator()
    )
    startOnStartup = ConfigItem("Software", "startOnStartup", False, BoolValidator())
    # Update
    checkUpdateOnStart = ConfigItem("Update", "checkUpdateOnStart", False, BoolValidator())

    # Download Advanced
    downloadThreads = RangeConfigItem(
        "Download",
        "downloadThreads",
        16,
        validator=RangeValidator(min=1, max=256),
    )

    # Force Parallel Download
    forceParallelDownload = ConfigItem("Download", "forceParallelDownload", False, BoolValidator())

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

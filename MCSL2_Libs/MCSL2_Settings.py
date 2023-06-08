from json import loads, dumps
from os import path as ospath

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from MCSL2_Libs.MCSL2_Logger import MCSL2Logger


class MCSL2Settings:
    def __init__(self):
        self.NeedUpdateConfigFile = 0
        self.ConfigList = ["AutoRunLastServer", "AcceptAllMojangEula", "SendStopInsteadOfKill", "AddServerMode",
                           "OnlySaveGlobalServerConfig", "MCSLAPIDownloadSource", "Aria2Thread",
                           "AlwaysAskSaveDirectory", "SaveSameFileException", "EnableConsoleQuickMenu",
                           "ConsoleOutputEncoding", "ConsoleInputDecoding", "BackgroundTransparency",
                           "UseTitleBarInsteadOfmacOSControlling", "ThemeMode", "StartOnStartup",
                           "AlwaysRunAsAdministrator", "LastUpdateTime"]
        if ospath.exists(r"./MCSL2/MCSL2_Config.json"):
            if ospath.getsize(r"./MCSL2/MCSL2_Config.json") != 0:
                with open(r"./MCSL2/MCSL2_Config.json", "r", encoding="utf-8") as ReadConfig:
                    self.ConfigJSON = loads(ReadConfig.read())
                    ReadConfig.close()
                    try:
                        self.AutoRunLastServer = self.ConfigJSON["auto_run_last_server"]
                    except KeyError:
                        self.AutoRunLastServer = False
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.AcceptAllMojangEula = self.ConfigJSON["accept_all_mojang_eula"]
                    except KeyError:
                        self.AcceptAllMojangEula = False
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.SendStopInsteadOfKill = self.ConfigJSON["send_stop_instead_of_kill"]
                    except KeyError:
                        self.SendStopInsteadOfKill = True
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.AddServerMode = self.ConfigJSON["add_server_mode"]
                    except KeyError:
                        self.AddServerMode = "Default"
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.OnlySaveGlobalServerConfig = self.ConfigJSON["only_save_global_server_config"]
                    except KeyError:
                        self.OnlySaveGlobalServerConfig = False
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.MCSLAPIDownloadSource = self.ConfigJSON["mcslapi_download_source"]
                    except KeyError:
                        self.MCSLAPIDownloadSource = "SharePoint"
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.Aria2Thread = self.ConfigJSON["aria2_thread"]
                    except KeyError:
                        self.Aria2Thread = 8
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.AlwaysAskSaveDirectory = self.ConfigJSON["always_ask_save_directory"]
                    except KeyError:
                        self.AlwaysAskSaveDirectory = True
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.SaveSameFileException = self.ConfigJSON["save_same_file_exception"]
                    except KeyError:
                        self.SaveSameFileException = "ask"
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.EnableConsoleQuickMenu = self.ConfigJSON["enable_console_quick_menu"]
                    except KeyError:
                        self.EnableConsoleQuickMenu = True
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.ConsoleOutputEncoding = self.ConfigJSON["console_output_encoding"]
                    except KeyError:
                        self.ConsoleOutputEncoding = "utf-8"
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.ConsoleInputDecoding = self.ConfigJSON["console_input_decoding"]
                    except KeyError:
                        self.ConsoleInputDecoding = "follow"
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.BackgroundTransparency = self.ConfigJSON["background_transparency"]
                    except KeyError:
                        self.BackgroundTransparency = 55
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.UseTitleBarInsteadOfmacOSControlling = self.ConfigJSON["use_title_bar_instead_of_macos_controlling"]
                    except KeyError:
                        self.UseTitleBarInsteadOfmacOSControlling = False
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.ThemeMode = self.ConfigJSON["theme_mode"]
                    except KeyError:
                        self.ThemeMode = "light"
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.StartOnStartup = self.ConfigJSON["start_on_startup"]
                    except KeyError:
                        self.StartOnStartup = False
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.AlwaysRunAsAdministrator = self.ConfigJSON["always_run_as_administrator"]
                    except KeyError:
                        self.AlwaysRunAsAdministrator = False
                        self.NeedUpdateConfigFile = 1
                        pass
                    try:
                        self.LastUpdateTime = self.ConfigJSON["last_update_time"]
                    except KeyError:
                        self.LastUpdateTime = "unknown"
                        self.NeedUpdateConfigFile = 1
                    if self.NeedUpdateConfigFile == 1:
                        self.SaveConfig()
                    else:
                        pass
            else:
                with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as InitConfig:
                    ConfigTemplate = {
                        "auto_run_last_server": False,
                        "accept_all_mojang_eula": False,
                        "send_stop_instead_of_kill": True,
                        "add_server_mode": "Default",
                        "only_save_global_server_config": False,
                        "mcslapi_download_source": "SharePoint",
                        "aria2_thread": 8,
                        "always_ask_save_directory": True,
                        "save_same_file_exception": "ask",
                        "enable_console_quick_menu": True,
                        "console_output_encoding": "utf-8",
                        "console_input_decoding": "follow",
                        "background_transparency": 55,
                        "use_title_bar_instead_of_macos_controlling": False,
                        "theme_mode": "light",
                        "start_on_startup": False,
                        "always_run_as_administrator": False,
                        "last_update_time": "unknown"
                    }
                    InitConfig.write(dumps(ConfigTemplate))
                    InitConfig.close()
        else:
            self.AutoRunLastServer = False
            self.AcceptAllMojangEula = False
            self.SendStopInsteadOfKill = True
            self.AddServerMode = "Default"
            self.OnlySaveGlobalServerConfig = False
            self.MCSLAPIDownloadSource = "SharePoint"
            self.Aria2Thread = 8
            self.AlwaysAskSaveDirectory = True
            self.SaveSameFileException = "ask"
            self.EnableConsoleQuickMenu = True
            self.ConsoleOutputEncoding = "utf-8"
            self.ConsoleInputDecoding = "follow"
            self.BackgroundTransparency = 55
            self.UseTitleBarInsteadOfmacOSControlling = False
            self.ThemeMode = "light"
            self.StartOnStartup = False
            self.AlwaysRunAsAdministrator = False
            self.LastUpdateTime = "unknown"

    def GetConfig(self, Type):
        if Type in self.ConfigList:
            return getattr(self, Type)
        else:
            return None

    def ChangeConfig(self, Type, Arg):
        if Type == "AutoRunLastServer":
            self.AutoRunLastServer = Arg
        elif Type == "AcceptAllMojangEula":
            self.AcceptAllMojangEula = Arg
        elif Type == "SendStopInsteadOfKill":
            self.SendStopInsteadOfKill = Arg
        elif Type == "AddServerMode":
            self.AddServerMode = Arg
        elif Type == "OnlySaveGlobalServerConfig":
            self.OnlySaveGlobalServerConfig = Arg
        elif Type == "MCSLAPIDownloadSource":
            self.MCSLAPIDownloadSource = Arg
        elif Type == "Aria2Thread":
            self.Aria2Thread = Arg
        elif Type == "AlwaysAskSaveDirectory":
            self.AlwaysAskSaveDirectory = Arg
        elif Type == "SaveSameFileException":
            self.SaveSameFileException = Arg
        elif Type == "EnableConsoleQuickMenu":
            self.EnableConsoleQuickMenu = Arg
        elif Type == "ConsoleOutputEncoding":
            self.ConsoleOutputEncoding = Arg
        elif Type == "ConsoleInputDecoding":
            self.ConsoleInputDecoding = Arg
        elif Type == "BackgroundTransparency":
            self.BackgroundTransparency = Arg
        elif Type == "UseTitleBarInsteadOfmacOSControlling":
            self.UseTitleBarInsteadOfmacOSControlling = Arg
        elif Type == "ThemeMode":
            self.ThemeMode = Arg
        elif Type == "StartOnStartup":
            self.StartOnStartup = Arg
        elif Type == "AlwaysRunAsAdministrator":
            self.AlwaysRunAsAdministrator = Arg
        elif Type == "LastUpdateTime":
            self.LastUpdateTime = Arg
        else:
            pass
        self.SaveConfig()

    def SaveConfig(self):
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as UpdateConfig:
            NewConfig = {
                "auto_run_last_server": self.AutoRunLastServer,
                "accept_all_mojang_eula": self.AcceptAllMojangEula,
                "send_stop_instead_of_kill": self.SendStopInsteadOfKill,
                "add_server_mode": self.AddServerMode,
                "only_save_global_server_config": self.OnlySaveGlobalServerConfig,
                "mcslapi_download_source": self.MCSLAPIDownloadSource,
                "aria2_thread": self.Aria2Thread,
                "always_ask_save_directory": self.AlwaysAskSaveDirectory,
                "save_same_file_exception": self.SaveSameFileException,
                "enable_console_quick_menu": self.EnableConsoleQuickMenu,
                "console_output_encoding": self.ConsoleOutputEncoding,
                "console_input_decoding": self.ConsoleInputDecoding,
                "background_transparency": self.BackgroundTransparency,
                "use_title_bar_instead_of_macos_controlling": self.UseTitleBarInsteadOfmacOSControlling,
                "theme_mode": self.ThemeMode,
                "start_on_startup": self.StartOnStartup,
                "always_run_as_administrator": self.AlwaysRunAsAdministrator,
                "last_update_time": self.LastUpdateTime
            }
            UpdateConfig.write(dumps(NewConfig))
            UpdateConfig.close()

def OpenWebUrl(Url, LogFilesCount):
    QDesktopServices.openUrl(QUrl(Url))
    MCSL2Logger("OpenWebBrowser", MsgArg=f"链接：\n{Url}", MsgLevel=0, LogFilesCount=LogFilesCount).Log()
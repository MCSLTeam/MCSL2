from json import loads, dumps


class MCSL2Settings:
    def __init__(self):
        with open(r"./MCSL2/MCSL2_Config.json", "r", encoding="utf-8") as ReadConfig:
            self.ConfigJSON = loads(ReadConfig.read())
            self.AutoRunLastServer = self.ConfigJSON["auto_run_last_server"]
            self.AcceptAllMojangEula = self.ConfigJSON["accept_all_mojang_eula"]
            self.SendStopInsteadOfKill = self.ConfigJSON["send_stop_instead_of_kill"]
            self.AddServerMode = self.ConfigJSON["add_server_mode"]
            self.OnlySaveGlobalServerConfig = self.ConfigJSON["only_save_global_server_config"]
            self.MCSLAPIDownloadSource = self.ConfigJSON["mcslapi_download_source"]
            self.Aria2Thread = self.ConfigJSON["aria2_thread"]
            self.AlwaysAskSaveDirectory = self.ConfigJSON["always_ask_save_directory"]
            self.SaveSameFileException = self.ConfigJSON["save_same_file_exception"]
            self.EnableConsoleQuickMenu = self.ConfigJSON["enable_console_quick_menu"]
            self.ConsoleOutputEncoding = self.ConfigJSON["console_output_encoding"]
            self.ConsoleInputDecoding = self.ConfigJSON["console_input_decoding"]
            self.BackgroundTransparency = self.ConfigJSON["background_transparency"]
            self.ExchangeWindowControllingButtons = self.ConfigJSON["exchange_window_controlling_buttons"]
            self.ThemeMode = self.ConfigJSON["thememode"]
            self.StartOnStartup = self.ConfigJSON["start_on_startup"]
            self.AlwaysRunAsAdministrator = self.ConfigJSON["always_run_as_administrator"]
            self.LastUpdateTime = self.ConfigJSON["last_update_time"]
            ReadConfig.close()
            self.ConfigList = ["AutoRunLastServer", "AcceptAllMojangEula", "SendStopInsteadOfKill", "AddServerMode",
                               "OnlySaveGlobalServerConfig", "MCSLAPIDownloadSource", "Aria2Thread",
                               "AlwaysAskSaveDirectory", "SaveSameFileException", "EnableConsoleQuickMenu",
                               "ConsoleOutputEncoding", "ConsoleInputDecoding", "BackgroundTransparency",
                               "ExchangeWindowControllingButtons", "DarkMode", "StartOnStartup",
                               "AlwaysRunAsAdministrator", "LastUpdateTime"]

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
        elif Type == "ExchangeWindowControllingButtons":
            self.ExchangeWindowControllingButtons = Arg
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
                "exchange_window_controlling_buttons": self.ExchangeWindowControllingButtons,
                "thememode": self.ThemeMode,
                "start_on_startup": self.StartOnStartup,
                "always_run_as_administrator": self.AlwaysRunAsAdministrator,
                "last_update_time": self.LastUpdateTime
            }
            UpdateConfig.write(dumps(NewConfig))
            UpdateConfig.close()
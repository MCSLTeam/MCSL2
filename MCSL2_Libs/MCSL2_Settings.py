from json import loads


class MCSL2Settings:
    def __init__(self):
        with open(r"./MCSL2/MCSL2_Config.json", "r", encoding="utf-8") as ReadConfig:
            ConfigJSON = loads(ReadConfig.read())
            self.AutoRunLastServer = ConfigJSON["auto_run_last_server"]
            self.AcceptAllMojangEula = ConfigJSON["accept_all_mojang_eula"]
            self.SendStopInsteadOfKill = ConfigJSON["send_stop_instead_of_kill"]
            self.AddServerMode = ConfigJSON["add_server_mode"]
            self.OnlySaveGlobalServerConfig = ConfigJSON["only_save_global_server_config"]
            self.MCSLAPIDownloadSource = ConfigJSON["mcslapi_download_source"]
            self.Aria2Thread = ConfigJSON["aria2_thread"]
            self.AlwaysAskSaveDirectory = ConfigJSON["always_ask_save_directory"]
            self.SaveSameFileException = ConfigJSON["save_same_file_exception"]
            self.EnableConsoleQuickMenu = ConfigJSON["enable_console_quick_menu"]
            self.ConsoleOutputEncoding = ConfigJSON["console_output_encoding"]
            self.ConsoleInputDecoding = ConfigJSON["console_input_decoding"]
            self.BackgroundTransparency = ConfigJSON["background_transparency"]
            self.ExchangeWindowControllingButtons = ConfigJSON["exchange_window_controling_buttons"]
            self.DarkMode = ConfigJSON["darkmode"]
            self.StartOnStartup = ConfigJSON["always_run_as_administrator"]
            self.LastUpdateTime = ConfigJSON["last_update_time"]
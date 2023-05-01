from json import dumps
from os import mkdir, path as ospath, listdir

from MCSL2_Libs.MCSL2_Logger import MCSL2Logger


def InitMCSL():
    if not ospath.exists(r"Servers"):
        mkdir(r"./Servers")
        MCSL2Logger("无Servers文件夹，创建", MsgArg=None, MsgLevel=0, LogFilesCount=len(listdir(r"MCSL2/Logs"))).Log()
    if not ospath.exists(r"MCSL2"):
        MCSL2Logger("程序执行InitMCSL()初始化中...", MsgArg=None, MsgLevel=0, LogFilesCount=len(listdir(r"MCSL2/Logs"))).Log()
        mkdir(r"MCSL2")
        mkdir(r"MCSL2/Logs")
        mkdir(r"MCSL2/Aria2")
        mkdir(r"MCSL2/Downloads")
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
                "exchange_window_controlling_buttons": False,
                "darkmode": "light",
                "start_on_startup": False,
                "always_run_as_administrator": False,
                "last_update_time": "unknown"
            }
            InitConfig.write(dumps(ConfigTemplate))
            InitConfig.close()
        with open(
                r"./MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
        ) as InitServerList:
            ServerListTemplate = '{\n  "MCSLServerList": [\n\n  ]\n}'
            InitServerList.write(ServerListTemplate)
            InitServerList.close()
    elif not ospath.exists(r"MCSL2/Aria2"):
        mkdir(r"MCSL2/Aria2")
        if not ospath.exists(r"MCSL2/Logs"):
            mkdir(r"MCSL2/Logs")
        if not ospath.exists(r"MCSL2/Downloads"):
            mkdir(r"MCSL2/Downloads")
            pass
    elif not ospath.exists(r"MCSL2/Logs"):
        mkdir(r"MCSL2/Logs")
        if not ospath.exists(r"MCSL2/Downloads"):
            mkdir(r"MCSL2/Downloads")
            pass
    elif not ospath.exists(r"MCSL2/Downloads"):
        mkdir(r"MCSL2/Downloads")
        pass
    else:
        pass
    return len(listdir(r"MCSL2/Logs"))
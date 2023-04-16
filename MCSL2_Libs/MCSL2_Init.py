from os import mkdir, path as ospath, listdir


def InitMCSL():
    global LogFilesCount
    if not ospath.exists(r"MCSL2"):
        LogFilesCount = 0
        mkdir(r"MCSL2")
        mkdir(r"MCSL2/Logs")
        mkdir(r"MCSL2/Aria2")
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as InitConfig:
            ConfigTemplate = ""
            InitConfig.write(ConfigTemplate)
            InitConfig.close()
        with open(
                r"./MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
        ) as InitServerList:
            ServerListTemplate = '{\n  "MCSLServerList": [\n    {\n      "name": "MCSLReplacer",\n      ' \
                                 '"core_file_name": "MCSLReplacer",\n      "java_path": "MCSLReplacer",' \
                                 '\n      "min_memory": "MCSLReplacer",\n      "max_memory": "MCSLReplacer"\n    }\n  ' \
                                 ']\n} '
            InitServerList.write(ServerListTemplate)
            InitServerList.close()
        if not ospath.exists(r"Servers"):
            mkdir(r"./Servers")
        if not ospath.exists(r"MCSL2/Logs"):
            mkdir(r"MCSL2/Logs")
        pass
    else:
        LogFilesCount = len(listdir(r"MCSL2/Logs"))
        if not ospath.exists(r"Servers"):
            mkdir(r"./Servers")
        if not ospath.exists(r"MCSL2/Logs"):
            mkdir(r"MCSL2/Logs")
        pass

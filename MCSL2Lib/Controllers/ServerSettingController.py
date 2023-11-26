import hashlib
import json
import os
from json import JSONDecodeError


class ServerSettingController:
    _servers: dict = {}

    @classmethod
    def calcMD5(cls, serverName):
        if serverName not in cls._servers:
            return ""

        file = os.path.join(
            "MCSL2", "Servers", serverName, cls._servers.get(serverName)["core_file_name"]
        )
        try:
            with open(file, "rb") as f:
                md5 = hashlib.md5(f.read()).hexdigest()
            return md5
        except FileNotFoundError:
            return ""

    @classmethod
    def addServerConfig(cls, serverName, serverConfig):
        cls._servers.update({serverName: serverConfig})

    @classmethod
    def checkServerConfig(cls, serverName):
        if serverName not in cls._servers:
            return False
        return cls._checkServerConfig(cls._servers.get(serverName))

    @classmethod
    def _checkServerConfig(cls, config):
        # check server core md5
        if (t := config.get("core_md5")) != (md5 := cls.calcMD5(config.get("name"))):
            if md5 == "":
                return False  # 无法定位核心文件
            elif t is None:
                config["core_md5"] = md5
            else:
                return False  # 核心文件已被修改

        # check server config
        keys = {
            "core_file_name": str,
            "java_path": str,
            "min_memory": int,
            "max_memory": int,
            "memory_unit": str,
            "jvm_arg": list,
            "server_type": str,
            "output_decoding": str,
            "input_encoding": str,
            "icon": str,
        }
        configKeys = set(config.keys())
        # if configKeys contains all keys
        if set(keys.keys()).issubset(configKeys):
            for key, _type in keys.items():
                if not isinstance(config[key], _type):
                    return False
                if _type == str and config[key] == "":
                    return False
                if _type == int and config[key] <= 0:
                    return False

        return True

    @classmethod
    def load(cls):
        """
        加载服务器配置,包括服务器列表和服务器配置,并检查配置是否正确
        """
        # load server list
        if os.path.exists(p := os.path.join("MCSL2", "MCSL2_Servers.json")):
            with open(p, "r") as f:
                try:
                    cls._servers = json.load(f)
                except JSONDecodeError:
                    # make backup
                    f.close()
                    if os.path.exists(p := os.path.join("MCSL2", "MCSL2_Servers.json")):
                        os.rename(p, p + ".bak")
        elif os.path.exists(p := os.path.join("MCSL2", "MCSL2_ServerList.json")):  # 旧版兼容
            with open(p, "r") as f:
                try:
                    cls._servers = json.load(f)["MCSLServerList"]  # 旧版兼容
                    cls._servers = {e["name"]: e for e in cls._servers}  # 将旧版的List转为Dict
                except JSONDecodeError:
                    # make backup
                    f.close()
                    if os.path.exists(p := os.path.join("MCSL2", "MCSL2_ServerList.json")):
                        os.rename(p, p + ".bak")
        else:
            pass  # 默认为空
        # end load server list

        # check server list
        for idx, e in enumerate(cls._servers.copy()):
            if not cls.checkServerConfig(e["name"]):
                cls._servers[e["name"]] = None
        cls._servers = {k: v for k, v in cls._servers.items() if v is not None}
        # end check server list

        # load server config from dirs : MCSL2\Servers\*
        servers: dict = {}
        for e in os.listdir(p := os.path.join("MCSL2", "Servers")):
            if not os.path.isdir(os.path.join(p, e)):
                continue

            if os.path.exists(os.path.join(p, e, "MCSL2ServerConfig.json")):
                try:
                    with open(os.path.join(p, e, "MCSL2ServerConfig.json"), "r") as f:
                        servers.append(json.load(f))
                except:
                    pass

        # check server config
        for name, e in enumerate(servers.items()):
            if not cls._checkServerConfig(e):
                if servers.get(name) is not None:
                    pass
                else:
                    servers[name] = None  # 如果存在重名的服务器,则不添加
        servers = {k: v for k, v in servers.items() if v is not None}
        # end check server config

        # combine server config
        cls._servers = {**cls._servers, **servers}

    @classmethod
    def save(cls):
        # make backup
        if os.path.exists(p := os.path.join("MCSL2", "MCSL2_Servers.json")):
            os.rename(p, p + ".bak")
        with open(p, "w") as f:
            json.dump(cls._servers, f)

        # save server config
        for name, e in cls._servers.items():
            # 如果服务器文件夹不存在，则跳过
            if not os.path.exists(os.path.exists(p := os.path.join("MCSL2", "Servers", name))):
                continue
            os.rename(p, p + ".bak")
            with open(p, "w") as f:
                json.dump(e, f)

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("不要new这个啊啊啊啊啊啊啊啊啊啊啊啊啊啊")

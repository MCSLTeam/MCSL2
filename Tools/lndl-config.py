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
import traceback

from typing import Tuple
from lib_not_dr.nuitka import raw_config_type, nuitka_config_type


def get_version() -> Tuple[str, str]:
    # 尽量不要写死在构建脚本里
    # 用点邪门的方法
    VERSION = "2.0"
    BUILD_VERSION = "0.3"
    try:
        with open("./MCSL2Lib/__init__.py", "r", encoding="utf-8") as f:
            for line in f.readlines():
                if line.startswith("VERSION"):
                    VERSION = line.strip('BUILD_VERSION = "')[:-2]
                if line.startswith("BUILD_VERSION"):
                    BUILD_VERSION = line.strip('BUILD_VERSION = "')[:-2]
    except Exception:
        # 尽量不导入
        traceback.print_exc()
        from MCSL2Lib import VERSION, BUILD_VERSION
    return (VERSION, BUILD_VERSION)


def main(raw_config: raw_config_type) -> nuitka_config_type:
    config: nuitka_config_type = raw_config["cli"]  # type: ignore

    versions = get_version()
    config["product-version"] = versions[0]
    config["file-version"] = versions[1]

    return config

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
Update Controller
"""

import sys
from os import remove, execl

from MCSL2Lib.ProgramControllers.settingsController import cfg
from MCSL2Lib.variables import GlobalMCSL2Variables


def restart():
    """重启，在移动文件后调用(此代码在开发时不起作用)"""
    if GlobalMCSL2Variables.devMode:
        return
    else:
        execl(
            cfg.get(cfg.oldExecuteable),
            cfg.get(cfg.oldExecuteable),
            *sys.argv,
        )


def deleteOldMCSL2():
    """删除旧的，在更新重启后调用"""
    if GlobalMCSL2Variables.devMode:
        return
    else:
        try:
            remove(f"{sys.executable}.old")
        except Exception:
            pass
        try:
            remove("MCSL2Lib/verification.so.old")
        except Exception:
            pass
        try:
            remove("MCSL2Lib/verification.pyd.old")
        except Exception:
            pass

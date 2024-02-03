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
An example for MCSL2's plugin.
"""

# 提示：声明Plugin()时，声明的变量名称需与文件夹名、config.json的plugin_name键的值相同！

# 实现一个Plugin类
from Adapters.Plugin import Plugin

PluginExample = Plugin()


def load():
    """写你的代码"""
    print("load")


def enable():
    """写你的代码"""
    print("enable")


def disable():
    """写你的代码"""
    print("disable")


# 注册加载代码
PluginExample.register_loadFunc(load)

# 注册应用代码
PluginExample.register_enableFunc(enable)

# 注册应用代码
PluginExample.register_disableFunc(disable)

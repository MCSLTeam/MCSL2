#     Copyright 2023, MCSL Team, mailto:lxhtt@vip.qq.com
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
为了解决本地构建测试时缺少一些东西不能测试构建的问题
所以直接把一些参数放到这里来
"""
from .variables import GlobalMCSL2Variables

VERSION = GlobalMCSL2Variables.MCSL2Version

BUILD_VERSION = "0.1.0.0"

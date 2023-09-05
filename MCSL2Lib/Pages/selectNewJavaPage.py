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
Select Java page, for modifying exists Minecraft servers.
"""

from MCSL2Lib.Pages.selectJavaPage import SelectJavaPage
from MCSL2Lib.singleton import Singleton


@Singleton
class SelectNewJavaPage(SelectJavaPage):
    """适用于修改服务器时的选择Java页面"""

    def scrollAreaProcessor(self, JavaPath):
        """判断索引"""
        index = int(str(self.sender().objectName()).split("Btn")[1])
        selectedJavaPath = str(JavaPath[index].path)
        self.setJavaPath.emit(selectedJavaPath)

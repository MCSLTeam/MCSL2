# Copyright 2024, MCSL Team, mailto:services@mcsl.com.cn
#
# Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
# Licensed under the GNU General Public License, Version 3.0, with our
# additional agreements. (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
"""
雨云资源站
"""

from MCSL2Lib.ProgramControllers.DownloadAPI.AListAPI import (
    AListDownloadURLParser,
    FetchAListDownloadURLThreadFactory,
)


class RainYunDownloadURLParser(AListDownloadURLParser):
    def __init__(self):
        super().__init__(endPoint="https://mirrors.rainyun.com")

    def decodeDownloadJsons(
        self, APIUrl, path: str, pathPrefix: str = "/服务端合集"
    ):
        return super().decodeDownloadJsons(APIUrl, path, pathPrefix=pathPrefix)


# 雨云镜像站下载源工厂
RainYunParser = RainYunDownloadURLParser()
FetchRainYunThreadFactory = FetchAListDownloadURLThreadFactory(parser=RainYunParser)

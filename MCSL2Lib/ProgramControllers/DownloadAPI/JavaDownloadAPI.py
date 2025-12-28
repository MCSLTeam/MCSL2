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
Java 下载镜像站
"""

from MCSL2Lib.ProgramControllers.DownloadAPI.AListAPI import (
    AListDownloadURLParser,
    FetchAListDownloadURLThreadFactory,
)


class JavaDownloadURLParser(AListDownloadURLParser):
    def __init__(self):
        super().__init__(endPoint="https://drive.mcsl.com.cn")

    def decodeDownloadJsons(
        self, APIUrl, path: str, pathPrefix: str = "/Java-Mirror"
    ):
        return super().decodeDownloadJsons(APIUrl, path, pathPrefix=pathPrefix)


# Java 下载镜像站工厂
JavaDownloadParser = JavaDownloadURLParser()
FetchJavaDownloadThreadFactory = FetchAListDownloadURLThreadFactory(parser=JavaDownloadParser)

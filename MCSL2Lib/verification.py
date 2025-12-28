#     Copyright 2024, MCSL Team, mailto:lxhtt@vip.qq.com
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

from MCSL2Lib.ProgramControllers.networkController import MCSLNetworkSession
from os import getlogin, name as osname, getenv
from platform import system as sysType, processor
from hashlib import md5


def getAnnouncement():
    header = __AuthorizationHeaders.copy()
    header.update(MCSLNetworkSession.MCSLNetworkHeaders)
    return MCSLNetworkSession().get("https://api.mcsl.com.cn/getAnnouncement", headers=header).text


def checkUpdate():
    header = __AuthorizationHeaders.copy()
    header.update(MCSLNetworkSession.MCSLNetworkHeaders)
    return MCSLNetworkSession().get("https://api.mcsl.com.cn/checkUpdate", headers=header).json()


def countUserAPI():
    header = __AuthorizationHeaders.copy()
    header.update(MCSLNetworkSession.MCSLNetworkHeaders)
    return (
        MCSLNetworkSession()
        .post(
            f"https://api.mcsl.com.cn/countUser?Identification={generateUniqueCode()}",
            headers=header,
        )
        .text
    )


def checkPreviewPermission():
    return (
        MCSLNetworkSession()
        .get(
            f"https://api.mcsl.com.cn/checkPreviewAvailable?Identification={generateUniqueCode()}",
            headers=MCSLNetworkSession.MCSLNetworkHeaders,
        )
        .json()["available"]
    )


# fmt: off
def generateUniqueCode():
    return "-".join([md5(f"{getlogin() if osname == 'nt' else getenv('USER')}{processor()}{sysType()}".encode()).hexdigest()[i:i + 4].upper() for i in range(0, 16, 4)])  # noqa: E501
# fmt: on


__AuthorizationHeaders = {
    "x-mcsl2-client-private-header": "8f528e4214fe0142c301f0b92a7abea204a309fe5149f783765e9ab287c08367"  # noqa: E501
}

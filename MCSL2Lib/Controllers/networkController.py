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
A modified network session for bypassing system proxies in order to allow MCSL2
to access the network normally.
"""

from requests import Session
from MCSL2Lib import MCSL2VERSION
from platform import (
    system as systemType,
    architecture as systemArchitecture,
    version as systemVersion,
)


class MCSLNetworkSession(Session):
    def __init__(self):
        super().__init__()
        #: Trust environment settings for proxy configuration, default
        #: authentication and similar.
        self.trust_env = False


MCSLNetworkHeaders = {
    "User-Agent": f"MCServerLauncher2/{MCSL2VERSION} ({systemType()} {systemVersion()} {systemArchitecture()})"  # noqa: E501
}

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

    MCSLNetworkHeaders = {
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47 MCServerLauncher2/{MCSL2VERSION} ({systemType()} {systemVersion()}; {systemArchitecture()[0]})"  # noqa: E501
    }

    def __init__(self):
        super().__init__()
        #: Trust environment settings for proxy configuration, default
        #: authentication and similar.
        self.trust_env = False

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
from pyperclip import copy


def ParseUrl():
    Url = input().split("/")
    NewUrl = f"https://{Url[2]}/{Url[5]}/{Url[6]}/_layouts/52/download.aspx?share={Url[7].split('?')[0]}"
    print(
        f"结果: \n{NewUrl}\n--------------------------------------------------------------------------------"
    )
    copy(NewUrl)


while True:
    ParseUrl()

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

# by shenjackyuanjie
# 20231125
# 为啥就把 requirements.txt 删掉了 (恼)

import tomli

with open("pyproject.toml", "r", encoding="utf-8") as f:
    pyproject = tomli.loads(f.read())

with open("requirements.txt", "w", encoding="utf-8") as f:
    for dependency in pyproject["project"]["dependencies"]:
        print(dependency)
        f.write(dependency + "\n")

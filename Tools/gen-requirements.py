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

import ast


def read_dependencies():
    with open("pyproject.toml", "r", encoding="utf-8") as f:
        lines = f.readlines()

    collecting = False
    dependency_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("dependencies = ["):
            collecting = True
            dependency_lines.append(stripped[len("dependencies = ") :])
            continue
        if collecting:
            dependency_lines.append(line)
            if stripped == "]":
                break

    return ast.literal_eval("".join(dependency_lines))


with open("requirements.txt", "w", encoding="utf-8") as f:
    for dependency in read_dependencies():
        print(dependency)
        f.write(dependency + "\n")

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
with open(r"./minecraftCommand.txt", "r", encoding="utf-8") as MCCmd:
    MCCmdList = MCCmd.readlines()
for i in range(len(MCCmdList)):
    MCCmdList[i] = MCCmdList[i].replace("\n", "")
print("MinecraftBuiltInCommand =", MCCmdList)

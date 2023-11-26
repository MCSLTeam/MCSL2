with open(r"./minecraftCommand.txt", "r", encoding="utf-8") as MCCmd:
    MCCmdList = MCCmd.readlines()
for i in range(len(MCCmdList)):
    MCCmdList[i] = MCCmdList[i].replace("\n", "")
print("MinecraftBuiltInCommand =", MCCmdList)

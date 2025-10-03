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
"""
Server config validator
"""

from MCSL2Lib.variables import BaseServerVariables
from PyQt5.QtCore import QObject


class ServerValidator(QObject):
    def __init__(self):
        super().__init__()

    def check(self, v, minMem, maxMem, name, jvmArg):
        a = self.checkJavaSet(v)
        b = self.checkMemSet(minMem, maxMem, v)
        c = self.checkCoreSet(v)
        d = self.checkServerNameSet(name, v)
        e = self.checkJVMArgSet(jvmArg, v)
        return "\n".join([
            a[0] if a[1] else "1",
            b[0] if b[1] else "1",
            c[0] if c[1] else "1",
            d[0] if d[1] else "1",
            e[0] if e[1] else "1",
        ]).replace("1\n", "").replace("1", ""), int(a[1] + b[1] + c[1] + d[1] + e[1])

    def checkJavaSet(self, v: BaseServerVariables):
        """检查Java设置"""
        # 基岩版服务器不需要Java
        if hasattr(v, 'serverType') and v.serverType == "bedrock":
            return self.tr("Java 检查: 跳过（基岩版服务器）"), 0
        if v.selectedJavaPath != "":
            return self.tr("Java 检查: 正常"), 0
        else:
            return self.tr("Java 检查: 出错，缺失"), 1

    def checkMemSet(self, minMem, maxMem, v: BaseServerVariables):
        """检查内存设置"""
        # 基岩版服务器不需要内存设置（不使用JVM）
        if hasattr(v, 'serverType') and v.serverType == "bedrock":
            v.minMem = 0
            v.maxMem = 0
            return self.tr("内存检查: 跳过（基岩版服务器）"), 0

        # 是否为空
        if minMem != "" and maxMem != "":
            # 是否是数字
            if minMem.isdigit() and maxMem.isdigit():
                # 是否为整数
                if not int(minMem) % 1 and not int(maxMem) % 1:
                    # 是否为整数
                    if int(minMem) <= int(minMem):
                        v.minMem = int(minMem)
                        v.maxMem = int(maxMem)
                        return self.tr("内存检查: 正常"), 0

                    else:
                        return (
                            self.tr("内存检查: 出错, 最小内存必须小于等于最大内存"),
                            1,
                        )
                else:
                    return self.tr("内存检查: 出错, 不为整数"), 1
            else:
                return self.tr("内存检查: 出错, 不为数字"), 1
        else:
            return self.tr("内存检查: 出错, 内容为空"), 1

    def checkCoreSet(self, v: BaseServerVariables):
        """检查核心设置"""
        if v.coreFileName != "":
            return self.tr("核心检查: 正常"), 0
        else:
            return self.tr("核心检查: 出错，缺失"), 1

    def checkServerNameSet(self, n, v: BaseServerVariables):
        """检查服务器名称设置"""
        errText = self.tr("服务器名称检查: 出错")
        isError: int
        illegalServerCharacterList = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
        illegalServerNameList = [
            "aux",
            "prn",
            "con",
            "lpt1",
            "lpt2",
            "nul",
            "com0",
            "com1",
            "com2",
            "com3",
            "com4",
            "com5",
            "com6",
            "com7",
            "com8",
            "com9",
        ]
        for i in range(len(illegalServerNameList)):
            if illegalServerNameList[i] == n:
                errText += self.tr("，名称与操作系统冲突")
                isError = 1
                break
            else:
                isError = 0
        for eachIllegalServerCharacter in illegalServerCharacterList:
            if eachIllegalServerCharacter not in n:
                pass
            else:
                errText += self.tr("，名称含有不合法字符")
                isError = 1
                break
        if n == "":
            errText += self.tr("，未填写")
            isError = 1
        if isError == 1:
            return errText, isError
        else:
            v.serverName = n
            return self.tr("服务器名称检查: 正常"), isError

    def checkJVMArgSet(self, j, v: BaseServerVariables):
        """检查JVM参数设置，同时设置"""
        # 基岩版服务器不需要JVM参数
        if hasattr(v, 'serverType') and v.serverType == "bedrock":
            v.jvmArg = []
            return self.tr("JVM 参数检查: 跳过（基岩版服务器）"), 0
        try:
            v.jvmArg = j.split(" ")
            return self.tr("JVM 参数检查: 正常"), 0
        except Exception:
            return self.tr("JVM 参数检查: 出错"), 1

#
#         From: Minecraft-Server-Launcher, by Waheal, modified by LxHTT.
#         URL: https://github.com/Waheal/Minecraft-Server-Launcher
#
################################################################################
"""
Minecraft Forge Servers Installer.
"""

import re


class ServerErrorHandler:
    lineCount: int = 0
    msg: str = ""

    @classmethod
    def detect(cls, errMsg):
        if cls.lineCount <= 50:
            cls.lineCount += 1

            if "UnsupportedClassVersionError" in errMsg:
                cls.msg += "Java版本不正确，请更换Java。\n"
                a = int(
                    errMsg[
                        errMsg.index("(class file version ") + 20 : errMsg.index(
                            "(class file version "
                        )
                        + 22
                    ]
                )

                versionMapping = {
                    52: "Java 8",
                    53: "Java 9",
                    54: "Java 10",
                    55: "Java 11",
                    56: "Java 12",
                    57: "Java 13",
                    58: "Java 14",
                    59: "Java 15",
                    60: "Java 16",
                    61: "Java 17",
                    62: "Java 18",
                    63: "Java 19",
                    64: "Java 20",
                }

                if a in versionMapping:
                    cls.msg += f"根据错误报告，推荐使用{versionMapping[a]}。\n"

            elif "Unsupported Java detected" in errMsg:
                cls.msg += "该服务器正在使用的Java与服务器不兼容。\n"
                cls.msg += f"请使用{errMsg[errMsg.index('Only up to ') + 11: errMsg.index('Only up to ') + 18]}\n"

            elif "requires running the server with" in errMsg:
                cls.msg += "该服务器正在使用的Java与服务器不匹配。\n"
                cls.msg += (
                    f"请使用{errMsg[errMsg.index('Java') + 4: errMsg.index('Java') + 11]}！\n"
                )

            elif "OutOfMemoryError" in errMsg:
                cls.msg += "服务器内存溢出。请检查服务器内存设置，不要超出可用内存，也不要太小。\n"

            elif "Invalid maximum heap size" in errMsg:
                cls.msg += "服务器最大内存分配有误：\n" + errMsg + "\n"

            elif "Unrecognized VM option" in errMsg:
                cls.msg += (
                    "服务器JVM参数有误，请前往服务器管理页修改或删除以下参数：\n"
                    + errMsg[errMsg.index("'") + 1 : errMsg.rindex(" '")]
                    + "\n"
                )

            elif (
                "There is insufficient memory for the Java Runtime Environment to continue"
                in errMsg
            ):
                cls.msg += "JVM内存分配不足，请尝试增加系统的虚拟内存。\n"

            elif "进程无法访问" in errMsg:
                if (
                    not cls.msg
                    or "文件被占用，您的服务器可能多开，请检查任务管理器等。\n" not in cls.msg
                ):
                    cls.msg += "文件被占用，您的服务器可能多开，请检查任务管理器等。\n"

            elif "FAILED TO BIND TO PORT" in errMsg:
                cls.msg += "端口被占用，您的服务器可能多开，请检查任务管理器等。\n"

            elif "Unable to access jarfile" in errMsg:
                cls.msg += "无法访问Jar可执行文件，请检查文件是否存在，或更换服务器核心或名称。\n"

            elif "加载 Java 代理时出错" in errMsg:
                cls.msg += "无法访问Jar可执行文件，请检查文件是否存在，或更换服务器核心或名称。\n"

            elif "ArraylndexOutOfBoundsException" in errMsg:
                cls.msg += "服务器发生数组越界错误，请尝试更换服务端。\n"

            elif "ClassCastException" in errMsg:
                cls.msg += "服务器发生类转换异常，请检查Java版本是否匹配。\n"

            elif "could not open" in errMsg and "jvm.cfg" in errMsg:
                cls.msg += (
                    "Java环境异常，请检查Java的安装是否完整，若无法确定原因，请尝试重装Java。\n"
                )

            elif "Failed to download vanilla jar" in errMsg:
                cls.msg += "服务器下载原版核心文件失败，请检查网络，必要的情况下请使用代理。\n"

            elif 'Exception in thread "main"' in errMsg:
                cls.msg += '服务端给出了如下报错：\nException in thread "main"\n请尝试更换Java版本或服务端。'

        if "Could not load" in errMsg and "plugin" in errMsg:
            cls.msg += "无法加载下列插件：\n"
            startIdx = errMsg.index("Could not load '") + 16
            endIdx = errMsg.index("' ", startIdx)
            cls.msg += "{}\n".format(errMsg[startIdx:endIdx])
        elif "Error loading plugin" in errMsg:
            cls.msg += "无法加载下列插件：\n"
            startIdx = errMsg.index(" '") + 2
            endIdx = errMsg.index("' ", startIdx)
            cls.msg += "{}\n".format(errMsg[startIdx:endIdx])

        elif "Error occurred while enabling " in errMsg:
            cls.msg += (
                f"在启用 {errMsg[errMsg.index('enabling ') + 9: errMsg.index(' (')]} 时发生了错误\n"
            )

        elif "Encountered an unexpected exception" in errMsg:
            cls.msg += "服务器出现意外崩溃，可能是由于模组冲突，请检查您的模组列表。\n如果使用的是整合包，请使用整合包制作方提供的服务器专用包开服。\n"

        elif "Mod" in errMsg and "requires" in errMsg:
            if "&" in errMsg:
                errMsg = "".join(everyMsg[1:] for everyMsg in errMsg.split("&") if everyMsg)

            elif "§" in errMsg:
                errMsg = "".join(every_msg[1:] for every_msg in errMsg.split("§") if every_msg)

            elif "\x1B" in errMsg:
                errMsg = "".join(
                    every_msg[every_msg.index("m") + 1:]
                    for every_msg in errMsg.split("\x1B")
                    if every_msg
                )

            modNamePattern = r"Mod (\w+) requires"
            preModPattern = r"requires (\w+ \d+\.\d+\.\d+)"

            modNameMatch = re.search(modNamePattern, errMsg)
            preModMatch = re.search(preModPattern, errMsg)

            if modNameMatch and preModMatch:
                modName = modNameMatch.group(1)
                preMod = preModMatch.group(1)

                if "or above" in errMsg:
                    cls.msg += f"*{modName} 模组出现问题！该模组需要前置 {preMod} 或以上版本！\n"
                else:
                    cls.msg += f"*{modName} 模组出现问题！该模组需要前置 {preMod}！\n"
        return cls.msg

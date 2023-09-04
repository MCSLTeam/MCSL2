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
Main entry.
"""
import time
from types import FrameType

begin = time.time()
print(f"{time.time() - begin}MCSL2: Importing...")
import os
import sys
from platform import system

from lib_not_dr.types.version import Version

print(f"{time.time() - begin}MCSL2: PyQt importing.")
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

print(f"{time.time() - begin}MCSL2: PyQt imported")
from MCSL2Lib.publicFunctions import initializeMCSL2

print(f"{time.time() - begin}MCSL2: initializeMCSL2 imported")

MAIN_VERSION = Version("2.2.1.0")
BUILD_VERSION = Version("0.0.1.0")


def profile_func(frame: FrameType, event, arg):
    # 打印函数名
    if "event" not in (a := frame.f_code.co_name).lower() and "angle" not in a.lower() and "C:\\" not in (b:= frame.f_code.co_filename) and "site-packages" not in b and "frozen" not in b:
        print(f"{a} || {b} || {frame.f_lineno}")


if __name__ == "__main__":
    # 初始化
    print(f"{time.time() - begin}MCSL2: Initializing...")
    initializeMCSL2()
    print(f"{time.time() - begin}MCSL2: Initialized.")

    # 高DPI适配
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # 适配Linux特殊情况
    if system().lower() == "linux":
        try:
            if os.environ["XDG_SESSION_TYPE"].lower() != "x11":
                os.environ["QT_QPA_PLATFORM"] = "wayland"
            else:
                pass
        except:
            pass
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "auto"

    # 启动
    app = QApplication(sys.argv)
    print(f"{time.time() - begin}MCSL2: QApplication initialized.")
    translator = FluentTranslator(QLocale())
    app.installTranslator(translator)
    print(f"{time.time() - begin}MCSL2: Fluent translation system initialized.")
    from MCSL2Lib.windowInterface import Window

    w = Window()
    w.show()
    print(f"{time.time() - begin}MCSL2: Window initialized.")
    app.exec_()

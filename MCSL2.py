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

import sys
from PyQt5.QtCore import Qt, QLocale, QObject, QEvent
from PyQt5.QtWidgets import QApplication

# from viztracer import VizTracer
from MCSL2Lib.utils import MCSL2Logger


class MCSL2Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

    def notify(self, a0: QObject, a1: QEvent) -> bool:
        try:
            done = super().notify(a0, a1)
            return done
        except Exception as e:
            MCSL2Logger.critical(e)
            return False


if __name__ == "__main__":
    # Debug
    # tracer = VizTracer()
    # tracer.enable_thread_tracing()
    # tracer.start()

    # Initialize
    from MCSL2Lib.utils import initializeMCSL2

    initializeMCSL2()
    del initializeMCSL2

    # Load config
    from qfluentwidgets import qconfig
    from MCSL2Lib.Controllers.settingsController import cfg

    qconfig.load(r"./MCSL2/MCSL2_Config.json", cfg)

    # Verify dev mode
    cfg.set(cfg.oldExecuteable, sys.executable.split("\\")[-1])
    from MCSL2Lib.variables import GlobalMCSL2Variables

    if (
        cfg.get(cfg.oldExecuteable) == "python"
        or cfg.get(cfg.oldExecuteable) == "python.exe"
        or cfg.get(cfg.oldExecuteable) == "py"
        or cfg.get(cfg.oldExecuteable) == "py.exe"
    ):
        GlobalMCSL2Variables.devMode = True
    else:
        GlobalMCSL2Variables.devMode = False

    # Try to delete old executable
    from os import path as osp

    if osp.exists(cfg.get(cfg.oldExecuteable)):
        from MCSL2Lib.Controllers.updateController import deleteOldMCSL2

        deleteOldMCSL2()
        del deleteOldMCSL2

    # Analyze user
    try:
        from MCSL2Lib.verification import countUserAPI
    except Exception:
        from MCSL2Lib.noVerification import countUserAPI

    try:
        countUserAPI()
    except Exception:
        pass
    del countUserAPI

    # High DPI scaling
    MCSL2Application.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    MCSL2Application.setAttribute(Qt.AA_EnableHighDpiScaling)
    MCSL2Application.setAttribute(Qt.AA_UseHighDpiPixmaps)
    MCSL2Application.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    MCSL2Application.setAttribute(Qt.AA_UseDesktopOpenGL)
    MCSL2Application.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents)
    MCSL2Application.setAttribute(Qt.AA_SynthesizeMouseForUnhandledTouchEvents)

    # Construct QApplication
    app = MCSL2Application(sys.argv)
    # i18n
    from qfluentwidgets import FluentTranslator

    fluentTranslator = FluentTranslator(QLocale(QLocale.Chinese))
    app.installTranslator(fluentTranslator)

    # Main Window
    from MCSL2Lib.windowInterface import Window

    w = Window()
    w.show()

    import gc

    gc.enable()

    app.exec_()

    # tracer.stop()
    # tracer.save()

    sys.exit()

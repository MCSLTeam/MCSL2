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

from PyQt5.QtCore import Qt, QLocale, QObject, QEvent, QTranslator
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator, qconfig
from MCSL2Lib.Controllers.updateController import deleteOldMCSL2
from MCSL2Lib.Controllers.settingsController import cfg
import gc
# from viztracer import VizTracer
from MCSL2Lib.utils import initializeMCSL2
from MCSL2Lib.utils import MCSL2Logger
from MCSL2Lib.variables import GlobalMCSL2Variables


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


class MCSL2Translator(QTranslator):
    def __init__(self, locale: QLocale = None, parent=None):
        super().__init__(parent=parent)
        self.load(locale or QLocale())

    def load(self, locale: QLocale):
        super().load(f"i18n/{locale.name()}.qm")


if __name__ == "__main__":
    # tracer = VizTracer()
    # tracer.enable_thread_tracing()
    # tracer.start()
    # 初始化
    initializeMCSL2()
    qconfig.load(r"./MCSL2/MCSL2_Config.json", cfg)
    cfg.set(cfg.oldExecuteable, sys.executable.split("\\")[-1])
    # 确认开发模式防止出事
    if (
        cfg.get(cfg.oldExecuteable) == "python"
        or cfg.get(cfg.oldExecuteable) == "python.exe"
        or cfg.get(cfg.oldExecuteable) == "py"
        or cfg.get(cfg.oldExecuteable) == "py.exe"
    ):
        GlobalMCSL2Variables.devMode = True
    else:
        GlobalMCSL2Variables.devMode = False

    deleteOldMCSL2()
    # 高DPI适配
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # 启动
    app = MCSL2Application(sys.argv)
    # fluentTranslator = FluentTranslator(QLocale(QLocale.English))
    # mcslTranslator = MCSL2Translator(QLocale(QLocale.English))
    fluentTranslator = FluentTranslator(QLocale(QLocale.Chinese))
    # mcslTranslator = MCSL2Translator(QLocale(QLocale.Chinese))
    app.installTranslator(fluentTranslator)
    # app.installTranslator(mcslTranslator)
    from MCSL2Lib.windowInterface import Window

    w = Window()
    w.show()
    gc.enable()
    app.exec_()
    # tracer.stop()
    # tracer.save()
    sys.exit()

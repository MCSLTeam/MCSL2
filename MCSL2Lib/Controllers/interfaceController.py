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
A stacked widget controller.
"""
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtWidgets import QAbstractScrollArea
from qfluentwidgets.window.stacked_widget import StackedWidget as QFStackedWidget


class ChildStackedWidget(QFStackedWidget):
    def setCurrentWidget(self, widget, popOut=False):
        if isinstance(widget, QAbstractScrollArea):
            widget.verticalScrollBar().setValue(0)

        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(widget, True, False, 200, QEasingCurve.OutQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)

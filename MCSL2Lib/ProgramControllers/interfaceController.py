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
A stacked widget controller.
"""

from typing import List  # noqa: F401
from PyQt5.QtCore import (
    QEasingCurve,
    Qt,
    QPropertyAnimation,
    pyqtSignal,
    QAbstractAnimation,
    QPoint,
)
from PyQt5.QtWidgets import (
    QAbstractScrollArea,
    QScrollArea,
    QStackedWidget,
    QWidget,
    QFrame,
    QHBoxLayout,
)
from qfluentwidgets import SmoothScrollArea, SmoothScrollDelegate
from MCSL2Lib.variables import GlobalMCSL2Variables


class EraseAniInfo:
    """Erase ani info"""

    def __init__(self, widget: QWidget, deltaX: int, deltaY, ani: QPropertyAnimation):
        self.widget = widget
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.ani = ani


class EraseStackedWidget(QStackedWidget):
    """Stacked widget with erase animation"""

    aniFinished = pyqtSignal()
    aniStart = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.aniInfos = []  # type: List[EraseAniInfo]
        self._nextIndex = None
        self._ani = None

    def addWidget(self, widget, deltaX=180, deltaY=0):
        """add widget to window

        Parameters
        -----------
        widget:
            widget to be added

        deltaX: int
            the x-axis offset from the beginning to the end of animation

        deltaY: int
            the y-axis offset from the beginning to the end of animation
        """
        super().addWidget(widget)

        self.aniInfos.append(
            EraseAniInfo(
                widget=widget,
                deltaX=deltaX,
                deltaY=deltaY,
                ani=QPropertyAnimation(widget, b"pos"),
            )
        )

    def setCurrentIndex(
        self,
        index: int,
        needPopOut: bool = False,
        showNextWidgetDirectly: bool = True,
        duration: int = 220,
        easingCurve=QEasingCurve.BezierSpline,
    ):
        """set current window to display

        Parameters
        ----------
        index: int
            the index of widget to display

        isNeedPopOut: bool
            need pop up animation or not

        showNextWidgetDirectly: bool
            whether to show next widget directly when animation started

        duration: int
            animation duration

        easingCurve: QEasingCurve
            the interpolation mode of animation
        """
        if index < 0 or index >= self.count():
            raise Exception(f"The index `{index}` is illegal")

        if index == self.currentIndex():
            return

        if self._ani and self._ani.state() == QAbstractAnimation.Running:
            self._ani.stop()
            self.__onAniFinished()

        # get the index of widget to be displayed
        self._nextIndex = index

        # get animation
        nextAniInfo = self.aniInfos[index]
        currentAniInfo = self.aniInfos[self.currentIndex()]

        currentWidget = self.currentWidget()
        nextWidget = nextAniInfo.widget
        ani = currentAniInfo.ani if needPopOut else nextAniInfo.ani
        self._ani = ani

        if needPopOut:
            deltaX, deltaY = currentAniInfo.deltaX, currentAniInfo.deltaY
            pos = currentWidget.pos() + QPoint(deltaX, deltaY)
            self.__setAnimation(ani, currentWidget.pos(), pos, duration, easingCurve)
            nextWidget.setVisible(showNextWidgetDirectly)
        else:
            deltaX, deltaY = nextAniInfo.deltaX, nextAniInfo.deltaY
            pos = nextWidget.pos() + QPoint(deltaX, deltaY)
            self.__setAnimation(ani, pos, QPoint(nextWidget.x(), 0), duration, easingCurve)
            super().setCurrentIndex(index)

        # start animation
        ani.finished.connect(self.__onAniFinished)
        ani.start()
        self.aniStart.emit()

    def setCurrentWidget(
        self,
        widget,
        needPopOut: bool = False,
        showNextWidgetDirectly: bool = True,
        duration: int = 220,
        easingCurve=QEasingCurve.BezierSpline,
    ):
        """set currect widget

        Parameters
        ----------
        widget:
            the widget to be displayed

        isNeedPopOut: bool
            need pop up animation or not

        showNextWidgetDirectly: bool
            whether to show next widget directly when animation started

        duration: int
            animation duration

        easingCurve: QEasingCurve
            the interpolation mode of animation
        """
        self.setCurrentIndex(
            self.indexOf(widget),
            needPopOut,
            showNextWidgetDirectly,
            duration,
            easingCurve,
        )

    def __setAnimation(
        self, ani, startValue, endValue, duration, easingCurve=QEasingCurve.BezierSpline
    ):
        """set the config of animation"""
        ani.setEasingCurve(easingCurve)
        ani.setStartValue(startValue)
        ani.setEndValue(endValue)
        ani.setDuration(duration)

    def __onAniFinished(self):
        """animation finished slot"""
        self._ani.disconnect()
        super().setCurrentIndex(self._nextIndex)
        self.aniFinished.emit()


class ChildStackedWidget(QFrame):
    """Stacked widget"""

    currentChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = EraseStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)
        self.setAttribute(Qt.WA_StyledBackground)

    def addWidget(self, widget):
        """add widget to view"""
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, popOut=False):
        if isinstance(widget, QAbstractScrollArea):
            widget.verticalScrollBar().setValue(0)

        if not popOut:
            self.view.setCurrentWidget(widget, duration=220)
        else:
            self.view.setCurrentWidget(widget, False, True, 220, QEasingCurve.BezierSpline)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)

    def currentIndex(self):
        return self.view.currentIndex()

    def currentWidget(self):
        return self.view.currentWidget()

    def indexOf(self, widget):
        return self.view.indexOf(widget)

    def count(self):
        return self.view.count()


class MySmoothScrollArea(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewport().setStyleSheet(GlobalMCSL2Variables.scrollAreaViewportQss)
        self.delegate = SmoothScrollDelegate(self, True)
        self.setFrameShape(QScrollArea.NoFrame)
        self.setAttribute(Qt.WA_StyledBackground)

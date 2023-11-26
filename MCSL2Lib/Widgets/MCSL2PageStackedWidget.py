import functools
from typing import List

from PyQt5.QtCore import (
    pyqtSignal,
    QPropertyAnimation,
    QEasingCurve,
    QAbstractAnimation,
    QPoint,
    QParallelAnimationGroup,
)
from PyQt5.QtWidgets import QStackedWidget, QWidget, QGraphicsOpacityEffect


class PopUpAniInfo:
    """Pop up ani info"""

    def __init__(
        self,
        widget: QWidget,
        deltaX: int,
        deltaY,
        aniGroup: QParallelAnimationGroup,
        anis: List[QPropertyAnimation],
        effect: QGraphicsOpacityEffect,
    ):
        self.widget = widget
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.aniGroup = aniGroup
        self.anis = anis
        self.effect = effect
        self.aniIn = True
        self.adjusted = False


class MCSL2PageStackedWidget(QStackedWidget):
    """Stacked widget with pop up animation"""

    halfAniFinished = pyqtSignal()
    aniFinished = pyqtSignal()
    aniStart = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.aniInfos = []  # type: List[PopUpAniInfo]
        self._nextIndex = None
        self._lastIndex = None
        self._ani = None

    def addWidget(self, widget, deltaX=0, deltaY=76):
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
        popAni = QPropertyAnimation(widget, b"pos", self)

        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)

        fadeAni = QPropertyAnimation(effect, b"opacity", self)

        aniGroup = QParallelAnimationGroup(widget)
        aniGroup.addAnimation(popAni)
        aniGroup.addAnimation(fadeAni)
        self.aniInfos.append(
            PopUpAniInfo(
                widget=widget,
                deltaX=deltaX,
                deltaY=deltaY,
                aniGroup=aniGroup,
                anis=[popAni, fadeAni],
                effect=effect,
            )
        )

    def setCurrentIndex(
        self,
        index: int,
        needPopOut: bool = False,
        showNextWidgetDirectly: bool = True,
        duration2: int = 200,
        easingCurve=QEasingCurve.OutExpo,
        duration1: int = 100,
    ):
        """set current window to display

        Parameters
        ----------
        index: int
            the index of widget to display

        showNextWidgetDirectly: bool
            whether to show next widget directly when animation started

        duration1: int
            pre animation duration

        duration2: int
            main animation duration

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

        self.__adjustCurrentWidget(self._lastIndex)

        # get the index of widget to be displayed
        self._nextIndex = index

        # get animation
        nextAniInfo = self.aniInfos[index]
        currentAniInfo = self.aniInfos[self.currentIndex()]

        currentWidget = self.currentWidget()

        aniGroup = currentAniInfo.aniGroup if needPopOut else nextAniInfo.aniGroup
        popAni, fadeAni = currentAniInfo.anis if needPopOut else nextAniInfo.anis

        if needPopOut:
            self._ani = aniGroup
            deltaX, deltaY = currentAniInfo.deltaX, currentAniInfo.deltaY
            pos = currentWidget.pos() + QPoint(deltaX, deltaY)

            nextAniInfo.aniIn = False
            nextAniInfo.adjusted = False
            # set current index pop out animation
            self.__setAnimation(popAni, currentWidget.pos(), pos, duration2, easingCurve)
            self.__setAnimation(fadeAni, 1, 0, duration2, easingCurve)
            aniGroup.finished.connect(
                functools.partial(
                    self.__onHalfAniFinished,
                    needPopOut,
                    currentAniInfo,
                    nextAniInfo,
                    duration1,
                    duration2,
                    easingCurve,
                    index,
                )
            )
            aniGroup.start()
        else:
            currentAniInfo.aniIn = False
            currentAniInfo.adjusted = False
            # set current index fade out animation
            preFadeAni = currentAniInfo.anis[1]
            self._ani = preFadeAni
            self.__setAnimation(preFadeAni, 1, 0, duration1, easingCurve)
            preFadeAni.finished.connect(
                functools.partial(
                    self.__onHalfAniFinished,
                    needPopOut,
                    currentAniInfo,
                    nextAniInfo,
                    duration1,
                    duration2,
                    easingCurve,
                    index,
                )
            )
            preFadeAni.start()

    def __onHalfAniFinished(
        self, needPopOut, currentAniInfo, nextAniInfo, duration1, duration2, easingCurve, index
    ):
        nextWidget = nextAniInfo.widget
        aniGroup = currentAniInfo.aniGroup if needPopOut else nextAniInfo.aniGroup
        popAni, fadeAni = currentAniInfo.anis if needPopOut else nextAniInfo.anis
        self._lastIndex = self.currentIndex()
        self._ani.disconnect()
        # self.__adjustCurrentWidget(self.currentIndex())
        if needPopOut:
            currentAniInfo.aniIn = True
            # set next index fade in animation
            postFadeAni = nextAniInfo.anis[1]
            self._ani = postFadeAni
            effect = nextAniInfo.effect
            effect.setOpacity(0)

            self.__setAnimation(postFadeAni, 0, 1, duration1, easingCurve)

            # start animation
            postFadeAni.finished.connect(self.__onAniFinished)
            nextWidget.setVisible(True)
            postFadeAni.start()
            self.aniStart.emit()
        else:
            currentAniInfo.aniIn = True
            # set next index pop in animation
            self._ani = aniGroup
            deltaX, deltaY = nextAniInfo.deltaX, nextAniInfo.deltaY
            pos = nextWidget.pos() + QPoint(deltaX, deltaY)
            self.__setAnimation(popAni, pos, nextWidget.pos(), duration2, easingCurve)
            self.__setAnimation(fadeAni, 0, 1, duration2, easingCurve)
            super().setCurrentIndex(index)

            # start animation
            aniGroup.finished.connect(self.__onAniFinished)
            aniGroup.start()
            self.aniStart.emit()

    def setCurrentWidget(
        self,
        widget,
        needPopOut: bool = False,
        showNextWidgetDirectly: bool = True,
        duration: int = 150,
        easingCurve=QEasingCurve.OutQuad,
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
            self.indexOf(widget), needPopOut, showNextWidgetDirectly, duration, easingCurve
        )

    def __setAnimation(self, ani, startValue, endValue, duration, easingCurve=QEasingCurve.Linear):
        """set the config of animation"""
        ani.setEasingCurve(easingCurve)
        ani.setStartValue(startValue)
        ani.setEndValue(endValue)
        ani.setDuration(duration)

    def __onAniFinished(self):
        """animation finished slot"""
        self._ani.disconnect()
        currentIndex = self.currentIndex()
        super().setCurrentIndex(self._nextIndex)
        # self.__adjustCurrentWidget(currentIndex)
        self._lastIndex = self.currentIndex()
        self.aniFinished.emit()

    def __adjustCurrentWidget(self, index):
        if index is None:
            return
        if self.aniInfos[index].aniIn and not self.aniInfos[index].adjusted:
            self.aniInfos[index].adjusted = True
            self.aniInfos[index].widget.move(0, 0)

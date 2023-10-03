from MCSL2Lib.variables import GlobalMCSL2Variables
from qfluentwidgets import SmoothScrollArea, SmoothScrollDelegate

class MySmoothScrollArea(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewport().setStyleSheet(GlobalMCSL2Variables.scrollAreaViewportQss)
        self.delegate = SmoothScrollDelegate(self, True)

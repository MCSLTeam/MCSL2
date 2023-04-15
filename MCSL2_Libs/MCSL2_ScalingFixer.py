# # from screeninfo import get_monitors
# #
# # class ScalingFixer:
# #     def __init__(self):
# #         # self.1080pb = 1
# #         self.Monitor = get_monitors()[0]
# #         self.Width, self.Height = self.Monitor.width, self.Monitor.height
# #         print(f"W:{self.Width}, H:{self.Height}")
# #
# #     def CalculateDPI(self):
# #         Diagonal = self.Monitor.width_mm / 25.4
# #         # 计算DPI和缩放比例
# #         self.DPI = round((self.Width ** 2 + self.Height ** 2) ** 0.5 / Diagonal, 2)
# #         self.Scaling = round(self.DPI / 96, 2)
# #         print(f"DPI:{self.DPI}\nScaling:{self.Scaling}")
# #
# # ScalingFixer().CalculateDPI()
#

from win32.lib import win32con
from win32.win32api import GetSystemMetrics
from win32.win32gui import GetDC
from win32.win32print import GetDeviceCaps


class ScalingFixer:
    def __init__(self):
        pass

    def Scan(self):
        RealResolution = self.GetRealResolution()
        ScreenSize = self.GetScreenSize()
        Scaling = round(RealResolution[0] / ScreenSize[0], 2)
        return str(Scaling)

    def GetRealResolution(self):
        """获取真实的分辨率"""
        hDC = GetDC(0)
        # 横向分辨率
        w = GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        # 纵向分辨率
        h = GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
        return w, h

    def GetScreenSize(self):
        """获取缩放后的分辨率"""
        w = GetSystemMetrics(0)
        h = GetSystemMetrics(1)
        return w, h

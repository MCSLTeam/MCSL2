from datetime import datetime
from json import dump
from os import getcwd, environ, remove, system as os_system, path as ospath
from pathlib import WindowsPath
from platform import system
from subprocess import CalledProcessError
from sys import argv, exit
from qfluentwidgets import ProgressBar, IndeterminateProgressBar
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsDropShadowEffect,
    QMainWindow, QListView,
    QGridLayout
)

from MCSL2_Libs import MCSL2_Icon as _  # noqa: F401
from MCSL2_Libs import MCSL2_JavaDetector
from MCSL2_Libs.MCSL2_Aria2Controller import Aria2Controller, DownloadWatcher
from MCSL2_Libs.MCSL2_Dialog import CallMCSL2Dialog
from MCSL2_Libs.MCSL2_DownloadURLParser import FetchDownloadURLThreadFactory
from MCSL2_Libs.MCSL2_Init import InitMCSL
from MCSL2_Libs.MCSL2_JavaDetector import GetJavaVersion, Java
from MCSL2_Libs.MCSL2_Logger import MCSL2Logger
from MCSL2_Libs.MCSL2_MainWindow import *  # noqa: F403
from MCSL2_Libs.MCSL2_ServerController import (
    CheckAvailableSaveServer,
    SaveServer,
    ReadGlobalServerConfig,
    ServerLauncher
)
from MCSL2_Libs.MCSL2_Settings import MCSL2Settings, OpenWebUrl
from MCSL2_Libs.MCSL2_Updater import Updater

MCSLLogger = MCSL2Logger()


# Initialize MainWindow
class MCSL2MainWindow(QMainWindow, Ui_MCSL2_MainWindow):

    def __init__(self):
        try:
            self.__mousePressPos = None
            self.__mouseMovePos = None
            self.DownloadURLList: list
            global DownloadSource
            MCSLLogger.Log(Msg="InitMCSL", MsgArg=None, MsgLevel=0)
            super(MCSL2MainWindow, self).__init__()
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            effect = QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(12)
            effect.setOffset(0, 0)
            effect.setColor(QColor("#F0F8FF"))
            self.setGraphicsEffect(effect)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setAutoFillBackground(True)
            self.setupUi(self)
            MCSLLogger.Log(Msg="InitUI", MsgArg=None, MsgLevel=0
                           )
            TitleBarSetting = MCSL2Settings().GetConfig(
                "UseTitleBarInsteadOfmacOSControlling")
            if TitleBarSetting:
                self.OptionsWidgetIndicator.setGeometry(QRect(20, 120, 3, 21))
            elif not TitleBarSetting:
                self.OptionsWidgetIndicator.setGeometry(QRect(20, 150, 3, 21))
            self.ExMemoryUnitComboBox.setCurrentIndex(0)
            self.TransparentPercentNum.setText(
                str(self.TransparentPercentSlider.value()) + "%")
            self.Home_Page_PushButton.setIcon(QIcon(":/MCSL2_Icon/Home.svg"))
            self.Home_Page_PushButton.setIconSize(QSize(24, 24))
            self.Config_Page_PushButton.setIcon(
                QIcon(":/MCSL2_Icon/Configuration.svg"))
            self.Config_Page_PushButton.setIconSize(QSize(24, 24))
            self.Download_Page_PushButton.setIcon(
                QIcon(":/MCSL2_Icon/Download.svg"))
            self.Download_Page_PushButton.setIconSize(QSize(24, 24))
            self.Server_Console_Page_PushButton.setIcon(
                QIcon(":/MCSL2_Icon/Console.svg"))
            self.Server_Console_Page_PushButton.setIconSize(QSize(24, 24))
            self.Tools_Page_PushButton.setIcon(QIcon(":/MCSL2_Icon/Toolbox.svg"))
            self.Tools_Page_PushButton.setIconSize(QSize(24, 24))
            self.About_Page_PushButton.setIcon(QIcon(":/MCSL2_Icon/About.svg"))
            self.About_Page_PushButton.setIconSize(QSize(24, 24))
            MCSL2Settings()
            MCSLLogger.Log(Msg="ReadConfig", MsgArg=None, MsgLevel=0
                           )
            MCSLLogger.Log(Msg="InitFunctionsBind", MsgArg=None, MsgLevel=0
                           )
            self.GetNotice()
            self.InitTitleBar()
            # Window event binding
            self.Close_PushButton.clicked.connect(self.Quit)
            self.Minimize_PushButton.clicked.connect(self.Minimize)
            self.Close_PushButton_R.clicked.connect(self.Quit)
            self.Minimize_PushButton_R.clicked.connect(self.Minimize)

            # Visible pages navigation binding
            self.Home_Page_PushButton.clicked.connect(self.VisiblePagesNavigation)
            self.Config_Page_PushButton.clicked.connect(self.VisiblePagesNavigation)
            self.Download_Page_PushButton.clicked.connect(self.VisiblePagesNavigation)
            self.Server_Console_Page_PushButton.clicked.connect(self.VisiblePagesNavigation)
            self.Tools_Page_PushButton.clicked.connect(self.VisiblePagesNavigation)
            self.About_Page_PushButton.clicked.connect(self.VisiblePagesNavigation)

            # Functions in home page
            self.Choose_Server_PushButton.clicked.connect(self.ToChooseServerPage)
            self.Config_PushButton.clicked.connect(self.LegacyToConfigPage)
            self.Start_PushButton.clicked.connect(self.StartMCServerHelper)

            # Functions in config page - lead page
            self.NoobAddServer.clicked.connect(
                lambda: self.ConfigModeWidget.setCurrentIndex(1))
            self.ExAddServer.clicked.connect(
                lambda: self.ConfigModeWidget.setCurrentIndex(2))

            # Functions in config page - noob page
            self.Manual_Import_Java_PushButton.clicked.connect(self.ManuallySelectJava)
            self.Auto_Find_Java_PushButton.clicked.connect(self.AutoDetectJava)
            self.Download_Java_PushButton.clicked.connect(self.ToDownloadJava)
            self.Founded_Java_List_PushButton.clicked.connect(
                self.ToChooseJavaPage)
            self.Manual_Import_Core_PushButton.clicked.connect(
                self.ManuallyImportCore)
            self.Download_Core_PushButton.clicked.connect(self.LegacyToDownloadCore)
            self.Completed_Save_PushButton.clicked.connect(
                self.SaveMinecraftServer)

            # Functions in config page - extended page
            self.ExManual_Import_Java_PushButton.clicked.connect(self.ManuallySelectJava)
            self.ExAuto_Find_Java_PushButton.clicked.connect(self.AutoDetectJava)
            self.ExDownload_Java_PushButton.clicked.connect(self.ToDownloadJava)
            self.ExFounded_Java_List_PushButton.clicked.connect(
                self.ToChooseJavaPage)
            self.ExManual_Import_Core_PushButton.clicked.connect(
                self.ManuallyImportCore)
            self.ExDownload_Core_PushButton.clicked.connect(self.LegacyToDownloadCore)
            # self.ExMemoryUnitComboBox.currentIndexChanged.connect()
            # self.ExConsoleOutputEncodingComboBox.currentIndexChanged.connect()
            # self.ExConsoleInputDecodingComboBox.currentIndexChanged.connect()
            self.ExCompleted_Save_PushButton.clicked.connect(
                self.SaveMinecraftServer)

            # Functions in download page
            self.DownloadSwitcher_TabWidget.currentChanged.connect(
                self.RefreshDownloadType)
            self.GoToDownloadSourceChangerPushButton.clicked.connect(
                self.LegacyToAboutPage)
            # self.More_Download_PushButton.clicked.connect()

            # Functions in console page
            # self.Send_Command_PushButton.clicked.connect()

            # Functions in choose java page
            self.Choose_Java_Back_PushButton.clicked.connect(
                self.ShowFoundedJavaList_Back)

            # Functions in update page
            self.DoNotUpdate_PushButton.clicked.connect(self.LegacyToAboutPage)
            # self.Update_PushButton.clicked.connect()

            # Register Java finder workThread factory
            self.javaPath = []
            self.JavaFindWorkThreadFactory = MCSL2_JavaDetector.JavaFindWorkThreadFactory()
            self.JavaFindWorkThreadFactory.FuzzySearch = True
            self.JavaFindWorkThreadFactory.SignalConnect = self.JavaDetectFinished
            self.JavaFindWorkThreadFactory.FinishSignalConnect = self.OnJavaFindWorkThreadFinished
            # Create java finder workThread instance and start
            self.JavaFindWorkThreadFactory.Create().start()

            # Init factories
            self.fetchDownloadURLThreadFactory = FetchDownloadURLThreadFactory()

            # Init download url dict
            self.downloadUrlDict = {}

            # Bind functions in settings page
            self.AutoRunLastServerSetting.clicked.connect(
                lambda: self.CheckBoxSettingsChanger("AutoRunLastServer"))
            self.AcceptAllMojangEULASetting.clicked.connect(
                lambda: self.CheckBoxSettingsChanger("AcceptAllMojangEula"))
            self.StopServerSettings.clicked.connect(
                lambda: self.CheckBoxSettingsChanger("SendStopInsteadOfKill"))
            self.OnlySaveGlobalServerConfigs.clicked.connect(
                lambda: self.CheckBoxSettingsChanger("OnlySaveGlobalServerConfig"))

            self.HowToAddServerComboBox.currentIndexChanged.connect(
                lambda: self.ComboBoxSettingChanger("AddServerMode", self.HowToAddServerComboBox.currentIndex()))
            self.MCSLAPIDownloadSourceComboBox.currentIndexChanged.connect(
                lambda: self.ComboBoxSettingChanger("MCSLAPIDownloadSource",
                                                    self.MCSLAPIDownloadSourceComboBox.currentIndex()))
            self.Aria2ThreadCountComboBox.currentIndexChanged.connect(
                lambda: self.ComboBoxSettingChanger("Aria2Thread", self.Aria2ThreadCountComboBox.currentIndex()))

            self.AlwaysAskDownloadPath.clicked.connect(
                lambda: self.CheckBoxSettingsChanger("AlwaysAskSaveDirectory"))

            self.SameFileExceptionAsk.clicked.connect(
                lambda: self.SameFileExceptionChanger("ask"))
            self.SameFileExceptionReWrite.clicked.connect(
                lambda: self.SameFileExceptionChanger("rewrite"))
            self.SameFileExceptionStop.clicked.connect(
                lambda: self.SameFileExceptionChanger("stop"))

            self.EnableQuickMenu.clicked.connect(
                lambda: self.CheckBoxSettingsChanger("EnableConsoleQuickMenu"))

            self.ConsoleOutputEncodingComboBox.currentIndexChanged.connect(
                lambda: self.ComboBoxSettingChanger("ConsoleOutputEncoding",
                                                    self.ConsoleOutputEncodingComboBox.currentIndex()))
            self.ConsoleInputDecodingComboBox.currentIndexChanged.connect(
                lambda: self.ComboBoxSettingChanger("ConsoleInputDecoding",
                                                    self.ConsoleInputDecodingComboBox.currentIndex()))
            self.TransparentPercentSlider.valueChanged.connect(
                self.TransparentPercentChanger)

            self.TitleBarInsteadOfmacOS.clicked.connect(
                lambda: self.CheckBoxSettingsChanger("UseTitleBarInsteadOfmacOSControlling"))
            self.TitleBarInsteadOfmacOS.clicked.connect(self.InitTitleBar)
            self.DarkModeComboBox.currentIndexChanged.connect(
                lambda: self.ComboBoxSettingChanger("ThemeMode", self.DarkModeComboBox.currentIndex()))
            self.StartOnStartup.clicked.connect(
                lambda: self.CheckBoxSettingsChanger("StartOnStartup"))
            self.AlwaysRunAsAdministrator.clicked.connect(
                lambda: self.CheckBoxSettingsChanger("AlwaysRunAsAdministrator"))
            self.UpdatePushButton.clicked.connect(self.CheckUpdate)
            self.OpenSourceCodePushButton.clicked.connect(lambda: OpenWebUrl(
                "https://www.github.com/LxHTT/MCSL2", ))
            self.JoinQQGroup.clicked.connect(lambda: OpenWebUrl(
                "https://jq.qq.com/?_wv=1027&k=x2ISlviQ", ))
            # self.SystemReportPushButton.clicked.connect()
            MCSLLogger.Log(Msg="InitAria2", MsgArg=None, MsgLevel=0
                           )
            Aria2Controller().InitAria2Configuration()
            isAria2 = Aria2Controller().CheckAria2()
            if not isAria2:
                Aria2Controller(
                ).ShowNoAria2Msg(self)
            MCSLLogger.Log(Msg="FinishStarting", MsgArg=None, MsgLevel=0
                           )
            self.InitDownloadProgressUI()
            DownloadSource = MCSL2Settings().MCSLAPIDownloadSource
            self.CurrentDownloadSourceLabel.setText(
                str(self.CurrentDownloadSourceLabel.text()) + str(DownloadSource))
            self.MenuList = [self.Home_Page_PushButton, self.Config_Page_PushButton, self.Download_Page_PushButton,
                             self.Server_Console_Page_PushButton, self.Tools_Page_PushButton,
                             self.About_Page_PushButton]
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def CheckBoxSettingsChanger(self, Type):
        try:
            if self.sender().isChecked():
                MCSLLogger.Log(Msg=
                               "ChangeConfig", MsgArg=f"{Type}设置为True", MsgLevel=0)
                MCSL2Settings().ChangeConfig(Type=Type, Arg=True)
            else:
                MCSLLogger.Log(Msg=
                               "ChangeConfig", MsgArg=f"{Type}设置为False", MsgLevel=0)
                MCSL2Settings().ChangeConfig(Type=Type, Arg=False)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def ComboBoxSettingChanger(self, Type, Count):
        try:
            ComboBoxAttr: list
            if Type == "AddServerMode":
                ComboBoxAttr = ["Default", "Noob", "Extended"]
            elif Type == "MCSLAPIDownloadSource":
                ComboBoxAttr = ["SharePoint", "Gitee",
                                "luoxisCloud", "GHProxy", "GitHub"]
                self.DownloadSourceChanger()
            elif Type == "Aria2Thread":
                ComboBoxAttr = [1, 2, 4, 8, 16]
            elif Type == "ConsoleOutputEncoding":
                ComboBoxAttr = ["utf-8", "gbk"]
            elif Type == "ConsoleInputDecoding":
                ComboBoxAttr = ["follow", "utf-8", "gbk"]
            elif Type == "ThemeMode":
                ComboBoxAttr = ["light", "dark", "system"]
            else:
                pass
            MCSLLogger.Log(Msg="ChangeConfig",
                           MsgArg=f"{Type}设置为{ComboBoxAttr[Count]}",
                           MsgLevel=0
                           )
            MCSL2Settings().ChangeConfig(Type=Type, Arg=ComboBoxAttr[Count])
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def SameFileExceptionChanger(self, Arg):
        try:
            MCSLLogger.Log(Msg="ChangeConfig",
                           MsgArg=f"SaveSameFileException设置为{Arg}",
                           MsgLevel=0
                           )
            MCSL2Settings().ChangeConfig(Type="SaveSameFileException", Arg=Arg)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def InitSettingUI(self):
        try:
            self.AutoRunLastServerSetting.setChecked(
                MCSL2Settings().AutoRunLastServer)
            self.AcceptAllMojangEULASetting.setChecked(
                MCSL2Settings().AcceptAllMojangEula)
            self.StopServerSettings.setChecked(
                MCSL2Settings().SendStopInsteadOfKill)
            HowToAddServerComboBoxAttr = ["Default", "Noob", "Extended"]
            self.HowToAddServerComboBox.setCurrentIndex(
                HowToAddServerComboBoxAttr.index(MCSL2Settings().AddServerMode))
            self.OnlySaveGlobalServerConfigs.setChecked(
                MCSL2Settings().OnlySaveGlobalServerConfig)
            MCSLAPIDownloadSourceAttr = [
                "SharePoint", "Gitee", "luoxisCloud", "GHProxy", "GitHub"]
            self.MCSLAPIDownloadSourceComboBox.setCurrentIndex(
                MCSLAPIDownloadSourceAttr.index(MCSL2Settings().MCSLAPIDownloadSource))
            Aria2ThreadAttr = [1, 2, 4, 8, 16]
            self.Aria2ThreadCountComboBox.setCurrentIndex(
                Aria2ThreadAttr.index(MCSL2Settings().Aria2Thread))
            self.AlwaysAskDownloadPath.setChecked(
                MCSL2Settings().AlwaysAskSaveDirectory)
            if MCSL2Settings().SaveSameFileException == "ask":
                self.SameFileExceptionAsk.setChecked(True)
                self.SameFileExceptionReWrite.setChecked(False)
                self.SameFileExceptionStop.setChecked(False)
            elif MCSL2Settings().SaveSameFileException == "rewrite":
                self.SameFileExceptionAsk.setChecked(False)
                self.SameFileExceptionReWrite.setChecked(True)
                self.SameFileExceptionStop.setChecked(False)
            elif MCSL2Settings().SaveSameFileException == "stop":
                self.SameFileExceptionAsk.setChecked(False)
                self.SameFileExceptionReWrite.setChecked(False)
                self.SameFileExceptionStop.setChecked(True)
            self.EnableQuickMenu.setChecked(MCSL2Settings().EnableConsoleQuickMenu)
            ConsoleOutputEncodingAttr = ["utf-8", "gbk"]
            self.ConsoleOutputEncodingComboBox.setCurrentIndex(
                ConsoleOutputEncodingAttr.index(MCSL2Settings().ConsoleOutputEncoding))
            ConsoleInputDecodingAttr = ["follow", "utf-8", "gbk"]
            self.ConsoleInputDecodingComboBox.setCurrentIndex(
                ConsoleInputDecodingAttr.index(MCSL2Settings().ConsoleInputDecoding))
            self.TransparentPercentSlider.setValue(
                MCSL2Settings().BackgroundTransparency)
            self.TitleBarInsteadOfmacOS.setChecked(
                MCSL2Settings().UseTitleBarInsteadOfmacOSControlling)
            ThemeModeAttr = ["light", "dark", "system"]
            self.DarkModeComboBox.setCurrentIndex(
                ThemeModeAttr.index(MCSL2Settings().ThemeMode))
            self.StartOnStartup.setChecked(MCSL2Settings().StartOnStartup)
            self.AlwaysRunAsAdministrator.setChecked(
                MCSL2Settings().AlwaysRunAsAdministrator)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def InitTitleBar(self):
        try:
            TitleBarSetting = MCSL2Settings().GetConfig(
                "UseTitleBarInsteadOfmacOSControlling")
            if TitleBarSetting:
                self.TitleBarWidget.setVisible(False)
                self.TitleBarWidget_R.setVisible(True)
                self.Home_Page_PushButton.move(20, 110)
                self.Config_Page_PushButton.move(20, 170)
                self.Download_Page_PushButton.move(20, 230)
                self.Server_Console_Page_PushButton.move(20, 290)
                self.Tools_Page_PushButton.move(20, 350)
                self.About_Page_PushButton.move(20, 410)
            elif not TitleBarSetting:
                self.TitleBarWidget.setVisible(True)
                self.TitleBarWidget_R.setVisible(False)
                self.Home_Page_PushButton.move(20, 140)
                self.Config_Page_PushButton.move(20, 200)
                self.Download_Page_PushButton.move(20, 260)
                self.Server_Console_Page_PushButton.move(20, 320)
                self.Tools_Page_PushButton.move(20, 380)
                self.About_Page_PushButton.move(20, 440)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def TransparentPercentChanger(self):
        try:
            self.Background_2.setStyleSheet("QLabel\n"
                                            "{\n"
                                            f"    background-color: rgba(255, 255, 255, {self.TransparentPercentSlider.value()}%); "
                                            "\n    border-radius: 10px\n"
                                            "}")
            self.TransparentPercentNum.setText(
                str(self.TransparentPercentSlider.value()) + "%")
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def mousePressEvent(self, event: QMouseEvent):
        try:
            if event.button() == Qt.LeftButton:
                self.__mousePressPos = event.globalPos()
                self.__mouseMovePos = event.globalPos()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def mouseMoveEvent(self, event: QMouseEvent):
        try:
            if event.buttons() == Qt.LeftButton:
                # 移动窗口
                currentPos = self.mapToGlobal(self.pos())
                globalPos = event.globalPos()
                if self.__mouseMovePos is None:
                    event.ignore()
                    return
                diff = globalPos - self.__mouseMovePos
                newPos = self.mapFromGlobal(currentPos + diff)
                self.move(newPos)
                self.__mouseMovePos = globalPos
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def mouseReleaseEvent(self, event: QMouseEvent):
        try:
            if event.button() == Qt.LeftButton:
                self.__mousePressPos = None
                self.__mouseMovePos = None
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def touchEvent(self, touch_event):
        try:
            if touch_event.touchPointStates() & Qt.TouchPointMoved:
                touch_points = touch_event.touchPoints()
                if len(touch_points) == 2:
                    # Two finger scroll detected
                    old_pos = touch_points[0].lastPos()
                    new_pos = touch_points[1].lastPos()
                    delta = new_pos - old_pos

                    # Determine scroll direction
                    if abs(delta.x()) > abs(delta.y()):
                        pass
                    else:
                        if self.FunctionsStackedWidget.currentIndex() == 2:
                            if self.DownloadSwitcher_TabWidget.currentIndex() == 0:
                                self.JavaScrollArea.setValue(
                                    self.JavaScrollArea.value() - delta.y())
                            if self.DownloadSwitcher_TabWidget.currentIndex() == 1:
                                self.SpigotScrollArea.setValue(
                                    self.SpigotScrollArea.value() - delta.y())
                            if self.DownloadSwitcher_TabWidget.currentIndex() == 2:
                                self.PaperScrollArea.setValue(
                                    self.PaperScrollArea.value() - delta.y())
                            if self.DownloadSwitcher_TabWidget.currentIndex() == 3:
                                self.BungeeCordScrollArea.setValue(
                                    self.BungeeCordScrollArea.value() - delta.y())
                            if self.DownloadSwitcher_TabWidget.currentIndex() == 4:
                                self.OfficialCoreScrollArea.setValue(
                                    self.OfficialCoreScrollArea.value() - delta.y())
                            else:
                                pass
                        elif self.FunctionsStackedWidget.currentIndex() == 5:
                            self.SettingsScrollArea.setValue(
                                self.SettingsScrollArea.value() - delta.y())
                        elif self.FunctionsStackedWidget.currentIndex() == 6:
                            self.ChooseServerScrollArea.setValue(
                                self.ChooseServerScrollArea.value() - delta.y())
                        elif self.FunctionsStackedWidget.currentIndex() == 7:
                            self.ChooseJavaScrollArea.setValue(
                                self.ChooseJavaScrollArea.value() - delta.y())
                        elif self.FunctionsStackedWidget.currentIndex() == 8:
                            self.Update_Introduction_LabelScrollAreascrollArea.setValue(
                                self.Update_Introduction_LabelScrollAreascrollArea.value() - delta.y())
                        else:
                            pass
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def Quit(self):
        try:

            MCSLLogger.Log(Msg="Close_ButtonPressed", MsgArg=None,
                           MsgLevel=1)
            MCSLLogger.Log(Msg="MCSLExit", MsgArg=None, MsgLevel=0
                           )
            Aria2Controller.Shutdown()
            MCSLLogger.Log(Msg="Aria2Shutdown", MsgArg=None, MsgLevel=0
                           )
            MCSLProcess.quit()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def Minimize(self):
        try:

            MCSLLogger.Log(Msg="Minimize_PushButtonPressed", MsgArg=None,
                           MsgLevel=1)
            MCSLLogger.Log(Msg="WindowMinimize", MsgArg=None, MsgLevel=0
                           )
            MCSLMainWindow.showMinimized()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    # Pages Navigation
    def VisiblePagesNavigation(self):
        try:
            LoggerMsg = ["ToHomePage", "ToConfigPage", "ToDownloadPage", "ToConsolePage", "ToToolsPage",
                         "ToSettingsPage"]
            TitleBarSetting = MCSL2Settings().GetConfig(
                "UseTitleBarInsteadOfmacOSControlling")
            OptionsWidgetIndicatorPositionX = 20
            if TitleBarSetting:
                OptionsWidgetIndicatorPositionY = [120, 180, 240, 300, 360, 420]
            elif not TitleBarSetting:
                OptionsWidgetIndicatorPositionY = [150, 210, 270, 330, 390, 450]
            MCSLLogger.Log(Msg=LoggerMsg[self.MenuList.index(self.sender())], MsgArg=None, MsgLevel=0)
            self.MenuList[self.FunctionsStackedWidget.currentIndex()].setStyleSheet(OtherNavigationStyleSheet)
            self.FunctionsStackedWidget.setCurrentIndex(self.MenuList.index(self.sender()))
            self.sender().setStyleSheet(CurrentNavigationStyleSheet)
            self.OptionsWidgetIndicator.move(OptionsWidgetIndicatorPositionX, OptionsWidgetIndicatorPositionY[
                self.FunctionsStackedWidget.currentIndex()])
            if self.FunctionsStackedWidget.currentIndex() == 2:
                self.downloadUrlDict.clear()
                self.RefreshDownloadType()
            else:
                pass
            if self.FunctionsStackedWidget.currentIndex() == 5:
                self.InitSettingUI()
                self.LastUpdateTime.setText(f"最后一次检查更新时间：{MCSL2Settings().GetConfig(Type='LastUpdateTime')}")
                MCSLLogger.Log(Msg="ChangeCurrentVersionLabel", MsgArg=None, MsgLevel=0
                               )
                self.CurrentVersionLabel.setText(f"当前版本：{Version}")
            else:
                pass
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def LegacyToConfigPage(self):
        try:
            MCSLLogger.Log(Msg="ToConfigPage", MsgArg=None, MsgLevel=0)
            self.MenuList[self.FunctionsStackedWidget.currentIndex()].setStyleSheet(OtherNavigationStyleSheet)
            self.FunctionsStackedWidget.setCurrentIndex(1)
            self.ConfigModeWidget.setCurrentIndex(0)
            self.Config_Page_PushButton.setStyleSheet(CurrentNavigationStyleSheet)
            TitleBarSetting = MCSL2Settings().GetConfig(
                "UseTitleBarInsteadOfmacOSControlling")
            OptionsWidgetIndicatorPositionX = 20
            if TitleBarSetting:
                OptionsWidgetIndicatorPositionY = 180
            elif not TitleBarSetting:
                OptionsWidgetIndicatorPositionY = 210
            self.OptionsWidgetIndicator.move(OptionsWidgetIndicatorPositionX, OptionsWidgetIndicatorPositionY)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def LegacyToDownloadCore(self):
        try:
            MCSLLogger.Log(Msg="ToDownloadPage", MsgArg=None, MsgLevel=0)
            self.MenuList[self.FunctionsStackedWidget.currentIndex()].setStyleSheet(OtherNavigationStyleSheet)
            self.FunctionsStackedWidget.setCurrentIndex(2)
            self.Download_Page_PushButton.setStyleSheet(CurrentNavigationStyleSheet)
            TitleBarSetting = MCSL2Settings().GetConfig(
                "UseTitleBarInsteadOfmacOSControlling")
            OptionsWidgetIndicatorPositionX = 20
            if TitleBarSetting:
                OptionsWidgetIndicatorPositionY = 240
            elif not TitleBarSetting:
                OptionsWidgetIndicatorPositionY = 270
            self.OptionsWidgetIndicator.move(OptionsWidgetIndicatorPositionX, OptionsWidgetIndicatorPositionY)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def LegacyToAboutPage(self):
        try:
            MCSLLogger.Log(Msg="ToSettingsPage", MsgArg=None, MsgLevel=0)
            self.MenuList[self.FunctionsStackedWidget.currentIndex()].setStyleSheet(OtherNavigationStyleSheet)
            self.FunctionsStackedWidget.setCurrentIndex(5)
            self.About_Page_PushButton.setStyleSheet(CurrentNavigationStyleSheet)
            TitleBarSetting = MCSL2Settings().GetConfig(
                "UseTitleBarInsteadOfmacOSControlling")
            OptionsWidgetIndicatorPositionX = 20
            if TitleBarSetting:
                OptionsWidgetIndicatorPositionY = 420
            elif not TitleBarSetting:
                OptionsWidgetIndicatorPositionY = 450
            self.OptionsWidgetIndicator.move(OptionsWidgetIndicatorPositionX, OptionsWidgetIndicatorPositionY)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def ToChooseServerPage(self):
        try:
            global GlobalServerList
            MCSLLogger.Log(Msg="Choose_Server_PushButtonPressed", MsgArg=None, MsgLevel=0)
            MCSLLogger.Log(Msg="TryToGetGlobalServerList", MsgArg=None, MsgLevel=0)
            GlobalConfig = ReadGlobalServerConfig()
            ServerCount = GlobalConfig[0]
            GlobalServerList = GlobalConfig[1]
            if str(GlobalServerList) == "[]":
                MCSLLogger.Log(Msg="NoServerCanBeFound", MsgArg=None, MsgLevel=1)
                MCSLLogger.Log(Msg="ShowDialog", MsgArg="AskMode", MsgLevel=0)
                ReturnNum = CallMCSL2Dialog(
                    Tip="ServerControllerNoServerCanBeFound",
                    OtherTextArg=None,
                    isNeededTwoButtons=1, ButtonArg="添加|取消")
                if ReturnNum == 1:
                    self.LegacyToConfigPage()
                    QApplication.processEvents()
                else:
                    pass
            else:
                self.FunctionsStackedWidget.setCurrentIndex(6)
                MCSLLogger.Log(Msg="TryRefreshDownloadType", MsgArg=None, MsgLevel=1)
                self.InitSelectServerSubWidget(ServerCount, GlobalServerList)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def ToChooseJavaPage(self):
        try:
            global JavaPaths
            MCSLLogger.Log(Msg="ToChooseJavaPage", MsgArg=None, MsgLevel=0)
            self.FunctionsStackedWidget.setCurrentIndex(7)
            self.InitSelectJavaSubWidget()
            MCSLLogger.Log(Msg="StartInitSelectJavaSubWidget", MsgArg=None, MsgLevel=0)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    # Start Server
    def StartMCServerHelper(self):
        try:
            global GlobalServerList, ServerIndexNum
            MCSLLogger.Log(Msg="Start_PushButtonPressed", MsgArg=None, MsgLevel=0)
            MCSLLogger.Log(Msg="TryToGetGlobalServerList", MsgArg=None, MsgLevel=0)
            GlobalServerList = ReadGlobalServerConfig()[1]
            if str(GlobalServerList) == "[]":
                MCSLLogger.Log(Msg="NoServerCanBeFound", MsgArg=None, MsgLevel=1)
                MCSLLogger.Log(Msg="ShowDialog", MsgArg="AskMode", MsgLevel=0)
                ReturnNum = CallMCSL2Dialog(
                    Tip="ServerControllerNoServerCanBeFound",
                    OtherTextArg=None,
                    isNeededTwoButtons=1, ButtonArg="添加|取消")
                if ReturnNum == 1:
                    self.LegacyToConfigPage()
                    QApplication.processEvents()
                else:
                    pass
            else:
                MCSLLogger.Log(Msg="TryToGetServerConfig", MsgArg=None, MsgLevel=0)
                ServerLauncher().GetGlobalServerConfig(ServerIndexNum=ServerIndexNum)
                self.ToConsolePage()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    # Download Sources Changer
    def DownloadSourceChanger(self):
        try:
            global DownloadSource

            MCSLLogger.Log(Msg="ChangeDownloadSource", MsgArg=str(self.MCSLAPIDownloadSourceComboBox.currentText()),
                           MsgLevel=0)
            DownloadSource = self.MCSLAPIDownloadSourceComboBox.currentText()
            self.CurrentDownloadSourceLabel.setText(
                "当前下载源：" + str(DownloadSource))
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def ManuallySelectJava(self):
        try:

            MCSLLogger.Log(Msg="StartManuallySelectJava", MsgArg=None, MsgLevel=0)
            MCSLLogger.Log(Msg="ShowQFileDialog", MsgArg=None, MsgLevel=0)
            JavaPathSysList = QFileDialog.getOpenFileName(
                self, "选择java.exe程序", getcwd(), "java.exe"
            )
            if JavaPathSysList[0] != "":
                v = GetJavaVersion(JavaPathSysList[0])
                if not isinstance(v, CalledProcessError):
                    JavaPaths.append(Java(JavaPathSysList[0], v))
                    MCSLLogger.Log(Msg="ChooseJavaOK", MsgArg=f"\nJava路径：{JavaPathSysList[0]}\nJava版本：{v}",
                                   MsgLevel=0)
                else:
                    MCSLLogger.Log(Msg="ChooseJavaInvalid", MsgArg=None, MsgLevel=2)
                    CallMCSL2Dialog("ConfigPageQFileDialogInvalidJava", OtherTextArg=f"{v.output}",
                                    isNeededTwoButtons=0,
                                    ButtonArg=None)
            else:
                MCSLLogger.Log(Msg="ChooseJavaNothing", MsgArg=None, MsgLevel=1)
                CallMCSL2Dialog("ConfigPageQFileDialogNoJava",
                                OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def ManuallyImportCore(self):
        try:

            global CorePath, CoreFileName
            MCSLLogger.Log(Msg="StartManuallySelectCore", MsgArg=None, MsgLevel=0)
            MCSLLogger.Log(Msg="ShowQFileDialog", MsgArg=None, MsgLevel=0)
            CoreSysList = QFileDialog.getOpenFileName(
                self, "选择服务器核心", getcwd(), "*.jar")
            if CoreSysList[0] != "":
                CorePath = CoreSysList[0]
                CoreFileName = CorePath.split("/")
                CoreFileName = CoreFileName[-1]
                MCSLLogger.Log(Msg="ChooseCoreOK", MsgArg=CoreFileName, MsgLevel=0)
            else:
                MCSLLogger.Log(Msg="ChooseCoreNothing", MsgArg=None, MsgLevel=1)
                CallMCSL2Dialog("ConfigPageQFileDialogNoCore",
                                OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def SaveMinecraftServer(self):
        try:

            global JavaPath, MaxMemory, MinMemory, CoreFileName, CanCreate
            """
            0 -> Illegal
            1 -> OK
            """
            MCSLLogger.Log(Msg="StartSaveMinecraftServer", MsgArg=None, MsgLevel=1)
            # The server core detector
            if CoreFileName != "":
                CoreStatus = 1
            else:
                CoreStatus = 0

            # The Java path parser
            if JavaPath != 0:
                if len(JavaPaths) != 0:
                    JavaStatus = 1
                else:
                    JavaStatus = 0
            else:
                JavaStatus = 0

            # The min memory parser
            if self.MinMemory_LineEdit.text() != "":
                ChkMin = self.MinMemory_LineEdit.text()
                if (
                        ChkMin.isdigit()
                        and int(self.MinMemory_LineEdit.text()) % 1 == 0
                        and int(self.MinMemory_LineEdit.text()) != 0
                ):
                    MinMemory = int(self.MinMemory_LineEdit.text())
                    MinMemStatus = 1
                else:
                    MinMemStatus = 0
            else:
                MinMemStatus = 0

            # The max memory parser
            if self.MaxMemory_LineEdit.text() != "":
                ChkMax = self.MaxMemory_LineEdit.text()
                if (
                        ChkMax.isdigit()
                        and int(self.MaxMemory_LineEdit.text()) % 1 == 0
                        and int(self.MaxMemory_LineEdit.text()) != 0
                ):
                    MaxMemory = int(self.MaxMemory_LineEdit.text())
                    MaxMemStatus = 1
                else:
                    MaxMemStatus = 0
            else:
                MaxMemStatus = 0

            # The server name parser
            if self.Server_Name_LineEdit.text() != "":
                TMPServerName = self.Server_Name_LineEdit.text()
                IllegalCodeList = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
                for i in range(len(IllegalCodeList)):
                    if not IllegalCodeList[i] in TMPServerName:
                        pass
                    else:
                        NameStatus = 0
                Path1 = ".\\" + TMPServerName
                if not ospath.exists(f"./Servers/{TMPServerName}"):
                    global ServerName
                    ServerName = TMPServerName
                    NameStatus = 1
                else:
                    NameStatus = 0
            else:
                NameStatus = 0

            # Pop-up determine
            # Create List
            ChkVal = []
            ChkVal.append(MinMemStatus)
            ChkVal.append(MaxMemStatus)
            ChkVal.append(NameStatus)
            ChkVal.append(JavaStatus)
            ChkVal.append(CoreStatus)
            CheckAvailable = CheckAvailableSaveServer(ChkVal)
            CanCreate = CheckAvailable[0]
            Tip = CheckAvailable[1]
            Log = CheckAvailable[2]

            # Server processor
            if CanCreate == 0:
                MCSLLogger.Log(Msg=Log, MsgArg=None, MsgLevel=2)
                MCSLLogger.Log(Msg="AddServerFailed", MsgArg=None, MsgLevel=2)
                CallMCSL2Dialog(Tip, OtherTextArg=None,
                                isNeededTwoButtons=0, ButtonArg=None)
            elif CanCreate == 1:
                MCSLLogger.Log(Msg=Log, MsgArg=None, MsgLevel=0)
                CallMCSL2Dialog(Tip, OtherTextArg=None,
                                isNeededTwoButtons=0, ButtonArg=None)
                AddServerType = None
                if self.ConfigModeWidget.currentIndex() == 1:
                    AddServerType = "noob"
                elif self.ExMemoryUnitComboBox.currentText() == "M":
                    AddServerType = "extended_m"
                elif self.ExMemoryUnitComboBox.currentText() == "G":
                    AddServerType = "extended_g"
                # noinspection PyUnboundLocalVariable
                SaveServer(ServerName=ServerName, CorePath=CorePath, JavaPath=JavaPath, MinMemory=MinMemory,
                           MaxMemory=MaxMemory, CoreFileName=CoreFileName, AddServerType=AddServerType)
                MinMemStatus = 0
                MaxMemStatus = 0
                NameStatus = 0
                JavaStatus = 0
                CoreStatus = 0
                JavaPath = 0
                MCSLLogger.Log(Msg="AddServerSuccess", MsgArg=None, MsgLevel=0)
            else:
                MCSLLogger.Log(Msg="AddServerUnexpectedFailed", MsgArg=None, MsgLevel=3)
                CallMCSL2Dialog("ConfigPageAddServerUnexpectedFailed", OtherTextArg=None, isNeededTwoButtons=0,
                                ButtonArg=None)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def AutoDetectJava(self):
        try:

            # 防止同时多次运行worker线程
            MCSLLogger.Log(Msg="StartAutoDetectJava", MsgArg=None, MsgLevel=0)
            self.Auto_Find_Java_PushButton.setDisabled(True)
            self.JavaFindWorkThreadFactory.Create().start()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @pyqtSlot(list)
    def JavaDetectFinished(self, _JavaPaths: list):
        try:
            global JavaPaths

            global JavaPathList
            # 向前兼容
            if ospath.exists("MCSL2/AutoDetectJavaHistory.txt"):
                remove("MCSL2/AutoDetectJavaHistory.txt")
            with open("MCSL2/AutoDetectJavaHistory.json", 'w+', encoding='utf-8') as SaveFoundedJava:
                JavaPaths = list({p[:-1] for p in SaveFoundedJava.readlines()
                                  }.union(set(JavaPaths)).union(set(_JavaPaths)))
                JavaPaths.sort(key=lambda x: x.Version, reverse=False)
                JavaPathList = [{"Path": e.Path, "Version": e.Version}
                                for e in JavaPaths]
                # 获取新发现的Java路径,或者用户选择的Java路径
                dump({"java": JavaPathList}, SaveFoundedJava,
                     sort_keys=True, indent=4, ensure_ascii=False)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @pyqtSlot(int)
    def OnJavaFindWorkThreadFinished(self, sequenceNumber):
        try:

            # 如果不是第一次运行worker线程
            if sequenceNumber > 1:
                MCSLLogger.Log(Msg="FinishedAutoDetectJava", MsgArg=f"{JavaPathList}\n共搜索到{len(JavaPaths)}个Java",
                               MsgLevel=0)
                CallMCSL2Dialog("ConfigPageAutoDetectJavaFinished", OtherTextArg=str(len(JavaPaths)),
                                isNeededTwoButtons=0,
                                ButtonArg=None)

            # 释放AutoDetectJava中禁用的按钮
            self.Auto_Find_Java_PushButton.setEnabled(True)
            # 更新self.ChooseJavaScrollAreaVerticalLayout中的内容
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def ShowFoundedJavaList_Back(self):
        try:

            MCSLLogger.Log(Msg="ManuallySkipChooseGotJava", MsgArg=None, MsgLevel=0)
            self.FunctionsStackedWidget.setCurrentIndex(1)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def ToDownloadJava(self):
        try:
            self.MenuList[self.FunctionsStackedWidget.currentIndex()].setStyleSheet(OtherNavigationStyleSheet)
            MCSLLogger.Log(Msg="GoToDownloadJava", MsgArg=None, MsgLevel=0)
            self.FunctionsStackedWidget.setCurrentIndex(2)
            self.MenuList[self.FunctionsStackedWidget.currentIndex()].setStyleSheet(CurrentNavigationStyleSheet)
            TitleBarSetting = MCSL2Settings().GetConfig(
                "UseTitleBarInsteadOfmacOSControlling")
            OptionsWidgetIndicatorPositionX = 20
            if TitleBarSetting:
                OptionsWidgetIndicatorPositionY = 240
            elif not TitleBarSetting:
                OptionsWidgetIndicatorPositionY = 270
            self.OptionsWidgetIndicator.move(OptionsWidgetIndicatorPositionX, OptionsWidgetIndicatorPositionY)
            MCSLLogger.Log(Msg="SelectJavaDownload", MsgArg=None, MsgLevel=0)
            self.DownloadSwitcher_TabWidget.setCurrentIndex(0)
            self.RefreshDownloadType()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    # The function of refreshing download type.
    def RefreshDownloadType(self):
        try:
            global DownloadSource, DownloadUrls

            MCSLLogger.Log(Msg="TryRefreshDownloadType", MsgArg=None, MsgLevel=1)
            # 如果存在DownloadSource且不为空,则不再重新获取
            if self.downloadUrlDict.get(DownloadSource) is not None:
                MCSLLogger.Log(Msg="NoNeedToRefreshDownloadType", MsgArg=None, MsgLevel=1)
                idx = self.DownloadSwitcher_TabWidget.currentIndex()
                self.InitDownloadSubWidget(
                    self.downloadUrlDict[DownloadSource][idx]['SubWidgetNames'])
                self.DownloadURLList = self.downloadUrlDict[DownloadSource][idx]['DownloadUrls']

            else:
                MCSLLogger.Log(Msg="StartInitDownloadSubWidget", MsgArg=None, MsgLevel=0)
                idx = self.DownloadSwitcher_TabWidget.currentIndex()
                self.RefreshingTip = QLabel()
                self.RefreshingTip.setGeometry(QRect(30, 80, 221, 51))
                font = QFont()
                font.setFamily("Microsoft YaHei UI")
                font.setPointSize(16)
                font.setWeight(75)
                self.RefreshingTip.setFont(font)
                self.RefreshingTip.setObjectName("RefreshingTip")
                self.RefreshingTip.setText("加载中\n\n")
                if idx == 0:
                    self.JavaVerticalLayout.addWidget(self.RefreshingTip)
                    self.JavaVerticalLayout.addWidget(
                        IndeterminateProgressBar(self))
                elif idx == 1:
                    self.SpigotVerticalLayout.addWidget(self.RefreshingTip)
                    self.SpigotVerticalLayout.addWidget(
                        IndeterminateProgressBar(self))
                elif idx == 2:
                    self.PaperVerticalLayout.addWidget(self.RefreshingTip)
                    self.PaperVerticalLayout.addWidget(
                        IndeterminateProgressBar(self))
                elif idx == 3:
                    self.BCVerticalLayout.addWidget(self.RefreshingTip)
                    self.BCVerticalLayout.addWidget(IndeterminateProgressBar(self))
                elif idx == 4:
                    self.OfficialCoreVerticalLayout.addWidget(self.RefreshingTip)
                    self.OfficialCoreVerticalLayout.addWidget(
                        IndeterminateProgressBar(self))
                else:
                    pass
                MCSLLogger.Log(Msg="StartRefreshDownloadType", MsgArg=None, MsgLevel=1)
                workThread = self.fetchDownloadURLThreadFactory.create(
                    downloadSrc=DownloadSource,
                    _singleton=True,
                    finishSlot=self.updateDownloadUrlDict
                )
                if workThread.isRunning():
                    return
                else:
                    workThread.start()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @pyqtSlot(dict)
    def updateDownloadUrlDict(self, _downloadUrlDict: dict):
        try:

            self.downloadUrlDict.update(_downloadUrlDict)
            self.RefreshDownloadType()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    @staticmethod
    def GetDownloadSubWidgetImage(GraphType):
        try:
            if GraphType == 0:
                return QPixmap(":/MCSL2_Icon/JavaIcon.png")
            elif GraphType == 1:
                return QPixmap(":/MCSL2_Icon/SpigotIcon.png")
            elif GraphType == 2:
                return QPixmap(":/MCSL2_Icon/PaperIcon.png")
            elif GraphType == 3:
                return QPixmap(":/MCSL2_Icon/BungeeCordIcon.png")
            elif GraphType == 4:
                return QPixmap(":/MCSL2_Icon/OfficialCoreIcon.png")
            else:
                return None
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def InitDownloadSubWidget(self, SubWidgetNames):
        try:

            GraphType = self.DownloadSwitcher_TabWidget.currentIndex()
            image = self.GetDownloadSubWidgetImage(GraphType)
            if GraphType == 0:
                self.initDownloadLayout(
                    self.JavaVerticalLayout, SubWidgetNames, QPixmap(":/MCSL2_Icon/JavaIcon.png"))
            elif GraphType == 1:
                self.initDownloadLayout(self.SpigotVerticalLayout, SubWidgetNames, image)
            elif GraphType == 2:
                self.initDownloadLayout(self.PaperVerticalLayout, SubWidgetNames, image)
            elif GraphType == 3:
                self.initDownloadLayout(self.BCVerticalLayout, SubWidgetNames, image)
            elif GraphType == 4:
                self.initDownloadLayout(self.OfficialCoreVerticalLayout, SubWidgetNames, image)
            else:
                pass
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def initDownloadSubWidget(self, i):
        try:

            self.MCSL2_SubWidget_Download = QWidget()
            self.MCSL2_SubWidget_Download.setGeometry(QRect(150, 190, 620, 70))
            self.MCSL2_SubWidget_Download.setMinimumSize(QSize(620, 70))
            self.MCSL2_SubWidget_Download.setStyleSheet(
                "QWidget\n"
                "{\n"
                "    border-radius: 4px;\n"
                "    background-color: rgba(247, 247, 247, 247)\n"
                "}"
            )
            self.MCSL2_SubWidget_Download.setObjectName("MCSL2_SubWidget_Download")
            self.IntroductionWidget_D = QWidget(self.MCSL2_SubWidget_Download)
            self.IntroductionWidget_D.setGeometry(QRect(100, 10, 421, 51))
            self.IntroductionWidget_D.setMinimumSize(QSize(421, 51))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(10)
            self.IntroductionWidget_D.setFont(font)
            self.IntroductionWidget_D.setStyleSheet(
                "QWidget\n"
                "{\n"
                "    background-color: rgb(247, 247, 247);\n"
                "    border-radius: 8px\n"
                "}"
            )
            self.IntroductionWidget_D.setObjectName("IntroductionWidget_D")
            self.IntroductionLabel_D = QLabel(self.IntroductionWidget_D)
            self.IntroductionLabel_D.setGeometry(QRect(10, 0, 401, 51))
            self.IntroductionLabel_D.setMinimumSize(QSize(401, 51))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(10)
            self.IntroductionLabel_D.setFont(font)
            self.IntroductionLabel_D.setText("")
            self.IntroductionLabel_D.setObjectName("IntroductionLabel_D")
            self.Download_PushButton = QPushButton(self.MCSL2_SubWidget_Download)
            self.Download_PushButton.setGeometry(QRect(540, 10, 51, 51))
            self.Download_PushButton.setMinimumSize(QSize(51, 51))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(10)
            self.Download_PushButton.setFont(font)
            self.Download_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
            self.Download_PushButton.setStyleSheet(
                "QPushButton\n"
                "{\n"
                "    background-color: rgb(0, 120, 212);\n"
                "    border-radius: 8px;\n"
                "    color: rgb(255, 255, 255);\n"
                "}\n"
                "QPushButton:hover\n"
                "{\n"
                "    background-color: rgb(0, 110, 212);\n"
                "    border-radius: 8px;\n"
                "    color: rgb(255, 255, 255);\n"
                "}\n"
                "QPushButton:pressed\n"
                "{\n"
                "    background-color: rgb(0, 100, 212);\n"
                "    border-radius: 8px;\n"
                "    color: rgb(255, 255, 255);\n"
                "}"
            )
            self.Download_PushButton.setFlat(False)
            self.Download_PushButton.setObjectName("Download_PushButton" + str(i))
            self.GraphWidget_D = QLabel(self.MCSL2_SubWidget_Download)
            self.GraphWidget_D.setGeometry(QRect(30, 10, 51, 51))
            self.GraphWidget_D.setMinimumSize(QSize(51, 51))
            self.GraphWidget_D.setStyleSheet(
                "QLabel\n"
                "{\n"
                "    background-color: rgb(247, 247, 247);\n"
                "    border-radius: 4px;\n"
                "}"
            )
            self.GraphWidget_D.setText("")
            self.GraphWidget_D.setObjectName("GraphWidget_D")
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def initDownloadLayout(self, layout, subWidgetNames, pixMap):
        try:

            if subWidgetNames == -2:
                Tip = "DownloadPageConnectToMCSLAPIFailed"
                CallMCSL2Dialog(Tip, OtherTextArg=None,
                                isNeededTwoButtons=0, ButtonArg=None)
                return
            elif subWidgetNames == -1:
                Tip = "DownloadPageEncodeMCSLAPIContentFailed"
                CallMCSL2Dialog(Tip, OtherTextArg=None,
                                isNeededTwoButtons=0, ButtonArg=None)
                return

            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
            for i in range(len(subWidgetNames)):
                self.initDownloadSubWidget(i)
                self.GraphWidget_D.setPixmap(pixMap)
                self.GraphWidget_D.setScaledContents(True)
                self.IntroductionLabel_D.setText(subWidgetNames[i])
                self.Download_PushButton.setText("下载")
                self.Download_PushButton.clicked.connect(
                    lambda: self.ParseSrollAreaItemButtons()
                )
                layout.addWidget(self.MCSL2_SubWidget_Download)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def InitSelectJavaSubWidget(self):
        try:
            global JavaPaths

            MCSLLogger.Log(Msg="StartInitSelectJavaSubWidget", MsgArg=None, MsgLevel=0)
            for i in reversed(range(self.ChooseJavaScrollAreaVerticalLayout.count())):
                self.ChooseJavaScrollAreaVerticalLayout.itemAt(
                    i).widget().setParent(None)

            for i in range(len(JavaPaths)):
                self.MCSL2_SubWidget_Select = QWidget()
                self.MCSL2_SubWidget_Select.setGeometry(QRect(150, 110, 620, 70))
                self.MCSL2_SubWidget_Select.setMinimumSize(QSize(620, 70))
                self.MCSL2_SubWidget_Select.setStyleSheet(
                    "QWidget\n"
                    "{\n"
                    "    border-radius: 4px;\n"
                    "    background-color: rgba(247, 247, 247, 247)\n"
                    "}"
                )
                self.MCSL2_SubWidget_Select.setObjectName("MCSL2_SubWidget_Select")
                self.Select_PushButton = QPushButton(self.MCSL2_SubWidget_Select)
                self.Select_PushButton.setGeometry(QRect(540, 10, 51, 51))
                self.Select_PushButton.setMinimumSize(QSize(51, 51))
                font = QFont()
                font.setFamily("Microsoft YaHei UI")
                font.setPointSize(10)
                self.Select_PushButton.setFont(font)
                self.Select_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
                self.Select_PushButton.setStyleSheet(
                    "QPushButton\n"
                    "{\n"
                    "    background-color: rgb(0, 120, 212);\n"
                    "    border-radius: 8px;\n"
                    "    color: rgb(255, 255, 255);\n"
                    "}\n"
                    "QPushButton:hover\n"
                    "{\n"
                    "    background-color: rgb(0, 110, 212);\n"
                    "    border-radius: 8px;\n"
                    "    color: rgb(255, 255, 255);\n"
                    "}\n"
                    "QPushButton:pressed\n"
                    "{\n"
                    "    background-color: rgb(0, 100, 212);\n"
                    "    border-radius: 8px;\n"
                    "    color: rgb(255, 255, 255);\n"
                    "}"
                )
                self.Select_PushButton.setFlat(False)
                self.Select_PushButton.setObjectName("Select_PushButton" + str(i))
                self.IntroductionWidget_S = QWidget(self.MCSL2_SubWidget_Select)
                self.IntroductionWidget_S.setGeometry(QRect(100, 10, 421, 51))
                self.IntroductionWidget_S.setMinimumSize(QSize(421, 51))
                font = QFont()
                font.setFamily("Microsoft YaHei UI")
                font.setPointSize(10)
                self.IntroductionWidget_S.setFont(font)
                self.IntroductionWidget_S.setStyleSheet(
                    "QWidget\n"
                    "{\n"
                    "    background-color: rgb(247, 247, 247);\n"
                    "    border-radius: 8px\n"
                    "}"
                )
                self.IntroductionWidget_S.setObjectName("IntroductionWidget_S")
                self.IntroductionLabel_S = QLabel(self.IntroductionWidget_S)
                self.IntroductionLabel_S.setGeometry(QRect(10, 0, 401, 51))
                self.IntroductionLabel_S.setMinimumSize(QSize(401, 51))
                font = QFont()
                font.setFamily("Microsoft YaHei UI")
                font.setPointSize(10)
                self.IntroductionLabel_S.setFont(font)
                self.IntroductionLabel_S.setText("")
                self.IntroductionLabel_S.setObjectName("IntroductionLabel_S")
                self.GraphWidget_S = QLabel(self.MCSL2_SubWidget_Select)
                self.GraphWidget_S.setGeometry(QRect(30, 10, 51, 51))
                self.GraphWidget_S.setMinimumSize(QSize(51, 51))
                self.GraphWidget_S.setStyleSheet(
                    "QLabel\n"
                    "{\n"
                    "    background-color: rgb(247, 247, 247);\n"
                    "    border-radius: 4px;\n"
                    "}"
                )
                self.GraphWidget_S.setText("")
                self.GraphWidget_S.setObjectName("GraphWidget_S")
                self.GraphWidget_S.setPixmap(QPixmap(":/MCSL2_Icon/JavaIcon.png"))
                self.GraphWidget_S.setScaledContents(True)
                self.IntroductionLabel_S.setText(
                    "Java版本：" + JavaPaths[i].Version + "\n" + JavaPaths[i].Path)
                self.Select_PushButton.setText("选择")
                self.Select_PushButton.clicked.connect(
                    lambda: self.ParseSrollAreaItemButtons())

                self.ChooseJavaScrollAreaVerticalLayout.addWidget(
                    self.MCSL2_SubWidget_Select)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def InitSelectServerSubWidget(self, ServerCount, ServerInfoJSON):
        try:

            for i in reversed(range(self.ChooseServerScrollAreaVerticalLayout.count())):
                self.ChooseServerScrollAreaVerticalLayout.itemAt(
                    i).widget().setParent(None)

            for i in range(ServerCount):
                WidgetServerName = f"名称：{ServerInfoJSON[i]['name']}\n"
                WidgetCoreFileName = f"服务器核心文件：{ServerInfoJSON[i]['core_file_name']}\n"
                WidgetJavaPath = f"Java路径：{ServerInfoJSON[i]['java_path']}\n"
                WidgetMinMemory = f"Java最小内存：{ServerInfoJSON[i]['min_memory']}\n"
                WidgetMaxMemory = f"Java最大内存：{ServerInfoJSON[i]['max_memory']}\n"
                if ServerInfoJSON[i]['jvm_arg'] == "":
                    WidgetJavaArg = "JVM参数：无"
                else:
                    WidgetJavaArg = f"JVM参数：{ServerInfoJSON[i]['jvm_arg']}"
                ServerInfo = WidgetServerName + WidgetCoreFileName + \
                             WidgetJavaPath + WidgetMinMemory + WidgetMaxMemory + WidgetJavaArg
                MCSLLogger.Log(Msg="GotServerInfo", MsgArg=f" - 第{i}个：\nServerInfo", MsgLevel=0)
                self.MCSL2_SubWidget_SelectS = QWidget()
                self.MCSL2_SubWidget_SelectS.setGeometry(QRect(150, 270, 620, 171))
                self.MCSL2_SubWidget_SelectS.setMinimumSize(QSize(620, 171))
                self.MCSL2_SubWidget_SelectS.setMaximumSize(QSize(620, 171))
                self.MCSL2_SubWidget_SelectS.setStyleSheet("QWidget\n"
                                                           "{\n"
                                                           "    border-radius: 4px;\n"
                                                           "    background-color: rgba(247, 247, 247, 247)\n"
                                                           "}")
                self.MCSL2_SubWidget_SelectS.setObjectName(
                    "MCSL2_SubWidget_SelectS")
                self.SelectS_PushButton = QPushButton(self.MCSL2_SubWidget_SelectS)
                self.SelectS_PushButton.setGeometry(QRect(540, 60, 51, 51))
                self.SelectS_PushButton.setMinimumSize(QSize(51, 51))
                font = QFont()
                font.setFamily("Microsoft YaHei UI")
                font.setPointSize(10)
                self.SelectS_PushButton.setFont(font)
                self.SelectS_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
                self.SelectS_PushButton.setStyleSheet("QPushButton\n"
                                                      "{\n"
                                                      "    background-color: rgb(0, 120, 212);\n"
                                                      "    border-radius: 8px;\n"
                                                      "    color: rgb(255, 255, 255);\n"
                                                      "}\n"
                                                      "QPushButton:hover\n"
                                                      "{\n"
                                                      "    background-color: rgb(0, 110, 212);\n"
                                                      "    border-radius: 8px;\n"
                                                      "    color: rgb(255, 255, 255);\n"
                                                      "}\n"
                                                      "QPushButton:pressed\n"
                                                      "{\n"
                                                      "    background-color: rgb(0, 100, 212);\n"
                                                      "    border-radius: 8px;\n"
                                                      "    color: rgb(255, 255, 255);\n"
                                                      "}")
                self.SelectS_PushButton.setFlat(False)
                self.SelectS_PushButton.setObjectName(
                    "SelectS_PushButton" + str(i))
                self.IntroductionWidget_SS = QWidget(self.MCSL2_SubWidget_SelectS)
                self.IntroductionWidget_SS.setGeometry(QRect(80, 10, 451, 151))
                self.IntroductionWidget_SS.setMinimumSize(QSize(421, 51))
                font = QFont()
                font.setFamily("Microsoft YaHei UI")
                font.setPointSize(10)
                self.IntroductionWidget_SS.setFont(font)
                self.IntroductionWidget_SS.setStyleSheet("QWidget\n"
                                                         "{\n"
                                                         "    background-color: rgb(247, 247, 247);\n"
                                                         "    border-radius: 8px\n"
                                                         "}")
                self.IntroductionWidget_SS.setObjectName("IntroductionWidget_SS")
                self.IntroductionLabel_SS = QLabel(self.IntroductionWidget_SS)
                self.IntroductionLabel_SS.setGeometry(QRect(10, 5, 431, 141))
                self.IntroductionLabel_SS.setMinimumSize(QSize(401, 51))
                font = QFont()
                font.setFamily("Microsoft YaHei UI")
                font.setPointSize(10)
                self.IntroductionLabel_SS.setFont(font)
                self.IntroductionLabel_SS.setText("")
                self.IntroductionLabel_SS.setObjectName("IntroductionLabel_SS")
                self.GraphWidget_SS = QLabel(self.MCSL2_SubWidget_SelectS)
                self.GraphWidget_SS.setGeometry(QRect(20, 60, 51, 51))
                self.GraphWidget_SS.setMinimumSize(QSize(51, 51))
                self.GraphWidget_SS.setStyleSheet("QLabel\n"
                                                  "{\n"
                                                  "    background-color: rgb(247, 247, 247);\n"
                                                  "    border-radius: 4px;\n"
                                                  "}")
                self.GraphWidget_SS.setText("")
                self.GraphWidget_SS.setScaledContents(True)
                self.GraphWidget_SS.setPixmap(QPixmap(":/MCSL2_Icon/JavaIcon.png"))
                self.GraphWidget_SS.setObjectName("GraphWidget_SS")
                self.IntroductionLabel_SS.setText(str(ServerInfo))
                self.SelectS_PushButton.setText("选择")
                self.SelectS_PushButton.clicked.connect(
                    lambda: self.ParseSrollAreaItemButtons())
                self.ChooseServerScrollAreaVerticalLayout.addWidget(
                    self.MCSL2_SubWidget_SelectS)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def ParseSrollAreaItemButtons(self):
        try:

            MCSLLogger.Log(Msg="RunParseSrollAreaItemButtons", MsgArg=str(self.FunctionsStackedWidget.currentIndex()),
                           MsgLevel=0)
            SelectDownloadItemIndexNumber = int(
                str(self.sender().objectName()).split("_PushButton")[1])
            MCSLLogger.Log(Msg="SrollAreaItemButtonNum", MsgArg=str(SelectDownloadItemIndexNumber), MsgLevel=0)
            if self.FunctionsStackedWidget.currentIndex() == 7:
                self.ChooseJava(JavaIndex=SelectDownloadItemIndexNumber)
            if self.FunctionsStackedWidget.currentIndex() == 6:
                self.ChooseServer(ServerIndex=SelectDownloadItemIndexNumber)
            if self.FunctionsStackedWidget.currentIndex() == 2:
                self.Download(DownloadItemIndex=SelectDownloadItemIndexNumber)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def InitDownloadProgressUI(self):
        # TODO 为界面添加eta以及文件大小等显示位置，如果需要的话,请注意，我通过手动修改的方式来调节了组件的位置，但我不确定UI文件里是否也有相应的修改，如果有的话，uic生成的文件记得比较一下异同
        try:
            self.MCSL2_DownloadProgress = QWidget(self.CentralWidget)
            setattr(self.MCSL2_DownloadProgress, "DownloadWatcher", None)
            self.MCSL2_DownloadProgress.setObjectName("MCSL2_DownloadProgress")
            self.MCSL2_DownloadProgress.resize(962, 601)
            sizePolicy = QSizePolicy(
                QSizePolicy.Fixed, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.MCSL2_DownloadProgress.sizePolicy().hasHeightForWidth())
            self.MCSL2_DownloadProgress.setSizePolicy(sizePolicy)
            self.MCSL2_DownloadProgress.setMinimumSize(QSize(962, 601))
            self.MCSL2_DownloadProgress.setMaximumSize(QSize(962, 601))
            self.Shadow = QLabel(self.MCSL2_DownloadProgress)
            self.Shadow.setGeometry(QRect(8, 8, 945, 585))
            self.Shadow.setStyleSheet("QLabel\n"
                                      "{\n"
                                      "    background-color: rgba(130, 130, 130, 50%);\n"
                                      "    border-radius: 10px\n"
                                      "}")
            self.Shadow.setText("")
            self.Shadow.setObjectName("Shadow")
            self.DownloadProgressWidget = QWidget(self.MCSL2_DownloadProgress)
            self.DownloadProgressWidget.setGeometry(QRect(8, 8, 945, 585))
            sizePolicy = QSizePolicy(
                QSizePolicy.Fixed, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.DownloadProgressWidget.sizePolicy().hasHeightForWidth())
            self.DownloadProgressWidget.setSizePolicy(sizePolicy)
            self.DownloadProgressWidget.setMinimumSize(QSize(945, 585))
            self.DownloadProgressWidget.setMaximumSize(QSize(945, 585))
            self.DownloadProgressWidget.setStyleSheet("QWidget\n"
                                                      "{\n"
                                                      "    border-radius: 10px;\n"
                                                      "    background-color: transparent;\n"
                                                      "}")
            self.DownloadProgressWidget.setObjectName("DownloadProgressWidget")
            self.gridLayout = QGridLayout(self.DownloadProgressWidget)
            self.gridLayout.setContentsMargins(0, 0, 0, 0)
            self.gridLayout.setObjectName("gridLayout")
            self.RealDownloadProgress = QWidget(
                self.DownloadProgressWidget)
            sizePolicy = QSizePolicy(
                QSizePolicy.Fixed, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.RealDownloadProgress.sizePolicy().hasHeightForWidth())
            self.RealDownloadProgress.setSizePolicy(sizePolicy)
            self.RealDownloadProgress.setMinimumSize(QSize(441, 181))
            self.RealDownloadProgress.setMaximumSize(QSize(441, 181))
            self.RealDownloadProgress.setStyleSheet("QWidget\n"
                                                    "{\n"
                                                    "    border-radius: 4px;\n"
                                                    "    background-color: rgba(247, 247, 247, 247)\n"
                                                    "}")
            self.RealDownloadProgress.setObjectName("RealDownloadProgress")
            self.GraphWidget_DownloadProgress = QLabel(
                self.RealDownloadProgress)
            self.GraphWidget_DownloadProgress.setGeometry(
                QRect(17, 60, 51, 51))
            self.GraphWidget_DownloadProgress.setMinimumSize(QSize(51, 51))
            self.GraphWidget_DownloadProgress.setStyleSheet("QLabel\n"
                                                            "{\n"
                                                            "    background-color: rgb(247, 247, 247);\n"
                                                            "    border-radius: 4px;\n"
                                                            "}")
            self.GraphWidget_DownloadProgress.setText("")
            self.GraphWidget_DownloadProgress.setScaledContents(True)
            self.GraphWidget_DownloadProgress.setObjectName(
                "GraphWidget_DownloadProgress")
            self.DownloadingFileNameLabel = QLabel(
                self.RealDownloadProgress)
            self.DownloadingFileNameLabel.setGeometry(
                QRect(80, 35, 311, 31))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(11)
            self.DownloadingFileNameLabel.setFont(font)
            self.DownloadingFileNameLabel.setTextFormat(Qt.PlainText)
            self.DownloadingFileNameLabel.setScaledContents(True)
            self.DownloadingFileNameLabel.setText("正在下载：")
            self.DownloadingFileNameLabel.setObjectName("DownloadingFileNameLabel")
            self.DownloadingSpeedLabel = QLabel(
                self.RealDownloadProgress)
            self.DownloadingSpeedLabel.setGeometry(QRect(80, 100, 161, 31))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(11)
            self.DownloadingSpeedLabel.setFont(font)
            self.DownloadingSpeedLabel.setTextFormat(Qt.PlainText)
            self.DownloadingSpeedLabel.setScaledContents(True)
            self.DownloadingSpeedLabel.setText("速度：")
            self.DownloadingSpeedLabel.setObjectName("DownloadingSpeedLabel")
            self.CancelDownloadPushButton = QPushButton(
                self.RealDownloadProgress)
            self.CancelDownloadPushButton.setGeometry(
                QRect(340, 130, 81, 31))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(10)
            self.CancelDownloadPushButton.setFont(font)
            self.CancelDownloadPushButton.setCursor(
                QCursor(Qt.PointingHandCursor))
            self.CancelDownloadPushButton.setText("取消")
            self.CancelDownloadPushButton.setStyleSheet("QPushButton\n"
                                                        "{\n"
                                                        "    background-color: rgb(0, 120, 212);\n"
                                                        "    border-radius: 6px;\n"
                                                        "    color: rgb(255, 255, 255);\n"
                                                        "}\n"
                                                        "QPushButton:hover\n"
                                                        "{\n"
                                                        "    background-color: rgb(0, 80, 212);\n"
                                                        "    border-radius: 6px;\n"
                                                        "    color: rgb(255, 255, 255);\n"
                                                        "}\n"
                                                        "QPushButton:pressed\n"
                                                        "{\n"
                                                        "    background-color: rgb(0, 100, 212);\n"
                                                        "    border-radius: 6px;\n"
                                                        "    color: rgb(255, 255, 255);\n"
                                                        "}")
            self.CancelDownloadPushButton.setFlat(False)
            self.CancelDownloadPushButton.setObjectName("CancelDownloadPushButton")
            self.DownloadingInfoWidget = QWidget(
                self.RealDownloadProgress)
            self.DownloadingInfoWidget.setGeometry(QRect(70, 70, 330, 26))
            self.DownloadingInfoWidget.setObjectName("DownloadingInfoWidget")
            self.DownloadingPercentLabel = QLabel(
                self.DownloadingInfoWidget)
            self.DownloadingPercentLabel.setGeometry(QRect(270, 0, 61, 26))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(11)
            self.DownloadingPercentLabel.setFont(font)
            self.DownloadingPercentLabel.setTextFormat(Qt.PlainText)
            self.DownloadingPercentLabel.setScaledContents(True)
            self.DownloadingPercentLabel.setText("%")
            self.DownloadingPercentLabel.setObjectName("DownloadingPercentLabel")
            self.ProgressBar = ProgressBar(self.DownloadingInfoWidget)
            self.ProgressBar.setGeometry(QRect(10, 10, 251, 4))
            self.ProgressBar.setObjectName("ProgressBar")
            self.gridLayout.addWidget(self.RealDownloadProgress, 0, 0, 1, 1)
            self.MCSL2_DownloadProgress.setVisible(False)
            self.CancelDownloadPushButton.clicked.connect(self.CancelDownload)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def Download(self, DownloadItemIndex):
        try:
            Watcher = DownloadWatcher(uris=[self.DownloadURLList[DownloadItemIndex]], parent=self,
                                      )
            self.DownloadingFileNameLabel.setText(
                f"正在下载：{self.downloadUrlDict[DownloadSource][self.DownloadSwitcher_TabWidget.currentIndex()]['SubWidgetNames'][DownloadItemIndex]}")
            self.MCSL2_DownloadProgress.setVisible(True)
            # reset
            self.ProgressBar.setMaximum(100)
            self.ProgressBar.setValue(0)
            self.DownloadingPercentLabel.setText("0%")
            self.DownloadingSpeedLabel.setText("速度：0KB/s")

            GraphType = self.DownloadSwitcher_TabWidget.currentIndex()
            image = self.GetDownloadSubWidgetImage(GraphType)
            self.GraphWidget_DownloadProgress.setPixmap(image)

            def downloadFinishedHandler():
                try:
                    self.ProgressBar.setValue(100)
                    self.MCSL2_DownloadProgress.setVisible(False)
                    if Watcher.StopOrCancel:
                        CallMCSL2Dialog(Tip="下载失败或被取消", OtherTextArg=None, isNeededTwoButtons=0,
                                        ButtonArg=None)
                    else:
                        CallMCSL2Dialog(Tip="下载完成", OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)
                        if system() == "Windows":
                            path = Watcher.Files[0]
                            if path.is_dir():
                                os_system(f'start {ospath.join(getcwd(), "MCSL2", "Downloads")}')
                            else:
                                os_system(f"explorer /select,{path}")
                except Exception as e:
                    print(e)

            Watcher.finished.connect(downloadFinishedHandler)
            Watcher.OnDownloadInfoGet.connect(lambda d: {
                self.DownloadingSpeedLabel.setText("速度：" + d['speed']),
                self.DownloadingPercentLabel.setText(d['progress']),
                self.ProgressBar.setValue(int(d['progress'][:-4]))
            })
            self.MCSL2_DownloadProgress.DownloadWatcher = Watcher
            Watcher.start()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def CancelDownload(self):
        try:
            self.MCSL2_DownloadProgress.setVisible(False)
            self.MCSL2_DownloadProgress.DownloadWatcher.StopWatch()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def ChooseJava(self, JavaIndex):
        try:
            global JavaPaths, JavaPath
            JavaPath = JavaPaths[JavaIndex].Path
            self.FunctionsStackedWidget.setCurrentIndex(1)
            self.Java_Version_Label.setText(JavaPaths[JavaIndex].Version)
            MCSLLogger.Log(Msg="ChoseJava", MsgArg=None, MsgLevel=0)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def ChooseServer(self, ServerIndex):
        try:
            global ServerIndexNum
            ServerIndexNum = ServerIndex
            # noinspection PyTypeChecker
            self.Selected_Server_Label.setText(
                f"服务器：{GlobalServerList[ServerIndex]['name']}")
            self.FunctionsStackedWidget.setCurrentIndex(0)
            MCSLLogger.Log(Msg="ChoseServer", MsgArg=str(self.Selected_Server_Label.text()), MsgLevel=0)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    # The function of checking update
    def CheckUpdate(self):
        try:
            global Version
            CurrentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.LastUpdateTime.setText(f"最后一次检查更新时间：{CurrentTime}")
            MCSL2Settings().ChangeConfig(Type="LastUpdateTime", Arg=CurrentTime)
            MCSLLogger.Log(Msg=
                           "CheckUpdate", MsgArg=f"当前版本{Version}", MsgLevel=0)
            LatestVersionInformation = Updater(
                Version).GetLatestVersionInformation()
            if LatestVersionInformation[0] == 1:
                MCSLLogger.Log(Msg="NewVersionAvailable", MsgArg=f"{LatestVersionInformation[1][0]}", MsgLevel=0)
                MCSLLogger.Log(Msg="UpdateContent", MsgArg=f"{LatestVersionInformation[1][1]}", MsgLevel=0)
                self.Update_Introduction_Title_Label.setText(
                    "这是最新版本 v" + LatestVersionInformation[1][0] + "的说明：")
                self.Update_Introduction_Label.setText(
                    str(LatestVersionInformation[1][1]).replace("\\n", "\n"))
                MCSLLogger.Log(Msg="ToUpdatePage", MsgArg=None, MsgLevel=0)
                self.FunctionsStackedWidget.setCurrentIndex(8)
            elif LatestVersionInformation[0] == 0:
                MCSLLogger.Log(Msg="NoNewVersionAvailable", MsgArg=f"{LatestVersionInformation[0]}", MsgLevel=0)
            else:
                MCSLLogger.Log(Msg="CheckUpdateFailed", MsgArg=None, MsgLevel=0)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def GetNotice(self):
        try:

            MCSLLogger.Log(Msg="GetNotice", MsgArg=None, MsgLevel=0)
            self.Notice_Label.setText(
                f"——————公告——————\n{str(Updater(Version).GetNoticeText())}")
        except Exception as e:
            MCSLLogger.ExceptionLog(e)


if __name__ == '__main__':
    JavaPath = 0
    JavaPaths = []
    DiskSymbols = []
    GlobalServerList = []
    JavaPathList = []
    ServerIndexNum = 0
    SearchStatus = 0
    CorePath = ""
    DownloadSource = 0
    CanCreate = 0
    CoreFileName = ""
    ServerName = ""
    Version = "2.1.3.7"
    CurrentNavigationStyleSheet = "QPushButton\n" \
                                  "{\n" \
                                  "    padding-left: 10px;\n" \
                                  "    text-align: left;\n" \
                                  "    background-color: rgb(247, 247, 247);\n" \
                                  "    border-radius: 7px;\n" \
                                  "}\n" \
                                  "QPushButton:hover\n" \
                                  "{\n" \
                                  "    text-align: left;\n" \
                                  "    background-color: rgb(243, 243, 243);\n" \
                                  "    border-radius: 7px;\n" \
                                  "}\n" \
                                  "QPushButton:pressed\n" \
                                  "{\n" \
                                  "    text-align: left;\n" \
                                  "    background-color: rgb(233, 233, 233);\n" \
                                  "    border-radius: 7px;\n" \
                                  "}"
    OtherNavigationStyleSheet = "QPushButton\n" \
                                "{\n" \
                                "    padding-left: 10px;\n" \
                                "    text-align: left;\n" \
                                "    background-color: rgb(255, 255, 255);\n" \
                                "    border-radius: 7px;\n" \
                                "}\n" \
                                "QPushButton:hover\n" \
                                "{\n" \
                                "    text-align: left;\n" \
                                "    background-color: rgb(243, 243, 243);\n" \
                                "    border-radius: 7px;\n" \
                                "}\n" \
                                "QPushButton:pressed\n" \
                                "{\n" \
                                "    text-align: left;\n" \
                                "    background-color: rgb(233, 233, 233);\n" \
                                "    border-radius: 7px;\n" \
                                "}"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    if system().lower() == 'linux':
        if environ["XDG_SESSION_TYPE"].lower() != 'x11':
            environ["QT_QPA_PLATFORM"] = "wayland"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "auto"
    MCSLProcess = QApplication(argv)
    MCSLMainWindow = MCSL2MainWindow()
    MCSLMainWindow.show()
    exit(MCSLProcess.exec_())

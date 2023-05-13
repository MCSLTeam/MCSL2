from platform import uname
from json import dump
from os import getcwd, environ, remove, path as ospath
from subprocess import CalledProcessError
from sys import argv, exit
from datetime import datetime
from PyQt5.QtCore import QPoint, pyqtSlot
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsDropShadowEffect,
    QMainWindow,
)
from MCSL2_Libs import MCSL2_Icon as _  # noqa: F401
from MCSL2_Libs import MCSL2_JavaDetector
from MCSL2_Libs.IndeterminateProgressBar import IndeterminateProgressBar
from MCSL2_Libs.MCSL2_Dialog import CallMCSL2Dialog
from MCSL2_Libs.MCSL2_DownloadURLParser import FetchDownloadURLThreadFactory
from MCSL2_Libs.MCSL2_Init import InitMCSL
from MCSL2_Libs.MCSL2_JavaDetector import GetJavaVersion, Java
from MCSL2_Libs.MCSL2_Logger import MCSL2Logger, InitNewLogFile
from MCSL2_Libs.MCSL2_MainWindow import *  # noqa: F403
from MCSL2_Libs.MCSL2_ServerController import (
    CheckAvailableSaveServer,
    SaveServer,
    ReadGlobalServerConfig,
    ServerLauncher
)
from MCSL2_Libs.MCSL2_Settings import MCSL2Settings, OpenWebUrl
from MCSL2_Libs.MCSL2_Updater import Updater


# Initialize MainWindow
class MCSL2MainWindow(QMainWindow, Ui_MCSL2_MainWindow):
    global LogFilesCount

    def __init__(self):
        global LogFilesCount
        LogFilesCount = InitMCSL()
        InitNewLogFile(LogFilesCount)
        MCSL2Logger("InitMCSL", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
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
        MCSL2Logger("InitUI", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.TransparentPercentNum.setText(str(self.TransparentPercentSlider.value()) + "%")
        self.Home_Page_PushButton.setIcon(QIcon(":/MCSL2_Icon/Home.svg"))
        self.Config_Page_PushButton.setIcon(QIcon(":/MCSL2_Icon/Configuration.svg"))
        self.Download_Page_PushButton.setIcon(QIcon(":/MCSL2_Icon/Download.svg"))
        self.Server_Console_Page_PushButton.setIcon(QIcon(":/MCSL2_Icon/Console.svg"))
        self.Tools_Page_PushButton.setIcon(QIcon(":/MCSL2_Icon/Toolbox.svg"))
        self.About_Page_PushButton.setIcon(QIcon(":/MCSL2_Icon/About.svg"))
        self.CurrentDownloadSourceLabel.setText(
            str(self.CurrentDownloadSourceLabel.text()) + str(self.MCSLAPIDownloadSourceComboBox.currentText()))
        self._startPos = None
        self._endPos = None
        self._tracking = False
        MCSL2Settings()
        MCSL2Logger("ReadConfig", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        MCSL2Logger("InitFunctionsBind", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.GetNotice()
        # Window event binding
        self.Close_PushButton.clicked.connect(self.Quit)
        self.Minimize_PushButton.clicked.connect(self.Minimize)

        # Pages navigation binding
        self.Home_Page_PushButton.clicked.connect(self.ToHomePage)
        self.Config_Page_PushButton.clicked.connect(self.ToConfigPage)
        self.Download_Page_PushButton.clicked.connect(self.ToDownloadPage)
        self.Server_Console_Page_PushButton.clicked.connect(self.ToConsolePage)
        self.Tools_Page_PushButton.clicked.connect(self.ToToolsPage)
        self.About_Page_PushButton.clicked.connect(self.ToAboutPage)

        # Functions in home page
        self.Choose_Server_PushButton.clicked.connect(self.ToChooseServerPage)
        self.Config_PushButton.clicked.connect(self.ToConfigPage)
        self.Start_PushButton.clicked.connect(self.StartMCServerHelper)

        # Functions in config page - lead page
        self.NoobAddServer.clicked.connect(lambda: self.ConfigModeWidget.setCurrentIndex(1))
        self.ExAddServer.clicked.connect(lambda: self.ConfigModeWidget.setCurrentIndex(2))

        # Functions in config page - noob page
        self.Auto_Find_Java_PushButton.clicked.connect(self.AutoDetectJava)
        self.Download_Java_PushButton.clicked.connect(self.ToDownloadJava)
        self.Founded_Java_List_PushButton.clicked.connect(self.ToChooseJavaPage)
        self.Manual_Import_Core_PushButton.clicked.connect(self.ManuallyImportCore)
        self.Download_Core_PushButton.clicked.connect(self.ToDownloadPage)
        self.Completed_Save_PushButton.clicked.connect(self.SaveMinecraftServer)

        # Functions in config page - extended page
        self.ExAuto_Find_Java_PushButton.clicked.connect(self.AutoDetectJava)
        self.ExDownload_Java_PushButton.clicked.connect(self.ToDownloadJava)
        self.ExFounded_Java_List_PushButton.clicked.connect(self.ToChooseJavaPage)
        self.ExManual_Import_Core_PushButton.clicked.connect(self.ManuallyImportCore)
        self.ExDownload_Core_PushButton.clicked.connect(self.ToDownloadPage)
        # self.ExMemoryUnitComboBox.currentIndexChanged.connect()
        # self.ExConsoleOutputEncodingComboBox.currentIndexChanged.connect()
        # self.ExConsoleInputDecodingComboBox.currentIndexChanged.connect()
        self.ExCompleted_Save_PushButton.clicked.connect(self.SaveMinecraftServer)

        # Functions in download page
        self.DownloadSwitcher_TabWidget.currentChanged.connect(self.RefreshDownloadType)
        self.GoToDownloadSourceChangerPushButton.clicked.connect(self.ToAboutPage)
        # self.More_Download_PushButton.clicked.connect()

        # Functions in console page
        # self.Send_Command_PushButton.clicked.connect()

        # Functions in choose java page
        self.Choose_Java_Back_PushButton.clicked.connect(self.ShowFoundedJavaList_Back)

        # Functions in update page
        self.DoNotUpdate_PushButton.clicked.connect(self.ToAboutPage)
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

        # Functions in settings page
        self.AutoRunLastServerSetting.clicked.connect(lambda: self.CheckBoxSettingsChanger("AutoRunLastServer"))
        self.AcceptAllMojangEULASetting.clicked.connect(lambda: self.CheckBoxSettingsChanger("AcceptAllMojangEula"))
        self.StopServerSettings.clicked.connect(lambda: self.CheckBoxSettingsChanger("SendStopInsteadOfKill"))
        self.OnlySaveGlobalServerConfigs.clicked.connect(
            lambda: self.CheckBoxSettingsChanger("OnlySaveGlobalServerConfig"))

        self.HowToAddServerComboBox.currentIndexChanged.connect(
            lambda: self.ComboBoxSettingChanger("AddServerMode", self.HowToAddServerComboBox.currentIndex()))
        self.MCSLAPIDownloadSourceComboBox.currentIndexChanged.connect(
            lambda: self.ComboBoxSettingChanger("MCSLAPIDownloadSource",
                                                self.MCSLAPIDownloadSourceComboBox.currentIndex()))
        self.Aria2ThreadCountComboBox.currentIndexChanged.connect(
            lambda: self.ComboBoxSettingChanger("Aria2Thread", self.Aria2ThreadCountComboBox.currentIndex()))

        self.AlwaysAskDownloadPath.clicked.connect(lambda: self.CheckBoxSettingsChanger("AlwaysAskSaveDirectory"))

        self.SameFileExceptionAsk.clicked.connect(lambda: self.SameFileExceptionChanger("ask"))
        self.SameFileExceptionReWrite.clicked.connect(lambda: self.SameFileExceptionChanger("rewrite"))
        self.SameFileExceptionStop.clicked.connect(lambda: self.SameFileExceptionChanger("stop"))

        self.EnableQuickMenu.clicked.connect(lambda: self.CheckBoxSettingsChanger("EnableConsoleQuickMenu"))

        self.ConsoleOutputEncodingComboBox.currentIndexChanged.connect(
            lambda: self.ComboBoxSettingChanger("ConsoleOutputEncoding",
                                                self.ConsoleOutputEncodingComboBox.currentIndex()))
        self.ConsoleInputDecodingComboBox.currentIndexChanged.connect(
            lambda: self.ComboBoxSettingChanger("ConsoleInputDecoding",
                                                self.ConsoleInputDecodingComboBox.currentIndex()))
        self.TransparentPercentSlider.valueChanged.connect(self.TransparentPercentChanger)

        self.ExchangeButton.clicked.connect(lambda: self.CheckBoxSettingsChanger("ExchangeWindowControllingButtons"))
        self.DarkModeComboBox.currentIndexChanged.connect(
            lambda: self.ComboBoxSettingChanger("ThemeMode", self.DarkModeComboBox.currentIndex()))
        self.StartOnStartup.clicked.connect(lambda: self.CheckBoxSettingsChanger("StartOnStartup"))
        self.AlwaysRunAsAdministrator.clicked.connect(lambda: self.CheckBoxSettingsChanger("AlwaysRunAsAdministrator"))
        self.UpdatePushButton.clicked.connect(self.CheckUpdate)
        self.OpenSourceCodePushButton.clicked.connect(lambda: OpenWebUrl("https://www.github.com/MCSL2", LogFilesCount=LogFilesCount))
        self.JoinQQGroup.clicked.connect(lambda: OpenWebUrl("https://jq.qq.com/?_wv=1027&k=x2ISlviQ", LogFilesCount=LogFilesCount))
        # self.SystemReportPushButton.clicked.connect()
        MCSL2Logger("FinishStarting", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()

    def CheckBoxSettingsChanger(self, Type):
        global LogFilesCount
        if self.sender().isChecked():
            MCSL2Logger("ChangeConfig", MsgArg=f"{Type}设置为True", MsgLevel=0, LogFilesCount=LogFilesCount).Log()
            MCSL2Settings().ChangeConfig(Type=Type, Arg=True)
        else:
            MCSL2Logger("ChangeConfig", MsgArg=f"{Type}设置为False", MsgLevel=0, LogFilesCount=LogFilesCount).Log()
            MCSL2Settings().ChangeConfig(Type=Type, Arg=False)

    def ComboBoxSettingChanger(self, Type, Count):
        global LogFilesCount
        ComboBoxAttr: list
        if Type == "AddServerMode":
            ComboBoxAttr = ["Default", "Noob", "Extended"]
        elif Type == "MCSLAPIDownloadSource":
            ComboBoxAttr = ["SharePoint", "Gitee", "luoxisCloud", "GHProxy", "GitHub"]
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
        # noinspection PyUnboundLocalVariable
        MCSL2Logger("ChangeConfig",
                    MsgArg=f"{Type}设置为{ComboBoxAttr[Count]}",
                    MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        MCSL2Settings().ChangeConfig(Type=Type, Arg=ComboBoxAttr[Count])

    def SameFileExceptionChanger(self, Arg):
        global LogFilesCount
        MCSL2Logger("ChangeConfig",
                    MsgArg=f"SaveSameFileException设置为{Arg}",
                    MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        MCSL2Settings().ChangeConfig(Type="SaveSameFileException", Arg=Arg)

    def InitSettingUI(self):
        self.AutoRunLastServerSetting.setChecked(MCSL2Settings().AutoRunLastServer)
        self.AcceptAllMojangEULASetting.setChecked(MCSL2Settings().AcceptAllMojangEula)
        self.StopServerSettings.setChecked(MCSL2Settings().SendStopInsteadOfKill)
        HowToAddServerComboBoxAttr = ["Default", "Noob", "Extended"]
        self.HowToAddServerComboBox.setCurrentIndex(HowToAddServerComboBoxAttr.index(MCSL2Settings().AddServerMode))
        self.OnlySaveGlobalServerConfigs.setChecked(MCSL2Settings().OnlySaveGlobalServerConfig)
        MCSLAPIDownloadSourceAttr = ["SharePoint", "Gitee", "luoxisCloud", "GHProxy", "GitHub"]
        self.MCSLAPIDownloadSourceComboBox.setCurrentIndex(
            MCSLAPIDownloadSourceAttr.index(MCSL2Settings().MCSLAPIDownloadSource))
        Aria2ThreadAttr = [1, 2, 4, 8, 16]
        self.Aria2ThreadCountComboBox.setCurrentIndex(Aria2ThreadAttr.index(MCSL2Settings().Aria2Thread))
        self.AlwaysAskDownloadPath.setChecked(MCSL2Settings().AlwaysAskSaveDirectory)
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
        self.TransparentPercentSlider.setValue(MCSL2Settings().BackgroundTransparency)
        self.ExchangeButton.setChecked(MCSL2Settings().ExchangeWindowControllingButtons)
        ThemeModeAttr = ["light", "dark", "system"]
        self.DarkModeComboBox.setCurrentIndex(ThemeModeAttr.index(MCSL2Settings().ThemeMode))
        self.StartOnStartup.setChecked(MCSL2Settings().StartOnStartup)
        self.AlwaysRunAsAdministrator.setChecked(MCSL2Settings().AlwaysRunAsAdministrator)

    def TransparentPercentChanger(self):
        global LogFilesCount
        self.Background_2.setStyleSheet("QLabel\n"
                                        "{\n"
                                        f"    background-color: rgba(255, 255, 255, {self.TransparentPercentSlider.value()}%); "
                                        "\n    border-radius: 10px\n"
                                        "}")
        self.TransparentPercentNum.setText(str(self.TransparentPercentSlider.value()) + "%")

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def Quit(self):
        global LogFilesCount
        MCSL2Logger("Close_ButtonPressed", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
        MCSL2Logger("MCSLExit", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        MCSLProcess.quit()

    def Minimize(self):
        global LogFilesCount
        MCSL2Logger("Minimize_PushButtonPressed", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
        MCSL2Logger("WindowMinimize", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        MCSLMainWindow.showMinimized()

    # Pages Navigation
    def ToHomePage(self):
        global LogFilesCount
        MCSL2Logger("ToHomePage", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.FunctionsStackedWidget.setCurrentIndex(0)
        MCSL2Logger("RefreshBlue", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.Blue1.setStyleSheet(BlueStyleSheet)
        self.Home_Page_PushButton.setStyleSheet(CurrentNavigationStyleSheet)
        self.Config_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Download_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Server_Console_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Tools_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.About_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Blue1.setVisible(True)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToConfigPage(self):
        global LogFilesCount
        MCSL2Logger("ToConfigPage", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.FunctionsStackedWidget.setCurrentIndex(1)
        MCSL2Logger("RefreshBlue", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.Blue2.setStyleSheet(BlueStyleSheet)
        self.Home_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Config_Page_PushButton.setStyleSheet(CurrentNavigationStyleSheet)
        self.Download_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Server_Console_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Tools_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.About_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(True)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToDownloadPage(self):
        global LogFilesCount
        self.downloadUrlDict.clear()
        MCSL2Logger("ToDownloadPage", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.FunctionsStackedWidget.setCurrentIndex(2)
        MCSL2Logger("RefreshBlue", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.Blue3.setStyleSheet(BlueStyleSheet)
        self.Home_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Config_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Download_Page_PushButton.setStyleSheet(CurrentNavigationStyleSheet)
        self.Server_Console_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Tools_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.About_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(True)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)
        self.RefreshDownloadType()

    def ToConsolePage(self):
        global LogFilesCount
        MCSL2Logger("ToConsolePage", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.FunctionsStackedWidget.setCurrentIndex(3)
        MCSL2Logger("RefreshBlue", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.Blue4.setStyleSheet(BlueStyleSheet)
        self.Home_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Config_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Download_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Server_Console_Page_PushButton.setStyleSheet(CurrentNavigationStyleSheet)
        self.Tools_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.About_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(True)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToToolsPage(self):
        global LogFilesCount
        MCSL2Logger("ToToolsPage", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.FunctionsStackedWidget.setCurrentIndex(4)
        MCSL2Logger("RefreshBlue", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.Blue5.setStyleSheet(BlueStyleSheet)
        self.Home_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Config_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Download_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Server_Console_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Tools_Page_PushButton.setStyleSheet(CurrentNavigationStyleSheet)
        self.About_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(True)
        self.Blue6.setVisible(False)

    def ToAboutPage(self):
        global LogFilesCount
        self.InitSettingUI()
        ShowLastUpdateTime = MCSL2Settings().GetConfig(Type="LastUpdateTime")
        self.LastUpdateTime.setText(f"最后一次检查更新时间：{ShowLastUpdateTime}")
        MCSL2Logger("ToSettingsPage", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.FunctionsStackedWidget.setCurrentIndex(5)
        MCSL2Logger("RefreshBlue", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.Blue6.setStyleSheet(BlueStyleSheet)
        self.Home_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Config_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Download_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Server_Console_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.Tools_Page_PushButton.setStyleSheet(OtherNavigationStyleSheet)
        self.About_Page_PushButton.setStyleSheet(CurrentNavigationStyleSheet)
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(True)
        MCSL2Logger("ChangeCurrentVersionLabel", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.CurrentVersionLabel.setText(f"当前版本：{Version}")

    def ToChooseServerPage(self):
        global GlobalServerList
        global LogFilesCount
        MCSL2Logger("Choose_Server_PushButtonPressed", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        MCSL2Logger("TryToGetGlobalServerList", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        GlobalConfig = ReadGlobalServerConfig()
        ServerCount = GlobalConfig[0]
        GlobalServerList = GlobalConfig[1]
        if str(GlobalServerList) == "[]":
            MCSL2Logger("NoServerCanBeFound", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
            MCSL2Logger("ShowDialog", MsgArg="AskMode", MsgLevel=0, LogFilesCount=LogFilesCount).Log()
            ReturnNum = CallMCSL2Dialog(
                Tip="ServerControllerNoServerCanBeFound",
                OtherTextArg=None,
                isNeededTwoButtons=1, ButtonArg="添加|取消")
            if ReturnNum == 1:
                self.ToConfigPage()
                QApplication.processEvents()
            else:
                pass
        else:
            self.FunctionsStackedWidget.setCurrentIndex(6)
            MCSL2Logger("TryRefreshDownloadType", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
            self.InitSelectServerSubWidget(ServerCount, GlobalServerList)

    def StartMCServerHelper(self):
        global GlobalServerList, ServerIndexNum
        global LogFilesCount
        MCSL2Logger("Start_PushButtonPressed", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        MCSL2Logger("TryToGetGlobalServerList", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        GlobalServerList = ReadGlobalServerConfig()[1]
        if str(GlobalServerList) == "[]":
            MCSL2Logger("NoServerCanBeFound", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
            MCSL2Logger("ShowDialog", MsgArg="AskMode", MsgLevel=0, LogFilesCount=LogFilesCount).Log()
            ReturnNum = CallMCSL2Dialog(
                Tip="ServerControllerNoServerCanBeFound",
                OtherTextArg=None,
                isNeededTwoButtons=1, ButtonArg="添加|取消")
            if ReturnNum == 1:
                self.ToConfigPage()
                QApplication.processEvents()
            else:
                pass
        else:
            MCSL2Logger("TryToGetServerConfig", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
            ServerLauncher().GetGlobalServerConfig(ServerIndexNum=ServerIndexNum)
            self.ToConsolePage()

    def ToChooseJavaPage(self):
        global JavaPaths
        global LogFilesCount
        MCSL2Logger("ToChooseJavaPage", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.FunctionsStackedWidget.setCurrentIndex(7)
        self.InitSelectJavaSubWidget()
        MCSL2Logger("StartInitSelectJavaSubWidget", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()

    # Download Sources Changer

    def DownloadSourceChanger(self):
        global DownloadSource
        global LogFilesCount
        MCSL2Logger("ChangeDownloadSource", MsgArg=str(self.MCSLAPIDownloadSourceComboBox.currentText()), MsgLevel=0,
                    LogFilesCount=LogFilesCount).Log()
        DownloadSource = int(self.MCSLAPIDownloadSourceComboBox.currentIndex())
        self.CurrentDownloadSourceLabel.setText("当前下载源：" + str(self.MCSLAPIDownloadSourceComboBox.currentText()))

    def ManuallySelectJava(self):
        global LogFilesCount
        MCSL2Logger("StartManuallySelectJava", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        MCSL2Logger("ShowQFileDialog", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        JavaPathSysList = QFileDialog.getOpenFileName(
            self, "选择java.exe程序", getcwd(), "java.exe"
        )
        if JavaPathSysList[0] != "":
            v = GetJavaVersion(JavaPathSysList[0])
            if not isinstance(v, CalledProcessError):
                JavaPaths.append(Java(JavaPathSysList[0], v))
                MCSL2Logger("ChooseJavaOK", MsgArg=f"\nJava路径：{JavaPathSysList[0]}\nJava版本：{v}", MsgLevel=0,
                            LogFilesCount=LogFilesCount).Log()
            else:
                MCSL2Logger("ChooseJavaInvalid", MsgArg=None, MsgLevel=2, LogFilesCount=LogFilesCount).Log()
                CallMCSL2Dialog("ConfigPageQFileDialogInvalidJava", OtherTextArg=f"{v.output}", isNeededTwoButtons=0,
                                ButtonArg=None)
        else:
            MCSL2Logger("ChooseJavaNothing", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
            CallMCSL2Dialog("ConfigPageQFileDialogNoJava", OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)

    def ManuallyImportCore(self):
        global LogFilesCount
        global CorePath, CoreFileName
        MCSL2Logger("StartManuallySelectCore", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        MCSL2Logger("ShowQFileDialog", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        CoreSysList = QFileDialog.getOpenFileName(self, "选择服务器核心", getcwd(), "*.jar")
        if CoreSysList[0] != "":
            CorePath = CoreSysList[0]
            CoreFileName = CorePath.split("/")
            CoreFileName = CoreFileName[-1]
            MCSL2Logger("ChooseCoreOK", MsgArg=CoreFileName, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        else:
            MCSL2Logger("ChooseCoreNothing", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
            CallMCSL2Dialog("ConfigPageQFileDialogNoCore", OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)

    def SaveMinecraftServer(self):
        global LogFilesCount
        global JavaPath, MaxMemory, MinMemory, CoreFileName, CanCreate
        """
        0 -> Illegal
        1 -> OK
        """
        MCSL2Logger("StartSaveMinecraftServer", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
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
            MCSL2Logger(Log, MsgArg=None, MsgLevel=2, LogFilesCount=LogFilesCount).Log()
            MCSL2Logger("AddServerFailed", MsgArg=None, MsgLevel=2, LogFilesCount=LogFilesCount).Log()
            CallMCSL2Dialog(Tip, OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)
        elif CanCreate == 1:
            MCSL2Logger(Log, MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
            CallMCSL2Dialog(Tip, OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)
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
            MCSL2Logger("AddServerSuccess", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        else:
            MCSL2Logger("AddServerUnexpectedFailed", MsgArg=None, MsgLevel=3, LogFilesCount=LogFilesCount).Log()
            CallMCSL2Dialog("ConfigPageAddServerUnexpectedFailed", OtherTextArg=None, isNeededTwoButtons=0,
                            ButtonArg=None)

    def AutoDetectJava(self):
        global LogFilesCount
        # 防止同时多次运行worker线程
        MCSL2Logger("StartAutoDetectJava", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.Auto_Find_Java_PushButton.setDisabled(True)
        self.JavaFindWorkThreadFactory.Create().start()

    @pyqtSlot(list)
    def JavaDetectFinished(self, _JavaPaths: list):
        global JavaPaths
        global LogFilesCount
        global JavaPathList
        # 向前兼容
        if ospath.exists("MCSL2/AutoDetectJavaHistory.txt"):
            remove("MCSL2/AutoDetectJavaHistory.txt")
        with open("MCSL2/AutoDetectJavaHistory.json", 'w+', encoding='utf-8') as SaveFoundedJava:
            JavaPaths = list({p[:-1] for p in SaveFoundedJava.readlines()}.union(set(JavaPaths)).union(set(_JavaPaths)))
            JavaPaths.sort(key=lambda x: x.Version, reverse=False)
            JavaPathList = [{"Path": e.Path, "Version": e.Version} for e in JavaPaths]
            # 获取新发现的Java路径,或者用户选择的Java路径
            dump({"java": JavaPathList}, SaveFoundedJava, sort_keys=True, indent=4, ensure_ascii=False)

    @pyqtSlot(int)
    def OnJavaFindWorkThreadFinished(self, sequenceNumber):
        global LogFilesCount
        # 如果不是第一次运行worker线程
        if sequenceNumber > 1:
            MCSL2Logger("FinishedAutoDetectJava", MsgArg=f"{JavaPathList}\n共搜索到{len(JavaPaths)}个Java", MsgLevel=0,
                        LogFilesCount=LogFilesCount).Log()
            CallMCSL2Dialog("ConfigPageAutoDetectJavaFinished", OtherTextArg=str(len(JavaPaths)), isNeededTwoButtons=0,
                            ButtonArg=None)

        # 释放AutoDetectJava中禁用的按钮
        self.Auto_Find_Java_PushButton.setEnabled(True)
        # 更新self.ChooseJavaScrollAreaVerticalLayout中的内容

    def ShowFoundedJavaList_Back(self):
        global LogFilesCount
        MCSL2Logger("ManuallySkipChooseGotJava", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.FunctionsStackedWidget.setCurrentIndex(1)
        self.Blue2.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 5px\n"
            "}"
        )
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(True)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToDownloadJava(self):
        global LogFilesCount
        MCSL2Logger("ManuallySkipChooseGotJava", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.FunctionsStackedWidget.setCurrentIndex(2)
        MCSL2Logger("SelectJavaDownload", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.DownloadSwitcher_TabWidget.setCurrentIndex(0)
        self.Blue3.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 5px\n"
            "}"
        )
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(True)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)
        self.RefreshDownloadType()

    # The function of refreshing download type.

    def RefreshDownloadType(self):
        global DownloadSource, DownloadUrls
        global LogFilesCount
        MCSL2Logger("TryRefreshDownloadType", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
        # 如果存在DownloadSource且不为空,则不再重新获取
        if self.downloadUrlDict.get(DownloadSource) is not None:
            MCSL2Logger("NoNeedToRefreshDownloadType", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
            idx = self.DownloadSwitcher_TabWidget.currentIndex()
            MCSL2Logger("StartInitDownloadSubWidget", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
            self.InitDownloadSubWidget(self.downloadUrlDict[DownloadSource][idx]['SubWidgetNames'])
            # self.downloadUrlDict[DownloadSource][idx]['DownloadUrls']
        else:
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
                self.JavaVerticalLayout.addWidget(IndeterminateProgressBar(self))
            elif idx == 1:
                self.SpigotVerticalLayout.addWidget(self.RefreshingTip)
                self.SpigotVerticalLayout.addWidget(IndeterminateProgressBar(self))
            elif idx == 2:
                self.PaperVerticalLayout.addWidget(self.RefreshingTip)
                self.PaperVerticalLayout.addWidget(IndeterminateProgressBar(self))
            elif idx == 3:
                self.BCVerticalLayout.addWidget(self.RefreshingTip)
                self.BCVerticalLayout.addWidget(IndeterminateProgressBar(self))
            elif idx == 4:
                self.OfficialCoreVerticalLayout.addWidget(self.RefreshingTip)
                self.OfficialCoreVerticalLayout.addWidget(IndeterminateProgressBar(self))
            else:
                pass
            MCSL2Logger("StartRefreshDownloadType", MsgArg=None, MsgLevel=1, LogFilesCount=LogFilesCount).Log()
            workThread = self.fetchDownloadURLThreadFactory.create(
                downloadSrc=DownloadSource,
                _singleton=True,
                finishSlot=self.updateDownloadUrlDict
            )
            if workThread.isRunning():
                return
            else:
                workThread.start()

    @pyqtSlot(dict)
    def updateDownloadUrlDict(self, _downloadUrlDict: dict):
        global LogFilesCount
        self.downloadUrlDict.update(_downloadUrlDict)
        self.RefreshDownloadType()

    def InitDownloadSubWidget(self, SubWidgetNames):
        global LogFilesCount
        GraphType = self.DownloadSwitcher_TabWidget.currentIndex()
        if GraphType == 0:
            self.initDownloadLayout(self.JavaVerticalLayout, SubWidgetNames, QPixmap(":/MCSL2_Icon/JavaIcon.png"))
        elif GraphType == 1:
            self.initDownloadLayout(self.SpigotVerticalLayout, SubWidgetNames, QPixmap(":/MCSL2_Icon/SpigotIcon.png"))
        elif GraphType == 2:
            self.initDownloadLayout(self.PaperVerticalLayout, SubWidgetNames, QPixmap(":/MCSL2_Icon/PaperIcon.png"))
        elif GraphType == 3:
            self.initDownloadLayout(self.BCVerticalLayout, SubWidgetNames, QPixmap(":/MCSL2_Icon/BungeeCordIcon.png"))
        elif GraphType == 4:
            self.initDownloadLayout(self.OfficialCoreVerticalLayout, SubWidgetNames,
                                    QPixmap(":/MCSL2_Icon/OfficialCoreIcon.png"))
        else:
            pass

    def initDownloadSubWidget(self, i):
        global LogFilesCount
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

    def initDownloadLayout(self, layout, subWidgetNames, pixMap):
        global LogFilesCount
        if subWidgetNames == -2:
            Tip = "DownloadPageConnectToMCSLAPIFailed"
            CallMCSL2Dialog(Tip, OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)
            return
        elif subWidgetNames == -1:
            Tip = "DownloadPageEncodeMCSLAPIContentFailed"
            CallMCSL2Dialog(Tip, OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)
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

    def InitSelectJavaSubWidget(self):
        global JavaPaths
        global LogFilesCount
        MCSL2Logger("StartInitSelectJavaSubWidget", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        for i in reversed(range(self.ChooseJavaScrollAreaVerticalLayout.count())):
            self.ChooseJavaScrollAreaVerticalLayout.itemAt(i).widget().setParent(None)

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
            self.IntroductionLabel_S.setText("Java版本：" + JavaPaths[i].Version + "\n" + JavaPaths[i].Path)
            self.Select_PushButton.setText("选择")
            self.Select_PushButton.clicked.connect(lambda: self.ParseSrollAreaItemButtons())

            self.ChooseJavaScrollAreaVerticalLayout.addWidget(self.MCSL2_SubWidget_Select)

    def InitSelectServerSubWidget(self, ServerCount, ServerInfoJSON):
        global LogFilesCount
        for i in reversed(range(self.ChooseServerScrollAreaVerticalLayout.count())):
            self.ChooseServerScrollAreaVerticalLayout.itemAt(i).widget().setParent(None)

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
            ServerInfo = WidgetServerName + WidgetCoreFileName + WidgetJavaPath + WidgetMinMemory + WidgetMaxMemory + WidgetJavaArg
            MCSL2Logger("GotServerInfo", MsgArg=f" - 第{i}个：\nServerInfo", MsgLevel=0,
                        LogFilesCount=LogFilesCount).Log()
            self.MCSL2_SubWidget_SelectS = QWidget()
            self.MCSL2_SubWidget_SelectS.setGeometry(QRect(150, 270, 620, 171))
            self.MCSL2_SubWidget_SelectS.setMinimumSize(QSize(620, 171))
            self.MCSL2_SubWidget_SelectS.setMaximumSize(QSize(620, 171))
            self.MCSL2_SubWidget_SelectS.setStyleSheet("QWidget\n"
                                                       "{\n"
                                                       "    border-radius: 4px;\n"
                                                       "    background-color: rgba(247, 247, 247, 247)\n"
                                                       "}")
            self.MCSL2_SubWidget_SelectS.setObjectName("MCSL2_SubWidget_SelectS")
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
            self.SelectS_PushButton.setObjectName("SelectS_PushButton" + str(i))
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
            self.SelectS_PushButton.clicked.connect(lambda: self.ParseSrollAreaItemButtons())
            self.ChooseServerScrollAreaVerticalLayout.addWidget(self.MCSL2_SubWidget_SelectS)

    def ParseSrollAreaItemButtons(self):
        global LogFilesCount
        MCSL2Logger("RunParseSrollAreaItemButtons", MsgArg=str(self.FunctionsStackedWidget.currentIndex()), MsgLevel=0,
                    LogFilesCount=LogFilesCount).Log()
        SelectDownloadItemIndexNumber = int(str(self.sender().objectName()).split("_PushButton")[1])
        MCSL2Logger("SrollAreaItemButtonNum", MsgArg=str(SelectDownloadItemIndexNumber), MsgLevel=0,
                    LogFilesCount=LogFilesCount).Log()
        if self.FunctionsStackedWidget.currentIndex() == 7:
            self.ChooseJava(JavaIndex=SelectDownloadItemIndexNumber)
        if self.FunctionsStackedWidget.currentIndex() == 6:
            self.ChooseServer(ServerIndex=SelectDownloadItemIndexNumber)

    def ChooseJava(self, JavaIndex):
        global JavaPaths, JavaPath
        global LogFilesCount
        JavaPath = JavaPaths[JavaIndex].Path
        self.FunctionsStackedWidget.setCurrentIndex(1)
        self.Java_Version_Label.setText(JavaPaths[JavaIndex].Version)
        MCSL2Logger("ChoseJava", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()

    def ChooseServer(self, ServerIndex):
        global ServerIndexNum
        global LogFilesCount
        ServerIndexNum = ServerIndex
        # noinspection PyTypeChecker
        self.Selected_Server_Label.setText(f"服务器：{GlobalServerList[ServerIndex]['name']}")
        self.FunctionsStackedWidget.setCurrentIndex(0)
        MCSL2Logger("ChoseServer", MsgArg=str(self.Selected_Server_Label.text()), MsgLevel=0,
                    LogFilesCount=LogFilesCount).Log()

    # The function of checking update
    def CheckUpdate(self):
        global LogFilesCount
        global Version
        CurrentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.LastUpdateTime.setText(f"最后一次检查更新时间：{CurrentTime}")
        MCSL2Settings().ChangeConfig(Type="LastUpdateTime", Arg=CurrentTime)
        MCSL2Logger("CheckUpdate", MsgArg=f"当前版本{Version}", MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        LatestVersionInformation = Updater(Version).GetLatestVersionInformation()
        if LatestVersionInformation[0] == 1:
            LatestVersionInformation = str(LatestVersionInformation[1]).replace("(", "").replace(")", "").replace(" ",
                                                                                                                  "").replace(
                "\'", "").split(",")
            MCSL2Logger("NewVersionAvailable", MsgArg=f"{LatestVersionInformation[0]}", MsgLevel=0,
                        LogFilesCount=LogFilesCount).Log()
            MCSL2Logger("UpdateContent", MsgArg=f"{LatestVersionInformation[1]}", MsgLevel=0,
                        LogFilesCount=LogFilesCount).Log()
            self.Update_Introduction_Title_Label.setText("这是最新版本 v" + LatestVersionInformation[0] + "的说明：")
            self.Update_Introduction_Label.setText(str(LatestVersionInformation[1]).replace("\\n", "\n"))
            MCSL2Logger("ToUpdatePage", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
            self.FunctionsStackedWidget.setCurrentIndex(8)
        elif LatestVersionInformation[0] == 0:
            LatestVersionInformation = str(LatestVersionInformation[1]).replace("(", "").replace(")", "").replace(" ",
                                                                                                                  "").replace(
                "\'", "").split(",")
            MCSL2Logger("NoNewVersionAvailable", MsgArg=f"{LatestVersionInformation[0]}", MsgLevel=0,
                        LogFilesCount=LogFilesCount).Log()
        else:
            MCSL2Logger("CheckUpdateFailed", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()

    def GetNotice(self):
        global LogFilesCount
        MCSL2Logger("GetNotice", MsgArg=None, MsgLevel=0, LogFilesCount=LogFilesCount).Log()
        self.Notice_Label.setText(f"——————公告——————\n{str(Updater(Version).GetNoticeText())}")



if __name__ == '__main__':
    JavaPath = 0
    LogFilesCount = 0
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
    Version = "2.1.3"
    CurrentNavigationStyleSheet = "QPushButton\n" \
                                  "{\n" \
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
    BlueStyleSheet = "QLabel\n" \
                     "{\n" \
                     "    background-color: rgb(0, 120, 212);\n" \
                     "    border-radius: 5px\n" \
                     "}"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    SysType = uname()[0]
    if SysType == "Linux":
        environ["QT_QPA_PLATFORM"] = "wayland"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "auto"
    MCSLProcess = QApplication(argv)
    MCSLMainWindow = MCSL2MainWindow()
    MCSLMainWindow.show()
    exit(MCSLProcess.exec_())

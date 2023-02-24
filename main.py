from PyQt5.QtCore import (
    Qt,
    QPoint,
    QThread,
    pyqtSignal,
    QRect,
    QCoreApplication,
    QMetaObject
)
from PyQt5.QtGui import QMouseEvent, QFont, QPixmap, QCursor, QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QMainWindow,
    QGraphicsDropShadowEffect,
    QFileDialog,
    QListView,
    QApplication,
    QLineEdit,
    QComboBox,
    QStackedWidget,
    QLabel,
    QDialog, QRadioButton, QTabWidget, QScrollArea, QFrame, QAbstractScrollArea
)
from json import loads, dumps
from requests import get
from shutil import copy
from sys import exit, argv
from os import getcwd, mkdir, remove, walk
from os import path as ospath
from time import sleep
from threading import Thread
from string import ascii_uppercase
import MCSL2_Icon
import MCSL2_DownloaderAPIParser
import MCSL2_Downloader
from MCSL2_MainWindow import *
from MCSL2_Dialog import *
from MCSL2_AskDialog import *
from MCSL2_SubWidget_ScrollArea_Download import *
from MCSL2_SubWidget_ScrollArea_Select import *
import subprocess


# Initialize MainWindow
class MCSL2MainWindow(QMainWindow, Ui_MCSL2_MainWindow):
    def __init__(self):
        super(MCSL2MainWindow, self).__init__()

        self.setupUi(self)
        self._startPos = None
        self._endPos = None
        self._tracking = False
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)

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
        self.Config_PushButton.clicked.connect(self.ToConfigPage)
        self.Choose_Server_PushButton.clicked.connect(self.ToChooseServerPage)
        self.Completed_Choose_Server_PushButton.clicked.connect(self.ToHomePage)
        self.Download_Core_PushButton.clicked.connect(self.ToDownloadPage)
        self.Completed_Choose_Java_PushButton.clicked.connect(self.ShowFoundedJavaList_Back)
        self.Founded_Java_List_PushButton.clicked.connect(self.ToChooseJavaPage)

        # Functions binding
        self.DownloadSwitcher_TabWidget.currentChanged.connect(self.RefreshDownloadType)
        self.Start_PushButton.clicked.connect(self.LaunchMinecraftServer)
        self.Manual_Select_Java_PushButton.clicked.connect(self.ManuallySelectJava)
        self.Manual_Import_Core_PushButton.clicked.connect(self.ManuallyImportCore)
        self.Download_Java_PushButton.clicked.connect(self.ToDownloadJava)
        self.Check_Update_PushButton.clicked.connect(self.CheckUpdate)
        # self.Download_PushButton.clicked.connect(self.StartDownload)
        # self.Download_Type_ComboBox.currentIndexChanged.connect(self.RefreshDownloadType)
        # self.Manually_Choose_Download_Save_Path_PushButton.clicked.connect(self.SetDownloadSavePath)
        self.Auto_Find_Java_PushButton.clicked.connect(self.AutoDetectJava)
        self.Completed_Save_PushButton.clicked.connect(self.SaveAMinecraftServer)

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
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
        MCSLProcess.quit()

    def Minimize(self):
        MCSLMainWindow.showMinimized()

        # Pages Navigation

    def ToHomePage(self):
        self.FunctionsStackedWidget.setCurrentIndex(0)
        self.Blue1.setStyleSheet("QLabel\n"
                                 "{\n"
                                 "    background-color: rgb(0, 120, 212);\n"
                                 "    border-radius: 5px\n"
                                 "}")
        self.Blue1.setVisible(True)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToConfigPage(self):
        self.FunctionsStackedWidget.setCurrentIndex(1)
        self.Blue2.setStyleSheet("QLabel\n"
                                 "{\n"
                                 "    background-color: rgb(0, 120, 212);\n"
                                 "    border-radius: 5px\n"
                                 "}")
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(True)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToDownloadPage(self):
        self.FunctionsStackedWidget.setCurrentIndex(2)
        self.Blue3.setStyleSheet("QLabel\n"
                                 "{\n"
                                 "    background-color: rgb(0, 120, 212);\n"
                                 "    border-radius: 5px\n"
                                 "}")
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(True)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToConsolePage(self):
        self.FunctionsStackedWidget.setCurrentIndex(3)
        self.Blue4.setStyleSheet("QLabel\n"
                                 "{\n"
                                 "    background-color: rgb(0, 120, 212);\n"
                                 "    border-radius: 5px\n"
                                 "}")
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(True)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToToolsPage(self):
        self.FunctionsStackedWidget.setCurrentIndex(4)
        self.Blue5.setStyleSheet("QLabel\n"
                                 "{\n"
                                 "    background-color: rgb(0, 120, 212);\n"
                                 "    border-radius: 5px\n"
                                 "}")
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(True)
        self.Blue6.setVisible(False)

    def ToAboutPage(self):
        self.FunctionsStackedWidget.setCurrentIndex(5)
        self.Blue6.setStyleSheet("QLabel\n"
                                 "{\n"
                                 "    background-color: rgb(0, 120, 212);\n"
                                 "    border-radius: 5px\n"
                                 "}")
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(True)

    def ToChooseServerPage(self):
        self.FunctionsStackedWidget.setCurrentIndex(6)

    def ToChooseJavaPage(self):
        global JavaPaths
        self.FunctionsStackedWidget.setCurrentIndex(7)
        # if len(JavaPaths) != 0:
        #     for i in range(len(JavaPaths)):
        #         self.Choose_Java_ComboBox.addItem(JavaPaths[i])

        # Download Sources Changer

    def ChoseSharePointDownloadSource(self):
        global DownloadSource
        DownloadSource = 0

    def ChoseGiteeDownloadSource(self):
        global DownloadSource
        DownloadSource = 1

    def ChoseLuoxisCloudSource(self):
        global DownloadSource
        DownloadSource = 2

    def ChoseGHProxyDownloadSource(self):
        global DownloadSource
        DownloadSource = 3

    def ChoseGitHubDownloadSource(self):
        global DownloadSource
        DownloadSource = 4

    def LaunchMinecraftServer(self):
        Tip = "cnm  没写完"
        CallMCSL2Dialog(Tip, 0)
        # Fix = '-Xms2048M -Xmx2048M -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -jar '
        # monitor = subprocess.Popen(LaunchCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # while True:
        #     result = monitor.stdout.readline()
        #     if result != b'':
        #         try:
        #             print(result.decode('gbk').strip('\r\n'))
        #         except:
        #             print(result.decode('utf-8').strip('\r\n'))
        #     else:
        #         break

    def ManuallySelectJava(self):
        JavaPathSysList = QFileDialog.getOpenFileName(self, '选择java.exe程序', getcwd(), "java.exe")
        if JavaPathSysList[0] != "":
            self.Select_Java_ComboBox.clear()
            JavaPaths.append(JavaPathSysList[0])
            for i in range(len(JavaPaths)):
                self.Select_Java_ComboBox.addItem(JavaPaths[i])
        else:
            Tip = "看来你没有选择任何的Java呢！"
            CallMCSL2Dialog(Tip, 0)

    def ManuallyImportCore(self):
        global CorePath
        CoreSysList = QFileDialog.getOpenFileName(self, '选择服务器核心', getcwd(), "*.jar")
        if CoreSysList[0] != "":
            CorePath = CoreSysList[0]
        else:
            Tip = "看来你没有选择任何的服务器核心呢！"
            CallMCSL2Dialog(Tip, 0)

    def SaveAMinecraftServer(self):
        global CorePath
        """
        0 -> Illegal
        1 -> OK
        """

        # The server core detector
        if CorePath != "":
            CoreStatus = 1
        else:
            CoreStatus = 0

        # The Java path parser
        if self.Select_Java_ComboBox.currentText() != "  请选择":
            if len(JavaPaths) != 0:
                JavaPath = JavaPaths[self.Select_Java_ComboBox.currentIndex()]
                JavaStatus = 1
            else:
                JavaStatus = 0
        else:
            JavaStatus = 0

        # The min memory parser
        if self.MinMemory_LineEdit.text() != "":
            if int(self.MinMemory_LineEdit.text()) % 1 == 0 and int(self.MinMemory_LineEdit.text()) != 0:
                MinMemory = int(self.MinMemory_LineEdit.text())
                MinMemStatus = 1
            else:
                MinMemStatus = 0
        else:
            MinMemStatus = 0

        # The max memory parser
        if self.MaxMemory_LineEdit.text() != "":
            if int(self.MaxMemory_LineEdit.text()) % 1 == 0 and int(self.MaxMemory_LineEdit.text()) != 0:
                MaxMemory = int(self.MaxMemory_LineEdit.text())
                MaxMemStatus = 1
            else:
                MaxMemStatus = 0
        else:
            MaxMemStatus = 0

        # The server name parser
        if self.Server_Name_LineEdit.text() != "":
            TMPServerName = self.Server_Name_LineEdit.text()
            IllegalCodeList = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
            for i in range(len(IllegalCodeList)):
                if not IllegalCodeList[i] in TMPServerName:
                    pass
                else:
                    NameStatus = 0
            Path1 = ".\\" + TMPServerName
            if not ospath.exists(TMPServerName):
                ServerName = TMPServerName
                NameStatus = 1
            else:
                NameStatus = 0
        else:
            NameStatus = 0

        # Pop-up determine
        # 5
        if MinMemStatus == 0 and MaxMemStatus == 0 and NameStatus == 0 and JavaStatus == 0 and CoreStatus == 0:
            CanCreate = 0
            Tip = "你什么都没设置好呢\n\n（恼"

        # 4
        elif MinMemStatus == 1 and MaxMemStatus == 0 and NameStatus == 0 and JavaStatus == 0 and CoreStatus == 0:
            CanCreate = 0
            Tip = "你只设置好了最小内存\n\n（恼"
        elif MinMemStatus == 0 and MaxMemStatus == 1 and NameStatus == 0 and JavaStatus == 0 and CoreStatus == 0:
            CanCreate = 0
            Tip = "你只设置好了最大内存\n\n（恼"
        elif MinMemStatus == 0 and MaxMemStatus == 0 and NameStatus == 1 and JavaStatus == 0 and CoreStatus == 0:
            CanCreate = 0
            Tip = "你只设置好了服务器名称\n\n（恼"
        elif MinMemStatus == 0 and MaxMemStatus == 0 and NameStatus == 0 and JavaStatus == 1 and CoreStatus == 0:
            CanCreate = 0
            Tip = "你只设置好了Java\n\n（恼"
        elif MinMemStatus == 0 and MaxMemStatus == 0 and NameStatus == 0 and JavaStatus == 0 and CoreStatus == 1:
            CanCreate = 0
            Tip = "你只设置好了Java\n\n（恼"

        # 3
        elif MinMemStatus == 1 and MaxMemStatus == 1 and NameStatus == 0 and JavaStatus == 0 and CoreStatus == 0:
            CanCreate = 0
            Tip = "你只设置好了内存\n\n（恼"
        elif MinMemStatus == 1 and MaxMemStatus == 0 and NameStatus == 1 and JavaStatus == 0 and CoreStatus == 0:
            CanCreate = 0
            Tip = "服务器核心、Java和最大内存还没设置好呢\n\n（恼"
        elif MinMemStatus == 1 and MaxMemStatus == 0 and NameStatus == 0 and JavaStatus == 1 and CoreStatus == 0:
            CanCreate = 0
            Tip = "服务器核心、服务器名称和最大内存还没设置好呢\n\n（恼"
        elif MinMemStatus == 1 and MaxMemStatus == 0 and NameStatus == 0 and JavaStatus == 0 and CoreStatus == 1:
            CanCreate = 0
            Tip = "Java、服务器名称和最大内存还没设置好呢\n\n（恼"
        elif MinMemStatus == 0 and MaxMemStatus == 1 and NameStatus == 1 and JavaStatus == 0 and CoreStatus == 0:
            CanCreate = 0
            Tip = "服务器核心、Java和最小内存还没设置好呢\n\n（恼"
        elif MinMemStatus == 0 and MaxMemStatus == 1 and NameStatus == 0 and JavaStatus == 1 and CoreStatus == 0:
            CanCreate = 0
            Tip = "服务器核心、服务器名称和最小内存还没设置好呢\n\n（恼"
        elif MinMemStatus == 0 and MaxMemStatus == 1 and NameStatus == 0 and JavaStatus == 0 and CoreStatus == 1:
            CanCreate = 0
            Tip = "Java、服务器名称和最小内存还没设置好呢\n\n（恼"
        elif MinMemStatus == 0 and MaxMemStatus == 0 and NameStatus == 1 and JavaStatus == 1 and CoreStatus == 0:
            CanCreate = 0
            Tip = "服务器核心和内存还没设置好呢\n\n（恼"
        elif MinMemStatus == 0 and MaxMemStatus == 0 and NameStatus == 1 and JavaStatus == 0 and CoreStatus == 1:
            CanCreate = 0
            Tip = "服务器核心和Java还没设置好呢\n\n（恼"
        elif MinMemStatus == 0 and MaxMemStatus == 0 and NameStatus == 0 and JavaStatus == 1 and CoreStatus == 1:
            CanCreate = 0
            Tip = "服务器名称和内存还没设置好呢\n\n（恼"

        # 2
        elif MinMemStatus == 1 and MaxMemStatus == 1 and NameStatus == 1 and JavaStatus == 0 and CoreStatus == 0:
            CanCreate = 0
            Tip = "只剩Java和服务器核心没设置好力\n\n（喜"
        elif MinMemStatus == 1 and MaxMemStatus == 1 and NameStatus == 0 and JavaStatus == 1 and CoreStatus == 0:
            CanCreate = 0
            Tip = "只剩服务器名称和服务器核心没设置好力\n\n（喜"
        elif MinMemStatus == 1 and MaxMemStatus == 1 and NameStatus == 0 and JavaStatus == 0 and CoreStatus == 1:
            CanCreate = 0
            Tip = "只剩服务器名称和Java没设置好力\n\n（喜"
        elif MinMemStatus == 1 and MaxMemStatus == 0 and NameStatus == 1 and JavaStatus == 1 and CoreStatus == 0:
            CanCreate = 0
            Tip = "只剩最大内存和服务器核心没设置好力\n\n（喜"
        elif MinMemStatus == 1 and MaxMemStatus == 0 and NameStatus == 1 and JavaStatus == 0 and CoreStatus == 1:
            CanCreate = 0
            Tip = "只剩最大内存和服务器核心没设置好力\n\n（喜"
        elif MinMemStatus == 1 and MaxMemStatus == 0 and NameStatus == 0 and JavaStatus == 1 and CoreStatus == 1:
            CanCreate = 0
            Tip = "只剩最大内存和服务器核心没设置好力\n\n（喜"
        elif MinMemStatus == 0 and MaxMemStatus == 1 and NameStatus == 1 and JavaStatus == 1 and CoreStatus == 0:
            CanCreate = 0
            Tip = "只剩服务器核心和最小内存没设置好力\n\n（喜"
        elif MinMemStatus == 0 and MaxMemStatus == 1 and NameStatus == 1 and JavaStatus == 0 and CoreStatus == 1:
            CanCreate = 0
            Tip = "只剩Java和最小内存没设置好力\n\n（喜"
        elif MinMemStatus == 0 and MaxMemStatus == 1 and NameStatus == 0 and JavaStatus == 1 and CoreStatus == 1:
            CanCreate = 0
            Tip = "只剩服务器名称和最小内存没设置好力\n\n（喜"
        elif MinMemStatus == 0 and MaxMemStatus == 0 and NameStatus == 1 and JavaStatus == 1 and CoreStatus == 1:
            CanCreate = 0
            Tip = "只剩内存没设置好力\n\n（喜"

        # 1
        elif MinMemStatus == 0 and MaxMemStatus == 1 and NameStatus == 1 and JavaStatus == 1 and CoreStatus == 1:
            CanCreate = 0
            Tip = "只剩最小内存没设置好力\n\n（喜"
        elif MinMemStatus == 1 and MaxMemStatus == 0 and NameStatus == 1 and JavaStatus == 1 and CoreStatus == 1:
            CanCreate = 0
            Tip = "只剩最大内存没设置好力\n\n（喜"
        elif MinMemStatus == 1 and MaxMemStatus == 1 and NameStatus == 0 and JavaStatus == 1 and CoreStatus == 1:
            CanCreate = 0
            Tip = "只剩服务器名称没设置好力\n\n（喜"
        elif MinMemStatus == 1 and MaxMemStatus == 1 and NameStatus == 1 and JavaStatus == 0 and CoreStatus == 1:
            CanCreate = 0
            Tip = "只剩Java没设置好力\n\n（喜"
        elif MinMemStatus == 1 and MaxMemStatus == 1 and NameStatus == 1 and JavaStatus == 1 and CoreStatus == 0:
            CanCreate = 0
            Tip = "只剩服务器核心没设置好力\n\n（喜"

        # 0
        elif MinMemStatus == 1 and MaxMemStatus == 1 and NameStatus == 1 and JavaStatus == 1 and CoreStatus == 1:
            CanCreate = 1
            Tip = "关闭此窗口后，\n\n服务器将会开始部署。"

        # Server processor
        if CanCreate == 0:
            CallMCSL2Dialog(Tip, 0)
        elif CanCreate == 1:
            CallMCSL2Dialog(Tip, 0)
            ServerFolderPath = ".\\" + ServerName
            mkdir(ServerFolderPath)
            copy(CorePath, ServerFolderPath)
            ServerConfigDict = {'name': ServerName, 'java_path': JavaPath, 'min_memory': MinMemory,
                                'max_memory': MaxMemory}
            ServerConfigJson = dumps(ServerConfigDict, ensure_ascii=False)
            ConfigPath = ".\\" + ServerName + ".\\" + "MCSL2ServerConfig.json"
            with open(ConfigPath, 'w+', encoding='utf-8') as SaveConfig:
                SaveConfig.write(ServerConfigJson)
                SaveConfig.close()
            # SaveConfig = open(ConfigPath, 'w+')
            # SaveConfig.write(ServerConfigJson)
            # SaveConfig.close()
            Tip = "服务器部署完毕！"
            CallMCSL2Dialog(Tip, 0)
        else:
            Tip = "服务器部署失败，\n\n但不是你的问题，\n\n去找开发者反馈吧！"
            CallMCSL2Dialog(Tip, 0)

    def AutoDetectJava(self):
        global SearchStatus, DiskSymbols
        for c in ascii_uppercase:
            DiskSymbol = c + ":"
            if ospath.isdir(DiskSymbol):
                DiskSymbol = c + ":\\"
                DiskSymbols.append(DiskSymbol)
        self.thread = fileSearchThread("java.exe")
        self.thread.start()
        # if len(JavaPaths) != 0:
        #     for i in range(len(JavaPaths)):
        #         self.Select_Java_ComboBox.addItem(JavaPaths[i])
        while True:
            if SearchStatus == 1:
                Tip = "搜索完毕。"
                CallMCSL2Dialog(Tip, 0)
                self.ToChooseJavaPage()
                break
            else:
                sleep(1)
                continue
        #
        # if len(JavaPaths) != 0:
        #     for i in range(len(JavaPaths)):

    def ShowFoundedJavaList_Back(self):
        self.FunctionsStackedWidget.setCurrentIndex(1)
        self.Blue2.setStyleSheet("QLabel\n"
                                 "{\n"
                                 "    background-color: rgb(0, 120, 212);\n"
                                 "    border-radius: 5px\n"
                                 "}")
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(True)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToDownloadJava(self):
        self.FunctionsStackedWidget.setCurrentIndex(2)
        self.DownloadSwitcher_TabWidget.setCurrentIndex(0)

        # The function of refreshing download type.

    def RefreshDownloadType(self):
        global DownloadSource
        MCSL2_DownloaderAPIParser.ParseDownloaderAPIUrl(DownloadSource, self.DownloadSwitcher_TabWidget.currentIndex())
        # self.InitSubWidget(Mode='0')
        self.AddWidgetToScrollArea()

        # Add SubWidget to Scroll area

    def AddWidgetToScrollArea(self):
        if self.DownloadSwitcher_TabWidget.currentIndex() == 0:
            for i in range(20):
                self.JavaScrollArea.setWidget(MCSL2SubWidget_Download)
        elif self.DownloadSwitcher_TabWidget.currentIndex() == 1:
            self.SpigotScrollArea.setWidget(MCSL2SubWidget_Download)
        elif self.DownloadSwitcher_TabWidget.currentIndex() == 2:
            self.PaperScrollArea.setWidget(MCSL2SubWidget_Download)
        elif self.DownloadSwitcher_TabWidget.currentIndex() == 3:
            self.BungeeCordScrollArea.setWidget(MCSL2SubWidget_Download)
        else:
            pass

    def InitSubWidget(self, Mode):
        if Mode == 0:  # Download
            pass
        # if Mode == 1:  # Select

        # The function of getting Minecraft server console's output
        # def GetMCConsoleOutput(self):
        #     subprocess.run(['cmd', '/c', 'dir'], stdout=subprocess.PIPE)
        #     output = result.stdout.decode('utf-8')

        # The function of checking update

    def CheckUpdate(self):
        CheckUpdateUrl = 'https://jsd.cdn.zzko.cn/gh/LxHTT/MCSL2@master/versionInfo'
        LatestVersion = float(get(CheckUpdateUrl).text)
        if float(LatestVersion) > Version:
            Tip = "检测到新版本:v" + str(LatestVersion)
            CallMCSL2Dialog(Tip, 0)
        elif float(LatestVersion) == Version:
            Tip = "已是最新版本:v" + str(LatestVersion)
            CallMCSL2Dialog(Tip, 0)
        elif float(LatestVersion) < Version:
            Tip = "开发者是不是(\n\n内部版本号: v" + str(Version) + "\n\n发布版本号: v" + str(LatestVersion)
            CallMCSL2Dialog(Tip, 0)
        else:
            pass


# Customize dialogs
class MCSL2Dialog(QDialog, Ui_MCSL2_Dialog):
    def __init__(self):
        super(MCSL2Dialog, self).__init__()
        self.setupUi(self)


class MCSL2AskDialog(QDialog, Ui_MCSL2_AskDialog):
    def __init__(self):
        super(MCSL2AskDialog, self).__init__()
        self.setupUi(self)


class MCSL2SubWidget_Download(QWidget, Ui_MCSL2_SubWidget_ScrollArea_Download):
    def __init__(self):
        super(MCSL2SubWidget_Download, self).__init__()
        self.setupUi(self)
    #
    # def SetGraph(self):
    #     while True:


class MCSL2SubWidget_Select(QWidget, Ui_MCSL2_SubWidget_ScrollArea_Select):
    def __init__(self):
        super(MCSL2SubWidget_Select, self).__init__()
        self.setupUi(self)


# The function of calling MCSL2 Dialog
def CallMCSL2Dialog(Tip, isNeededTwoButtons):
    SaveTip = open(r'Tip', 'w+')
    SaveTip.write(Tip)
    SaveTip.close()
    if isNeededTwoButtons == 0:
        MCSL2Dialog().exec()
        remove(r'Tip')
    elif isNeededTwoButtons == 1:
        MCSL2AskDialog().exec()
        remove(r'Tip')
    else:
        pass


class fileSearchThread(QThread):
    global JavaPaths
    sinOut = pyqtSignal(str)

    def __init__(self, key):
        super().__init__()
        self.key = key

    def run(self):
        global SearchStatus
        threads = []
        for each in DiskSymbols:
            t = Thread(target=self.search, args=(self.key, each,))
            threads.append(t)
            t.start()
        for i in range(len(threads)):
            threads[i].join()
        SearchStatus = 1

    def search(self, keyword, path):
        global JavaPaths
        for DirPath, DirNames, SearchFileNames in walk(path):
            for SearchFileName in SearchFileNames:
                if SearchFileName.__contains__(keyword):
                    SearchTMP_1 = ospath.join(DirPath, SearchFileName)
                    JavaPaths.append(SearchTMP_1)
                    self.sinOut.emit(ospath.join(DirPath, SearchFileName))
            for folder in DirNames:
                if folder.__contains__(keyword):
                    SearchTMP_2 = ospath.join(DirPath, folder)
                    JavaPaths.append(SearchTMP_2)
                    self.sinOut.emit(ospath.join(DirPath, folder))


# Start MCSL
JavaPaths = []
DiskSymbols = []
SearchStatus = 0
CorePath = ""
DownloadSource = 0
Version = 2.0
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
MCSLProcess = QApplication(argv)
MCSLMainWindow = MCSL2MainWindow()
MCSLMainWindow.show()
# CallMCSL2Dialog(Tip="请注意：\n\n本程序无法在125%的\n\nDPI缩放比下正常运行。")
exit(MCSLProcess.exec_())

from re import search
from subprocess import check_output, STDOUT
from json import dumps
from os import getcwd
from shutil import copy
from sys import argv, exit
from PyQt5.QtCore import QPoint, QSize, pyqtSlot
from PyQt5.QtGui import QColor, QMouseEvent, QPainter
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsDropShadowEffect,
    QMainWindow,
)

from MCSL2_Libs import MCSL2_Icon as _  # noqa: F401
from MCSL2_Libs import MCSL2_JavaDetector
from MCSL2_Libs.MCSL2_MainWindow import *  # noqa: F403
from MCSL2_Libs.MCSL2_Utils import *


# Initialize MainWindow
class MCSL2MainWindow(QMainWindow, Ui_MCSL2_MainWindow):
    def __init__(self):
        InitMCSL()
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
        self._startPos = None
        self._endPos = None
        self._tracking = False

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
        self.Choose_Java_Back_PushButton.clicked.connect(self.ShowFoundedJavaList_Back)
        self.Founded_Java_List_PushButton.clicked.connect(self.ToChooseJavaPage)
        self.DoNotUpdate_PushButton.clicked.connect(self.ToAboutPage)

        # Functions binding
        self.DownloadSwitcher_TabWidget.currentChanged.connect(self.RefreshDownloadType)
        self.Start_PushButton.clicked.connect(self.LaunchMinecraftServer)
        self.Manual_Import_Core_PushButton.clicked.connect(self.ManuallyImportCore)
        self.Download_Java_PushButton.clicked.connect(self.ToDownloadJava)
        self.Check_Update_PushButton.clicked.connect(self.CheckUpdate)
        # self.Download_PushButton.clicked.connect(self.StartDownload)
        self.Auto_Find_Java_PushButton.clicked.connect(self.AutoDetectJava)
        self.Completed_Save_PushButton.clicked.connect(self.SaveMinecraftServer)

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

    def paintEvent(self, event):
        super().paintEvent(event)
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)
        pat2.setBrush(QColor("#F0F8FF"))
        pat2.setPen(Qt.transparent)

        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width() - 9)
        rect.setHeight(rect.height() - 9)
        pat2.drawRoundedRect(rect, 4, 4)

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
        MCSLProcess.quit()

    def Minimize(self):
        MCSLMainWindow.showMinimized()

        # Pages Navigation

    def ToHomePage(self):
        self.FunctionsStackedWidget.setCurrentIndex(0)
        self.Blue1.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 5px\n"
            "}"
        )
        self.Blue1.setVisible(True)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToConfigPage(self):
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

    def ToDownloadPage(self):
        # 清空缓存
        self.downloadUrlDict.clear()
        self.FunctionsStackedWidget.setCurrentIndex(2)
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

    def ToConsolePage(self):
        self.FunctionsStackedWidget.setCurrentIndex(3)
        self.Blue4.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 5px\n"
            "}"
        )
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(True)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(False)

    def ToToolsPage(self):
        self.FunctionsStackedWidget.setCurrentIndex(4)
        self.Blue5.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 5px\n"
            "}"
        )
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(True)
        self.Blue6.setVisible(False)

    def ToAboutPage(self):
        self.FunctionsStackedWidget.setCurrentIndex(5)
        self.Blue6.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 5px\n"
            "}"
        )
        self.Blue1.setVisible(False)
        self.Blue2.setVisible(False)
        self.Blue3.setVisible(False)
        self.Blue4.setVisible(False)
        self.Blue5.setVisible(False)
        self.Blue6.setVisible(True)
        self.Check_Update_PushButton.setText("检查更新 (当前版本" + Version + ")")

    def ToChooseServerPage(self):
        self.FunctionsStackedWidget.setCurrentIndex(6)

    def ToChooseJavaPage(self):
        global JavaPaths

        self.FunctionsStackedWidget.setCurrentIndex(7)
        self.InitSelectJavaSubWidget()

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
        Fix = '-Xms2048M -Xmx2048M -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -jar '
        # LaunchCommand = "\\" + str(JavaPath) + "\\" + Fix + "./Servers/" + ServerName +
        # monitor = Popen(LaunchCommand, shell=True, stdout=PIPE, stderr=PIPE)
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
        JavaPathSysList = QFileDialog.getOpenFileName(
            self, "选择java.exe程序", getcwd(), "java.exe"
        )
        if JavaPathSysList[0] != "":
            JavaPaths.append(JavaPathSysList[0])
        else:
            Tip = "看来你没有选择任何的Java呢！"
            CallMCSL2Dialog(Tip, 0)

    def ManuallyImportCore(self):
        global CorePath, CoreFileName
        CoreSysList = QFileDialog.getOpenFileName(self, "选择服务器核心", getcwd(), "*.jar")
        if CoreSysList[0] != "":
            CorePath = CoreSysList[0]
            print(CorePath)
            CoreFileName = CorePath.split("/")[-1]
        else:
            Tip = "看来你没有选择任何的服务器核心呢！"
            CallMCSL2Dialog(Tip, 0)

    def SaveMinecraftServer(self):
        global CorePath, JavaPath, MaxMemory, MinMemory, CoreFileName
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
            if not ospath.exists(TMPServerName):
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
        if (ChkVal[0] == 1):
            if (ChkVal[1] == 1):
                if (ChkVal[2] == 1):
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 1
                            Tip = "关闭此窗口后，\n\n服务器将会开始部署。"
                        else:
                            CanCreate = 0
                            Tip = "只剩服务器核心没设置好力\n\n（喜"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩Java没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "只剩Java和服务器核心没设置好力\n\n（喜"
                else:
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩服务器名称没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "只剩服务器名称和服务器核心没设置好力\n\n（喜"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩服务器名称和Java没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "你只设置好了内存\n\n（恼"
            else:
                if (ChkVal[2] == 1):
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩最大内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "只剩最大内存和服务器核心没设置好力\n\n（喜"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩最大内存和Java没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "服务器核心、Java和最大内存还没设置好呢\n\n（恼"
                else:
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩服务器名称和最大内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "服务器核心、服务器名称和最大内存还没设置好呢\n\n（恼"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "Java、服务器名称和最大内存还没设置好呢\n\n（恼"
                        else:
                            CanCreate = 0
                            Tip = "你只设置好了最小内存\n\n（恼"
        else:
            if (ChkVal[1] == 1):
                if (ChkVal[2] == 1):
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩最小内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "只剩服务器核心和最小内存没设置好力\n\n（喜"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩Java和最小内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "服务器核心、Java和最小内存还没设置好呢\n\n（恼"
                else:
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩服务器名称和最小内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "服务器核心、服务器名称和最小内存还没设置好呢\n\n（恼"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "Java、服务器名称和最小内存还没设置好呢\n\n（恼"
                        else:
                            CanCreate = 0
                            Tip = "你只设置好了最大内存\n\n（恼"
            else:
                if (ChkVal[2] == 1):
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "只剩内存没设置好力\n\n（喜"
                        else:
                            CanCreate = 0
                            Tip = "服务器核心和内存还没设置好呢\n\n（恼"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "Java和内存还没设置好呢\n\n（恼"
                        else:
                            CanCreate = 0
                            Tip = "你只设置好了服务器名称\n\n（恼"
                else:
                    if (ChkVal[3] == 1):
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "服务器名称和内存还没设置好呢\n\n（恼"
                        else:
                            CanCreate = 0
                            Tip = "你只设置好了Java\n\n（恼"
                    else:
                        if (ChkVal[4] == 1):
                            CanCreate = 0
                            Tip = "你只设置好了服务器核心\n\n（恼"
                        else:
                            CanCreate = 0
                            Tip = "你什么都没设置好呢\n\n（恼"
                            # 终于写完了.jpg

        # Server processor
        if CanCreate == 0:
            CallMCSL2Dialog(Tip, 0)
        elif CanCreate == 1:
            global GlobalServerList
            CallMCSL2Dialog(Tip, 0)
            ServerFolderPath = "./Servers/" + ServerName
            mkdir(ServerFolderPath)
            copy(CorePath, ServerFolderPath)
            ServerConfigDict = {
                "name": ServerName,
                "java_path": JavaPath,
                "min_memory": MinMemory,
                "max_memory": MaxMemory,
            }
            ServerConfigJson = dumps(ServerConfigDict, ensure_ascii=False)
            with open(r'MCSL2/MCSL2_ServerList.json', "r", encoding='utf-8') as ReadGlobalServerListFile:
                GlobalServerList = loads(ReadGlobalServerListFile.read())
                print(GlobalServerList)
                print(type(GlobalServerList))
                ServerCount = len(GlobalServerList)
                print(ServerCount)
                GlobalServerList['MCSLServerList'].append({
                    "name": ServerName,
                    "core_file_name": CoreFileName,
                    "java_path": JavaPath,
                    "min_memory": MinMemory,
                    "max_memory": MaxMemory,
                })
                ReadGlobalServerListFile.close()
            with open(r'MCSL2/MCSL2_ServerList.json', "w", encoding='utf-8') as WriteGlobalServerListFile:
                WriteGlobalServerListFile.write(dumps(GlobalServerList))
                WriteGlobalServerListFile.close()

            print(ServerConfigJson)
            ConfigPath = "Servers//" + ServerName + "//" + "MCSL2ServerConfig.json"
            with open(ConfigPath, "w+") as SaveConfig:
                SaveConfig.write(ServerConfigJson)
                SaveConfig.close()
            SaveConfig = open(ConfigPath, "w+")
            SaveConfig.write(ServerConfigJson)
            SaveConfig.close()
            Tip = "服务器部署完毕！"
            MinMemStatus = 0
            MaxMemStatus = 0
            NameStatus = 0
            JavaStatus = 0
            CoreStatus = 0
            JavaPath = 0
            CallMCSL2Dialog(Tip, 0)
        else:
            Tip = "服务器部署失败，\n\n但不是你的问题，\n\n去找开发者反馈吧！"
            CallMCSL2Dialog(Tip, 0)

    def AutoDetectJava(self):
        # 防止同时多次运行worker线程
        self.Auto_Find_Java_PushButton.setDisabled(True)
        self.JavaFindWorkThreadFactory.Create().start()

    @pyqtSlot(list)
    def JavaDetectFinished(self, _JavaPaths: list):
        global JavaPaths

        with open("MCSL2/AutoDetectJavaHistory.txt", 'w+', encoding='utf-8') as SaveFoundedJava:
            JavaPaths = list({p[:-1] for p in SaveFoundedJava.readlines()}.union(set(JavaPaths)).union(set(_JavaPaths)))
            # 获取新发现的Java路径,或者用户选择的Java路径
            SaveFoundedJava.writelines([p + '\n' for p in JavaPaths])

    @pyqtSlot(int)
    def OnJavaFindWorkThreadFinished(self, sequenceNumber):

        # 如果不是第一次运行worker线程
        if sequenceNumber > 1:
            Tip = "搜索完毕。\n找到" + str(len(JavaPaths)) + "个Java。\n请点击Java列表查看。"
            CallMCSL2Dialog(Tip, isNeededTwoButtons=0)

        # 释放AutoDetectJava中禁用的按钮
        self.Auto_Find_Java_PushButton.setEnabled(True)
        # 更新self.ChooseJavaScrollAreaVerticalLayout中的内容

    def ShowFoundedJavaList_Back(self):
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
        self.FunctionsStackedWidget.setCurrentIndex(2)
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
        # 如果存在DownloadSource且不为空,则不再重新获取
        if self.downloadUrlDict.get(DownloadSource) is not None:
            idx = self.DownloadSwitcher_TabWidget.currentIndex()
            self.InitDownloadSubWidget(
                self.downloadUrlDict[DownloadSource][idx]['SubWidgetNames'],
                self.downloadUrlDict[DownloadSource][idx]['DownloadUrls']
            )
        else:
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
        self.downloadUrlDict.update(_downloadUrlDict)
        self.RefreshDownloadType()

    def InitDownloadSubWidget(self, SubWidgetNames, DownloadUrls):
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

        # The function of getting Minecraft server console's output
        # def GetMCConsoleOutput(self):
        #     subprocess.run(['cmd', '/c', 'dir'], stdout=subprocess.PIPE)
        #     output = result.stdout.decode('utf-8')

    def initDownloadSubWidget(self, i):
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
        if subWidgetNames == -2:
            Tip = "无法连接MCSLAPI，\n\n请检查网络或系统代理设置"
            CallMCSL2Dialog(Tip, isNeededTwoButtons=0)
            return
        elif subWidgetNames == -1:
            Tip = "可能解析api内容失败\n\n请检查网络或自己的节点设置"
            CallMCSL2Dialog(Tip, isNeededTwoButtons=0)
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
        # 清空self.ChooseJavaScrollAreaVerticalLayout下的所有子控件
        for i in reversed(range(self.ChooseJavaScrollAreaVerticalLayout.count())):
            self.ChooseJavaScrollAreaVerticalLayout.itemAt(i).widget().setParent(None)

        # 重新添加子控件
        if len(JavaPaths) == 0:
            if ospath.exists("MCSL2/AutoDetectJavaHistory.txt"):
                with open("MCSL2/AutoDetectJavaHistory.txt", 'r', encoding='utf-8') as ReadFoundedJava:
                    FoundedJavaTMP = [p[:-1] for p in ReadFoundedJava.readlines()]
                    print(FoundedJavaTMP)
                    JavaPaths = FoundedJavaTMP

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
            JavaVersion = GetJavaVersion(File=JavaPaths[i])
            self.IntroductionLabel_S.setText("Java版本：" + JavaVersion + "\n" + JavaPaths[i])
            self.Select_PushButton.setText("选择")
            self.Select_PushButton.clicked.connect(lambda: self.ParseSrollAreaItemButtons())

            self.ChooseJavaScrollAreaVerticalLayout.addWidget(self.MCSL2_SubWidget_Select)

    def ParseSrollAreaItemButtons(self):
        global ScrollAreaStatus
        SenderButton = str(self.sender().objectName()).split("_PushButton")
        SelectDownloadItemIndexNumber = int(SenderButton[1])
        if self.FunctionsStackedWidget.currentIndex() == 7:
            self.ChooseJava(JavaIndex=SelectDownloadItemIndexNumber)

    def ChooseJava(self, JavaIndex):
        global JavaPaths, JavaPath
        JavaPath = JavaPaths[JavaIndex]
        self.FunctionsStackedWidget.setCurrentIndex(1)
        self.Java_Version_Label.setText(GetJavaVersion(File=JavaPath))

    # The function of checking update
    def CheckUpdate(self):
        CheckUpdateUrlPrefix = "http://api.2018k.cn/checkVersion?id=BCF5D58B4AE6471E98CFD5A56604560B&version="
        CheckUpdateUrl = CheckUpdateUrlPrefix + Version
        LatestVersionInformation = get(CheckUpdateUrl).text.split("|")
        if LatestVersionInformation[0] == "true":
            # New version.
            UpdateDownloadUrl = LatestVersionInformation[3]
            GetUpdateContentsUrl = "http://api.2018k.cn/getExample?id=BCF5D58B4AE6471E98CFD5A56604560B&data=remark"
            WhatInLatestVersion = get(GetUpdateContentsUrl).text
            LatestVersionNumber = LatestVersionInformation[4]
            self.Update_Introduction_Title_Label.setText(
                "这是最新版本" + LatestVersionNumber + "的说明："
            )
            self.Update_Introduction_Label.setText(WhatInLatestVersion)
            self.FunctionsStackedWidget.setCurrentIndex(8)
        elif LatestVersionInformation[0] == "false":
            Tip = "已经是最新版！"
            CallMCSL2Dialog(Tip, isNeededTwoButtons=0)


def GetJavaVersion(File):
    # 运行java.exe并捕获输出
    output = check_output([File, '-version'], stderr=STDOUT)
    # 从输出中提取版本信息
    version_pattern = r'(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[._](\d+))?(?:-(.+))?'
    version_match = search(version_pattern, output.decode('utf-8'))

    # 输出版本信息
    if version_match:
        version = '.'.join(filter(None, version_match.groups()))
        return version
    else:
        return "Failed to retrieve Java version information."


if __name__ == '__main__':
    JavaPath = 0
    JavaPaths = []
    DiskSymbols = []
    SearchStatus = 0
    CorePath = ""
    DownloadSource = 0
    Version = "2.0.1"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    MCSLProcess = QApplication(argv)
    MCSLMainWindow = MCSL2MainWindow()
    MCSLMainWindow.show()
    exit(MCSLProcess.exec_())

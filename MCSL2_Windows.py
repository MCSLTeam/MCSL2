from json import dump
from os import getcwd, environ, remove, path as ospath
from subprocess import CalledProcessError
from sys import argv, exit

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
from MCSL2_Libs.MCSL2_Dialog import CallMCSL2Dialog
from MCSL2_Libs.MCSL2_DownloadURLParser import FetchDownloadURLThreadFactory
from MCSL2_Libs.MCSL2_Init import InitMCSL
from MCSL2_Libs.MCSL2_JavaDetector import GetJavaVersion, Java
from MCSL2_Libs.MCSL2_MainWindow import *  # noqa: F403
from MCSL2_Libs.MCSL2_ServerController import CheckAvailableSaveServer, SaveServer, ReadGlobalServerConfig, \
    ServerLauncher
from MCSL2_Libs.MCSL2_Updater import Updater


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
        self.Download_Core_PushButton.clicked.connect(self.ToDownloadPage)
        self.Choose_Java_Back_PushButton.clicked.connect(self.ShowFoundedJavaList_Back)
        self.Founded_Java_List_PushButton.clicked.connect(self.ToChooseJavaPage)
        self.DoNotUpdate_PushButton.clicked.connect(self.ToAboutPage)

        # Functions binding
        self.DownloadSwitcher_TabWidget.currentChanged.connect(self.RefreshDownloadType)
        self.GoToDownloadSourceChangerPushButton.clicked.connect(self.ToAboutPage)
        self.Start_PushButton.clicked.connect(self.StartMCServerHelper)
        self.MCSLAPIDownloadSourceComboBox.currentIndexChanged.connect(self.DownloadSourceChanger)
        self.Manual_Import_Core_PushButton.clicked.connect(self.ManuallyImportCore)
        self.Download_Java_PushButton.clicked.connect(self.ToDownloadJava)
        self.UpdatePushButton.clicked.connect(self.CheckUpdate)
        # self.Download_PushButton.clicked.connect(self.StartDownload)
        self.Auto_Find_Java_PushButton.clicked.connect(self.AutoDetectJava)
        self.Completed_Save_PushButton.clicked.connect(self.SaveMinecraftServer)
        self.NoobAddServer.clicked.connect(lambda: self.ConfigModeWidget.setCurrentIndex(1))
        self.ExAddServer.clicked.connect(lambda: self.ConfigModeWidget.setCurrentIndex(2))
        # self.HowToAddServerComboBox.currentIndexChanged.connect(self.ChangeAddServerMode)
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
        self.FunctionsStackedWidget.setCurrentIndex(1)
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
        # 清空缓存
        self.downloadUrlDict.clear()
        self.FunctionsStackedWidget.setCurrentIndex(2)
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
        self.FunctionsStackedWidget.setCurrentIndex(3)
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
        self.FunctionsStackedWidget.setCurrentIndex(4)
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
        self.FunctionsStackedWidget.setCurrentIndex(5)
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
        self.CurrentVersionLabel.setText(f"当前版本：{Version}")

    def ToChooseServerPage(self):
        global GlobalServerList

        GlobalConfig = ReadGlobalServerConfig()
        ServerCount = GlobalConfig[0]
        GlobalServerList = GlobalConfig[1]
        if str(GlobalServerList) == "[]":
            ReturnNum = CallMCSL2Dialog(Tip="没有找到任何已添加的服务器。\n\n点击添加去添加一个吧！\n\n此处界面卡顿请按几下Alt或者Option",
                                        isNeededTwoButtons=1, ButtonArg="添加|取消")
            print(ReturnNum)
            if ReturnNum == 1:
                self.ToConfigPage()
                QApplication.processEvents()
            else:
                pass
        else:
            self.FunctionsStackedWidget.setCurrentIndex(6)
            self.InitSelectServerSubWidget(ServerCount, GlobalServerList)

    def StartMCServerHelper(self):
        global GlobalServerList, ServerIndexNum

        GlobalServerList = ReadGlobalServerConfig()[1]
        if str(GlobalServerList) == "[]":
            ReturnNum = CallMCSL2Dialog(Tip="没有找到任何已添加的服务器。\n\n点击添加去添加一个吧！\n\n此处界面卡顿请按几下Alt或者Option",
                                        isNeededTwoButtons=1, ButtonArg="添加|取消")
            print(ReturnNum)
            if ReturnNum == 1:
                self.ToConfigPage()
                QApplication.processEvents()
            else:
                pass
        ServerLauncher().GetGlobalServerConfig(ServerIndexNum=ServerIndexNum)

    def ToChooseJavaPage(self):
        global JavaPaths

        self.FunctionsStackedWidget.setCurrentIndex(7)
        self.InitSelectJavaSubWidget()

    # def ChangeAddServerMode(self):
    #

    # Download Sources Changer

    def DownloadSourceChanger(self):
        global DownloadSource
        DownloadSource = int(self.MCSLAPIDownloadSourceComboBox.currentIndex())
        self.CurrentDownloadSourceLabel.setText("当前下载源：" + str(self.MCSLAPIDownloadSourceComboBox.currentText()))

    def ManuallySelectJava(self):
        JavaPathSysList = QFileDialog.getOpenFileName(
            self, "选择java.exe程序", getcwd(), "java.exe"
        )
        if JavaPathSysList[0] != "":
            v = GetJavaVersion(JavaPathSysList[0])
            if not isinstance(v, CalledProcessError):
                JavaPaths.append(Java(JavaPathSysList[0], v))
            else:
                CallMCSL2Dialog(f"选择的Java无效:\t\n{v.output}", 0, ButtonArg=None)
        else:
            Tip = "看来你没有选择任何的Java呢！"
            CallMCSL2Dialog(Tip, 0, ButtonArg=None)

    def ManuallyImportCore(self):
        global CorePath, CoreFileName
        CoreSysList = QFileDialog.getOpenFileName(self, "选择服务器核心", getcwd(), "*.jar")
        if CoreSysList[0] != "":
            CorePath = CoreSysList[0]
            CoreFileName = CorePath.split("/")
            CoreFileName = CoreFileName[-1]
        else:
            Tip = "看来你没有选择任何的服务器核心呢！"
            CallMCSL2Dialog(Tip, 0, ButtonArg=None)

    def SaveMinecraftServer(self):
        global JavaPath, MaxMemory, MinMemory, CoreFileName, CanCreate
        """
        0 -> Illegal
        1 -> OK
        """

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

        # Server processor
        if CanCreate == 0:
            CallMCSL2Dialog(Tip, 0, ButtonArg=None)
        elif CanCreate == 1:
            CallMCSL2Dialog(Tip, isNeededTwoButtons=0, ButtonArg=None)
            SaveServer(ServerName=ServerName, CorePath=CorePath, JavaPath=JavaPath, MinMemory=MinMemory,
                       MaxMemory=MaxMemory, CoreFileName=CoreFileName)
            MinMemStatus = 0
            MaxMemStatus = 0
            NameStatus = 0
            JavaStatus = 0
            CoreStatus = 0
            JavaPath = 0
        else:
            Tip = "服务器部署失败，\n\n但不是你的问题，\n\n去找开发者反馈吧！"
            CallMCSL2Dialog(Tip, isNeededTwoButtons=0, ButtonArg=None)

    def AutoDetectJava(self):
        # 防止同时多次运行worker线程
        self.Auto_Find_Java_PushButton.setDisabled(True)
        self.JavaFindWorkThreadFactory.Create().start()

    @pyqtSlot(list)
    def JavaDetectFinished(self, _JavaPaths: list):
        global JavaPaths
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

        # 如果不是第一次运行worker线程
        if sequenceNumber > 1:
            Tip = "搜索完毕。\n找到" + str(len(JavaPaths)) + "个Java。\n请点击Java列表查看。"
            CallMCSL2Dialog(Tip, isNeededTwoButtons=0, ButtonArg=None)

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
            self.InitDownloadSubWidget(self.downloadUrlDict[DownloadSource][idx]['SubWidgetNames'])
            # self.downloadUrlDict[DownloadSource][idx]['DownloadUrls']
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

    def InitDownloadSubWidget(self, SubWidgetNames):
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
            CallMCSL2Dialog(Tip, isNeededTwoButtons=0, ButtonArg=None)
            return
        elif subWidgetNames == -1:
            Tip = "可能解析API内容失败\n\n请检查网络或自己的节点设置"
            CallMCSL2Dialog(Tip, isNeededTwoButtons=0, ButtonArg=None)
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
        global ScrollAreaStatus
        SelectDownloadItemIndexNumber = int(str(self.sender().objectName()).split("_PushButton")[1])
        if self.FunctionsStackedWidget.currentIndex() == 7:
            self.ChooseJava(JavaIndex=SelectDownloadItemIndexNumber)
        if self.FunctionsStackedWidget.currentIndex() == 6:
            self.ChooseServer(ServerIndex=SelectDownloadItemIndexNumber)

    def ChooseJava(self, JavaIndex):
        global JavaPaths, JavaPath
        JavaPath = JavaPaths[JavaIndex].Path
        self.FunctionsStackedWidget.setCurrentIndex(1)
        self.Java_Version_Label.setText(JavaPaths[JavaIndex].Version)

    def ChooseServer(self, ServerIndex):
        global ServerIndexNum
        ServerIndexNum = ServerIndex
        self.Selected_Server_Label.setText(f"服务器：{GlobalServerList[ServerIndex]['name']}")
        self.FunctionsStackedWidget.setCurrentIndex(0)

    # The function of checking update
    def CheckUpdate(self):
        LatestVersionInformation = Updater(Version).GetLatestVersionInformation()
        if LatestVersionInformation[0] == 1:
            LatestVersionInformation = str(LatestVersionInformation[1]).replace("(", "").replace(")", "").replace(" ",
                                                                                                                  "").replace(
                "\'", "").split(",")
            self.Update_Introduction_Title_Label.setText("这是最新版本" + LatestVersionInformation[0] + "的说明：")
            self.Update_Introduction_Label.setText(str(LatestVersionInformation[1]).replace("\\n", "\n"))
            self.FunctionsStackedWidget.setCurrentIndex(8)
        else:
            pass


if __name__ == '__main__':
    JavaPath = 0
    JavaPaths = []
    DiskSymbols = []
    GlobalServerList = []
    ServerIndexNum = 0
    SearchStatus = 0
    CorePath = ""
    DownloadSource = 0
    CanCreate = 0
    CoreFileName = ""
    ServerName = ""
    Version = "2.0.1"
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
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "auto"
    MCSLProcess = QApplication(argv)
    MCSLMainWindow = MCSL2MainWindow()
    MCSLMainWindow.show()
    exit(MCSLProcess.exec_())

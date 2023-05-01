from PyQt5.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PyQt5.QtGui import QCursor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QDialog


class Ui_MCSL2_Dialog(object):
    def setupUi(self, MCSL2_Dialog):
        MCSL2_Dialog.setObjectName("MCSL2_Dialog")
        MCSL2_Dialog.setFixedSize(413, 242)
        MCSLWindowIcon = QIcon()
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Normal, QIcon.Off
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Normal, QIcon.On
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Disabled, QIcon.Off
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Disabled, QIcon.On
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Active, QIcon.Off
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Active, QIcon.On
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Selected, QIcon.Off
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Selected, QIcon.On
        )
        MCSL2_Dialog.setWindowIcon(MCSLWindowIcon)
        self.Dialog_PushButton = QPushButton(MCSL2_Dialog)
        self.Dialog_PushButton.setGeometry(QRect(160, 190, 91, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Dialog_PushButton.setFont(font)
        self.Dialog_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Dialog_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 7px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(0, 110, 212);\n"
            "    border-radius: 7px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 100, 212);\n"
            "    border-radius: 7px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Dialog_PushButton.setObjectName("Dialog_PushButton")
        self.Dialog_label = QLabel(MCSL2_Dialog)
        self.Dialog_label.setGeometry(QRect(30, 20, 351, 151))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Dialog_label.setFont(font)
        self.Dialog_label.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Dialog_label.setText("")
        self.Dialog_label.setAlignment(Qt.AlignCenter)
        self.Dialog_label.setObjectName("Dialog_label")
        self.Background = QLabel(MCSL2_Dialog)
        self.Background.setGeometry(QRect(0, 0, 413, 242))
        self.Background.setStyleSheet(
            "QLabel\n" "{\n" "    background-color: rgba(247, 247, 247,85%);\n" "}"
        )
        self.Background.setText("")
        self.Background.setObjectName("Background")
        self.Background.raise_()
        self.Dialog_PushButton.raise_()
        self.Dialog_label.raise_()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.retranslateUi(MCSL2_Dialog)
        QMetaObject.connectSlotsByName(MCSL2_Dialog)

    def retranslateUi(self, MCSL2_Dialog):
        _translate = QCoreApplication.translate
        MCSL2_Dialog.setWindowTitle(_translate("MCSL2_Dialog", "提示"))
        self.Dialog_PushButton.setText(_translate("MCSL2_Dialog", "知道了"))
        self.Dialog_PushButton.clicked.connect(self.close)


class Ui_MCSL2_AskDialog(object):
    def setupUi(self, MCSL2_AskDialog):
        MCSL2_AskDialog.setObjectName("MCSL2_AskDialog")
        MCSL2_AskDialog.setFixedSize(413, 242)
        MCSLWindowIcon = QIcon()
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Normal, QIcon.Off
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Normal, QIcon.On
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Disabled, QIcon.Off
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Disabled, QIcon.On
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Active, QIcon.Off
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Active, QIcon.On
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Selected, QIcon.Off
        )
        MCSLWindowIcon.addPixmap(
            QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"), QIcon.Selected, QIcon.On
        )
        MCSL2_AskDialog.setWindowIcon(MCSLWindowIcon)
        self.Dialog_PushButton_Accept = QPushButton(MCSL2_AskDialog)
        self.Dialog_PushButton_Accept.setGeometry(QRect(90, 190, 91, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Dialog_PushButton_Accept.setFont(font)
        self.Dialog_PushButton_Accept.setCursor(QCursor(Qt.PointingHandCursor))
        self.Dialog_PushButton_Accept.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 7px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(0, 110, 212);\n"
            "    border-radius: 7px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 100, 212);\n"
            "    border-radius: 7px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Dialog_PushButton_Accept.setObjectName("Dialog_PushButton")
        self.Dialog_label = QLabel(MCSL2_AskDialog)
        self.Dialog_label.setGeometry(QRect(30, 20, 351, 151))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Dialog_label.setFont(font)
        self.Dialog_label.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Dialog_label.setText("")
        self.Dialog_label.setAlignment(Qt.AlignCenter)
        self.Dialog_label.setObjectName("Dialog_label")
        self.Background = QLabel(MCSL2_AskDialog)
        self.Background.setGeometry(QRect(0, 0, 413, 242))
        self.Background.setStyleSheet(
            "QLabel\n" "{\n" "    background-color: rgba(247, 247, 247,85%);\n" "}"
        )
        self.Background.setText("")
        self.Background.setObjectName("Background")
        self.Dialog_PushButton_Cancel = QPushButton(MCSL2_AskDialog)
        self.Dialog_PushButton_Cancel.setGeometry(QRect(230, 190, 91, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Dialog_PushButton_Cancel.setFont(font)
        self.Dialog_PushButton_Cancel.setCursor(QCursor(Qt.PointingHandCursor))
        self.Dialog_PushButton_Cancel.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(240, 240, 240);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(229, 229, 229);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.Dialog_PushButton_Cancel.setObjectName("Dialog_PushButton_2")
        self.Background.raise_()
        self.Dialog_PushButton_Accept.raise_()
        self.Dialog_label.raise_()
        self.Dialog_PushButton_Cancel.raise_()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.retranslateUi(MCSL2_AskDialog)
        QMetaObject.connectSlotsByName(MCSL2_AskDialog)

    def retranslateUi(self, MCSL2_AskDialog):
        _translate = QCoreApplication.translate
        MCSL2_AskDialog.setWindowTitle(_translate("MCSL2_AskDialog", "提示"))
        self.Dialog_PushButton_Accept.setText(_translate("MCSL2_AskDialog", "确定"))
        self.Dialog_PushButton_Cancel.setText(_translate("MCSL2_AskDialog", "取消"))


# Customize dialogs
class MCSL2Dialog(QDialog, Ui_MCSL2_Dialog):
    def __init__(self, Tip, parent=None):
        super(MCSL2Dialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.Dialog_label.setText(Tip)


class MCSL2AskDialog(QDialog, Ui_MCSL2_AskDialog):
    def __init__(self, Tip, ButtonArg, parent=None):
        super(MCSL2AskDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.ReturnN = None
        ButtonArg = str(ButtonArg).split("|")
        self.Dialog_label.setText(Tip)
        self.Dialog_PushButton_Accept.setText(ButtonArg[0])
        self.Dialog_PushButton_Cancel.setText(ButtonArg[1])
        self.Dialog_PushButton_Accept.clicked.connect(self.Accept)
        self.Dialog_PushButton_Cancel.clicked.connect(self.Cancel)

    def Accept(self):
        global ReturnNum
        ReturnNum = 1
        self.close()

    def Cancel(self):
        global ReturnNum
        ReturnNum = 0
        self.close()


# The function of calling MCSL2 Dialog
def CallMCSL2Dialog(Tip, OtherTextArg, isNeededTwoButtons, ButtonArg, parent=None):
    if OtherTextArg is None:
        OtherTextArg = ""
    else:
        pass
    try:
        Tip = getattr(DialogMsg(), Tip) + OtherTextArg
    except AttributeError:
        Tip = Tip + OtherTextArg
    if isNeededTwoButtons == 0:
        Dialog = MCSL2Dialog(Tip, parent)
    elif isNeededTwoButtons == 1:
        Dialog = MCSL2AskDialog(Tip, ButtonArg, parent)
    else:
        return
    Dialog.exec_()
    return ReturnNum


class DialogMsg:
    def __init__(self):
        self.ProgramVersionIsUpToDate = "已经是最新版！"
        self.ConfigPageBeginToSetUpServer = "关闭此窗口后，\n\n服务器将会开始部署。"
        self.ConfigPageNoServerCore = "只剩服务器核心没设置好力\n\n（喜"
        self.ConfigPageNoJava = "只剩Java没设置好力\n\n（喜"
        self.ConfigPageNoJavaAndServerCore = "只剩Java和服务器核心没设置好力\n\n（喜"
        self.ConfigPageNoServerName = "只剩服务器名称没设置好力\n\n（喜"
        self.ConfigPageNoServerNameAndServerCore = "只剩服务器名称和服务器核心没设置好力\n\n（喜"
        self.ConfigPageNoServerNameAndJava = "只剩服务器名称和Java没设置好力\n\n（喜"
        self.ConfigPageOnlyMinMemoryAndMaxMemory = "你只设置好了内存\n\n（恼"
        self.ConfigPageNoMaxMemory = "只剩最大内存没设置好力\n\n（喜"
        self.ConfigPageNoMaxMemoryAndServerCore = "只剩最大内存和服务器核心没设置好力\n\n（喜"
        self.ConfigPageNoMaxMemoryAndJava = "只剩最大内存和Java没设置好力\n\n（喜"
        self.ConfigPageNoServerCoreAndJavaAndMaxMemory = "服务器核心、Java和最大内存还没设置好呢\n\n（恼"
        self.ConfigPageNoServerNameAndMaxMemory = "只剩服务器名称和最大内存没设置好力\n\n（喜"
        self.ConfigPageNoServerCodeAndServerNameAndMaxMemory = "服务器核心、服务器名称和最大内存还没设置好呢\n\n（恼"
        self.ConfigPageNoJavaAndServerNameAndMaxMemory = "Java、服务器名称和最大内存还没设置好呢\n\n（恼"
        self.ConfigPageOnlyMinMemory = "你只设置好了最小内存\n\n（恼"
        self.ConfigPageNoMinMemory = "只剩最小内存没设置好力\n\n（喜"
        self.ConfigPageNoServerCoreAndMinMemory = "只剩服务器核心和最小内存没设置好力\n\n（喜"
        self.ConfigPageNoJavaAndMinMemory = "只剩Java和最小内存没设置好力\n\n（喜"
        self.ConfigPageNoServerCoreAndJavaAndMinMemory = "服务器核心、Java和最小内存还没设置好呢\n\n（恼"
        self.ConfigPageNoServerNameAndMinMemory = "只剩服务器名称和最小内存没设置好力\n\n（喜"
        self.ConfigPageNoServerCoreAndServerNameAndMinMemory = "服务器核心、服务器名称和最小内存还没设置好呢\n\n（恼"
        self.ConfigPageNoJavaAndServerNameAndMinMemory = "Java、服务器名称和最小内存还没设置好呢\n\n（恼"
        self.ConfigPageOnlyMaxMemory = "你只设置好了最大内存\n\n（恼"
        self.ConfigPageNoMinMemoryAndMaxMemory = "只剩内存没设置好力\n\n（喜"
        self.ConfigPageNoServerCoreAndMinMemoryAndMaxMemory = "服务器核心和内存还没设置好呢\n\n（恼"
        self.ConfigPageNoJavaAndMinMemoryAndMaxMemory = "Java和内存还没设置好呢\n\n（恼"
        self.ConfigPageOnlyServerName = "你只设置好了服务器名称\n\n（恼"
        self.ConfigPageNoServerNameAndMinMemoryAndMaxMemory = "服务器名称和内存还没设置好呢\n\n（恼"
        self.ConfigPageOnlyJava = "你只设置好了Java\n\n（恼"
        self.ConfigPageOnlyServerCore = "你只设置好了服务器核心\n\n（恼"
        self.ConfigPageNothing = "你什么都没设置好呢\n\n（恼"
        self.ConfigPageQFileDialogNoCore = "看来你没有选择任何的服务器核心呢！"
        self.ConfigPageQFileDialogNoJava = "看来你没有选择任何的Java呢！"
        self.ConfigPageQFileDialogInvalidJava = "选择的Java无效:\t\n"
        self.ConfigPageAutoDetectJavaFinished = "搜索完毕,请点击Java列表查看。\n结果数量为"
        self.ConfigPageAddServerUnexpectedFailed = "服务器部署失败，\n\n但不是你的问题，\n\n去找开发者反馈吧！"

        self.ServerControllerNoServerCanBeFound = "没有找到任何已添加的服务器。\n\n点击添加去添加一个吧！\n\n此处界面卡顿请按几下Alt或者Option"
        self.ServerControllerNoAcceptedMojangEula = "您所启动的服务器\n并未同意Mojang EULA。\n按下\"确定\"来同意，\n或点击\"取消\"以拒绝。"

        self.DownloadPageConnectToMCSLAPIFailed = "无法连接MCSLAPI，\n\n请检查网络或系统代理设置"
        self.DownloadPageEncodeMCSLAPIContentFailed = "可能解析API内容失败\n\n请检查网络或自己的节点设置"

ReturnNum = 0

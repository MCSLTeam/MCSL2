from PyQt5.QtCore import QCoreApplication, QMetaObject, QRect, Qt, QSize
from PyQt5.QtGui import QCursor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QDialog, QSpacerItem, QSizePolicy, QHBoxLayout, QWidget, QGridLayout
from MCSL2_Libs.MCSL2_Logger import MCSL2Logger
MCSLLogger = MCSL2Logger()

class Ui_MCSL2_Dialog(object):
    def setupUi(self, MCSL2_Dialog):
        try:
            MCSL2_Dialog.setObjectName("MCSL2_Dialog")
            MCSL2_Dialog.setFixedSize(413, 242)
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                MCSL2_Dialog.sizePolicy().hasHeightForWidth())
            MCSL2_Dialog.setSizePolicy(sizePolicy)
            MCSL2_Dialog.setMinimumSize(QSize(413, 260))
            MCSL2_Dialog.setMaximumSize(QSize(413, 16777215))
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
            MCSL2_Dialog.setStyleSheet("QDialog\n"
                                    "{\n"
                                    "    background-color: rgba(247, 247, 247,85%);\n"
                                    "}")
            self.gridLayout = QGridLayout(MCSL2_Dialog)
            self.gridLayout.setObjectName("gridLayout")
            self.Dialog_label = QLabel(MCSL2_Dialog)
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.Dialog_label.sizePolicy().hasHeightForWidth())
            self.Dialog_label.setSizePolicy(sizePolicy)
            self.Dialog_label.setMinimumSize(QSize(351, 151))
            self.Dialog_label.setMaximumSize(QSize(351, 16777215))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(11)
            self.Dialog_label.setFont(font)
            self.Dialog_label.setStyleSheet("QLabel\n"
                                            "{\n"
                                            "    background-color: rgb(255, 255, 255);\n"
                                            "    border-radius: 10px\n"
                                            "}")
            self.Dialog_label.setText("")
            self.Dialog_label.setAlignment(Qt.AlignCenter)
            self.Dialog_label.setObjectName("Dialog_label")
            self.gridLayout.addWidget(self.Dialog_label, 1, 1, 1, 1)
            spacerItem = QSpacerItem(
                40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
            spacerItem1 = QSpacerItem(
                40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
            self.Dialog_PushButton = QPushButton(MCSL2_Dialog)
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.Dialog_PushButton.sizePolicy().hasHeightForWidth())
            self.Dialog_PushButton.setSizePolicy(sizePolicy)
            self.Dialog_PushButton.setMinimumSize(QSize(351, 31))
            self.Dialog_PushButton.setMaximumSize(QSize(351, 31))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(10)
            self.Dialog_PushButton.setFont(font)
            self.Dialog_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
            self.Dialog_PushButton.setStyleSheet("QPushButton\n"
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
                                                "}")
            self.Dialog_PushButton.setObjectName("Dialog_PushButton")
            self.gridLayout.addWidget(self.Dialog_PushButton, 3, 1, 1, 1)
            spacerItem2 = QSpacerItem(
                40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
            spacerItem3 = QSpacerItem(
                40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.gridLayout.addItem(spacerItem3, 1, 0, 1, 1)
            spacerItem4 = QSpacerItem(
                40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.gridLayout.addItem(spacerItem4, 4, 1, 1, 1)

            self.retranslateUi(MCSL2_Dialog)
            QMetaObject.connectSlotsByName(MCSL2_Dialog)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

        def retranslateUi(self, MCSL2_Dialog):
            try:
                _translate = QCoreApplication.translate
                MCSL2_Dialog.setWindowTitle(_translate("MCSL2_Dialog", "提示"))
                self.Dialog_PushButton.setText(_translate("MCSL2_Dialog", "知道了"))
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
            except Exception as e:
                MCSLLogger.ExceptionLog(e)

    def retranslateUi(self, MCSL2_Dialog):
        
        try:
            _translate = QCoreApplication.translate
            MCSL2_Dialog.setWindowTitle(_translate("MCSL2_Dialog", "提示"))
            self.Dialog_PushButton.setText(_translate("MCSL2_Dialog", "知道了"))
            self.Dialog_PushButton.clicked.connect(self.close)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)


class Ui_MCSL2_AskDialog(object):
    def setupUi(self, MCSL2_AskDialog):
        try:
            MCSL2_AskDialog.setObjectName("MCSL2_AskDialog")
            MCSL2_AskDialog.setFixedSize(413, 242)
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                MCSL2_AskDialog.sizePolicy().hasHeightForWidth())
            MCSL2_AskDialog.setSizePolicy(sizePolicy)
            MCSL2_AskDialog.setMinimumSize(QSize(413, 260))
            MCSL2_AskDialog.setMaximumSize(QSize(413, 16777215))
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
            MCSL2_AskDialog.setStyleSheet("QDialog\n"
                                        "{\n"
                                        "    background-color: rgba(247, 247, 247,85%);\n"
                                        "}")
            self.gridLayout = QGridLayout(MCSL2_AskDialog)
            self.gridLayout.setObjectName("gridLayout")
            self.Dialog_label = QLabel(MCSL2_AskDialog)
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.Dialog_label.sizePolicy().hasHeightForWidth())
            self.Dialog_label.setSizePolicy(sizePolicy)
            self.Dialog_label.setMinimumSize(QSize(351, 151))
            self.Dialog_label.setMaximumSize(QSize(351, 16777215))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(11)
            self.Dialog_label.setFont(font)
            self.Dialog_label.setStyleSheet("QLabel\n"
                                            "{\n"
                                            "    background-color: rgb(255, 255, 255);\n"
                                            "    border-radius: 10px\n"
                                            "}")
            self.Dialog_label.setText("")
            self.Dialog_label.setAlignment(Qt.AlignCenter)
            self.Dialog_label.setObjectName("Dialog_label")
            self.gridLayout.addWidget(self.Dialog_label, 1, 1, 1, 1)
            spacerItem = QSpacerItem(
                40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
            self.ButtonWidget = QWidget(MCSL2_AskDialog)
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(35)
            sizePolicy.setVerticalStretch(40)
            sizePolicy.setHeightForWidth(
                self.ButtonWidget.sizePolicy().hasHeightForWidth())
            self.ButtonWidget.setSizePolicy(sizePolicy)
            self.ButtonWidget.setMinimumSize(QSize(351, 40))
            self.ButtonWidget.setMaximumSize(QSize(351, 40))
            self.ButtonWidget.setObjectName("ButtonWidget")
            self.horizontalLayout = QHBoxLayout(self.ButtonWidget)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.Dialog_PushButton_Cancel = QPushButton(self.ButtonWidget)
            sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.Dialog_PushButton_Cancel.sizePolicy().hasHeightForWidth())
            self.Dialog_PushButton_Cancel.setSizePolicy(sizePolicy)
            self.Dialog_PushButton_Cancel.setMinimumSize(QSize(165, 31))
            self.Dialog_PushButton_Cancel.setMaximumSize(QSize(170, 31))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(10)
            self.Dialog_PushButton_Cancel.setFont(font)
            self.Dialog_PushButton_Cancel.setCursor(QCursor(Qt.PointingHandCursor))
            self.Dialog_PushButton_Cancel.setStyleSheet("QPushButton\n"
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
                                                        "}")
            self.Dialog_PushButton_Cancel.setObjectName("Dialog_PushButton_Cancel")
            self.horizontalLayout.addWidget(self.Dialog_PushButton_Cancel)
            self.Dialog_PushButton_Accept = QPushButton(self.ButtonWidget)
            sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.Dialog_PushButton_Accept.sizePolicy().hasHeightForWidth())
            self.Dialog_PushButton_Accept.setSizePolicy(sizePolicy)
            self.Dialog_PushButton_Accept.setMinimumSize(QSize(160, 31))
            self.Dialog_PushButton_Accept.setMaximumSize(QSize(170, 31))
            font = QFont()
            font.setFamily("Microsoft YaHei UI")
            font.setPointSize(10)
            self.Dialog_PushButton_Accept.setFont(font)
            self.Dialog_PushButton_Accept.setCursor(QCursor(Qt.PointingHandCursor))
            self.Dialog_PushButton_Accept.setStyleSheet("QPushButton\n"
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
                                                        "}")
            self.Dialog_PushButton_Accept.setObjectName("Dialog_PushButton_Accept")
            self.horizontalLayout.addWidget(self.Dialog_PushButton_Accept)
            self.gridLayout.addWidget(self.ButtonWidget, 2, 1, 1, 1)
            spacerItem1 = QSpacerItem(
                40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)
            spacerItem2 = QSpacerItem(
                40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
            spacerItem3 = QSpacerItem(
                40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.gridLayout.addItem(spacerItem3, 1, 0, 1, 1)

            self.retranslateUi(MCSL2_AskDialog)
            QMetaObject.connectSlotsByName(MCSL2_AskDialog)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def retranslateUi(self, MCSL2_AskDialog):
        
        try:
            _translate = QCoreApplication.translate
            MCSL2_AskDialog.setWindowTitle(_translate("MCSL2_AskDialog", "提示"))
            self.Dialog_PushButton_Cancel.setText(
                _translate("MCSL2_AskDialog", "取消"))
            self.Dialog_PushButton_Accept.setText(
                _translate("MCSL2_AskDialog", "确定"))
        except Exception as e:
            MCSLLogger.ExceptionLog(e)


# Customize dialogs
class MCSL2Dialog(QDialog, Ui_MCSL2_Dialog):
    def __init__(self, Tip, parent=None):
        
        try:
            super(MCSL2Dialog, self).__init__(parent=parent)
            self.setupUi(self)
            self.Dialog_label.setText(Tip)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)


class MCSL2AskDialog(QDialog, Ui_MCSL2_AskDialog):
    def __init__(self, Tip, ButtonArg, parent=None):
        
        try:
            super(MCSL2AskDialog, self).__init__(parent=parent)
            self.setupUi(self)
            self.ReturnN = None
            ButtonArg = str(ButtonArg).split("|")
            self.Dialog_label.setText(Tip)
            self.Dialog_PushButton_Accept.setText(ButtonArg[0])
            self.Dialog_PushButton_Cancel.setText(ButtonArg[1])
            self.Dialog_PushButton_Accept.clicked.connect(self.Accept)
            self.Dialog_PushButton_Cancel.clicked.connect(self.Cancel)
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def Accept(self):
        
        try:
            global ReturnNum
            ReturnNum = 1
            self.close()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)

    def Cancel(self):
        
        try:
            global ReturnNum
            ReturnNum = 0
            self.close()
        except Exception as e:
            MCSLLogger.ExceptionLog(e)


# The function of calling MCSL2 Dialog
def CallMCSL2Dialog(Tip, OtherTextArg, isNeededTwoButtons, ButtonArg, parent=None):
    
    try:
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
    except Exception as e:
        MCSLLogger.ExceptionLog(e)


class DialogMsg:
    def __init__(self):
        try:
            self.ProgramVersionIsUpToDate = "已经是最新版！"
            self.ProgramCheckUpdateFailed = "检查更新失败！"
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
            self.NoAria2 = "未找到Aria2！是否需要安装？"
            self.InstallAria2Failed = "安装Aria2失败，\n\n请自行上网寻找解决办法，\n\n有能力可向开发者反馈。"

            self.Debug = "测试消息：\n"
        except Exception as e:
            MCSLLogger.ExceptionLog(e)


ReturnNum = 0

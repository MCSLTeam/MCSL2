from PyQt5.QtCore import Qt, QCoreApplication, QMetaObject, QRect
from PyQt5.QtGui import QFont, QCursor, QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton, QLabel


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
        Tip = open(r"Tip", "r").read()
        self.Dialog_label.setText(_translate("MCSL2_AskDialog", Tip))
        self.Dialog_PushButton_Accept.clicked.connect(self.close)

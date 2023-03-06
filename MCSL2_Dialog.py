from PyQt5.QtCore import Qt, QCoreApplication, QMetaObject, QRect
from PyQt5.QtGui import QFont, QCursor, QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton, QLabel, QDialog


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
        Tip = open(r"Tip", "r").read()
        self.Dialog_label.setText(_translate("MCSL2_Dialog", Tip))
        self.Dialog_PushButton.clicked.connect(self.close)

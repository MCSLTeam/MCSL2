from PyQt5.QtCore import Qt, QCoreApplication, QMetaObject, QRect
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import Qt

class Ui_MCSL2_Dialog(object):
    def setupUi(self, MCSL2_Dialog):
        MCSL2_Dialog.setObjectName("MCSL2_Dialog")
        MCSL2_Dialog.resize(340, 196)
        self.Dialog_PushButton = QPushButton(MCSL2_Dialog)
        self.Dialog_PushButton.setGeometry(QRect(120, 140, 91, 31))
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
                                             "QPushButton:pressed\n"
                                             "{\n"
                                             "    background-color: rgb(0, 107, 212);\n"
                                             "    border-radius: 7px;\n"
                                             "    color: rgb(255, 255, 255);\n"
                                             "}")
        self.Dialog_PushButton.setObjectName("Dialog_PushButton")
        self.Dialog_label = QLabel(MCSL2_Dialog)
        self.Dialog_label.setGeometry(QRect(30, 20, 281, 101))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Dialog_label.setFont(font)
        self.Dialog_label.setText("")
        self.Dialog_label.setAlignment(Qt.AlignCenter)
        self.Dialog_label.setObjectName("Dialog_label")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.retranslateUi(MCSL2_Dialog)
        QMetaObject.connectSlotsByName(MCSL2_Dialog)

    def retranslateUi(self, MCSL2_Dialog):
        _translate = QCoreApplication.translate
        MCSL2_Dialog.setWindowTitle(_translate("MCSL2_Dialog", "提示"))
        self.Dialog_PushButton.setText(_translate("MCSL2_Dialog", "知道了"))
        Tip = open(r'Tip', 'r').read()
        self.Dialog_label.setText(_translate("MCSL2_Dialog", Tip))
        self.Dialog_PushButton.clicked.connect(self.close)

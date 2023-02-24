from PyQt5.QtCore import QRect, QCoreApplication, QMetaObject, Qt
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QPushButton, QWidget


class Ui_MCSL2_SubWidget_ScrollArea_Select(object):
    def setupUi(self, MCSL2_SubWidget_ScrollArea_Select):
        MCSL2_SubWidget_ScrollArea_Select.setObjectName("MCSL2_SubWidget_ScrollArea_Select")
        MCSL2_SubWidget_ScrollArea_Select.setFixedSize(580, 70)
        self.GraphWidget = QWidget(MCSL2_SubWidget_ScrollArea_Select)
        self.GraphWidget.setGeometry(QRect(10, 10, 51, 51))
        self.GraphWidget.setStyleSheet("QWidget{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 4px;\n"
"}")
        self.GraphWidget.setObjectName("GraphWidget")
        self.IntroductionWidget = QWidget(MCSL2_SubWidget_ScrollArea_Select)
        self.IntroductionWidget.setGeometry(QRect(70, 10, 421, 51))
        self.IntroductionWidget.setStyleSheet("QWidget\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 8px\n"
"}")
        self.IntroductionWidget.setObjectName("IntroductionWidget")
        self.Select_PushButton = QPushButton(MCSL2_SubWidget_ScrollArea_Select)
        self.Select_PushButton.setGeometry(QRect(510, 10, 51, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Select_PushButton.setFont(font)
        self.Select_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Select_PushButton.setStyleSheet("QPushButton\n"
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
        self.Select_PushButton.setFlat(False)
        self.Select_PushButton.setObjectName("Select_PushButton")

        self.retranslateUi(MCSL2_SubWidget_ScrollArea_Select)
        QMetaObject.connectSlotsByName(MCSL2_SubWidget_ScrollArea_Select)

    def retranslateUi(self, MCSL2_SubWidget_ScrollArea_Select):
        _translate = QCoreApplication.translate
        MCSL2_SubWidget_ScrollArea_Select.setWindowTitle(_translate("MCSL2_SubWidget_ScrollArea_Select", "MCSL 2"))
        self.Select_PushButton.setText(_translate("MCSL2_SubWidget_ScrollArea_Select", "选择"))

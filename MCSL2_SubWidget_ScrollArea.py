from PyQt5.QtCore import QRect, Qt, QMetaObject, QCoreApplication
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QPushButton, QWidget


class Ui_MCSL2_SubWidget_ScrollArea(object):
    def setupUi(self, MCSL2_SubWidget_ScrollArea):
        MCSL2_SubWidget_ScrollArea.setObjectName("MCSL2_SubWidget_ScrollArea")
        MCSL2_SubWidget_ScrollArea.resize(580, 70)
        self.GraphWidget = QWidget(MCSL2_SubWidget_ScrollArea)
        self.GraphWidget.setGeometry(QRect(10, 10, 51, 51))
        self.GraphWidget.setStyleSheet("QWidget{\n"
                                       "    background-color: rgb(247, 247, 247);\n"
                                       "    border-radius: 4px;\n"
                                       "}")
        self.GraphWidget.setObjectName("GraphWidget")
        self.IntroductionWidget = QWidget(MCSL2_SubWidget_ScrollArea)
        self.IntroductionWidget.setGeometry(QRect(70, 10, 421, 51))
        self.IntroductionWidget.setStyleSheet("QWidget\n"
                                              "{\n"
                                              "    background-color: rgb(247, 247, 247);\n"
                                              "    border-radius: 8px\n"
                                              "}")
        self.IntroductionWidget.setObjectName("IntroductionWidget")
        self.Download_PushButton = QPushButton(MCSL2_SubWidget_ScrollArea)
        self.Download_PushButton.setGeometry(QRect(510, 10, 51, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Download_PushButton.setFont(font)
        self.Download_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Download_PushButton.setStyleSheet("QPushButton\n"
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
        self.Download_PushButton.setFlat(False)
        self.Download_PushButton.setObjectName("Download_PushButton")

        self.retranslateUi(MCSL2_SubWidget_ScrollArea)
        QMetaObject.connectSlotsByName(MCSL2_SubWidget_ScrollArea)

    def retranslateUi(self, MCSL2_SubWidget_ScrollArea):
        _translate = QCoreApplication.translate
        MCSL2_SubWidget_ScrollArea.setWindowTitle(_translate("MCSL2_SubWidget_ScrollArea", "MCSL 2"))
        self.Download_PushButton.setText(_translate("MCSL2_SubWidget_ScrollArea", "下载"))

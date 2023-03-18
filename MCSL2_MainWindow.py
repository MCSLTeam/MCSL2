from PyQt5.QtCore import Qt, pyqtSignal, QRect, QCoreApplication, QMetaObject
from PyQt5.QtGui import QFont, QPixmap, QCursor, QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QComboBox,
    QStackedWidget,
    QLabel,
    QRadioButton,
    QTabWidget,
    QScrollArea,
    QFrame,
    QAbstractScrollArea,
    QVBoxLayout,
)
import MCSL2_Icon


class Ui_MCSL2_MainWindow(object):
    def setupUi(self, MCSL2_MainWindow):
        MCSL2_MainWindow.setObjectName("MCSL2_MainWindow")
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
        MCSL2_MainWindow.setWindowIcon(MCSLWindowIcon)
        MCSL2_MainWindow.setFixedSize(944, 583)  # Make the size of window unchangeable.
        self.CentralWidget = QWidget(MCSL2_MainWindow)
        self.CentralWidget.setObjectName("CentralWidget")
        self.OptionsWidget = QWidget(self.CentralWidget)
        self.OptionsWidget.setGeometry(QRect(0, 0, 211, 581))
        self.OptionsWidget.setObjectName("OptionsWidget")
        self.Close_PushButton = QPushButton(self.OptionsWidget)
        self.Close_PushButton.setGeometry(QRect(20, 20, 31, 23))
        self.Close_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Close_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(232, 17, 35);\n"
            "    border-radius: 11px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(193, 6, 16);\n"
            "    border-radius: 11px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(170, 0, 0);\n"
            "    border-radius: 11px;\n"
            "}"
        )
        self.Close_PushButton.setText("")
        self.Close_PushButton.setObjectName("Close_PushButton")
        self.Minimize_PushButton = QPushButton(self.OptionsWidget)
        self.Minimize_PushButton.setGeometry(QRect(60, 20, 31, 23))
        self.Minimize_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Minimize_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(225, 225, 0);\n"
            "    border-radius: 11px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(161, 182, 0);\n"
            "    border-radius: 11px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(161, 161, 0);\n"
            "    border-radius: 11px;\n"
            "}"
        )
        self.Minimize_PushButton.setText("")
        self.Minimize_PushButton.setObjectName("Minimize_PushButton")
        self.Home_Page_PushButton = QPushButton(self.OptionsWidget)
        self.Home_Page_PushButton.setEnabled(True)
        self.Home_Page_PushButton.setGeometry(QRect(20, 140, 171, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.Home_Page_PushButton.setFont(font)
        self.Home_Page_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Home_Page_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(243, 243, 243);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(233, 233, 233);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.Home_Page_PushButton.setObjectName("Home_Page_PushButton")
        self.Config_Page_PushButton = QPushButton(self.OptionsWidget)
        self.Config_Page_PushButton.setEnabled(True)
        self.Config_Page_PushButton.setGeometry(QRect(20, 200, 171, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.Config_Page_PushButton.setFont(font)
        self.Config_Page_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Config_Page_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(243, 243, 243);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(233, 233, 233);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.Config_Page_PushButton.setObjectName("Config_Page_PushButton")
        self.MCSL2_Title_Label = QLabel(self.OptionsWidget)
        self.MCSL2_Title_Label.setGeometry(QRect(100, 60, 111, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.MCSL2_Title_Label.setFont(font)
        self.MCSL2_Title_Label.setObjectName("MCSL2_Title_Label")
        self.MCSL2_Title_Author_Label = QLabel(self.OptionsWidget)
        self.MCSL2_Title_Author_Label.setGeometry(QRect(100, 90, 111, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.MCSL2_Title_Author_Label.setFont(font)
        self.MCSL2_Title_Author_Label.setObjectName("MCSL2_Title_Author_Label")
        self.MCSL2_Title_Icon_Label = QLabel(self.OptionsWidget)
        self.MCSL2_Title_Icon_Label.setGeometry(QRect(20, 50, 71, 71))
        self.MCSL2_Title_Icon_Label.setText("")
        self.MCSL2_Title_Icon_Label.setPixmap(QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"))
        self.MCSL2_Title_Icon_Label.setScaledContents(True)
        self.MCSL2_Title_Icon_Label.setObjectName("MCSL2_Title_Icon_Label")
        self.Download_Page_PushButton = QPushButton(self.OptionsWidget)
        self.Download_Page_PushButton.setEnabled(True)
        self.Download_Page_PushButton.setGeometry(QRect(20, 260, 171, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.Download_Page_PushButton.setFont(font)
        self.Download_Page_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Download_Page_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(243, 243, 243);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(233, 233, 233);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.Download_Page_PushButton.setObjectName("Download_Page_PushButton")
        self.Server_Console_Page_PushButton = QPushButton(self.OptionsWidget)
        self.Server_Console_Page_PushButton.setEnabled(True)
        self.Server_Console_Page_PushButton.setGeometry(QRect(20, 320, 171, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.Server_Console_Page_PushButton.setFont(font)
        self.Server_Console_Page_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Server_Console_Page_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(243, 243, 243);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(233, 233, 233);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.Server_Console_Page_PushButton.setObjectName(
            "Server_Console_Page_PushButton"
        )
        self.Tools_Page_PushButton = QPushButton(self.OptionsWidget)
        self.Tools_Page_PushButton.setEnabled(True)
        self.Tools_Page_PushButton.setGeometry(QRect(20, 380, 171, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.Tools_Page_PushButton.setFont(font)
        self.Tools_Page_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Tools_Page_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(243, 243, 243);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(233, 233, 233);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.Tools_Page_PushButton.setObjectName("Tools_Page_PushButton")
        self.About_Page_PushButton = QPushButton(self.OptionsWidget)
        self.About_Page_PushButton.setEnabled(True)
        self.About_Page_PushButton.setGeometry(QRect(20, 440, 171, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.About_Page_PushButton.setFont(font)
        self.About_Page_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.About_Page_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(243, 243, 243);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(233, 233, 233);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.About_Page_PushButton.setObjectName("About_Page_PushButton")
        self.Blue1 = QLabel(self.OptionsWidget)
        self.Blue1.setEnabled(True)
        self.Blue1.setVisible(True)
        self.Blue1.setGeometry(QRect(20, 150, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue1.setFont(font)
        self.Blue1.setAutoFillBackground(False)
        self.Blue1.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 5px\n"
            "}"
        )
        self.Blue1.setText("")
        self.Blue1.setObjectName("Blue1")
        self.Blue2 = QLabel(self.OptionsWidget)
        self.Blue2.setEnabled(True)
        self.Blue2.setVisible(False)
        self.Blue2.setGeometry(QRect(20, 210, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue2.setFont(font)
        self.Blue2.setAutoFillBackground(False)
        self.Blue2.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Blue2.setText("")
        self.Blue2.setObjectName("Blue2")
        self.Blue3 = QLabel(self.OptionsWidget)
        self.Blue3.setEnabled(True)
        self.Blue3.setVisible(False)
        self.Blue3.setGeometry(QRect(20, 270, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue3.setFont(font)
        self.Blue3.setAutoFillBackground(False)
        self.Blue3.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Blue3.setText("")
        self.Blue3.setObjectName("Blue3")
        self.Blue4 = QLabel(self.OptionsWidget)
        self.Blue4.setEnabled(True)
        self.Blue4.setVisible(False)
        self.Blue4.setGeometry(QRect(20, 330, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue4.setFont(font)
        self.Blue4.setAutoFillBackground(False)
        self.Blue4.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Blue4.setText("")
        self.Blue4.setObjectName("Blue4")
        self.Blue5 = QLabel(self.OptionsWidget)
        self.Blue5.setEnabled(True)
        self.Blue5.setVisible(False)
        self.Blue5.setGeometry(QRect(20, 390, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue5.setFont(font)
        self.Blue5.setAutoFillBackground(False)
        self.Blue5.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Blue5.setText("")
        self.Blue5.setObjectName("Blue5")
        self.Blue6 = QLabel(self.OptionsWidget)
        self.Blue6.setEnabled(True)
        self.Blue6.setVisible(False)
        self.Blue6.setGeometry(QRect(20, 450, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue6.setFont(font)
        self.Blue6.setAutoFillBackground(False)
        self.Blue6.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Blue6.setText("")
        self.Blue6.setObjectName("Blue6")
        self.FunctionsStackedWidget = QStackedWidget(self.CentralWidget)
        self.FunctionsStackedWidget.setGeometry(QRect(210, -20, 731, 601))
        self.FunctionsStackedWidget.setAutoFillBackground(False)
        self.FunctionsStackedWidget.setObjectName("FunctionsStackedWidget")
        self.HomePage = QWidget()
        self.HomePage.setObjectName("HomePage")
        self.Home_Label = QLabel(self.HomePage)
        self.Home_Label.setGeometry(QRect(30, 80, 71, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.Home_Label.setFont(font)
        self.Home_Label.setObjectName("Home_Label")
        self.Notice_Widget = QWidget(self.HomePage)
        self.Notice_Widget.setGeometry(QRect(30, 140, 321, 141))
        self.Notice_Widget.setStyleSheet(
            "QWidget\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Notice_Widget.setObjectName("Notice_Widget")
        self.Notice_Label = QLabel(self.Notice_Widget)
        self.Notice_Label.setGeometry(QRect(10, 20, 281, 101))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Notice_Label.setFont(font)
        self.Notice_Label.setAutoFillBackground(False)
        self.Notice_Label.setStyleSheet("")
        self.Notice_Label.setObjectName("Notice_Label")
        self.HomeTip1_Widget = QWidget(self.HomePage)
        self.HomeTip1_Widget.setGeometry(QRect(30, 290, 321, 171))
        self.HomeTip1_Widget.setStyleSheet(
            "QWidget\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.HomeTip1_Widget.setObjectName("HomeTip1_Widget")
        self.HomeTip1_Label = QLabel(self.HomeTip1_Widget)
        self.HomeTip1_Label.setGeometry(QRect(10, 20, 281, 131))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.HomeTip1_Label.setFont(font)
        self.HomeTip1_Label.setAutoFillBackground(False)
        self.HomeTip1_Label.setStyleSheet("")
        self.HomeTip1_Label.setObjectName("HomeTip1_Label")
        self.HomePageButtons_Widget = QWidget(self.HomePage)
        self.HomePageButtons_Widget.setGeometry(QRect(470, 410, 251, 181))
        self.HomePageButtons_Widget.setObjectName("HomePageButtons_Widget")
        self.Selected_Server_Label = QLabel(self.HomePageButtons_Widget)
        self.Selected_Server_Label.setGeometry(QRect(20, 150, 221, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.Selected_Server_Label.setFont(font)
        self.Selected_Server_Label.setObjectName("Selected_Server_Label")
        self.Start_PushButton = QPushButton(self.HomePageButtons_Widget)
        self.Start_PushButton.setGeometry(QRect(10, 80, 231, 61))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(16)
        self.Start_PushButton.setFont(font)
        self.Start_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Start_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 10px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(0, 110, 212);\n"
            "    border-radius: 10px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 100, 212);\n"
            "    border-radius: 10px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Start_PushButton.setFlat(False)
        self.Start_PushButton.setObjectName("Start_PushButton")
        self.Config_PushButton = QPushButton(self.HomePageButtons_Widget)
        self.Config_PushButton.setGeometry(QRect(130, 10, 111, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.Config_PushButton.setFont(font)
        self.Config_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Config_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(230, 230, 230);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(225, 225, 225);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.Config_PushButton.setObjectName("Config_PushButton")
        self.Choose_Server_PushButton = QPushButton(self.HomePageButtons_Widget)
        self.Choose_Server_PushButton.setGeometry(QRect(10, 10, 111, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.Choose_Server_PushButton.setFont(font)
        self.Choose_Server_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Choose_Server_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(230, 230, 230);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(225, 225, 225);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.Choose_Server_PushButton.setObjectName("Choose_Server_PushButton")
        self.FunctionsStackedWidget.addWidget(self.HomePage)
        self.ConfigPage = QWidget()
        self.ConfigPage.setObjectName("ConfigPage")
        self.Config_Label = QLabel(self.ConfigPage)
        self.Config_Label.setGeometry(QRect(30, 80, 221, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.Config_Label.setFont(font)
        self.Config_Label.setObjectName("Config_Label")
        self.Others_Background = QLabel(self.ConfigPage)
        self.Others_Background.setGeometry(QRect(30, 400, 251, 121))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Others_Background.setFont(font)
        self.Others_Background.setAutoFillBackground(False)
        self.Others_Background.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Others_Background.setText("")
        self.Others_Background.setObjectName("Others_Background")
        self.Server_Name_Label = QLabel(self.ConfigPage)
        self.Server_Name_Label.setGeometry(QRect(50, 420, 91, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Server_Name_Label.setFont(font)
        self.Server_Name_Label.setObjectName("Server_Name_Label")
        self.Server_Name_LineEdit = QLineEdit(self.ConfigPage)
        self.Server_Name_LineEdit.setGeometry(QRect(150, 430, 111, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.Server_Name_LineEdit.setFont(font)
        self.Server_Name_LineEdit.setStyleSheet(
            "QLineEdit\n"
            "{\n"
            "    border-radius: 3px;\n"
            "    border: 2px;\n"
            "    border-color: rgb(223, 223, 223);\n"
            "    border-style: solid;\n"
            "}\n"
            ""
        )
        self.Server_Name_LineEdit.setObjectName("Server_Name_LineEdit")
        self.Completed_Save_PushButton = QPushButton(self.ConfigPage)
        self.Completed_Save_PushButton.setGeometry(QRect(50, 470, 211, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Completed_Save_PushButton.setFont(font)
        self.Completed_Save_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Completed_Save_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(0, 110, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 100, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Completed_Save_PushButton.setFlat(False)
        self.Completed_Save_PushButton.setObjectName("Completed_Save_PushButton")
        self.ConfigTip1_Widget = QWidget(self.ConfigPage)
        self.ConfigTip1_Widget.setGeometry(QRect(30, 140, 251, 121))
        self.ConfigTip1_Widget.setStyleSheet(
            "QWidget\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.ConfigTip1_Widget.setObjectName("ConfigTip1_Widget")
        self.ConfigTip1_Label = QLabel(self.ConfigTip1_Widget)
        self.ConfigTip1_Label.setGeometry(QRect(10, 20, 211, 81))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ConfigTip1_Label.setFont(font)
        self.ConfigTip1_Label.setAutoFillBackground(False)
        self.ConfigTip1_Label.setStyleSheet("")
        self.ConfigTip1_Label.setObjectName("ConfigTip1_Label")
        self.ConfigTip2_Widget = QWidget(self.ConfigPage)
        self.ConfigTip2_Widget.setGeometry(QRect(30, 280, 251, 101))
        self.ConfigTip2_Widget.setStyleSheet(
            "QWidget\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.ConfigTip2_Widget.setObjectName("ConfigTip2_Widget")
        self.ConfigTip2_Label = QLabel(self.ConfigTip2_Widget)
        self.ConfigTip2_Label.setGeometry(QRect(10, 10, 211, 81))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ConfigTip2_Label.setFont(font)
        self.ConfigTip2_Label.setAutoFillBackground(False)
        self.ConfigTip2_Label.setStyleSheet("")
        self.ConfigTip2_Label.setObjectName("ConfigTip2_Label")
        self.Configuration_Widget = QWidget(self.ConfigPage)
        self.Configuration_Widget.setGeometry(QRect(310, 140, 351, 341))
        self.Configuration_Widget.setObjectName("Configuration_Widget")
        self.Download_Core_PushButton = QPushButton(self.Configuration_Widget)
        self.Download_Core_PushButton.setGeometry(QRect(230, 240, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Download_Core_PushButton.setFont(font)
        self.Download_Core_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Download_Core_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(0, 110, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 100, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Download_Core_PushButton.setFlat(False)
        self.Download_Core_PushButton.setObjectName("Download_Core_PushButton")
        self.Download_Java_PushButton = QPushButton(self.Configuration_Widget)
        self.Download_Java_PushButton.setGeometry(QRect(130, 70, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Download_Java_PushButton.setFont(font)
        self.Download_Java_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Download_Java_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(0, 110, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 100, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Download_Java_PushButton.setFlat(False)
        self.Download_Java_PushButton.setObjectName("Download_Java_PushButton")
        self.Manual_Import_Core_PushButton = QPushButton(self.Configuration_Widget)
        self.Manual_Import_Core_PushButton.setGeometry(QRect(120, 240, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Manual_Import_Core_PushButton.setFont(font)
        self.Manual_Import_Core_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Manual_Import_Core_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(0, 110, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 100, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Manual_Import_Core_PushButton.setFlat(False)
        self.Manual_Import_Core_PushButton.setObjectName(
            "Manual_Import_Core_PushButton"
        )
        self.Set_Core_Background = QLabel(self.Configuration_Widget)
        self.Set_Core_Background.setGeometry(QRect(0, 220, 351, 121))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Set_Core_Background.setFont(font)
        self.Set_Core_Background.setAutoFillBackground(False)
        self.Set_Core_Background.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Set_Core_Background.setText("")
        self.Set_Core_Background.setObjectName("Set_Core_Background")
        self.Set_Java_Background = QLabel(self.Configuration_Widget)
        self.Set_Java_Background.setGeometry(QRect(0, 0, 351, 121))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Set_Java_Background.setFont(font)
        self.Set_Java_Background.setAutoFillBackground(False)
        self.Set_Java_Background.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Set_Java_Background.setText("")
        self.Set_Java_Background.setObjectName("Set_Java_Background")
        self.Memory_1_Label = QLabel(self.Configuration_Widget)
        self.Memory_1_Label.setGeometry(QRect(20, 150, 71, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Memory_1_Label.setFont(font)
        self.Memory_1_Label.setObjectName("Memory_1_Label")
        self.MinMemory_LineEdit = QLineEdit(self.Configuration_Widget)
        self.MinMemory_LineEdit.setGeometry(QRect(70, 160, 91, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.MinMemory_LineEdit.setFont(font)
        self.MinMemory_LineEdit.setStyleSheet(
            "QLineEdit\n"
            "{\n"
            "    border-radius: 3px;\n"
            "    border: 2px;\n"
            "    border-color: rgb(223, 223, 223);\n"
            "    border-style: solid;\n"
            "}\n"
            ""
        )
        self.MinMemory_LineEdit.setObjectName("MinMemory_LineEdit")
        self.Set_Memory_Background = QLabel(self.Configuration_Widget)
        self.Set_Memory_Background.setGeometry(QRect(0, 140, 351, 61))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Set_Memory_Background.setFont(font)
        self.Set_Memory_Background.setAutoFillBackground(False)
        self.Set_Memory_Background.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Set_Memory_Background.setText("")
        self.Set_Memory_Background.setObjectName("Set_Memory_Background")
        self.ConfigTip3_Label = QLabel(self.Configuration_Widget)
        self.ConfigTip3_Label.setGeometry(QRect(20, 280, 311, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ConfigTip3_Label.setFont(font)
        self.ConfigTip3_Label.setStyleSheet("")
        self.ConfigTip3_Label.setObjectName("ConfigTip3_Label")
        self.Java_Label = QLabel(self.Configuration_Widget)
        self.Java_Label.setGeometry(QRect(20, 20, 71, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Java_Label.setFont(font)
        self.Java_Label.setObjectName("Java_Label")
        self.MaxMemory_LineEdit = QLineEdit(self.Configuration_Widget)
        self.MaxMemory_LineEdit.setGeometry(QRect(190, 160, 91, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.MaxMemory_LineEdit.setFont(font)
        self.MaxMemory_LineEdit.setStyleSheet(
            "QLineEdit\n"
            "{\n"
            "    border-radius: 3px;\n"
            "    border: 2px;\n"
            "    border-color: rgb(223, 223, 223);\n"
            "    border-style: solid;\n"
            "}\n"
            ""
        )
        self.MaxMemory_LineEdit.setObjectName("MaxMemory_LineEdit")
        self.Memory_2_Label = QLabel(self.Configuration_Widget)
        self.Memory_2_Label.setGeometry(QRect(170, 150, 21, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.Memory_2_Label.setFont(font)
        self.Memory_2_Label.setObjectName("Memory_2_Label")
        self.Core_Label = QLabel(self.Configuration_Widget)
        self.Core_Label.setGeometry(QRect(20, 240, 91, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Core_Label.setFont(font)
        self.Core_Label.setObjectName("Core_Label")
        self.Auto_Find_Java_PushButton = QPushButton(self.Configuration_Widget)
        self.Auto_Find_Java_PushButton.setGeometry(QRect(20, 70, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Auto_Find_Java_PushButton.setFont(font)
        self.Auto_Find_Java_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Auto_Find_Java_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(0, 110, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 100, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Auto_Find_Java_PushButton.setFlat(False)
        self.Auto_Find_Java_PushButton.setObjectName("Auto_Find_Java_PushButton")
        self.Memory_Unit_Label = QLabel(self.Configuration_Widget)
        self.Memory_Unit_Label.setGeometry(QRect(290, 150, 51, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Memory_Unit_Label.setFont(font)
        self.Memory_Unit_Label.setObjectName("Memory_Unit_Label")
        self.Java_Version_Label = QLabel(self.Configuration_Widget)
        self.Java_Version_Label.setGeometry(QRect(80, 20, 191, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Java_Version_Label.setFont(font)
        self.Java_Version_Label.setText("")
        self.Java_Version_Label.setObjectName("Java_Version_Label")
        self.Founded_Java_List_PushButton = QPushButton(self.Configuration_Widget)
        self.Founded_Java_List_PushButton.setGeometry(QRect(240, 70, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Founded_Java_List_PushButton.setFont(font)
        self.Founded_Java_List_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Founded_Java_List_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(230, 230, 230);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(227, 227, 227);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(225, 225, 225);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.Founded_Java_List_PushButton.setObjectName("Founded_Java_List_PushButton")
        self.Set_Core_Background.raise_()
        self.Set_Memory_Background.raise_()
        self.Set_Java_Background.raise_()
        self.Download_Core_PushButton.raise_()
        self.Download_Java_PushButton.raise_()
        self.Manual_Import_Core_PushButton.raise_()
        self.Memory_1_Label.raise_()
        self.MinMemory_LineEdit.raise_()
        self.ConfigTip3_Label.raise_()
        self.Java_Label.raise_()
        self.MaxMemory_LineEdit.raise_()
        self.Memory_2_Label.raise_()
        self.Core_Label.raise_()
        self.Auto_Find_Java_PushButton.raise_()
        self.Memory_Unit_Label.raise_()
        self.Java_Version_Label.raise_()
        self.Founded_Java_List_PushButton.raise_()
        self.FunctionsStackedWidget.addWidget(self.ConfigPage)
        self.DownloadPage = QWidget()
        self.DownloadPage.setObjectName("DownloadPage")
        self.Download_Label = QLabel(self.DownloadPage)
        self.Download_Label.setGeometry(QRect(30, 80, 71, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.Download_Label.setFont(font)
        self.Download_Label.setObjectName("Download_Label")
        self.Download_Source_Background = QLabel(self.DownloadPage)
        self.Download_Source_Background.setGeometry(QRect(250, 60, 431, 71))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Download_Source_Background.setFont(font)
        self.Download_Source_Background.setAutoFillBackground(False)
        self.Download_Source_Background.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Download_Source_Background.setText("")
        self.Download_Source_Background.setObjectName("Download_Source_Background")
        self.Download_Source_Label = QLabel(self.DownloadPage)
        self.Download_Source_Label.setGeometry(QRect(270, 80, 91, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.Download_Source_Label.setFont(font)
        self.Download_Source_Label.setObjectName("Download_Source_Label")
        self.luoxisCloud_radioButton = QRadioButton(self.DownloadPage)
        self.luoxisCloud_radioButton.setGeometry(QRect(560, 70, 101, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.luoxisCloud_radioButton.setFont(font)
        self.luoxisCloud_radioButton.setObjectName("luoxisCloud_radioButton")
        self.Gitee_radioButton = QRadioButton(self.DownloadPage)
        self.Gitee_radioButton.setGeometry(QRect(460, 70, 101, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Gitee_radioButton.setFont(font)
        self.Gitee_radioButton.setObjectName("Gitee_radioButton")
        self.SharePoint_radioButton = QRadioButton(self.DownloadPage)
        self.SharePoint_radioButton.setGeometry(QRect(350, 70, 101, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.SharePoint_radioButton.setFont(font)
        self.SharePoint_radioButton.setChecked(True)
        self.SharePoint_radioButton.setObjectName("SharePoint_radioButton")
        self.GitHub_radioButton = QRadioButton(self.DownloadPage)
        self.GitHub_radioButton.setGeometry(QRect(460, 100, 101, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.GitHub_radioButton.setFont(font)
        self.GitHub_radioButton.setObjectName("GitHub_radioButton")
        self.GHProxy_radioButton = QRadioButton(self.DownloadPage)
        self.GHProxy_radioButton.setGeometry(QRect(350, 100, 101, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.GHProxy_radioButton.setFont(font)
        self.GHProxy_radioButton.setObjectName("GHProxy_radioButton")
        self.DownloadSwitcher_TabWidget = QTabWidget(self.DownloadPage)
        self.DownloadSwitcher_TabWidget.setGeometry(QRect(30, 150, 651, 411))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.DownloadSwitcher_TabWidget.setFont(font)
        self.DownloadSwitcher_TabWidget.setCursor(QCursor(Qt.ArrowCursor))
        self.DownloadSwitcher_TabWidget.setStyleSheet(
            "QTabWidget\n"
            "{\n"
            "    background-color:rgb(247, 247, 247);\n"
            "}\n"
            "QTabWidget::pane\n"
            "{\n"
            "    background-color: rgb(235, 235, 235);\n"
            "    border-top-right-radius: 8px;\n"
            "    border-bottom-right-radius: 8px;\n"
            "    border-bottom-left-radius: 8px;\n"
            "    border:none;\n"
            "}\n"
            "QTabBar::tab\n"
            "{\n"
            "    background-color:rgb(247, 247, 247);\n"
            "    border-top-left-radius: 7px;\n"
            "    border-top-right-radius: 7px;\n"
            "    min-width: 100px;\n"
            "    min-height: 20px;\n"
            "    padding: 8px;\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected\n"
            "{\n"
            "    background-color: rgb(235, 235, 235);\n"
            "}"
        )
        self.DownloadSwitcher_TabWidget.setTabPosition(QTabWidget.North)
        self.DownloadSwitcher_TabWidget.setElideMode(Qt.ElideMiddle)
        self.DownloadSwitcher_TabWidget.setUsesScrollButtons(False)
        self.DownloadSwitcher_TabWidget.setObjectName("DownloadSwitcher_TabWidget")
        self.JavaTab = QWidget()
        self.JavaTab.setObjectName("JavaTab")
        self.JavaScrollArea = QScrollArea(self.JavaTab)
        self.JavaScrollArea.setGeometry(QRect(10, 10, 631, 351))
        self.JavaScrollArea.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.JavaScrollArea.setStyleSheet(
            "QScrollArea{\n"
            "    border: 0px solid;\n"
            "    border-right-color: #dcdbdc;\n"
            "    background-color: transparent;\n"
            "}\n"
            "QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: transparent;\n"
            "    width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "    background: none;\n"
            "}"
        )
        self.JavaScrollArea.setFrameShape(QFrame.NoFrame)
        self.JavaScrollArea.setFrameShadow(QFrame.Plain)
        self.JavaScrollArea.setLineWidth(0)
        self.JavaScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.JavaScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.JavaScrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.JavaScrollArea.setWidgetResizable(True)
        self.JavaScrollArea.setObjectName("JavaScrollArea")
        self.JavaScrollAreaWidgetContents = QWidget()
        self.JavaScrollAreaWidgetContents.setGeometry(QRect(0, 0, 619, 351))
        self.JavaScrollAreaWidgetContents.setObjectName("JavaScrollAreaWidgetContents")
        self.verticalLayout_2 = QVBoxLayout(self.JavaScrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.JavaVerticalLayout = QVBoxLayout()
        self.JavaVerticalLayout.setObjectName("JavaVerticalLayout")
        self.verticalLayout_2.addLayout(self.JavaVerticalLayout)
        self.JavaScrollArea.setWidget(self.JavaScrollAreaWidgetContents)
        self.DownloadSwitcher_TabWidget.addTab(self.JavaTab, "")
        self.SpigotTab = QWidget()
        self.SpigotTab.setObjectName("SpigotTab")
        self.SpigotScrollArea = QScrollArea(self.SpigotTab)
        self.SpigotScrollArea.setGeometry(QRect(10, 10, 631, 351))
        self.SpigotScrollArea.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.SpigotScrollArea.setStyleSheet(
            "QScrollArea{\n"
            "    border: 0px solid;\n"
            "    border-right-color: #dcdbdc;\n"
            "    background-color: transparent;\n"
            "}\n"
            "QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: transparent;\n"
            "    width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "    background: none;\n"
            "}"
        )
        self.SpigotScrollArea.setFrameShape(QFrame.NoFrame)
        self.SpigotScrollArea.setFrameShadow(QFrame.Plain)
        self.SpigotScrollArea.setLineWidth(0)
        self.SpigotScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.SpigotScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SpigotScrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.SpigotScrollArea.setWidgetResizable(True)
        self.SpigotScrollArea.setObjectName("SpigotScrollArea")
        self.SpigotScrollAreaWidgetContents = QWidget()
        self.SpigotScrollAreaWidgetContents.setGeometry(QRect(0, 0, 619, 351))
        self.SpigotScrollAreaWidgetContents.setObjectName("SpigotScrollAreaWidgetContents")
        self.verticalLayout = QVBoxLayout(self.SpigotScrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.SpigotVerticalLayout = QVBoxLayout()
        self.SpigotVerticalLayout.setObjectName("SpigotVerticalLayout")
        self.verticalLayout.addLayout(self.SpigotVerticalLayout)
        self.SpigotScrollArea.setWidget(self.SpigotScrollAreaWidgetContents)
        self.DownloadSwitcher_TabWidget.addTab(self.SpigotTab, "")
        self.PaperTab = QWidget()
        self.PaperTab.setObjectName("PaperTab")
        self.PaperScrollArea = QScrollArea(self.PaperTab)
        self.PaperScrollArea.setGeometry(QRect(10, 10, 631, 351))
        self.PaperScrollArea.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.PaperScrollArea.setStyleSheet(
            "QScrollArea{\n"
            "    border: 0px solid;\n"
            "    border-right-color: #dcdbdc;\n"
            "    background-color: transparent;\n"
            "}\n"
            "QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: transparent;\n"
            "    width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "    background: none;\n"
            "}"
        )
        self.PaperScrollArea.setFrameShape(QFrame.NoFrame)
        self.PaperScrollArea.setFrameShadow(QFrame.Plain)
        self.PaperScrollArea.setLineWidth(0)
        self.PaperScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.PaperScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.PaperScrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.PaperScrollArea.setWidgetResizable(True)
        self.PaperScrollArea.setObjectName("PaperScrollArea")
        self.PaperScrollAreaWidgetContents = QWidget()
        self.PaperScrollAreaWidgetContents.setGeometry(QRect(0, 0, 619, 351))
        self.PaperScrollAreaWidgetContents.setObjectName("PaperScrollAreaWidgetContents")
        self.verticalLayout_3 = QVBoxLayout(self.PaperScrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.PaperVerticalLayout = QVBoxLayout()
        self.PaperVerticalLayout.setObjectName("PaperVerticalLayout")
        self.verticalLayout_3.addLayout(self.PaperVerticalLayout)
        self.PaperScrollArea.setWidget(self.PaperScrollAreaWidgetContents)
        self.DownloadSwitcher_TabWidget.addTab(self.PaperTab, "")
        self.BungeeCordTab = QWidget()
        self.BungeeCordTab.setObjectName("BungeeCordTab")
        self.BungeeCordScrollArea = QScrollArea(self.BungeeCordTab)
        self.BungeeCordScrollArea.setGeometry(QRect(10, 10, 631, 351))
        self.BungeeCordScrollArea.viewport().setProperty(
            "cursor", QCursor(Qt.ArrowCursor)
        )
        self.BungeeCordScrollArea.setStyleSheet(
            "QScrollArea{\n"
            "    border: 0px solid;\n"
            "    border-right-color: #dcdbdc;\n"
            "    background-color: transparent;\n"
            "}\n"
            "QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: transparent;\n"
            "    width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "    background: none;\n"
            "}"
        )
        self.BungeeCordScrollArea.setFrameShape(QFrame.NoFrame)
        self.BungeeCordScrollArea.setFrameShadow(QFrame.Plain)
        self.BungeeCordScrollArea.setLineWidth(0)
        self.BungeeCordScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.BungeeCordScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.BungeeCordScrollArea.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents
        )
        self.BungeeCordScrollArea.setWidgetResizable(True)
        self.BungeeCordScrollArea.setObjectName("BungeeCordScrollArea")
        self.BungeeCordScrollAreaWidgetContents = QWidget()
        self.BungeeCordScrollAreaWidgetContents.setGeometry(QRect(0, 0, 619, 351))
        self.BungeeCordScrollAreaWidgetContents.setObjectName("BungeeCordScrollAreaWidgetContents")
        self.verticalLayout_4 = QVBoxLayout(self.BungeeCordScrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.BCVerticalLayout = QVBoxLayout()
        self.BCVerticalLayout.setObjectName("BCVerticalLayout")
        self.verticalLayout_4.addLayout(self.BCVerticalLayout)
        self.BungeeCordScrollArea.setWidget(self.BungeeCordScrollAreaWidgetContents)
        self.DownloadSwitcher_TabWidget.addTab(self.BungeeCordTab, "")
        self.OfficialCoreTab = QWidget()
        self.OfficialCoreTab.setObjectName("OfficialCoreTab")
        self.OfficialCoreScrollArea = QScrollArea(self.OfficialCoreTab)
        self.OfficialCoreScrollArea.setGeometry(QRect(10, 10, 631, 351))
        self.OfficialCoreScrollArea.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.OfficialCoreScrollArea.setStyleSheet("QScrollArea{\n"
"    border: 0px solid;\n"
"    border-right-color: #dcdbdc;\n"
"    background-color: transparent;\n"
"}\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 12px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: rgb(220, 220, 220);\n"
"    min-height: 20px;\n"
"    border-radius: 5px;\n"
"}\n"
"QScrollBar::add-line:vertial \n"
"{    \n"
"    height: 0px;\n"
"}\n"
"QScrollBar::sub-line:vertial \n"
"{    \n"
"    height: 0px;\n"
"}\n"
"QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
"{    \n"
"    height: 0px;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.OfficialCoreScrollArea.setFrameShape(QFrame.NoFrame)
        self.OfficialCoreScrollArea.setFrameShadow(QFrame.Plain)
        self.OfficialCoreScrollArea.setLineWidth(0)
        self.OfficialCoreScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.OfficialCoreScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.OfficialCoreScrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.OfficialCoreScrollArea.setWidgetResizable(True)
        self.OfficialCoreScrollArea.setObjectName("OfficialCoreScrollArea")
        self.OfficialCoreScrollAreaWidgetContents = QWidget()
        self.OfficialCoreScrollAreaWidgetContents.setGeometry(QRect(0, 0, 619, 351))
        self.OfficialCoreScrollAreaWidgetContents.setObjectName("OfficialCoreScrollAreaWidgetContents")
        self.verticalLayout_5 = QVBoxLayout(self.OfficialCoreScrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.OfficialCoreVerticalLayout = QVBoxLayout()
        self.OfficialCoreVerticalLayout.setObjectName("OfficialCoreVerticalLayout")
        self.verticalLayout_5.addLayout(self.OfficialCoreVerticalLayout)
        self.OfficialCoreScrollArea.setWidget(self.OfficialCoreScrollAreaWidgetContents)
        self.DownloadSwitcher_TabWidget.addTab(self.OfficialCoreTab, "")
        self.More_Download_PushButton = QPushButton(self.DownloadPage)
        self.More_Download_PushButton.setGeometry(QRect(640, 140, 51, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.More_Download_PushButton.setFont(font)
        self.More_Download_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.More_Download_PushButton.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(230, 230, 230);\n"
"    border-radius: 7px;\n"
"}\n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(227, 227, 227);\n"
"    border-radius: 7px;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(225, 225, 225);\n"
"    border-radius: 7px;\n"
"}")
        self.More_Download_PushButton.setObjectName("More_Download_PushButton")
        self.FunctionsStackedWidget.addWidget(self.DownloadPage)
        self.ConsolePage = QWidget()
        self.ConsolePage.setObjectName("ConsolePage")
        self.Console_Label = QLabel(self.ConsolePage)
        self.Console_Label.setGeometry(QRect(30, 80, 221, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.Console_Label.setFont(font)
        self.Console_Label.setObjectName("Console_Label")
        self.Console_Background = QLabel(self.ConsolePage)
        self.Console_Background.setGeometry(QRect(30, 140, 651, 311))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Console_Background.setFont(font)
        self.Console_Background.setAutoFillBackground(False)
        self.Console_Background.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Console_Background.setText("")
        self.Console_Background.setObjectName("Console_Background")
        self.Command_Background = QLabel(self.ConsolePage)
        self.Command_Background.setGeometry(QRect(30, 470, 651, 51))
        font = QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Command_Background.setFont(font)
        self.Command_Background.setAutoFillBackground(False)
        self.Command_Background.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Command_Background.setObjectName("Command_Background")
        self.Send_Command_PushButton = QPushButton(self.ConsolePage)
        self.Send_Command_PushButton.setGeometry(QRect(570, 480, 91, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Send_Command_PushButton.setFont(font)
        self.Send_Command_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Send_Command_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(0, 110, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 100, 212);\n"
            "    border-radius: 6px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Send_Command_PushButton.setFlat(False)
        self.Send_Command_PushButton.setObjectName("Send_Command_PushButton")
        self.Command_LineEdit = QLineEdit(self.ConsolePage)
        self.Command_LineEdit.setGeometry(QRect(70, 480, 491, 31))
        font = QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.Command_LineEdit.setFont(font)
        self.Command_LineEdit.setStyleSheet(
            "QLineEdit\n" "{\n" "    border-radius: 3px;\n" "}\n" ""
        )
        self.Command_LineEdit.setObjectName("Command_LineEdit")
        self.FunctionsStackedWidget.addWidget(self.ConsolePage)
        self.ToolsPage = QWidget()
        self.ToolsPage.setObjectName("ToolsPage")
        self.Tools_Label = QLabel(self.ToolsPage)
        self.Tools_Label.setGeometry(QRect(30, 80, 141, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.Tools_Label.setFont(font)
        self.Tools_Label.setObjectName("Tools_Label")
        self.FunctionsStackedWidget.addWidget(self.ToolsPage)
        self.AboutPage = QWidget()
        self.AboutPage.setObjectName("AboutPage")
        self.About_Label = QLabel(self.AboutPage)
        self.About_Label.setGeometry(QRect(30, 80, 71, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.About_Label.setFont(font)
        self.About_Label.setObjectName("About_Label")
        self.About_Background = QLabel(self.AboutPage)
        self.About_Background.setGeometry(QRect(30, 140, 261, 231))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.About_Background.setFont(font)
        self.About_Background.setAutoFillBackground(False)
        self.About_Background.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.About_Background.setText("")
        self.About_Background.setObjectName("About_Background")
        self.MCSL2_Icon_Label = QLabel(self.AboutPage)
        self.MCSL2_Icon_Label.setGeometry(QRect(60, 170, 71, 71))
        self.MCSL2_Icon_Label.setText("")
        self.MCSL2_Icon_Label.setPixmap(QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"))
        self.MCSL2_Icon_Label.setScaledContents(True)
        self.MCSL2_Icon_Label.setObjectName("MCSL2_Icon_Label")
        self.MCSL2_Label = QLabel(self.AboutPage)
        self.MCSL2_Label.setGeometry(QRect(150, 180, 111, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.MCSL2_Label.setFont(font)
        self.MCSL2_Label.setObjectName("MCSL2_Label")
        self.MCSL2_Author_Label_1 = QLabel(self.AboutPage)
        self.MCSL2_Author_Label_1.setGeometry(QRect(150, 210, 111, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.MCSL2_Author_Label_1.setFont(font)
        self.MCSL2_Author_Label_1.setObjectName("MCSL2_Author_Label_1")
        self.MCSL2_Author_Avatar = QLabel(self.AboutPage)
        self.MCSL2_Author_Avatar.setGeometry(QRect(60, 270, 71, 71))
        self.MCSL2_Author_Avatar.setText("")
        self.MCSL2_Author_Avatar.setPixmap(QPixmap(":/MCSL2_Icon/MCSL2_Author.png"))
        self.MCSL2_Author_Avatar.setScaledContents(True)
        self.MCSL2_Author_Avatar.setObjectName("MCSL2_Author_Avatar")
        self.MCSL2_Author_Label_2 = QLabel(self.AboutPage)
        self.MCSL2_Author_Label_2.setGeometry(QRect(150, 280, 111, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.MCSL2_Author_Label_2.setFont(font)
        self.MCSL2_Author_Label_2.setObjectName("MCSL2_Author_Label_2")
        self.Description_Label = QLabel(self.AboutPage)
        self.Description_Label.setGeometry(QRect(310, 140, 381, 311))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Description_Label.setFont(font)
        self.Description_Label.setAutoFillBackground(False)
        self.Description_Label.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Description_Label.setObjectName("Description_Label")
        self.Check_Update_PushButton = QPushButton(self.AboutPage)
        self.Check_Update_PushButton.setGeometry(QRect(30, 390, 261, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.Check_Update_PushButton.setFont(font)
        self.Check_Update_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Check_Update_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:hover\n"
            "{\n"
            "    background-color: rgb(230, 230, 230);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(225, 225, 225);\n"
            "    border-radius: 7px;\n"
            "}"
        )
        self.Check_Update_PushButton.setObjectName("Check_Update_PushButton")
        self.FunctionsStackedWidget.addWidget(self.AboutPage)
        self.ChooseServerPage = QWidget()
        self.ChooseServerPage.setObjectName("ChooseServerPage")
        self.Choose_Server_Label = QLabel(self.ChooseServerPage)
        self.Choose_Server_Label.setGeometry(QRect(30, 80, 171, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.Choose_Server_Label.setFont(font)
        self.Choose_Server_Label.setObjectName("Choose_Server_Label")
        self.Choose_Server_ComboBox = QComboBox(self.ChooseServerPage)
        self.Choose_Server_ComboBox.setGeometry(QRect(220, 320, 411, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.Choose_Server_ComboBox.setFont(font)
        self.Choose_Server_ComboBox.setStyleSheet(
            "QComboBox {\n"
            "    border-radius: 3px;\n"
            "    padding: 1px 2px 1px 2px;\n"
            "    min-width: 9em;\n"
            "    border: 2px solid rgb(223, 223, 223);\n"
            "}\n"
            "QComboBox::drop-down\n"
            "{\n"
            "    subcontrol-origin: padding;\n"
            "    subcontrol-position: top right;\n"
            "    width: 20px;\n"
            "    border-left-color: rgb(223, 223, 223);\n"
            "    border-left-style: solid;\n"
            "    border-top-right-radius: 4px;\n"
            "    border-bottom-right-radius: 4px;\n"
            "}\n"
            "QComboBox::down-arrow\n"
            "{\n"
            "    border-image: url(:/MCSL2_Icon/QComboBox.png);\n"
            "}\n"
            "QComboBox QAbstractItemView\n"
            "{\n"
            "    border-radius: 10px;\n"
            "    background: rgba(255,255,255,1);\n"
            "    border: 1px solid rgba(228,228,228,1);\n"
            "    border-radius: 0px 0px 5px 5px;\n"
            "    font-size: 14px;\n"
            "    outline: 0px;\n"
            "}\n"
            "QComboBox QAbstractItemView::item\n"
            "{\n"
            "    border-radius: 7px;\n"
            "    font-size:25px;\n"
            "    color:#666667;\n"
            "    padding-left:9px;\n"
            "    background-color:#FFFFFF;\n"
            "    min-height: 33px;\n"
            "    min-width: 60px;\n"
            "}\n"
            "QComboBox QAbstractItemView::item:hover\n"
            "{\n"
            "    border-radius: 7px;\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    color:#FFFFFF;\n"
            "}\n"
            ""
        )
        self.Choose_Server_ComboBox.setObjectName("Choose_Server_ComboBox")
        self.Choose_Server_ComboBox.addItem("")
        self.Choose_Server_Label2 = QLabel(self.ChooseServerPage)
        self.Choose_Server_Label2.setGeometry(QRect(60, 320, 141, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.Choose_Server_Label2.setFont(font)
        self.Choose_Server_Label2.setObjectName("Choose_Server_Label2")
        self.Choose_Server_Background = QLabel(self.ChooseServerPage)
        self.Choose_Server_Background.setGeometry(QRect(30, 280, 651, 111))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Choose_Server_Background.setFont(font)
        self.Choose_Server_Background.setAutoFillBackground(False)
        self.Choose_Server_Background.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Choose_Server_Background.setText("")
        self.Choose_Server_Background.setObjectName("Choose_Server_Background")
        self.Completed_Choose_Server_PushButton = QPushButton(self.ChooseServerPage)
        self.Completed_Choose_Server_PushButton.setGeometry(QRect(560, 510, 121, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.Completed_Choose_Server_PushButton.setFont(font)
        self.Completed_Choose_Server_PushButton.setCursor(
            QCursor(Qt.PointingHandCursor)
        )
        self.Completed_Choose_Server_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 8px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 107, 212);\n"
            "    border-radius: 8px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Completed_Choose_Server_PushButton.setFlat(False)
        self.Completed_Choose_Server_PushButton.setObjectName(
            "Completed_Choose_Server_PushButton"
        )
        self.Choose_Server_Tip1_Widget = QWidget(self.ChooseServerPage)
        self.Choose_Server_Tip1_Widget.setGeometry(QRect(30, 140, 651, 81))
        self.Choose_Server_Tip1_Widget.setStyleSheet(
            "QWidget\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Choose_Server_Tip1_Widget.setObjectName("Choose_Server_Tip1_Widget")
        self.Choose_Server_Tip1_Label = QLabel(self.Choose_Server_Tip1_Widget)
        self.Choose_Server_Tip1_Label.setGeometry(QRect(20, 0, 601, 71))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Choose_Server_Tip1_Label.setFont(font)
        self.Choose_Server_Tip1_Label.setAutoFillBackground(False)
        self.Choose_Server_Tip1_Label.setStyleSheet("")
        self.Choose_Server_Tip1_Label.setObjectName("Choose_Server_Tip1_Label")
        self.ChooseServerScrollArea = QScrollArea(self.ChooseServerPage)
        self.ChooseServerScrollArea.setGeometry(QRect(30, 240, 651, 251))
        self.ChooseServerScrollArea.viewport().setProperty(
            "cursor", QCursor(Qt.ArrowCursor)
        )
        self.ChooseServerScrollArea.setStyleSheet(
            "QScrollArea{\n"
            "    border: 0px solid;\n"
            "    border-right-color: #dcdbdc;\n"
            "    background-color: rgb(230, 230, 230);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: transparent;\n"
            "    width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "    background: none;\n"
            "}"
        )
        self.ChooseServerScrollArea.setFrameShape(QFrame.NoFrame)
        self.ChooseServerScrollArea.setFrameShadow(QFrame.Plain)
        self.ChooseServerScrollArea.setLineWidth(0)
        self.ChooseServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ChooseServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ChooseServerScrollArea.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents
        )
        self.ChooseServerScrollArea.setWidgetResizable(True)
        self.ChooseServerScrollArea.setObjectName("ChooseServerScrollArea")
        self.ChooseServerScrollAreaWidgetContents = QWidget()
        self.ChooseServerScrollAreaWidgetContents.setGeometry(QRect(0, 0, 639, 251))
        self.ChooseServerScrollAreaWidgetContents.setObjectName(
            "ChooseServerScrollAreaWidgetContents"
        )
        self.ChooseServerScrollArea.setWidget(self.ChooseServerScrollAreaWidgetContents)
        self.FunctionsStackedWidget.addWidget(self.ChooseServerPage)
        self.ChooseJavaPage = QWidget()
        self.ChooseJavaPage.setObjectName("ChooseJavaPage")
        self.Choose_Java_Label = QLabel(self.ChooseJavaPage)
        self.Choose_Java_Label.setGeometry(QRect(30, 80, 171, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.Choose_Java_Label.setFont(font)
        self.Choose_Java_Label.setObjectName("Choose_Java_Label")
        self.Completed_Choose_Java_PushButton = QPushButton(self.ChooseJavaPage)
        self.Completed_Choose_Java_PushButton.setGeometry(QRect(560, 490, 121, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.Completed_Choose_Java_PushButton.setFont(font)
        self.Completed_Choose_Java_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Completed_Choose_Java_PushButton.setStyleSheet(
            "QPushButton\n"
            "{\n"
            "    background-color: rgb(0, 120, 212);\n"
            "    border-radius: 8px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "QPushButton:pressed\n"
            "{\n"
            "    background-color: rgb(0, 107, 212);\n"
            "    border-radius: 8px;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.Completed_Choose_Java_PushButton.setFlat(False)
        self.Completed_Choose_Java_PushButton.setObjectName(
            "Completed_Choose_Java_PushButton"
        )
        self.ChooseJavaScrollArea = QScrollArea(self.ChooseJavaPage)
        self.ChooseJavaScrollArea.setGeometry(QRect(40, 150, 631, 321))
        self.ChooseJavaScrollArea.viewport().setProperty(
            "cursor", QCursor(Qt.ArrowCursor)
        )
        self.ChooseJavaScrollArea.setStyleSheet(
            "QScrollArea{\n"
            "    border: 0px solid;\n"
            "    border-right-color: #dcdbdc;\n"
            "    background-color: transparent;\n"
            "}\n"
            "QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: transparent;\n"
            "    width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    height: 0px;\n"
            "}\n"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "    background: none;\n"
            "}"
        )
        self.ChooseJavaScrollArea.setFrameShape(QFrame.NoFrame)
        self.ChooseJavaScrollArea.setFrameShadow(QFrame.Plain)
        self.ChooseJavaScrollArea.setLineWidth(0)
        self.ChooseJavaScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ChooseJavaScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ChooseJavaScrollArea.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents
        )
        self.ChooseJavaScrollArea.setWidgetResizable(True)
        self.ChooseJavaScrollArea.setObjectName("ChooseJavaScrollArea")
        self.ChooseJavaScrollAreaWidgetContents = QWidget()
        self.ChooseJavaScrollAreaWidgetContents.setGeometry(QRect(0, 0, 619, 321))
        self.ChooseJavaScrollAreaWidgetContents.setObjectName(
            "ChooseJavaScrollAreaWidgetContents"
        )
        self.ChooseJavaScrollArea.setWidget(self.ChooseJavaScrollAreaWidgetContents)
        self.FunctionsStackedWidget.addWidget(self.ChooseJavaPage)
        self.UpdatePage = QWidget()
        self.UpdatePage.setObjectName("UpdatePage")
        self.Update_Label = QLabel(self.UpdatePage)
        self.Update_Label.setGeometry(QRect(30, 80, 171, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.Update_Label.setFont(font)
        self.Update_Label.setObjectName("Update_Label")
        self.Update_Tip1_Widget = QWidget(self.UpdatePage)
        self.Update_Tip1_Widget.setGeometry(QRect(30, 140, 651, 81))
        self.Update_Tip1_Widget.setStyleSheet("QWidget\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.Update_Tip1_Widget.setObjectName("Update_Tip1_Widget")
        self.Update_Tip1_Label = QLabel(self.Update_Tip1_Widget)
        self.Update_Tip1_Label.setGeometry(QRect(20, 10, 601, 61))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Update_Tip1_Label.setFont(font)
        self.Update_Tip1_Label.setAutoFillBackground(False)
        self.Update_Tip1_Label.setStyleSheet("")
        self.Update_Tip1_Label.setObjectName("Update_Tip1_Label")
        self.DoNotUpdate_PushButton = QPushButton(self.UpdatePage)
        self.DoNotUpdate_PushButton.setGeometry(QRect(340, 490, 101, 61))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.DoNotUpdate_PushButton.setFont(font)
        self.DoNotUpdate_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.DoNotUpdate_PushButton.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 7px;\n"
"}\n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(230, 230, 230);\n"
"    border-radius: 7px;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(225, 225, 225);\n"
"    border-radius: 7px;\n"
"}")
        self.DoNotUpdate_PushButton.setObjectName("DoNotUpdate_PushButton")
        self.Update_PushButton = QPushButton(self.UpdatePage)
        self.Update_PushButton.setGeometry(QRect(450, 490, 231, 61))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(16)
        self.Update_PushButton.setFont(font)
        self.Update_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Update_PushButton.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(0, 120, 212);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(0, 110, 212);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(0, 100, 212);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.Update_PushButton.setFlat(False)
        self.Update_PushButton.setObjectName("Update_PushButton")
        self.Update_Introduction_Widget = QWidget(self.UpdatePage)
        self.Update_Introduction_Widget.setGeometry(QRect(30, 230, 651, 221))
        self.Update_Introduction_Widget.setStyleSheet("QWidget\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.Update_Introduction_Widget.setObjectName("Update_Introduction_Widget")
        self.Update_Introduction_Title_Label = QLabel(self.Update_Introduction_Widget)
        self.Update_Introduction_Title_Label.setGeometry(QRect(20, 20, 601, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Update_Introduction_Title_Label.setFont(font)
        self.Update_Introduction_Title_Label.setAutoFillBackground(False)
        self.Update_Introduction_Title_Label.setStyleSheet("")
        self.Update_Introduction_Title_Label.setObjectName("Update_Introduction_Title_Label")
        self.Update_Introduction_Label = QLabel(self.Update_Introduction_Widget)
        self.Update_Introduction_Label.setGeometry(QRect(20, 60, 601, 141))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Update_Introduction_Label.setFont(font)
        self.Update_Introduction_Label.setAutoFillBackground(False)
        self.Update_Introduction_Label.setStyleSheet("")
        self.Update_Introduction_Label.setText("")
        self.Update_Introduction_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.Update_Introduction_Label.setObjectName("Update_Introduction_Label")
        self.FunctionsStackedWidget.addWidget(self.UpdatePage)
        self.Background = QLabel(self.CentralWidget)
        self.Background.setGeometry(QRect(0, 0, 211, 581))
        self.Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px\n"
"}")
        self.Background.setText("")
        self.Background.setObjectName("Background")
        self.Background_2 = QLabel(self.CentralWidget)
        self.Background_2.setGeometry(QRect(120, 0, 821, 581))
        self.Background_2.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgba(255, 255, 255,82%);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Background_2.setText("")
        self.Background_2.setObjectName("Background_2")
        self.Background_2.raise_()
        self.Background.raise_()
        self.OptionsWidget.raise_()
        self.FunctionsStackedWidget.raise_()
        MCSL2_MainWindow.setCentralWidget(self.CentralWidget)
        self.retranslateUi(MCSL2_MainWindow)
        self.FunctionsStackedWidget.setCurrentIndex(0)
        self.DownloadSwitcher_TabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MCSL2_MainWindow)

    def retranslateUi(self, MCSL2_MainWindow):
        _translate = QCoreApplication.translate
        MCSL2_MainWindow.setWindowTitle(_translate("MCSL2_MainWindow", "MCSL 2"))
        self.Home_Page_PushButton.setText(_translate("MCSL2_MainWindow", "主页"))
        self.Config_Page_PushButton.setText(_translate("MCSL2_MainWindow", "配置服务器"))
        self.MCSL2_Title_Label.setText(_translate("MCSL2_MainWindow", "MCSL 2"))
        self.MCSL2_Title_Author_Label.setText(
            _translate("MCSL2_MainWindow", "by LxHTT")
        )
        self.Download_Page_PushButton.setText(_translate("MCSL2_MainWindow", "下载"))
        self.Server_Console_Page_PushButton.setText(
            _translate("MCSL2_MainWindow", "服务器控制台")
        )
        self.Tools_Page_PushButton.setText(_translate("MCSL2_MainWindow", "更多工具"))
        self.About_Page_PushButton.setText(_translate("MCSL2_MainWindow", "关于"))
        self.Home_Label.setText(_translate("MCSL2_MainWindow", "主页"))
        self.Notice_Label.setText(_translate("MCSL2_MainWindow", "正在获取公告..."))
        self.HomeTip1_Label.setText(
            _translate(
                "MCSL2_MainWindow",
                "如何搭建一个Java版Minecraft服务器？\n"
                "1.准备好Java、核心、电脑\n"
                "（提示：可使用本程序下载）\n"
                "2.配置参数（本程序“配置服务器”页）\n"
                "3. 开启服务器。将服务器IP告诉玩家。",
            )
        )
        self.Selected_Server_Label.setText(_translate("MCSL2_MainWindow", "未选择服务器！"))
        self.Start_PushButton.setText(_translate("MCSL2_MainWindow", "启动服务器"))
        self.Config_PushButton.setText(_translate("MCSL2_MainWindow", "配置"))
        self.Choose_Server_PushButton.setText(_translate("MCSL2_MainWindow", "选择"))
        self.Config_Label.setText(_translate("MCSL2_MainWindow", "配置服务器"))
        self.Server_Name_Label.setText(_translate("MCSL2_MainWindow", "服务器名称："))
        self.Completed_Save_PushButton.setText(_translate("MCSL2_MainWindow", "保存"))
        self.ConfigTip1_Label.setText(
            _translate(
                "MCSL2_MainWindow",
                "一个服务器最基础的三个部件\n" "1.存放的文件夹路径\n" "2.服务器核心\n" "3.Java路径",
            )
        )
        self.ConfigTip2_Label.setText(
            _translate(
                "MCSL2_MainWindow", "MCSL 2将会在程序目录生成\n" "以服务器名称命名的文件夹\n" "以存储服务器文件。"
            )
        )
        self.Download_Core_PushButton.setText(_translate("MCSL2_MainWindow", "下载核心"))
        self.Download_Java_PushButton.setText(_translate("MCSL2_MainWindow", "下载Java"))
        self.Manual_Import_Core_PushButton.setText(
            _translate("MCSL2_MainWindow", "手动导入")
        )
        self.Memory_1_Label.setText(_translate("MCSL2_MainWindow", "内存："))
        self.ConfigTip3_Label.setText(
            _translate(
                "MCSL2_MainWindow",
                "MCSL 2会把核心复制到文件夹中。当然，\n" "你也可以自己复制，并重命名为server.jar。",
            )
        )
        self.Java_Label.setText(_translate("MCSL2_MainWindow", "Java:"))
        self.Memory_2_Label.setText(_translate("MCSL2_MainWindow", "~"))
        self.Core_Label.setText(_translate("MCSL2_MainWindow", "服务器核心："))
        self.Auto_Find_Java_PushButton.setText(_translate("MCSL2_MainWindow", "自动查找"))
        self.Memory_Unit_Label.setText(_translate("MCSL2_MainWindow", "MB"))
        self.Founded_Java_List_PushButton.setText(
            _translate("MCSL2_MainWindow", "Java列表")
        )
        self.Download_Label.setText(_translate("MCSL2_MainWindow", "下载"))
        self.Download_Source_Label.setText(_translate("MCSL2_MainWindow", "下载源："))
        self.luoxisCloud_radioButton.setText(_translate("MCSL2_MainWindow", "luoxis云"))
        self.Gitee_radioButton.setText(_translate("MCSL2_MainWindow", "Gitee"))
        self.SharePoint_radioButton.setText(
            _translate("MCSL2_MainWindow", "SharePoint")
        )
        self.GitHub_radioButton.setText(_translate("MCSL2_MainWindow", "GitHub"))
        self.GHProxy_radioButton.setText(_translate("MCSL2_MainWindow", "GHProxy"))
        self.DownloadSwitcher_TabWidget.setTabText(self.DownloadSwitcher_TabWidget.indexOf(self.JavaTab), _translate("MCSL2_MainWindow", "[ 运行环境 ] Java"))
        self.DownloadSwitcher_TabWidget.setTabText(self.DownloadSwitcher_TabWidget.indexOf(self.SpigotTab), _translate("MCSL2_MainWindow", "[ 核心 ] Spigot"))
        self.DownloadSwitcher_TabWidget.setTabText(self.DownloadSwitcher_TabWidget.indexOf(self.PaperTab), _translate("MCSL2_MainWindow", "[ 核心 ] Paper"))
        self.DownloadSwitcher_TabWidget.setTabText(self.DownloadSwitcher_TabWidget.indexOf(self.BungeeCordTab), _translate("MCSL2_MainWindow", "[ 核心 ] BungeeCord"))
        self.DownloadSwitcher_TabWidget.setTabText(self.DownloadSwitcher_TabWidget.indexOf(self.OfficialCoreTab), _translate("MCSL2_MainWindow", "[ 核心 ] 官方"))
        self.More_Download_PushButton.setText(_translate("MCSL2_MainWindow", "更多"))
        self.Console_Label.setText(_translate("MCSL2_MainWindow", "服务器控制台"))
        self.Command_Background.setText(_translate("MCSL2_MainWindow", "  >"))
        self.Send_Command_PushButton.setText(_translate("MCSL2_MainWindow", "发送"))
        self.Tools_Label.setText(_translate("MCSL2_MainWindow", "更多工具"))
        self.About_Label.setText(_translate("MCSL2_MainWindow", "关于"))
        self.MCSL2_Label.setText(_translate("MCSL2_MainWindow", "MCSL 2"))
        self.MCSL2_Author_Label_1.setText(_translate("MCSL2_MainWindow", "by LxHTT"))
        self.MCSL2_Author_Label_2.setText(_translate("MCSL2_MainWindow", "Bilibili：\n"
"落雪无痕LxHTT"))
        self.Description_Label.setText(_translate("MCSL2_MainWindow", "    这是对MCSL的Remake。 \n"
"\n"
"    本来使用C#开发，但由于知识有限，无奈继续\n"
"\n"
"    使用Python。 \n"
"\n"
"    MCSL 2 重构UI，使用更加清晰的代码逻辑开发，\n"
"\n"
"    除了启动、配置、下载以外，添加了诸多拓展工具。 \n"
"\n"
"    遇到Bug，请积极反馈，以帮助改进MCSL 2。 \n"
"\n"
"    作者邮箱: lxhtz.dl@qq.com "))
        self.Check_Update_PushButton.setText(_translate("MCSL2_MainWindow", "检查更新"))
        self.Choose_Server_Label.setText(_translate("MCSL2_MainWindow", "选择服务器"))
        self.Completed_Choose_Server_PushButton.setText(_translate("MCSL2_MainWindow", "选好了"))
        self.Choose_Server_Tip1_Label.setText(_translate("MCSL2_MainWindow", "MCSL 2存放服务器数据的路径位于MCSL 2根目录以服务器名称命名的文件夹。\n"
"MCSL 2将会读取目录下的文件夹名称以确定一个服务器。"))
        self.Choose_Java_Label.setText(_translate("MCSL2_MainWindow", "选择Java"))
        self.Completed_Choose_Java_PushButton.setText(_translate("MCSL2_MainWindow", "选好了"))
        self.Update_Label.setText(_translate("MCSL2_MainWindow", "程序更新"))
        self.Update_Tip1_Label.setText(_translate("MCSL2_MainWindow", "MCSL 2发布新版本啦！你想更新吗？"))
        self.DoNotUpdate_PushButton.setText(_translate("MCSL2_MainWindow", "丑拒"))
        self.Update_PushButton.setText(_translate("MCSL2_MainWindow", "火速更新"))
        self.Update_Introduction_Title_Label.setText(_translate("MCSL2_MainWindow", "这是最新版本的说明："))


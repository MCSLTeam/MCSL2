from PyQt5.QtCore import QCoreApplication, QRect, Qt, QSize, QMetaObject
from PyQt5.QtGui import QCursor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QAbstractScrollArea,
    QComboBox,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget, QCheckBox, QSizePolicy, QSlider, QCommandLinkButton, QTextEdit,
)


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
        MCSL2_MainWindow.setFixedSize(962, 601)  # Make the size of window unchangeable.
        self.CentralWidget = QWidget(MCSL2_MainWindow)
        self.CentralWidget.setObjectName("CentralWidget")
        self.OptionsWidget = QWidget(self.CentralWidget)
        self.OptionsWidget.setGeometry(QRect(10, 10, 211, 581))
        self.OptionsWidget.setObjectName("OptionsWidget")
        self.Close_PushButton = QPushButton(self.OptionsWidget)
        self.Close_PushButton.setGeometry(QRect(20, 20, 22, 22))
        self.Close_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Close_PushButton.setStyleSheet("QPushButton\n"
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
                                            "}")
        self.Close_PushButton.setText("")
        self.Close_PushButton.setObjectName("Close_PushButton")
        self.Minimize_PushButton = QPushButton(self.OptionsWidget)
        self.Minimize_PushButton.setGeometry(QRect(50, 20, 22, 22))
        self.Minimize_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Minimize_PushButton.setStyleSheet("QPushButton\n"
                                               "{\n"
                                               "    background-color: rgb(225, 225, 0);\n"
                                               "    border-radius: 11px;\n"
                                               "}\n"
                                               "QPushButton:hover\n"
                                               "{\n"
                                               "    background-color: rgb(183, 161, 0);\n"
                                               "    border-radius: 11px;\n"
                                               "}\n"
                                               "QPushButton:pressed\n"
                                               "{\n"
                                               "    background-color: rgb(161, 161, 0);\n"
                                               "    border-radius: 11px;\n"
                                               "}")
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
        self.Home_Page_PushButton.setStyleSheet("QPushButton\n"
                                                "{\n"
                                                "    text-align: left;\n"
                                                "    background-color: rgb(247, 247, 247);\n"
                                                "    border-radius: 7px;\n"
                                                "}\n"
                                                "QPushButton:hover\n"
                                                "{\n"
                                                "    text-align: left;\n"
                                                "    background-color: rgb(243, 243, 243);\n"
                                                "    border-radius: 7px;\n"
                                                "}\n"
                                                "QPushButton:pressed\n"
                                                "{\n"
                                                "    text-align: left;\n"
                                                "    background-color: rgb(233, 233, 233);\n"
                                                "    border-radius: 7px;\n"
                                                "}")
        self.Home_Page_PushButton.setCheckable(False)
        self.Home_Page_PushButton.setChecked(False)
        self.Home_Page_PushButton.setAutoExclusive(False)
        self.Home_Page_PushButton.setFlat(False)
        self.Home_Page_PushButton.setObjectName("Home_Page_PushButton")
        self.Config_Page_PushButton = QPushButton(self.OptionsWidget)
        self.Config_Page_PushButton.setEnabled(True)
        self.Config_Page_PushButton.setGeometry(QRect(20, 200, 171, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.Config_Page_PushButton.setFont(font)
        self.Config_Page_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Config_Page_PushButton.setStyleSheet("QPushButton\n"
                                                  "{\n"
                                                  "    text-align: left;\n"
                                                  "    background-color: rgb(255, 255, 255);\n"
                                                  "    border-radius: 7px;\n"
                                                  "}\n"
                                                  "QPushButton:hover\n"
                                                  "{\n"
                                                  "    text-align: left;\n"
                                                  "    background-color: rgb(243, 243, 243);\n"
                                                  "    border-radius: 7px;\n"
                                                  "}\n"
                                                  "QPushButton:pressed\n"
                                                  "{\n"
                                                  "    text-align: left;\n"
                                                  "    background-color: rgb(233, 233, 233);\n"
                                                  "    border-radius: 7px;\n"
                                                  "}")
        self.Config_Page_PushButton.setCheckable(False)
        self.Config_Page_PushButton.setChecked(False)
        self.Config_Page_PushButton.setAutoExclusive(False)
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
        self.Download_Page_PushButton.setStyleSheet("QPushButton\n"
                                                    "{\n"
                                                    "    text-align: left;\n"
                                                    "    background-color: rgb(255, 255, 255);\n"
                                                    "    border-radius: 7px;\n"
                                                    "}\n"
                                                    "QPushButton:hover\n"
                                                    "{\n"
                                                    "    text-align: left;\n"
                                                    "    background-color: rgb(243, 243, 243);\n"
                                                    "    border-radius: 7px;\n"
                                                    "}\n"
                                                    "QPushButton:pressed\n"
                                                    "{\n"
                                                    "    text-align: left;\n"
                                                    "    background-color: rgb(233, 233, 233);\n"
                                                    "    border-radius: 7px;\n"
                                                    "}")
        self.Download_Page_PushButton.setCheckable(False)
        self.Download_Page_PushButton.setChecked(False)
        self.Download_Page_PushButton.setAutoExclusive(False)
        self.Download_Page_PushButton.setObjectName("Download_Page_PushButton")
        self.Server_Console_Page_PushButton = QPushButton(self.OptionsWidget)
        self.Server_Console_Page_PushButton.setEnabled(True)
        self.Server_Console_Page_PushButton.setGeometry(QRect(20, 320, 171, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.Server_Console_Page_PushButton.setFont(font)
        self.Server_Console_Page_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Server_Console_Page_PushButton.setStyleSheet("QPushButton\n"
                                                          "{\n"
                                                          "    text-align: left;\n"
                                                          "    background-color: rgb(255, 255, 255);\n"
                                                          "    border-radius: 7px;\n"
                                                          "}\n"
                                                          "QPushButton:hover\n"
                                                          "{\n"
                                                          "    text-align: left;\n"
                                                          "    background-color: rgb(243, 243, 243);\n"
                                                          "    border-radius: 7px;\n"
                                                          "}\n"
                                                          "QPushButton:pressed\n"
                                                          "{\n"
                                                          "    text-align: left;\n"
                                                          "    background-color: rgb(233, 233, 233);\n"
                                                          "    border-radius: 7px;\n"
                                                          "}")
        self.Server_Console_Page_PushButton.setCheckable(False)
        self.Server_Console_Page_PushButton.setChecked(False)
        self.Server_Console_Page_PushButton.setAutoExclusive(False)
        self.Server_Console_Page_PushButton.setObjectName("Server_Console_Page_PushButton")
        self.Tools_Page_PushButton = QPushButton(self.OptionsWidget)
        self.Tools_Page_PushButton.setEnabled(True)
        self.Tools_Page_PushButton.setGeometry(QRect(20, 380, 171, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.Tools_Page_PushButton.setFont(font)
        self.Tools_Page_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Tools_Page_PushButton.setStyleSheet("QPushButton\n"
                                                 "{\n"
                                                 "    text-align: left;\n"
                                                 "    background-color: rgb(255, 255, 255);\n"
                                                 "    border-radius: 7px;\n"
                                                 "}\n"
                                                 "QPushButton:hover\n"
                                                 "{\n"
                                                 "    text-align: left;\n"
                                                 "    background-color: rgb(243, 243, 243);\n"
                                                 "    border-radius: 7px;\n"
                                                 "}\n"
                                                 "QPushButton:pressed\n"
                                                 "{\n"
                                                 "    text-align: left;\n"
                                                 "    background-color: rgb(233, 233, 233);\n"
                                                 "    border-radius: 7px;\n"
                                                 "}")
        self.Tools_Page_PushButton.setCheckable(False)
        self.Tools_Page_PushButton.setChecked(False)
        self.Tools_Page_PushButton.setAutoExclusive(False)
        self.Tools_Page_PushButton.setObjectName("Tools_Page_PushButton")
        self.About_Page_PushButton = QPushButton(self.OptionsWidget)
        self.About_Page_PushButton.setEnabled(True)
        self.About_Page_PushButton.setGeometry(QRect(20, 440, 171, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(13)
        self.About_Page_PushButton.setFont(font)
        self.About_Page_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.About_Page_PushButton.setStyleSheet("QPushButton\n"
                                                 "{\n"
                                                 "    text-align: left;\n"
                                                 "    background-color: rgb(255, 255, 255);\n"
                                                 "    border-radius: 7px;\n"
                                                 "}\n"
                                                 "QPushButton:hover\n"
                                                 "{\n"
                                                 "    text-align: left;\n"
                                                 "    background-color: rgb(243, 243, 243);\n"
                                                 "    border-radius: 7px;\n"
                                                 "}\n"
                                                 "QPushButton:pressed\n"
                                                 "{\n"
                                                 "    text-align: left;\n"
                                                 "    background-color: rgb(233, 233, 233);\n"
                                                 "    border-radius: 7px;\n"
                                                 "}")
        self.About_Page_PushButton.setCheckable(False)
        self.About_Page_PushButton.setChecked(False)
        self.About_Page_PushButton.setAutoExclusive(False)
        self.About_Page_PushButton.setObjectName("About_Page_PushButton")
        self.Blue1 = QLabel(self.OptionsWidget)
        self.Blue1.setEnabled(True)
        self.Blue1.setVisible(True)
        self.Blue1.setGeometry(QRect(45, 150, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue1.setFont(font)
        self.Blue1.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.Blue2.setGeometry(QRect(45, 210, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue2.setFont(font)
        self.Blue2.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.Blue3.setGeometry(QRect(45, 270, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue3.setFont(font)
        self.Blue3.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.Blue4.setGeometry(QRect(45, 330, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue4.setFont(font)
        self.Blue4.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.Blue5.setGeometry(QRect(45, 390, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue5.setFont(font)
        self.Blue5.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.Blue6.setGeometry(QRect(45, 450, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Blue6.setFont(font)
        self.Blue6.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.FunctionsStackedWidget.setGeometry(QRect(210, -10, 731, 601))
        self.FunctionsStackedWidget.setAutoFillBackground(False)
        self.FunctionsStackedWidget.setFrameShape(QFrame.NoFrame)
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
        self.HomeTip1_Widget.setStyleSheet("QWidget\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
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
        self.ConfigModeWidget = QStackedWidget(self.ConfigPage)
        self.ConfigModeWidget.setGeometry(QRect(30, 140, 670, 451))
        self.ConfigModeWidget.setFrameShadow(QFrame.Plain)
        self.ConfigModeWidget.setLineWidth(1)
        self.ConfigModeWidget.setObjectName("ConfigModeWidget")
        self.LeadCPage = QWidget()
        self.LeadCPage.setObjectName("LeadCPage")
        self.LeadConfigTip1 = QLabel(self.LeadCPage)
        self.LeadConfigTip1.setGeometry(QRect(215, 100, 240, 40))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.LeadConfigTip1.setFont(font)
        self.LeadConfigTip1.setAutoFillBackground(False)
        self.LeadConfigTip1.setStyleSheet("")
        self.LeadConfigTip1.setObjectName("LeadConfigTip1")
        self.NoobAddServer = QCommandLinkButton(self.LeadCPage)
        self.NoobAddServer.setGeometry(QRect(30, 210, 190, 50))
        self.NoobAddServer.setMinimumSize(QSize(190, 50))
        self.NoobAddServer.setMaximumSize(QSize(190, 50))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.NoobAddServer.setFont(font)
        self.NoobAddServer.setCursor(QCursor(Qt.PointingHandCursor))
        self.NoobAddServer.setAutoFillBackground(False)
        self.NoobAddServer.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 7px;\n"
"    font: 14px \'Microsoft YaHei UI\';\n"
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
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/MCSL2_Icon/QuickStart.svg"), QIcon.Normal, QIcon.Off)
        icon1.addPixmap(QPixmap(":/MCSL2_Icon/QuickStart.svg"), QIcon.Normal, QIcon.On)
        icon1.addPixmap(QPixmap(":/MCSL2_Icon/QuickStart.svg"), QIcon.Disabled, QIcon.Off)
        icon1.addPixmap(QPixmap(":/MCSL2_Icon/QuickStart.svg"), QIcon.Disabled, QIcon.On)
        icon1.addPixmap(QPixmap(":/MCSL2_Icon/QuickStart.svg"), QIcon.Active, QIcon.Off)
        icon1.addPixmap(QPixmap(":/MCSL2_Icon/QuickStart.svg"), QIcon.Active, QIcon.On)
        icon1.addPixmap(QPixmap(":/MCSL2_Icon/QuickStart.svg"), QIcon.Selected, QIcon.Off)
        icon1.addPixmap(QPixmap(":/MCSL2_Icon/QuickStart.svg"), QIcon.Selected, QIcon.On)
        self.NoobAddServer.setIcon(icon1)
        self.NoobAddServer.setIconSize(QSize(30, 30))
        self.NoobAddServer.setCheckable(True)
        self.NoobAddServer.setChecked(False)
        self.NoobAddServer.setAutoDefault(True)
        self.NoobAddServer.setDefault(True)
        self.NoobAddServer.setDescription("")
        self.NoobAddServer.setObjectName("NoobAddServer")
        self.ExAddServer = QCommandLinkButton(self.LeadCPage)
        self.ExAddServer.setGeometry(QRect(240, 210, 190, 50))
        self.ExAddServer.setMinimumSize(QSize(190, 50))
        self.ExAddServer.setMaximumSize(QSize(190, 50))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.ExAddServer.setFont(font)
        self.ExAddServer.setCursor(QCursor(Qt.PointingHandCursor))
        self.ExAddServer.setAutoFillBackground(False)
        self.ExAddServer.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 7px;\n"
"    font: 14px \'Microsoft YaHei UI\';\n"
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
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/MCSL2_Icon/Add.svg"), QIcon.Normal, QIcon.Off)
        icon2.addPixmap(QPixmap(":/MCSL2_Icon/Add.svg"), QIcon.Normal, QIcon.On)
        icon2.addPixmap(QPixmap(":/MCSL2_Icon/Add.svg"), QIcon.Disabled, QIcon.Off)
        icon2.addPixmap(QPixmap(":/MCSL2_Icon/Add.svg"), QIcon.Disabled, QIcon.On)
        icon2.addPixmap(QPixmap(":/MCSL2_Icon/Add.svg"), QIcon.Active, QIcon.Off)
        icon2.addPixmap(QPixmap(":/MCSL2_Icon/Add.svg"), QIcon.Active, QIcon.On)
        icon2.addPixmap(QPixmap(":/MCSL2_Icon/Add.svg"), QIcon.Selected, QIcon.Off)
        icon2.addPixmap(QPixmap(":/MCSL2_Icon/Add.svg"), QIcon.Selected, QIcon.On)
        self.ExAddServer.setIcon(icon2)
        self.ExAddServer.setIconSize(QSize(30, 30))
        self.ExAddServer.setCheckable(True)
        self.ExAddServer.setChecked(False)
        self.ExAddServer.setAutoDefault(True)
        self.ExAddServer.setDefault(True)
        self.ExAddServer.setDescription("")
        self.ExAddServer.setObjectName("ExAddServer")
        self.ImportServer = QCommandLinkButton(self.LeadCPage)
        self.ImportServer.setGeometry(QRect(450, 210, 190, 50))
        self.ImportServer.setMinimumSize(QSize(190, 50))
        self.ImportServer.setMaximumSize(QSize(190, 50))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.ImportServer.setFont(font)
        self.ImportServer.setCursor(QCursor(Qt.PointingHandCursor))
        self.ImportServer.setAutoFillBackground(False)
        self.ImportServer.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 7px;\n"
"    font: 14px \'Microsoft YaHei UI\';\n"
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
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(":/MCSL2_Icon/Import.svg"), QIcon.Normal, QIcon.Off)
        icon3.addPixmap(QPixmap(":/MCSL2_Icon/Import.svg"), QIcon.Normal, QIcon.On)
        icon3.addPixmap(QPixmap(":/MCSL2_Icon/Import.svg"), QIcon.Disabled, QIcon.Off)
        icon3.addPixmap(QPixmap(":/MCSL2_Icon/Import.svg"), QIcon.Disabled, QIcon.On)
        icon3.addPixmap(QPixmap(":/MCSL2_Icon/Import.svg"), QIcon.Active, QIcon.Off)
        icon3.addPixmap(QPixmap(":/MCSL2_Icon/Import.svg"), QIcon.Active, QIcon.On)
        icon3.addPixmap(QPixmap(":/MCSL2_Icon/Import.svg"), QIcon.Selected, QIcon.Off)
        icon3.addPixmap(QPixmap(":/MCSL2_Icon/Import.svg"), QIcon.Selected, QIcon.On)
        self.ImportServer.setIcon(icon3)
        self.ImportServer.setIconSize(QSize(30, 30))
        self.ImportServer.setCheckable(False)
        self.ImportServer.setChecked(False)
        self.ImportServer.setAutoDefault(True)
        self.ImportServer.setDefault(True)
        self.ImportServer.setDescription("")
        self.ImportServer.setObjectName("ImportServer")
        self.LeadConfigTip2 = QLabel(self.LeadCPage)
        self.LeadConfigTip2.setGeometry(QRect(60, 260, 131, 141))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.LeadConfigTip2.setFont(font)
        self.LeadConfigTip2.setAutoFillBackground(False)
        self.LeadConfigTip2.setStyleSheet("")
        self.LeadConfigTip2.setTextFormat(Qt.AutoText)
        self.LeadConfigTip2.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.LeadConfigTip2.setObjectName("LeadConfigTip2")
        self.LeadConfigTip2_2 = QLabel(self.LeadCPage)
        self.LeadConfigTip2_2.setGeometry(QRect(270, 260, 141, 71))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.LeadConfigTip2_2.setFont(font)
        self.LeadConfigTip2_2.setAutoFillBackground(False)
        self.LeadConfigTip2_2.setStyleSheet("")
        self.LeadConfigTip2_2.setTextFormat(Qt.AutoText)
        self.LeadConfigTip2_2.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.LeadConfigTip2_2.setObjectName("LeadConfigTip2_2")
        self.LeadConfigTip2_3 = QLabel(self.LeadCPage)
        self.LeadConfigTip2_3.setGeometry(QRect(480, 260, 141, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.LeadConfigTip2_3.setFont(font)
        self.LeadConfigTip2_3.setAutoFillBackground(False)
        self.LeadConfigTip2_3.setStyleSheet("")
        self.LeadConfigTip2_3.setTextFormat(Qt.AutoText)
        self.LeadConfigTip2_3.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.LeadConfigTip2_3.setObjectName("LeadConfigTip2_3")
        self.ConfigModeWidget.addWidget(self.LeadCPage)
        self.NoobCPage = QWidget()
        self.NoobCPage.setObjectName("NoobCPage")
        self.Completed_Save_PushButton = QPushButton(self.NoobCPage)
        self.Completed_Save_PushButton.setGeometry(QRect(20, 330, 211, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Completed_Save_PushButton.setFont(font)
        self.Completed_Save_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Completed_Save_PushButton.setStyleSheet("QPushButton\n"
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
"}")
        self.Completed_Save_PushButton.setFlat(False)
        self.Completed_Save_PushButton.setObjectName("Completed_Save_PushButton")
        self.Server_Name_Label = QLabel(self.NoobCPage)
        self.Server_Name_Label.setGeometry(QRect(20, 280, 91, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Server_Name_Label.setFont(font)
        self.Server_Name_Label.setObjectName("Server_Name_Label")
        self.Server_Name_LineEdit = QLineEdit(self.NoobCPage)
        self.Server_Name_LineEdit.setGeometry(QRect(120, 290, 111, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.Server_Name_LineEdit.setFont(font)
        self.Server_Name_LineEdit.setStyleSheet("QLineEdit\n"
"{\n"
"    border-radius: 3px;\n"
"    border: 2px;\n"
"    border-color: rgb(223, 223, 223);\n"
"    border-style: solid;\n"
"}\n"
"")
        self.Server_Name_LineEdit.setObjectName("Server_Name_LineEdit")
        self.Others_Background = QLabel(self.NoobCPage)
        self.Others_Background.setGeometry(QRect(0, 260, 251, 121))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Others_Background.setFont(font)
        self.Others_Background.setAutoFillBackground(False)
        self.Others_Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.Others_Background.setText("")
        self.Others_Background.setObjectName("Others_Background")
        self.Configuration_Widget = QWidget(self.NoobCPage)
        self.Configuration_Widget.setGeometry(QRect(280, 0, 351, 291))
        self.Configuration_Widget.setObjectName("Configuration_Widget")
        self.Download_Core_PushButton = QPushButton(self.Configuration_Widget)
        self.Download_Core_PushButton.setGeometry(QRect(230, 240, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Download_Core_PushButton.setFont(font)
        self.Download_Core_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Download_Core_PushButton.setStyleSheet("QPushButton\n"
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
"}")
        self.Download_Core_PushButton.setFlat(False)
        self.Download_Core_PushButton.setObjectName("Download_Core_PushButton")
        self.Download_Java_PushButton = QPushButton(self.Configuration_Widget)
        self.Download_Java_PushButton.setGeometry(QRect(130, 70, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Download_Java_PushButton.setFont(font)
        self.Download_Java_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Download_Java_PushButton.setStyleSheet("QPushButton\n"
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
"}")
        self.Download_Java_PushButton.setFlat(False)
        self.Download_Java_PushButton.setObjectName("Download_Java_PushButton")
        self.Manual_Import_Core_PushButton = QPushButton(self.Configuration_Widget)
        self.Manual_Import_Core_PushButton.setGeometry(QRect(120, 240, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Manual_Import_Core_PushButton.setFont(font)
        self.Manual_Import_Core_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Manual_Import_Core_PushButton.setStyleSheet("QPushButton\n"
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
"}")
        self.Manual_Import_Core_PushButton.setFlat(False)
        self.Manual_Import_Core_PushButton.setObjectName("Manual_Import_Core_PushButton")
        self.Set_Core_Background = QLabel(self.Configuration_Widget)
        self.Set_Core_Background.setGeometry(QRect(0, 220, 351, 71))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Set_Core_Background.setFont(font)
        self.Set_Core_Background.setAutoFillBackground(False)
        self.Set_Core_Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.Set_Core_Background.setText("")
        self.Set_Core_Background.setObjectName("Set_Core_Background")
        self.Set_Java_Background = QLabel(self.Configuration_Widget)
        self.Set_Java_Background.setGeometry(QRect(0, 0, 351, 121))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Set_Java_Background.setFont(font)
        self.Set_Java_Background.setAutoFillBackground(False)
        self.Set_Java_Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
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
        self.MinMemory_LineEdit.setStyleSheet("QLineEdit\n"
"{\n"
"    border-radius: 3px;\n"
"    border: 2px;\n"
"    border-color: rgb(223, 223, 223);\n"
"    border-style: solid;\n"
"}\n"
"")
        self.MinMemory_LineEdit.setObjectName("MinMemory_LineEdit")
        self.Set_Memory_Background = QLabel(self.Configuration_Widget)
        self.Set_Memory_Background.setGeometry(QRect(0, 140, 351, 61))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Set_Memory_Background.setFont(font)
        self.Set_Memory_Background.setAutoFillBackground(False)
        self.Set_Memory_Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.Set_Memory_Background.setText("")
        self.Set_Memory_Background.setObjectName("Set_Memory_Background")
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
        self.MaxMemory_LineEdit.setStyleSheet("QLineEdit\n"
"{\n"
"    border-radius: 3px;\n"
"    border: 2px;\n"
"    border-color: rgb(223, 223, 223);\n"
"    border-style: solid;\n"
"}\n"
"")
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
        self.Auto_Find_Java_PushButton.setStyleSheet("QPushButton\n"
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
"}")
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
        self.Founded_Java_List_PushButton.setStyleSheet("QPushButton\n"
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
        self.Founded_Java_List_PushButton.setObjectName("Founded_Java_List_PushButton")
        self.Set_Core_Background.raise_()
        self.Set_Memory_Background.raise_()
        self.Set_Java_Background.raise_()
        self.Download_Core_PushButton.raise_()
        self.Download_Java_PushButton.raise_()
        self.Manual_Import_Core_PushButton.raise_()
        self.Memory_1_Label.raise_()
        self.MinMemory_LineEdit.raise_()
        self.Java_Label.raise_()
        self.MaxMemory_LineEdit.raise_()
        self.Memory_2_Label.raise_()
        self.Core_Label.raise_()
        self.Auto_Find_Java_PushButton.raise_()
        self.Memory_Unit_Label.raise_()
        self.Java_Version_Label.raise_()
        self.Founded_Java_List_PushButton.raise_()
        self.ConfigTip1_Widget = QWidget(self.NoobCPage)
        self.ConfigTip1_Widget.setGeometry(QRect(0, 0, 251, 121))
        self.ConfigTip1_Widget.setStyleSheet("QWidget\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
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
        self.ConfigTip2_Widget = QWidget(self.NoobCPage)
        self.ConfigTip2_Widget.setGeometry(QRect(0, 140, 251, 101))
        self.ConfigTip2_Widget.setStyleSheet("QWidget\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.ConfigTip2_Widget.setObjectName("ConfigTip2_Widget")
        self.ConfigTip2_Label = QLabel(self.ConfigTip2_Widget)
        self.ConfigTip2_Label.setGeometry(QRect(10, 10, 231, 81))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ConfigTip2_Label.setFont(font)
        self.ConfigTip2_Label.setAutoFillBackground(False)
        self.ConfigTip2_Label.setStyleSheet("")
        self.ConfigTip2_Label.setObjectName("ConfigTip2_Label")
        self.Others_Background.raise_()
        self.Completed_Save_PushButton.raise_()
        self.Server_Name_Label.raise_()
        self.Server_Name_LineEdit.raise_()
        self.Configuration_Widget.raise_()
        self.ConfigTip1_Widget.raise_()
        self.ConfigTip2_Widget.raise_()
        self.ConfigModeWidget.addWidget(self.NoobCPage)
        self.ExtendedCPage = QWidget()
        self.ExtendedCPage.setObjectName("ExtendedCPage")
        self.ExConfiguration_Widget = QWidget(self.ExtendedCPage)
        self.ExConfiguration_Widget.setGeometry(QRect(0, 0, 671, 451))
        self.ExConfiguration_Widget.setObjectName("ExConfiguration_Widget")
        self.ExDownload_Core_PushButton = QPushButton(self.ExConfiguration_Widget)
        self.ExDownload_Core_PushButton.setGeometry(QRect(560, 145, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.ExDownload_Core_PushButton.setFont(font)
        self.ExDownload_Core_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.ExDownload_Core_PushButton.setStyleSheet("QPushButton\n"
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
"}")
        self.ExDownload_Core_PushButton.setFlat(False)
        self.ExDownload_Core_PushButton.setObjectName("ExDownload_Core_PushButton")
        self.ExDownload_Java_PushButton = QPushButton(self.ExConfiguration_Widget)
        self.ExDownload_Java_PushButton.setGeometry(QRect(130, 70, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.ExDownload_Java_PushButton.setFont(font)
        self.ExDownload_Java_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.ExDownload_Java_PushButton.setStyleSheet("QPushButton\n"
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
"}")
        self.ExDownload_Java_PushButton.setFlat(False)
        self.ExDownload_Java_PushButton.setObjectName("ExDownload_Java_PushButton")
        self.ExManual_Import_Core_PushButton = QPushButton(self.ExConfiguration_Widget)
        self.ExManual_Import_Core_PushButton.setGeometry(QRect(450, 145, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.ExManual_Import_Core_PushButton.setFont(font)
        self.ExManual_Import_Core_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.ExManual_Import_Core_PushButton.setStyleSheet("QPushButton\n"
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
"}")
        self.ExManual_Import_Core_PushButton.setFlat(False)
        self.ExManual_Import_Core_PushButton.setObjectName("ExManual_Import_Core_PushButton")
        self.ExSet_Core_Background = QLabel(self.ExConfiguration_Widget)
        self.ExSet_Core_Background.setGeometry(QRect(330, 130, 341, 61))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExSet_Core_Background.setFont(font)
        self.ExSet_Core_Background.setAutoFillBackground(False)
        self.ExSet_Core_Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.ExSet_Core_Background.setText("")
        self.ExSet_Core_Background.setObjectName("ExSet_Core_Background")
        self.ExSet_Java_Background = QLabel(self.ExConfiguration_Widget)
        self.ExSet_Java_Background.setGeometry(QRect(0, 0, 361, 121))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExSet_Java_Background.setFont(font)
        self.ExSet_Java_Background.setAutoFillBackground(False)
        self.ExSet_Java_Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.ExSet_Java_Background.setText("")
        self.ExSet_Java_Background.setObjectName("ExSet_Java_Background")
        self.ExMemory_1_Label = QLabel(self.ExConfiguration_Widget)
        self.ExMemory_1_Label.setGeometry(QRect(20, 140, 71, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExMemory_1_Label.setFont(font)
        self.ExMemory_1_Label.setObjectName("ExMemory_1_Label")
        self.ExMinMemory_LineEdit = QLineEdit(self.ExConfiguration_Widget)
        self.ExMinMemory_LineEdit.setGeometry(QRect(70, 150, 61, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.ExMinMemory_LineEdit.setFont(font)
        self.ExMinMemory_LineEdit.setStyleSheet("QLineEdit\n"
"{\n"
"    border-radius: 3px;\n"
"    border: 2px;\n"
"    border-color: rgb(223, 223, 223);\n"
"    border-style: solid;\n"
"}\n"
"")
        self.ExMinMemory_LineEdit.setObjectName("ExMinMemory_LineEdit")
        self.ExSet_Memory_Background = QLabel(self.ExConfiguration_Widget)
        self.ExSet_Memory_Background.setGeometry(QRect(0, 130, 341, 61))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExSet_Memory_Background.setFont(font)
        self.ExSet_Memory_Background.setAutoFillBackground(False)
        self.ExSet_Memory_Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.ExSet_Memory_Background.setText("")
        self.ExSet_Memory_Background.setObjectName("ExSet_Memory_Background")
        self.ExJava_Label = QLabel(self.ExConfiguration_Widget)
        self.ExJava_Label.setGeometry(QRect(20, 20, 71, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExJava_Label.setFont(font)
        self.ExJava_Label.setObjectName("ExJava_Label")
        self.ExMaxMemory_LineEdit = QLineEdit(self.ExConfiguration_Widget)
        self.ExMaxMemory_LineEdit.setGeometry(QRect(165, 150, 61, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.ExMaxMemory_LineEdit.setFont(font)
        self.ExMaxMemory_LineEdit.setStyleSheet("QLineEdit\n"
"{\n"
"    border-radius: 3px;\n"
"    border: 2px;\n"
"    border-color: rgb(223, 223, 223);\n"
"    border-style: solid;\n"
"}\n"
"")
        self.ExMaxMemory_LineEdit.setObjectName("ExMaxMemory_LineEdit")
        self.ExMemory_2_Label = QLabel(self.ExConfiguration_Widget)
        self.ExMemory_2_Label.setGeometry(QRect(140, 140, 21, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.ExMemory_2_Label.setFont(font)
        self.ExMemory_2_Label.setObjectName("ExMemory_2_Label")
        self.ExCore_Label = QLabel(self.ExConfiguration_Widget)
        self.ExCore_Label.setGeometry(QRect(350, 145, 91, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExCore_Label.setFont(font)
        self.ExCore_Label.setObjectName("ExCore_Label")
        self.ExAuto_Find_Java_PushButton = QPushButton(self.ExConfiguration_Widget)
        self.ExAuto_Find_Java_PushButton.setGeometry(QRect(20, 70, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.ExAuto_Find_Java_PushButton.setFont(font)
        self.ExAuto_Find_Java_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.ExAuto_Find_Java_PushButton.setStyleSheet("QPushButton\n"
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
"}")
        self.ExAuto_Find_Java_PushButton.setFlat(False)
        self.ExAuto_Find_Java_PushButton.setObjectName("ExAuto_Find_Java_PushButton")
        self.ExJava_Version_Label = QLabel(self.ExConfiguration_Widget)
        self.ExJava_Version_Label.setGeometry(QRect(80, 20, 261, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExJava_Version_Label.setFont(font)
        self.ExJava_Version_Label.setText("")
        self.ExJava_Version_Label.setObjectName("ExJava_Version_Label")
        self.ExFounded_Java_List_PushButton = QPushButton(self.ExConfiguration_Widget)
        self.ExFounded_Java_List_PushButton.setGeometry(QRect(240, 70, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.ExFounded_Java_List_PushButton.setFont(font)
        self.ExFounded_Java_List_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.ExFounded_Java_List_PushButton.setStyleSheet("QPushButton\n"
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
        self.ExFounded_Java_List_PushButton.setObjectName("ExFounded_Java_List_PushButton")
        self.ExOthers_Background = QLabel(self.ExConfiguration_Widget)
        self.ExOthers_Background.setGeometry(QRect(370, 0, 301, 121))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExOthers_Background.setFont(font)
        self.ExOthers_Background.setAutoFillBackground(False)
        self.ExOthers_Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.ExOthers_Background.setText("")
        self.ExOthers_Background.setObjectName("ExOthers_Background")
        self.ExServer_Name_LineEdit = QLineEdit(self.ExConfiguration_Widget)
        self.ExServer_Name_LineEdit.setGeometry(QRect(500, 30, 151, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.ExServer_Name_LineEdit.setFont(font)
        self.ExServer_Name_LineEdit.setStyleSheet("QLineEdit\n"
"{\n"
"    border-radius: 3px;\n"
"    border: 2px;\n"
"    border-color: rgb(223, 223, 223);\n"
"    border-style: solid;\n"
"}\n"
"")
        self.ExServer_Name_LineEdit.setObjectName("ExServer_Name_LineEdit")
        self.ExServer_Name_Label = QLabel(self.ExConfiguration_Widget)
        self.ExServer_Name_Label.setGeometry(QRect(400, 20, 91, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExServer_Name_Label.setFont(font)
        self.ExServer_Name_Label.setObjectName("ExServer_Name_Label")
        self.ExCompleted_Save_PushButton = QPushButton(self.ExConfiguration_Widget)
        self.ExCompleted_Save_PushButton.setGeometry(QRect(400, 70, 251, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExCompleted_Save_PushButton.setFont(font)
        self.ExCompleted_Save_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.ExCompleted_Save_PushButton.setStyleSheet("QPushButton\n"
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
"}")
        self.ExCompleted_Save_PushButton.setFlat(False)
        self.ExCompleted_Save_PushButton.setObjectName("ExCompleted_Save_PushButton")
        self.ExMemoryUnitComboBox = QComboBox(self.ExConfiguration_Widget)
        self.ExMemoryUnitComboBox.setGeometry(QRect(240, 145, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setKerning(True)
        self.ExMemoryUnitComboBox.setFont(font)
        self.ExMemoryUnitComboBox.setStyleSheet("QComboBox {\n"
"    border: 1px solid rgb(238, 239, 238);\n"
"    border-radius: 5px;\n"
"    border-bottom: 1px solid rgb(212, 213, 212);\n"
"    padding: 5px 31px 6px 11px;\n"
"    color: black;\n"
"    background-color: rgb(254, 254, 254);\n"
"    text-align: left;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: rgb(251, 251, 251);\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: rgb(252, 252, 252);\n"
"    border-bottom: 1px solid rgb(238, 239, 238);\n"
"    color: rgba(0, 0, 0, 0.63);\n"
"}\n"
"QComboBox::drop-down\n"
"{\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: right;\n"
"    width: 35px;\n"
"    border-left-style: solid;\n"
"}\n"
"QComboBox::down-arrow\n"
"{\n"
"    border-image: url(:/MCSL2_Icon/QComboBoxDownArrow.svg);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid rgba(0, 0, 0, 0.1);\n"
"    border-radius: 9px;\n"
"    background-color: rgb(249, 249, 249);\n"
"    outline: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding-left: 0px;\n"
"    padding-right: 10px;\n"
"    border-radius: 5px;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background-color: rgba(0, 0, 0, 9);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(0, 0, 0, 7);\n"
"    color: black;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected:active {\n"
"    background-color: rgba(0, 0, 0, 0.06);\n"
"    color: rgba(0, 0, 0, 0.7);\n"
"}")
        self.ExMemoryUnitComboBox.setObjectName("ExMemoryUnitComboBox")
        self.ExMemoryUnitComboBox.addItem("")
        self.ExMemoryUnitComboBox.addItem("")
        self.ExSet_Encoding_Background = QLabel(self.ExConfiguration_Widget)
        self.ExSet_Encoding_Background.setGeometry(QRect(0, 200, 671, 111))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExSet_Encoding_Background.setFont(font)
        self.ExSet_Encoding_Background.setAutoFillBackground(False)
        self.ExSet_Encoding_Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.ExSet_Encoding_Background.setText("")
        self.ExSet_Encoding_Background.setObjectName("ExSet_Encoding_Background")
        self.ExConsoleInputDecoding = QLabel(self.ExConfiguration_Widget)
        self.ExConsoleInputDecoding.setGeometry(QRect(20, 263, 251, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.ExConsoleInputDecoding.setFont(font)
        self.ExConsoleInputDecoding.setObjectName("ExConsoleInputDecoding")
        self.ExConsoleOutputEncodingComboBox = QComboBox(self.ExConfiguration_Widget)
        self.ExConsoleOutputEncodingComboBox.setGeometry(QRect(390, 220, 241, 31))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ExConsoleOutputEncodingComboBox.sizePolicy().hasHeightForWidth())
        self.ExConsoleOutputEncodingComboBox.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setKerning(True)
        self.ExConsoleOutputEncodingComboBox.setFont(font)
        self.ExConsoleOutputEncodingComboBox.setStyleSheet("QComboBox {\n"
"    border: 1px solid rgb(238, 239, 238);\n"
"    border-radius: 5px;\n"
"    border-bottom: 1px solid rgb(212, 213, 212);\n"
"    padding: 5px 31px 6px 11px;\n"
"    color: black;\n"
"    background-color: rgb(254, 254, 254);\n"
"    text-align: left;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: rgb(251, 251, 251);\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: rgb(252, 252, 252);\n"
"    border-bottom: 1px solid rgb(238, 239, 238);\n"
"    color: rgba(0, 0, 0, 0.63);\n"
"}\n"
"QComboBox::drop-down\n"
"{\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: right;\n"
"    width: 35px;\n"
"    border-left-style: solid;\n"
"}\n"
"QComboBox::down-arrow\n"
"{\n"
"    border-image: url(:/MCSL2_Icon/QComboBoxDownArrow.svg);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid rgba(0, 0, 0, 0.1);\n"
"    border-radius: 9px;\n"
"    background-color: rgb(249, 249, 249);\n"
"    outline: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding-left: 0px;\n"
"    padding-right: 10px;\n"
"    border-radius: 5px;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background-color: rgba(0, 0, 0, 9);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(0, 0, 0, 7);\n"
"    color: black;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected:active {\n"
"    background-color: rgba(0, 0, 0, 0.06);\n"
"    color: rgba(0, 0, 0, 0.7);\n"
"}")
        self.ExConsoleOutputEncodingComboBox.setObjectName("ExConsoleOutputEncodingComboBox")
        self.ExConsoleOutputEncodingComboBox.addItem("")
        self.ExConsoleOutputEncodingComboBox.addItem("")
        self.ExConsoleInputDecodingComboBox = QComboBox(self.ExConfiguration_Widget)
        self.ExConsoleInputDecodingComboBox.setGeometry(QRect(390, 260, 241, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setKerning(True)
        self.ExConsoleInputDecodingComboBox.setFont(font)
        self.ExConsoleInputDecodingComboBox.setStyleSheet("QComboBox {\n"
"    border: 1px solid rgb(238, 239, 238);\n"
"    border-radius: 5px;\n"
"    border-bottom: 1px solid rgb(212, 213, 212);\n"
"    padding: 5px 31px 6px 11px;\n"
"    color: black;\n"
"    background-color: rgb(254, 254, 254);\n"
"    text-align: left;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: rgb(251, 251, 251);\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: rgb(252, 252, 252);\n"
"    border-bottom: 1px solid rgb(238, 239, 238);\n"
"    color: rgba(0, 0, 0, 0.63);\n"
"}\n"
"QComboBox::drop-down\n"
"{\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: right;\n"
"    width: 35px;\n"
"    border-left-style: solid;\n"
"}\n"
"QComboBox::down-arrow\n"
"{\n"
"    border-image: url(:/MCSL2_Icon/QComboBoxDownArrow.svg);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid rgba(0, 0, 0, 0.1);\n"
"    border-radius: 9px;\n"
"    background-color: rgb(249, 249, 249);\n"
"    outline: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    padding-left: 0px;\n"
"    padding-right: 10px;\n"
"    border-radius: 5px;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background-color: rgba(0, 0, 0, 9);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: rgba(0, 0, 0, 7);\n"
"    color: black;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:selected:active {\n"
"    background-color: rgba(0, 0, 0, 0.06);\n"
"    color: rgba(0, 0, 0, 0.7);\n"
"}")
        self.ExConsoleInputDecodingComboBox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.ExConsoleInputDecodingComboBox.setFrame(True)
        self.ExConsoleInputDecodingComboBox.setObjectName("ExConsoleInputDecodingComboBox")
        self.ExConsoleInputDecodingComboBox.addItem("")
        self.ExConsoleInputDecodingComboBox.addItem("")
        self.ExConsoleInputDecodingComboBox.addItem("")
        self.ExConsoleOutputEncoding = QLabel(self.ExConfiguration_Widget)
        self.ExConsoleOutputEncoding.setGeometry(QRect(20, 223, 271, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.ExConsoleOutputEncoding.setFont(font)
        self.ExConsoleOutputEncoding.setObjectName("ExConsoleOutputEncoding")
        self.ExJVMArg = QLabel(self.ExConfiguration_Widget)
        self.ExJVMArg.setGeometry(QRect(20, 330, 251, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.ExJVMArg.setFont(font)
        self.ExJVMArg.setObjectName("ExJVMArg")
        self.ExJVMArg_Background = QLabel(self.ExConfiguration_Widget)
        self.ExJVMArg_Background.setGeometry(QRect(0, 320, 671, 131))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ExJVMArg_Background.setFont(font)
        self.ExJVMArg_Background.setAutoFillBackground(False)
        self.ExJVMArg_Background.setStyleSheet("QLabel\n"
"{\n"
"    background-color: rgb(247, 247, 247);\n"
"    border-radius: 10px\n"
"}")
        self.ExJVMArg_Background.setText("")
        self.ExJVMArg_Background.setObjectName("ExJVMArg_Background")
        self.textEdit = QTextEdit(self.ExConfiguration_Widget)
        self.textEdit.setGeometry(QRect(20, 360, 631, 81))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("QTextEdit\n"
"{\n"
"    border-radius: 3px;\n"
"    border: 2px;\n"
"    border-color: rgb(223, 223, 223);\n"
"    border-style: solid;\n"
"}\n"
"")
        self.textEdit.setObjectName("textEdit")
        self.ExJVMArg_Background.raise_()
        self.ExSet_Encoding_Background.raise_()
        self.ExSet_Java_Background.raise_()
        self.ExSet_Core_Background.raise_()
        self.ExSet_Memory_Background.raise_()
        self.ExDownload_Core_PushButton.raise_()
        self.ExDownload_Java_PushButton.raise_()
        self.ExManual_Import_Core_PushButton.raise_()
        self.ExMemory_1_Label.raise_()
        self.ExMinMemory_LineEdit.raise_()
        self.ExJava_Label.raise_()
        self.ExMaxMemory_LineEdit.raise_()
        self.ExMemory_2_Label.raise_()
        self.ExCore_Label.raise_()
        self.ExAuto_Find_Java_PushButton.raise_()
        self.ExJava_Version_Label.raise_()
        self.ExFounded_Java_List_PushButton.raise_()
        self.ExOthers_Background.raise_()
        self.ExServer_Name_LineEdit.raise_()
        self.ExServer_Name_Label.raise_()
        self.ExCompleted_Save_PushButton.raise_()
        self.ExMemoryUnitComboBox.raise_()
        self.ExConsoleInputDecoding.raise_()
        self.ExConsoleOutputEncodingComboBox.raise_()
        self.ExConsoleInputDecodingComboBox.raise_()
        self.ExConsoleOutputEncoding.raise_()
        self.ExJVMArg.raise_()
        self.textEdit.raise_()
        self.ConfigModeWidget.addWidget(self.ExtendedCPage)
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
            "    min-Width: 100px;\n"
            "    min-Height: 20px;\n"
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
            "    Width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-Height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    Height: 0px;\n"
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
            "    Width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-Height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    Height: 0px;\n"
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
        self.SpigotScrollAreaWidgetContents.setObjectName(
            "SpigotScrollAreaWidgetContents"
        )
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
            "    Width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-Height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    Height: 0px;\n"
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
        self.PaperScrollAreaWidgetContents.setObjectName(
            "PaperScrollAreaWidgetContents"
        )
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
            "    Width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-Height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    Height: 0px;\n"
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
        self.BungeeCordScrollAreaWidgetContents.setObjectName(
            "BungeeCordScrollAreaWidgetContents"
        )
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
        self.OfficialCoreScrollArea.viewport().setProperty(
            "cursor", QCursor(Qt.ArrowCursor)
        )
        self.OfficialCoreScrollArea.setStyleSheet(
            "QScrollArea{\n"
            "    border: 0px solid;\n"
            "    border-right-color: #dcdbdc;\n"
            "    background-color: transparent;\n"
            "}\n"
            "QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: transparent;\n"
            "    Width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-Height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "    background: none;\n"
            "}"
        )
        self.OfficialCoreScrollArea.setFrameShape(QFrame.NoFrame)
        self.OfficialCoreScrollArea.setFrameShadow(QFrame.Plain)
        self.OfficialCoreScrollArea.setLineWidth(0)
        self.OfficialCoreScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.OfficialCoreScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.OfficialCoreScrollArea.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents
        )
        self.OfficialCoreScrollArea.setWidgetResizable(True)
        self.OfficialCoreScrollArea.setObjectName("OfficialCoreScrollArea")
        self.OfficialCoreScrollAreaWidgetContents = QWidget()
        self.OfficialCoreScrollAreaWidgetContents.setGeometry(QRect(0, 0, 619, 351))
        self.OfficialCoreScrollAreaWidgetContents.setObjectName(
            "OfficialCoreScrollAreaWidgetContents"
        )
        self.verticalLayout_5 = QVBoxLayout(self.OfficialCoreScrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.OfficialCoreVerticalLayout = QVBoxLayout()
        self.OfficialCoreVerticalLayout.setObjectName("OfficialCoreVerticalLayout")
        self.verticalLayout_5.addLayout(self.OfficialCoreVerticalLayout)
        self.OfficialCoreScrollArea.setWidget(self.OfficialCoreScrollAreaWidgetContents)
        self.DownloadSwitcher_TabWidget.addTab(self.OfficialCoreTab, "")
        self.More_Download_PushButton = QPushButton(self.DownloadPage)
        self.More_Download_PushButton.setGeometry(QRect(610, 100, 71, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.More_Download_PushButton.setFont(font)
        self.More_Download_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.More_Download_PushButton.setStyleSheet(
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
        self.More_Download_PushButton.setObjectName("More_Download_PushButton")
        self.GoToDownloadSourceChangerPushButton = QPushButton(self.DownloadPage)
        self.GoToDownloadSourceChangerPushButton.setGeometry(QRect(500, 100, 101, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.GoToDownloadSourceChangerPushButton.setFont(font)
        self.GoToDownloadSourceChangerPushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.GoToDownloadSourceChangerPushButton.setStyleSheet("QPushButton\n"
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
        self.GoToDownloadSourceChangerPushButton.setObjectName("GoToDownloadSourceChangerPushButton")
        self.CurrentDownloadSourceLabel = QLabel(self.DownloadPage)
        self.CurrentDownloadSourceLabel.setGeometry(QRect(100, 90, 281, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.CurrentDownloadSourceLabel.setFont(font)
        self.CurrentDownloadSourceLabel.setAutoFillBackground(False)
        self.CurrentDownloadSourceLabel.setStyleSheet("")
        self.CurrentDownloadSourceLabel.setObjectName("CurrentDownloadSourceLabel")
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
        self.SettingsPage = QWidget()
        self.SettingsPage.setObjectName("SettingsPage")
        self.About_Label = QLabel(self.SettingsPage)
        self.About_Label.setGeometry(QRect(30, 80, 71, 51))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.About_Label.setFont(font)
        self.About_Label.setObjectName("About_Label")
        self.SettingsScrollArea = QScrollArea(self.SettingsPage)
        self.SettingsScrollArea.setGeometry(QRect(30, 130, 641, 421))
        self.SettingsScrollArea.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.SettingsScrollArea.setStyleSheet("QScrollArea{\n"
                                              "    border: 0px solid;\n"
                                              "    background-color: transparent;\n"
                                              "}\n"
                                              "QScrollBar:vertical {\n"
                                              "    border: none;\n"
                                              "    background: transparent;\n"
                                              "    width: 0px;\n"
                                              "}\n"
                                              "QScrollBar::handle:vertical {\n"
                                              "    min-height: 0px;\n"
                                              "}\n"
                                              "QScrollBar::add-line:vertial\n"
                                              "{\n"
                                              "    height: 0px;\n"
                                              "}\n"
                                              "QScrollBar::sub-line:vertial\n"
                                              "{\n"
                                              "    height: 0px;\n"
                                              "}\n"
                                              "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
                                              "{\n"
                                              "    height: 0px;\n"
                                              "}\n"
                                              "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                              "    background: none;\n"
                                              "}")
        self.SettingsScrollArea.setFrameShape(QFrame.NoFrame)
        self.SettingsScrollArea.setFrameShadow(QFrame.Plain)
        self.SettingsScrollArea.setLineWidth(0)
        self.SettingsScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.SettingsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SettingsScrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.SettingsScrollArea.setWidgetResizable(True)
        self.SettingsScrollArea.setObjectName("SettingsScrollArea")
        self.SettingsScrollAreaWidgetContents = QWidget()
        self.SettingsScrollAreaWidgetContents.setGeometry(QRect(0, 0, 641, 1677))
        self.SettingsScrollAreaWidgetContents.setObjectName("SettingsScrollAreaWidgetContents")
        self.verticalLayout_7 = QVBoxLayout(self.SettingsScrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.SettingsVerticalLayout = QVBoxLayout()
        self.SettingsVerticalLayout.setObjectName("SettingsVerticalLayout")
        self.ServerSettingsWidget = QWidget(self.SettingsScrollAreaWidgetContents)
        self.ServerSettingsWidget.setMinimumSize(QSize(620, 160))
        self.ServerSettingsWidget.setMaximumSize(QSize(620, 160))
        self.ServerSettingsWidget.setStyleSheet("QWidget\n"
                                                "{\n"
                                                "    border-radius: 7px;\n"
                                                "    background-color: rgba(247, 247, 247, 247)\n"
                                                "}")
        self.ServerSettingsWidget.setObjectName("ServerSettingsWidget")
        self.AutoRunLastServerSetting = QCheckBox(self.ServerSettingsWidget)
        self.AutoRunLastServerSetting.setGeometry(QRect(30, 50, 410, 30))
        self.AutoRunLastServerSetting.setMinimumSize(QSize(28, 20))
        self.AutoRunLastServerSetting.setMaximumSize(QSize(410, 30))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.AutoRunLastServerSetting.setFont(font)
        self.AutoRunLastServerSetting.setStyleSheet("QCheckBox {\n"
                                                    "    color: black;\n"
                                                    "    spacing: 8px;\n"
                                                    "    min-width: 28px;\n"
                                                    "    min-height: 20px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator {\n"
                                                    "    width: 18px;\n"
                                                    "    height: 18px;\n"
                                                    "    border-radius: 5px;\n"
                                                    "    border: 1px solid rgb(135, 135, 135);\n"
                                                    "    background-color: rgb(241, 241, 241);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:hover {\n"
                                                    "    border: 1px solid rgb(132, 132, 132);\n"
                                                    "    background-color: rgb(232, 232, 232);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:pressed {\n"
                                                    "    border: 1px solid rgb(184, 184, 184);\n"
                                                    "    background-color: rgb(224, 224, 224);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked,\n"
                                                    "QCheckBox::indicator:indeterminate {\n"
                                                    "    border: 1px solid rgb(0, 120, 212);\n"
                                                    "    background-color: rgb(0, 120, 212);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked {\n"
                                                    "    image: url(:/MCSL2_Icon/QCheckBoxAccept.svg);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:indeterminate {\n"
                                                    "    image: url(:/MCSL2_Icon/QCheckBoxPartialAccept.svg);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked:hover,\n"
                                                    "QCheckBox::indicator:indeterminate:hover {\n"
                                                    "    border: 1px solid --ThemeColorLight1;\n"
                                                    "    background-color: --ThemeColorLight1;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked:pressed,\n"
                                                    "QCheckBox::indicator:indeterminate:pressed {\n"
                                                    "    border: 1px solid --ThemeColorLight3;\n"
                                                    "    background-color: --ThemeColorLight3;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox:disabled {\n"
                                                    "    color: rgba(0, 0, 0, 110);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:disabled {\n"
                                                    "    border: 1px solid #bbbbbb;\n"
                                                    "    background-color: rgb(224, 224, 224);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked:disabled,\n"
                                                    "QCheckBox::indicator:indeterminate:disabled {\n"
                                                    "    border: 1px solid rgb(199, 199, 199);\n"
                                                    "    background-color: rgb(199, 199, 199);\n"
                                                    "}")
        self.AutoRunLastServerSetting.setObjectName("AutoRunLastServerSetting")
        self.AcceptAllMojangEULASetting = QCheckBox(self.ServerSettingsWidget)
        self.AcceptAllMojangEULASetting.setGeometry(QRect(30, 80, 410, 30))
        self.AcceptAllMojangEULASetting.setMinimumSize(QSize(28, 20))
        self.AcceptAllMojangEULASetting.setMaximumSize(QSize(410, 30))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.AcceptAllMojangEULASetting.setFont(font)
        self.AcceptAllMojangEULASetting.setStyleSheet("QCheckBox {\n"
                                                      "    color: black;\n"
                                                      "    spacing: 8px;\n"
                                                      "    min-width: 28px;\n"
                                                      "    min-height: 20px;\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox::indicator {\n"
                                                      "    width: 18px;\n"
                                                      "    height: 18px;\n"
                                                      "    border-radius: 5px;\n"
                                                      "    border: 1px solid rgb(135, 135, 135);\n"
                                                      "    background-color: rgb(241, 241, 241);\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox::indicator:hover {\n"
                                                      "    border: 1px solid rgb(132, 132, 132);\n"
                                                      "    background-color: rgb(232, 232, 232);\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox::indicator:pressed {\n"
                                                      "    border: 1px solid rgb(184, 184, 184);\n"
                                                      "    background-color: rgb(224, 224, 224);\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox::indicator:checked,\n"
                                                      "QCheckBox::indicator:indeterminate {\n"
                                                      "    border: 1px solid rgb(0, 120, 212);\n"
                                                      "    background-color: rgb(0, 120, 212);\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox::indicator:checked {\n"
                                                      "    image: url(:/MCSL2_Icon/QCheckBoxAccept.svg);\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox::indicator:indeterminate {\n"
                                                      "    image: url(:/MCSL2_Icon/QCheckBoxPartialAccept.svg);\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox::indicator:checked:hover,\n"
                                                      "QCheckBox::indicator:indeterminate:hover {\n"
                                                      "    border: 1px solid --ThemeColorLight1;\n"
                                                      "    background-color: --ThemeColorLight1;\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox::indicator:checked:pressed,\n"
                                                      "QCheckBox::indicator:indeterminate:pressed {\n"
                                                      "    border: 1px solid --ThemeColorLight3;\n"
                                                      "    background-color: --ThemeColorLight3;\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox:disabled {\n"
                                                      "    color: rgba(0, 0, 0, 110);\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox::indicator:disabled {\n"
                                                      "    border: 1px solid #bbbbbb;\n"
                                                      "    background-color: rgb(224, 224, 224);\n"
                                                      "}\n"
                                                      "\n"
                                                      "QCheckBox::indicator:checked:disabled,\n"
                                                      "QCheckBox::indicator:indeterminate:disabled {\n"
                                                      "    border: 1px solid rgb(199, 199, 199);\n"
                                                      "    background-color: rgb(199, 199, 199);\n"
                                                      "}")
        self.AcceptAllMojangEULASetting.setIconSize(QSize(32, 32))
        self.AcceptAllMojangEULASetting.setObjectName("AcceptAllMojangEULASetting")
        self.StopServerSettings = QCheckBox(self.ServerSettingsWidget)
        self.StopServerSettings.setGeometry(QRect(30, 110, 410, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.StopServerSettings.setFont(font)
        self.StopServerSettings.setStyleSheet("QCheckBox {\n"
                                              "    color: black;\n"
                                              "    spacing: 8px;\n"
                                              "    min-width: 28px;\n"
                                              "    min-height: 20px;\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator {\n"
                                              "    width: 18px;\n"
                                              "    height: 18px;\n"
                                              "    border-radius: 5px;\n"
                                              "    border: 1px solid rgb(135, 135, 135);\n"
                                              "    background-color: rgb(241, 241, 241);\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:hover {\n"
                                              "    border: 1px solid rgb(132, 132, 132);\n"
                                              "    background-color: rgb(232, 232, 232);\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:pressed {\n"
                                              "    border: 1px solid rgb(184, 184, 184);\n"
                                              "    background-color: rgb(224, 224, 224);\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:checked,\n"
                                              "QCheckBox::indicator:indeterminate {\n"
                                              "    border: 1px solid rgb(0, 120, 212);\n"
                                              "    background-color: rgb(0, 120, 212);\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:checked {\n"
                                              "    image: url(:/MCSL2_Icon/QCheckBoxAccept.svg);\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:indeterminate {\n"
                                              "    image: url(:/MCSL2_Icon/QCheckBoxPartialAccept.svg);\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:checked:hover,\n"
                                              "QCheckBox::indicator:indeterminate:hover {\n"
                                              "    border: 1px solid --ThemeColorLight1;\n"
                                              "    background-color: --ThemeColorLight1;\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:checked:pressed,\n"
                                              "QCheckBox::indicator:indeterminate:pressed {\n"
                                              "    border: 1px solid --ThemeColorLight3;\n"
                                              "    background-color: --ThemeColorLight3;\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox:disabled {\n"
                                              "    color: rgba(0, 0, 0, 110);\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:disabled {\n"
                                              "    border: 1px solid #bbbbbb;\n"
                                              "    background-color: rgb(224, 224, 224);\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:checked:disabled,\n"
                                              "QCheckBox::indicator:indeterminate:disabled {\n"
                                              "    border: 1px solid rgb(199, 199, 199);\n"
                                              "    background-color: rgb(199, 199, 199);\n"
                                              "}")
        self.StopServerSettings.setIconSize(QSize(32, 32))
        self.StopServerSettings.setChecked(True)
        self.StopServerSettings.setObjectName("StopServerSettings")
        self.ServerSettingsTitle = QWidget(self.ServerSettingsWidget)
        self.ServerSettingsTitle.setGeometry(QRect(20, 10, 120, 40))
        self.ServerSettingsTitle.setMinimumSize(QSize(120, 40))
        self.ServerSettingsTitle.setStyleSheet("QWidget\n"
                                               "{\n"
                                               "    background-color: rgb(247, 247, 247);\n"
                                               "    border-radius: 10px\n"
                                               "}")
        self.ServerSettingsTitle.setObjectName("ServerSettingsTitle")
        self.ServerSettingsWidgetTitleLabel = QLabel(self.ServerSettingsTitle)
        self.ServerSettingsWidgetTitleLabel.setGeometry(QRect(30, 10, 81, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.ServerSettingsWidgetTitleLabel.setFont(font)
        self.ServerSettingsWidgetTitleLabel.setObjectName("ServerSettingsWidgetTitleLabel")
        self.ServerSettingsWidgetBlue = QLabel(self.ServerSettingsTitle)
        self.ServerSettingsWidgetBlue.setGeometry(QRect(10, 10, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ServerSettingsWidgetBlue.setFont(font)
        self.ServerSettingsWidgetBlue.setCursor(QCursor(Qt.ArrowCursor))
        self.ServerSettingsWidgetBlue.setAutoFillBackground(False)
        self.ServerSettingsWidgetBlue.setStyleSheet("QLabel\n"
                                                    "{\n"
                                                    "    background-color: rgb(0, 120, 212);\n"
                                                    "    border-radius: 10px\n"
                                                    "}")
        self.ServerSettingsWidgetBlue.setText("")
        self.ServerSettingsWidgetBlue.setObjectName("ServerSettingsWidgetBlue")
        self.SettingsVerticalLayout.addWidget(self.ServerSettingsWidget)
        self.ConfigPageSettingsWidget = QWidget(self.SettingsScrollAreaWidgetContents)
        self.ConfigPageSettingsWidget.setMinimumSize(QSize(620, 160))
        self.ConfigPageSettingsWidget.setMaximumSize(QSize(620, 160))
        self.ConfigPageSettingsWidget.setStyleSheet("QWidget\n"
                                                    "{\n"
                                                    "    border-radius: 7px;\n"
                                                    "    background-color: rgba(247, 247, 247, 247)\n"
                                                    "}")
        self.ConfigPageSettingsWidget.setObjectName("ConfigPageSettingsWidget")
        self.OnlySaveGlobalServerConfigs = QCheckBox(self.ConfigPageSettingsWidget)
        self.OnlySaveGlobalServerConfigs.setGeometry(QRect(30, 93, 410, 30))
        self.OnlySaveGlobalServerConfigs.setMinimumSize(QSize(28, 20))
        self.OnlySaveGlobalServerConfigs.setMaximumSize(QSize(410, 30))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.OnlySaveGlobalServerConfigs.setFont(font)
        self.OnlySaveGlobalServerConfigs.setStyleSheet("QCheckBox {\n"
                                                       "    color: black;\n"
                                                       "    spacing: 8px;\n"
                                                       "    min-width: 28px;\n"
                                                       "    min-height: 20px;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox::indicator {\n"
                                                       "    width: 18px;\n"
                                                       "    height: 18px;\n"
                                                       "    border-radius: 5px;\n"
                                                       "    border: 1px solid rgb(135, 135, 135);\n"
                                                       "    background-color: rgb(241, 241, 241);\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox::indicator:hover {\n"
                                                       "    border: 1px solid rgb(132, 132, 132);\n"
                                                       "    background-color: rgb(232, 232, 232);\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox::indicator:pressed {\n"
                                                       "    border: 1px solid rgb(184, 184, 184);\n"
                                                       "    background-color: rgb(224, 224, 224);\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox::indicator:checked,\n"
                                                       "QCheckBox::indicator:indeterminate {\n"
                                                       "    border: 1px solid rgb(0, 120, 212);\n"
                                                       "    background-color: rgb(0, 120, 212);\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox::indicator:checked {\n"
                                                       "    image: url(:/MCSL2_Icon/QCheckBoxAccept.svg);\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox::indicator:indeterminate {\n"
                                                       "    image: url(:/MCSL2_Icon/QCheckBoxPartialAccept.svg);\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox::indicator:checked:hover,\n"
                                                       "QCheckBox::indicator:indeterminate:hover {\n"
                                                       "    border: 1px solid --ThemeColorLight1;\n"
                                                       "    background-color: --ThemeColorLight1;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox::indicator:checked:pressed,\n"
                                                       "QCheckBox::indicator:indeterminate:pressed {\n"
                                                       "    border: 1px solid --ThemeColorLight3;\n"
                                                       "    background-color: --ThemeColorLight3;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox:disabled {\n"
                                                       "    color: rgba(0, 0, 0, 110);\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox::indicator:disabled {\n"
                                                       "    border: 1px solid #bbbbbb;\n"
                                                       "    background-color: rgb(224, 224, 224);\n"
                                                       "}\n"
                                                       "\n"
                                                       "QCheckBox::indicator:checked:disabled,\n"
                                                       "QCheckBox::indicator:indeterminate:disabled {\n"
                                                       "    border: 1px solid rgb(199, 199, 199);\n"
                                                       "    background-color: rgb(199, 199, 199);\n"
                                                       "}")
        self.OnlySaveGlobalServerConfigs.setObjectName("OnlySaveGlobalServerConfigs")
        self.ConfigPageSettingsTitle = QWidget(self.ConfigPageSettingsWidget)
        self.ConfigPageSettingsTitle.setGeometry(QRect(20, 10, 120, 40))
        self.ConfigPageSettingsTitle.setMinimumSize(QSize(120, 40))
        self.ConfigPageSettingsTitle.setStyleSheet("QWidget\n"
                                                   "{\n"
                                                   "    background-color: rgb(247, 247, 247);\n"
                                                   "    border-radius: 10px\n"
                                                   "}")
        self.ConfigPageSettingsTitle.setObjectName("ConfigPageSettingsTitle")
        self.ConfigPageSettingsWidgetTitleLabel = QLabel(self.ConfigPageSettingsTitle)
        self.ConfigPageSettingsWidgetTitleLabel.setGeometry(QRect(30, 10, 81, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.ConfigPageSettingsWidgetTitleLabel.setFont(font)
        self.ConfigPageSettingsWidgetTitleLabel.setObjectName("ConfigPageSettingsWidgetTitleLabel")
        self.ConfigPageSettingsWidgetBlue = QLabel(self.ConfigPageSettingsTitle)
        self.ConfigPageSettingsWidgetBlue.setGeometry(QRect(10, 10, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ConfigPageSettingsWidgetBlue.setFont(font)
        self.ConfigPageSettingsWidgetBlue.setCursor(QCursor(Qt.ArrowCursor))
        self.ConfigPageSettingsWidgetBlue.setAutoFillBackground(False)
        self.ConfigPageSettingsWidgetBlue.setStyleSheet("QLabel\n"
                                                        "{\n"
                                                        "    background-color: rgb(0, 120, 212);\n"
                                                        "    border-radius: 10px\n"
                                                        "}")
        self.ConfigPageSettingsWidgetBlue.setText("")
        self.ConfigPageSettingsWidgetBlue.setObjectName("ConfigPageSettingsWidgetBlue")
        self.HowToAddServer = QLabel(self.ConfigPageSettingsWidget)
        self.HowToAddServer.setGeometry(QRect(30, 63, 171, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.HowToAddServer.setFont(font)
        self.HowToAddServer.setObjectName("HowToAddServer")
        self.HowToAddServerComboBox = QComboBox(self.ConfigPageSettingsWidget)
        self.HowToAddServerComboBox.setGeometry(QRect(370, 60, 221, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setKerning(True)
        self.HowToAddServerComboBox.setFont(font)
        self.HowToAddServerComboBox.setStyleSheet("QComboBox {\n"
                                                  "    border: 1px solid rgb(238, 239, 238);\n"
                                                  "    border-radius: 5px;\n"
                                                  "    border-bottom: 1px solid rgb(212, 213, 212);\n"
                                                  "    padding: 5px 31px 6px 11px;\n"
                                                  "    color: black;\n"
                                                  "    background-color: rgb(254, 254, 254);\n"
                                                  "    text-align: left;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QComboBox:hover {\n"
                                                  "    background-color: rgb(251, 251, 251);\n"
                                                  "}\n"
                                                  "\n"
                                                  "QComboBox:pressed {\n"
                                                  "    background-color: rgb(252, 252, 252);\n"
                                                  "    border-bottom: 1px solid rgb(238, 239, 238);\n"
                                                  "    color: rgba(0, 0, 0, 0.63);\n"
                                                  "}\n"
                                                  "QComboBox::drop-down\n"
                                                  "{\n"
                                                  "    subcontrol-origin: padding;\n"
                                                  "    subcontrol-position: right;\n"
                                                  "    width: 35px;\n"
                                                  "    border-left-style: solid;\n"
                                                  "}\n"
                                                  "QComboBox::down-arrow\n"
                                                  "{\n"
                                                  "    border-image: url(:/MCSL2_Icon/QComboBoxDownArrow.svg);\n"
                                                  "}\n"
                                                  "QComboBox QAbstractItemView {\n"
                                                  "    border: 1px solid rgba(0, 0, 0, 0.1);\n"
                                                  "    border-radius: 9px;\n"
                                                  "    background-color: rgb(249, 249, 249);\n"
                                                  "    outline: none;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QComboBox QAbstractItemView::item {\n"
                                                  "    padding-left: 0px;\n"
                                                  "    padding-right: 10px;\n"
                                                  "    border-radius: 5px;\n"
                                                  "    border: none;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QComboBox QAbstractItemView::item:hover {\n"
                                                  "    background-color: rgba(0, 0, 0, 9);\n"
                                                  "}\n"
                                                  "\n"
                                                  "QComboBox QAbstractItemView::item:selected {\n"
                                                  "    background-color: rgba(0, 0, 0, 7);\n"
                                                  "    color: black;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QComboBox QAbstractItemView::item:selected:active {\n"
                                                  "    background-color: rgba(0, 0, 0, 0.06);\n"
                                                  "    color: rgba(0, 0, 0, 0.7);\n"
                                                  "}")
        self.HowToAddServerComboBox.setObjectName("HowToAddServerComboBox")
        self.HowToAddServerComboBox.addItem("")
        self.HowToAddServerComboBox.addItem("")
        self.HowToAddServerComboBox.addItem("")
        self.SettingsVerticalLayout.addWidget(self.ConfigPageSettingsWidget)
        self.DownloadSettingsWidget = QWidget(self.SettingsScrollAreaWidgetContents)
        self.DownloadSettingsWidget.setMinimumSize(QSize(620, 250))
        self.DownloadSettingsWidget.setMaximumSize(QSize(620, 250))
        self.DownloadSettingsWidget.setStyleSheet("QWidget\n"
                                                  "{\n"
                                                  "    border-radius: 7px;\n"
                                                  "    background-color: rgba(247, 247, 247, 247)\n"
                                                  "}")
        self.DownloadSettingsWidget.setObjectName("DownloadSettingsWidget")
        self.DownloadSettingsTitle = QWidget(self.DownloadSettingsWidget)
        self.DownloadSettingsTitle.setGeometry(QRect(20, 10, 120, 40))
        self.DownloadSettingsTitle.setMinimumSize(QSize(120, 40))
        self.DownloadSettingsTitle.setStyleSheet("QWidget\n"
                                                 "{\n"
                                                 "    background-color: rgb(247, 247, 247);\n"
                                                 "    border-radius: 10px\n"
                                                 "}")
        self.DownloadSettingsTitle.setObjectName("DownloadSettingsTitle")
        self.DownloadSettingsWidgetTitleLabel = QLabel(self.DownloadSettingsTitle)
        self.DownloadSettingsWidgetTitleLabel.setGeometry(QRect(30, 10, 81, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.DownloadSettingsWidgetTitleLabel.setFont(font)
        self.DownloadSettingsWidgetTitleLabel.setObjectName("DownloadSettingsWidgetTitleLabel")
        self.DownloadSettingsWidgetBlue = QLabel(self.DownloadSettingsTitle)
        self.DownloadSettingsWidgetBlue.setGeometry(QRect(10, 10, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.DownloadSettingsWidgetBlue.setFont(font)
        self.DownloadSettingsWidgetBlue.setCursor(QCursor(Qt.ArrowCursor))
        self.DownloadSettingsWidgetBlue.setAutoFillBackground(False)
        self.DownloadSettingsWidgetBlue.setStyleSheet("QLabel\n"
                                                      "{\n"
                                                      "    background-color: rgb(0, 120, 212);\n"
                                                      "    border-radius: 10px\n"
                                                      "}")
        self.DownloadSettingsWidgetBlue.setText("")
        self.DownloadSettingsWidgetBlue.setObjectName("DownloadSettingsWidgetBlue")
        self.MCSLAPIDownloadSource = QLabel(self.DownloadSettingsWidget)
        self.MCSLAPIDownloadSource.setGeometry(QRect(30, 63, 171, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.MCSLAPIDownloadSource.setFont(font)
        self.MCSLAPIDownloadSource.setObjectName("MCSLAPIDownloadSource")
        self.MCSLAPIDownloadSourceComboBox = QComboBox(self.DownloadSettingsWidget)
        self.MCSLAPIDownloadSourceComboBox.setGeometry(QRect(350, 60, 241, 31))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLAPIDownloadSourceComboBox.sizePolicy().hasHeightForWidth())
        self.MCSLAPIDownloadSourceComboBox.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setKerning(True)
        self.MCSLAPIDownloadSourceComboBox.setFont(font)
        self.MCSLAPIDownloadSourceComboBox.setStyleSheet("QComboBox {\n"
                                                         "    border: 1px solid rgb(238, 239, 238);\n"
                                                         "    border-radius: 5px;\n"
                                                         "    border-bottom: 1px solid rgb(212, 213, 212);\n"
                                                         "    padding: 5px 31px 6px 11px;\n"
                                                         "    color: black;\n"
                                                         "    background-color: rgb(254, 254, 254);\n"
                                                         "    text-align: left;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox:hover {\n"
                                                         "    background-color: rgb(251, 251, 251);\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox:pressed {\n"
                                                         "    background-color: rgb(252, 252, 252);\n"
                                                         "    border-bottom: 1px solid rgb(238, 239, 238);\n"
                                                         "    color: rgba(0, 0, 0, 0.63);\n"
                                                         "}\n"
                                                         "QComboBox::drop-down\n"
                                                         "{\n"
                                                         "    subcontrol-origin: padding;\n"
                                                         "    subcontrol-position: right;\n"
                                                         "    width: 35px;\n"
                                                         "    border-left-style: solid;\n"
                                                         "}\n"
                                                         "QComboBox::down-arrow\n"
                                                         "{\n"
                                                         "    border-image: url(:/MCSL2_Icon/QComboBoxDownArrow.svg);\n"
                                                         "}\n"
                                                         "QComboBox QAbstractItemView {\n"
                                                         "    border: 1px solid rgba(0, 0, 0, 0.1);\n"
                                                         "    border-radius: 9px;\n"
                                                         "    background-color: rgb(249, 249, 249);\n"
                                                         "    outline: none;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox QAbstractItemView::item {\n"
                                                         "    padding-left: 0px;\n"
                                                         "    padding-right: 10px;\n"
                                                         "    border-radius: 5px;\n"
                                                         "    border: none;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox QAbstractItemView::item:hover {\n"
                                                         "    background-color: rgba(0, 0, 0, 9);\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox QAbstractItemView::item:selected {\n"
                                                         "    background-color: rgba(0, 0, 0, 7);\n"
                                                         "    color: black;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox QAbstractItemView::item:selected:active {\n"
                                                         "    background-color: rgba(0, 0, 0, 0.06);\n"
                                                         "    color: rgba(0, 0, 0, 0.7);\n"
                                                         "}")
        self.MCSLAPIDownloadSourceComboBox.setObjectName("MCSLAPIDownloadSourceComboBox")
        self.MCSLAPIDownloadSourceComboBox.addItem("")
        self.MCSLAPIDownloadSourceComboBox.addItem("")
        self.MCSLAPIDownloadSourceComboBox.addItem("")
        self.MCSLAPIDownloadSourceComboBox.addItem("")
        self.MCSLAPIDownloadSourceComboBox.addItem("")
        self.Aria2ThreadCount = QLabel(self.DownloadSettingsWidget)
        self.Aria2ThreadCount.setGeometry(QRect(30, 103, 171, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Aria2ThreadCount.setFont(font)
        self.Aria2ThreadCount.setObjectName("Aria2ThreadCount")
        self.Aria2ThreadCountComboBox = QComboBox(self.DownloadSettingsWidget)
        self.Aria2ThreadCountComboBox.setGeometry(QRect(490, 100, 101, 35))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setKerning(True)
        self.Aria2ThreadCountComboBox.setFont(font)
        self.Aria2ThreadCountComboBox.setStyleSheet("QComboBox {\n"
                                                    "    border: 1px solid rgb(238, 239, 238);\n"
                                                    "    border-radius: 5px;\n"
                                                    "    border-bottom: 1px solid rgb(212, 213, 212);\n"
                                                    "    padding: 5px 31px 6px 11px;\n"
                                                    "    color: black;\n"
                                                    "    background-color: rgb(254, 254, 254);\n"
                                                    "    text-align: left;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QComboBox:hover {\n"
                                                    "    background-color: rgb(251, 251, 251);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QComboBox:pressed {\n"
                                                    "    background-color: rgb(252, 252, 252);\n"
                                                    "    border-bottom: 1px solid rgb(238, 239, 238);\n"
                                                    "    color: rgba(0, 0, 0, 0.63);\n"
                                                    "}\n"
                                                    "QComboBox::drop-down\n"
                                                    "{\n"
                                                    "    subcontrol-origin: padding;\n"
                                                    "    subcontrol-position: right;\n"
                                                    "    width: 35px;\n"
                                                    "    border-left-style: solid;\n"
                                                    "}\n"
                                                    "QComboBox::down-arrow\n"
                                                    "{\n"
                                                    "    border-image: url(:/MCSL2_Icon/QComboBoxDownArrow.svg);\n"
                                                    "}\n"
                                                    "QComboBox QAbstractItemView {\n"
                                                    "    border: 1px solid rgba(0, 0, 0, 0.1);\n"
                                                    "    border-radius: 9px;\n"
                                                    "    background-color: rgb(249, 249, 249);\n"
                                                    "    outline: none;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QComboBox QAbstractItemView::item {\n"
                                                    "    padding-left: 0px;\n"
                                                    "    padding-right: 10px;\n"
                                                    "    border-radius: 5px;\n"
                                                    "    border: none;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QComboBox QAbstractItemView::item:hover {\n"
                                                    "    background-color: rgba(0, 0, 0, 9);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QComboBox QAbstractItemView::item:selected {\n"
                                                    "    background-color: rgba(0, 0, 0, 7);\n"
                                                    "    color: black;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QComboBox QAbstractItemView::item:selected:active {\n"
                                                    "    background-color: rgba(0, 0, 0, 0.06);\n"
                                                    "    color: rgba(0, 0, 0, 0.7);\n"
                                                    "}")
        self.Aria2ThreadCountComboBox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.Aria2ThreadCountComboBox.setFrame(True)
        self.Aria2ThreadCountComboBox.setObjectName("Aria2ThreadCountComboBox")
        self.Aria2ThreadCountComboBox.addItem("")
        self.Aria2ThreadCountComboBox.addItem("")
        self.Aria2ThreadCountComboBox.addItem("")
        self.Aria2ThreadCountComboBox.addItem("")
        self.Aria2ThreadCountComboBox.addItem("")
        self.AlwaysAskDownloadPath = QCheckBox(self.DownloadSettingsWidget)
        self.AlwaysAskDownloadPath.setGeometry(QRect(30, 140, 410, 30))
        self.AlwaysAskDownloadPath.setMinimumSize(QSize(28, 20))
        self.AlwaysAskDownloadPath.setMaximumSize(QSize(410, 30))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.AlwaysAskDownloadPath.setFont(font)
        self.AlwaysAskDownloadPath.setStyleSheet("QCheckBox {\n"
                                                 "    color: black;\n"
                                                 "    spacing: 8px;\n"
                                                 "    min-width: 28px;\n"
                                                 "    min-height: 20px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator {\n"
                                                 "    width: 18px;\n"
                                                 "    height: 18px;\n"
                                                 "    border-radius: 5px;\n"
                                                 "    border: 1px solid rgb(135, 135, 135);\n"
                                                 "    background-color: rgb(241, 241, 241);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:hover {\n"
                                                 "    border: 1px solid rgb(132, 132, 132);\n"
                                                 "    background-color: rgb(232, 232, 232);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:pressed {\n"
                                                 "    border: 1px solid rgb(184, 184, 184);\n"
                                                 "    background-color: rgb(224, 224, 224);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:checked,\n"
                                                 "QCheckBox::indicator:indeterminate {\n"
                                                 "    border: 1px solid rgb(0, 120, 212);\n"
                                                 "    background-color: rgb(0, 120, 212);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:checked {\n"
                                                 "    image: url(:/MCSL2_Icon/QCheckBoxAccept.svg);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:indeterminate {\n"
                                                 "    image: url(:/MCSL2_Icon/QCheckBoxPartialAccept.svg);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:checked:hover,\n"
                                                 "QCheckBox::indicator:indeterminate:hover {\n"
                                                 "    border: 1px solid --ThemeColorLight1;\n"
                                                 "    background-color: --ThemeColorLight1;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:checked:pressed,\n"
                                                 "QCheckBox::indicator:indeterminate:pressed {\n"
                                                 "    border: 1px solid --ThemeColorLight3;\n"
                                                 "    background-color: --ThemeColorLight3;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox:disabled {\n"
                                                 "    color: rgba(0, 0, 0, 110);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:disabled {\n"
                                                 "    border: 1px solid #bbbbbb;\n"
                                                 "    background-color: rgb(224, 224, 224);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QCheckBox::indicator:checked:disabled,\n"
                                                 "QCheckBox::indicator:indeterminate:disabled {\n"
                                                 "    border: 1px solid rgb(199, 199, 199);\n"
                                                 "    background-color: rgb(199, 199, 199);\n"
                                                 "}")
        self.AlwaysAskDownloadPath.setChecked(True)
        self.AlwaysAskDownloadPath.setObjectName("AlwaysAskDownloadPath")
        self.AlwaysAskDownloadPathTip = QLabel(self.DownloadSettingsWidget)
        self.AlwaysAskDownloadPathTip.setGeometry(QRect(60, 170, 451, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.AlwaysAskDownloadPathTip.setFont(font)
        self.AlwaysAskDownloadPathTip.setObjectName("AlwaysAskDownloadPathTip")
        self.SameFileException = QLabel(self.DownloadSettingsWidget)
        self.SameFileException.setGeometry(QRect(30, 203, 221, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.SameFileException.setFont(font)
        self.SameFileException.setObjectName("SameFileException")
        self.SameFileExceptionStop = QRadioButton(self.DownloadSettingsWidget)
        self.SameFileExceptionStop.setGeometry(QRect(510, 200, 81, 24))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.SameFileExceptionStop.setFont(font)
        self.SameFileExceptionStop.setStyleSheet("QRadioButton {\n"
                                                 "    min-height: 24px;\n"
                                                 "    max-height: 24px;\n"
                                                 "    background-color: transparent;\n"
                                                 "    color: black;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QRadioButton::indicator {\n"
                                                 "    width: 16px;\n"
                                                 "    height: 16px;\n"
                                                 "    border-radius: 10px;\n"
                                                 "    border: 2px solid #999999;\n"
                                                 "    background-color: rgba(0, 0, 0, 5);\n"
                                                 "    margin-right: 4px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QRadioButton::indicator:hover {\n"
                                                 "    background-color: rgba(0, 0, 0, 0);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QRadioButton::indicator:pressed {\n"
                                                 "    border: 2px solid #bbbbbb;\n"
                                                 "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                 "            stop:0 rgb(255, 255, 255),\n"
                                                 "            stop:0.5 rgb(255, 255, 255),\n"
                                                 "            stop:0.6 rgb(225, 224, 223),\n"
                                                 "            stop:1 rgb(225, 224, 223));\n"
                                                 "}\n"
                                                 "\n"
                                                 "QRadioButton::indicator:checked {\n"
                                                 "    height: 20px;\n"
                                                 "    width: 20px;\n"
                                                 "    border: none;\n"
                                                 "    border-radius: 10px;\n"
                                                 "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                 "            stop:0 rgb(255, 255, 255),\n"
                                                 "            stop:0.5 rgb(255, 255, 255),\n"
                                                 "            stop:0.6 rgb(0, 120, 212),\n"
                                                 "            stop:1 rgb(0, 120, 212));\n"
                                                 "}\n"
                                                 "\n"
                                                 "QRadioButton::indicator:checked:hover {\n"
                                                 "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                 "            stop:0 rgb(255, 255, 255),\n"
                                                 "            stop:0.6 rgb(255, 255, 255),\n"
                                                 "            stop:0.7 rgb(0, 120, 212),\n"
                                                 "            stop:1 rgb(0, 120, 212));\n"
                                                 "}\n"
                                                 "\n"
                                                 "QRadioButton::indicator:checked:pressed {\n"
                                                 "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                 "            stop:0 rgb(255, 255, 255),\n"
                                                 "            stop:0.5 rgb(255, 255, 255),\n"
                                                 "            stop:0.6 rgb(0, 120, 212),\n"
                                                 "            stop:1 rgb(0, 120, 212));\n"
                                                 "}\n"
                                                 "\n"
                                                 "QRadioButton:disabled {\n"
                                                 "    color: rgba(0, 0, 0, 110);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QRadioButton::indicator:disabled {\n"
                                                 "    border: 2px solid #bbbbbb;\n"
                                                 "    background-color: rgba(0, 0, 0, 0);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QRadioButton::indicator:checked {\n"
                                                 "    height: 20px;\n"
                                                 "    width: 20px;\n"
                                                 "    border: none;\n"
                                                 "    border-radius: 10px;\n"
                                                 "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                 "            stop:0 rgb(255, 255, 255),\n"
                                                 "            stop:0.5 rgb(255, 255, 255),\n"
                                                 "            stop:0.6 rgb(0, 120, 212),\n"
                                                 "            stop:1 rgb(0, 120, 212));\n"
                                                 "}\n"
                                                 "")
        self.SameFileExceptionStop.setObjectName("SameFileExceptionStop")
        self.SameFileExceptionAsk = QRadioButton(self.DownloadSettingsWidget)
        self.SameFileExceptionAsk.setGeometry(QRect(350, 200, 71, 24))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.SameFileExceptionAsk.setFont(font)
        self.SameFileExceptionAsk.setStyleSheet("QRadioButton {\n"
                                                "    min-height: 24px;\n"
                                                "    max-height: 24px;\n"
                                                "    background-color: transparent;\n"
                                                "    color: black;\n"
                                                "}\n"
                                                "\n"
                                                "QRadioButton::indicator {\n"
                                                "    width: 16px;\n"
                                                "    height: 16px;\n"
                                                "    border-radius: 10px;\n"
                                                "    border: 2px solid #999999;\n"
                                                "    background-color: rgba(0, 0, 0, 5);\n"
                                                "    margin-right: 4px;\n"
                                                "}\n"
                                                "\n"
                                                "QRadioButton::indicator:hover {\n"
                                                "    background-color: rgba(0, 0, 0, 0);\n"
                                                "}\n"
                                                "\n"
                                                "QRadioButton::indicator:pressed {\n"
                                                "    border: 2px solid #bbbbbb;\n"
                                                "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                "            stop:0 rgb(255, 255, 255),\n"
                                                "            stop:0.5 rgb(255, 255, 255),\n"
                                                "            stop:0.6 rgb(225, 224, 223),\n"
                                                "            stop:1 rgb(225, 224, 223));\n"
                                                "}\n"
                                                "\n"
                                                "QRadioButton::indicator:checked {\n"
                                                "    height: 20px;\n"
                                                "    width: 20px;\n"
                                                "    border: none;\n"
                                                "    border-radius: 10px;\n"
                                                "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                "            stop:0 rgb(255, 255, 255),\n"
                                                "            stop:0.5 rgb(255, 255, 255),\n"
                                                "            stop:0.6 rgb(0, 120, 212),\n"
                                                "            stop:1 rgb(0, 120, 212));\n"
                                                "}\n"
                                                "\n"
                                                "QRadioButton::indicator:checked:hover {\n"
                                                "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                "            stop:0 rgb(255, 255, 255),\n"
                                                "            stop:0.6 rgb(255, 255, 255),\n"
                                                "            stop:0.7 rgb(0, 120, 212),\n"
                                                "            stop:1 rgb(0, 120, 212));\n"
                                                "}\n"
                                                "\n"
                                                "QRadioButton::indicator:checked:pressed {\n"
                                                "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                "            stop:0 rgb(255, 255, 255),\n"
                                                "            stop:0.5 rgb(255, 255, 255),\n"
                                                "            stop:0.6 rgb(0, 120, 212),\n"
                                                "            stop:1 rgb(0, 120, 212));\n"
                                                "}\n"
                                                "\n"
                                                "QRadioButton:disabled {\n"
                                                "    color: rgba(0, 0, 0, 110);\n"
                                                "}\n"
                                                "\n"
                                                "QRadioButton::indicator:disabled {\n"
                                                "    border: 2px solid #bbbbbb;\n"
                                                "    background-color: rgba(0, 0, 0, 0);\n"
                                                "}\n"
                                                "\n"
                                                "QRadioButton::indicator:checked {\n"
                                                "    height: 20px;\n"
                                                "    width: 20px;\n"
                                                "    border: none;\n"
                                                "    border-radius: 10px;\n"
                                                "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                "            stop:0 rgb(255, 255, 255),\n"
                                                "            stop:0.5 rgb(255, 255, 255),\n"
                                                "            stop:0.6 rgb(0, 120, 212),\n"
                                                "            stop:1 rgb(0, 120, 212));\n"
                                                "}\n"
                                                "")
        self.SameFileExceptionAsk.setChecked(True)
        self.SameFileExceptionAsk.setObjectName("SameFileExceptionAsk")
        self.SameFileExceptionReWrite = QRadioButton(self.DownloadSettingsWidget)
        self.SameFileExceptionReWrite.setGeometry(QRect(430, 200, 71, 24))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.SameFileExceptionReWrite.setFont(font)
        self.SameFileExceptionReWrite.setStyleSheet("QRadioButton {\n"
                                                    "    min-height: 24px;\n"
                                                    "    max-height: 24px;\n"
                                                    "    background-color: transparent;\n"
                                                    "    color: black;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QRadioButton::indicator {\n"
                                                    "    width: 16px;\n"
                                                    "    height: 16px;\n"
                                                    "    border-radius: 10px;\n"
                                                    "    border: 2px solid #999999;\n"
                                                    "    background-color: rgba(0, 0, 0, 5);\n"
                                                    "    margin-right: 4px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QRadioButton::indicator:hover {\n"
                                                    "    background-color: rgba(0, 0, 0, 0);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QRadioButton::indicator:pressed {\n"
                                                    "    border: 2px solid #bbbbbb;\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "            stop:0 rgb(255, 255, 255),\n"
                                                    "            stop:0.5 rgb(255, 255, 255),\n"
                                                    "            stop:0.6 rgb(225, 224, 223),\n"
                                                    "            stop:1 rgb(225, 224, 223));\n"
                                                    "}\n"
                                                    "\n"
                                                    "QRadioButton::indicator:checked {\n"
                                                    "    height: 20px;\n"
                                                    "    width: 20px;\n"
                                                    "    border: none;\n"
                                                    "    border-radius: 10px;\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "            stop:0 rgb(255, 255, 255),\n"
                                                    "            stop:0.5 rgb(255, 255, 255),\n"
                                                    "            stop:0.6 rgb(0, 120, 212),\n"
                                                    "            stop:1 rgb(0, 120, 212));\n"
                                                    "}\n"
                                                    "\n"
                                                    "QRadioButton::indicator:checked:hover {\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "            stop:0 rgb(255, 255, 255),\n"
                                                    "            stop:0.6 rgb(255, 255, 255),\n"
                                                    "            stop:0.7 rgb(0, 120, 212),\n"
                                                    "            stop:1 rgb(0, 120, 212));\n"
                                                    "}\n"
                                                    "\n"
                                                    "QRadioButton::indicator:checked:pressed {\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "            stop:0 rgb(255, 255, 255),\n"
                                                    "            stop:0.5 rgb(255, 255, 255),\n"
                                                    "            stop:0.6 rgb(0, 120, 212),\n"
                                                    "            stop:1 rgb(0, 120, 212));\n"
                                                    "}\n"
                                                    "\n"
                                                    "QRadioButton:disabled {\n"
                                                    "    color: rgba(0, 0, 0, 110);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QRadioButton::indicator:disabled {\n"
                                                    "    border: 2px solid #bbbbbb;\n"
                                                    "    background-color: rgba(0, 0, 0, 0);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QRadioButton::indicator:checked {\n"
                                                    "    height: 20px;\n"
                                                    "    width: 20px;\n"
                                                    "    border: none;\n"
                                                    "    border-radius: 10px;\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "            stop:0 rgb(255, 255, 255),\n"
                                                    "            stop:0.5 rgb(255, 255, 255),\n"
                                                    "            stop:0.6 rgb(0, 120, 212),\n"
                                                    "            stop:1 rgb(0, 120, 212));\n"
                                                    "}\n"
                                                    "")
        self.SameFileExceptionReWrite.setObjectName("SameFileExceptionReWrite")
        self.SettingsVerticalLayout.addWidget(self.DownloadSettingsWidget)
        self.ConsoleSettingsWidget = QWidget(self.SettingsScrollAreaWidgetContents)
        self.ConsoleSettingsWidget.setMinimumSize(QSize(620, 195))
        self.ConsoleSettingsWidget.setMaximumSize(QSize(620, 195))
        self.ConsoleSettingsWidget.setStyleSheet("QWidget\n"
                                                 "{\n"
                                                 "    border-radius: 7px;\n"
                                                 "    background-color: rgba(247, 247, 247, 247)\n"
                                                 "}")
        self.ConsoleSettingsWidget.setObjectName("ConsoleSettingsWidget")
        self.ConsoleSettingsTitle = QWidget(self.ConsoleSettingsWidget)
        self.ConsoleSettingsTitle.setGeometry(QRect(20, 10, 120, 40))
        self.ConsoleSettingsTitle.setMinimumSize(QSize(120, 40))
        self.ConsoleSettingsTitle.setStyleSheet("QWidget\n"
                                                "{\n"
                                                "    background-color: rgb(247, 247, 247);\n"
                                                "    border-radius: 10px\n"
                                                "}")
        self.ConsoleSettingsTitle.setObjectName("ConsoleSettingsTitle")
        self.ConsoleSettingsWidgetTitleLabel = QLabel(self.ConsoleSettingsTitle)
        self.ConsoleSettingsWidgetTitleLabel.setGeometry(QRect(30, 10, 81, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.ConsoleSettingsWidgetTitleLabel.setFont(font)
        self.ConsoleSettingsWidgetTitleLabel.setObjectName("ConsoleSettingsWidgetTitleLabel")
        self.ConsoleSettingsWidgetBlue = QLabel(self.ConsoleSettingsTitle)
        self.ConsoleSettingsWidgetBlue.setGeometry(QRect(10, 10, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.ConsoleSettingsWidgetBlue.setFont(font)
        self.ConsoleSettingsWidgetBlue.setCursor(QCursor(Qt.ArrowCursor))
        self.ConsoleSettingsWidgetBlue.setAutoFillBackground(False)
        self.ConsoleSettingsWidgetBlue.setStyleSheet("QLabel\n"
                                                     "{\n"
                                                     "    background-color: rgb(0, 120, 212);\n"
                                                     "    border-radius: 10px\n"
                                                     "}")
        self.ConsoleSettingsWidgetBlue.setText("")
        self.ConsoleSettingsWidgetBlue.setObjectName("ConsoleSettingsWidgetBlue")
        self.ConsoleOutputEncoding = QLabel(self.ConsoleSettingsWidget)
        self.ConsoleOutputEncoding.setGeometry(QRect(30, 103, 171, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.ConsoleOutputEncoding.setFont(font)
        self.ConsoleOutputEncoding.setObjectName("ConsoleOutputEncoding")
        self.ConsoleOutputEncodingComboBox = QComboBox(self.ConsoleSettingsWidget)
        self.ConsoleOutputEncodingComboBox.setGeometry(QRect(350, 100, 241, 31))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ConsoleOutputEncodingComboBox.sizePolicy().hasHeightForWidth())
        self.ConsoleOutputEncodingComboBox.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setKerning(True)
        self.ConsoleOutputEncodingComboBox.setFont(font)
        self.ConsoleOutputEncodingComboBox.setStyleSheet("QComboBox {\n"
                                                         "    border: 1px solid rgb(238, 239, 238);\n"
                                                         "    border-radius: 5px;\n"
                                                         "    border-bottom: 1px solid rgb(212, 213, 212);\n"
                                                         "    padding: 5px 31px 6px 11px;\n"
                                                         "    color: black;\n"
                                                         "    background-color: rgb(254, 254, 254);\n"
                                                         "    text-align: left;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox:hover {\n"
                                                         "    background-color: rgb(251, 251, 251);\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox:pressed {\n"
                                                         "    background-color: rgb(252, 252, 252);\n"
                                                         "    border-bottom: 1px solid rgb(238, 239, 238);\n"
                                                         "    color: rgba(0, 0, 0, 0.63);\n"
                                                         "}\n"
                                                         "QComboBox::drop-down\n"
                                                         "{\n"
                                                         "    subcontrol-origin: padding;\n"
                                                         "    subcontrol-position: right;\n"
                                                         "    width: 35px;\n"
                                                         "    border-left-style: solid;\n"
                                                         "}\n"
                                                         "QComboBox::down-arrow\n"
                                                         "{\n"
                                                         "    border-image: url(:/MCSL2_Icon/QComboBoxDownArrow.svg);\n"
                                                         "}\n"
                                                         "QComboBox QAbstractItemView {\n"
                                                         "    border: 1px solid rgba(0, 0, 0, 0.1);\n"
                                                         "    border-radius: 9px;\n"
                                                         "    background-color: rgb(249, 249, 249);\n"
                                                         "    outline: none;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox QAbstractItemView::item {\n"
                                                         "    padding-left: 0px;\n"
                                                         "    padding-right: 10px;\n"
                                                         "    border-radius: 5px;\n"
                                                         "    border: none;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox QAbstractItemView::item:hover {\n"
                                                         "    background-color: rgba(0, 0, 0, 9);\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox QAbstractItemView::item:selected {\n"
                                                         "    background-color: rgba(0, 0, 0, 7);\n"
                                                         "    color: black;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QComboBox QAbstractItemView::item:selected:active {\n"
                                                         "    background-color: rgba(0, 0, 0, 0.06);\n"
                                                         "    color: rgba(0, 0, 0, 0.7);\n"
                                                         "}")
        self.ConsoleOutputEncodingComboBox.setObjectName("ConsoleOutputEncodingComboBox")
        self.ConsoleOutputEncodingComboBox.addItem("")
        self.ConsoleOutputEncodingComboBox.addItem("")
        self.ConsoleInputDecoding = QLabel(self.ConsoleSettingsWidget)
        self.ConsoleInputDecoding.setGeometry(QRect(30, 143, 171, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.ConsoleInputDecoding.setFont(font)
        self.ConsoleInputDecoding.setObjectName("ConsoleInputDecoding")
        self.ConsoleInputDecodingComboBox = QComboBox(self.ConsoleSettingsWidget)
        self.ConsoleInputDecodingComboBox.setGeometry(QRect(350, 140, 241, 35))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setKerning(True)
        self.ConsoleInputDecodingComboBox.setFont(font)
        self.ConsoleInputDecodingComboBox.setStyleSheet("QComboBox {\n"
                                                        "    border: 1px solid rgb(238, 239, 238);\n"
                                                        "    border-radius: 5px;\n"
                                                        "    border-bottom: 1px solid rgb(212, 213, 212);\n"
                                                        "    padding: 5px 31px 6px 11px;\n"
                                                        "    color: black;\n"
                                                        "    background-color: rgb(254, 254, 254);\n"
                                                        "    text-align: left;\n"
                                                        "}\n"
                                                        "\n"
                                                        "QComboBox:hover {\n"
                                                        "    background-color: rgb(251, 251, 251);\n"
                                                        "}\n"
                                                        "\n"
                                                        "QComboBox:pressed {\n"
                                                        "    background-color: rgb(252, 252, 252);\n"
                                                        "    border-bottom: 1px solid rgb(238, 239, 238);\n"
                                                        "    color: rgba(0, 0, 0, 0.63);\n"
                                                        "}\n"
                                                        "QComboBox::drop-down\n"
                                                        "{\n"
                                                        "    subcontrol-origin: padding;\n"
                                                        "    subcontrol-position: right;\n"
                                                        "    width: 35px;\n"
                                                        "    border-left-style: solid;\n"
                                                        "}\n"
                                                        "QComboBox::down-arrow\n"
                                                        "{\n"
                                                        "    border-image: url(:/MCSL2_Icon/QComboBoxDownArrow.svg);\n"
                                                        "}\n"
                                                        "QComboBox QAbstractItemView {\n"
                                                        "    border: 1px solid rgba(0, 0, 0, 0.1);\n"
                                                        "    border-radius: 9px;\n"
                                                        "    background-color: rgb(249, 249, 249);\n"
                                                        "    outline: none;\n"
                                                        "}\n"
                                                        "\n"
                                                        "QComboBox QAbstractItemView::item {\n"
                                                        "    padding-left: 0px;\n"
                                                        "    padding-right: 10px;\n"
                                                        "    border-radius: 5px;\n"
                                                        "    border: none;\n"
                                                        "}\n"
                                                        "\n"
                                                        "QComboBox QAbstractItemView::item:hover {\n"
                                                        "    background-color: rgba(0, 0, 0, 9);\n"
                                                        "}\n"
                                                        "\n"
                                                        "QComboBox QAbstractItemView::item:selected {\n"
                                                        "    background-color: rgba(0, 0, 0, 7);\n"
                                                        "    color: black;\n"
                                                        "}\n"
                                                        "\n"
                                                        "QComboBox QAbstractItemView::item:selected:active {\n"
                                                        "    background-color: rgba(0, 0, 0, 0.06);\n"
                                                        "    color: rgba(0, 0, 0, 0.7);\n"
                                                        "}")
        self.ConsoleInputDecodingComboBox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.ConsoleInputDecodingComboBox.setFrame(True)
        self.ConsoleInputDecodingComboBox.setObjectName("ConsoleInputDecodingComboBox")
        self.ConsoleInputDecodingComboBox.addItem("")
        self.ConsoleInputDecodingComboBox.addItem("")
        self.ConsoleInputDecodingComboBox.addItem("")
        self.EnableQuickMenu = QCheckBox(self.ConsoleSettingsWidget)
        self.EnableQuickMenu.setGeometry(QRect(30, 60, 410, 30))
        self.EnableQuickMenu.setMinimumSize(QSize(28, 20))
        self.EnableQuickMenu.setMaximumSize(QSize(410, 30))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.EnableQuickMenu.setFont(font)
        self.EnableQuickMenu.setStyleSheet("QCheckBox {\n"
                                           "    color: black;\n"
                                           "    spacing: 8px;\n"
                                           "    min-width: 28px;\n"
                                           "    min-height: 20px;\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator {\n"
                                           "    width: 18px;\n"
                                           "    height: 18px;\n"
                                           "    border-radius: 5px;\n"
                                           "    border: 1px solid rgb(135, 135, 135);\n"
                                           "    background-color: rgb(241, 241, 241);\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:hover {\n"
                                           "    border: 1px solid rgb(132, 132, 132);\n"
                                           "    background-color: rgb(232, 232, 232);\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:pressed {\n"
                                           "    border: 1px solid rgb(184, 184, 184);\n"
                                           "    background-color: rgb(224, 224, 224);\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:checked,\n"
                                           "QCheckBox::indicator:indeterminate {\n"
                                           "    border: 1px solid rgb(0, 120, 212);\n"
                                           "    background-color: rgb(0, 120, 212);\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:checked {\n"
                                           "    image: url(:/MCSL2_Icon/QCheckBoxAccept.svg);\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:indeterminate {\n"
                                           "    image: url(:/MCSL2_Icon/QCheckBoxPartialAccept.svg);\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:checked:hover,\n"
                                           "QCheckBox::indicator:indeterminate:hover {\n"
                                           "    border: 1px solid --ThemeColorLight1;\n"
                                           "    background-color: --ThemeColorLight1;\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:checked:pressed,\n"
                                           "QCheckBox::indicator:indeterminate:pressed {\n"
                                           "    border: 1px solid --ThemeColorLight3;\n"
                                           "    background-color: --ThemeColorLight3;\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox:disabled {\n"
                                           "    color: rgba(0, 0, 0, 110);\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:disabled {\n"
                                           "    border: 1px solid #bbbbbb;\n"
                                           "    background-color: rgb(224, 224, 224);\n"
                                           "}\n"
                                           "\n"
                                           "QCheckBox::indicator:checked:disabled,\n"
                                           "QCheckBox::indicator:indeterminate:disabled {\n"
                                           "    border: 1px solid rgb(199, 199, 199);\n"
                                           "    background-color: rgb(199, 199, 199);\n"
                                           "}")
        self.EnableQuickMenu.setChecked(True)
        self.EnableQuickMenu.setObjectName("EnableQuickMenu")
        self.SettingsVerticalLayout.addWidget(self.ConsoleSettingsWidget)
        self.UISettingsWidget = QWidget(self.SettingsScrollAreaWidgetContents)
        self.UISettingsWidget.setMinimumSize(QSize(620, 200))
        self.UISettingsWidget.setMaximumSize(QSize(620, 200))
        self.UISettingsWidget.setStyleSheet("QWidget\n"
                                            "{\n"
                                            "    border-radius: 7px;\n"
                                            "    background-color: rgba(247, 247, 247, 247)\n"
                                            "}")
        self.UISettingsWidget.setObjectName("UISettingsWidget")
        self.UISettingsTitle = QWidget(self.UISettingsWidget)
        self.UISettingsTitle.setGeometry(QRect(20, 10, 120, 40))
        self.UISettingsTitle.setMinimumSize(QSize(120, 40))
        self.UISettingsTitle.setStyleSheet("QWidget\n"
                                           "{\n"
                                           "    background-color: rgb(247, 247, 247);\n"
                                           "    border-radius: 10px\n"
                                           "}")
        self.UISettingsTitle.setObjectName("UISettingsTitle")
        self.UISettingsWidgetTitleLabel = QLabel(self.UISettingsTitle)
        self.UISettingsWidgetTitleLabel.setGeometry(QRect(30, 10, 81, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.UISettingsWidgetTitleLabel.setFont(font)
        self.UISettingsWidgetTitleLabel.setObjectName("UISettingsWidgetTitleLabel")
        self.UISettingsWidgetBlue = QLabel(self.UISettingsTitle)
        self.UISettingsWidgetBlue.setGeometry(QRect(10, 10, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.UISettingsWidgetBlue.setFont(font)
        self.UISettingsWidgetBlue.setCursor(QCursor(Qt.ArrowCursor))
        self.UISettingsWidgetBlue.setAutoFillBackground(False)
        self.UISettingsWidgetBlue.setStyleSheet("QLabel\n"
                                                "{\n"
                                                "    background-color: rgb(0, 120, 212);\n"
                                                "    border-radius: 10px\n"
                                                "}")
        self.UISettingsWidgetBlue.setText("")
        self.UISettingsWidgetBlue.setObjectName("UISettingsWidgetBlue")
        self.TransparentSetting = QLabel(self.UISettingsWidget)
        self.TransparentSetting.setGeometry(QRect(30, 60, 171, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.TransparentSetting.setFont(font)
        self.TransparentSetting.setObjectName("TransparentSetting")
        self.DarkMode = QLabel(self.UISettingsWidget)
        self.DarkMode.setGeometry(QRect(30, 143, 171, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.DarkMode.setFont(font)
        self.DarkMode.setObjectName("DarkMode")
        self.DarkModeComboBox = QComboBox(self.UISettingsWidget)
        self.DarkModeComboBox.setGeometry(QRect(470, 144, 121, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setKerning(True)
        self.DarkModeComboBox.setFont(font)
        self.DarkModeComboBox.setStyleSheet("QComboBox {\n"
                                            "    border: 1px solid rgb(238, 239, 238);\n"
                                            "    border-radius: 5px;\n"
                                            "    border-bottom: 1px solid rgb(212, 213, 212);\n"
                                            "    padding: 5px 31px 6px 11px;\n"
                                            "    color: black;\n"
                                            "    background-color: rgb(254, 254, 254);\n"
                                            "    text-align: left;\n"
                                            "}\n"
                                            "\n"
                                            "QComboBox:hover {\n"
                                            "    background-color: rgb(251, 251, 251);\n"
                                            "}\n"
                                            "\n"
                                            "QComboBox:pressed {\n"
                                            "    background-color: rgb(252, 252, 252);\n"
                                            "    border-bottom: 1px solid rgb(238, 239, 238);\n"
                                            "    color: rgba(0, 0, 0, 0.63);\n"
                                            "}\n"
                                            "QComboBox::drop-down\n"
                                            "{\n"
                                            "    subcontrol-origin: padding;\n"
                                            "    subcontrol-position: right;\n"
                                            "    width: 35px;\n"
                                            "    border-left-style: solid;\n"
                                            "}\n"
                                            "QComboBox::down-arrow\n"
                                            "{\n"
                                            "    border-image: url(:/MCSL2_Icon/QComboBoxDownArrow.svg);\n"
                                            "}\n"
                                            "QComboBox QAbstractItemView {\n"
                                            "    border: 1px solid rgba(0, 0, 0, 0.1);\n"
                                            "    border-radius: 9px;\n"
                                            "    background-color: rgb(249, 249, 249);\n"
                                            "    outline: none;\n"
                                            "}\n"
                                            "\n"
                                            "QComboBox QAbstractItemView::item {\n"
                                            "    padding-left: 0px;\n"
                                            "    padding-right: 10px;\n"
                                            "    border-radius: 5px;\n"
                                            "    border: none;\n"
                                            "}\n"
                                            "\n"
                                            "QComboBox QAbstractItemView::item:hover {\n"
                                            "    background-color: rgba(0, 0, 0, 9);\n"
                                            "}\n"
                                            "\n"
                                            "QComboBox QAbstractItemView::item:selected {\n"
                                            "    background-color: rgba(0, 0, 0, 7);\n"
                                            "    color: black;\n"
                                            "}\n"
                                            "\n"
                                            "QComboBox QAbstractItemView::item:selected:active {\n"
                                            "    background-color: rgba(0, 0, 0, 0.06);\n"
                                            "    color: rgba(0, 0, 0, 0.7);\n"
                                            "}")
        self.DarkModeComboBox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.DarkModeComboBox.setFrame(True)
        self.DarkModeComboBox.setObjectName("DarkModeComboBox")
        self.DarkModeComboBox.addItem("")
        self.DarkModeComboBox.addItem("")
        self.DarkModeComboBox.addItem("")
        self.ExchangeButton = QCheckBox(self.UISettingsWidget)
        self.ExchangeButton.setGeometry(QRect(30, 100, 261, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.ExchangeButton.setFont(font)
        self.ExchangeButton.setStyleSheet("QCheckBox {\n"
                                          "    color: black;\n"
                                          "    spacing: 8px;\n"
                                          "    min-width: 28px;\n"
                                          "    min-height: 20px;\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator {\n"
                                          "    width: 18px;\n"
                                          "    height: 18px;\n"
                                          "    border-radius: 5px;\n"
                                          "    border: 1px solid rgb(135, 135, 135);\n"
                                          "    background-color: rgb(241, 241, 241);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:hover {\n"
                                          "    border: 1px solid rgb(132, 132, 132);\n"
                                          "    background-color: rgb(232, 232, 232);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:pressed {\n"
                                          "    border: 1px solid rgb(184, 184, 184);\n"
                                          "    background-color: rgb(224, 224, 224);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:checked,\n"
                                          "QCheckBox::indicator:indeterminate {\n"
                                          "    border: 1px solid rgb(0, 120, 212);\n"
                                          "    background-color: rgb(0, 120, 212);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:checked {\n"
                                          "    image: url(:/MCSL2_Icon/QCheckBoxAccept.svg);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:indeterminate {\n"
                                          "    image: url(:/MCSL2_Icon/QCheckBoxPartialAccept.svg);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:checked:hover,\n"
                                          "QCheckBox::indicator:indeterminate:hover {\n"
                                          "    border: 1px solid --ThemeColorLight1;\n"
                                          "    background-color: --ThemeColorLight1;\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:checked:pressed,\n"
                                          "QCheckBox::indicator:indeterminate:pressed {\n"
                                          "    border: 1px solid --ThemeColorLight3;\n"
                                          "    background-color: --ThemeColorLight3;\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox:disabled {\n"
                                          "    color: rgba(0, 0, 0, 110);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:disabled {\n"
                                          "    border: 1px solid #bbbbbb;\n"
                                          "    background-color: rgb(224, 224, 224);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:checked:disabled,\n"
                                          "QCheckBox::indicator:indeterminate:disabled {\n"
                                          "    border: 1px solid rgb(199, 199, 199);\n"
                                          "    background-color: rgb(199, 199, 199);\n"
                                          "}")
        self.ExchangeButton.setIconSize(QSize(32, 32))
        self.ExchangeButton.setCheckable(True)
        self.ExchangeButton.setChecked(False)
        self.ExchangeButton.setObjectName("ExchangeButton")
        self.TransparentPercentSlider = QSlider(self.UISettingsWidget)
        self.TransparentPercentSlider.setGeometry(QRect(370, 70, 181, 24))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.TransparentPercentSlider.setFont(font)
        self.TransparentPercentSlider.setStyleSheet("QSlider:horizontal {\n"
                                                    "    min-height: 24px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::groove:horizontal {\n"
                                                    "    height: 4px;\n"
                                                    "    background-color: rgba(0, 0, 0, 100);\n"
                                                    "    border-radius: 2px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::sub-page:horizontal {\n"
                                                    "    background: rgb(0, 120, 212);\n"
                                                    "    height: 4px;\n"
                                                    "    border-radius: 2px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::handle:horizontal {\n"
                                                    "    border: 1px solid rgb(222, 222, 222);\n"
                                                    "    width: 20px;\n"
                                                    "    min-height: 24px;\n"
                                                    "    margin: -9px 0;\n"
                                                    "    border-radius: 11px;\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "        stop:0 rgb(0, 120, 212),\n"
                                                    "        stop:0.48 rgb(0, 120, 212),\n"
                                                    "        stop:0.55 rgb(255, 255, 255),\n"
                                                    "        stop:1 rgb(255, 255, 255));\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::handle:horizontal:hover {\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "        stop:0 rgb(0, 120, 212),\n"
                                                    "        stop:0.55 rgb(0, 120, 212),\n"
                                                    "        stop:0.65 rgb(255, 255, 255),\n"
                                                    "        stop:1 rgb(255, 255, 255));\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::handle:horizontal:pressed {\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "        stop:0 rgb(0, 120, 212),\n"
                                                    "        stop:0.4 rgb(0, 120, 212),\n"
                                                    "        stop:0.5 rgb(255, 255, 255),\n"
                                                    "        stop:1 rgb(255, 255, 255));\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::groove:horizontal:disabled {\n"
                                                    "    background-color: rgba(0, 0, 0, 75);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::handle:horizontal:disabled {\n"
                                                    "    background-color: #808080;\n"
                                                    "    border: 5px solid #cccccc;\n"
                                                    "}\n"
                                                    "\n"
                                                    "\n"
                                                    "QSlider:vertical {\n"
                                                    "    min-width: 24px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::groove:vertical {\n"
                                                    "    width: 4px;\n"
                                                    "    background-color: rgba(0, 0, 0, 100);\n"
                                                    "    border-radius: 2px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::add-page:vertical {\n"
                                                    "    background: rgb(0, 120, 212);\n"
                                                    "    width: 4px;\n"
                                                    "    border-radius: 2px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::handle:vertical {\n"
                                                    "    border: 1px solid rgb(222, 222, 222);\n"
                                                    "    height: 20px;\n"
                                                    "    min-width: 24px;\n"
                                                    "    margin: 0 -9px;\n"
                                                    "    border-radius: 11px;\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "        stop:0 rgb(0, 120, 212),\n"
                                                    "        stop:0.48 rgb(0, 120, 212),\n"
                                                    "        stop:0.55 rgb(255, 255, 255),\n"
                                                    "        stop:1 rgb(255, 255, 255));\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::handle:vertical:hover {\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "        stop:0 rgb(0, 120, 212),\n"
                                                    "        stop:0.55 rgb(0, 120, 212),\n"
                                                    "        stop:0.65 rgb(255, 255, 255),\n"
                                                    "        stop:1 rgb(255, 255, 255));\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::handle:vertical:pressed {\n"
                                                    "    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,\n"
                                                    "        stop:0 rgb(0, 120, 212),\n"
                                                    "        stop:0.4 rgb(0, 120, 212),\n"
                                                    "        stop:0.5 rgb(255, 255, 255),\n"
                                                    "        stop:1 rgb(255, 255, 255));\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::groove:vertical:disabled {\n"
                                                    "    background-color: rgba(0, 0, 0, 75);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider::handle:vertical:disabled {\n"
                                                    "    background-color: #808080;\n"
                                                    "    border: 5px solid #cccccc;\n"
                                                    "}\n"
                                                    "")
        self.TransparentPercentSlider.setMaximum(100)
        self.TransparentPercentSlider.setProperty("value", 55)
        self.TransparentPercentSlider.setOrientation(Qt.Horizontal)
        self.TransparentPercentSlider.setInvertedAppearance(False)
        self.TransparentPercentSlider.setTickPosition(QSlider.NoTicks)
        self.TransparentPercentSlider.setObjectName("TransparentPercentSlider")
        self.TransparentPercentNum = QLabel(self.UISettingsWidget)
        self.TransparentPercentNum.setGeometry(QRect(560, 60, 31, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.TransparentPercentNum.setFont(font)
        self.TransparentPercentNum.setObjectName("TransparentPercentNum")
        self.SettingsVerticalLayout.addWidget(self.UISettingsWidget)
        self.SoftwareSettingsWidget = QWidget(self.SettingsScrollAreaWidgetContents)
        self.SoftwareSettingsWidget.setMinimumSize(QSize(620, 160))
        self.SoftwareSettingsWidget.setMaximumSize(QSize(620, 160))
        self.SoftwareSettingsWidget.setStyleSheet("QWidget\n"
                                                  "{\n"
                                                  "    border-radius: 7px;\n"
                                                  "    background-color: rgba(247, 247, 247, 247)\n"
                                                  "}")
        self.SoftwareSettingsWidget.setObjectName("SoftwareSettingsWidget")
        self.AlwaysRunAsAdministrator = QCheckBox(self.SoftwareSettingsWidget)
        self.AlwaysRunAsAdministrator.setGeometry(QRect(30, 93, 410, 30))
        self.AlwaysRunAsAdministrator.setMinimumSize(QSize(28, 20))
        self.AlwaysRunAsAdministrator.setMaximumSize(QSize(410, 30))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.AlwaysRunAsAdministrator.setFont(font)
        self.AlwaysRunAsAdministrator.setStyleSheet("QCheckBox {\n"
                                                    "    color: black;\n"
                                                    "    spacing: 8px;\n"
                                                    "    min-width: 28px;\n"
                                                    "    min-height: 20px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator {\n"
                                                    "    width: 18px;\n"
                                                    "    height: 18px;\n"
                                                    "    border-radius: 5px;\n"
                                                    "    border: 1px solid rgb(135, 135, 135);\n"
                                                    "    background-color: rgb(241, 241, 241);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:hover {\n"
                                                    "    border: 1px solid rgb(132, 132, 132);\n"
                                                    "    background-color: rgb(232, 232, 232);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:pressed {\n"
                                                    "    border: 1px solid rgb(184, 184, 184);\n"
                                                    "    background-color: rgb(224, 224, 224);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked,\n"
                                                    "QCheckBox::indicator:indeterminate {\n"
                                                    "    border: 1px solid rgb(0, 120, 212);\n"
                                                    "    background-color: rgb(0, 120, 212);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked {\n"
                                                    "    image: url(:/MCSL2_Icon/QCheckBoxAccept.svg);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:indeterminate {\n"
                                                    "    image: url(:/MCSL2_Icon/QCheckBoxPartialAccept.svg);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked:hover,\n"
                                                    "QCheckBox::indicator:indeterminate:hover {\n"
                                                    "    border: 1px solid --ThemeColorLight1;\n"
                                                    "    background-color: --ThemeColorLight1;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked:pressed,\n"
                                                    "QCheckBox::indicator:indeterminate:pressed {\n"
                                                    "    border: 1px solid --ThemeColorLight3;\n"
                                                    "    background-color: --ThemeColorLight3;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox:disabled {\n"
                                                    "    color: rgba(0, 0, 0, 110);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:disabled {\n"
                                                    "    border: 1px solid #bbbbbb;\n"
                                                    "    background-color: rgb(224, 224, 224);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QCheckBox::indicator:checked:disabled,\n"
                                                    "QCheckBox::indicator:indeterminate:disabled {\n"
                                                    "    border: 1px solid rgb(199, 199, 199);\n"
                                                    "    background-color: rgb(199, 199, 199);\n"
                                                    "}")
        self.AlwaysRunAsAdministrator.setObjectName("AlwaysRunAsAdministrator")
        self.SoftwareSettingsTitle = QWidget(self.SoftwareSettingsWidget)
        self.SoftwareSettingsTitle.setGeometry(QRect(20, 10, 120, 40))
        self.SoftwareSettingsTitle.setMinimumSize(QSize(120, 40))
        self.SoftwareSettingsTitle.setStyleSheet("QWidget\n"
                                                 "{\n"
                                                 "    background-color: rgb(247, 247, 247);\n"
                                                 "    border-radius: 10px\n"
                                                 "}")
        self.SoftwareSettingsTitle.setObjectName("SoftwareSettingsTitle")
        self.SoftwareSettingsWidgetTitleLabel = QLabel(self.SoftwareSettingsTitle)
        self.SoftwareSettingsWidgetTitleLabel.setGeometry(QRect(30, 10, 81, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.SoftwareSettingsWidgetTitleLabel.setFont(font)
        self.SoftwareSettingsWidgetTitleLabel.setObjectName("SoftwareSettingsWidgetTitleLabel")
        self.SoftwareSettingsWidgetBlue = QLabel(self.SoftwareSettingsTitle)
        self.SoftwareSettingsWidgetBlue.setGeometry(QRect(10, 10, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.SoftwareSettingsWidgetBlue.setFont(font)
        self.SoftwareSettingsWidgetBlue.setCursor(QCursor(Qt.ArrowCursor))
        self.SoftwareSettingsWidgetBlue.setAutoFillBackground(False)
        self.SoftwareSettingsWidgetBlue.setStyleSheet("QLabel\n"
                                                      "{\n"
                                                      "    background-color: rgb(0, 120, 212);\n"
                                                      "    border-radius: 10px\n"
                                                      "}")
        self.SoftwareSettingsWidgetBlue.setText("")
        self.SoftwareSettingsWidgetBlue.setObjectName("SoftwareSettingsWidgetBlue")
        self.StartOnStartup = QCheckBox(self.SoftwareSettingsWidget)
        self.StartOnStartup.setGeometry(QRect(30, 60, 410, 30))
        self.StartOnStartup.setMinimumSize(QSize(28, 20))
        self.StartOnStartup.setMaximumSize(QSize(410, 30))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.StartOnStartup.setFont(font)
        self.StartOnStartup.setStyleSheet("QCheckBox {\n"
                                          "    color: black;\n"
                                          "    spacing: 8px;\n"
                                          "    min-width: 28px;\n"
                                          "    min-height: 20px;\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator {\n"
                                          "    width: 18px;\n"
                                          "    height: 18px;\n"
                                          "    border-radius: 5px;\n"
                                          "    border: 1px solid rgb(135, 135, 135);\n"
                                          "    background-color: rgb(241, 241, 241);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:hover {\n"
                                          "    border: 1px solid rgb(132, 132, 132);\n"
                                          "    background-color: rgb(232, 232, 232);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:pressed {\n"
                                          "    border: 1px solid rgb(184, 184, 184);\n"
                                          "    background-color: rgb(224, 224, 224);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:checked,\n"
                                          "QCheckBox::indicator:indeterminate {\n"
                                          "    border: 1px solid rgb(0, 120, 212);\n"
                                          "    background-color: rgb(0, 120, 212);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:checked {\n"
                                          "    image: url(:/MCSL2_Icon/QCheckBoxAccept.svg);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:indeterminate {\n"
                                          "    image: url(:/MCSL2_Icon/QCheckBoxPartialAccept.svg);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:checked:hover,\n"
                                          "QCheckBox::indicator:indeterminate:hover {\n"
                                          "    border: 1px solid --ThemeColorLight1;\n"
                                          "    background-color: --ThemeColorLight1;\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:checked:pressed,\n"
                                          "QCheckBox::indicator:indeterminate:pressed {\n"
                                          "    border: 1px solid --ThemeColorLight3;\n"
                                          "    background-color: --ThemeColorLight3;\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox:disabled {\n"
                                          "    color: rgba(0, 0, 0, 110);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:disabled {\n"
                                          "    border: 1px solid #bbbbbb;\n"
                                          "    background-color: rgb(224, 224, 224);\n"
                                          "}\n"
                                          "\n"
                                          "QCheckBox::indicator:checked:disabled,\n"
                                          "QCheckBox::indicator:indeterminate:disabled {\n"
                                          "    border: 1px solid rgb(199, 199, 199);\n"
                                          "    background-color: rgb(199, 199, 199);\n"
                                          "}")
        self.StartOnStartup.setObjectName("StartOnStartup")
        self.SettingsVerticalLayout.addWidget(self.SoftwareSettingsWidget)
        self.UpdaterWidget = QWidget(self.SettingsScrollAreaWidgetContents)
        self.UpdaterWidget.setMinimumSize(QSize(620, 160))
        self.UpdaterWidget.setMaximumSize(QSize(620, 160))
        self.UpdaterWidget.setStyleSheet("QWidget\n"
                                         "{\n"
                                         "    border-radius: 7px;\n"
                                         "    background-color: rgba(247, 247, 247, 247)\n"
                                         "}")
        self.UpdaterWidget.setObjectName("UpdaterWidget")
        self.UpdaterTitle = QWidget(self.UpdaterWidget)
        self.UpdaterTitle.setGeometry(QRect(20, 10, 120, 40))
        self.UpdaterTitle.setMinimumSize(QSize(120, 40))
        self.UpdaterTitle.setStyleSheet("QWidget\n"
                                        "{\n"
                                        "    background-color: rgb(247, 247, 247);\n"
                                        "    border-radius: 10px\n"
                                        "}")
        self.UpdaterTitle.setObjectName("UpdaterTitle")
        self.UpdaterWidgetTitleLabel = QLabel(self.UpdaterTitle)
        self.UpdaterWidgetTitleLabel.setGeometry(QRect(30, 10, 81, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.UpdaterWidgetTitleLabel.setFont(font)
        self.UpdaterWidgetTitleLabel.setObjectName("UpdaterWidgetTitleLabel")
        self.UpdaterWidgetBlue = QLabel(self.UpdaterTitle)
        self.UpdaterWidgetBlue.setGeometry(QRect(10, 10, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.UpdaterWidgetBlue.setFont(font)
        self.UpdaterWidgetBlue.setCursor(QCursor(Qt.ArrowCursor))
        self.UpdaterWidgetBlue.setAutoFillBackground(False)
        self.UpdaterWidgetBlue.setStyleSheet("QLabel\n"
                                             "{\n"
                                             "    background-color: rgb(0, 120, 212);\n"
                                             "    border-radius: 10px\n"
                                             "}")
        self.UpdaterWidgetBlue.setText("")
        self.UpdaterWidgetBlue.setObjectName("UpdaterWidgetBlue")
        self.CurrentVersionLabel = QLabel(self.UpdaterWidget)
        self.CurrentVersionLabel.setGeometry(QRect(30, 60, 571, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.CurrentVersionLabel.setFont(font)
        self.CurrentVersionLabel.setObjectName("CurrentVersionLabel")
        self.LastUpdateTime = QLabel(self.UpdaterWidget)
        self.LastUpdateTime.setGeometry(QRect(150, 110, 311, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.LastUpdateTime.setFont(font)
        self.LastUpdateTime.setObjectName("LastUpdateTime")
        self.UpdatePushButton = QPushButton(self.UpdaterWidget)
        self.UpdatePushButton.setGeometry(QRect(30, 110, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.UpdatePushButton.setFont(font)
        self.UpdatePushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.UpdatePushButton.setStyleSheet("QPushButton\n"
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
                                            "}")
        self.UpdatePushButton.setFlat(False)
        self.UpdatePushButton.setObjectName("UpdatePushButton")
        self.SettingsVerticalLayout.addWidget(self.UpdaterWidget)
        self.AboutWidget = QWidget(self.SettingsScrollAreaWidgetContents)
        self.AboutWidget.setMinimumSize(QSize(620, 330))
        self.AboutWidget.setMaximumSize(QSize(620, 330))
        self.AboutWidget.setStyleSheet("QWidget\n"
                                       "{\n"
                                       "    border-radius: 7px;\n"
                                       "    background-color: rgba(247, 247, 247, 247)\n"
                                       "}")
        self.AboutWidget.setObjectName("AboutWidget")
        self.AboutTitle = QWidget(self.AboutWidget)
        self.AboutTitle.setGeometry(QRect(20, 10, 120, 40))
        self.AboutTitle.setMinimumSize(QSize(120, 40))
        self.AboutTitle.setStyleSheet("QWidget\n"
                                      "{\n"
                                      "    background-color: rgb(247, 247, 247);\n"
                                      "    border-radius: 10px\n"
                                      "}")
        self.AboutTitle.setObjectName("AboutTitle")
        self.AboutWidgetTitleLabel = QLabel(self.AboutTitle)
        self.AboutWidgetTitleLabel.setGeometry(QRect(30, 10, 51, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.AboutWidgetTitleLabel.setFont(font)
        self.AboutWidgetTitleLabel.setObjectName("AboutWidgetTitleLabel")
        self.AboutWidgetBlue = QLabel(self.AboutTitle)
        self.AboutWidgetBlue.setGeometry(QRect(10, 10, 10, 21))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.AboutWidgetBlue.setFont(font)
        self.AboutWidgetBlue.setCursor(QCursor(Qt.ArrowCursor))
        self.AboutWidgetBlue.setAutoFillBackground(False)
        self.AboutWidgetBlue.setStyleSheet("QLabel\n"
                                           "{\n"
                                           "    background-color: rgb(0, 120, 212);\n"
                                           "    border-radius: 10px\n"
                                           "}")
        self.AboutWidgetBlue.setText("")
        self.AboutWidgetBlue.setObjectName("AboutWidgetBlue")
        self.AboutContent = QLabel(self.AboutWidget)
        self.AboutContent.setGeometry(QRect(30, 55, 571, 131))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.AboutContent.setFont(font)
        self.AboutContent.setObjectName("AboutContent")
        self.OpenSourceCodePushButton = QPushButton(self.AboutWidget)
        self.OpenSourceCodePushButton.setGeometry(QRect(30, 280, 121, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.OpenSourceCodePushButton.setFont(font)
        self.OpenSourceCodePushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.OpenSourceCodePushButton.setStyleSheet("QPushButton\n"
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
                                                    "}")
        self.OpenSourceCodePushButton.setFlat(False)
        self.OpenSourceCodePushButton.setObjectName("OpenSourceCodePushButton")
        self.MCSL2_Author_Label_1 = QLabel(self.AboutWidget)
        self.MCSL2_Author_Label_1.setGeometry(QRect(120, 240, 111, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.MCSL2_Author_Label_1.setFont(font)
        self.MCSL2_Author_Label_1.setObjectName("MCSL2_Author_Label_1")
        self.MCSL2_Label = QLabel(self.AboutWidget)
        self.MCSL2_Label.setGeometry(QRect(120, 210, 111, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.MCSL2_Label.setFont(font)
        self.MCSL2_Label.setObjectName("MCSL2_Label")
        self.MCSL2_Icon_Label = QLabel(self.AboutWidget)
        self.MCSL2_Icon_Label.setGeometry(QRect(30, 200, 71, 71))
        self.MCSL2_Icon_Label.setText("")
        self.MCSL2_Icon_Label.setPixmap(QPixmap(":/MCSL2_Icon/MCSL2_Icon.png"))
        self.MCSL2_Icon_Label.setScaledContents(True)
        self.MCSL2_Icon_Label.setObjectName("MCSL2_Icon_Label")
        self.MCSL2_Author_Label_2 = QLabel(self.AboutWidget)
        self.MCSL2_Author_Label_2.setGeometry(QRect(300, 210, 111, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.MCSL2_Author_Label_2.setFont(font)
        self.MCSL2_Author_Label_2.setObjectName("MCSL2_Author_Label_2")
        self.MCSL2_Author_Avatar = QLabel(self.AboutWidget)
        self.MCSL2_Author_Avatar.setGeometry(QRect(210, 200, 71, 71))
        self.MCSL2_Author_Avatar.setText("")
        self.MCSL2_Author_Avatar.setPixmap(QPixmap(":/MCSL2_Icon/MCSL2_Author.png"))
        self.MCSL2_Author_Avatar.setScaledContents(True)
        self.MCSL2_Author_Avatar.setObjectName("MCSL2_Author_Avatar")
        self.JoinQQGroup = QPushButton(self.AboutWidget)
        self.JoinQQGroup.setGeometry(QRect(160, 280, 121, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.JoinQQGroup.setFont(font)
        self.JoinQQGroup.setCursor(QCursor(Qt.PointingHandCursor))
        self.JoinQQGroup.setStyleSheet("QPushButton\n"
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
                                       "}")
        self.JoinQQGroup.setFlat(False)
        self.JoinQQGroup.setObjectName("JoinQQGroup")
        self.SystemReportPushButton = QPushButton(self.AboutWidget)
        self.SystemReportPushButton.setGeometry(QRect(290, 280, 101, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.SystemReportPushButton.setFont(font)
        self.SystemReportPushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.SystemReportPushButton.setStyleSheet("QPushButton\n"
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
                                                  "}")
        self.SystemReportPushButton.setFlat(False)
        self.SystemReportPushButton.setObjectName("SystemReportPushButton")
        self.SettingsVerticalLayout.addWidget(self.AboutWidget)
        self.verticalLayout_7.addLayout(self.SettingsVerticalLayout)
        self.SettingsScrollArea.setWidget(self.SettingsScrollAreaWidgetContents)
        self.FunctionsStackedWidget.addWidget(self.SettingsPage)
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
        self.ChooseServerScrollArea = QScrollArea(self.ChooseServerPage)
        self.ChooseServerScrollArea.setGeometry(QRect(30, 140, 641, 401))
        self.ChooseServerScrollArea.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.ChooseServerScrollArea.setStyleSheet("QScrollArea{\n"
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
"QScrollBar::add-line:vertial\n"
"{\n"
"    height: 0px;\n"
"}\n"
"QScrollBar::sub-line:vertial\n"
"{\n"
"    height: 0px;\n"
"}\n"
"QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
"{\n"
"    height: 0px;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.ChooseServerScrollArea.setFrameShape(QFrame.NoFrame)
        self.ChooseServerScrollArea.setFrameShadow(QFrame.Plain)
        self.ChooseServerScrollArea.setLineWidth(0)
        self.ChooseServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ChooseServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ChooseServerScrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.ChooseServerScrollArea.setWidgetResizable(True)
        self.ChooseServerScrollArea.setObjectName("ChooseServerScrollArea")
        self.ChooseServerScrollAreaWidgetContents = QWidget()
        self.ChooseServerScrollAreaWidgetContents.setGeometry(QRect(0, 0, 629, 401))
        self.ChooseServerScrollAreaWidgetContents.setObjectName("ChooseServerScrollAreaWidgetContents")
        self.verticalLayout_8 = QVBoxLayout(self.ChooseServerScrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.ChooseServerScrollAreaVerticalLayout = QVBoxLayout()
        self.ChooseServerScrollAreaVerticalLayout.setObjectName("ChooseServerScrollAreaVerticalLayout")
        self.verticalLayout_8.addLayout(self.ChooseServerScrollAreaVerticalLayout)
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
        self.Choose_Java_Back_PushButton = QPushButton(self.ChooseJavaPage)
        self.Choose_Java_Back_PushButton.setGeometry(QRect(200, 90, 101, 41))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(14)
        self.Choose_Java_Back_PushButton.setFont(font)
        self.Choose_Java_Back_PushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Choose_Java_Back_PushButton.setStyleSheet(
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
        self.Choose_Java_Back_PushButton.setFlat(False)
        self.Choose_Java_Back_PushButton.setObjectName("Choose_Java_Back_PushButton")
        self.ChooseJavaScrollArea = QScrollArea(self.ChooseJavaPage)
        self.ChooseJavaScrollArea.setGeometry(QRect(40, 150, 641, 401))
        self.ChooseJavaScrollArea.viewport().setProperty(
            "cursor", QCursor(Qt.ArrowCursor)
        )
        self.ChooseJavaScrollArea.setStyleSheet(
            "QScrollArea{\n"
            "    border: 0px solid;\n"
            "    border-right-color: #dcdbdc;\n"
            "    background-color: rgb(230, 230, 230);\n"
            "    border-radius: 7px;\n"
            "}\n"
            "QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: transparent;\n"
            "    Width: 12px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background: rgb(220, 220, 220);\n"
            "    min-Height: 20px;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::sub-line:vertial \n"
            "{    \n"
            "    Height: 0px;\n"
            "}\n"
            "QScrollBar::up-arrow:vertial,QScrollBar::down-arrow:vertial\n"
            "{    \n"
            "    Height: 0px;\n"
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
        self.ChooseJavaScrollAreaWidgetContents.setGeometry(QRect(0, 0, 629, 401))
        self.ChooseJavaScrollAreaWidgetContents.setObjectName(
            "ChooseJavaScrollAreaWidgetContents"
        )
        self.verticalLayout_6 = QVBoxLayout(self.ChooseJavaScrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.ChooseJavaScrollAreaVerticalLayout = QVBoxLayout()
        self.ChooseJavaScrollAreaVerticalLayout.setObjectName(
            "ChooseJavaScrollAreaVerticalLayout"
        )
        self.verticalLayout_6.addLayout(self.ChooseJavaScrollAreaVerticalLayout)
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
        self.Update_Tip1_Widget.setStyleSheet(
            "QWidget\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
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
        self.Update_Introduction_Widget.setStyleSheet(
            "QWidget\n"
            "{\n"
            "    background-color: rgb(247, 247, 247);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Update_Introduction_Widget.setObjectName("Update_Introduction_Widget")
        self.Update_Introduction_Title_Label = QLabel(self.Update_Introduction_Widget)
        self.Update_Introduction_Title_Label.setGeometry(QRect(20, 20, 601, 31))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Update_Introduction_Title_Label.setFont(font)
        self.Update_Introduction_Title_Label.setAutoFillBackground(False)
        self.Update_Introduction_Title_Label.setStyleSheet("")
        self.Update_Introduction_Title_Label.setObjectName(
            "Update_Introduction_Title_Label"
        )
        self.Update_Introduction_Label = QLabel(self.Update_Introduction_Widget)
        self.Update_Introduction_Label.setGeometry(QRect(20, 60, 601, 141))
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Update_Introduction_Label.setFont(font)
        self.Update_Introduction_Label.setAutoFillBackground(False)
        self.Update_Introduction_Label.setStyleSheet("")
        self.Update_Introduction_Label.setText("")
        self.Update_Introduction_Label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self.Update_Introduction_Label.setObjectName("Update_Introduction_Label")
        self.FunctionsStackedWidget.addWidget(self.UpdatePage)
        self.Background = QLabel(self.CentralWidget)
        self.Background.setGeometry(QRect(10, 10, 211, 581))
        self.Background.setStyleSheet(
            "QLabel\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px\n"
            "}"
        )
        self.Background.setText("")
        self.Background.setObjectName("Background")
        self.Shadow = QLabel(self.CentralWidget)
        self.Shadow.setGeometry(QRect(8, 8, 945, 585))
        self.Shadow.setStyleSheet("QLabel\n"
                                  "{\n"
                                  "    background-color: rgba(230, 230, 230, 15%);\n"
                                  "    border-radius: 10px\n"
                                  "}")
        self.Shadow.setText("")
        self.Shadow.setObjectName("Shadow")
        self.Background_2 = QLabel(self.CentralWidget)
        self.Background_2.setGeometry(QRect(200, 10, 751, 581))
        self.Background_2.setStyleSheet("QLabel\n"
                                        "{\n"
                                        "    background-color: rgba(255, 255, 255, 55%);\n"
                                        "    border-radius: 10px\n"
                                        "}")
        self.Background_2.setText("")
        self.Background_2.setObjectName("Background_2")
        self.Background_2.raise_()
        self.Shadow.raise_()
        self.Background.raise_()
        self.OptionsWidget.raise_()
        self.FunctionsStackedWidget.raise_()
        MCSL2_MainWindow.setCentralWidget(self.CentralWidget)
        self.retranslateUi(MCSL2_MainWindow)
        self.FunctionsStackedWidget.setCurrentIndex(0)
        self.ConfigModeWidget.setCurrentIndex(0)
        self.ExConsoleInputDecodingComboBox.setCurrentIndex(0)
        self.DownloadSwitcher_TabWidget.setCurrentIndex(0)
        self.Aria2ThreadCountComboBox.setCurrentIndex(3)
        self.ConsoleInputDecodingComboBox.setCurrentIndex(0)
        self.DarkModeComboBox.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MCSL2_MainWindow)

    def retranslateUi(self, MCSL2_MainWindow):
        _translate = QCoreApplication.translate
        MCSL2_MainWindow.setWindowTitle(_translate("MCSL2_MainWindow", "MCSL 2"))
        self.Home_Page_PushButton.setText(_translate("MCSL2_MainWindow", "     主页"))
        self.Config_Page_PushButton.setText(_translate("MCSL2_MainWindow", "     配置"))
        self.MCSL2_Title_Label.setText(_translate("MCSL2_MainWindow", "MCSL 2"))
        self.MCSL2_Title_Author_Label.setText(_translate("MCSL2_MainWindow", "by LxHTT"))
        self.Download_Page_PushButton.setText(_translate("MCSL2_MainWindow", "     下载"))
        self.Server_Console_Page_PushButton.setText(_translate("MCSL2_MainWindow", "     终端"))
        self.Tools_Page_PushButton.setText(_translate("MCSL2_MainWindow", "     工具"))
        self.About_Page_PushButton.setText(_translate("MCSL2_MainWindow", "     更多"))
        self.Home_Label.setText(_translate("MCSL2_MainWindow", "主页"))
        self.Notice_Label.setText(_translate("MCSL2_MainWindow", "正在获取公告..."))
        self.HomeTip1_Label.setText(_translate("MCSL2_MainWindow", "如何搭建一个Java版Minecraft服务器？\n"
"1.准备好Java、核心、电脑\n"
"（提示：可使用本程序下载）\n"
"2.配置参数（本程序“配置服务器”页）\n"
"3. 开启服务器。将服务器IP告诉玩家。"))
        self.Selected_Server_Label.setText(_translate("MCSL2_MainWindow", "未选择服务器！"))
        self.Start_PushButton.setText(_translate("MCSL2_MainWindow", "启动服务器"))
        self.Config_PushButton.setText(_translate("MCSL2_MainWindow", "配置"))
        self.Choose_Server_PushButton.setText(_translate("MCSL2_MainWindow", "选择"))
        self.Config_Label.setText(_translate("MCSL2_MainWindow", "配置服务器"))
        self.LeadConfigTip1.setText(_translate("MCSL2_MainWindow", "请选择您想要添加服务器的方式："))
        self.NoobAddServer.setText(_translate("MCSL2_MainWindow", "  简易配置"))
        self.ExAddServer.setText(_translate("MCSL2_MainWindow", "  进阶模式"))
        self.ImportServer.setText(_translate("MCSL2_MainWindow", "  导入服务器压缩包"))
        self.LeadConfigTip2.setText(_translate("MCSL2_MainWindow", "保留基础配置。\n"
" - Java\n"
" - 服务器核心\n"
" - 最小最大内存\n"
" - 服务器名称"))
        self.LeadConfigTip2_2.setText(_translate("MCSL2_MainWindow", "较简易配置来说，\n"
"可以配置更多选项。"))
        self.LeadConfigTip2_3.setText(_translate("MCSL2_MainWindow", "  （未开发完成）"))
        self.Completed_Save_PushButton.setText(_translate("MCSL2_MainWindow", "保存"))
        self.Server_Name_Label.setText(_translate("MCSL2_MainWindow", "服务器名称："))
        self.Download_Core_PushButton.setText(_translate("MCSL2_MainWindow", "下载核心"))
        self.Download_Java_PushButton.setText(_translate("MCSL2_MainWindow", "下载Java"))
        self.Manual_Import_Core_PushButton.setText(_translate("MCSL2_MainWindow", "手动导入"))
        self.Memory_1_Label.setText(_translate("MCSL2_MainWindow", "内存："))
        self.Java_Label.setText(_translate("MCSL2_MainWindow", "Java:"))
        self.Memory_2_Label.setText(_translate("MCSL2_MainWindow", "~"))
        self.Core_Label.setText(_translate("MCSL2_MainWindow", "服务器核心："))
        self.Auto_Find_Java_PushButton.setText(_translate("MCSL2_MainWindow", "自动查找"))
        self.Memory_Unit_Label.setText(_translate("MCSL2_MainWindow", "M"))
        self.Founded_Java_List_PushButton.setText(_translate("MCSL2_MainWindow", "Java列表"))
        self.ConfigTip1_Label.setText(_translate("MCSL2_MainWindow", "一个服务器最基础的三个部件\n"
"1.存放的文件夹路径\n"
"2.服务器核心\n"
"3.Java路径"))
        self.ConfigTip2_Label.setText(_translate("MCSL2_MainWindow", "MCSL 2将会在Servers目录\n"
"生成以服务器名称命名的文件夹\n"
"以存储服务器文件。"))
        self.ExDownload_Core_PushButton.setText(_translate("MCSL2_MainWindow", "下载核心"))
        self.ExDownload_Java_PushButton.setText(_translate("MCSL2_MainWindow", "下载Java"))
        self.ExManual_Import_Core_PushButton.setText(_translate("MCSL2_MainWindow", "手动导入"))
        self.ExMemory_1_Label.setText(_translate("MCSL2_MainWindow", "内存："))
        self.ExJava_Label.setText(_translate("MCSL2_MainWindow", "Java:"))
        self.ExMemory_2_Label.setText(_translate("MCSL2_MainWindow", "~"))
        self.ExCore_Label.setText(_translate("MCSL2_MainWindow", "服务器核心："))
        self.ExAuto_Find_Java_PushButton.setText(_translate("MCSL2_MainWindow", "自动查找"))
        self.ExFounded_Java_List_PushButton.setText(_translate("MCSL2_MainWindow", "Java列表"))
        self.ExServer_Name_Label.setText(_translate("MCSL2_MainWindow", "服务器名称："))
        self.ExCompleted_Save_PushButton.setText(_translate("MCSL2_MainWindow", "保存"))
        self.ExMemoryUnitComboBox.setItemText(0, _translate("MCSL2_MainWindow", "M"))
        self.ExMemoryUnitComboBox.setItemText(1, _translate("MCSL2_MainWindow", "G"))
        self.ExConsoleInputDecoding.setText(_translate("MCSL2_MainWindow", "发送指令编码(优先级高于全局设置）"))
        self.ExConsoleOutputEncodingComboBox.setItemText(0, _translate("MCSL2_MainWindow", "UTF-8（默认）"))
        self.ExConsoleOutputEncodingComboBox.setItemText(1, _translate("MCSL2_MainWindow", "GBK（乱码可尝试）"))
        self.ExConsoleInputDecodingComboBox.setItemText(0, _translate("MCSL2_MainWindow", "与输出相同"))
        self.ExConsoleInputDecodingComboBox.setItemText(1, _translate("MCSL2_MainWindow", "UTF-8"))
        self.ExConsoleInputDecodingComboBox.setItemText(2, _translate("MCSL2_MainWindow", "GBK"))
        self.ExConsoleOutputEncoding.setText(_translate("MCSL2_MainWindow", "控制台输出编码(优先级高于全局设置）"))
        self.ExJVMArg.setText(_translate("MCSL2_MainWindow", "启动时的JVM参数（可不填）"))
        self.Download_Label.setText(_translate("MCSL2_MainWindow", "下载"))
        self.DownloadSwitcher_TabWidget.setTabText(self.DownloadSwitcher_TabWidget.indexOf(self.JavaTab), _translate("MCSL2_MainWindow", "[ 运行环境 ] Java"))
        self.DownloadSwitcher_TabWidget.setTabText(self.DownloadSwitcher_TabWidget.indexOf(self.SpigotTab), _translate("MCSL2_MainWindow", "[ 核心 ] Spigot"))
        self.DownloadSwitcher_TabWidget.setTabText(self.DownloadSwitcher_TabWidget.indexOf(self.PaperTab), _translate("MCSL2_MainWindow", "[ 核心 ] Paper"))
        self.DownloadSwitcher_TabWidget.setTabText(self.DownloadSwitcher_TabWidget.indexOf(self.BungeeCordTab), _translate("MCSL2_MainWindow", "[ 核心 ] BungeeCord"))
        self.DownloadSwitcher_TabWidget.setTabText(self.DownloadSwitcher_TabWidget.indexOf(self.OfficialCoreTab), _translate("MCSL2_MainWindow", "[ 核心 ] 官方"))
        self.More_Download_PushButton.setText(_translate("MCSL2_MainWindow", "更多"))
        self.GoToDownloadSourceChangerPushButton.setText(_translate("MCSL2_MainWindow", "下载源设置"))
        self.CurrentDownloadSourceLabel.setText(_translate("MCSL2_MainWindow", "当前下载源："))
        self.Console_Label.setText(_translate("MCSL2_MainWindow", "服务器控制台"))
        self.Command_Background.setText(_translate("MCSL2_MainWindow", "  >"))
        self.Send_Command_PushButton.setText(_translate("MCSL2_MainWindow", "发送"))
        self.Tools_Label.setText(_translate("MCSL2_MainWindow", "更多工具"))
        self.About_Label.setText(_translate("MCSL2_MainWindow", "更多"))
        self.AutoRunLastServerSetting.setText(_translate("MCSL2_MainWindow", "开启MCSL2时自动运行上次运行的服务器"))
        self.AcceptAllMojangEULASetting.setText(_translate("MCSL2_MainWindow", "同意所有新添加服务器的Mojang EULA"))
        self.StopServerSettings.setText(_translate("MCSL2_MainWindow", "关闭服务器时向服务器发送 stop 指令而不是结束进程"))
        self.ServerSettingsWidgetTitleLabel.setText(_translate("MCSL2_MainWindow", "服务器设置"))
        self.OnlySaveGlobalServerConfigs.setText(_translate("MCSL2_MainWindow", "仅保存全局服务器设置"))
        self.ConfigPageSettingsWidgetTitleLabel.setText(_translate("MCSL2_MainWindow", "配置页设置"))
        self.HowToAddServer.setText(_translate("MCSL2_MainWindow", "添加服务器引导方式"))
        self.HowToAddServerComboBox.setItemText(0, _translate("MCSL2_MainWindow", "初始 (新手+进阶)"))
        self.HowToAddServerComboBox.setItemText(1, _translate("MCSL2_MainWindow", "总是新手"))
        self.HowToAddServerComboBox.setItemText(2, _translate("MCSL2_MainWindow", "总是进阶"))
        self.DownloadSettingsWidgetTitleLabel.setText(_translate("MCSL2_MainWindow", "下载设置"))
        self.MCSLAPIDownloadSource.setText(_translate("MCSL2_MainWindow", "MCSLAPI下载源选择"))
        self.MCSLAPIDownloadSourceComboBox.setItemText(0, _translate("MCSL2_MainWindow", "国内SharePoint"))
        self.MCSLAPIDownloadSourceComboBox.setItemText(1, _translate("MCSL2_MainWindow", "Gitee"))
        self.MCSLAPIDownloadSourceComboBox.setItemText(2, _translate("MCSL2_MainWindow", "luoxis云（暂不可用）"))
        self.MCSLAPIDownloadSourceComboBox.setItemText(3, _translate("MCSL2_MainWindow", "GHProxy"))
        self.MCSLAPIDownloadSourceComboBox.setItemText(4, _translate("MCSL2_MainWindow", "GitHub"))
        self.Aria2ThreadCount.setText(_translate("MCSL2_MainWindow", "Aria2引擎线程数"))
        self.Aria2ThreadCountComboBox.setItemText(0, _translate("MCSL2_MainWindow", "1"))
        self.Aria2ThreadCountComboBox.setItemText(1, _translate("MCSL2_MainWindow", "2"))
        self.Aria2ThreadCountComboBox.setItemText(2, _translate("MCSL2_MainWindow", "4"))
        self.Aria2ThreadCountComboBox.setItemText(3, _translate("MCSL2_MainWindow", "8"))
        self.Aria2ThreadCountComboBox.setItemText(4, _translate("MCSL2_MainWindow", "16"))
        self.AlwaysAskDownloadPath.setText(_translate("MCSL2_MainWindow", "总是询问下载保存位置"))
        self.AlwaysAskDownloadPathTip.setText(_translate("MCSL2_MainWindow", "若不勾选，则会保存至MCSL2/Downloads文件夹。"))
        self.SameFileException.setText(_translate("MCSL2_MainWindow", "下载保存位置存在同名文件处理"))
        self.SameFileExceptionStop.setText(_translate("MCSL2_MainWindow", "停止"))
        self.SameFileExceptionAsk.setText(_translate("MCSL2_MainWindow", "询问"))
        self.SameFileExceptionReWrite.setText(_translate("MCSL2_MainWindow", "覆盖"))
        self.ConsoleSettingsWidgetTitleLabel.setText(_translate("MCSL2_MainWindow", "终端设置"))
        self.ConsoleOutputEncoding.setText(_translate("MCSL2_MainWindow", "控制台输出编码"))
        self.ConsoleOutputEncodingComboBox.setItemText(0, _translate("MCSL2_MainWindow", "UTF-8（默认）"))
        self.ConsoleOutputEncodingComboBox.setItemText(1, _translate("MCSL2_MainWindow", "GBK（乱码可尝试）"))
        self.ConsoleInputDecoding.setText(_translate("MCSL2_MainWindow", "发送指令编码"))
        self.ConsoleInputDecodingComboBox.setItemText(0, _translate("MCSL2_MainWindow", "与输出相同"))
        self.ConsoleInputDecodingComboBox.setItemText(1, _translate("MCSL2_MainWindow", "UTF-8"))
        self.ConsoleInputDecodingComboBox.setItemText(2, _translate("MCSL2_MainWindow", "GBK"))
        self.EnableQuickMenu.setText(_translate("MCSL2_MainWindow", "启用快捷菜单"))
        self.UISettingsWidgetTitleLabel.setText(_translate("MCSL2_MainWindow", "界面设置"))
        self.TransparentSetting.setText(_translate("MCSL2_MainWindow", "背景透明度"))
        self.DarkMode.setText(_translate("MCSL2_MainWindow", "深色模式"))
        self.DarkModeComboBox.setItemText(0, _translate("MCSL2_MainWindow", "浅色"))
        self.DarkModeComboBox.setItemText(1, _translate("MCSL2_MainWindow", "深色"))
        self.DarkModeComboBox.setItemText(2, _translate("MCSL2_MainWindow", "跟随系统"))
        self.ExchangeButton.setText(_translate("MCSL2_MainWindow", "交换窗口最小化和关闭按钮顺序"))
        self.TransparentPercentNum.setText(_translate("MCSL2_MainWindow", "--%"))
        self.AlwaysRunAsAdministrator.setText(_translate("MCSL2_MainWindow", "总以管理员身份运行"))
        self.SoftwareSettingsWidgetTitleLabel.setText(_translate("MCSL2_MainWindow", "软件设置"))
        self.StartOnStartup.setText(_translate("MCSL2_MainWindow", "开机自动启动"))
        self.UpdaterWidgetTitleLabel.setText(_translate("MCSL2_MainWindow", "软件更新"))
        self.CurrentVersionLabel.setText(_translate("MCSL2_MainWindow", "当前版本："))
        self.LastUpdateTime.setText(_translate("MCSL2_MainWindow", "最后一次检查更新时间："))
        self.UpdatePushButton.setText(_translate("MCSL2_MainWindow", "检查更新"))
        self.AboutWidgetTitleLabel.setText(_translate("MCSL2_MainWindow", "关于"))
        self.AboutContent.setText(_translate("MCSL2_MainWindow", "MCSL2是一个开源非营利性项目，遵循GNU GPL 3.0开源协议。\n"
"任何人皆可使用MCSL2的源码进行再编译、修改以及发行，\n"
"但必须在相关源代码中以及软件中给出声明，\n"
"并且二次分发版本的项目名称应与“MCSL2”有明显辨识度。\n"
"\n"
"Copyright ©落雪无痕LxHTT. All right reserved."))
        self.OpenSourceCodePushButton.setText(_translate("MCSL2_MainWindow", "打开源代码仓库"))
        self.MCSL2_Author_Label_1.setText(_translate("MCSL2_MainWindow", "by LxHTT"))
        self.MCSL2_Label.setText(_translate("MCSL2_MainWindow", "MCSL 2"))
        self.MCSL2_Author_Label_2.setText(_translate("MCSL2_MainWindow", "Bilibili：\n"
"落雪无痕LxHTT"))
        self.JoinQQGroup.setText(_translate("MCSL2_MainWindow", "加入官方群聊"))
        self.SystemReportPushButton.setText(_translate("MCSL2_MainWindow", "系统报告"))
        self.Choose_Server_Label.setText(_translate("MCSL2_MainWindow", "选择服务器"))
        self.Choose_Java_Label.setText(_translate("MCSL2_MainWindow", "选择Java"))
        self.Choose_Java_Back_PushButton.setText(_translate("MCSL2_MainWindow", "返回"))
        self.Update_Label.setText(_translate("MCSL2_MainWindow", "程序更新"))
        self.Update_Tip1_Label.setText(_translate("MCSL2_MainWindow", "MCSL 2发布新版本啦！你想更新吗？"))
        self.DoNotUpdate_PushButton.setText(_translate("MCSL2_MainWindow", "丑拒"))
        self.Update_PushButton.setText(_translate("MCSL2_MainWindow", "火速更新"))
        self.Update_Introduction_Title_Label.setText(_translate("MCSL2_MainWindow", "这是最新版本的说明："))

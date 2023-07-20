from json import dump
from os import getcwd, remove, path as ospath
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QSize, QRect, pyqtSlot
from PyQt5.QtWidgets import (
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QHBoxLayout,
    QFrame,
    QFileDialog
)

from qfluentwidgets import (
    ComboBox,
    LineEdit,
    PlainTextEdit,
    PrimaryPushButton,
    PushButton,
    SmoothScrollArea,
    StrongBodyLabel,
    SubtitleLabel,
    TitleLabel,
    TransparentToolButton,
    FluentIcon as FIF,
    InfoBar,
    InfoBarPosition,
    MessageBox
)

from MCSL2Lib.variables import scrollAreaViewportQss
from MCSL2Lib import javaDetector


class _ConfigurePage(QWidget):

    def __init__(self):
        
        super().__init__()

        self.javaPath = []
        self.javaFindWorkThreadFactory = javaDetector.JavaFindWorkThreadFactory()
        self.javaFindWorkThreadFactory.FuzzySearch = True
        self.javaFindWorkThreadFactory.SignalConnect = self.autoDetectJavaFinished
        self.javaFindWorkThreadFactory.FinishSignalConnect = self.onJavaFindWorkThreadFinished
        self.javaFindWorkThreadFactory.Create().start()
        self.minMem: int
        self.maxMem: int
        self.corePath = ""
        self.coreFileName = ""
        self.selectedJavaPath = ""
        self.selectedJavaVersion = ""
        self.memUnit = ""
        self.consoleOutputDeEncoding: str
        self.consoleInputDeEncoding: str
        self.consoleOutputDeEncodingList = ["follow", "utf-8", "gbk"]
        self.consoleInputDeEncodingList = ["follow", "utf-8", "gbk"]
        self.memUnitList = ["M", "G"]
        self.jvmArg = [str]
        self.serverName: str

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.verticalLayout = QVBoxLayout(self.titleLimitWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.verticalLayout.addWidget(self.subTitleLabel)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 1, 1)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.newServerStackedWidget = QStackedWidget(self)
        self.newServerStackedWidget.setObjectName("newServerStackedWidget")

        self.guideNewServerPage = QWidget()
        self.guideNewServerPage.setObjectName("guideNewServerPage")

        self.guideNewServerVerticalLayout = QVBoxLayout(self.guideNewServerPage)
        self.guideNewServerVerticalLayout.setObjectName("guideNewServerVerticalLayout")

        self.noobNewServerWidget = QWidget(self.guideNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobNewServerWidget.sizePolicy().hasHeightForWidth())
        self.noobNewServerWidget.setSizePolicy(sizePolicy)
        self.noobNewServerWidget.setMinimumSize(QSize(0, 132))
        self.noobNewServerWidget.setObjectName("noobNewServerWidget")

        self.guideNoobHorizontalLayout = QHBoxLayout(self.noobNewServerWidget)
        self.guideNoobHorizontalLayout.setObjectName("guideNoobHorizontalLayout")

        self.noobNewServerBtn = PrimaryPushButton(self.noobNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobNewServerBtn.sizePolicy().hasHeightForWidth())
        self.noobNewServerBtn.setSizePolicy(sizePolicy)
        self.noobNewServerBtn.setMinimumSize(QSize(215, 33))
        self.noobNewServerBtn.setMaximumSize(QSize(215, 33))
        self.noobNewServerBtn.setObjectName("noobNewServerBtn")

        self.guideNoobHorizontalLayout.addWidget(self.noobNewServerBtn)
        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.guideNoobHorizontalLayout.addItem(spacerItem1)
        self.noobNewServerIntro = StrongBodyLabel(self.noobNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobNewServerIntro.sizePolicy().hasHeightForWidth())
        self.noobNewServerIntro.setSizePolicy(sizePolicy)
        self.noobNewServerIntro.setTextFormat(Qt.MarkdownText)
        self.noobNewServerIntro.setObjectName("noobNewServerIntro")

        self.guideNoobHorizontalLayout.addWidget(self.noobNewServerIntro)
        self.guideNewServerVerticalLayout.addWidget(self.noobNewServerWidget)
        self.extendedNewServerWidget = QWidget(self.guideNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedNewServerWidget.sizePolicy().hasHeightForWidth())
        self.extendedNewServerWidget.setSizePolicy(sizePolicy)
        self.extendedNewServerWidget.setMinimumSize(QSize(0, 132))
        self.extendedNewServerWidget.setObjectName("extendedNewServerWidget")

        self.guideExtendedHorizontalLayout = QHBoxLayout(self.extendedNewServerWidget)
        self.guideExtendedHorizontalLayout.setObjectName("guideExtendedHorizontalLayout")

        self.extendedNewServerBtn = PrimaryPushButton(self.extendedNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedNewServerBtn.sizePolicy().hasHeightForWidth())
        self.extendedNewServerBtn.setSizePolicy(sizePolicy)
        self.extendedNewServerBtn.setMinimumSize(QSize(215, 33))
        self.extendedNewServerBtn.setMaximumSize(QSize(215, 33))
        self.extendedNewServerBtn.setObjectName("extendedNewServerBtn")

        self.guideExtendedHorizontalLayout.addWidget(self.extendedNewServerBtn)
        spacerItem2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.guideExtendedHorizontalLayout.addItem(spacerItem2)
        self.extendedNewServerIntro = StrongBodyLabel(self.extendedNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedNewServerIntro.sizePolicy().hasHeightForWidth())
        self.extendedNewServerIntro.setSizePolicy(sizePolicy)
        self.extendedNewServerIntro.setTextFormat(Qt.MarkdownText)
        self.extendedNewServerIntro.setObjectName("extendedNewServerIntro")

        self.guideExtendedHorizontalLayout.addWidget(self.extendedNewServerIntro)
        self.guideNewServerVerticalLayout.addWidget(self.extendedNewServerWidget)
        self.importNewServerWidget = QWidget(self.guideNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importNewServerWidget.sizePolicy().hasHeightForWidth())
        self.importNewServerWidget.setSizePolicy(sizePolicy)
        self.importNewServerWidget.setMinimumSize(QSize(0, 132))
        self.importNewServerWidget.setObjectName("importNewServerWidget")

        self.guideImportHorizontalLayout = QHBoxLayout(self.importNewServerWidget)
        self.guideImportHorizontalLayout.setObjectName("guideImportHorizontalLayout")

        self.importNewServerBtn = PrimaryPushButton(self.importNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importNewServerBtn.sizePolicy().hasHeightForWidth())
        self.importNewServerBtn.setSizePolicy(sizePolicy)
        self.importNewServerBtn.setMinimumSize(QSize(215, 33))
        self.importNewServerBtn.setMaximumSize(QSize(215, 33))
        self.importNewServerBtn.setObjectName("importNewServerBtn")

        self.guideImportHorizontalLayout.addWidget(self.importNewServerBtn)
        spacerItem3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.guideImportHorizontalLayout.addItem(spacerItem3)
        self.importNewServerIntro = StrongBodyLabel(self.importNewServerWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importNewServerIntro.sizePolicy().hasHeightForWidth())
        self.importNewServerIntro.setSizePolicy(sizePolicy)
        self.importNewServerIntro.setTextFormat(Qt.MarkdownText)
        self.importNewServerIntro.setObjectName("importNewServerIntro")

        self.guideImportHorizontalLayout.addWidget(self.importNewServerIntro)
        self.guideNewServerVerticalLayout.addWidget(self.importNewServerWidget)
        self.newServerStackedWidget.addWidget(self.guideNewServerPage)
        self.noobNewServerPage = QWidget()
        self.noobNewServerPage.setObjectName("noobNewServerPage")

        self.noobNewServerGridLayout = QGridLayout(self.noobNewServerPage)
        self.noobNewServerGridLayout.setObjectName("noobNewServerGridLayout")

        self.noobNewServerScrollArea = SmoothScrollArea(self.noobNewServerPage)
        self.noobNewServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.noobNewServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.noobNewServerScrollArea.setWidgetResizable(True)
        self.noobNewServerScrollArea.setObjectName("noobNewServerScrollArea")
        self.noobNewServerScrollArea.setFrameShape(QFrame.NoFrame)

        self.noobNewServerScrollAreaContents = QWidget()
        self.noobNewServerScrollAreaContents.setGeometry(QRect(0, -100, 586, 453))
        self.noobNewServerScrollAreaContents.setObjectName("noobNewServerScrollAreaContents")

        self.noobNewServerScrollAreaVerticalLayout = QVBoxLayout(self.noobNewServerScrollAreaContents)
        self.noobNewServerScrollAreaVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.noobNewServerScrollAreaVerticalLayout.setObjectName("noobNewServerScrollAreaVerticalLayout")

        self.noobSetJavaWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSetJavaWidget.sizePolicy().hasHeightForWidth())
        self.noobSetJavaWidget.setSizePolicy(sizePolicy)
        self.noobSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.noobSetJavaWidget.setObjectName("noobSetJavaWidget")

        self.gridLayout_3 = QGridLayout(self.noobSetJavaWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.noobJavaSubtitleLabel = SubtitleLabel(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobJavaSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.noobJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobJavaSubtitleLabel.setObjectName("noobJavaSubtitleLabel")

        self.gridLayout_3.addWidget(self.noobJavaSubtitleLabel, 0, 0, 1, 1)
        self.noobJavaInfoLabel = SubtitleLabel(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobJavaInfoLabel.sizePolicy().hasHeightForWidth())
        self.noobJavaInfoLabel.setSizePolicy(sizePolicy)
        self.noobJavaInfoLabel.setObjectName("noobJavaInfoLabel")

        self.gridLayout_3.addWidget(self.noobJavaInfoLabel, 0, 1, 1, 1)
        self.noobSetJavaBtnWidget = QWidget(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSetJavaBtnWidget.sizePolicy().hasHeightForWidth())
        self.noobSetJavaBtnWidget.setSizePolicy(sizePolicy)
        self.noobSetJavaBtnWidget.setObjectName("noobSetJavaBtnWidget")

        self.horizontalLayout_6 = QHBoxLayout(self.noobSetJavaBtnWidget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.noobDownloadJavaPrimaryPushBtn = PrimaryPushButton(self.noobSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.noobDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobDownloadJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobDownloadJavaPrimaryPushBtn.setObjectName("noobDownloadJavaPrimaryPushBtn")

        self.horizontalLayout_6.addWidget(self.noobDownloadJavaPrimaryPushBtn)
        self.noobManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(self.noobSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.noobManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobManuallyAddJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobManuallyAddJavaPrimaryPushBtn.setObjectName("noobManuallyAddJavaPrimaryPushBtn")

        self.horizontalLayout_6.addWidget(self.noobManuallyAddJavaPrimaryPushBtn)
        self.noobAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(self.noobSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.noobAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobAutoDetectJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobAutoDetectJavaPrimaryPushBtn.setObjectName("noobAutoDetectJavaPrimaryPushBtn")

        self.horizontalLayout_6.addWidget(self.noobAutoDetectJavaPrimaryPushBtn)
        self.noobJavaListPushBtn = PushButton(self.noobSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobJavaListPushBtn.sizePolicy().hasHeightForWidth())
        self.noobJavaListPushBtn.setSizePolicy(sizePolicy)
        self.noobJavaListPushBtn.setMinimumSize(QSize(90, 0))
        self.noobJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobJavaListPushBtn.setObjectName("noobJavaListPushBtn")

        self.horizontalLayout_6.addWidget(self.noobJavaListPushBtn)
        spacerItem4 = QSpacerItem(127, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.gridLayout_3.addWidget(self.noobSetJavaBtnWidget, 1, 0, 1, 2)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetJavaWidget)
        self.noobSetMemWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSetMemWidget.sizePolicy().hasHeightForWidth())
        self.noobSetMemWidget.setSizePolicy(sizePolicy)
        self.noobSetMemWidget.setObjectName("noobSetMemWidget")

        self.gridLayout_4 = QGridLayout(self.noobSetMemWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")

        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem5, 1, 5, 1, 1)
        self.noobMinMemLineEdit = LineEdit(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobMinMemLineEdit.sizePolicy().hasHeightForWidth())
        self.noobMinMemLineEdit.setSizePolicy(sizePolicy)
        self.noobMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noobMinMemLineEdit.setObjectName("noobMinMemLineEdit")

        self.gridLayout_4.addWidget(self.noobMinMemLineEdit, 1, 1, 1, 1)
        self.noobMemUnitLabel = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobMemUnitLabel.sizePolicy().hasHeightForWidth())
        self.noobMemUnitLabel.setSizePolicy(sizePolicy)
        self.noobMemUnitLabel.setObjectName("noobMemUnitLabel")

        self.gridLayout_4.addWidget(self.noobMemUnitLabel, 1, 4, 1, 1)
        self.noobMaxMemLineEdit = LineEdit(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobMaxMemLineEdit.sizePolicy().hasHeightForWidth())
        self.noobMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.noobMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noobMaxMemLineEdit.setObjectName("noobMaxMemLineEdit")

        self.gridLayout_4.addWidget(self.noobMaxMemLineEdit, 1, 3, 1, 1)
        self.noobToSymbol = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobToSymbol.sizePolicy().hasHeightForWidth())
        self.noobToSymbol.setSizePolicy(sizePolicy)
        self.noobToSymbol.setObjectName("noobToSymbol")

        self.gridLayout_4.addWidget(self.noobToSymbol, 1, 2, 1, 1)
        self.noobMemSubtitleLabel = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobMemSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.noobMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobMemSubtitleLabel.setObjectName("noobMemSubtitleLabel")

        self.gridLayout_4.addWidget(self.noobMemSubtitleLabel, 0, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetMemWidget)
        self.noobSetCoreWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSetCoreWidget.sizePolicy().hasHeightForWidth())
        self.noobSetCoreWidget.setSizePolicy(sizePolicy)
        self.noobSetCoreWidget.setObjectName("noobSetCoreWidget")

        self.gridLayout_5 = QGridLayout(self.noobSetCoreWidget)
        self.gridLayout_5.setObjectName("gridLayout_5")

        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem6, 1, 3, 1, 1)
        self.noobDownloadCorePrimaryPushBtn = PrimaryPushButton(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.noobDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobDownloadCorePrimaryPushBtn.setObjectName("noobDownloadCorePrimaryPushBtn")

        self.gridLayout_5.addWidget(self.noobDownloadCorePrimaryPushBtn, 1, 2, 1, 1)
        self.noobManuallyAddCorePrimaryPushBtn = PrimaryPushButton(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.noobManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobManuallyAddCorePrimaryPushBtn.setObjectName("noobManuallyAddCorePrimaryPushBtn")

        self.gridLayout_5.addWidget(self.noobManuallyAddCorePrimaryPushBtn, 1, 1, 1, 1)
        self.noobCoreSubtitleLabel = SubtitleLabel(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobCoreSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.noobCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobCoreSubtitleLabel.setObjectName("noobCoreSubtitleLabel")

        self.gridLayout_5.addWidget(self.noobCoreSubtitleLabel, 0, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetCoreWidget)
        self.noobSetServerNameWidget = QWidget(self.noobNewServerScrollAreaContents)
        self.noobSetServerNameWidget.setObjectName("noobSetServerNameWidget")

        self.verticalLayout_4 = QVBoxLayout(self.noobSetServerNameWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.noobServerNameSubtitleLabel = SubtitleLabel(self.noobSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobServerNameSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.noobServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobServerNameSubtitleLabel.setObjectName("noobServerNameSubtitleLabel")
        
        self.verticalLayout_4.addWidget(self.noobServerNameSubtitleLabel)
        self.noobServerNameLineEdit = LineEdit(self.noobSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobServerNameLineEdit.sizePolicy().hasHeightForWidth())
        self.noobServerNameLineEdit.setSizePolicy(sizePolicy)
        self.noobServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.noobServerNameLineEdit.setObjectName("noobServerNameLineEdit")

        self.verticalLayout_4.addWidget(self.noobServerNameLineEdit)
        self.noobSaveServerPrimaryPushBtn = PrimaryPushButton(self.noobSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.noobSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.noobSaveServerPrimaryPushBtn.setObjectName("noobSaveServerPrimaryPushBtn")

        self.verticalLayout_4.addWidget(self.noobSaveServerPrimaryPushBtn)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetServerNameWidget)
        spacerItem7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.noobNewServerScrollAreaVerticalLayout.addItem(spacerItem7)
        self.noobNewServerScrollArea.setWidget(self.noobNewServerScrollAreaContents)
        self.noobNewServerGridLayout.addWidget(self.noobNewServerScrollArea, 2, 2, 1, 1)
        self.noobTitleWidget = QWidget(self.noobNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobTitleWidget.sizePolicy().hasHeightForWidth())
        self.noobTitleWidget.setSizePolicy(sizePolicy)
        self.noobTitleWidget.setObjectName("noobTitleWidget")

        self.horizontalLayout_4 = QHBoxLayout(self.noobTitleWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.noobBackToGuidePushButton = TransparentToolButton(FIF.PAGE_LEFT, self.noobTitleWidget)
        self.noobBackToGuidePushButton.setObjectName("noobBackToGuidePushButton")

        self.horizontalLayout_4.addWidget(self.noobBackToGuidePushButton)
        self.noobSubtitleLabel = SubtitleLabel(self.noobTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.noobSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobSubtitleLabel.setObjectName("noobSubtitleLabel")

        self.horizontalLayout_4.addWidget(self.noobSubtitleLabel)
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.noobNewServerGridLayout.addWidget(self.noobTitleWidget, 0, 1, 2, 2)
        spacerItem9 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.noobNewServerGridLayout.addItem(spacerItem9, 0, 0, 3, 1)
        self.newServerStackedWidget.addWidget(self.noobNewServerPage)

        self.extendedNewServerPage = QWidget()
        self.extendedNewServerPage.setObjectName("extendedNewServerPage")
        
        self.gridLayout_2 = QGridLayout(self.extendedNewServerPage)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.extendedTitleWidget = QWidget(self.extendedNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedTitleWidget.sizePolicy().hasHeightForWidth())
        self.extendedTitleWidget.setSizePolicy(sizePolicy)
        self.extendedTitleWidget.setObjectName("extendedTitleWidget")

        self.horizontalLayout_5 = QHBoxLayout(self.extendedTitleWidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.extendedBackToGuidePushButton = TransparentToolButton(FIF.PAGE_LEFT, self.extendedTitleWidget)
        self.extendedBackToGuidePushButton.setObjectName("extendedBackToGuidePushButton")

        self.horizontalLayout_5.addWidget(self.extendedBackToGuidePushButton)
        self.extendedSubtitleLabel = SubtitleLabel(self.extendedTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.extendedSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedSubtitleLabel.setObjectName("extendedSubtitleLabel")

        self.horizontalLayout_5.addWidget(self.extendedSubtitleLabel)
        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem10)
        self.gridLayout_2.addWidget(self.extendedTitleWidget, 0, 1, 1, 1)
        self.extendedNewServerScrollArea = SmoothScrollArea(self.extendedNewServerPage)
        self.extendedNewServerScrollArea.setFrameShape(QFrame.NoFrame)
        self.extendedNewServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.extendedNewServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.extendedNewServerScrollArea.setWidgetResizable(True)
        self.extendedNewServerScrollArea.setObjectName("extendedNewServerScrollArea")

        self.extendedNewServerScrollAreaContents = QWidget()
        self.extendedNewServerScrollAreaContents.setGeometry(QRect(0, 0, 594, 734))
        self.extendedNewServerScrollAreaContents.setObjectName("extendedNewServerScrollAreaContents")

        self.noobNewServerScrollAreaVerticalLayout_2 = QVBoxLayout(self.extendedNewServerScrollAreaContents)
        self.noobNewServerScrollAreaVerticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.noobNewServerScrollAreaVerticalLayout_2.setObjectName("noobNewServerScrollAreaVerticalLayout_2")

        self.extendedSetJavaWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSetJavaWidget.sizePolicy().hasHeightForWidth())
        self.extendedSetJavaWidget.setSizePolicy(sizePolicy)
        self.extendedSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.extendedSetJavaWidget.setObjectName("extendedSetJavaWidget")

        self.gridLayout_6 = QGridLayout(self.extendedSetJavaWidget)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.extendedJavaSubtitleLabel = SubtitleLabel(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedJavaSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.extendedJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedJavaSubtitleLabel.setObjectName("extendedJavaSubtitleLabel")

        self.gridLayout_6.addWidget(self.extendedJavaSubtitleLabel, 0, 0, 1, 1)
        self.extendedJavaInfoLabel = SubtitleLabel(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedJavaInfoLabel.sizePolicy().hasHeightForWidth())
        self.extendedJavaInfoLabel.setSizePolicy(sizePolicy)
        self.extendedJavaInfoLabel.setObjectName("extendedJavaInfoLabel")

        self.gridLayout_6.addWidget(self.extendedJavaInfoLabel, 0, 1, 1, 1)
        self.extendedSetJavaBtnWidget = QWidget(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSetJavaBtnWidget.sizePolicy().hasHeightForWidth())
        self.extendedSetJavaBtnWidget.setSizePolicy(sizePolicy)
        self.extendedSetJavaBtnWidget.setObjectName("extendedSetJavaBtnWidget")

        self.horizontalLayout_7 = QHBoxLayout(self.extendedSetJavaBtnWidget)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.extendedDownloadJavaPrimaryPushBtn = PrimaryPushButton(self.extendedSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.extendedDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedDownloadJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.extendedDownloadJavaPrimaryPushBtn.setObjectName("extendedDownloadJavaPrimaryPushBtn")

        self.horizontalLayout_7.addWidget(self.extendedDownloadJavaPrimaryPushBtn)
        self.extendedManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(self.extendedSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.extendedManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedManuallyAddJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.extendedManuallyAddJavaPrimaryPushBtn.setObjectName("extendedManuallyAddJavaPrimaryPushBtn")

        self.horizontalLayout_7.addWidget(self.extendedManuallyAddJavaPrimaryPushBtn)
        self.extendedAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(self.extendedSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.extendedAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedAutoDetectJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.extendedAutoDetectJavaPrimaryPushBtn.setObjectName("extendedAutoDetectJavaPrimaryPushBtn")

        self.horizontalLayout_7.addWidget(self.extendedAutoDetectJavaPrimaryPushBtn)
        self.extendedJavaListPushBtn = PushButton(self.extendedSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedJavaListPushBtn.sizePolicy().hasHeightForWidth())
        self.extendedJavaListPushBtn.setSizePolicy(sizePolicy)
        self.extendedJavaListPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.extendedJavaListPushBtn.setObjectName("extendedJavaListPushBtn")

        self.horizontalLayout_7.addWidget(self.extendedJavaListPushBtn)
        spacerItem11 = QSpacerItem(127, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem11)
        self.gridLayout_6.addWidget(self.extendedSetJavaBtnWidget, 1, 0, 1, 2)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetJavaWidget)
        self.extendedSetMemWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSetMemWidget.sizePolicy().hasHeightForWidth())
        self.extendedSetMemWidget.setSizePolicy(sizePolicy)
        self.extendedSetMemWidget.setObjectName("extendedSetMemWidget")

        self.gridLayout_7 = QGridLayout(self.extendedSetMemWidget)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.extendedMinMemLineEdit = LineEdit(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedMinMemLineEdit.sizePolicy().hasHeightForWidth())
        self.extendedMinMemLineEdit.setSizePolicy(sizePolicy)
        self.extendedMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedMinMemLineEdit.setObjectName("extendedMinMemLineEdit")

        self.gridLayout_7.addWidget(self.extendedMinMemLineEdit, 1, 1, 1, 1)
        self.extendedMemSubtitleLabel = SubtitleLabel(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedMemSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.extendedMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedMemSubtitleLabel.setObjectName("extendedMemSubtitleLabel")

        self.gridLayout_7.addWidget(self.extendedMemSubtitleLabel, 0, 1, 1, 1)
        self.extendedMaxMemLineEdit = LineEdit(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedMaxMemLineEdit.sizePolicy().hasHeightForWidth())
        self.extendedMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.extendedMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedMaxMemLineEdit.setObjectName("extendedMaxMemLineEdit")

        self.gridLayout_7.addWidget(self.extendedMaxMemLineEdit, 1, 3, 1, 1)
        self.extendedToSymbol = SubtitleLabel(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedToSymbol.sizePolicy().hasHeightForWidth())
        self.extendedToSymbol.setSizePolicy(sizePolicy)
        self.extendedToSymbol.setObjectName("extendedToSymbol")

        self.gridLayout_7.addWidget(self.extendedToSymbol, 1, 2, 1, 1)
        spacerItem12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem12, 1, 5, 1, 1)
        self.extendedMemUnitComboBox = ComboBox(self.extendedSetMemWidget)
        self.extendedMemUnitComboBox.setObjectName("extendedMemUnitComboBox")

        self.gridLayout_7.addWidget(self.extendedMemUnitComboBox, 1, 4, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetMemWidget)
        self.extendedSetCoreWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSetCoreWidget.sizePolicy().hasHeightForWidth())
        self.extendedSetCoreWidget.setSizePolicy(sizePolicy)
        self.extendedSetCoreWidget.setObjectName("extendedSetCoreWidget")

        self.gridLayout_8 = QGridLayout(self.extendedSetCoreWidget)
        self.gridLayout_8.setObjectName("gridLayout_8")

        spacerItem13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem13, 1, 3, 1, 1)
        self.extendedDownloadCorePrimaryPushBtn = PrimaryPushButton(self.extendedSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.extendedDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedDownloadCorePrimaryPushBtn.setObjectName("extendedDownloadCorePrimaryPushBtn")

        self.gridLayout_8.addWidget(self.extendedDownloadCorePrimaryPushBtn, 1, 2, 1, 1)
        self.extendedManuallyAddCorePrimaryPushBtn = PrimaryPushButton(self.extendedSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.extendedManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedManuallyAddCorePrimaryPushBtn.setObjectName("extendedManuallyAddCorePrimaryPushBtn")

        self.gridLayout_8.addWidget(self.extendedManuallyAddCorePrimaryPushBtn, 1, 1, 1, 1)
        self.extendedCoreSubtitleLabel = SubtitleLabel(self.extendedSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedCoreSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.extendedCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedCoreSubtitleLabel.setObjectName("extendedCoreSubtitleLabel")

        self.gridLayout_8.addWidget(self.extendedCoreSubtitleLabel, 0, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetCoreWidget)
        self.extendedSetDeEncodingWidget = QWidget(self.extendedNewServerScrollAreaContents)
        self.extendedSetDeEncodingWidget.setObjectName("extendedSetDeEncodingWidget")

        self.gridLayout_9 = QGridLayout(self.extendedSetDeEncodingWidget)
        self.gridLayout_9.setObjectName("gridLayout_9")

        self.extendedOutputDeEncodingComboBox = ComboBox(self.extendedSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth())
        self.extendedOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.extendedOutputDeEncodingComboBox.setObjectName("extendedOutputDeEncodingComboBox")

        self.gridLayout_9.addWidget(self.extendedOutputDeEncodingComboBox, 2, 1, 1, 1)
        self.extendedDeEncodingSubtitleLabel = SubtitleLabel(self.extendedSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.extendedDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedDeEncodingSubtitleLabel.setObjectName("extendedDeEncodingSubtitleLabel")

        self.gridLayout_9.addWidget(self.extendedDeEncodingSubtitleLabel, 0, 0, 1, 1)
        self.extendedInputDeEncodingComboBox = ComboBox(self.extendedSetDeEncodingWidget)
        self.extendedInputDeEncodingComboBox.setText("")
        self.extendedInputDeEncodingComboBox.setObjectName("extendedInputDeEncodingComboBox")

        self.gridLayout_9.addWidget(self.extendedInputDeEncodingComboBox, 3, 1, 1, 1)
        self.extendedOutputDeEncodingLabel = StrongBodyLabel(self.extendedSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedOutputDeEncodingLabel.sizePolicy().hasHeightForWidth())
        self.extendedOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.extendedOutputDeEncodingLabel.setObjectName("extendedOutputDeEncodingLabel")

        self.gridLayout_9.addWidget(self.extendedOutputDeEncodingLabel, 2, 0, 1, 1)
        self.extendedInputDeEncodingLabel = StrongBodyLabel(self.extendedSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedInputDeEncodingLabel.sizePolicy().hasHeightForWidth())
        self.extendedInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.extendedInputDeEncodingLabel.setObjectName("extendedInputDeEncodingLabel")

        self.gridLayout_9.addWidget(self.extendedInputDeEncodingLabel, 3, 0, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetDeEncodingWidget)
        self.extendedSetJVMArgWidget = QWidget(self.extendedNewServerScrollAreaContents)
        self.extendedSetJVMArgWidget.setObjectName("extendedSetJVMArgWidget")

        self.gridLayout_10 = QGridLayout(self.extendedSetJVMArgWidget)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.extendedJVMArgSubtitleLabel = SubtitleLabel(self.extendedSetJVMArgWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.extendedJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedJVMArgSubtitleLabel.setObjectName("extendedJVMArgSubtitleLabel")

        self.gridLayout_10.addWidget(self.extendedJVMArgSubtitleLabel, 0, 0, 1, 1)
        self.JVMArgPlainTextEdit = PlainTextEdit(self.extendedSetJVMArgWidget)
        self.JVMArgPlainTextEdit.setObjectName("JVMArgPlainTextEdit")

        self.gridLayout_10.addWidget(self.JVMArgPlainTextEdit, 1, 0, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetJVMArgWidget)
        self.extendedSetServerNameWidget = QWidget(self.extendedNewServerScrollAreaContents)
        self.extendedSetServerNameWidget.setObjectName("extendedSetServerNameWidget")

        self.verticalLayout_5 = QVBoxLayout(self.extendedSetServerNameWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.extendedServerNameSubtitleLabel = SubtitleLabel(self.extendedSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedServerNameSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.extendedServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedServerNameSubtitleLabel.setObjectName("extendedServerNameSubtitleLabel")

        self.verticalLayout_5.addWidget(self.extendedServerNameSubtitleLabel)
        self.extendedServerNameLineEdit = LineEdit(self.extendedSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedServerNameLineEdit.sizePolicy().hasHeightForWidth())
        self.extendedServerNameLineEdit.setSizePolicy(sizePolicy)
        self.extendedServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedServerNameLineEdit.setObjectName("extendedServerNameLineEdit")

        self.verticalLayout_5.addWidget(self.extendedServerNameLineEdit)
        self.extendedSaveServerPrimaryPushBtn = PrimaryPushButton(self.extendedSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.extendedSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.extendedSaveServerPrimaryPushBtn.setObjectName("extendedSaveServerPrimaryPushBtn")

        self.verticalLayout_5.addWidget(self.extendedSaveServerPrimaryPushBtn)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetServerNameWidget)
        spacerItem14 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.noobNewServerScrollAreaVerticalLayout_2.addItem(spacerItem14)
        self.extendedNewServerScrollArea.setWidget(self.extendedNewServerScrollAreaContents)
        self.gridLayout_2.addWidget(self.extendedNewServerScrollArea, 1, 1, 1, 1)
        spacerItem15 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem15, 0, 0, 2, 1)
        self.newServerStackedWidget.addWidget(self.extendedNewServerPage)
        self.importNewServerPage = QWidget()
        self.importNewServerPage.setObjectName("importNewServerPage")

        self.gridLayout_21 = QGridLayout(self.importNewServerPage)
        self.gridLayout_21.setObjectName("gridLayout_21")

        self.importTitleWidget = QWidget(self.importNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importTitleWidget.sizePolicy().hasHeightForWidth())
        self.importTitleWidget.setSizePolicy(sizePolicy)
        self.importTitleWidget.setObjectName("importTitleWidget")

        self.horizontalLayout_10 = QHBoxLayout(self.importTitleWidget)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.importBackToGuidePushButton = TransparentToolButton(FIF.PAGE_LEFT, self.importTitleWidget)
        self.importBackToGuidePushButton.setObjectName("importBackToGuidePushButton")

        self.horizontalLayout_10.addWidget(self.importBackToGuidePushButton)
        self.importSubtitleLabel = SubtitleLabel(self.importTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.importSubtitleLabel.setSizePolicy(sizePolicy)
        self.importSubtitleLabel.setObjectName("importSubtitleLabel")
        self.horizontalLayout_10.addWidget(self.importSubtitleLabel)

        self.horizontalLayout_10.addWidget(self.importSubtitleLabel)
        spacerItem16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem16)
        self.gridLayout_21.addWidget(self.importTitleWidget, 0, 1, 1, 1)
        self.importNewServerScrollArea = SmoothScrollArea(self.importNewServerPage)
        self.importNewServerScrollArea.setFrameShape(QFrame.NoFrame)
        self.importNewServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.importNewServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.importNewServerScrollArea.setWidgetResizable(True)

        self.importNewServerScrollAreaContents = QWidget()
        self.importNewServerScrollAreaContents.setGeometry(QRect(0, 0, 608, 355))

        self.noobNewServerScrollAreaVerticalLayout_4 = QVBoxLayout(self.importNewServerScrollAreaContents)
        self.noobNewServerScrollAreaVerticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.noobNewServerScrollAreaVerticalLayout_4.setObjectName("noobNewServerScrollAreaVerticalLayout_4")

        spacerItem17 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.noobNewServerScrollAreaVerticalLayout_4.addItem(spacerItem17)
        self.importNewServerScrollArea.setWidget(self.importNewServerScrollAreaContents)
        self.gridLayout_21.addWidget(self.importNewServerScrollArea, 1, 1, 1, 1)
        spacerItem18 = QSpacerItem(20, 406, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_21.addItem(spacerItem18, 0, 0, 2, 1)
        self.newServerStackedWidget.addWidget(self.importNewServerPage)
        self.gridLayout.addWidget(self.newServerStackedWidget, 2, 2, 1, 1)
        spacerItem19 = QSpacerItem(15, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem19, 1, 3, 2, 1)
        spacerItem20 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem20, 1, 0, 2, 1)

        self.newServerStackedWidget.setCurrentIndex(0)

        self.setObjectName("ConfigureInterface")

        self.noobNewServerScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.noobNewServerScrollArea.setStyleSheet("QScrollArea {background-color: transparent; border: none;}")
        self.extendedNewServerScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.extendedNewServerScrollArea.setStyleSheet("QScrollArea {background-color: transparent; border: none;}")

        # 引导页
        self.titleLabel.setText("新建服务器")
        self.subTitleLabel.setText("有3种方式供你选择。")
        self.noobNewServerBtn.setText("简易模式")
        self.noobNewServerIntro.setText("保留基础配置。\n"
                                        " - Java\n"
                                        " - 服务器核心\n"
                                        " - 最小最大内存\n"
                                        " - 服务器名称")
        self.extendedNewServerBtn.setText("进阶模式")
        self.extendedNewServerIntro.setText("在简易模式基础上\n"
                                            "，\n"
                                            "还能设置：\n"
                                            " - 内存单位\n"
                                            " - 控制台流编码\n"
                                            " - JVM参数")
        self.importNewServerBtn.setText("导入")
        self.importNewServerIntro.setText("暂未完成。")

        # 简易模式
        self.noobJavaSubtitleLabel.setText("Java:")
        self.noobJavaInfoLabel.setText("[选择的Java的信息]")
        self.noobDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.noobManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.noobAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.noobJavaListPushBtn.setText("Java列表")
        self.noobMemUnitLabel.setText("M")
        self.noobToSymbol.setText("~")
        self.noobMemSubtitleLabel.setText("内存:")
        self.noobDownloadCorePrimaryPushBtn.setText("下载核心")
        self.noobManuallyAddCorePrimaryPushBtn.setText("手动导入")
        self.noobCoreSubtitleLabel.setText("核心：")
        self.noobServerNameSubtitleLabel.setText("服务器名称：")
        self.noobSaveServerPrimaryPushBtn.setText("保存！")
        self.noobSubtitleLabel.setText("简易模式")
        self.noobMinMemLineEdit.setPlaceholderText("整数")
        self.noobMaxMemLineEdit.setPlaceholderText("整数")
        self.noobServerNameLineEdit.setPlaceholderText("不能包含非法字符")

        # 进阶模式
        self.extendedSubtitleLabel.setText("进阶模式")
        self.extendedJavaSubtitleLabel.setText("Java:")
        self.extendedJavaInfoLabel.setText("[选择的Java的信息]")
        self.extendedDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.extendedManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.extendedAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.extendedJavaListPushBtn.setText("Java列表")
        self.extendedMemSubtitleLabel.setText("内存:")
        self.extendedToSymbol.setText("~")
        self.extendedDownloadCorePrimaryPushBtn.setText("下载核心")
        self.extendedManuallyAddCorePrimaryPushBtn.setText("手动导入")
        self.extendedCoreSubtitleLabel.setText("核心：")
        self.extendedDeEncodingSubtitleLabel.setText("编码设置：")
        self.extendedOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.extendedInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.extendedJVMArgSubtitleLabel.setText("JVM参数：")
        self.JVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.extendedServerNameSubtitleLabel.setText("服务器名称：")
        self.extendedSaveServerPrimaryPushBtn.setText("保存！")
        self.importSubtitleLabel.setText("导入")
        self.extendedMinMemLineEdit.setPlaceholderText("整数")
        self.extendedMaxMemLineEdit.setPlaceholderText("整数")
        self.extendedServerNameLineEdit.setPlaceholderText("不能包含非法字符")
        self.extendedOutputDeEncodingComboBox.addItems(["跟随全局", "UTF-8", "GBK"])
        self.extendedOutputDeEncodingComboBox.setCurrentIndex(0)
        self.extendedInputDeEncodingComboBox.addItems(["跟随全局", "UTF-8", "GBK"])
        self.extendedInputDeEncodingComboBox.setCurrentIndex(0)
        self.extendedMemUnitComboBox.addItems(["M", "G"])
        self.extendedMemUnitComboBox.setCurrentIndex(0)

        # 引导页绑定
        self.noobNewServerBtn.clicked.connect(self.newServerStackedWidgetNavigation)
        self.extendedNewServerBtn.clicked.connect(self.newServerStackedWidgetNavigation)
        self.importNewServerBtn.clicked.connect(self.newServerStackedWidgetNavigation)

        # # 简易模式绑定
        self.noobBackToGuidePushButton.clicked.connect(self.newServerStackedWidgetNavigateToGuide)
        self.noobManuallyAddJavaPrimaryPushBtn.clicked.connect(self.addJavaManually)
        self.noobAutoDetectJavaPrimaryPushBtn.clicked.connect(self.autoDetectJava)
        # self.noobJavaListPushBtn.clicked.connect()
        self.noobManuallyAddCorePrimaryPushBtn.clicked.connect(self.addCoreManually)
        self.noobSaveServerPrimaryPushBtn.clicked.connect(self.finishNewServer)

        # # 进阶模式绑定
        self.extendedBackToGuidePushButton.clicked.connect(self.newServerStackedWidgetNavigateToGuide)
        self.extendedManuallyAddJavaPrimaryPushBtn.clicked.connect(self.addJavaManually)
        self.extendedAutoDetectJavaPrimaryPushBtn.clicked.connect(self.autoDetectJava)
        # self.extendedJavaListPushBtn.clicked.connect()
        self.extendedManuallyAddCorePrimaryPushBtn.clicked.connect(self.addCoreManually)
        self.extendedSaveServerPrimaryPushBtn.clicked.connect(self.finishNewServer)

        # # 导入法绑定
        self.importBackToGuidePushButton.clicked.connect(self.newServerStackedWidgetNavigateToGuide)

        self.noobNewServerScrollArea.viewport().setStyleSheet(scrollAreaViewportQss)
        self.extendedNewServerScrollArea.viewport().setStyleSheet(scrollAreaViewportQss)
        self.importNewServerScrollArea.viewport().setStyleSheet(scrollAreaViewportQss)

    def newServerStackedWidgetNavigation(self):
        naviList = ["PlaceHolder", self.noobNewServerBtn, self.extendedNewServerBtn, self.importNewServerBtn]
        self.newServerStackedWidget.setCurrentIndex(naviList.index(self.sender()))

    def newServerStackedWidgetNavigateToGuide(self):
        self.newServerStackedWidget.setCurrentIndex(0)

    def addJavaManually(self):
        tmpJavaPath = str(QFileDialog.getOpenFileName(self, "选择java.exe程序", getcwd(), "java.exe")[0])
        if tmpJavaPath != "":
            tmpJavaPath = tmpJavaPath.replace("/", "\\")
            if v := javaDetector.GetJavaVersion(tmpJavaPath):
                tmpNewJavaPath = self.javaPath
                if javaDetector.Java(tmpJavaPath, v) not in tmpNewJavaPath:
                    tmpNewJavaPath.append(javaDetector.Java(tmpJavaPath, v))
                    InfoBar.success(
                        title='已添加',
                        content=f"Java路径：{tmpJavaPath}\n版本：{v}\n已选中此Java。\n但你还需要继续到Java列表中选取。",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                        )
                else:
                    InfoBar.warning(
                        title='未添加',
                        content="此Java已被添加过，也有可能是自动查找Java时已经搜索到了。请检查Java列表。",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=4848,
                        parent=self
                        )
                self.javaPath.clear()
                self.javaPath = tmpNewJavaPath
            else:
                InfoBar.error(
                    title='添加失败',
                    content="此Java无效！",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                    )
        else:
            InfoBar.warning(
                    title='未添加',
                    content="你并没有选择Java。",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                    )

    def autoDetectJava(self):
        # 防止同时多次运行worker线程
        self.noobAutoDetectJavaPrimaryPushBtn.setEnabled(False)
        self.extendedAutoDetectJavaPrimaryPushBtn.setEnabled(False)
        self.javaFindWorkThreadFactory.Create().start()

    @pyqtSlot(list)
    def autoDetectJavaFinished(self, _JavaPaths: list):
        if ospath.exists("MCSL2/AutoDetectJavaHistory.txt"):
            remove("MCSL2/AutoDetectJavaHistory.txt")

        with open("MCSL2/AutoDetectJavaHistory.json", 'w+', encoding='utf-8') as SaveFoundedJava:
            tmpNewJavaPath = self.javaPath
            self.javaPath = list({p[:-1] for p in SaveFoundedJava.readlines()
                                  }.union(set(self.javaPath)).union(set(_JavaPaths)))
            self.javaPath.sort(key=lambda x: x.Version, reverse=False)
            for d in self.javaPath:
                if d not in tmpNewJavaPath:
                    tmpNewJavaPath.append(d)
                else:
                    pass
            self.javaPath.clear()
            self.javaPath = tmpNewJavaPath
                
            JavaPathList = [{"Path": e.Path, "Version": e.Version}
                            for e in self.javaPath]
            dump({"java": JavaPathList}, SaveFoundedJava,
                    sort_keys=True, indent=4, ensure_ascii=False)

    @pyqtSlot(int)
    def onJavaFindWorkThreadFinished(self, sequenceNumber):
        if sequenceNumber > 1:
            InfoBar.success(
            title='查找完毕',
            content=f"一共搜索到了{len(self.javaPath)}个Java。\n请单击“Java列表”按钮查看、选择。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
            )

        self.noobAutoDetectJavaPrimaryPushBtn.setEnabled(True)
        self.extendedAutoDetectJavaPrimaryPushBtn.setEnabled(True)

    def addCoreManually(self):
        tmpCorePath = str(QFileDialog.getOpenFileName(self, "选择*.jar文件", getcwd(), "*.jar")[0]).replace("/", "\\")
        if tmpCorePath != "":
            self.corePath = tmpCorePath
            self.coreFileName = tmpCorePath.split("\\")[-1]
            InfoBar.success(
                        title='已添加',
                        content=f"核心文件名：{self.coreFileName}",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                        )
        else:
            InfoBar.warning(
                    title='未添加',
                    content="你并没有选择服务器核心。",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                    )
    
    def finishNewServer(self):
        # 定义
        currentNewServerType = self.newServerStackedWidget.currentIndex()
        # 检查
        javaResult = self.checkJavaSet()
        memResult = self.checkMemSet(currentNewServerType)
        coreResult = self.checkCoreSet()
        serverNameResult = self.checkServerNameSet(currentNewServerType)
        consoleDeEncodingResult = self.checkDeEncodingSet(currentNewServerType)
        jvmArgResult = self.checkJVMArgSet(currentNewServerType)
        memUnitResult = self.checkMemUnitSet(currentNewServerType)
        totalResultMsg = f"{javaResult[0]}\n{memResult[0]}\n{memUnitResult[0]}\n{coreResult[0]}\n{serverNameResult[0]}\n{consoleDeEncodingResult[0]}\n{jvmArgResult[0]}"
        totalResultIndicator = [javaResult[1], memResult[1], memUnitResult[1], coreResult[1], serverNameResult[1], consoleDeEncodingResult[1], jvmArgResult[1]]
        # 错了多少
        errCount = 0
        for indicator in totalResultIndicator:
            if indicator == 1:
                errCount += 1
            else:
                pass
        # 如果出错
        if errCount != 0:
            title = f'创建服务器失败！有{errCount}个问题。'
            content = f"{totalResultMsg}\n----------------------------\n请根据上方提示，修改后再尝试保存。\n如果确认自己填写的没有问题，请联系开发者。"
            w = MessageBox(title, content, self)
            w.yesButton.setText("好的")
            w.cancelButton.setParent(None)
            w.exec()
        else:
            title = f'请再次检查你设置的参数是否有误：'
            totalJVMArg = ""
            for arg in self.jvmArg:
                totalJVMArg += f"{str(arg)} "
            content = f"{totalResultMsg}\n----------------------------\nJava：{self.selectedJavaPath}\nJava版本：{self.selectedJavaVersion}\n内存：{self.minMem}~{self.maxMem}{self.memUnit}\n服务器核心：{self.corePath}\n服务器核心文件名：{self.coreFileName}\n输出编码设置：{self.extendedOutputDeEncodingComboBox.itemText(self.consoleOutputDeEncoding.index(self.consoleOutputDeEncodingList))}\n输入编码设置：{self.extendedInputDeEncodingComboBox.itemText(self.consoleInputDeEncoding.index(self.consoleInputDeEncodingList))}\nJVM参数：{totalJVMArg}\n服务器名称：{self.serverName}"
            w = MessageBox(title, content, self)
            w.yesButton.setText("无误，添加")
            w.cancelButton.setText("我再看看")
            w.exec()

    def checkJavaSet(self):
        '''检查Java设置'''
        if self.selectedJavaPath != "":
            return "Java检查: 正常", 0
        else:
            return "Java检查: 出错，缺失", 1

    def checkMemSet(self, currentNewServerType):
        '''检查内存设置'''
        minMemLineEditItems = [None, self.noobMinMemLineEdit, self.extendedMinMemLineEdit]
        maxMemLineEditItems = [None, self.noobMaxMemLineEdit, self.noobMaxMemLineEdit]

        # 是否为空
        if (
            minMemLineEditItems[currentNewServerType].text() != ""
            and maxMemLineEditItems[currentNewServerType].text() != ""
        ):
            # 是否是数字
            if (
                minMemLineEditItems[currentNewServerType].text().isdigit()
                and maxMemLineEditItems[currentNewServerType].text().isdigit()
            ):
                # 是否为整数
                if (
                    int(minMemLineEditItems[currentNewServerType].text()) % 1 == 0
                    and int(maxMemLineEditItems[currentNewServerType].text()) % 1 == 0
                ):
                    # 设!
                    self.minMem = int(minMemLineEditItems[currentNewServerType].text())
                    self.maxMem = int(maxMemLineEditItems[currentNewServerType].text())
                    return "内存检查: 正常", 0
                else:
                    return "内存检查: 出错, 不为整数", 1
            else:
                return "内存检查: 出错, 不为数字", 1
        else:
            return "内存检查: 出错, 内容为空", 1

    def checkCoreSet(self):
        '''检查核心设置'''
        if (self.corePath != ""
            and self.coreFileName != ""
            ):
            return "核心检查: 正常", 0
        else:
            return "核心检查: 出错，缺失", 1
        
    def checkServerNameSet(self, currentNewServerType):
        '''检查服务器名称设置'''
        errText = "服务器名称检查: 出错"
        isError: int
        illegalServerNameList = ["aux", "com1", "com2", "prn", "con", "lpt1", "lpt2", "nul"]
        illegalServerCharacterList = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
        serverNameLineEditItems = [None, self.noobServerNameLineEdit, self.extendedServerNameLineEdit]
        for eachIllegalServerName in illegalServerNameList:
            if serverNameLineEditItems[currentNewServerType].text() != eachIllegalServerName:
                isError = 0
            else:
                errText += "，名称与操作系统冲突"
                isError = 1
                break
        for eachIllegalServerCharacter in illegalServerCharacterList:
            if not eachIllegalServerCharacter in serverNameLineEditItems[currentNewServerType].text():
                isError = 0
            else:
                errText += "，名称含有不合法字符"
                isError = 1
                break
        if serverNameLineEditItems[currentNewServerType].text() == "":
            errText += "，未填写"
            isError = 1
        if isError == 1:
            return errText, isError
        else:
            self.serverName = serverNameLineEditItems[currentNewServerType].text()
            return "服务器名称检查: 正常", isError
        
    def checkDeEncodingSet(self, currentNewServerType):
        '''检查编码设置'''
        # Noob
        if currentNewServerType == 1:
            self.consoleOutputDeEncoding = self.consoleOutputDeEncodingList[0]
            self.consoleInputDeEncoding = self.consoleInputDeEncodingList[0]
            return "编码检查：正常（自动处理）", 0
        # Extended
        elif currentNewServerType == 2:
            self.consoleOutputDeEncoding = self.consoleOutputDeEncodingList[self.extendedOutputDeEncodingComboBox.currentIndex()]
            self.consoleInputDeEncoding = self.consoleInputDeEncodingList[self.extendedInputDeEncodingComboBox.currentIndex()]
            return "编码检查：正常（手动设置）", 0

    def checkJVMArgSet(self, currentNewServerType):
        '''检查JVM参数设置'''
        if currentNewServerType == 2:
            # 有写
            if self.JVMArgPlainTextEdit.document() != "":
                self.jvmArg = self.JVMArgPlainTextEdit.toPlainText().split(" ")
                return "JVM参数检查：正常（手动设置）", 0
            # 没写
            else:
                self.jvmArg = ["-Dlog4j2.formatMsgNoLookups=true"]
                return "JVM参数检查：正常（无手动参数，自动启用log4j2防护）", 0
        elif currentNewServerType == 1:
            self.jvmArg = ["-Dlog4j2.formatMsgNoLookups=true"]
            return "JVM参数检查：正常（无手动参数，自动启用log4j2防护）", 0
        
    def checkMemUnitSet(self, currentNewServerType):
        '''检查JVM内存堆单位设置'''
        if currentNewServerType == 1:
            self.memUnit = self.memUnitList[0]
            return "JVM内存堆单位检查：正常（自动设置）", 0
        elif currentNewServerType == 2:
            self.memUnit = self.memUnitList[self.extendedMemUnitComboBox.currentIndex()]
            return "JVM内存堆单位检查：正常（手动设置）", 0
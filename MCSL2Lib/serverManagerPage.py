from PyQt5.QtWidgets import (
    QSizePolicy,
    QFrame,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QSpacerItem,
    QStackedWidget,
    QHBoxLayout
)
from PyQt5.QtCore import (
    Qt,
    QRect,
    QSize,
    pyqtSlot,
    pyqtSignal,
    QThread
)
from PyQt5.QtGui import QPixmap, QCursor
from qfluentwidgets import (
    BodyLabel,
    ComboBox,
    PixmapLabel,
    LineEdit,
    PlainTextEdit,
    PrimaryPushButton,
    PushButton,
    SmoothScrollArea,
    StrongBodyLabel,
    SubtitleLabel,
    TextEdit,
    TitleLabel,
    TransparentToolButton,
    FluentIcon as FIF,
    MessageBox,
    isDarkTheme,
    InfoBar,
    InfoBarPosition,
    Action,
    RoundMenu
)
from MCSL2Lib.serverController import readGlobalServerConfig
from MCSL2Lib.serverManagerWidget import singleServerManager
from MCSL2Lib.variables import _globalMCSL2Variables
from json import loads, dumps
from shutil import rmtree

class _ServerManagerPage(QWidget):

    deleteBtnEnabled = pyqtSignal(bool)

    def __init__(self):

        super().__init__()

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.gridLayout_2 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayout_2.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.gridLayout_2.addWidget(self.subTitleLabel, 1, 0, 1, 1)
        self.stackedWidget = QStackedWidget(self.titleLimitWidget)
        self.stackedWidget.setObjectName("stackedWidget")

        self.serversPage = QWidget()
        self.serversPage.setObjectName("serversPage")

        self.verticalLayout_2 = QVBoxLayout(self.serversPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.serversSmoothScrollArea = SmoothScrollArea(self.serversPage)
        self.serversSmoothScrollArea.setFrameShape(QFrame.NoFrame)
        self.serversSmoothScrollArea.setFrameShadow(QFrame.Plain)
        self.serversSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.serversSmoothScrollArea.setWidgetResizable(True)
        self.serversSmoothScrollArea.setObjectName("serversSmoothScrollArea")

        self.serversScrollAreaWidgetContents = QWidget()
        self.serversScrollAreaWidgetContents.setGeometry(QRect(0, 0, 640, 451))
        self.serversScrollAreaWidgetContents.setObjectName("serversScrollAreaWidgetContents")

        self.verticalLayout = QVBoxLayout(self.serversScrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.serversSmoothScrollArea.setWidget(self.serversScrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.serversSmoothScrollArea)
        self.stackedWidget.addWidget(self.serversPage)
        self.editServerPage = QWidget()
        self.editServerPage.setObjectName("editServerPage")

        self.gridLayout_3 = QGridLayout(self.editServerPage)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.editServerScrollArea = SmoothScrollArea(self.editServerPage)
        self.editServerScrollArea.setFrameShape(QFrame.NoFrame)
        self.editServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.editServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.editServerScrollArea.setWidgetResizable(True)
        self.editServerScrollArea.setObjectName("editServerScrollArea")

        self.editServerScrollAreaContents = QWidget()
        self.editServerScrollAreaContents.setGeometry(QRect(0, -427, 623, 871))
        self.editServerScrollAreaContents.setObjectName("editServerScrollAreaContents")

        self.noobNewServerScrollAreaVerticalLayout_2 = QVBoxLayout(self.editServerScrollAreaContents)
        self.noobNewServerScrollAreaVerticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.noobNewServerScrollAreaVerticalLayout_2.setObjectName("noobNewServerScrollAreaVerticalLayout_2")

        self.editSetJavaWidget = QWidget(self.editServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editSetJavaWidget.sizePolicy().hasHeightForWidth())
        self.editSetJavaWidget.setSizePolicy(sizePolicy)
        self.editSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.editSetJavaWidget.setObjectName("editSetJavaWidget")

        self.gridLayout_6 = QGridLayout(self.editSetJavaWidget)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.editAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(self.editSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.editAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.editAutoDetectJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.editAutoDetectJavaPrimaryPushBtn.setObjectName("editAutoDetectJavaPrimaryPushBtn")

        self.gridLayout_6.addWidget(self.editAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1)
        self.editJavaSubtitleLabel = SubtitleLabel(self.editSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editJavaSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.editJavaSubtitleLabel.setObjectName("editJavaSubtitleLabel")

        self.gridLayout_6.addWidget(self.editJavaSubtitleLabel, 0, 0, 1, 1)
        self.editJavaListPushBtn = PushButton(self.editSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editJavaListPushBtn.sizePolicy().hasHeightForWidth())
        self.editJavaListPushBtn.setSizePolicy(sizePolicy)
        self.editJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.editJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.editJavaListPushBtn.setObjectName("editJavaListPushBtn")

        self.gridLayout_6.addWidget(self.editJavaListPushBtn, 3, 2, 1, 1)
        self.editManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(self.editSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.editManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.editManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.editManuallyAddJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.editManuallyAddJavaPrimaryPushBtn.setObjectName("editManuallyAddJavaPrimaryPushBtn")

        self.gridLayout_6.addWidget(self.editManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1)
        self.editDownloadJavaPrimaryPushBtn = PrimaryPushButton(self.editSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.editDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.editDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.editDownloadJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.editDownloadJavaPrimaryPushBtn.setObjectName("editDownloadJavaPrimaryPushBtn")

        self.gridLayout_6.addWidget(self.editDownloadJavaPrimaryPushBtn, 3, 1, 1, 1)
        self.editJavaTextEdit = TextEdit(self.editSetJavaWidget)
        self.editJavaTextEdit.setObjectName("editJavaTextEdit")

        self.gridLayout_6.addWidget(self.editJavaTextEdit, 2, 0, 2, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetJavaWidget)
        self.editSetMemWidget = QWidget(self.editServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editSetMemWidget.sizePolicy().hasHeightForWidth())
        self.editSetMemWidget.setSizePolicy(sizePolicy)
        self.editSetMemWidget.setObjectName("editSetMemWidget")

        self.gridLayout_7 = QGridLayout(self.editSetMemWidget)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.editToSymbol = SubtitleLabel(self.editSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editToSymbol.sizePolicy().hasHeightForWidth())
        self.editToSymbol.setSizePolicy(sizePolicy)
        self.editToSymbol.setObjectName("editToSymbol")

        self.gridLayout_7.addWidget(self.editToSymbol, 1, 2, 1, 1)
        self.editMemUnitComboBox = ComboBox(self.editSetMemWidget)
        self.editMemUnitComboBox.setObjectName("editMemUnitComboBox")
        self.gridLayout_7.addWidget(self.editMemUnitComboBox, 1, 4, 1, 1)
        self.editMaxMemLineEdit = LineEdit(self.editSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editMaxMemLineEdit.sizePolicy().hasHeightForWidth())
        self.editMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.editMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.editMaxMemLineEdit.setObjectName("editMaxMemLineEdit")

        self.gridLayout_7.addWidget(self.editMaxMemLineEdit, 1, 3, 1, 1)
        self.editMemSubtitleLabel = SubtitleLabel(self.editSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editMemSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.editMemSubtitleLabel.setObjectName("editMemSubtitleLabel")

        self.gridLayout_7.addWidget(self.editMemSubtitleLabel, 0, 1, 1, 1)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem2, 1, 5, 1, 1)
        self.editMinMemLineEdit = LineEdit(self.editSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editMinMemLineEdit.sizePolicy().hasHeightForWidth())
        self.editMinMemLineEdit.setSizePolicy(sizePolicy)
        self.editMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.editMinMemLineEdit.setObjectName("editMinMemLineEdit")

        self.gridLayout_7.addWidget(self.editMinMemLineEdit, 1, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetMemWidget)
        self.editSetCoreWidget = QWidget(self.editServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editSetCoreWidget.sizePolicy().hasHeightForWidth())
        self.editSetCoreWidget.setSizePolicy(sizePolicy)
        self.editSetCoreWidget.setObjectName("editSetCoreWidget")

        self.gridLayout_8 = QGridLayout(self.editSetCoreWidget)
        self.gridLayout_8.setObjectName("gridLayout_8")

        self.noobDownloadCorePrimaryPushBtn = PrimaryPushButton(self.editSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.noobDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobDownloadCorePrimaryPushBtn.setObjectName("noobDownloadCorePrimaryPushBtn")

        self.gridLayout_8.addWidget(self.noobDownloadCorePrimaryPushBtn, 1, 3, 1, 1)
        self.editCoreSubtitleLabel = SubtitleLabel(self.editSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editCoreSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.editCoreSubtitleLabel.setObjectName("editCoreSubtitleLabel")

        self.gridLayout_8.addWidget(self.editCoreSubtitleLabel, 0, 1, 1, 1)
        self.coreLineEdit = LineEdit(self.editSetCoreWidget)
        self.coreLineEdit.setObjectName("coreLineEdit")

        self.gridLayout_8.addWidget(self.coreLineEdit, 1, 1, 1, 1)
        self.noobManuallyAddCorePrimaryPushBtn = PrimaryPushButton(self.editSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.noobManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobManuallyAddCorePrimaryPushBtn.setObjectName("noobManuallyAddCorePrimaryPushBtn")

        self.gridLayout_8.addWidget(self.noobManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetCoreWidget)
        self.editSetDeEncodingWidget = QWidget(self.editServerScrollAreaContents)
        self.editSetDeEncodingWidget.setObjectName("editSetDeEncodingWidget")

        self.gridLayout_9 = QGridLayout(self.editSetDeEncodingWidget)
        self.gridLayout_9.setObjectName("gridLayout_9")

        self.editOutputDeEncodingComboBox = ComboBox(self.editSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth())
        self.editOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.editOutputDeEncodingComboBox.setObjectName("editOutputDeEncodingComboBox")

        self.gridLayout_9.addWidget(self.editOutputDeEncodingComboBox, 2, 1, 1, 1)
        self.editDeEncodingSubtitleLabel = SubtitleLabel(self.editSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.editDeEncodingSubtitleLabel.setObjectName("editDeEncodingSubtitleLabel")

        self.gridLayout_9.addWidget(self.editDeEncodingSubtitleLabel, 0, 0, 1, 1)
        self.editInputDeEncodingComboBox = ComboBox(self.editSetDeEncodingWidget)
        self.editInputDeEncodingComboBox.setText("")
        self.editInputDeEncodingComboBox.setObjectName("editInputDeEncodingComboBox")

        self.gridLayout_9.addWidget(self.editInputDeEncodingComboBox, 3, 1, 1, 1)
        self.editOutputDeEncodingLabel = StrongBodyLabel(self.editSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editOutputDeEncodingLabel.sizePolicy().hasHeightForWidth())
        self.editOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.editOutputDeEncodingLabel.setObjectName("editOutputDeEncodingLabel")

        self.gridLayout_9.addWidget(self.editOutputDeEncodingLabel, 2, 0, 1, 1)
        self.editInputDeEncodingLabel = StrongBodyLabel(self.editSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editInputDeEncodingLabel.sizePolicy().hasHeightForWidth())
        self.editInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.editInputDeEncodingLabel.setObjectName("editInputDeEncodingLabel")

        self.gridLayout_9.addWidget(self.editInputDeEncodingLabel, 3, 0, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetDeEncodingWidget)
        self.editSetJVMArgWidget = QWidget(self.editServerScrollAreaContents)
        self.editSetJVMArgWidget.setObjectName("editSetJVMArgWidget")

        self.gridLayout_10 = QGridLayout(self.editSetJVMArgWidget)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.editJVMArgSubtitleLabel = SubtitleLabel(self.editSetJVMArgWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.editJVMArgSubtitleLabel.setObjectName("editJVMArgSubtitleLabel")

        self.gridLayout_10.addWidget(self.editJVMArgSubtitleLabel, 0, 0, 1, 1)
        self.JVMArgPlainTextEdit = PlainTextEdit(self.editSetJVMArgWidget)
        self.JVMArgPlainTextEdit.setObjectName("JVMArgPlainTextEdit")

        self.gridLayout_10.addWidget(self.JVMArgPlainTextEdit, 1, 0, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetJVMArgWidget)
        self.editSetServerIconWidget = QWidget(self.editServerScrollAreaContents)
        self.editSetServerIconWidget.setObjectName("editSetServerIconWidget")

        self.gridLayout_4 = QGridLayout(self.editSetServerIconWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.tipLabel = BodyLabel(self.editSetServerIconWidget)
        self.tipLabel.setObjectName("tipLabel")

        self.gridLayout_4.addWidget(self.tipLabel, 2, 0, 1, 4)
        self.editServerIcon = ComboBox(self.editSetServerIconWidget)
        self.editServerIcon.setObjectName("editServerIcon")

        self.gridLayout_4.addWidget(self.editServerIcon, 4, 0, 1, 1)
        self.editServerIconSubtitleLabel = SubtitleLabel(self.editSetServerIconWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editServerIconSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editServerIconSubtitleLabel.setSizePolicy(sizePolicy)
        self.editServerIconSubtitleLabel.setObjectName("editServerIconSubtitleLabel")


        self.gridLayout_4.addWidget(self.editServerIconSubtitleLabel, 0, 0, 1, 1)
        self.editServerPixmapLabel = PixmapLabel(self.editSetServerIconWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editServerPixmapLabel.sizePolicy().hasHeightForWidth())
        self.editServerPixmapLabel.setSizePolicy(sizePolicy)
        self.editServerPixmapLabel.setObjectName("editServerPixmapLabel")


        self.gridLayout_4.addWidget(self.editServerPixmapLabel, 4, 2, 1, 1)
        spacerItem3 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 4, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetServerIconWidget)
        self.editSetServerNameWidget = QWidget(self.editServerScrollAreaContents)
        self.editSetServerNameWidget.setObjectName("editSetServerNameWidget")

        self.verticalLayout_5 = QVBoxLayout(self.editSetServerNameWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.editServerNameSubtitleLabel = SubtitleLabel(self.editSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editServerNameSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.editServerNameSubtitleLabel.setObjectName("editServerNameSubtitleLabel")

        self.verticalLayout_5.addWidget(self.editServerNameSubtitleLabel)
        self.editServerNameLineEdit = LineEdit(self.editSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editServerNameLineEdit.sizePolicy().hasHeightForWidth())
        self.editServerNameLineEdit.setSizePolicy(sizePolicy)
        self.editServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.editServerNameLineEdit.setObjectName("editServerNameLineEdit")

        self.verticalLayout_5.addWidget(self.editServerNameLineEdit)
        self.editSaveServerPrimaryPushBtn = PrimaryPushButton(self.editSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth())
        self.editSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.editSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.editSaveServerPrimaryPushBtn.setObjectName("editSaveServerPrimaryPushBtn")

        self.verticalLayout_5.addWidget(self.editSaveServerPrimaryPushBtn)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.editSetServerNameWidget)
        spacerItem4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.noobNewServerScrollAreaVerticalLayout_2.addItem(spacerItem4)
        self.editServerScrollArea.setWidget(self.editServerScrollAreaContents)
        self.gridLayout_3.addWidget(self.editServerScrollArea, 1, 0, 1, 1)
        self.editServerTitleWidget = QWidget(self.editServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editServerTitleWidget.sizePolicy().hasHeightForWidth())
        self.editServerTitleWidget.setSizePolicy(sizePolicy)
        self.editServerTitleWidget.setObjectName("editServerTitleWidget")

        self.horizontalLayout_4 = QHBoxLayout(self.editServerTitleWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.editServerBackPushBtn = TransparentToolButton(FIF.PAGE_LEFT, self.editServerTitleWidget)
        self.editServerBackPushBtn.setObjectName("editServerBackPushBtn")

        self.horizontalLayout_4.addWidget(self.editServerBackPushBtn)
        self.editServerSubtitleLabel = SubtitleLabel(self.editServerTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editServerSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.editServerSubtitleLabel.setSizePolicy(sizePolicy)
        self.editServerSubtitleLabel.setObjectName("editServerSubtitleLabel")
        self.horizontalLayout_4.addWidget(self.editServerSubtitleLabel)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.gridLayout_3.addWidget(self.editServerTitleWidget, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.editServerPage)
        self.gridLayout_2.addWidget(self.stackedWidget, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 2, 2)

        self.setObjectName("ManagerInterface")

        self.subTitleLabel.setText("在此处，管理你所有的服务器。")
        self.titleLabel.setText("管理")
        self.editAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.editJavaSubtitleLabel.setText("Java:")
        self.editJavaListPushBtn.setText("Java列表")
        self.editManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.editDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.editToSymbol.setText("~")
        self.editMemSubtitleLabel.setText("内存:")
        self.noobDownloadCorePrimaryPushBtn.setText("下载核心")
        self.editCoreSubtitleLabel.setText("核心：")
        self.noobManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.editDeEncodingSubtitleLabel.setText("编码设置：")
        self.editOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.editInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.editJVMArgSubtitleLabel.setText("JVM参数：")
        self.JVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.editServerIconSubtitleLabel.setText("服务器图标：")
        self.tipLabel.setText("提示：此处设置的是服务器在MCSL2中显示的图标，不能代表服务器MOTD的图标。")
        self.editServerNameSubtitleLabel.setText("服务器名称：")
        self.editServerNameLineEdit.setPlaceholderText("不能包含非法字符")
        self.editSaveServerPrimaryPushBtn.setText("保存！")
        self.editServerBackPushBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.serversSmoothScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.serversSmoothScrollArea.viewport().setStyleSheet(_globalMCSL2Variables.scrollAreaViewportQss)
        self.editServerScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.editServerScrollArea.viewport().setStyleSheet(_globalMCSL2Variables.scrollAreaViewportQss)

    @pyqtSlot(int)
    def onPageChangedRefresh(self, currentChanged):
        if currentChanged == 2:
            self.refreshServers()
        else:
            pass

    def refreshServers(self):
        
        # 先把旧的清空
        for i in reversed(range(self.verticalLayout.count())):
                self.verticalLayout.itemAt(
                    i).widget().setParent(None)
                
        # 读取全局设置
        globalConfig = readGlobalServerConfig()

        # 添加新的
        for i in range(len(globalConfig)):
            self.tmpSingleServerWidget = singleServerManager()
            self.tmpSingleServerWidget.mem.setText(f"{globalConfig[i]['min_memory']}{globalConfig[i]['memory_unit']}~{globalConfig[i]['max_memory']}{globalConfig[i]['memory_unit']}")
            self.tmpSingleServerWidget.coreFileName.setText(f"{globalConfig[i]['core_file_name']}")
            self.tmpSingleServerWidget.javaPath.setText(f"{globalConfig[i]['java_path']}")
            self.tmpSingleServerWidget.serverName.setText(f"{globalConfig[i]['name']}")
            self.tmpSingleServerWidget.Icon.setPixmap(QPixmap(f":/build-InIcons/{globalConfig[i]['icon']}"))
            self.tmpSingleServerWidget.Icon.setFixedSize(QSize(60, 60))

            self.tmpSingleServerWidget.selectBtn.clicked.connect(self.scrollAreaProcessor)

            self.tmpSingleServerWidget.editBtn.clicked.connect(self.scrollAreaProcessor)

            self.tmpSingleServerWidget.deleteBtn.clicked.connect(self.scrollAreaProcessor)

            self.tmpSingleServerWidget.selectBtn.setObjectName(f"selectBtn{str(i)}")
            self.tmpSingleServerWidget.editBtn.setObjectName(f"editBtn{str(i)}")
            self.tmpSingleServerWidget.deleteBtn.setObjectName(f"deleteBtn{str(i)}")
            self.verticalLayout.addWidget(self.tmpSingleServerWidget)

    # 判断第几个
    def scrollAreaProcessor(self):
        type = str(self.sender().objectName()).split("Btn")[0]
        index = int(str(self.sender().objectName()).split("Btn")[1])
        if type == "select":
            pass
        elif type == "edit":
            self.initEditServerInterface(index=index)
        elif type == "delete":
            self.deleteServer_Step1(index=index)
    
    def deleteServer_Step1(self, index):
        globalConfig: list = readGlobalServerConfig()
        title = f"是否要删除服务器\"{globalConfig[index]['name']}\"?"
        content = f"此操作是不可逆的！你确定这么做吗？"
        w = MessageBox(title, content, self)
        w.yesButton.setText("取消")
        w.cancelButton.setText("删除")
        if isDarkTheme:
            w.cancelButton.setStyleSheet("PushButton {\n"
                                        "    color: black;\n"
                                        "    background: rgba(255, 255, 255, 0.7);\n"
                                        "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                                        "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                        "    border-radius: 5px;\n"
                                        "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                        "    padding: 5px 12px 6px 12px;\n"
                                        "    outline: none;\n"
                                        "}\n"
                                        "QPushButton {\n"
                                        "    background-color: rgba(255, 117, 117, 30%);\n"
                                        "    color: rgb(245, 0, 0)\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: rgba(255, 122, 122, 50%);\n"
                                        "    color: rgb(245, 0, 0)\n"
                                        "}")
        else:
            w.cancelButton.setStyleSheet("PushButton {\n"
                                        "    color: black;\n"
                                        "    background: rgba(255, 255, 255, 0.7);\n"
                                        "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                                        "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                        "    border-radius: 5px;\n"
                                        "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                        "    padding: 5px 12px 6px 12px;\n"
                                        "    outline: none;\n"
                                        "}\n"
                                        "QPushButton {\n"
                                        "    background-color: rgba(255, 117, 117, 30%);\n"
                                        "    color: rgb(255, 0, 0)\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: rgba(255, 122, 122, 50%);\n"
                                        "    color: rgb(255, 0, 0)\n"
                                        "}")
        w.cancelButton.clicked.connect(lambda: self.deleteServer_Step2(index=index))
        w.exec()
    
    def deleteServer_Step2(self, index):
        globalConfig: list = readGlobalServerConfig()
        title = f"你真的要删除服务器\"{globalConfig[index]['name']}\"?"
        content = f"此操作是不可逆的！它会失去很久，很久！\n如果真的要删除，请在下方输入框内输入\"{globalConfig[index]['name']}\"，然后点击“删除”按钮："
        w2 = MessageBox(title, content, self)
        w2.yesButton.setText("取消")
        w2.cancelButton.setText("删除")
        if isDarkTheme:
            w2.cancelButton.setStyleSheet("PushButton {\n"
                                        "    color: black;\n"
                                        "    background: rgba(255, 255, 255, 0.7);\n"
                                        "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                                        "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                        "    border-radius: 5px;\n"
                                        "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                        "    padding: 5px 12px 6px 12px;\n"
                                        "    outline: none;\n"
                                        "}\n"
                                        "QPushButton {\n"
                                        "    background-color: rgba(255, 117, 117, 30%);\n"
                                        "    color: rgb(245, 0, 0)\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: rgba(255, 122, 122, 50%);\n"
                                        "    color: rgb(245, 0, 0)\n"
                                        "}\n"
                                        "QPushButton:disabled {\n"
                                        "    background-color: transparent\n"
                                        "}")
        else:
            w2.cancelButton.setStyleSheet("PushButton {\n"
                                        "    color: black;\n"
                                        "    background: rgba(255, 255, 255, 0.7);\n"
                                        "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                                        "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                        "    border-radius: 5px;\n"
                                        "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                        "    padding: 5px 12px 6px 12px;\n"
                                        "    outline: none;\n"
                                        "}\n"
                                        "QPushButton {\n"
                                        "    background-color: rgba(255, 117, 117, 30%);\n"
                                        "    color: rgb(255, 0, 0)\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: rgba(255, 122, 122, 50%);\n"
                                        "    color: rgb(255, 0, 0)\n"
                                        "}")
        w2.cancelButton.setEnabled(False)
        confirmLineEdit = LineEdit(w2)
        confirmLineEdit.textChanged.connect(lambda: self.compareDeleteServerName(name=globalConfig[index]['name'], LineEditText=confirmLineEdit.text()))
        confirmLineEdit.setPlaceholderText(f"在此输入\"{globalConfig[index]['name']}\"")
        self.deleteBtnEnabled.connect(w2.cancelButton.setEnabled)
        w2.cancelButton.clicked.connect(lambda: self.deleteServer_Step3(index=index))
        w2.vBoxLayout.addWidget(confirmLineEdit)
        w2.exec()
    
    def compareDeleteServerName(self, name, LineEditText):
        self.deleteBtnEnabled.emit(name == LineEditText)

    def deleteServer_Step3(self, index):
        globalConfig: list = readGlobalServerConfig()
        delServerName = globalConfig[index]["name"]

        i = InfoBar.warning(
                        title='警告',
                        content=f"正在删除服务器\"{globalConfig[index]['name']}\"，可能需要一点时间...",
                        orient=Qt.Horizontal,
                        isClosable=False,
                        position=InfoBarPosition.TOP,
                        duration=-1,
                        parent=self
                        )

        self.thread = DeleteServerThread(index=index, delServerName=delServerName)
        self.thread.killWarning.connect(i.setParent)
        self.thread.exit1Msg.connect(self.deleteServer_Step4)
        self.thread.start()
    
    @pyqtSlot(str)
    def deleteServer_Step4(self, exit1Msg):
        if exit1Msg == "":
            InfoBar.success(
                            title='提示',
                            content=f"删除服务器成功！",
                            orient=Qt.Horizontal,
                            isClosable=False,
                            position=InfoBarPosition.TOP,
                            duration=2000,
                            parent=self
                            )
        else:
            InfoBar.error(
                            title='错误',
                            content=f"删除服务器失败！{exit1Msg}",
                            orient=Qt.Horizontal,
                            isClosable=False,
                            position=InfoBarPosition.TOP,
                            duration=2000,
                            parent=self
                            )
        self.refreshServers()

    def initEditServerInterface(self, index):
        globalConfig: list = readGlobalServerConfig()
        self.stackedWidget.setCurrentIndex(1)
        
        consoleOutputDeEncodingList = ["follow", "utf-8", "gbk"]
        consoleInputDeEncodingList = ["follow", "utf-8", "gbk"]
        memUnitList = ["M", "G"]
        self.editServerSubtitleLabel.setText(f"编辑服务器-{globalConfig[index]['name']}")
        self.editJavaTextEdit.setText(globalConfig[index]['java_path'])
        self.editMinMemLineEdit.setText(str(globalConfig[index]['min_memory']))
        self.editMaxMemLineEdit.setText(str(globalConfig[index]['max_memory']))
        self.editJavaTextEdit.setPlaceholderText("写错了就启动不了了（悲")
        self.editMinMemLineEdit.setPlaceholderText("整数")
        self.editMaxMemLineEdit.setPlaceholderText("整数")
        self.editServerNameLineEdit.setPlaceholderText("不能包含非法字符")

        self.editOutputDeEncodingComboBox.addItems(["跟随全局", "UTF-8", "GBK"])
        self.editInputDeEncodingComboBox.addItems(["跟随全局", "UTF-8", "GBK"])
        self.editMemUnitComboBox.addItems(["M", "G"])

        self.editOutputDeEncodingComboBox.setCurrentIndex(consoleOutputDeEncodingList.index(globalConfig[index]['output_decoding']))
        self.editInputDeEncodingComboBox.setCurrentIndex(consoleInputDeEncodingList.index(globalConfig[index]['input_encoding']))
        self.editMemUnitComboBox.setCurrentIndex(memUnitList.index(globalConfig[index]['memory_unit']))
        self.coreLineEdit.setText(globalConfig[index]['core_file_name'])
        self.coreLineEdit.setEnabled(False)
        self.JVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.JVMArgPlainTextEdit.setPlainText(globalConfig[index]['jvm_arg'])
        self.editServerNameLineEdit.setText(globalConfig[index]['name'])
        iconsList = [
            "铁砧",
            "布料",
            "圆石",
            "命令方块",
            "工作台",
            "鸡蛋",
            "玻璃",
            "金块",
            "草方块",
            "草径",
            "Java",
            "MCSL2",
            "Paper核心",
            "红石块",
            "关闭的红石灯",
            "打开的红石灯",
            "Spigot核心"
        ]
        self.editServerIcon.addItems(iconsList)
        iconsDict = {
            "铁砧": "Anvil.png",
            "布料": "Cloth.png",
            "圆石": "CobbleStone.png",
            "命令方块": "CommandBlock.png",
            "工作台": "CraftingTable.png",
            "鸡蛋": "Egg.png",
            "玻璃": "Glass.png",
            "金块": "GoldBlock.png",
            "草方块": "Grass.png",
            "草径": "GrassPath.png",
            "Java": "JavaSpigot.svg",
            "MCSL2": "MCSL2.png",
            "Paper核心": "Paper.png",
            "红石块": "RedstoneBlock.png",
            "关闭的红石灯": "RedstoneLampOff.png",
            "打开的红石灯": "RedstoneLampOn.png",
            "Spigot核心": "Spigot.svg"
        }
        self.editServerPixmapLabel.setPixmap(QPixmap(f":/build-InIcons/{globalConfig[index]['icon']}"))
        print(iconsDict.get(globalConfig[index]['icon']))
        # self.editServerIcon.setCurrentIndex(iconsList.index())
        self.editServerIcon.currentIndexChanged.connect(lambda: self.changeIcon(iconsDict))
        self.editServerPixmapLabel.setFixedSize(QSize(60, 60))

    def changeIcon(self, iconsDict):
        self.editServerPixmapLabel.setPixmap(QPixmap(f":/build-InIcons/{iconsDict[self.editServerIcon.text()]}"))
        self.editServerPixmapLabel.setFixedSize(QSize(60, 60))

# 使用多线程防止假死
class DeleteServerThread(QThread):

    killWarning = pyqtSignal(type(None))
    exitCode = pyqtSignal(int)
    exit1Msg = pyqtSignal(str)

    def __init__(self, index, delServerName, parent=None):
        super().__init__(parent)
        self.index = index
        self.delServerName = delServerName
        self.setObjectName("DeleteServerThread")

    def run(self):
        exit1Msg = ""
        # 删配置
        try:
            with open(r'MCSL2/MCSL2_ServerList.json', "r", encoding='utf-8') as RglobalServerListFile:
                globalServerList = loads(RglobalServerListFile.read())
                RglobalServerListFile.close()
            globalServerList['MCSLServerList'].pop(self.index)
            with open(r'MCSL2/MCSL2_ServerList.json', "w+", encoding='utf-8') as WglobalServerConfigFile:
                WglobalServerConfigFile.write(dumps(globalServerList, indent=4))
                WglobalServerConfigFile.close()
        except Exception as e:
            self.exitCode.emit(1)
            exit1Msg += f"\n{e}"

        # 删文件
        try:
            rmtree(f"Servers//{self.delServerName}")
        except Exception as e:
            self.exitCode.emit(1)
            exit1Msg += f"\n{e}"

        self.killWarning.emit(None)
        self.exit1Msg.emit(exit1Msg)
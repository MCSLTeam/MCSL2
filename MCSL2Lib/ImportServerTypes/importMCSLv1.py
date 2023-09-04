from os import getcwd
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QFrame,
    QFileDialog,
)
from qfluentwidgets import (
    BodyLabel,
    PixmapLabel,
    SubtitleLabel,
    PrimaryPushButton,
    SmoothScrollArea,
    TransparentToolButton,
    FluentIcon as FIF,
    CardWidget,
    ComboBox,
    LineEdit,
    PlainTextEdit,
    StrongBodyLabel,
    PushButton,
    TextEdit,
    InfoBarPosition,
    InfoBar
)

from MCSL2Lib.variables import GlobalMCSL2Variables, MCSLv1ImportVariables
importVariables = MCSLv1ImportVariables()


class MCSLv1(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MCSLv1")
        self.gridLayout_49 = QGridLayout(self)
        self.gridLayout_49.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_49.setObjectName("gridLayout_49")
        spacerItem53 = QSpacerItem(415, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_49.addItem(spacerItem53, 0, 4, 1, 1)
        self.MCSLv1BackToMain = TransparentToolButton(FIF.PAGE_LEFT, self)
        self.MCSLv1BackToMain.setObjectName("MCSLv1BackToMain")
        self.gridLayout_49.addWidget(self.MCSLv1BackToMain, 0, 2, 1, 1)
        spacerItem54 = QSpacerItem(20, 346, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_49.addItem(spacerItem54, 1, 2, 1, 1)
        self.MCSLv1Title = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv1Title.sizePolicy().hasHeightForWidth())
        self.MCSLv1Title.setSizePolicy(sizePolicy)
        self.MCSLv1Title.setObjectName("MCSLv1Title")
        self.gridLayout_49.addWidget(self.MCSLv1Title, 0, 3, 1, 1)
        spacerItem55 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_49.addItem(spacerItem55, 0, 1, 2, 1)
        self.MCSLv1ScrollArea = SmoothScrollArea(self)
        self.MCSLv1ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSLv1ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSLv1ScrollArea.setWidgetResizable(True)
        self.MCSLv1ScrollArea.setAlignment(Qt.AlignCenter)
        self.MCSLv1ScrollArea.setObjectName("MCSLv1ScrollArea")
        self.MCSLv1ScrollAreaWidgetContents = QWidget()
        self.MCSLv1ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 935))
        self.MCSLv1ScrollAreaWidgetContents.setObjectName(
            "MCSLv1ScrollAreaWidgetContents"
        )
        self.verticalLayout_7 = QVBoxLayout(self.MCSLv1ScrollAreaWidgetContents)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.MCSLv1Import = CardWidget(self.MCSLv1ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv1Import.sizePolicy().hasHeightForWidth())
        self.MCSLv1Import.setSizePolicy(sizePolicy)
        self.MCSLv1Import.setMinimumSize(QSize(0, 150))
        self.MCSLv1Import.setMaximumSize(QSize(16777215, 150))
        self.MCSLv1Import.setObjectName("MCSLv1Import")
        self.gridLayout_33 = QGridLayout(self.MCSLv1Import)
        self.gridLayout_33.setObjectName("gridLayout_33")
        self.MCSLv1ImportStatusText = BodyLabel(self.MCSLv1Import)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ImportStatusText.setSizePolicy(sizePolicy)
        self.MCSLv1ImportStatusText.setObjectName("MCSLv1ImportStatusText")
        self.gridLayout_33.addWidget(self.MCSLv1ImportStatusText, 1, 1, 1, 2)
        self.MCSLv1ImportTitle = SubtitleLabel(self.MCSLv1Import)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ImportTitle.setSizePolicy(sizePolicy)
        self.MCSLv1ImportTitle.setObjectName("MCSLv1ImportTitle")
        self.gridLayout_33.addWidget(self.MCSLv1ImportTitle, 0, 2, 1, 1)
        spacerItem56 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_33.addItem(spacerItem56, 2, 5, 1, 3)
        self.MCSLv1ImportStatus = PixmapLabel(self.MCSLv1Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ImportStatus.setSizePolicy(sizePolicy)
        self.MCSLv1ImportStatus.setMinimumSize(QSize(30, 30))
        self.MCSLv1ImportStatus.setMaximumSize(QSize(30, 30))
        self.MCSLv1ImportStatus.setObjectName("MCSLv1ImportStatus")
        self.gridLayout_33.addWidget(self.MCSLv1ImportStatus, 0, 1, 1, 1)
        spacerItem57 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_33.addItem(spacerItem57, 0, 0, 3, 1)
        self.MCSLv1ImportArchives = PrimaryPushButton(self.MCSLv1Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ImportArchives.setSizePolicy(sizePolicy)
        self.MCSLv1ImportArchives.setMinimumSize(QSize(110, 32))
        self.MCSLv1ImportArchives.setMaximumSize(QSize(150, 32))
        self.MCSLv1ImportArchives.setObjectName("MCSLv1ImportArchives")
        self.gridLayout_33.addWidget(self.MCSLv1ImportArchives, 2, 1, 1, 2)
        self.verticalLayout_7.addWidget(self.MCSLv1Import)
        self.MCSLv1ValidateArgs = CardWidget(self.MCSLv1ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgs.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgs.setMinimumSize(QSize(0, 630))
        self.MCSLv1ValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.MCSLv1ValidateArgs.setObjectName("MCSLv1ValidateArgs")
        self.gridLayout_43 = QGridLayout(self.MCSLv1ValidateArgs)
        self.gridLayout_43.setObjectName("gridLayout_43")
        spacerItem58 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_43.addItem(spacerItem58, 0, 0, 21, 1)
        self.MCSLv1ValidateArgsJavaWidget = QWidget(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.MCSLv1ValidateArgsJavaWidget.setObjectName("MCSLv1ValidateArgsJavaWidget")
        self.gridLayout_44 = QGridLayout(self.MCSLv1ValidateArgsJavaWidget)
        self.gridLayout_44.setObjectName("gridLayout_44")
        self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv1ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_44.addWidget(
            self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.MCSLv1ValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.MCSLv1ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsJavaSubtitleLabel.setObjectName(
            "MCSLv1ValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_44.addWidget(
            self.MCSLv1ValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSLv1ValidateArgsJavaListPushBtn = PushButton(
            self.MCSLv1ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.MCSLv1ValidateArgsJavaListPushBtn.setObjectName(
            "MCSLv1ValidateArgsJavaListPushBtn"
        )
        self.gridLayout_44.addWidget(self.MCSLv1ValidateArgsJavaListPushBtn, 3, 2, 1, 1)
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv1ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_44.addWidget(
            self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv1ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_44.addWidget(
            self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.MCSLv1ValidateArgsJavaTextEdit = TextEdit(
            self.MCSLv1ValidateArgsJavaWidget
        )
        self.MCSLv1ValidateArgsJavaTextEdit.setObjectName(
            "MCSLv1ValidateArgsJavaTextEdit"
        )
        self.gridLayout_44.addWidget(self.MCSLv1ValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsJavaWidget, 5, 2, 1, 3)
        self.MCSLv1ValidateArgsDeEncodingWidget = QWidget(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.MCSLv1ValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.MCSLv1ValidateArgsDeEncodingWidget.setObjectName(
            "MCSLv1ValidateArgsDeEncodingWidget"
        )
        self.gridLayout_45 = QGridLayout(self.MCSLv1ValidateArgsDeEncodingWidget)
        self.gridLayout_45.setObjectName("gridLayout_45")
        self.MCSLv1ValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.MCSLv1ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsOutputDeEncodingComboBox.setObjectName(
            "MCSLv1ValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_45.addWidget(
            self.MCSLv1ValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.MCSLv1ValidateArgsInputDeEncodingComboBox = ComboBox(
            self.MCSLv1ValidateArgsDeEncodingWidget
        )
        self.MCSLv1ValidateArgsInputDeEncodingComboBox.setText("")
        self.MCSLv1ValidateArgsInputDeEncodingComboBox.setObjectName(
            "MCSLv1ValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_45.addWidget(
            self.MCSLv1ValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.MCSLv1ValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.MCSLv1ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsOutputDeEncodingLabel.setObjectName(
            "MCSLv1ValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_45.addWidget(
            self.MCSLv1ValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.MCSLv1ValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.MCSLv1ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "MCSLv1ValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_45.addWidget(
            self.MCSLv1ValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSLv1ValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.MCSLv1ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsInputDeEncodingLabel.setObjectName(
            "MCSLv1ValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_45.addWidget(
            self.MCSLv1ValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_43.addWidget(
            self.MCSLv1ValidateArgsDeEncodingWidget, 8, 2, 1, 3
        )
        self.MCSLv1ValidateArgsJVMArgWidget = QWidget(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.MCSLv1ValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.MCSLv1ValidateArgsJVMArgWidget.setObjectName(
            "MCSLv1ValidateArgsJVMArgWidget"
        )
        self.gridLayout_46 = QGridLayout(self.MCSLv1ValidateArgsJVMArgWidget)
        self.gridLayout_46.setObjectName("gridLayout_46")
        self.MCSLv1ValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.MCSLv1ValidateArgsJVMArgWidget
        )
        self.MCSLv1ValidateArgsJVMArgPlainTextEdit.setObjectName(
            "MCSLv1ValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_46.addWidget(
            self.MCSLv1ValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.MCSLv1ValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.MCSLv1ValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsJVMArgSubtitleLabel.setObjectName(
            "MCSLv1ValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_46.addWidget(
            self.MCSLv1ValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.MCSLv1ValidateArgsStatus = PixmapLabel(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsStatus.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.MCSLv1ValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.MCSLv1ValidateArgsStatus.setObjectName("MCSLv1ValidateArgsStatus")
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsStatus, 0, 2, 1, 1)
        self.MCSLv1ValidateArgsMemWidget = QWidget(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.MCSLv1ValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.MCSLv1ValidateArgsMemWidget.setObjectName("MCSLv1ValidateArgsMemWidget")
        self.gridLayout_47 = QGridLayout(self.MCSLv1ValidateArgsMemWidget)
        self.gridLayout_47.setObjectName("gridLayout_47")
        self.MCSLv1ValidateArgsMinMemLineEdit = LineEdit(
            self.MCSLv1ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv1ValidateArgsMinMemLineEdit.setObjectName(
            "MCSLv1ValidateArgsMinMemLineEdit"
        )
        self.gridLayout_47.addWidget(self.MCSLv1ValidateArgsMinMemLineEdit, 1, 1, 1, 1)
        self.MCSLv1ValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.MCSLv1ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsMemSubtitleLabel.setObjectName(
            "MCSLv1ValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_47.addWidget(
            self.MCSLv1ValidateArgsMemSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSLv1ValidateArgsMaxMemLineEdit = LineEdit(
            self.MCSLv1ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv1ValidateArgsMaxMemLineEdit.setObjectName(
            "MCSLv1ValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_47.addWidget(self.MCSLv1ValidateArgsMaxMemLineEdit, 1, 3, 1, 1)
        self.MCSLv1ValidateArgsToSymbol = SubtitleLabel(
            self.MCSLv1ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsToSymbol.setObjectName("MCSLv1ValidateArgsToSymbol")
        self.gridLayout_47.addWidget(self.MCSLv1ValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem59 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_47.addItem(spacerItem59, 1, 5, 1, 1)
        self.MCSLv1ValidateArgsMemUnitComboBox = ComboBox(
            self.MCSLv1ValidateArgsMemWidget
        )
        self.MCSLv1ValidateArgsMemUnitComboBox.setObjectName(
            "MCSLv1ValidateArgsMemUnitComboBox"
        )
        self.gridLayout_47.addWidget(self.MCSLv1ValidateArgsMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsMemWidget, 6, 2, 1, 3)
        self.MCSLv1ValidateArgsTitle = SubtitleLabel(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsTitle.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsTitle.setObjectName("MCSLv1ValidateArgsTitle")
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsTitle, 0, 3, 1, 1)
        self.MCSLv1ValidateArgsCoreWidget = QWidget(self.MCSLv1ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsCoreWidget.setObjectName("MCSLv1ValidateArgsCoreWidget")
        self.gridLayout_48 = QGridLayout(self.MCSLv1ValidateArgsCoreWidget)
        self.gridLayout_48.setObjectName("gridLayout_48")
        self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSLv1ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "MCSLv1ValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_48.addWidget(
            self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.MCSLv1ValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.MCSLv1ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsCoreSubtitleLabel.setObjectName(
            "MCSLv1ValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_48.addWidget(
            self.MCSLv1ValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSLv1ValidateArgsCoreLineEdit = LineEdit(
            self.MCSLv1ValidateArgsCoreWidget
        )
        self.MCSLv1ValidateArgsCoreLineEdit.setObjectName(
            "MCSLv1ValidateArgsCoreLineEdit"
        )
        self.gridLayout_48.addWidget(self.MCSLv1ValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSLv1ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_48.addWidget(
            self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_43.addWidget(self.MCSLv1ValidateArgsCoreWidget, 7, 2, 1, 3)
        self.verticalLayout_7.addWidget(self.MCSLv1ValidateArgs)
        self.MCSLv1Save = CardWidget(self.MCSLv1ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv1Save.sizePolicy().hasHeightForWidth())
        self.MCSLv1Save.setSizePolicy(sizePolicy)
        self.MCSLv1Save.setMinimumSize(QSize(0, 125))
        self.MCSLv1Save.setMaximumSize(QSize(16777215, 125))
        self.MCSLv1Save.setObjectName("MCSLv1Save")
        self.gridLayout_50 = QGridLayout(self.MCSLv1Save)
        self.gridLayout_50.setObjectName("gridLayout_50")
        self.MCSLv1SaveTitle = SubtitleLabel(self.MCSLv1Save)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1SaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1SaveTitle.setSizePolicy(sizePolicy)
        self.MCSLv1SaveTitle.setObjectName("MCSLv1SaveTitle")
        self.gridLayout_50.addWidget(self.MCSLv1SaveTitle, 0, 1, 1, 1)
        self.MCSLv1SaveServerNameLineEdit = LineEdit(self.MCSLv1Save)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1SaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1SaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv1SaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv1SaveServerNameLineEdit.setObjectName("MCSLv1SaveServerNameLineEdit")
        self.gridLayout_50.addWidget(self.MCSLv1SaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem60 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_50.addItem(spacerItem60, 0, 0, 3, 1)
        self.MCSLv1SaveServerPrimaryPushBtn = PrimaryPushButton(self.MCSLv1Save)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv1SaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv1SaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv1SaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.MCSLv1SaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.MCSLv1SaveServerPrimaryPushBtn.setObjectName(
            "MCSLv1SaveServerPrimaryPushBtn"
        )
        self.gridLayout_50.addWidget(self.MCSLv1SaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_7.addWidget(self.MCSLv1Save)
        self.MCSLv1ScrollArea.setWidget(self.MCSLv1ScrollAreaWidgetContents)
        self.gridLayout_49.addWidget(self.MCSLv1ScrollArea, 1, 3, 1, 2)
        self.MCSLv1Title.setText("导入 MCSL 1的服务器")
        self.MCSLv1ImportStatusText.setText("[状态文本]")
        self.MCSLv1ImportTitle.setText("1. 选择MCSL 1主程序")
        self.MCSLv1ImportArchives.setText("选择主程序")
        self.MCSLv1ValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.MCSLv1ValidateArgsJavaSubtitleLabel.setText("Java:")
        self.MCSLv1ValidateArgsJavaListPushBtn.setText("Java列表")
        self.MCSLv1ValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.MCSLv1ValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.MCSLv1ValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.MCSLv1ValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.MCSLv1ValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.MCSLv1ValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.MCSLv1ValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.MCSLv1ValidateArgsMemSubtitleLabel.setText("内存:")
        self.MCSLv1ValidateArgsToSymbol.setText("~")
        self.MCSLv1ValidateArgsTitle.setText("2. 确认参数")
        self.MCSLv1ValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.MCSLv1ValidateArgsCoreSubtitleLabel.setText("核心：")
        self.MCSLv1ValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.MCSLv1SaveTitle.setText("3. 完成导入")
        self.MCSLv1SaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.MCSLv1SaveServerPrimaryPushBtn.setText("导入！")

        self.MCSLv1ScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )

        self.MCSLv1ScrollArea.setFrameShape(QFrame.NoFrame)
        # self.MCSLv1ImportArchives.clicked.connect()
        self.MCSLv1ImportStatus.setPixmap(QPixmap(":/built-InIcons/not.svg"))
        self.MCSLv1ValidateArgsStatus.setPixmap(QPixmap(":/built-InIcons/not.svg"))
        self.MCSLv1ImportStatus.setFixedSize(QSize(30, 30))
        self.MCSLv1ValidateArgsStatus.setFixedSize(QSize(30, 30))
        self.MCSLv1ValidateArgs.setEnabled(False)
        self.MCSLv1Save.setEnabled(False)
        

    def _MCSLv1Import_Func(self):
        tmpCorePath = str(
            QFileDialog.getOpenFileName(self, "选择MCSL 1.x主程序", getcwd(), "*.exe")[0]
        ).replace("/", "\\")
        if tmpCorePath != "":
            configureServerVariables.corePath = tmpCorePath
            configureServerVariables.coreFileName = tmpCorePath.split("\\")[-1]
            InfoBar.success(
                title="已添加",
                content=f"核心文件名：{configureServerVariables.coreFileName}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        else:
            InfoBar.warning(
                title="未添加",
                content="你并没有选择服务器核心。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def _MCSLv1ValidateArgs_Func(self):
        pass
    def _MCSLv1Save_Func(self):
        pass
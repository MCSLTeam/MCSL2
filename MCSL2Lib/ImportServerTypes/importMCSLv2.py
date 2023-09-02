from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
)
from PyQt5.QtCore import QSize, Qt, QRect
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
)
from MCSL2Lib.variables import GlobalMCSL2Variables


class MCSLv2(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MCSLv2")
        self.gridLayout_58 = QGridLayout(self)
        self.gridLayout_58.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_58.setObjectName("gridLayout_58")
        spacerItem61 = QSpacerItem(20, 346, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_58.addItem(spacerItem61, 1, 2, 1, 1)
        self.MCSLv2Title = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv2Title.sizePolicy().hasHeightForWidth())
        self.MCSLv2Title.setSizePolicy(sizePolicy)
        self.MCSLv2Title.setObjectName("MCSLv2Title")
        self.gridLayout_58.addWidget(self.MCSLv2Title, 0, 3, 1, 1)
        self.MCSLv2BackToMain = TransparentToolButton(FIF.PAGE_LEFT, self)
        self.MCSLv2BackToMain.setObjectName("MCSLv2BackToMain")
        self.gridLayout_58.addWidget(self.MCSLv2BackToMain, 0, 2, 1, 1)
        self.MCSLv2ScrollArea = SmoothScrollArea(self)
        self.MCSLv2ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSLv2ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSLv2ScrollArea.setWidgetResizable(True)
        self.MCSLv2ScrollArea.setAlignment(Qt.AlignCenter)
        self.MCSLv2ScrollArea.setObjectName("MCSLv2ScrollArea")
        self.MCSLv2ScrollAreaWidgetContents = QWidget()
        self.MCSLv2ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 526, 935))
        self.MCSLv2ScrollAreaWidgetContents.setObjectName(
            "MCSLv2ScrollAreaWidgetContents"
        )
        self.verticalLayout_8 = QVBoxLayout(self.MCSLv2ScrollAreaWidgetContents)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.MCSLv2Import = CardWidget(self.MCSLv2ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv2Import.sizePolicy().hasHeightForWidth())
        self.MCSLv2Import.setSizePolicy(sizePolicy)
        self.MCSLv2Import.setMinimumSize(QSize(0, 150))
        self.MCSLv2Import.setMaximumSize(QSize(16777215, 150))
        self.MCSLv2Import.setObjectName("MCSLv2Import")
        self.gridLayout_42 = QGridLayout(self.MCSLv2Import)
        self.gridLayout_42.setObjectName("gridLayout_42")
        self.MCSLv2ImportStatusText = BodyLabel(self.MCSLv2Import)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ImportStatusText.setSizePolicy(sizePolicy)
        self.MCSLv2ImportStatusText.setObjectName("MCSLv2ImportStatusText")
        self.gridLayout_42.addWidget(self.MCSLv2ImportStatusText, 1, 1, 1, 2)
        self.MCSLv2ImportTitle = SubtitleLabel(self.MCSLv2Import)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ImportTitle.setSizePolicy(sizePolicy)
        self.MCSLv2ImportTitle.setObjectName("MCSLv2ImportTitle")
        self.gridLayout_42.addWidget(self.MCSLv2ImportTitle, 0, 2, 1, 1)
        spacerItem62 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_42.addItem(spacerItem62, 2, 5, 1, 3)
        self.MCSLv2ImportStatus = PixmapLabel(self.MCSLv2Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ImportStatus.setSizePolicy(sizePolicy)
        self.MCSLv2ImportStatus.setMinimumSize(QSize(30, 30))
        self.MCSLv2ImportStatus.setMaximumSize(QSize(30, 30))
        self.MCSLv2ImportStatus.setObjectName("MCSLv2ImportStatus")
        self.gridLayout_42.addWidget(self.MCSLv2ImportStatus, 0, 1, 1, 1)
        spacerItem63 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_42.addItem(spacerItem63, 0, 0, 3, 1)
        self.MCSLv2ImportArchives = PrimaryPushButton(self.MCSLv2Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ImportArchives.setSizePolicy(sizePolicy)
        self.MCSLv2ImportArchives.setMinimumSize(QSize(110, 32))
        self.MCSLv2ImportArchives.setMaximumSize(QSize(150, 32))
        self.MCSLv2ImportArchives.setObjectName("MCSLv2ImportArchives")
        self.gridLayout_42.addWidget(self.MCSLv2ImportArchives, 2, 1, 1, 2)
        self.verticalLayout_8.addWidget(self.MCSLv2Import)
        self.MCSLv2ValidateArgs = CardWidget(self.MCSLv2ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgs.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgs.setMinimumSize(QSize(0, 630))
        self.MCSLv2ValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.MCSLv2ValidateArgs.setObjectName("MCSLv2ValidateArgs")
        self.gridLayout_51 = QGridLayout(self.MCSLv2ValidateArgs)
        self.gridLayout_51.setObjectName("gridLayout_51")
        spacerItem64 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_51.addItem(spacerItem64, 0, 0, 21, 1)
        self.MCSLv2ValidateArgsJavaWidget = QWidget(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.MCSLv2ValidateArgsJavaWidget.setObjectName("MCSLv2ValidateArgsJavaWidget")
        self.gridLayout_52 = QGridLayout(self.MCSLv2ValidateArgsJavaWidget)
        self.gridLayout_52.setObjectName("gridLayout_52")
        self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv2ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_52.addWidget(
            self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.MCSLv2ValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.MCSLv2ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsJavaSubtitleLabel.setObjectName(
            "MCSLv2ValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_52.addWidget(
            self.MCSLv2ValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSLv2ValidateArgsJavaListPushBtn = PushButton(
            self.MCSLv2ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.MCSLv2ValidateArgsJavaListPushBtn.setObjectName(
            "MCSLv2ValidateArgsJavaListPushBtn"
        )
        self.gridLayout_52.addWidget(self.MCSLv2ValidateArgsJavaListPushBtn, 3, 2, 1, 1)
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv2ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_52.addWidget(
            self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSLv2ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_52.addWidget(
            self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.MCSLv2ValidateArgsJavaTextEdit = TextEdit(
            self.MCSLv2ValidateArgsJavaWidget
        )
        self.MCSLv2ValidateArgsJavaTextEdit.setObjectName(
            "MCSLv2ValidateArgsJavaTextEdit"
        )
        self.gridLayout_52.addWidget(self.MCSLv2ValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsJavaWidget, 5, 2, 1, 3)
        self.MCSLv2ValidateArgsDeEncodingWidget = QWidget(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.MCSLv2ValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.MCSLv2ValidateArgsDeEncodingWidget.setObjectName(
            "MCSLv2ValidateArgsDeEncodingWidget"
        )
        self.gridLayout_53 = QGridLayout(self.MCSLv2ValidateArgsDeEncodingWidget)
        self.gridLayout_53.setObjectName("gridLayout_53")
        self.MCSLv2ValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.MCSLv2ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsOutputDeEncodingComboBox.setObjectName(
            "MCSLv2ValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_53.addWidget(
            self.MCSLv2ValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.MCSLv2ValidateArgsInputDeEncodingComboBox = ComboBox(
            self.MCSLv2ValidateArgsDeEncodingWidget
        )
        self.MCSLv2ValidateArgsInputDeEncodingComboBox.setText("")
        self.MCSLv2ValidateArgsInputDeEncodingComboBox.setObjectName(
            "MCSLv2ValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_53.addWidget(
            self.MCSLv2ValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.MCSLv2ValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.MCSLv2ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsOutputDeEncodingLabel.setObjectName(
            "MCSLv2ValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_53.addWidget(
            self.MCSLv2ValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.MCSLv2ValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.MCSLv2ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "MCSLv2ValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_53.addWidget(
            self.MCSLv2ValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSLv2ValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.MCSLv2ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsInputDeEncodingLabel.setObjectName(
            "MCSLv2ValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_53.addWidget(
            self.MCSLv2ValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_51.addWidget(
            self.MCSLv2ValidateArgsDeEncodingWidget, 8, 2, 1, 3
        )
        self.MCSLv2ValidateArgsJVMArgWidget = QWidget(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.MCSLv2ValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.MCSLv2ValidateArgsJVMArgWidget.setObjectName(
            "MCSLv2ValidateArgsJVMArgWidget"
        )
        self.gridLayout_54 = QGridLayout(self.MCSLv2ValidateArgsJVMArgWidget)
        self.gridLayout_54.setObjectName("gridLayout_54")
        self.MCSLv2ValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.MCSLv2ValidateArgsJVMArgWidget
        )
        self.MCSLv2ValidateArgsJVMArgPlainTextEdit.setObjectName(
            "MCSLv2ValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_54.addWidget(
            self.MCSLv2ValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.MCSLv2ValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.MCSLv2ValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsJVMArgSubtitleLabel.setObjectName(
            "MCSLv2ValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_54.addWidget(
            self.MCSLv2ValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.MCSLv2ValidateArgsStatus = PixmapLabel(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsStatus.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.MCSLv2ValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.MCSLv2ValidateArgsStatus.setObjectName("MCSLv2ValidateArgsStatus")
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsStatus, 0, 2, 1, 1)
        self.MCSLv2ValidateArgsMemWidget = QWidget(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.MCSLv2ValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.MCSLv2ValidateArgsMemWidget.setObjectName("MCSLv2ValidateArgsMemWidget")
        self.gridLayout_55 = QGridLayout(self.MCSLv2ValidateArgsMemWidget)
        self.gridLayout_55.setObjectName("gridLayout_55")
        self.MCSLv2ValidateArgsMinMemLineEdit = LineEdit(
            self.MCSLv2ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv2ValidateArgsMinMemLineEdit.setObjectName(
            "MCSLv2ValidateArgsMinMemLineEdit"
        )
        self.gridLayout_55.addWidget(self.MCSLv2ValidateArgsMinMemLineEdit, 1, 1, 1, 1)
        self.MCSLv2ValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.MCSLv2ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsMemSubtitleLabel.setObjectName(
            "MCSLv2ValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_55.addWidget(
            self.MCSLv2ValidateArgsMemSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSLv2ValidateArgsMaxMemLineEdit = LineEdit(
            self.MCSLv2ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv2ValidateArgsMaxMemLineEdit.setObjectName(
            "MCSLv2ValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_55.addWidget(self.MCSLv2ValidateArgsMaxMemLineEdit, 1, 3, 1, 1)
        self.MCSLv2ValidateArgsToSymbol = SubtitleLabel(
            self.MCSLv2ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsToSymbol.setObjectName("MCSLv2ValidateArgsToSymbol")
        self.gridLayout_55.addWidget(self.MCSLv2ValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem65 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_55.addItem(spacerItem65, 1, 5, 1, 1)
        self.MCSLv2ValidateArgsMemUnitComboBox = ComboBox(
            self.MCSLv2ValidateArgsMemWidget
        )
        self.MCSLv2ValidateArgsMemUnitComboBox.setObjectName(
            "MCSLv2ValidateArgsMemUnitComboBox"
        )
        self.gridLayout_55.addWidget(self.MCSLv2ValidateArgsMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsMemWidget, 6, 2, 1, 3)
        self.MCSLv2ValidateArgsTitle = SubtitleLabel(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsTitle.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsTitle.setObjectName("MCSLv2ValidateArgsTitle")
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsTitle, 0, 3, 1, 1)
        self.MCSLv2ValidateArgsCoreWidget = QWidget(self.MCSLv2ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsCoreWidget.setObjectName("MCSLv2ValidateArgsCoreWidget")
        self.gridLayout_56 = QGridLayout(self.MCSLv2ValidateArgsCoreWidget)
        self.gridLayout_56.setObjectName("gridLayout_56")
        self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSLv2ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "MCSLv2ValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_56.addWidget(
            self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.MCSLv2ValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.MCSLv2ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsCoreSubtitleLabel.setObjectName(
            "MCSLv2ValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_56.addWidget(
            self.MCSLv2ValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSLv2ValidateArgsCoreLineEdit = LineEdit(
            self.MCSLv2ValidateArgsCoreWidget
        )
        self.MCSLv2ValidateArgsCoreLineEdit.setObjectName(
            "MCSLv2ValidateArgsCoreLineEdit"
        )
        self.gridLayout_56.addWidget(self.MCSLv2ValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSLv2ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_56.addWidget(
            self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_51.addWidget(self.MCSLv2ValidateArgsCoreWidget, 7, 2, 1, 3)
        self.verticalLayout_8.addWidget(self.MCSLv2ValidateArgs)
        self.MCSLv2Save = CardWidget(self.MCSLv2ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSLv2Save.sizePolicy().hasHeightForWidth())
        self.MCSLv2Save.setSizePolicy(sizePolicy)
        self.MCSLv2Save.setMinimumSize(QSize(0, 125))
        self.MCSLv2Save.setMaximumSize(QSize(16777215, 125))
        self.MCSLv2Save.setObjectName("MCSLv2Save")
        self.gridLayout_57 = QGridLayout(self.MCSLv2Save)
        self.gridLayout_57.setObjectName("gridLayout_57")
        self.MCSLv2SaveTitle = SubtitleLabel(self.MCSLv2Save)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2SaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2SaveTitle.setSizePolicy(sizePolicy)
        self.MCSLv2SaveTitle.setObjectName("MCSLv2SaveTitle")
        self.gridLayout_57.addWidget(self.MCSLv2SaveTitle, 0, 1, 1, 1)
        self.MCSLv2SaveServerNameLineEdit = LineEdit(self.MCSLv2Save)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2SaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2SaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.MCSLv2SaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSLv2SaveServerNameLineEdit.setObjectName("MCSLv2SaveServerNameLineEdit")
        self.gridLayout_57.addWidget(self.MCSLv2SaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem66 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_57.addItem(spacerItem66, 0, 0, 3, 1)
        self.MCSLv2SaveServerPrimaryPushBtn = PrimaryPushButton(self.MCSLv2Save)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSLv2SaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSLv2SaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSLv2SaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.MCSLv2SaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.MCSLv2SaveServerPrimaryPushBtn.setObjectName(
            "MCSLv2SaveServerPrimaryPushBtn"
        )
        self.gridLayout_57.addWidget(self.MCSLv2SaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_8.addWidget(self.MCSLv2Save)
        self.MCSLv2ScrollArea.setWidget(self.MCSLv2ScrollAreaWidgetContents)
        self.gridLayout_58.addWidget(self.MCSLv2ScrollArea, 1, 3, 1, 2)
        spacerItem67 = QSpacerItem(415, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_58.addItem(spacerItem67, 0, 4, 1, 1)
        spacerItem68 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_58.addItem(spacerItem68, 0, 1, 2, 1)
        self.MCSLv2Title.setText("导入 MCSL 2的服务器")
        self.MCSLv2ImportStatusText.setText("[状态文本]")
        self.MCSLv2ImportTitle.setText("1. 选择MCSL 2生成的MCSL2ServerConfig.json")
        self.MCSLv2ImportArchives.setText("选择配置文件")
        self.MCSLv2ValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.MCSLv2ValidateArgsJavaSubtitleLabel.setText("Java:")
        self.MCSLv2ValidateArgsJavaListPushBtn.setText("Java列表")
        self.MCSLv2ValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.MCSLv2ValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.MCSLv2ValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.MCSLv2ValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.MCSLv2ValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.MCSLv2ValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.MCSLv2ValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.MCSLv2ValidateArgsMemSubtitleLabel.setText("内存:")
        self.MCSLv2ValidateArgsToSymbol.setText("~")
        self.MCSLv2ValidateArgsTitle.setText("2. 确认参数")
        self.MCSLv2ValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.MCSLv2ValidateArgsCoreSubtitleLabel.setText("核心：")
        self.MCSLv2ValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.MCSLv2SaveTitle.setText("3. 完成导入")
        self.MCSLv2SaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.MCSLv2SaveServerPrimaryPushBtn.setText("导入！")

        self.MCSLv2ScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )

from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QFrame,
)
from qfluentwidgets import (
    BodyLabel,
    PixmapLabel,
    SubtitleLabel,
    PrimaryPushButton,
    TransparentToolButton,
    FluentIcon as FIF,
    CardWidget,
    TreeWidget,
    ComboBox,
    LineEdit,
    PlainTextEdit,
    StrongBodyLabel,
    PushButton,
    TextEdit,
)
from MCSL2Lib.Widgets.myScrollArea import MySmoothScrollArea

from MCSL2Lib.variables import GlobalMCSL2Variables


class MCSM8(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MCSM8")
        self.gridLayout_87 = QGridLayout(self)
        self.gridLayout_87.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_87.setObjectName("gridLayout_87")
        self.MCSM8BackToMain = TransparentToolButton(FIF.PAGE_LEFT, self)
        self.MCSM8BackToMain.setObjectName("MCSM8BackToMain")
        self.gridLayout_87.addWidget(self.MCSM8BackToMain, 0, 2, 1, 1)
        spacerItem86 = QSpacerItem(373, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_87.addItem(spacerItem86, 0, 4, 1, 1)
        spacerItem87 = QSpacerItem(20, 340, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_87.addItem(spacerItem87, 1, 2, 1, 1)
        self.MCSM8Title = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM8Title.sizePolicy().hasHeightForWidth())
        self.MCSM8Title.setSizePolicy(sizePolicy)
        self.MCSM8Title.setObjectName("MCSM8Title")
        self.gridLayout_87.addWidget(self.MCSM8Title, 0, 3, 1, 1)
        self.MCSM8ScrollArea = MySmoothScrollArea(self)
        self.MCSM8ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSM8ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSM8ScrollArea.setWidgetResizable(True)
        self.MCSM8ScrollArea.setAlignment(Qt.AlignCenter)
        self.MCSM8ScrollArea.setObjectName("MCSM8ScrollArea")
        self.MCSM8ScrollAreaWidgetContents = QWidget()
        self.MCSM8ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 1191))
        self.MCSM8ScrollAreaWidgetContents.setObjectName(
            "MCSM8ScrollAreaWidgetContents"
        )
        self.verticalLayout_11 = QVBoxLayout(self.MCSM8ScrollAreaWidgetContents)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.MCSM8Import = CardWidget(self.MCSM8ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM8Import.sizePolicy().hasHeightForWidth())
        self.MCSM8Import.setSizePolicy(sizePolicy)
        self.MCSM8Import.setMinimumSize(QSize(0, 150))
        self.MCSM8Import.setMaximumSize(QSize(16777215, 150))
        self.MCSM8Import.setObjectName("MCSM8Import")
        self.gridLayout_70 = QGridLayout(self.MCSM8Import)
        self.gridLayout_70.setObjectName("gridLayout_70")
        spacerItem88 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_70.addItem(spacerItem88, 0, 0, 3, 1)
        self.MCSM8ImportTitle = SubtitleLabel(self.MCSM8Import)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ImportTitle.setSizePolicy(sizePolicy)
        self.MCSM8ImportTitle.setObjectName("MCSM8ImportTitle")
        self.gridLayout_70.addWidget(self.MCSM8ImportTitle, 0, 2, 1, 1)
        self.MCSM8ImportStatusText = BodyLabel(self.MCSM8Import)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ImportStatusText.setSizePolicy(sizePolicy)
        self.MCSM8ImportStatusText.setObjectName("MCSM8ImportStatusText")
        self.gridLayout_70.addWidget(self.MCSM8ImportStatusText, 1, 1, 1, 2)
        self.MCSM8ImportStatus = PixmapLabel(self.MCSM8Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ImportStatus.setSizePolicy(sizePolicy)
        self.MCSM8ImportStatus.setMinimumSize(QSize(30, 30))
        self.MCSM8ImportStatus.setMaximumSize(QSize(30, 30))
        self.MCSM8ImportStatus.setObjectName("MCSM8ImportStatus")
        self.gridLayout_70.addWidget(self.MCSM8ImportStatus, 0, 1, 1, 1)
        spacerItem89 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_70.addItem(spacerItem89, 2, 4, 1, 4)
        self.MCSM8ImportArchives = PrimaryPushButton(self.MCSM8Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ImportArchives.setSizePolicy(sizePolicy)
        self.MCSM8ImportArchives.setMinimumSize(QSize(110, 32))
        self.MCSM8ImportArchives.setMaximumSize(QSize(150, 32))
        self.MCSM8ImportArchives.setObjectName("MCSM8ImportArchives")
        self.gridLayout_70.addWidget(self.MCSM8ImportArchives, 2, 1, 1, 2)
        self.verticalLayout_11.addWidget(self.MCSM8Import)
        self.MCSM8SelectServer = CardWidget(self.MCSM8ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SelectServer.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SelectServer.setSizePolicy(sizePolicy)
        self.MCSM8SelectServer.setMinimumSize(QSize(0, 250))
        self.MCSM8SelectServer.setObjectName("MCSM8SelectServer")
        self.gridLayout_79 = QGridLayout(self.MCSM8SelectServer)
        self.gridLayout_79.setObjectName("gridLayout_79")
        self.MCSM8SelectServerStatus = PixmapLabel(self.MCSM8SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SelectServerStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SelectServerStatus.setSizePolicy(sizePolicy)
        self.MCSM8SelectServerStatus.setMinimumSize(QSize(30, 30))
        self.MCSM8SelectServerStatus.setMaximumSize(QSize(30, 30))
        self.MCSM8SelectServerStatus.setObjectName("MCSM8SelectServerStatus")
        self.gridLayout_79.addWidget(self.MCSM8SelectServerStatus, 0, 1, 1, 1)
        spacerItem90 = QSpacerItem(20, 279, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_79.addItem(spacerItem90, 0, 0, 3, 1)
        self.MCSM8SelectServerStatusText = BodyLabel(self.MCSM8SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SelectServerStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SelectServerStatusText.setSizePolicy(sizePolicy)
        self.MCSM8SelectServerStatusText.setObjectName("MCSM8SelectServerStatusText")
        self.gridLayout_79.addWidget(self.MCSM8SelectServerStatusText, 1, 1, 1, 2)
        self.MCSM8SelectServerTitle = SubtitleLabel(self.MCSM8SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SelectServerTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SelectServerTitle.setSizePolicy(sizePolicy)
        self.MCSM8SelectServerTitle.setObjectName("MCSM8SelectServerTitle")
        self.gridLayout_79.addWidget(self.MCSM8SelectServerTitle, 0, 2, 1, 1)
        self.MCSM8SelectServerTreeWidget = TreeWidget(self.MCSM8SelectServer)
        self.MCSM8SelectServerTreeWidget.setObjectName("MCSM8SelectServerTreeWidget")
        self.MCSM8SelectServerTreeWidget.headerItem().setText(0, "1")
        self.gridLayout_79.addWidget(self.MCSM8SelectServerTreeWidget, 2, 1, 1, 2)
        self.verticalLayout_11.addWidget(self.MCSM8SelectServer)
        self.MCSM8ValidateArgs = CardWidget(self.MCSM8ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgs.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgs.setMinimumSize(QSize(0, 630))
        self.MCSM8ValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.MCSM8ValidateArgs.setObjectName("MCSM8ValidateArgs")
        self.gridLayout_80 = QGridLayout(self.MCSM8ValidateArgs)
        self.gridLayout_80.setObjectName("gridLayout_80")
        self.MCSM8ValidateArgsJavaWidget = QWidget(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.MCSM8ValidateArgsJavaWidget.setObjectName("MCSM8ValidateArgsJavaWidget")
        self.gridLayout_81 = QGridLayout(self.MCSM8ValidateArgsJavaWidget)
        self.gridLayout_81.setObjectName("gridLayout_81")
        self.MCSM8ValidateArgsJavaListPushBtn = PushButton(
            self.MCSM8ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.MCSM8ValidateArgsJavaListPushBtn.setObjectName(
            "MCSM8ValidateArgsJavaListPushBtn"
        )
        self.gridLayout_81.addWidget(self.MCSM8ValidateArgsJavaListPushBtn, 3, 2, 1, 1)
        self.MCSM8ValidateArgsJavaTextEdit = TextEdit(self.MCSM8ValidateArgsJavaWidget)
        self.MCSM8ValidateArgsJavaTextEdit.setObjectName(
            "MCSM8ValidateArgsJavaTextEdit"
        )
        self.gridLayout_81.addWidget(self.MCSM8ValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM8ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_81.addWidget(
            self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM8ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_81.addWidget(
            self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM8ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "MCSM8ValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_81.addWidget(
            self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.MCSM8ValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.MCSM8ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsJavaSubtitleLabel.setObjectName(
            "MCSM8ValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_81.addWidget(
            self.MCSM8ValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsJavaWidget, 5, 2, 1, 3)
        self.MCSM8ValidateArgsDeEncodingWidget = QWidget(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.MCSM8ValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.MCSM8ValidateArgsDeEncodingWidget.setObjectName(
            "MCSM8ValidateArgsDeEncodingWidget"
        )
        self.gridLayout_82 = QGridLayout(self.MCSM8ValidateArgsDeEncodingWidget)
        self.gridLayout_82.setObjectName("gridLayout_82")
        self.MCSM8ValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.MCSM8ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsOutputDeEncodingComboBox.setObjectName(
            "MCSM8ValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_82.addWidget(
            self.MCSM8ValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.MCSM8ValidateArgsInputDeEncodingComboBox = ComboBox(
            self.MCSM8ValidateArgsDeEncodingWidget
        )
        self.MCSM8ValidateArgsInputDeEncodingComboBox.setText("")
        self.MCSM8ValidateArgsInputDeEncodingComboBox.setObjectName(
            "MCSM8ValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_82.addWidget(
            self.MCSM8ValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.MCSM8ValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.MCSM8ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsOutputDeEncodingLabel.setObjectName(
            "MCSM8ValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_82.addWidget(
            self.MCSM8ValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.MCSM8ValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.MCSM8ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "MCSM8ValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_82.addWidget(
            self.MCSM8ValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSM8ValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.MCSM8ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsInputDeEncodingLabel.setObjectName(
            "MCSM8ValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_82.addWidget(
            self.MCSM8ValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsDeEncodingWidget, 8, 2, 1, 3)
        spacerItem91 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_80.addItem(spacerItem91, 0, 0, 21, 1)
        self.MCSM8ValidateArgsJVMArgWidget = QWidget(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.MCSM8ValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.MCSM8ValidateArgsJVMArgWidget.setObjectName(
            "MCSM8ValidateArgsJVMArgWidget"
        )
        self.gridLayout_83 = QGridLayout(self.MCSM8ValidateArgsJVMArgWidget)
        self.gridLayout_83.setObjectName("gridLayout_83")
        self.MCSM8ValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.MCSM8ValidateArgsJVMArgWidget
        )
        self.MCSM8ValidateArgsJVMArgPlainTextEdit.setObjectName(
            "MCSM8ValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_83.addWidget(
            self.MCSM8ValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.MCSM8ValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.MCSM8ValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsJVMArgSubtitleLabel.setObjectName(
            "MCSM8ValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_83.addWidget(
            self.MCSM8ValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.MCSM8ValidateArgsCoreWidget = QWidget(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsCoreWidget.setObjectName("MCSM8ValidateArgsCoreWidget")
        self.gridLayout_84 = QGridLayout(self.MCSM8ValidateArgsCoreWidget)
        self.gridLayout_84.setObjectName("gridLayout_84")
        self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSM8ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "MCSM8ValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_84.addWidget(
            self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.MCSM8ValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.MCSM8ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsCoreSubtitleLabel.setObjectName(
            "MCSM8ValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_84.addWidget(
            self.MCSM8ValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSM8ValidateArgsCoreLineEdit = LineEdit(self.MCSM8ValidateArgsCoreWidget)
        self.MCSM8ValidateArgsCoreLineEdit.setObjectName(
            "MCSM8ValidateArgsCoreLineEdit"
        )
        self.gridLayout_84.addWidget(self.MCSM8ValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSM8ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_84.addWidget(
            self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsCoreWidget, 7, 2, 1, 3)
        self.MCSM8ValidateArgsMemWidget = QWidget(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.MCSM8ValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.MCSM8ValidateArgsMemWidget.setObjectName("MCSM8ValidateArgsMemWidget")
        self.gridLayout_85 = QGridLayout(self.MCSM8ValidateArgsMemWidget)
        self.gridLayout_85.setObjectName("gridLayout_85")
        self.MCSM8ValidateArgsMinMemLineEdit = LineEdit(self.MCSM8ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM8ValidateArgsMinMemLineEdit.setObjectName(
            "MCSM8ValidateArgsMinMemLineEdit"
        )
        self.gridLayout_85.addWidget(self.MCSM8ValidateArgsMinMemLineEdit, 1, 1, 1, 1)
        self.MCSM8ValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.MCSM8ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsMemSubtitleLabel.setObjectName(
            "MCSM8ValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_85.addWidget(self.MCSM8ValidateArgsMemSubtitleLabel, 0, 1, 1, 1)
        self.MCSM8ValidateArgsMaxMemLineEdit = LineEdit(self.MCSM8ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM8ValidateArgsMaxMemLineEdit.setObjectName(
            "MCSM8ValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_85.addWidget(self.MCSM8ValidateArgsMaxMemLineEdit, 1, 3, 1, 1)
        self.MCSM8ValidateArgsToSymbol = SubtitleLabel(self.MCSM8ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsToSymbol.setObjectName("MCSM8ValidateArgsToSymbol")
        self.gridLayout_85.addWidget(self.MCSM8ValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem92 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_85.addItem(spacerItem92, 1, 5, 1, 1)
        self.MCSM8ValidateArgsMemUnitComboBox = ComboBox(
            self.MCSM8ValidateArgsMemWidget
        )
        self.MCSM8ValidateArgsMemUnitComboBox.setObjectName(
            "MCSM8ValidateArgsMemUnitComboBox"
        )
        self.gridLayout_85.addWidget(self.MCSM8ValidateArgsMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsMemWidget, 6, 2, 1, 3)
        self.MCSM8ValidateArgsTitle = SubtitleLabel(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsTitle.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsTitle.setObjectName("MCSM8ValidateArgsTitle")
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsTitle, 0, 3, 1, 1)
        self.MCSM8ValidateArgsStatus = PixmapLabel(self.MCSM8ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8ValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8ValidateArgsStatus.setSizePolicy(sizePolicy)
        self.MCSM8ValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.MCSM8ValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.MCSM8ValidateArgsStatus.setObjectName("MCSM8ValidateArgsStatus")
        self.gridLayout_80.addWidget(self.MCSM8ValidateArgsStatus, 0, 2, 1, 1)
        self.verticalLayout_11.addWidget(self.MCSM8ValidateArgs)
        self.MCSM8Save = CardWidget(self.MCSM8ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM8Save.sizePolicy().hasHeightForWidth())
        self.MCSM8Save.setSizePolicy(sizePolicy)
        self.MCSM8Save.setMinimumSize(QSize(0, 125))
        self.MCSM8Save.setMaximumSize(QSize(16777215, 125))
        self.MCSM8Save.setObjectName("MCSM8Save")
        self.gridLayout_86 = QGridLayout(self.MCSM8Save)
        self.gridLayout_86.setObjectName("gridLayout_86")
        self.MCSM8SaveTitle = SubtitleLabel(self.MCSM8Save)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SaveTitle.setSizePolicy(sizePolicy)
        self.MCSM8SaveTitle.setObjectName("MCSM8SaveTitle")
        self.gridLayout_86.addWidget(self.MCSM8SaveTitle, 0, 1, 1, 1)
        self.MCSM8SaveServerNameLineEdit = LineEdit(self.MCSM8Save)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.MCSM8SaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM8SaveServerNameLineEdit.setObjectName("MCSM8SaveServerNameLineEdit")
        self.gridLayout_86.addWidget(self.MCSM8SaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem93 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_86.addItem(spacerItem93, 0, 0, 3, 1)
        self.MCSM8SaveServerPrimaryPushBtn = PrimaryPushButton(self.MCSM8Save)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM8SaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM8SaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM8SaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.MCSM8SaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.MCSM8SaveServerPrimaryPushBtn.setObjectName(
            "MCSM8SaveServerPrimaryPushBtn"
        )
        self.gridLayout_86.addWidget(self.MCSM8SaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_11.addWidget(self.MCSM8Save)
        self.MCSM8ScrollArea.setWidget(self.MCSM8ScrollAreaWidgetContents)
        self.gridLayout_87.addWidget(self.MCSM8ScrollArea, 1, 3, 1, 2)
        spacerItem94 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_87.addItem(spacerItem94, 0, 1, 2, 1)
        self.MCSM8Title.setText("导入 MCSManager 8 的服务器")
        self.MCSM8ImportTitle.setText("1. 选择 MCSM8 运行目录")
        self.MCSM8ImportStatusText.setText("[状态文本]")
        self.MCSM8ImportArchives.setText("选择文件夹")
        self.MCSM8SelectServerStatusText.setText("[状态文本]")
        self.MCSM8SelectServerTitle.setText("2.选择需要导入的服务器")
        self.MCSM8ValidateArgsJavaListPushBtn.setText("Java列表")
        self.MCSM8ValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.MCSM8ValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.MCSM8ValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.MCSM8ValidateArgsJavaSubtitleLabel.setText("Java:")
        self.MCSM8ValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.MCSM8ValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.MCSM8ValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.MCSM8ValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.MCSM8ValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.MCSM8ValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.MCSM8ValidateArgsCoreSubtitleLabel.setText("核心：")
        self.MCSM8ValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.MCSM8ValidateArgsMemSubtitleLabel.setText("内存:")
        self.MCSM8ValidateArgsToSymbol.setText("~")
        self.MCSM8ValidateArgsTitle.setText("3. 确认参数")
        self.MCSM8SaveTitle.setText("4. 完成导入")
        self.MCSM8SaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.MCSM8SaveServerPrimaryPushBtn.setText("导入！")

        self.MCSM8ScrollArea.setFrameShape(QFrame.NoFrame)

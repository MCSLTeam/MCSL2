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


class MCSM9(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MCSM9")
        self.gridLayout_97 = QGridLayout(self)
        self.gridLayout_97.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_97.setObjectName("gridLayout_97")
        spacerItem95 = QSpacerItem(20, 340, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_97.addItem(spacerItem95, 1, 2, 1, 1)
        self.MCSM9ScrollArea = MySmoothScrollArea(self)
        self.MCSM9ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSM9ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MCSM9ScrollArea.setWidgetResizable(True)
        self.MCSM9ScrollArea.setAlignment(Qt.AlignCenter)
        self.MCSM9ScrollArea.setObjectName("MCSM9ScrollArea")
        self.MCSM9ScrollAreaWidgetContents = QWidget()
        self.MCSM9ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 506, 1191))
        self.MCSM9ScrollAreaWidgetContents.setObjectName(
            "MCSM9ScrollAreaWidgetContents"
        )
        self.verticalLayout_12 = QVBoxLayout(self.MCSM9ScrollAreaWidgetContents)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.MCSM9Import = CardWidget(self.MCSM9ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM9Import.sizePolicy().hasHeightForWidth())
        self.MCSM9Import.setSizePolicy(sizePolicy)
        self.MCSM9Import.setMinimumSize(QSize(0, 150))
        self.MCSM9Import.setMaximumSize(QSize(16777215, 150))
        self.MCSM9Import.setObjectName("MCSM9Import")
        self.gridLayout_88 = QGridLayout(self.MCSM9Import)
        self.gridLayout_88.setObjectName("gridLayout_88")
        spacerItem96 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_88.addItem(spacerItem96, 0, 0, 3, 1)
        self.MCSM9ImportTitle = SubtitleLabel(self.MCSM9Import)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ImportTitle.setSizePolicy(sizePolicy)
        self.MCSM9ImportTitle.setObjectName("MCSM9ImportTitle")
        self.gridLayout_88.addWidget(self.MCSM9ImportTitle, 0, 2, 1, 1)
        self.MCSM9ImportStatusText = BodyLabel(self.MCSM9Import)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ImportStatusText.setSizePolicy(sizePolicy)
        self.MCSM9ImportStatusText.setObjectName("MCSM9ImportStatusText")
        self.gridLayout_88.addWidget(self.MCSM9ImportStatusText, 1, 1, 1, 2)
        self.MCSM9ImportStatus = PixmapLabel(self.MCSM9Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ImportStatus.setSizePolicy(sizePolicy)
        self.MCSM9ImportStatus.setMinimumSize(QSize(30, 30))
        self.MCSM9ImportStatus.setMaximumSize(QSize(30, 30))
        self.MCSM9ImportStatus.setObjectName("MCSM9ImportStatus")
        self.gridLayout_88.addWidget(self.MCSM9ImportStatus, 0, 1, 1, 1)
        spacerItem97 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_88.addItem(spacerItem97, 2, 4, 1, 4)
        self.MCSM9ImportArchives = PrimaryPushButton(self.MCSM9Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ImportArchives.setSizePolicy(sizePolicy)
        self.MCSM9ImportArchives.setMinimumSize(QSize(110, 32))
        self.MCSM9ImportArchives.setMaximumSize(QSize(150, 32))
        self.MCSM9ImportArchives.setObjectName("MCSM9ImportArchives")
        self.gridLayout_88.addWidget(self.MCSM9ImportArchives, 2, 1, 1, 2)
        self.verticalLayout_12.addWidget(self.MCSM9Import)
        self.MCSM9SelectServer = CardWidget(self.MCSM9ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SelectServer.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SelectServer.setSizePolicy(sizePolicy)
        self.MCSM9SelectServer.setMinimumSize(QSize(0, 250))
        self.MCSM9SelectServer.setObjectName("MCSM9SelectServer")
        self.gridLayout_89 = QGridLayout(self.MCSM9SelectServer)
        self.gridLayout_89.setObjectName("gridLayout_89")
        self.MCSM9SelectServerStatus = PixmapLabel(self.MCSM9SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SelectServerStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SelectServerStatus.setSizePolicy(sizePolicy)
        self.MCSM9SelectServerStatus.setMinimumSize(QSize(30, 30))
        self.MCSM9SelectServerStatus.setMaximumSize(QSize(30, 30))
        self.MCSM9SelectServerStatus.setObjectName("MCSM9SelectServerStatus")
        self.gridLayout_89.addWidget(self.MCSM9SelectServerStatus, 0, 1, 1, 1)
        spacerItem98 = QSpacerItem(20, 279, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_89.addItem(spacerItem98, 0, 0, 3, 1)
        self.MCSM9SelectServerStatusText = BodyLabel(self.MCSM9SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SelectServerStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SelectServerStatusText.setSizePolicy(sizePolicy)
        self.MCSM9SelectServerStatusText.setObjectName("MCSM9SelectServerStatusText")
        self.gridLayout_89.addWidget(self.MCSM9SelectServerStatusText, 1, 1, 1, 2)
        self.MCSM9SelectServerTitle = SubtitleLabel(self.MCSM9SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SelectServerTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SelectServerTitle.setSizePolicy(sizePolicy)
        self.MCSM9SelectServerTitle.setObjectName("MCSM9SelectServerTitle")
        self.gridLayout_89.addWidget(self.MCSM9SelectServerTitle, 0, 2, 1, 1)
        self.MCSM9SelectServerTreeWidget = TreeWidget(self.MCSM9SelectServer)
        self.MCSM9SelectServerTreeWidget.setObjectName("MCSM9SelectServerTreeWidget")
        self.MCSM9SelectServerTreeWidget.headerItem().setText(0, "1")
        self.gridLayout_89.addWidget(self.MCSM9SelectServerTreeWidget, 2, 1, 1, 2)
        self.verticalLayout_12.addWidget(self.MCSM9SelectServer)
        self.MCSM9ValidateArgs = CardWidget(self.MCSM9ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgs.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgs.setMinimumSize(QSize(0, 630))
        self.MCSM9ValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.MCSM9ValidateArgs.setObjectName("MCSM9ValidateArgs")
        self.gridLayout_90 = QGridLayout(self.MCSM9ValidateArgs)
        self.gridLayout_90.setObjectName("gridLayout_90")
        self.MCSM9ValidateArgsJavaWidget = QWidget(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.MCSM9ValidateArgsJavaWidget.setObjectName("MCSM9ValidateArgsJavaWidget")
        self.gridLayout_91 = QGridLayout(self.MCSM9ValidateArgsJavaWidget)
        self.gridLayout_91.setObjectName("gridLayout_91")
        self.MCSM9ValidateArgsJavaListPushBtn = PushButton(
            self.MCSM9ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.MCSM9ValidateArgsJavaListPushBtn.setObjectName(
            "MCSM9ValidateArgsJavaListPushBtn"
        )
        self.gridLayout_91.addWidget(self.MCSM9ValidateArgsJavaListPushBtn, 3, 2, 1, 1)
        self.MCSM9ValidateArgsJavaTextEdit = TextEdit(self.MCSM9ValidateArgsJavaWidget)
        self.MCSM9ValidateArgsJavaTextEdit.setObjectName(
            "MCSM9ValidateArgsJavaTextEdit"
        )
        self.gridLayout_91.addWidget(self.MCSM9ValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM9ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_91.addWidget(
            self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM9ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_91.addWidget(
            self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.MCSM9ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "MCSM9ValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_91.addWidget(
            self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.MCSM9ValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.MCSM9ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsJavaSubtitleLabel.setObjectName(
            "MCSM9ValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_91.addWidget(
            self.MCSM9ValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsJavaWidget, 5, 2, 1, 3)
        self.MCSM9ValidateArgsDeEncodingWidget = QWidget(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.MCSM9ValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.MCSM9ValidateArgsDeEncodingWidget.setObjectName(
            "MCSM9ValidateArgsDeEncodingWidget"
        )
        self.gridLayout_92 = QGridLayout(self.MCSM9ValidateArgsDeEncodingWidget)
        self.gridLayout_92.setObjectName("gridLayout_92")
        self.MCSM9ValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.MCSM9ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsOutputDeEncodingComboBox.setObjectName(
            "MCSM9ValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_92.addWidget(
            self.MCSM9ValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.MCSM9ValidateArgsInputDeEncodingComboBox = ComboBox(
            self.MCSM9ValidateArgsDeEncodingWidget
        )
        self.MCSM9ValidateArgsInputDeEncodingComboBox.setText("")
        self.MCSM9ValidateArgsInputDeEncodingComboBox.setObjectName(
            "MCSM9ValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_92.addWidget(
            self.MCSM9ValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.MCSM9ValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.MCSM9ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsOutputDeEncodingLabel.setObjectName(
            "MCSM9ValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_92.addWidget(
            self.MCSM9ValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.MCSM9ValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.MCSM9ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "MCSM9ValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_92.addWidget(
            self.MCSM9ValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.MCSM9ValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.MCSM9ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsInputDeEncodingLabel.setObjectName(
            "MCSM9ValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_92.addWidget(
            self.MCSM9ValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsDeEncodingWidget, 8, 2, 1, 3)
        spacerItem99 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_90.addItem(spacerItem99, 0, 0, 21, 1)
        self.MCSM9ValidateArgsJVMArgWidget = QWidget(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.MCSM9ValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.MCSM9ValidateArgsJVMArgWidget.setObjectName(
            "MCSM9ValidateArgsJVMArgWidget"
        )
        self.gridLayout_93 = QGridLayout(self.MCSM9ValidateArgsJVMArgWidget)
        self.gridLayout_93.setObjectName("gridLayout_93")
        self.MCSM9ValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.MCSM9ValidateArgsJVMArgWidget
        )
        self.MCSM9ValidateArgsJVMArgPlainTextEdit.setObjectName(
            "MCSM9ValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_93.addWidget(
            self.MCSM9ValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.MCSM9ValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.MCSM9ValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsJVMArgSubtitleLabel.setObjectName(
            "MCSM9ValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_93.addWidget(
            self.MCSM9ValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.MCSM9ValidateArgsCoreWidget = QWidget(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsCoreWidget.setObjectName("MCSM9ValidateArgsCoreWidget")
        self.gridLayout_94 = QGridLayout(self.MCSM9ValidateArgsCoreWidget)
        self.gridLayout_94.setObjectName("gridLayout_94")
        self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSM9ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "MCSM9ValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_94.addWidget(
            self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.MCSM9ValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.MCSM9ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsCoreSubtitleLabel.setObjectName(
            "MCSM9ValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_94.addWidget(
            self.MCSM9ValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.MCSM9ValidateArgsCoreLineEdit = LineEdit(self.MCSM9ValidateArgsCoreWidget)
        self.MCSM9ValidateArgsCoreLineEdit.setObjectName(
            "MCSM9ValidateArgsCoreLineEdit"
        )
        self.gridLayout_94.addWidget(self.MCSM9ValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.MCSM9ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_94.addWidget(
            self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsCoreWidget, 7, 2, 1, 3)
        self.MCSM9ValidateArgsMemWidget = QWidget(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.MCSM9ValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.MCSM9ValidateArgsMemWidget.setObjectName("MCSM9ValidateArgsMemWidget")
        self.gridLayout_95 = QGridLayout(self.MCSM9ValidateArgsMemWidget)
        self.gridLayout_95.setObjectName("gridLayout_95")
        self.MCSM9ValidateArgsMinMemLineEdit = LineEdit(self.MCSM9ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM9ValidateArgsMinMemLineEdit.setObjectName(
            "MCSM9ValidateArgsMinMemLineEdit"
        )
        self.gridLayout_95.addWidget(self.MCSM9ValidateArgsMinMemLineEdit, 1, 1, 1, 1)
        self.MCSM9ValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.MCSM9ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsMemSubtitleLabel.setObjectName(
            "MCSM9ValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_95.addWidget(self.MCSM9ValidateArgsMemSubtitleLabel, 0, 1, 1, 1)
        self.MCSM9ValidateArgsMaxMemLineEdit = LineEdit(self.MCSM9ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM9ValidateArgsMaxMemLineEdit.setObjectName(
            "MCSM9ValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_95.addWidget(self.MCSM9ValidateArgsMaxMemLineEdit, 1, 3, 1, 1)
        self.MCSM9ValidateArgsToSymbol = SubtitleLabel(self.MCSM9ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsToSymbol.setObjectName("MCSM9ValidateArgsToSymbol")
        self.gridLayout_95.addWidget(self.MCSM9ValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem100 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_95.addItem(spacerItem100, 1, 5, 1, 1)
        self.MCSM9ValidateArgsMemUnitComboBox = ComboBox(
            self.MCSM9ValidateArgsMemWidget
        )
        self.MCSM9ValidateArgsMemUnitComboBox.setObjectName(
            "MCSM9ValidateArgsMemUnitComboBox"
        )
        self.gridLayout_95.addWidget(self.MCSM9ValidateArgsMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsMemWidget, 6, 2, 1, 3)
        self.MCSM9ValidateArgsTitle = SubtitleLabel(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsTitle.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsTitle.setObjectName("MCSM9ValidateArgsTitle")
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsTitle, 0, 3, 1, 1)
        self.MCSM9ValidateArgsStatus = PixmapLabel(self.MCSM9ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9ValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9ValidateArgsStatus.setSizePolicy(sizePolicy)
        self.MCSM9ValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.MCSM9ValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.MCSM9ValidateArgsStatus.setObjectName("MCSM9ValidateArgsStatus")
        self.gridLayout_90.addWidget(self.MCSM9ValidateArgsStatus, 0, 2, 1, 1)
        self.verticalLayout_12.addWidget(self.MCSM9ValidateArgs)
        self.MCSM9Save = CardWidget(self.MCSM9ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM9Save.sizePolicy().hasHeightForWidth())
        self.MCSM9Save.setSizePolicy(sizePolicy)
        self.MCSM9Save.setMinimumSize(QSize(0, 125))
        self.MCSM9Save.setMaximumSize(QSize(16777215, 125))
        self.MCSM9Save.setObjectName("MCSM9Save")
        self.gridLayout_96 = QGridLayout(self.MCSM9Save)
        self.gridLayout_96.setObjectName("gridLayout_96")
        self.MCSM9SaveTitle = SubtitleLabel(self.MCSM9Save)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SaveTitle.setSizePolicy(sizePolicy)
        self.MCSM9SaveTitle.setObjectName("MCSM9SaveTitle")
        self.gridLayout_96.addWidget(self.MCSM9SaveTitle, 0, 1, 1, 1)
        self.MCSM9SaveServerNameLineEdit = LineEdit(self.MCSM9Save)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.MCSM9SaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.MCSM9SaveServerNameLineEdit.setObjectName("MCSM9SaveServerNameLineEdit")
        self.gridLayout_96.addWidget(self.MCSM9SaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem101 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_96.addItem(spacerItem101, 0, 0, 3, 1)
        self.MCSM9SaveServerPrimaryPushBtn = PrimaryPushButton(self.MCSM9Save)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MCSM9SaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MCSM9SaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MCSM9SaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.MCSM9SaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.MCSM9SaveServerPrimaryPushBtn.setObjectName(
            "MCSM9SaveServerPrimaryPushBtn"
        )
        self.gridLayout_96.addWidget(self.MCSM9SaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_12.addWidget(self.MCSM9Save)
        self.MCSM9ScrollArea.setWidget(self.MCSM9ScrollAreaWidgetContents)
        self.gridLayout_97.addWidget(self.MCSM9ScrollArea, 1, 3, 1, 2)
        self.MCSM9BackToMain = TransparentToolButton(FIF.PAGE_LEFT, self)
        self.MCSM9BackToMain.setObjectName("MCSM9BackToMain")
        self.gridLayout_97.addWidget(self.MCSM9BackToMain, 0, 2, 1, 1)
        spacerItem102 = QSpacerItem(373, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_97.addItem(spacerItem102, 0, 4, 1, 1)
        self.MCSM9Title = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MCSM9Title.sizePolicy().hasHeightForWidth())
        self.MCSM9Title.setSizePolicy(sizePolicy)
        self.MCSM9Title.setObjectName("MCSM9Title")
        self.gridLayout_97.addWidget(self.MCSM9Title, 0, 3, 1, 1)
        spacerItem103 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_97.addItem(spacerItem103, 0, 1, 2, 1)
        self.MCSM9ImportTitle.setText("1. 选择 MCSM9守护进程运行目录daemon")
        self.MCSM9ImportStatusText.setText("[状态文本]")
        self.MCSM9ImportArchives.setText("选择文件夹")
        self.MCSM9SelectServerStatusText.setText("[状态文本]")
        self.MCSM9SelectServerTitle.setText("2.选择需要导入的服务器")
        self.MCSM9ValidateArgsJavaListPushBtn.setText("Java列表")
        self.MCSM9ValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.MCSM9ValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.MCSM9ValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.MCSM9ValidateArgsJavaSubtitleLabel.setText("Java:")
        self.MCSM9ValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.MCSM9ValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.MCSM9ValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.MCSM9ValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.MCSM9ValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.MCSM9ValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.MCSM9ValidateArgsCoreSubtitleLabel.setText("核心：")
        self.MCSM9ValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.MCSM9ValidateArgsMemSubtitleLabel.setText("内存:")
        self.MCSM9ValidateArgsToSymbol.setText("~")
        self.MCSM9ValidateArgsTitle.setText("3. 确认参数")
        self.MCSM9SaveTitle.setText("4. 完成导入")
        self.MCSM9SaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.MCSM9SaveServerPrimaryPushBtn.setText("导入！")
        self.MCSM9Title.setText("导入 MCSManager 9 的服务器")

        self.MCSM9ScrollArea.setFrameShape(QFrame.NoFrame)

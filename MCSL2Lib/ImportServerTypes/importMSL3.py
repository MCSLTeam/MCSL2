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


class MSL3(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MSL3")
        self.gridLayout_67 = QGridLayout(self)
        self.gridLayout_67.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_67.setObjectName("gridLayout_67")
        self.MSL3Title = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MSL3Title.sizePolicy().hasHeightForWidth())
        self.MSL3Title.setSizePolicy(sizePolicy)
        self.MSL3Title.setObjectName("MSL3Title")
        self.gridLayout_67.addWidget(self.MSL3Title, 0, 3, 1, 1)
        spacerItem69 = QSpacerItem(415, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_67.addItem(spacerItem69, 0, 4, 1, 1)
        self.MSL3ScrollArea = MySmoothScrollArea(self)
        self.MSL3ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MSL3ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.MSL3ScrollArea.setWidgetResizable(True)
        self.MSL3ScrollArea.setAlignment(Qt.AlignCenter)
        self.MSL3ScrollArea.setObjectName("MSL3ScrollArea")
        self.MSL3ScrollAreaWidgetContents = QWidget()
        self.MSL3ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 452, 1191))
        self.MSL3ScrollAreaWidgetContents.setObjectName("MSL3ScrollAreaWidgetContents")
        self.verticalLayout_9 = QVBoxLayout(self.MSL3ScrollAreaWidgetContents)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.MSL3Import = CardWidget(self.MSL3ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MSL3Import.sizePolicy().hasHeightForWidth())
        self.MSL3Import.setSizePolicy(sizePolicy)
        self.MSL3Import.setMinimumSize(QSize(0, 150))
        self.MSL3Import.setMaximumSize(QSize(16777215, 150))
        self.MSL3Import.setObjectName("MSL3Import")
        self.gridLayout_59 = QGridLayout(self.MSL3Import)
        self.gridLayout_59.setObjectName("gridLayout_59")
        spacerItem70 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_59.addItem(spacerItem70, 0, 0, 3, 1)
        self.MSL3ImportTitle = SubtitleLabel(self.MSL3Import)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ImportTitle.setSizePolicy(sizePolicy)
        self.MSL3ImportTitle.setObjectName("MSL3ImportTitle")
        self.gridLayout_59.addWidget(self.MSL3ImportTitle, 0, 2, 1, 1)
        self.MSL3ImportStatusText = BodyLabel(self.MSL3Import)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ImportStatusText.setSizePolicy(sizePolicy)
        self.MSL3ImportStatusText.setObjectName("MSL3ImportStatusText")
        self.gridLayout_59.addWidget(self.MSL3ImportStatusText, 1, 1, 1, 2)
        self.MSL3ImportStatus = PixmapLabel(self.MSL3Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ImportStatus.setSizePolicy(sizePolicy)
        self.MSL3ImportStatus.setMinimumSize(QSize(30, 30))
        self.MSL3ImportStatus.setMaximumSize(QSize(30, 30))
        self.MSL3ImportStatus.setObjectName("MSL3ImportStatus")
        self.gridLayout_59.addWidget(self.MSL3ImportStatus, 0, 1, 1, 1)
        spacerItem71 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_59.addItem(spacerItem71, 2, 4, 1, 4)
        self.MSL3ImportArchives = PrimaryPushButton(self.MSL3Import)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ImportArchives.setSizePolicy(sizePolicy)
        self.MSL3ImportArchives.setMinimumSize(QSize(110, 32))
        self.MSL3ImportArchives.setMaximumSize(QSize(150, 32))
        self.MSL3ImportArchives.setObjectName("MSL3ImportArchives")
        self.gridLayout_59.addWidget(self.MSL3ImportArchives, 2, 1, 1, 2)
        self.verticalLayout_9.addWidget(self.MSL3Import)
        self.MSL3SelectServer = CardWidget(self.MSL3ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SelectServer.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SelectServer.setSizePolicy(sizePolicy)
        self.MSL3SelectServer.setMinimumSize(QSize(0, 250))
        self.MSL3SelectServer.setObjectName("MSL3SelectServer")
        self.gridLayout_68 = QGridLayout(self.MSL3SelectServer)
        self.gridLayout_68.setObjectName("gridLayout_68")
        self.MSL3SelectServerStatus = PixmapLabel(self.MSL3SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SelectServerStatus.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SelectServerStatus.setSizePolicy(sizePolicy)
        self.MSL3SelectServerStatus.setMinimumSize(QSize(30, 30))
        self.MSL3SelectServerStatus.setMaximumSize(QSize(30, 30))
        self.MSL3SelectServerStatus.setObjectName("MSL3SelectServerStatus")
        self.gridLayout_68.addWidget(self.MSL3SelectServerStatus, 0, 1, 1, 1)
        spacerItem72 = QSpacerItem(20, 279, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_68.addItem(spacerItem72, 0, 0, 3, 1)
        self.MSL3SelectServerStatusText = BodyLabel(self.MSL3SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SelectServerStatusText.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SelectServerStatusText.setSizePolicy(sizePolicy)
        self.MSL3SelectServerStatusText.setObjectName("MSL3SelectServerStatusText")
        self.gridLayout_68.addWidget(self.MSL3SelectServerStatusText, 1, 1, 1, 2)
        self.MSL3SelectServerTitle = SubtitleLabel(self.MSL3SelectServer)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SelectServerTitle.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SelectServerTitle.setSizePolicy(sizePolicy)
        self.MSL3SelectServerTitle.setObjectName("MSL3SelectServerTitle")
        self.gridLayout_68.addWidget(self.MSL3SelectServerTitle, 0, 2, 1, 1)
        self.MSL3SelectServerTreeWidget = TreeWidget(self.MSL3SelectServer)
        self.MSL3SelectServerTreeWidget.setObjectName("MSL3SelectServerTreeWidget")
        self.MSL3SelectServerTreeWidget.headerItem().setText(0, "1")
        self.gridLayout_68.addWidget(self.MSL3SelectServerTreeWidget, 2, 1, 1, 2)
        self.verticalLayout_9.addWidget(self.MSL3SelectServer)
        self.MSL3ValidateArgs = CardWidget(self.MSL3ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgs.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgs.setMinimumSize(QSize(0, 630))
        self.MSL3ValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.MSL3ValidateArgs.setObjectName("MSL3ValidateArgs")
        self.gridLayout_60 = QGridLayout(self.MSL3ValidateArgs)
        self.gridLayout_60.setObjectName("gridLayout_60")
        self.MSL3ValidateArgsJavaWidget = QWidget(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.MSL3ValidateArgsJavaWidget.setObjectName("MSL3ValidateArgsJavaWidget")
        self.gridLayout_61 = QGridLayout(self.MSL3ValidateArgsJavaWidget)
        self.gridLayout_61.setObjectName("gridLayout_61")
        self.MSL3ValidateArgsJavaListPushBtn = PushButton(
            self.MSL3ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.MSL3ValidateArgsJavaListPushBtn.setObjectName(
            "MSL3ValidateArgsJavaListPushBtn"
        )
        self.gridLayout_61.addWidget(self.MSL3ValidateArgsJavaListPushBtn, 3, 2, 1, 1)
        self.MSL3ValidateArgsJavaTextEdit = TextEdit(self.MSL3ValidateArgsJavaWidget)
        self.MSL3ValidateArgsJavaTextEdit.setObjectName("MSL3ValidateArgsJavaTextEdit")
        self.gridLayout_61.addWidget(self.MSL3ValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.MSL3ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_61.addWidget(
            self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.MSL3ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_61.addWidget(
            self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.MSL3ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "MSL3ValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_61.addWidget(
            self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.MSL3ValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.MSL3ValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsJavaSubtitleLabel.setObjectName(
            "MSL3ValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_61.addWidget(self.MSL3ValidateArgsJavaSubtitleLabel, 0, 0, 1, 1)
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsJavaWidget, 5, 2, 1, 3)
        self.MSL3ValidateArgsDeEncodingWidget = QWidget(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.MSL3ValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.MSL3ValidateArgsDeEncodingWidget.setObjectName(
            "MSL3ValidateArgsDeEncodingWidget"
        )
        self.gridLayout_62 = QGridLayout(self.MSL3ValidateArgsDeEncodingWidget)
        self.gridLayout_62.setObjectName("gridLayout_62")
        self.MSL3ValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.MSL3ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsOutputDeEncodingComboBox.setObjectName(
            "MSL3ValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_62.addWidget(
            self.MSL3ValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.MSL3ValidateArgsInputDeEncodingComboBox = ComboBox(
            self.MSL3ValidateArgsDeEncodingWidget
        )
        self.MSL3ValidateArgsInputDeEncodingComboBox.setText("")
        self.MSL3ValidateArgsInputDeEncodingComboBox.setObjectName(
            "MSL3ValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_62.addWidget(
            self.MSL3ValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.MSL3ValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.MSL3ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsOutputDeEncodingLabel.setObjectName(
            "MSL3ValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_62.addWidget(
            self.MSL3ValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.MSL3ValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.MSL3ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "MSL3ValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_62.addWidget(
            self.MSL3ValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.MSL3ValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.MSL3ValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsInputDeEncodingLabel.setObjectName(
            "MSL3ValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_62.addWidget(
            self.MSL3ValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsDeEncodingWidget, 8, 2, 1, 3)
        spacerItem73 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_60.addItem(spacerItem73, 0, 0, 21, 1)
        self.MSL3ValidateArgsJVMArgWidget = QWidget(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.MSL3ValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.MSL3ValidateArgsJVMArgWidget.setObjectName("MSL3ValidateArgsJVMArgWidget")
        self.gridLayout_63 = QGridLayout(self.MSL3ValidateArgsJVMArgWidget)
        self.gridLayout_63.setObjectName("gridLayout_63")
        self.MSL3ValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.MSL3ValidateArgsJVMArgWidget
        )
        self.MSL3ValidateArgsJVMArgPlainTextEdit.setObjectName(
            "MSL3ValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_63.addWidget(
            self.MSL3ValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.MSL3ValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.MSL3ValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsJVMArgSubtitleLabel.setObjectName(
            "MSL3ValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_63.addWidget(
            self.MSL3ValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.MSL3ValidateArgsCoreWidget = QWidget(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsCoreWidget.setObjectName("MSL3ValidateArgsCoreWidget")
        self.gridLayout_65 = QGridLayout(self.MSL3ValidateArgsCoreWidget)
        self.gridLayout_65.setObjectName("gridLayout_65")
        self.MSL3ValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.MSL3ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MSL3ValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "MSL3ValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_65.addWidget(
            self.MSL3ValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.MSL3ValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.MSL3ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsCoreSubtitleLabel.setObjectName(
            "MSL3ValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_65.addWidget(self.MSL3ValidateArgsCoreSubtitleLabel, 0, 1, 1, 1)
        self.MSL3ValidateArgsCoreLineEdit = LineEdit(self.MSL3ValidateArgsCoreWidget)
        self.MSL3ValidateArgsCoreLineEdit.setObjectName("MSL3ValidateArgsCoreLineEdit")
        self.gridLayout_65.addWidget(self.MSL3ValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.MSL3ValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "MSL3ValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_65.addWidget(
            self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsCoreWidget, 7, 2, 1, 3)
        self.MSL3ValidateArgsMemWidget = QWidget(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.MSL3ValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.MSL3ValidateArgsMemWidget.setObjectName("MSL3ValidateArgsMemWidget")
        self.gridLayout_64 = QGridLayout(self.MSL3ValidateArgsMemWidget)
        self.gridLayout_64.setObjectName("gridLayout_64")
        self.MSL3ValidateArgsMinMemLineEdit = LineEdit(self.MSL3ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MSL3ValidateArgsMinMemLineEdit.setObjectName(
            "MSL3ValidateArgsMinMemLineEdit"
        )
        self.gridLayout_64.addWidget(self.MSL3ValidateArgsMinMemLineEdit, 1, 1, 1, 1)
        self.MSL3ValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.MSL3ValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsMemSubtitleLabel.setObjectName(
            "MSL3ValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_64.addWidget(self.MSL3ValidateArgsMemSubtitleLabel, 0, 1, 1, 1)
        self.MSL3ValidateArgsMaxMemLineEdit = LineEdit(self.MSL3ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.MSL3ValidateArgsMaxMemLineEdit.setObjectName(
            "MSL3ValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_64.addWidget(self.MSL3ValidateArgsMaxMemLineEdit, 1, 3, 1, 1)
        self.MSL3ValidateArgsToSymbol = SubtitleLabel(self.MSL3ValidateArgsMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsToSymbol.setObjectName("MSL3ValidateArgsToSymbol")
        self.gridLayout_64.addWidget(self.MSL3ValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem74 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_64.addItem(spacerItem74, 1, 5, 1, 1)
        self.MSL3ValidateArgsMemUnitComboBox = ComboBox(self.MSL3ValidateArgsMemWidget)
        self.MSL3ValidateArgsMemUnitComboBox.setObjectName(
            "MSL3ValidateArgsMemUnitComboBox"
        )
        self.gridLayout_64.addWidget(self.MSL3ValidateArgsMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsMemWidget, 6, 2, 1, 3)
        self.MSL3ValidateArgsTitle = SubtitleLabel(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsTitle.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsTitle.setObjectName("MSL3ValidateArgsTitle")
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsTitle, 0, 3, 1, 1)
        self.MSL3ValidateArgsStatus = PixmapLabel(self.MSL3ValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3ValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.MSL3ValidateArgsStatus.setSizePolicy(sizePolicy)
        self.MSL3ValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.MSL3ValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.MSL3ValidateArgsStatus.setObjectName("MSL3ValidateArgsStatus")
        self.gridLayout_60.addWidget(self.MSL3ValidateArgsStatus, 0, 2, 1, 1)
        self.verticalLayout_9.addWidget(self.MSL3ValidateArgs)
        self.MSL3Save = CardWidget(self.MSL3ScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MSL3Save.sizePolicy().hasHeightForWidth())
        self.MSL3Save.setSizePolicy(sizePolicy)
        self.MSL3Save.setMinimumSize(QSize(0, 125))
        self.MSL3Save.setMaximumSize(QSize(16777215, 125))
        self.MSL3Save.setObjectName("MSL3Save")
        self.gridLayout_66 = QGridLayout(self.MSL3Save)
        self.gridLayout_66.setObjectName("gridLayout_66")
        self.MSL3SaveTitle = SubtitleLabel(self.MSL3Save)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SaveTitle.setSizePolicy(sizePolicy)
        self.MSL3SaveTitle.setObjectName("MSL3SaveTitle")
        self.gridLayout_66.addWidget(self.MSL3SaveTitle, 0, 1, 1, 1)
        self.MSL3SaveServerNameLineEdit = LineEdit(self.MSL3Save)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.MSL3SaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.MSL3SaveServerNameLineEdit.setObjectName("MSL3SaveServerNameLineEdit")
        self.gridLayout_66.addWidget(self.MSL3SaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem75 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_66.addItem(spacerItem75, 0, 0, 3, 1)
        self.MSL3SaveServerPrimaryPushBtn = PrimaryPushButton(self.MSL3Save)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MSL3SaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.MSL3SaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.MSL3SaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.MSL3SaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.MSL3SaveServerPrimaryPushBtn.setObjectName("MSL3SaveServerPrimaryPushBtn")
        self.gridLayout_66.addWidget(self.MSL3SaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_9.addWidget(self.MSL3Save)
        self.MSL3ScrollArea.setWidget(self.MSL3ScrollAreaWidgetContents)
        self.gridLayout_67.addWidget(self.MSL3ScrollArea, 1, 3, 1, 2)
        self.MSL3BackToMain = TransparentToolButton(FIF.PAGE_LEFT, self)
        self.MSL3BackToMain.setObjectName("MSL3BackToMain")
        self.gridLayout_67.addWidget(self.MSL3BackToMain, 0, 2, 1, 1)
        spacerItem76 = QSpacerItem(20, 346, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_67.addItem(spacerItem76, 1, 2, 1, 1)
        spacerItem77 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_67.addItem(spacerItem77, 0, 1, 2, 1)
        self.MSL3Title.setText("导入 MSL 的服务器")
        self.MSL3ImportTitle.setText("1. 选择MSL文件夹中的ServerList.json")
        self.MSL3ImportStatusText.setText("[状态文本]")
        self.MSL3ImportArchives.setText("选择配置文件")
        self.MSL3SelectServerStatusText.setText("[状态文本]")
        self.MSL3SelectServerTitle.setText("2.选择需要导入的服务器")
        self.MSL3ValidateArgsJavaListPushBtn.setText("Java列表")
        self.MSL3ValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.MSL3ValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.MSL3ValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.MSL3ValidateArgsJavaSubtitleLabel.setText("Java:")
        self.MSL3ValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.MSL3ValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.MSL3ValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.MSL3ValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.MSL3ValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.MSL3ValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.MSL3ValidateArgsCoreSubtitleLabel.setText("核心：")
        self.MSL3ValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.MSL3ValidateArgsMemSubtitleLabel.setText("内存:")
        self.MSL3ValidateArgsToSymbol.setText("~")
        self.MSL3ValidateArgsTitle.setText("3. 确认参数")
        self.MSL3SaveTitle.setText("4. 完成导入")
        self.MSL3SaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.MSL3SaveServerPrimaryPushBtn.setText("导入！")

        self.MSL3ScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )
        self.MSL3ScrollArea.setFrameShape(QFrame.NoFrame)

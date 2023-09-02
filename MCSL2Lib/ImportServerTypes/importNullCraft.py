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


class NullCraft(QWidget):
    def __init__(self):
        super().__init__()
        self.NullCraft = QWidget()
        self.NullCraft.setObjectName("NullCraft")
        self.gridLayout_78 = QGridLayout(self)
        self.gridLayout_78.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_78.setObjectName("gridLayout_78")
        self.NullCraftScrollArea = SmoothScrollArea(self)
        self.NullCraftScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.NullCraftScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.NullCraftScrollArea.setWidgetResizable(True)
        self.NullCraftScrollArea.setAlignment(Qt.AlignCenter)
        self.NullCraftScrollArea.setObjectName("NullCraftScrollArea")
        self.NullCraftScrollAreaWidgetContents = QWidget()
        self.NullCraftScrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 935))
        self.NullCraftScrollAreaWidgetContents.setObjectName(
            "NullCraftScrollAreaWidgetContents"
        )
        self.verticalLayout_10 = QVBoxLayout(self.NullCraftScrollAreaWidgetContents)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.NullCraftImport = CardWidget(self.NullCraftScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftImport.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftImport.setSizePolicy(sizePolicy)
        self.NullCraftImport.setMinimumSize(QSize(0, 150))
        self.NullCraftImport.setMaximumSize(QSize(16777215, 150))
        self.NullCraftImport.setObjectName("NullCraftImport")
        self.gridLayout_69 = QGridLayout(self.NullCraftImport)
        self.gridLayout_69.setObjectName("gridLayout_69")
        spacerItem78 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_69.addItem(spacerItem78, 0, 0, 3, 1)
        self.NullCraftImportTitle = SubtitleLabel(self.NullCraftImport)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftImportTitle.setSizePolicy(sizePolicy)
        self.NullCraftImportTitle.setObjectName("NullCraftImportTitle")
        self.gridLayout_69.addWidget(self.NullCraftImportTitle, 0, 2, 1, 1)
        self.NullCraftImportStatusText = BodyLabel(self.NullCraftImport)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftImportStatusText.setSizePolicy(sizePolicy)
        self.NullCraftImportStatusText.setObjectName("NullCraftImportStatusText")
        self.gridLayout_69.addWidget(self.NullCraftImportStatusText, 1, 1, 1, 2)
        self.NullCraftImportStatus = PixmapLabel(self.NullCraftImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftImportStatus.setSizePolicy(sizePolicy)
        self.NullCraftImportStatus.setMinimumSize(QSize(30, 30))
        self.NullCraftImportStatus.setMaximumSize(QSize(30, 30))
        self.NullCraftImportStatus.setObjectName("NullCraftImportStatus")
        self.gridLayout_69.addWidget(self.NullCraftImportStatus, 0, 1, 1, 1)
        spacerItem79 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_69.addItem(spacerItem79, 2, 4, 1, 4)
        self.NullCraftImportArchives = PrimaryPushButton(self.NullCraftImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftImportArchives.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftImportArchives.setSizePolicy(sizePolicy)
        self.NullCraftImportArchives.setMinimumSize(QSize(110, 32))
        self.NullCraftImportArchives.setMaximumSize(QSize(150, 32))
        self.NullCraftImportArchives.setObjectName("NullCraftImportArchives")
        self.gridLayout_69.addWidget(self.NullCraftImportArchives, 2, 1, 1, 2)
        self.verticalLayout_10.addWidget(self.NullCraftImport)
        self.NullCraftValidateArgs = CardWidget(self.NullCraftScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgs.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgs.setMinimumSize(QSize(0, 630))
        self.NullCraftValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.NullCraftValidateArgs.setObjectName("NullCraftValidateArgs")
        self.gridLayout_71 = QGridLayout(self.NullCraftValidateArgs)
        self.gridLayout_71.setObjectName("gridLayout_71")
        self.NullCraftValidateArgsJavaWidget = QWidget(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.NullCraftValidateArgsJavaWidget.setObjectName(
            "NullCraftValidateArgsJavaWidget"
        )
        self.gridLayout_72 = QGridLayout(self.NullCraftValidateArgsJavaWidget)
        self.gridLayout_72.setObjectName("gridLayout_72")
        self.NullCraftValidateArgsJavaListPushBtn = PushButton(
            self.NullCraftValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.NullCraftValidateArgsJavaListPushBtn.setObjectName(
            "NullCraftValidateArgsJavaListPushBtn"
        )
        self.gridLayout_72.addWidget(
            self.NullCraftValidateArgsJavaListPushBtn, 3, 2, 1, 1
        )
        self.NullCraftValidateArgsJavaTextEdit = TextEdit(
            self.NullCraftValidateArgsJavaWidget
        )
        self.NullCraftValidateArgsJavaTextEdit.setObjectName(
            "NullCraftValidateArgsJavaTextEdit"
        )
        self.gridLayout_72.addWidget(self.NullCraftValidateArgsJavaTextEdit, 2, 0, 2, 1)
        self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.NullCraftValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_72.addWidget(
            self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.NullCraftValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_72.addWidget(
            self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.NullCraftValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "NullCraftValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_72.addWidget(
            self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.NullCraftValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.NullCraftValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsJavaSubtitleLabel.setObjectName(
            "NullCraftValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_72.addWidget(
            self.NullCraftValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsJavaWidget, 5, 2, 1, 3)
        self.NullCraftValidateArgsDeEncodingWidget = QWidget(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.NullCraftValidateArgsDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.NullCraftValidateArgsDeEncodingWidget.setObjectName(
            "NullCraftValidateArgsDeEncodingWidget"
        )
        self.gridLayout_73 = QGridLayout(self.NullCraftValidateArgsDeEncodingWidget)
        self.gridLayout_73.setObjectName("gridLayout_73")
        self.NullCraftValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.NullCraftValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsOutputDeEncodingComboBox.setObjectName(
            "NullCraftValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_73.addWidget(
            self.NullCraftValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.NullCraftValidateArgsInputDeEncodingComboBox = ComboBox(
            self.NullCraftValidateArgsDeEncodingWidget
        )
        self.NullCraftValidateArgsInputDeEncodingComboBox.setText("")
        self.NullCraftValidateArgsInputDeEncodingComboBox.setObjectName(
            "NullCraftValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_73.addWidget(
            self.NullCraftValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.NullCraftValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.NullCraftValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsOutputDeEncodingLabel.setObjectName(
            "NullCraftValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_73.addWidget(
            self.NullCraftValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.NullCraftValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.NullCraftValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "NullCraftValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_73.addWidget(
            self.NullCraftValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.NullCraftValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.NullCraftValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsInputDeEncodingLabel.setObjectName(
            "NullCraftValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_73.addWidget(
            self.NullCraftValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_71.addWidget(
            self.NullCraftValidateArgsDeEncodingWidget, 8, 2, 1, 3
        )
        spacerItem80 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_71.addItem(spacerItem80, 0, 0, 21, 1)
        self.NullCraftValidateArgsJVMArgWidget = QWidget(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.NullCraftValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.NullCraftValidateArgsJVMArgWidget.setObjectName(
            "NullCraftValidateArgsJVMArgWidget"
        )
        self.gridLayout_74 = QGridLayout(self.NullCraftValidateArgsJVMArgWidget)
        self.gridLayout_74.setObjectName("gridLayout_74")
        self.NullCraftValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.NullCraftValidateArgsJVMArgWidget
        )
        self.NullCraftValidateArgsJVMArgPlainTextEdit.setObjectName(
            "NullCraftValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_74.addWidget(
            self.NullCraftValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.NullCraftValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.NullCraftValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsJVMArgSubtitleLabel.setObjectName(
            "NullCraftValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_74.addWidget(
            self.NullCraftValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsJVMArgWidget, 9, 2, 1, 3)
        self.NullCraftValidateArgsCoreWidget = QWidget(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsCoreWidget.setObjectName(
            "NullCraftValidateArgsCoreWidget"
        )
        self.gridLayout_75 = QGridLayout(self.NullCraftValidateArgsCoreWidget)
        self.gridLayout_75.setObjectName("gridLayout_75")
        self.NullCraftValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.NullCraftValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.NullCraftValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "NullCraftValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_75.addWidget(
            self.NullCraftValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.NullCraftValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.NullCraftValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsCoreSubtitleLabel.setObjectName(
            "NullCraftValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_75.addWidget(
            self.NullCraftValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.NullCraftValidateArgsCoreLineEdit = LineEdit(
            self.NullCraftValidateArgsCoreWidget
        )
        self.NullCraftValidateArgsCoreLineEdit.setObjectName(
            "NullCraftValidateArgsCoreLineEdit"
        )
        self.gridLayout_75.addWidget(self.NullCraftValidateArgsCoreLineEdit, 1, 1, 1, 1)
        self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.NullCraftValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "NullCraftValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_75.addWidget(
            self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsCoreWidget, 7, 2, 1, 3)
        self.NullCraftValidateArgsMemWidget = QWidget(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.NullCraftValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.NullCraftValidateArgsMemWidget.setObjectName(
            "NullCraftValidateArgsMemWidget"
        )
        self.gridLayout_76 = QGridLayout(self.NullCraftValidateArgsMemWidget)
        self.gridLayout_76.setObjectName("gridLayout_76")
        self.NullCraftValidateArgsMinMemLineEdit = LineEdit(
            self.NullCraftValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.NullCraftValidateArgsMinMemLineEdit.setObjectName(
            "NullCraftValidateArgsMinMemLineEdit"
        )
        self.gridLayout_76.addWidget(
            self.NullCraftValidateArgsMinMemLineEdit, 1, 1, 1, 1
        )
        self.NullCraftValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.NullCraftValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsMemSubtitleLabel.setObjectName(
            "NullCraftValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_76.addWidget(
            self.NullCraftValidateArgsMemSubtitleLabel, 0, 1, 1, 1
        )
        self.NullCraftValidateArgsMaxMemLineEdit = LineEdit(
            self.NullCraftValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.NullCraftValidateArgsMaxMemLineEdit.setObjectName(
            "NullCraftValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_76.addWidget(
            self.NullCraftValidateArgsMaxMemLineEdit, 1, 3, 1, 1
        )
        self.NullCraftValidateArgsToSymbol = SubtitleLabel(
            self.NullCraftValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsToSymbol.setObjectName(
            "NullCraftValidateArgsToSymbol"
        )
        self.gridLayout_76.addWidget(self.NullCraftValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem81 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_76.addItem(spacerItem81, 1, 5, 1, 1)
        self.NullCraftValidateArgsMemUnitComboBox = ComboBox(
            self.NullCraftValidateArgsMemWidget
        )
        self.NullCraftValidateArgsMemUnitComboBox.setObjectName(
            "NullCraftValidateArgsMemUnitComboBox"
        )
        self.gridLayout_76.addWidget(
            self.NullCraftValidateArgsMemUnitComboBox, 1, 4, 1, 1
        )
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsMemWidget, 6, 2, 1, 3)
        self.NullCraftValidateArgsTitle = SubtitleLabel(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsTitle.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsTitle.setObjectName("NullCraftValidateArgsTitle")
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsTitle, 0, 3, 1, 1)
        self.NullCraftValidateArgsStatus = PixmapLabel(self.NullCraftValidateArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftValidateArgsStatus.setSizePolicy(sizePolicy)
        self.NullCraftValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.NullCraftValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.NullCraftValidateArgsStatus.setObjectName("NullCraftValidateArgsStatus")
        self.gridLayout_71.addWidget(self.NullCraftValidateArgsStatus, 0, 2, 1, 1)
        self.verticalLayout_10.addWidget(self.NullCraftValidateArgs)
        self.NullCraftSave = CardWidget(self.NullCraftScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftSave.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftSave.setSizePolicy(sizePolicy)
        self.NullCraftSave.setMinimumSize(QSize(0, 125))
        self.NullCraftSave.setMaximumSize(QSize(16777215, 125))
        self.NullCraftSave.setObjectName("NullCraftSave")
        self.gridLayout_77 = QGridLayout(self.NullCraftSave)
        self.gridLayout_77.setObjectName("gridLayout_77")
        self.NullCraftSaveTitle = SubtitleLabel(self.NullCraftSave)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftSaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftSaveTitle.setSizePolicy(sizePolicy)
        self.NullCraftSaveTitle.setObjectName("NullCraftSaveTitle")
        self.gridLayout_77.addWidget(self.NullCraftSaveTitle, 0, 1, 1, 1)
        self.NullCraftSaveServerNameLineEdit = LineEdit(self.NullCraftSave)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftSaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftSaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.NullCraftSaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.NullCraftSaveServerNameLineEdit.setObjectName(
            "NullCraftSaveServerNameLineEdit"
        )
        self.gridLayout_77.addWidget(self.NullCraftSaveServerNameLineEdit, 1, 1, 1, 1)
        spacerItem82 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_77.addItem(spacerItem82, 0, 0, 3, 1)
        self.NullCraftSaveServerPrimaryPushBtn = PrimaryPushButton(self.NullCraftSave)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.NullCraftSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.NullCraftSaveServerPrimaryPushBtn.setMaximumSize(QSize(16777215, 30))
        self.NullCraftSaveServerPrimaryPushBtn.setObjectName(
            "NullCraftSaveServerPrimaryPushBtn"
        )
        self.gridLayout_77.addWidget(self.NullCraftSaveServerPrimaryPushBtn, 2, 1, 1, 1)
        self.verticalLayout_10.addWidget(self.NullCraftSave)
        self.NullCraftScrollArea.setWidget(self.NullCraftScrollAreaWidgetContents)
        self.gridLayout_78.addWidget(self.NullCraftScrollArea, 1, 3, 1, 2)
        spacerItem83 = QSpacerItem(20, 340, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_78.addItem(spacerItem83, 1, 2, 1, 1)
        spacerItem84 = QSpacerItem(289, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_78.addItem(spacerItem84, 0, 4, 1, 1)
        self.NullCraftBackToMain = TransparentToolButton(FIF.PAGE_LEFT, self)
        self.NullCraftBackToMain.setObjectName("NullCraftBackToMain")
        self.gridLayout_78.addWidget(self.NullCraftBackToMain, 0, 2, 1, 1)
        self.NullCraftTitle = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.NullCraftTitle.sizePolicy().hasHeightForWidth()
        )
        self.NullCraftTitle.setSizePolicy(sizePolicy)
        self.NullCraftTitle.setObjectName("NullCraftTitle")
        self.gridLayout_78.addWidget(self.NullCraftTitle, 0, 3, 1, 1)
        spacerItem85 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_78.addItem(spacerItem85, 0, 1, 2, 1)
        self.NullCraftImportTitle.setText("1. 选择灵工艺开服器主程序")
        self.NullCraftImportStatusText.setText("[状态文本]")
        self.NullCraftImportArchives.setText("选择主程序")
        self.NullCraftValidateArgsJavaListPushBtn.setText("Java列表")
        self.NullCraftValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.NullCraftValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.NullCraftValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.NullCraftValidateArgsJavaSubtitleLabel.setText("Java:")
        self.NullCraftValidateArgsOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.NullCraftValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.NullCraftValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.NullCraftValidateArgsJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.NullCraftValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.NullCraftValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.NullCraftValidateArgsCoreSubtitleLabel.setText("核心：")
        self.NullCraftValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.NullCraftValidateArgsMemSubtitleLabel.setText("内存:")
        self.NullCraftValidateArgsToSymbol.setText("~")
        self.NullCraftValidateArgsTitle.setText("2. 确认参数")
        self.NullCraftSaveTitle.setText("3. 完成导入")
        self.NullCraftSaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.NullCraftSaveServerPrimaryPushBtn.setText("导入！")
        self.NullCraftTitle.setText("导入 灵工艺我的世界「轻」开服器 的服务器")

        self.NullCraftScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
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
    TreeWidget,
    ComboBox,
    LineEdit,
    PlainTextEdit,
    StrongBodyLabel,
    PushButton,
    TextEdit,
)


class ShellArchives(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("shellArchives")
        self.gridLayout_30 = QGridLayout(self)
        self.gridLayout_30.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.shellArchivesBackToMain = TransparentToolButton(FIF.PAGE_LEFT, self)
        self.shellArchivesBackToMain.setObjectName("shellArchivesBackToMain")
        self.gridLayout_30.addWidget(self.shellArchivesBackToMain, 0, 1, 1, 1)
        self.shellArchivesTitle = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesTitle.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesTitle.setSizePolicy(sizePolicy)
        self.shellArchivesTitle.setObjectName("shellArchivesTitle")
        self.gridLayout_30.addWidget(self.shellArchivesTitle, 0, 2, 1, 1)
        spacerItem36 = QSpacerItem(81, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_30.addItem(spacerItem36, 0, 3, 1, 1)
        spacerItem37 = QSpacerItem(20, 299, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_30.addItem(spacerItem37, 1, 1, 1, 1)
        self.shellArchivesScrollArea = SmoothScrollArea(self)
        self.shellArchivesScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.shellArchivesScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.shellArchivesScrollArea.setWidgetResizable(True)
        self.shellArchivesScrollArea.setAlignment(Qt.AlignCenter)
        self.shellArchivesScrollArea.setObjectName("shellArchivesScrollArea")
        self.shellArchivesScrollAreaWidgetContents = QWidget()
        self.shellArchivesScrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 1191))
        self.shellArchivesScrollAreaWidgetContents.setObjectName(
            "shellArchivesScrollAreaWidgetContents"
        )
        self.verticalLayout_3 = QVBoxLayout(self.shellArchivesScrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.shellArchivesImport = CardWidget(
            self.shellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesImport.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesImport.setSizePolicy(sizePolicy)
        self.shellArchivesImport.setMinimumSize(QSize(0, 150))
        self.shellArchivesImport.setMaximumSize(QSize(16777215, 150))
        self.shellArchivesImport.setObjectName("shellArchivesImport")
        self.gridLayout_22 = QGridLayout(self.shellArchivesImport)
        self.gridLayout_22.setObjectName("gridLayout_22")
        spacerItem38 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_22.addItem(spacerItem38, 0, 0, 3, 1)
        self.shellArchivesImportStatus = PixmapLabel(self.shellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesImportStatus.setSizePolicy(sizePolicy)
        self.shellArchivesImportStatus.setMinimumSize(QSize(30, 30))
        self.shellArchivesImportStatus.setMaximumSize(QSize(30, 30))
        self.shellArchivesImportStatus.setObjectName("shellArchivesImportStatus")
        self.gridLayout_22.addWidget(self.shellArchivesImportStatus, 0, 1, 1, 1)
        self.shellArchivesImportStatusText = BodyLabel(self.shellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesImportStatusText.setSizePolicy(sizePolicy)
        self.shellArchivesImportStatusText.setObjectName(
            "shellArchivesImportStatusText"
        )
        self.gridLayout_22.addWidget(self.shellArchivesImportStatusText, 1, 1, 1, 2)
        self.shellArchivesImportBtnWidget = QWidget(self.shellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesImportBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesImportBtnWidget.setSizePolicy(sizePolicy)
        self.shellArchivesImportBtnWidget.setObjectName("shellArchivesImportBtnWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.shellArchivesImportBtnWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.shellArchivesImportArchives = PrimaryPushButton(
            self.shellArchivesImportBtnWidget
        )
        self.shellArchivesImportArchives.setMinimumSize(QSize(110, 32))
        self.shellArchivesImportArchives.setMaximumSize(QSize(110, 32))
        self.shellArchivesImportArchives.setObjectName("shellArchivesImportArchives")
        self.horizontalLayout_3.addWidget(self.shellArchivesImportArchives)
        self.shellArchivesImportFolder = PrimaryPushButton(
            self.shellArchivesImportBtnWidget
        )
        self.shellArchivesImportFolder.setMinimumSize(QSize(110, 32))
        self.shellArchivesImportFolder.setMaximumSize(QSize(110, 32))
        self.shellArchivesImportFolder.setObjectName("shellArchivesImportFolder")
        self.horizontalLayout_3.addWidget(self.shellArchivesImportFolder)
        self.gridLayout_22.addWidget(self.shellArchivesImportBtnWidget, 2, 1, 1, 2)
        spacerItem39 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_22.addItem(spacerItem39, 2, 6, 1, 2)
        self.shellArchivesImportTitle = SubtitleLabel(self.shellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesImportTitle.setSizePolicy(sizePolicy)
        self.shellArchivesImportTitle.setObjectName("shellArchivesImportTitle")
        self.gridLayout_22.addWidget(self.shellArchivesImportTitle, 0, 2, 1, 1)
        self.verticalLayout_3.addWidget(self.shellArchivesImport)
        self.shellArchivesSelectShell = CardWidget(
            self.shellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSelectShell.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSelectShell.setSizePolicy(sizePolicy)
        self.shellArchivesSelectShell.setMinimumSize(QSize(0, 250))
        self.shellArchivesSelectShell.setObjectName("shellArchivesSelectShell")
        self.gridLayout_23 = QGridLayout(self.shellArchivesSelectShell)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.shellArchivesSelectShellStatus = PixmapLabel(self.shellArchivesSelectShell)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSelectShellStatus.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSelectShellStatus.setSizePolicy(sizePolicy)
        self.shellArchivesSelectShellStatus.setMinimumSize(QSize(30, 30))
        self.shellArchivesSelectShellStatus.setMaximumSize(QSize(30, 30))
        self.shellArchivesSelectShellStatus.setObjectName(
            "shellArchivesSelectShellStatus"
        )
        self.gridLayout_23.addWidget(self.shellArchivesSelectShellStatus, 0, 1, 1, 1)
        spacerItem40 = QSpacerItem(20, 279, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_23.addItem(spacerItem40, 0, 0, 3, 1)
        self.shellArchivesSelectShellStatusText = BodyLabel(
            self.shellArchivesSelectShell
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSelectShellStatusText.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSelectShellStatusText.setSizePolicy(sizePolicy)
        self.shellArchivesSelectShellStatusText.setObjectName(
            "shellArchivesSelectShellStatusText"
        )
        self.gridLayout_23.addWidget(
            self.shellArchivesSelectShellStatusText, 1, 1, 1, 2
        )
        self.shellArchivesSelectShellTitle = SubtitleLabel(
            self.shellArchivesSelectShell
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSelectShellTitle.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSelectShellTitle.setSizePolicy(sizePolicy)
        self.shellArchivesSelectShellTitle.setObjectName(
            "shellArchivesSelectShellTitle"
        )
        self.gridLayout_23.addWidget(self.shellArchivesSelectShellTitle, 0, 2, 1, 1)
        self.shellArchivesSelectShellTreeWidget = TreeWidget(
            self.shellArchivesSelectShell
        )
        self.shellArchivesSelectShellTreeWidget.setObjectName(
            "shellArchivesSelectShellTreeWidget"
        )
        self.shellArchivesSelectShellTreeWidget.headerItem().setText(0, "1")
        self.gridLayout_23.addWidget(
            self.shellArchivesSelectShellTreeWidget, 2, 1, 1, 2
        )
        self.verticalLayout_3.addWidget(self.shellArchivesSelectShell)
        self.shellArchivesValidateArgs = CardWidget(
            self.shellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgs.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgs.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgs.setMinimumSize(QSize(0, 630))
        self.shellArchivesValidateArgs.setMaximumSize(QSize(16777215, 630))
        self.shellArchivesValidateArgs.setObjectName("shellArchivesValidateArgs")
        self.gridLayout_24 = QGridLayout(self.shellArchivesValidateArgs)
        self.gridLayout_24.setObjectName("gridLayout_24")
        spacerItem41 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_24.addItem(spacerItem41, 0, 0, 21, 1)
        self.shellArchivesValidateArgsJavaWidget = QWidget(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsJavaWidget.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsJavaWidget.setMinimumSize(QSize(0, 120))
        self.shellArchivesValidateArgsJavaWidget.setObjectName(
            "shellArchivesValidateArgsJavaWidget"
        )
        self.gridLayout_26 = QGridLayout(self.shellArchivesValidateArgsJavaWidget)
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn.setObjectName(
            "shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.shellArchivesValidateArgsJavaSubtitleLabel = SubtitleLabel(
            self.shellArchivesValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsJavaSubtitleLabel.setObjectName(
            "shellArchivesValidateArgsJavaSubtitleLabel"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.shellArchivesValidateArgsJavaListPushBtn = PushButton(
            self.shellArchivesValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsJavaListPushBtn.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.shellArchivesValidateArgsJavaListPushBtn.setObjectName(
            "shellArchivesValidateArgsJavaListPushBtn"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsJavaListPushBtn, 3, 2, 1, 1
        )
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.setObjectName(
            "shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesValidateArgsJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.setObjectName(
            "shellArchivesValidateArgsDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.shellArchivesValidateArgsJavaTextEdit = TextEdit(
            self.shellArchivesValidateArgsJavaWidget
        )
        self.shellArchivesValidateArgsJavaTextEdit.setObjectName(
            "shellArchivesValidateArgsJavaTextEdit"
        )
        self.gridLayout_26.addWidget(
            self.shellArchivesValidateArgsJavaTextEdit, 2, 0, 2, 1
        )
        self.gridLayout_24.addWidget(
            self.shellArchivesValidateArgsJavaWidget, 5, 2, 1, 3
        )
        self.shellArchivesValidateArgsDeEncodingWidget = QWidget(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsDeEncodingWidget.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.shellArchivesValidateArgsDeEncodingWidget.setMaximumSize(
            QSize(16777215, 122)
        )
        self.shellArchivesValidateArgsDeEncodingWidget.setObjectName(
            "shellArchivesValidateArgsDeEncodingWidget"
        )
        self.gridLayout_27 = QGridLayout(self.shellArchivesValidateArgsDeEncodingWidget)
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.shellArchivesValidateArgsOutputDeEncodingComboBox = ComboBox(
            self.shellArchivesValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsOutputDeEncodingComboBox.setObjectName(
            "shellArchivesValidateArgsOutputDeEncodingComboBox"
        )
        self.gridLayout_27.addWidget(
            self.shellArchivesValidateArgsOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.shellArchivesValidateArgsInputDeEncodingComboBox = ComboBox(
            self.shellArchivesValidateArgsDeEncodingWidget
        )
        self.shellArchivesValidateArgsInputDeEncodingComboBox.setText("")
        self.shellArchivesValidateArgsInputDeEncodingComboBox.setObjectName(
            "shellArchivesValidateArgsInputDeEncodingComboBox"
        )
        self.gridLayout_27.addWidget(
            self.shellArchivesValidateArgsInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.shellArchivesValidateArgsOutputDeEncodingLabel = StrongBodyLabel(
            self.shellArchivesValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsOutputDeEncodingLabel.setObjectName(
            "shellArchivesValidateArgsOutputDeEncodingLabel"
        )
        self.gridLayout_27.addWidget(
            self.shellArchivesValidateArgsOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.shellArchivesValidateArgsDeEncodingSubtitleLabel = SubtitleLabel(
            self.shellArchivesValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsDeEncodingSubtitleLabel.setObjectName(
            "shellArchivesValidateArgsDeEncodingSubtitleLabel"
        )
        self.gridLayout_27.addWidget(
            self.shellArchivesValidateArgsDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.shellArchivesValidateArgsInputDeEncodingLabel = StrongBodyLabel(
            self.shellArchivesValidateArgsDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsInputDeEncodingLabel.setObjectName(
            "shellArchivesValidateArgsInputDeEncodingLabel"
        )
        self.gridLayout_27.addWidget(
            self.shellArchivesValidateArgsInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_24.addWidget(
            self.shellArchivesValidateArgsDeEncodingWidget, 8, 2, 1, 3
        )
        self.shellArchivesValidateArgsJVMArgWidget = QWidget(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsJVMArgWidget.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.shellArchivesValidateArgsJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.shellArchivesValidateArgsJVMArgWidget.setObjectName(
            "shellArchivesValidateArgsJVMArgWidget"
        )
        self.gridLayout_25 = QGridLayout(self.shellArchivesValidateArgsJVMArgWidget)
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.shellArchivesValidateArgsJVMArgPlainTextEdit = PlainTextEdit(
            self.shellArchivesValidateArgsJVMArgWidget
        )
        self.shellArchivesValidateArgsJVMArgPlainTextEdit.setObjectName(
            "shellArchivesValidateArgsJVMArgPlainTextEdit"
        )
        self.gridLayout_25.addWidget(
            self.shellArchivesValidateArgsJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.shellArchivesValidateArgsJVMArgSubtitleLabel = SubtitleLabel(
            self.shellArchivesValidateArgsJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsJVMArgSubtitleLabel.setObjectName(
            "shellArchivesValidateArgsJVMArgSubtitleLabel"
        )
        self.gridLayout_25.addWidget(
            self.shellArchivesValidateArgsJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_24.addWidget(
            self.shellArchivesValidateArgsJVMArgWidget, 9, 2, 1, 3
        )
        self.shellArchivesValidateArgsStatus = PixmapLabel(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsStatus.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsStatus.setMinimumSize(QSize(30, 30))
        self.shellArchivesValidateArgsStatus.setMaximumSize(QSize(30, 30))
        self.shellArchivesValidateArgsStatus.setObjectName(
            "shellArchivesValidateArgsStatus"
        )
        self.gridLayout_24.addWidget(self.shellArchivesValidateArgsStatus, 0, 2, 1, 1)
        self.shellArchivesValidateArgsMemWidget = QWidget(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsMemWidget.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsMemWidget.setMinimumSize(QSize(0, 85))
        self.shellArchivesValidateArgsMemWidget.setMaximumSize(QSize(16777215, 85))
        self.shellArchivesValidateArgsMemWidget.setObjectName(
            "shellArchivesValidateArgsMemWidget"
        )
        self.gridLayout_28 = QGridLayout(self.shellArchivesValidateArgsMemWidget)
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.shellArchivesValidateArgsMinMemLineEdit = LineEdit(
            self.shellArchivesValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsMinMemLineEdit.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.shellArchivesValidateArgsMinMemLineEdit.setObjectName(
            "shellArchivesValidateArgsMinMemLineEdit"
        )
        self.gridLayout_28.addWidget(
            self.shellArchivesValidateArgsMinMemLineEdit, 1, 1, 1, 1
        )
        self.shellArchivesValidateArgsMemSubtitleLabel = SubtitleLabel(
            self.shellArchivesValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsMemSubtitleLabel.setObjectName(
            "shellArchivesValidateArgsMemSubtitleLabel"
        )
        self.gridLayout_28.addWidget(
            self.shellArchivesValidateArgsMemSubtitleLabel, 0, 1, 1, 1
        )
        self.shellArchivesValidateArgsMaxMemLineEdit = LineEdit(
            self.shellArchivesValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.shellArchivesValidateArgsMaxMemLineEdit.setObjectName(
            "shellArchivesValidateArgsMaxMemLineEdit"
        )
        self.gridLayout_28.addWidget(
            self.shellArchivesValidateArgsMaxMemLineEdit, 1, 3, 1, 1
        )
        self.shellArchivesValidateArgsToSymbol = SubtitleLabel(
            self.shellArchivesValidateArgsMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsToSymbol.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsToSymbol.setObjectName(
            "shellArchivesValidateArgsToSymbol"
        )
        self.gridLayout_28.addWidget(self.shellArchivesValidateArgsToSymbol, 1, 2, 1, 1)
        spacerItem42 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_28.addItem(spacerItem42, 1, 5, 1, 1)
        self.shellArchivesValidateArgsMemUnitComboBox = ComboBox(
            self.shellArchivesValidateArgsMemWidget
        )
        self.shellArchivesValidateArgsMemUnitComboBox.setObjectName(
            "shellArchivesValidateArgsMemUnitComboBox"
        )
        self.gridLayout_28.addWidget(
            self.shellArchivesValidateArgsMemUnitComboBox, 1, 4, 1, 1
        )
        self.gridLayout_24.addWidget(
            self.shellArchivesValidateArgsMemWidget, 6, 2, 1, 3
        )
        self.shellArchivesValidateArgsTitle = SubtitleLabel(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsTitle.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsTitle.setObjectName(
            "shellArchivesValidateArgsTitle"
        )
        self.gridLayout_24.addWidget(self.shellArchivesValidateArgsTitle, 0, 3, 1, 1)
        self.shellArchivesValidateArgsCoreWidget = QWidget(
            self.shellArchivesValidateArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsCoreWidget.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsCoreWidget.setObjectName(
            "shellArchivesValidateArgsCoreWidget"
        )
        self.gridLayout_31 = QGridLayout(self.shellArchivesValidateArgsCoreWidget)
        self.gridLayout_31.setObjectName("gridLayout_31")
        self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn.setObjectName(
            "shellArchivesValidateArgsDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_31.addWidget(
            self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.shellArchivesValidateArgsCoreSubtitleLabel = SubtitleLabel(
            self.shellArchivesValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.shellArchivesValidateArgsCoreSubtitleLabel.setObjectName(
            "shellArchivesValidateArgsCoreSubtitleLabel"
        )
        self.gridLayout_31.addWidget(
            self.shellArchivesValidateArgsCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.shellArchivesValidateArgsCoreLineEdit = LineEdit(
            self.shellArchivesValidateArgsCoreWidget
        )
        self.shellArchivesValidateArgsCoreLineEdit.setObjectName(
            "shellArchivesValidateArgsCoreLineEdit"
        )
        self.gridLayout_31.addWidget(
            self.shellArchivesValidateArgsCoreLineEdit, 1, 1, 1, 1
        )
        self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesValidateArgsCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn.setSizePolicy(
            sizePolicy
        )
        self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn.setMinimumSize(
            QSize(90, 0)
        )
        self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn.setObjectName(
            "shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_31.addWidget(
            self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_24.addWidget(
            self.shellArchivesValidateArgsCoreWidget, 7, 2, 1, 3
        )
        self.verticalLayout_3.addWidget(self.shellArchivesValidateArgs)
        self.shellArchivesSave = CardWidget(self.shellArchivesScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSave.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSave.setSizePolicy(sizePolicy)
        self.shellArchivesSave.setMinimumSize(QSize(0, 125))
        self.shellArchivesSave.setMaximumSize(QSize(16777215, 125))
        self.shellArchivesSave.setObjectName("shellArchivesSave")
        self.gridLayout_29 = QGridLayout(self.shellArchivesSave)
        self.gridLayout_29.setObjectName("gridLayout_29")
        self.shellArchivesSaveTitle = SubtitleLabel(self.shellArchivesSave)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSaveTitle.setSizePolicy(sizePolicy)
        self.shellArchivesSaveTitle.setObjectName("shellArchivesSaveTitle")
        self.gridLayout_29.addWidget(self.shellArchivesSaveTitle, 0, 1, 1, 1)
        self.shellArchivesSaveServerNameLineEdit = LineEdit(self.shellArchivesSave)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.shellArchivesSaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.shellArchivesSaveServerNameLineEdit.setObjectName(
            "shellArchivesSaveServerNameLineEdit"
        )
        self.gridLayout_29.addWidget(
            self.shellArchivesSaveServerNameLineEdit, 1, 1, 1, 1
        )
        spacerItem43 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_29.addItem(spacerItem43, 0, 0, 3, 1)
        self.shellArchivesSaveSaveServerPrimaryPushBtn = PrimaryPushButton(
            self.shellArchivesSave
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shellArchivesSaveSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.shellArchivesSaveSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.shellArchivesSaveSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.shellArchivesSaveSaveServerPrimaryPushBtn.setMaximumSize(
            QSize(16777215, 30)
        )
        self.shellArchivesSaveSaveServerPrimaryPushBtn.setObjectName(
            "shellArchivesSaveSaveServerPrimaryPushBtn"
        )
        self.gridLayout_29.addWidget(
            self.shellArchivesSaveSaveServerPrimaryPushBtn, 2, 1, 1, 1
        )
        self.verticalLayout_3.addWidget(self.shellArchivesSave)
        self.shellArchivesScrollArea.setWidget(
            self.shellArchivesScrollAreaWidgetContents
        )
        self.gridLayout_30.addWidget(self.shellArchivesScrollArea, 1, 2, 1, 2)
        spacerItem44 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_30.addItem(spacerItem44, 0, 0, 2, 1)
        self.shellArchivesTitle.setText("导入 含开服脚本的 完整的 服务器 压缩包/文件夹")
        self.shellArchivesImportStatusText.setText("[状态文本]")
        self.shellArchivesImportArchives.setText("导入文件")
        self.shellArchivesImportFolder.setText("导入文件夹")
        self.shellArchivesImportTitle.setText("1. 导入文件/文件夹")
        self.shellArchivesSelectShellStatusText.setText("[状态文本]")
        self.shellArchivesSelectShellTitle.setText("2.选择开服脚本")
        self.shellArchivesValidateArgsAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.shellArchivesValidateArgsJavaSubtitleLabel.setText("Java:")
        self.shellArchivesValidateArgsJavaListPushBtn.setText("Java列表")
        self.shellArchivesValidateArgsManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.shellArchivesValidateArgsDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.shellArchivesValidateArgsOutputDeEncodingLabel.setText(
            "控制台输出编码（优先级高于全局设置）"
        )
        self.shellArchivesValidateArgsDeEncodingSubtitleLabel.setText("编码设置：")
        self.shellArchivesValidateArgsInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.shellArchivesValidateArgsJVMArgPlainTextEdit.setPlaceholderText(
            "可选，用一个空格分组"
        )
        self.shellArchivesValidateArgsJVMArgSubtitleLabel.setText("JVM参数：")
        self.shellArchivesValidateArgsMemSubtitleLabel.setText("内存:")
        self.shellArchivesValidateArgsToSymbol.setText("~")
        self.shellArchivesValidateArgsTitle.setText("3. 确认参数")
        self.shellArchivesValidateArgsDownloadCorePrimaryPushBtn.setText("下载核心")
        self.shellArchivesValidateArgsCoreSubtitleLabel.setText("核心：")
        self.shellArchivesValidateArgsManuallyAddCorePrimaryPushBtn.setText("重新导入")
        self.shellArchivesSaveTitle.setText("4. 完成导入")
        self.shellArchivesSaveServerNameLineEdit.setPlaceholderText("设置服务器昵称，不能包含非法字符")
        self.shellArchivesSaveSaveServerPrimaryPushBtn.setText("导入！")

from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
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
    TreeWidget,
)

from MCSL2Lib.variables import GlobalMCSL2Variables


class NoShellArchives(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("noShellArchives")
        self.gridLayout_12 = QGridLayout(self)
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_12.setObjectName("gridLayout_12")
        spacerItem26 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem26, 1, 1, 1, 1)
        self.noShellArchivesTitle = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesTitle.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesTitle.setSizePolicy(sizePolicy)
        self.noShellArchivesTitle.setObjectName("noShellArchivesTitle")
        self.gridLayout_12.addWidget(self.noShellArchivesTitle, 0, 3, 1, 1)
        spacerItem27 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem27, 0, 0, 2, 1)
        self.noShellArchivesBackToMain = TransparentToolButton(FIF.PAGE_LEFT, self)
        self.noShellArchivesBackToMain.setObjectName("noShellArchivesBackToMain")
        self.gridLayout_12.addWidget(self.noShellArchivesBackToMain, 0, 1, 1, 1)
        spacerItem28 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem28, 0, 4, 1, 1)
        self.noShellArchivesScrollArea = SmoothScrollArea(self)
        self.noShellArchivesScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.noShellArchivesScrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.noShellArchivesScrollArea.setWidgetResizable(True)
        self.noShellArchivesScrollArea.setAlignment(Qt.AlignCenter)
        self.noShellArchivesScrollArea.setObjectName("noShellArchivesScrollArea")
        self.noShellArchivesScrollAreaWidgetContents = QWidget()
        self.noShellArchivesScrollAreaWidgetContents.setGeometry(QRect(0, 0, 500, 1141))
        self.noShellArchivesScrollAreaWidgetContents.setObjectName(
            "noShellArchivesScrollAreaWidgetContents"
        )
        self.verticalLayout_2 = QVBoxLayout(
            self.noShellArchivesScrollAreaWidgetContents
        )
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.noShellArchivesImport = CardWidget(
            self.noShellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesImport.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesImport.setSizePolicy(sizePolicy)
        self.noShellArchivesImport.setMinimumSize(QSize(0, 150))
        self.noShellArchivesImport.setMaximumSize(QSize(16777215, 150))
        self.noShellArchivesImport.setObjectName("noShellArchivesImport")
        self.gridLayout_13 = QGridLayout(self.noShellArchivesImport)
        self.gridLayout_13.setObjectName("gridLayout_13")
        spacerItem29 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem29, 0, 0, 3, 1)
        self.noShellArchivesImportStatus = PixmapLabel(self.noShellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesImportStatus.setSizePolicy(sizePolicy)
        self.noShellArchivesImportStatus.setMinimumSize(QSize(30, 30))
        self.noShellArchivesImportStatus.setMaximumSize(QSize(30, 30))
        self.noShellArchivesImportStatus.setObjectName("noShellArchivesImportStatus")
        self.gridLayout_13.addWidget(self.noShellArchivesImportStatus, 0, 1, 1, 1)
        self.noShellArchivesImportStatusText = BodyLabel(self.noShellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesImportStatusText.setSizePolicy(sizePolicy)
        self.noShellArchivesImportStatusText.setObjectName(
            "noShellArchivesImportStatusText"
        )
        self.gridLayout_13.addWidget(self.noShellArchivesImportStatusText, 1, 1, 1, 2)
        self.noShellArchivesImportBtnWidget = QWidget(self.noShellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesImportBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesImportBtnWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesImportBtnWidget.setObjectName(
            "noShellArchivesImportBtnWidget"
        )
        self.horizontalLayout_2 = QHBoxLayout(self.noShellArchivesImportBtnWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.noShellArchivesImportArchives = PrimaryPushButton(
            self.noShellArchivesImportBtnWidget
        )
        self.noShellArchivesImportArchives.setMinimumSize(QSize(110, 32))
        self.noShellArchivesImportArchives.setMaximumSize(QSize(110, 32))
        self.noShellArchivesImportArchives.setObjectName(
            "noShellArchivesImportArchives"
        )
        self.horizontalLayout_2.addWidget(self.noShellArchivesImportArchives)
        self.noShellArchivesImportFolder = PrimaryPushButton(
            self.noShellArchivesImportBtnWidget
        )
        self.noShellArchivesImportFolder.setMinimumSize(QSize(110, 32))
        self.noShellArchivesImportFolder.setMaximumSize(QSize(110, 32))
        self.noShellArchivesImportFolder.setObjectName("noShellArchivesImportFolder")
        self.horizontalLayout_2.addWidget(self.noShellArchivesImportFolder)
        self.gridLayout_13.addWidget(self.noShellArchivesImportBtnWidget, 2, 1, 1, 2)
        spacerItem30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem30, 2, 6, 1, 2)
        self.noShellArchivesImportTitle = SubtitleLabel(self.noShellArchivesImport)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesImportTitle.setSizePolicy(sizePolicy)
        self.noShellArchivesImportTitle.setObjectName("noShellArchivesImportTitle")
        self.gridLayout_13.addWidget(self.noShellArchivesImportTitle, 0, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.noShellArchivesImport)
        self.noShellArchivesSelectCore = CardWidget(
            self.noShellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSelectCore.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSelectCore.setSizePolicy(sizePolicy)
        self.noShellArchivesSelectCore.setMinimumSize(QSize(0, 250))
        self.noShellArchivesSelectCore.setObjectName("noShellArchivesSelectCore")
        self.gridLayout_14 = QGridLayout(self.noShellArchivesSelectCore)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.noShellArchivesSelectCoreStatus = PixmapLabel(
            self.noShellArchivesSelectCore
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSelectCoreStatus.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSelectCoreStatus.setSizePolicy(sizePolicy)
        self.noShellArchivesSelectCoreStatus.setMinimumSize(QSize(30, 30))
        self.noShellArchivesSelectCoreStatus.setMaximumSize(QSize(30, 30))
        self.noShellArchivesSelectCoreStatus.setObjectName(
            "noShellArchivesSelectCoreStatus"
        )
        self.gridLayout_14.addWidget(self.noShellArchivesSelectCoreStatus, 0, 1, 1, 1)
        spacerItem31 = QSpacerItem(20, 279, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_14.addItem(spacerItem31, 0, 0, 3, 1)
        self.noShellArchivesSelectCoreStatusText = BodyLabel(
            self.noShellArchivesSelectCore
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSelectCoreStatusText.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSelectCoreStatusText.setSizePolicy(sizePolicy)
        self.noShellArchivesSelectCoreStatusText.setObjectName(
            "noShellArchivesSelectCoreStatusText"
        )
        self.gridLayout_14.addWidget(
            self.noShellArchivesSelectCoreStatusText, 1, 1, 1, 2
        )
        self.noShellArchivesSelectCoreTitle = SubtitleLabel(
            self.noShellArchivesSelectCore
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSelectCoreTitle.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSelectCoreTitle.setSizePolicy(sizePolicy)
        self.noShellArchivesSelectCoreTitle.setObjectName(
            "noShellArchivesSelectCoreTitle"
        )
        self.gridLayout_14.addWidget(self.noShellArchivesSelectCoreTitle, 0, 2, 1, 1)
        self.noShellArchivesSelectCoreTreeWidget = TreeWidget(
            self.noShellArchivesSelectCore
        )
        self.noShellArchivesSelectCoreTreeWidget.setObjectName(
            "noShellArchivesSelectCoreTreeWidget"
        )
        self.noShellArchivesSelectCoreTreeWidget.headerItem().setText(0, "1")
        self.gridLayout_14.addWidget(
            self.noShellArchivesSelectCoreTreeWidget, 2, 1, 1, 2
        )
        self.verticalLayout_2.addWidget(self.noShellArchivesSelectCore)
        self.noShellArchivesSetArgs = CardWidget(
            self.noShellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetArgs.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetArgs.setSizePolicy(sizePolicy)
        self.noShellArchivesSetArgs.setMinimumSize(QSize(0, 580))
        self.noShellArchivesSetArgs.setMaximumSize(QSize(16777215, 580))
        self.noShellArchivesSetArgs.setObjectName("noShellArchivesSetArgs")
        self.gridLayout_19 = QGridLayout(self.noShellArchivesSetArgs)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.noShellArchivesSetJVMArgWidget = QWidget(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetJVMArgWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesSetJVMArgWidget.setMinimumSize(QSize(0, 171))
        self.noShellArchivesSetJVMArgWidget.setMaximumSize(QSize(16777215, 171))
        self.noShellArchivesSetJVMArgWidget.setObjectName(
            "noShellArchivesSetJVMArgWidget"
        )
        self.gridLayout_18 = QGridLayout(self.noShellArchivesSetJVMArgWidget)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.noShellArchivesJVMArgPlainTextEdit = PlainTextEdit(
            self.noShellArchivesSetJVMArgWidget
        )
        self.noShellArchivesJVMArgPlainTextEdit.setObjectName(
            "noShellArchivesJVMArgPlainTextEdit"
        )
        self.gridLayout_18.addWidget(
            self.noShellArchivesJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.noShellArchivesJVMArgSubtitleLabel = SubtitleLabel(
            self.noShellArchivesSetJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesJVMArgSubtitleLabel.setObjectName(
            "noShellArchivesJVMArgSubtitleLabel"
        )
        self.gridLayout_18.addWidget(
            self.noShellArchivesJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_19.addWidget(self.noShellArchivesSetJVMArgWidget, 7, 2, 1, 3)
        self.noShellArchivesSetArgsTitle = SubtitleLabel(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetArgsTitle.setSizePolicy(sizePolicy)
        self.noShellArchivesSetArgsTitle.setObjectName("noShellArchivesSetArgsTitle")
        self.gridLayout_19.addWidget(self.noShellArchivesSetArgsTitle, 0, 3, 1, 1)
        spacerItem32 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_19.addItem(spacerItem32, 0, 0, 19, 1)
        self.noShellArchivesSetArgsStatus = PixmapLabel(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetArgsStatus.setSizePolicy(sizePolicy)
        self.noShellArchivesSetArgsStatus.setMinimumSize(QSize(30, 30))
        self.noShellArchivesSetArgsStatus.setMaximumSize(QSize(30, 30))
        self.noShellArchivesSetArgsStatus.setObjectName("noShellArchivesSetArgsStatus")
        self.gridLayout_19.addWidget(self.noShellArchivesSetArgsStatus, 0, 2, 1, 1)
        self.noShellArchivesSetJavaWidget = QWidget(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetJavaWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesSetJavaWidget.setMinimumSize(QSize(0, 100))
        self.noShellArchivesSetJavaWidget.setMaximumSize(QSize(16777215, 100))
        self.noShellArchivesSetJavaWidget.setObjectName("noShellArchivesSetJavaWidget")
        self.gridLayout_17 = QGridLayout(self.noShellArchivesSetJavaWidget)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.noShellArchivesSetJavaBtnWidget = QWidget(
            self.noShellArchivesSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetJavaBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetJavaBtnWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesSetJavaBtnWidget.setObjectName(
            "noShellArchivesSetJavaBtnWidget"
        )
        self.horizontalLayout_8 = QHBoxLayout(self.noShellArchivesSetJavaBtnWidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.noShellArchivesDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.noShellArchivesSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noShellArchivesDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noShellArchivesDownloadJavaPrimaryPushBtn.setObjectName(
            "noShellArchivesDownloadJavaPrimaryPushBtn"
        )
        self.horizontalLayout_8.addWidget(
            self.noShellArchivesDownloadJavaPrimaryPushBtn
        )
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.noShellArchivesSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn.setObjectName(
            "noShellArchivesManuallyAddJavaPrimaryPushBtn"
        )
        self.horizontalLayout_8.addWidget(
            self.noShellArchivesManuallyAddJavaPrimaryPushBtn
        )
        self.noShellArchivesAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.noShellArchivesSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noShellArchivesAutoDetectJavaPrimaryPushBtn.setObjectName(
            "noShellArchivesAutoDetectJavaPrimaryPushBtn"
        )
        self.horizontalLayout_8.addWidget(
            self.noShellArchivesAutoDetectJavaPrimaryPushBtn
        )
        self.noShellArchivesJavaListPushBtn = PushButton(
            self.noShellArchivesSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesJavaListPushBtn.setSizePolicy(sizePolicy)
        self.noShellArchivesJavaListPushBtn.setMinimumSize(QSize(90, 0))
        self.noShellArchivesJavaListPushBtn.setObjectName(
            "noShellArchivesJavaListPushBtn"
        )
        self.horizontalLayout_8.addWidget(self.noShellArchivesJavaListPushBtn)
        spacerItem33 = QSpacerItem(127, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem33)
        self.gridLayout_17.addWidget(self.noShellArchivesSetJavaBtnWidget, 1, 0, 1, 2)
        self.noShellArchivesJavaInfoLabel = SubtitleLabel(
            self.noShellArchivesSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesJavaInfoLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesJavaInfoLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesJavaInfoLabel.setObjectName("noShellArchivesJavaInfoLabel")
        self.gridLayout_17.addWidget(self.noShellArchivesJavaInfoLabel, 0, 1, 1, 1)
        self.noShellArchivesJavaSubtitleLabel = SubtitleLabel(
            self.noShellArchivesSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesJavaSubtitleLabel.setObjectName(
            "noShellArchivesJavaSubtitleLabel"
        )
        self.gridLayout_17.addWidget(self.noShellArchivesJavaSubtitleLabel, 0, 0, 1, 1)
        self.gridLayout_19.addWidget(self.noShellArchivesSetJavaWidget, 4, 2, 1, 3)
        self.noShellArchivesSetDeEncodingWidget = QWidget(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetDeEncodingWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesSetDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.noShellArchivesSetDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.noShellArchivesSetDeEncodingWidget.setObjectName(
            "noShellArchivesSetDeEncodingWidget"
        )
        self.gridLayout_16 = QGridLayout(self.noShellArchivesSetDeEncodingWidget)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.noShellArchivesOutputDeEncodingComboBox = ComboBox(
            self.noShellArchivesSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.noShellArchivesOutputDeEncodingComboBox.setObjectName(
            "noShellArchivesOutputDeEncodingComboBox"
        )
        self.gridLayout_16.addWidget(
            self.noShellArchivesOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.noShellArchivesInputDeEncodingComboBox = ComboBox(
            self.noShellArchivesSetDeEncodingWidget
        )
        self.noShellArchivesInputDeEncodingComboBox.setText("")
        self.noShellArchivesInputDeEncodingComboBox.setObjectName(
            "noShellArchivesInputDeEncodingComboBox"
        )
        self.gridLayout_16.addWidget(
            self.noShellArchivesInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.noShellArchivesOutputDeEncodingLabel = StrongBodyLabel(
            self.noShellArchivesSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesOutputDeEncodingLabel.setObjectName(
            "noShellArchivesOutputDeEncodingLabel"
        )
        self.gridLayout_16.addWidget(
            self.noShellArchivesOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.noShellArchivesDeEncodingSubtitleLabel = SubtitleLabel(
            self.noShellArchivesSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesDeEncodingSubtitleLabel.setObjectName(
            "noShellArchivesDeEncodingSubtitleLabel"
        )
        self.gridLayout_16.addWidget(
            self.noShellArchivesDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.noShellArchivesInputDeEncodingLabel = StrongBodyLabel(
            self.noShellArchivesSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesInputDeEncodingLabel.setObjectName(
            "noShellArchivesInputDeEncodingLabel"
        )
        self.gridLayout_16.addWidget(
            self.noShellArchivesInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_19.addWidget(
            self.noShellArchivesSetDeEncodingWidget, 6, 2, 1, 3
        )
        self.noShellArchivesSetMemWidget = QWidget(self.noShellArchivesSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSetMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSetMemWidget.setSizePolicy(sizePolicy)
        self.noShellArchivesSetMemWidget.setMinimumSize(QSize(0, 85))
        self.noShellArchivesSetMemWidget.setMaximumSize(QSize(16777215, 85))
        self.noShellArchivesSetMemWidget.setObjectName("noShellArchivesSetMemWidget")
        self.gridLayout_15 = QGridLayout(self.noShellArchivesSetMemWidget)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.noShellArchivesMinMemLineEdit = LineEdit(self.noShellArchivesSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesMinMemLineEdit.setSizePolicy(sizePolicy)
        self.noShellArchivesMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noShellArchivesMinMemLineEdit.setObjectName(
            "noShellArchivesMinMemLineEdit"
        )
        self.gridLayout_15.addWidget(self.noShellArchivesMinMemLineEdit, 1, 1, 1, 1)
        self.noShellArchivesMemSubtitleLabel = SubtitleLabel(
            self.noShellArchivesSetMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.noShellArchivesMemSubtitleLabel.setObjectName(
            "noShellArchivesMemSubtitleLabel"
        )
        self.gridLayout_15.addWidget(self.noShellArchivesMemSubtitleLabel, 0, 1, 1, 1)
        self.noShellArchivesMaxMemLineEdit = LineEdit(self.noShellArchivesSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.noShellArchivesMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noShellArchivesMaxMemLineEdit.setObjectName(
            "noShellArchivesMaxMemLineEdit"
        )
        self.gridLayout_15.addWidget(self.noShellArchivesMaxMemLineEdit, 1, 3, 1, 1)
        self.noShellArchivesToSymbol = SubtitleLabel(self.noShellArchivesSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesToSymbol.setSizePolicy(sizePolicy)
        self.noShellArchivesToSymbol.setObjectName("noShellArchivesToSymbol")
        self.gridLayout_15.addWidget(self.noShellArchivesToSymbol, 1, 2, 1, 1)
        spacerItem34 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_15.addItem(spacerItem34, 1, 5, 1, 1)
        self.noShellArchivesMemUnitComboBox = ComboBox(self.noShellArchivesSetMemWidget)
        self.noShellArchivesMemUnitComboBox.setObjectName(
            "noShellArchivesMemUnitComboBox"
        )
        self.gridLayout_15.addWidget(self.noShellArchivesMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_19.addWidget(self.noShellArchivesSetMemWidget, 5, 2, 1, 3)
        self.verticalLayout_2.addWidget(self.noShellArchivesSetArgs)
        self.noShellArchivesSave = CardWidget(
            self.noShellArchivesScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSave.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSave.setSizePolicy(sizePolicy)
        self.noShellArchivesSave.setMinimumSize(QSize(0, 125))
        self.noShellArchivesSave.setMaximumSize(QSize(16777215, 125))
        self.noShellArchivesSave.setObjectName("noShellArchivesSave")
        self.gridLayout_20 = QGridLayout(self.noShellArchivesSave)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.noShellArchivesSaveTitle = SubtitleLabel(self.noShellArchivesSave)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSaveTitle.setSizePolicy(sizePolicy)
        self.noShellArchivesSaveTitle.setObjectName("noShellArchivesSaveTitle")
        self.gridLayout_20.addWidget(self.noShellArchivesSaveTitle, 0, 1, 1, 1)
        self.noShellArchivesSaveServerNameLineEdit = LineEdit(self.noShellArchivesSave)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSaveServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSaveServerNameLineEdit.setSizePolicy(sizePolicy)
        self.noShellArchivesSaveServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.noShellArchivesSaveServerNameLineEdit.setObjectName(
            "noShellArchivesSaveServerNameLineEdit"
        )
        self.gridLayout_20.addWidget(
            self.noShellArchivesSaveServerNameLineEdit, 1, 1, 1, 1
        )
        spacerItem35 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_20.addItem(spacerItem35, 0, 0, 3, 1)
        self.noShellArchivesSaveSaveServerPrimaryPushBtn = PrimaryPushButton(
            self.noShellArchivesSave
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noShellArchivesSaveSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noShellArchivesSaveSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noShellArchivesSaveSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.noShellArchivesSaveSaveServerPrimaryPushBtn.setMaximumSize(
            QSize(16777215, 30)
        )
        self.noShellArchivesSaveSaveServerPrimaryPushBtn.setObjectName(
            "noShellArchivesSaveSaveServerPrimaryPushBtn"
        )
        self.gridLayout_20.addWidget(
            self.noShellArchivesSaveSaveServerPrimaryPushBtn, 2, 1, 1, 1
        )
        self.verticalLayout_2.addWidget(self.noShellArchivesSave)
        self.noShellArchivesScrollArea.setWidget(
            self.noShellArchivesScrollAreaWidgetContents
        )
        self.gridLayout_12.addWidget(self.noShellArchivesScrollArea, 1, 3, 1, 2)
        self.noShellArchivesTitle.setText("导入 不含开服脚本的 完整的 服务器 压缩包/文件夹")
        self.noShellArchivesImportStatusText.setText("[状态文本]")
        self.noShellArchivesImportArchives.setText("导入文件")
        self.noShellArchivesImportFolder.setText("导入文件夹")
        self.noShellArchivesImportTitle.setText("1. 导入文件/文件夹")
        self.noShellArchivesSelectCoreStatusText.setText("[状态文本]")
        self.noShellArchivesSelectCoreTitle.setText("2.选择核心")
        self.noShellArchivesJVMArgPlainTextEdit.setPlaceholderText("可选，用一个空格分组")
        self.noShellArchivesJVMArgSubtitleLabel.setText("JVM参数：")
        self.noShellArchivesSetArgsTitle.setText("3. 设置参数")
        self.noShellArchivesDownloadJavaPrimaryPushBtn.setText("下载Java")
        self.noShellArchivesManuallyAddJavaPrimaryPushBtn.setText("手动导入")
        self.noShellArchivesAutoDetectJavaPrimaryPushBtn.setText("自动查找Java")
        self.noShellArchivesJavaListPushBtn.setText("Java列表")
        self.noShellArchivesJavaInfoLabel.setText("[选择的Java的信息]")
        self.noShellArchivesJavaSubtitleLabel.setText("Java:")
        self.noShellArchivesOutputDeEncodingLabel.setText("控制台输出编码（优先级高于全局设置）")
        self.noShellArchivesDeEncodingSubtitleLabel.setText("编码设置：")
        self.noShellArchivesInputDeEncodingLabel.setText("指令输入编码（优先级高于全局设置）")
        self.noShellArchivesMemSubtitleLabel.setText("内存:")
        self.noShellArchivesToSymbol.setText("~")
        self.noShellArchivesSaveTitle.setText("4. 完成导入")
        self.noShellArchivesSaveServerNameLineEdit.setPlaceholderText(
            "设置服务器昵称，不能包含非法字符"
        )
        self.noShellArchivesSaveSaveServerPrimaryPushBtn.setText("导入！")

        self.noShellArchivesScrollArea.viewport().setStyleSheet(
            GlobalMCSL2Variables.scrollAreaViewportQss
        )

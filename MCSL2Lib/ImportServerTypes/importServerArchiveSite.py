from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
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
    ComboBox,
    LineEdit,
    PlainTextEdit,
    StrongBodyLabel,
    PushButton,
    TextEdit,
)
from MCSL2Lib.Widgets.myScrollArea import MySmoothScrollArea

from MCSL2Lib.variables import GlobalMCSL2Variables


class ServerArchiveSite(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("serverArchiveSite")
        self.gridLayout_41 = QGridLayout(self)
        self.gridLayout_41.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_41.setObjectName("gridLayout_41")
        spacerItem45 = QSpacerItem(256, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_41.addItem(spacerItem45, 0, 3, 1, 1)
        self.serverArchiveSiteScrollArea = MySmoothScrollArea(self)
        self.serverArchiveSiteScrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.serverArchiveSiteScrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.serverArchiveSiteScrollArea.setWidgetResizable(True)
        self.serverArchiveSiteScrollArea.setAlignment(Qt.AlignCenter)
        self.serverArchiveSiteScrollArea.setObjectName("serverArchiveSiteScrollArea")
        self.serverArchiveSiteScrollAreaWidgetContents = QWidget()
        self.serverArchiveSiteScrollAreaWidgetContents.setGeometry(
            QRect(0, 0, 450, 935)
        )
        self.serverArchiveSiteScrollAreaWidgetContents.setObjectName(
            "serverArchiveSiteScrollAreaWidgetContents"
        )
        self.verticalLayout_6 = QVBoxLayout(
            self.serverArchiveSiteScrollAreaWidgetContents
        )
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.serverArchiveSiteImport = CardWidget(
            self.serverArchiveSiteScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteImport.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteImport.setSizePolicy(sizePolicy)
        self.serverArchiveSiteImport.setMinimumSize(QSize(0, 150))
        self.serverArchiveSiteImport.setMaximumSize(QSize(16777215, 150))
        self.serverArchiveSiteImport.setObjectName("serverArchiveSiteImport")
        self.gridLayout_32 = QGridLayout(self.serverArchiveSiteImport)
        self.gridLayout_32.setObjectName("gridLayout_32")
        spacerItem46 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_32.addItem(spacerItem46, 0, 0, 3, 1)
        self.serverArchiveSiteImportStatus = PixmapLabel(self.serverArchiveSiteImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteImportStatus.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteImportStatus.setSizePolicy(sizePolicy)
        self.serverArchiveSiteImportStatus.setMinimumSize(QSize(30, 30))
        self.serverArchiveSiteImportStatus.setMaximumSize(QSize(30, 30))
        self.serverArchiveSiteImportStatus.setObjectName(
            "serverArchiveSiteImportStatus"
        )
        self.gridLayout_32.addWidget(self.serverArchiveSiteImportStatus, 0, 1, 1, 1)
        self.serverArchiveSiteImportStatusText = BodyLabel(self.serverArchiveSiteImport)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteImportStatusText.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteImportStatusText.setSizePolicy(sizePolicy)
        self.serverArchiveSiteImportStatusText.setObjectName(
            "serverArchiveSiteImportStatusText"
        )
        self.gridLayout_32.addWidget(self.serverArchiveSiteImportStatusText, 1, 1, 1, 2)
        self.serverArchiveSiteImportBtnWidget = QWidget(self.serverArchiveSiteImport)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteImportBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteImportBtnWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteImportBtnWidget.setObjectName(
            "serverArchiveSiteImportBtnWidget"
        )
        self.horizontalLayout_9 = QHBoxLayout(self.serverArchiveSiteImportBtnWidget)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.serverArchiveSiteImportArchives = PrimaryPushButton(
            self.serverArchiveSiteImportBtnWidget
        )
        self.serverArchiveSiteImportArchives.setMinimumSize(QSize(110, 32))
        self.serverArchiveSiteImportArchives.setMaximumSize(QSize(110, 32))
        self.serverArchiveSiteImportArchives.setObjectName(
            "serverArchiveSiteImportArchives"
        )
        self.horizontalLayout_9.addWidget(self.serverArchiveSiteImportArchives)
        self.serverArchiveSiteImportFolder = PrimaryPushButton(
            self.serverArchiveSiteImportBtnWidget
        )
        self.serverArchiveSiteImportFolder.setMinimumSize(QSize(110, 32))
        self.serverArchiveSiteImportFolder.setMaximumSize(QSize(110, 32))
        self.serverArchiveSiteImportFolder.setObjectName(
            "serverArchiveSiteImportFolder"
        )
        self.horizontalLayout_9.addWidget(self.serverArchiveSiteImportFolder)
        self.gridLayout_32.addWidget(self.serverArchiveSiteImportBtnWidget, 2, 1, 1, 2)
        spacerItem47 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_32.addItem(spacerItem47, 2, 6, 1, 2)
        self.serverArchiveSiteImportTitle = SubtitleLabel(self.serverArchiveSiteImport)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteImportTitle.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteImportTitle.setSizePolicy(sizePolicy)
        self.serverArchiveSiteImportTitle.setObjectName("serverArchiveSiteImportTitle")
        self.gridLayout_32.addWidget(self.serverArchiveSiteImportTitle, 0, 2, 1, 1)
        self.verticalLayout_6.addWidget(self.serverArchiveSiteImport)
        self.serverArchiveSiteSetArgs = CardWidget(
            self.serverArchiveSiteScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetArgs.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetArgs.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetArgs.setMinimumSize(QSize(0, 630))
        self.serverArchiveSiteSetArgs.setMaximumSize(QSize(16777215, 630))
        self.serverArchiveSiteSetArgs.setObjectName("serverArchiveSiteSetArgs")
        self.gridLayout_34 = QGridLayout(self.serverArchiveSiteSetArgs)
        self.gridLayout_34.setObjectName("gridLayout_34")
        spacerItem48 = QSpacerItem(20, 102, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_34.addItem(spacerItem48, 0, 0, 21, 1)
        self.serverArchiveSiteSetJavaWidget = QWidget(self.serverArchiveSiteSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetJavaWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetJavaWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.serverArchiveSiteSetJavaWidget.setObjectName(
            "serverArchiveSiteSetJavaWidget"
        )
        self.gridLayout_35 = QGridLayout(self.serverArchiveSiteSetJavaWidget)
        self.gridLayout_35.setObjectName("gridLayout_35")
        self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn.setObjectName(
            "serverArchiveSiteAutoDetectJavaPrimaryPushBtn"
        )
        self.gridLayout_35.addWidget(
            self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn, 2, 2, 1, 1
        )
        self.serverArchiveSiteJavaSubtitleLabel = SubtitleLabel(
            self.serverArchiveSiteSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteJavaSubtitleLabel.setObjectName(
            "serverArchiveSiteJavaSubtitleLabel"
        )
        self.gridLayout_35.addWidget(
            self.serverArchiveSiteJavaSubtitleLabel, 0, 0, 1, 1
        )
        self.serverArchiveSiteJavaListPushBtn = PushButton(
            self.serverArchiveSiteSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteJavaListPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteJavaListPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteJavaListPushBtn.setMinimumSize(QSize(108, 31))
        self.serverArchiveSiteJavaListPushBtn.setObjectName(
            "serverArchiveSiteJavaListPushBtn"
        )
        self.gridLayout_35.addWidget(self.serverArchiveSiteJavaListPushBtn, 3, 2, 1, 1)
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.setObjectName(
            "serverArchiveSiteManuallyAddJavaPrimaryPushBtn"
        )
        self.gridLayout_35.addWidget(
            self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn, 2, 1, 1, 1
        )
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSetJavaWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn.setObjectName(
            "serverArchiveSiteDownloadJavaPrimaryPushBtn"
        )
        self.gridLayout_35.addWidget(
            self.serverArchiveSiteDownloadJavaPrimaryPushBtn, 3, 1, 1, 1
        )
        self.serverArchiveSiteJavaTextEdit = TextEdit(
            self.serverArchiveSiteSetJavaWidget
        )
        self.serverArchiveSiteJavaTextEdit.setObjectName(
            "serverArchiveSiteJavaTextEdit"
        )
        self.gridLayout_35.addWidget(self.serverArchiveSiteJavaTextEdit, 2, 0, 2, 1)
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetJavaWidget, 5, 2, 1, 3)
        self.serverArchiveSiteSetDeEncodingWidget = QWidget(
            self.serverArchiveSiteSetArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetDeEncodingWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetDeEncodingWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetDeEncodingWidget.setMinimumSize(QSize(0, 122))
        self.serverArchiveSiteSetDeEncodingWidget.setMaximumSize(QSize(16777215, 122))
        self.serverArchiveSiteSetDeEncodingWidget.setObjectName(
            "serverArchiveSiteSetDeEncodingWidget"
        )
        self.gridLayout_36 = QGridLayout(self.serverArchiveSiteSetDeEncodingWidget)
        self.gridLayout_36.setObjectName("gridLayout_36")
        self.serverArchiveSiteOutputDeEncodingComboBox = ComboBox(
            self.serverArchiveSiteSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.serverArchiveSiteOutputDeEncodingComboBox.setObjectName(
            "serverArchiveSiteOutputDeEncodingComboBox"
        )
        self.gridLayout_36.addWidget(
            self.serverArchiveSiteOutputDeEncodingComboBox, 2, 1, 1, 1
        )
        self.serverArchiveSiteInputDeEncodingComboBox = ComboBox(
            self.serverArchiveSiteSetDeEncodingWidget
        )
        self.serverArchiveSiteInputDeEncodingComboBox.setText("")
        self.serverArchiveSiteInputDeEncodingComboBox.setObjectName(
            "serverArchiveSiteInputDeEncodingComboBox"
        )
        self.gridLayout_36.addWidget(
            self.serverArchiveSiteInputDeEncodingComboBox, 3, 1, 1, 1
        )
        self.serverArchiveSiteOutputDeEncodingLabel = StrongBodyLabel(
            self.serverArchiveSiteSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteOutputDeEncodingLabel.setObjectName(
            "serverArchiveSiteOutputDeEncodingLabel"
        )
        self.gridLayout_36.addWidget(
            self.serverArchiveSiteOutputDeEncodingLabel, 2, 0, 1, 1
        )
        self.serverArchiveSiteDeEncodingSubtitleLabel = SubtitleLabel(
            self.serverArchiveSiteSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteDeEncodingSubtitleLabel.setObjectName(
            "serverArchiveSiteDeEncodingSubtitleLabel"
        )
        self.gridLayout_36.addWidget(
            self.serverArchiveSiteDeEncodingSubtitleLabel, 0, 0, 1, 1
        )
        self.serverArchiveSiteInputDeEncodingLabel = StrongBodyLabel(
            self.serverArchiveSiteSetDeEncodingWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteInputDeEncodingLabel.setObjectName(
            "serverArchiveSiteInputDeEncodingLabel"
        )
        self.gridLayout_36.addWidget(
            self.serverArchiveSiteInputDeEncodingLabel, 3, 0, 1, 1
        )
        self.gridLayout_34.addWidget(
            self.serverArchiveSiteSetDeEncodingWidget, 8, 2, 1, 3
        )
        self.serverArchiveSiteSetJVMArgWidget = QWidget(self.serverArchiveSiteSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetJVMArgWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetJVMArgWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetJVMArgWidget.setMinimumSize(QSize(0, 140))
        self.serverArchiveSiteSetJVMArgWidget.setMaximumSize(QSize(16777215, 140))
        self.serverArchiveSiteSetJVMArgWidget.setObjectName(
            "serverArchiveSiteSetJVMArgWidget"
        )
        self.gridLayout_37 = QGridLayout(self.serverArchiveSiteSetJVMArgWidget)
        self.gridLayout_37.setObjectName("gridLayout_37")
        self.serverArchiveSiteJVMArgPlainTextEdit = PlainTextEdit(
            self.serverArchiveSiteSetJVMArgWidget
        )
        self.serverArchiveSiteJVMArgPlainTextEdit.setObjectName(
            "serverArchiveSiteJVMArgPlainTextEdit"
        )
        self.gridLayout_37.addWidget(
            self.serverArchiveSiteJVMArgPlainTextEdit, 1, 0, 1, 1
        )
        self.serverArchiveSiteJVMArgSubtitleLabel = SubtitleLabel(
            self.serverArchiveSiteSetJVMArgWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteJVMArgSubtitleLabel.setObjectName(
            "serverArchiveSiteJVMArgSubtitleLabel"
        )
        self.gridLayout_37.addWidget(
            self.serverArchiveSiteJVMArgSubtitleLabel, 0, 0, 1, 1
        )
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetJVMArgWidget, 9, 2, 1, 3)
        self.serverArchiveSiteSetArgsStatus = PixmapLabel(self.serverArchiveSiteSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetArgsStatus.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetArgsStatus.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetArgsStatus.setMinimumSize(QSize(30, 30))
        self.serverArchiveSiteSetArgsStatus.setMaximumSize(QSize(30, 30))
        self.serverArchiveSiteSetArgsStatus.setObjectName(
            "serverArchiveSiteSetArgsStatus"
        )
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetArgsStatus, 0, 2, 1, 1)
        self.serverArchiveSiteSetMemWidget = QWidget(self.serverArchiveSiteSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetMemWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetMemWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetMemWidget.setMinimumSize(QSize(0, 85))
        self.serverArchiveSiteSetMemWidget.setMaximumSize(QSize(16777215, 85))
        self.serverArchiveSiteSetMemWidget.setObjectName(
            "serverArchiveSiteSetMemWidget"
        )
        self.gridLayout_38 = QGridLayout(self.serverArchiveSiteSetMemWidget)
        self.gridLayout_38.setObjectName("gridLayout_38")
        self.serverArchiveSiteMinMemLineEdit = LineEdit(
            self.serverArchiveSiteSetMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteMinMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteMinMemLineEdit.setSizePolicy(sizePolicy)
        self.serverArchiveSiteMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.serverArchiveSiteMinMemLineEdit.setObjectName(
            "serverArchiveSiteMinMemLineEdit"
        )
        self.gridLayout_38.addWidget(self.serverArchiveSiteMinMemLineEdit, 1, 1, 1, 1)
        self.serverArchiveSiteMemSubtitleLabel = SubtitleLabel(
            self.serverArchiveSiteSetMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteMemSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteMemSubtitleLabel.setObjectName(
            "serverArchiveSiteMemSubtitleLabel"
        )
        self.gridLayout_38.addWidget(self.serverArchiveSiteMemSubtitleLabel, 0, 1, 1, 1)
        self.serverArchiveSiteMaxMemLineEdit = LineEdit(
            self.serverArchiveSiteSetMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteMaxMemLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.serverArchiveSiteMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.serverArchiveSiteMaxMemLineEdit.setObjectName(
            "serverArchiveSiteMaxMemLineEdit"
        )
        self.gridLayout_38.addWidget(self.serverArchiveSiteMaxMemLineEdit, 1, 3, 1, 1)
        self.serverArchiveSiteToSymbol = SubtitleLabel(
            self.serverArchiveSiteSetMemWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteToSymbol.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteToSymbol.setSizePolicy(sizePolicy)
        self.serverArchiveSiteToSymbol.setObjectName("serverArchiveSiteToSymbol")
        self.gridLayout_38.addWidget(self.serverArchiveSiteToSymbol, 1, 2, 1, 1)
        spacerItem49 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_38.addItem(spacerItem49, 1, 5, 1, 1)
        self.serverArchiveSiteMemUnitComboBox = ComboBox(
            self.serverArchiveSiteSetMemWidget
        )
        self.serverArchiveSiteMemUnitComboBox.setObjectName(
            "serverArchiveSiteMemUnitComboBox"
        )
        self.gridLayout_38.addWidget(self.serverArchiveSiteMemUnitComboBox, 1, 4, 1, 1)
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetMemWidget, 6, 2, 1, 3)
        self.serverArchiveSiteSetArgsTitle = SubtitleLabel(
            self.serverArchiveSiteSetArgs
        )
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetArgsTitle.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetArgsTitle.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetArgsTitle.setObjectName(
            "serverArchiveSiteSetArgsTitle"
        )
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetArgsTitle, 0, 3, 1, 1)
        self.serverArchiveSiteSetCoreWidget = QWidget(self.serverArchiveSiteSetArgs)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSetCoreWidget.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSetCoreWidget.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSetCoreWidget.setObjectName(
            "serverArchiveSiteSetCoreWidget"
        )
        self.gridLayout_39 = QGridLayout(self.serverArchiveSiteSetCoreWidget)
        self.gridLayout_39.setObjectName("gridLayout_39")
        self.serverArchiveSiteDownloadCorePrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.serverArchiveSiteDownloadCorePrimaryPushBtn.setObjectName(
            "serverArchiveSiteDownloadCorePrimaryPushBtn"
        )
        self.gridLayout_39.addWidget(
            self.serverArchiveSiteDownloadCorePrimaryPushBtn, 1, 3, 1, 1
        )
        self.serverArchiveSiteCoreSubtitleLabel = SubtitleLabel(
            self.serverArchiveSiteSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.serverArchiveSiteCoreSubtitleLabel.setObjectName(
            "serverArchiveSiteCoreSubtitleLabel"
        )
        self.gridLayout_39.addWidget(
            self.serverArchiveSiteCoreSubtitleLabel, 0, 1, 1, 1
        )
        self.serverArchiveSiteCoreLineEdit = LineEdit(
            self.serverArchiveSiteSetCoreWidget
        )
        self.serverArchiveSiteCoreLineEdit.setObjectName(
            "serverArchiveSiteCoreLineEdit"
        )
        self.gridLayout_39.addWidget(self.serverArchiveSiteCoreLineEdit, 1, 1, 1, 1)
        self.serverArchiveSiteManuallyAddCorePrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSetCoreWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.serverArchiveSiteManuallyAddCorePrimaryPushBtn.setObjectName(
            "serverArchiveSiteManuallyAddCorePrimaryPushBtn"
        )
        self.gridLayout_39.addWidget(
            self.serverArchiveSiteManuallyAddCorePrimaryPushBtn, 1, 2, 1, 1
        )
        self.gridLayout_34.addWidget(self.serverArchiveSiteSetCoreWidget, 7, 2, 1, 3)
        self.verticalLayout_6.addWidget(self.serverArchiveSiteSetArgs)
        self.serverArchiveSiteSave = CardWidget(
            self.serverArchiveSiteScrollAreaWidgetContents
        )
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSave.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSave.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSave.setMinimumSize(QSize(0, 125))
        self.serverArchiveSiteSave.setMaximumSize(QSize(16777215, 125))
        self.serverArchiveSiteSave.setObjectName("serverArchiveSiteSave")
        self.gridLayout_40 = QGridLayout(self.serverArchiveSiteSave)
        self.gridLayout_40.setObjectName("gridLayout_40")
        self.serverArchiveSiteSaveTitle = SubtitleLabel(self.serverArchiveSiteSave)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSaveTitle.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSaveTitle.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSaveTitle.setObjectName("serverArchiveSiteSaveTitle")
        self.gridLayout_40.addWidget(self.serverArchiveSiteSaveTitle, 0, 1, 1, 1)
        self.serverArchiveSiteServerNameLineEdit = LineEdit(self.serverArchiveSiteSave)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteServerNameLineEdit.setSizePolicy(sizePolicy)
        self.serverArchiveSiteServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.serverArchiveSiteServerNameLineEdit.setObjectName(
            "serverArchiveSiteServerNameLineEdit"
        )
        self.gridLayout_40.addWidget(
            self.serverArchiveSiteServerNameLineEdit, 1, 1, 1, 1
        )
        spacerItem50 = QSpacerItem(20, 79, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_40.addItem(spacerItem50, 0, 0, 3, 1)
        self.serverArchiveSiteSaveServerPrimaryPushBtn = PrimaryPushButton(
            self.serverArchiveSiteSave
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.serverArchiveSiteSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 30))
        self.serverArchiveSiteSaveServerPrimaryPushBtn.setMaximumSize(
            QSize(16777215, 30)
        )
        self.serverArchiveSiteSaveServerPrimaryPushBtn.setObjectName(
            "serverArchiveSiteSaveServerPrimaryPushBtn"
        )
        self.gridLayout_40.addWidget(
            self.serverArchiveSiteSaveServerPrimaryPushBtn, 2, 1, 1, 1
        )
        self.verticalLayout_6.addWidget(self.serverArchiveSiteSave)
        self.serverArchiveSiteScrollArea.setWidget(
            self.serverArchiveSiteScrollAreaWidgetContents
        )
        self.gridLayout_41.addWidget(self.serverArchiveSiteScrollArea, 1, 2, 1, 2)
        self.serverArchiveSiteBackToMain = TransparentToolButton(FIF.PAGE_LEFT, self)
        self.serverArchiveSiteBackToMain.setObjectName("serverArchiveSiteBackToMain")
        self.gridLayout_41.addWidget(self.serverArchiveSiteBackToMain, 0, 1, 1, 1)
        self.serverArchiveSiteTitle = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverArchiveSiteTitle.sizePolicy().hasHeightForWidth()
        )
        self.serverArchiveSiteTitle.setSizePolicy(sizePolicy)
        self.serverArchiveSiteTitle.setObjectName("serverArchiveSiteTitle")
        self.gridLayout_41.addWidget(self.serverArchiveSiteTitle, 0, 2, 1, 1)
        spacerItem51 = QSpacerItem(20, 299, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_41.addItem(spacerItem51, 1, 1, 1, 1)
        spacerItem52 = QSpacerItem(20, 335, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_41.addItem(spacerItem52, 0, 0, 2, 1)
        self.serverArchiveSiteImportStatusText.setText(self.tr("[状态文本]"))
        self.serverArchiveSiteImportArchives.setText(self.tr("导入文件"))
        self.serverArchiveSiteImportFolder.setText(self.tr("导入文件夹"))
        self.serverArchiveSiteImportTitle.setText(self.tr("1. 导入文件/文件夹"))
        self.serverArchiveSiteAutoDetectJavaPrimaryPushBtn.setText(self.tr("自动查找Java"))
        self.serverArchiveSiteJavaSubtitleLabel.setText(self.tr("Java:"))
        self.serverArchiveSiteJavaListPushBtn.setText(self.tr("Java列表"))
        self.serverArchiveSiteManuallyAddJavaPrimaryPushBtn.setText(self.tr("手动导入"))
        self.serverArchiveSiteDownloadJavaPrimaryPushBtn.setText(self.tr("下载Java"))
        self.serverArchiveSiteOutputDeEncodingLabel.setText(self.tr("控制台输出编码（优先级高于全局设置）"))
        self.serverArchiveSiteDeEncodingSubtitleLabel.setText(self.tr("编码设置："))
        self.serverArchiveSiteInputDeEncodingLabel.setText(self.tr("指令输入编码（优先级高于全局设置）"))
        self.serverArchiveSiteJVMArgPlainTextEdit.setPlaceholderText(self.tr("可选，用一个空格分组"))
        self.serverArchiveSiteJVMArgSubtitleLabel.setText(self.tr("JVM参数："))
        self.serverArchiveSiteMemSubtitleLabel.setText(self.tr("内存:"))
        self.serverArchiveSiteToSymbol.setText(self.tr("~"))
        self.serverArchiveSiteSetArgsTitle.setText(self.tr("2. 设置参数"))
        self.serverArchiveSiteDownloadCorePrimaryPushBtn.setText(self.tr("下载核心"))
        self.serverArchiveSiteCoreSubtitleLabel.setText(self.tr("核心："))
        self.serverArchiveSiteManuallyAddCorePrimaryPushBtn.setText(self.tr("重新导入"))
        self.serverArchiveSiteSaveTitle.setText(self.tr("4. 完成导入"))
        self.serverArchiveSiteServerNameLineEdit.setPlaceholderText(self.tr("设置服务器昵称，不能包含非法字符"))
        self.serverArchiveSiteSaveServerPrimaryPushBtn.setText(self.tr("导入！"))
        self.serverArchiveSiteTitle.setText(self.tr("导入 服务器 存档 压缩包/文件夹"))

        self.serverArchiveSiteScrollArea.setFrameShape(QFrame.NoFrame)

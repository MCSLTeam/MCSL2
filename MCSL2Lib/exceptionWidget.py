from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget
from qfluentwidgets import SmoothScrollArea


class ExceptionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.exceptionWidget = QWidget(self)
        self.exceptionWidget.setGeometry(QRect(30, 40, 501, 351))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.exceptionWidget.sizePolicy().hasHeightForWidth()
        )
        self.exceptionWidget.setSizePolicy(sizePolicy)

        self.verticalLayout = QVBoxLayout(self.exceptionWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.exceptionScrollArea = SmoothScrollArea(self.exceptionWidget)
        self.exceptionScrollArea.setWidgetResizable(True)
        self.exceptionScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.exceptionScrollArea.setMinimumSize(QSize(480, 320))
        self.exceptionScrollArea.setMaximumSize(QSize(480, 320))

        self.exceptionScrollAreaWidgetContents = QWidget()
        self.exceptionScrollAreaWidgetContents.setGeometry(QRect(0, 0, 481, 331))

        self.verticalLayout_2 = QVBoxLayout(self.exceptionScrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.exceptionLabel = QLabel(self.exceptionScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.exceptionLabel.sizePolicy().hasHeightForWidth()
        )
        self.exceptionLabel.setSizePolicy(sizePolicy)
        self.exceptionLabel.setMinimumSize(QSize(463, 313))
        self.exceptionLabel.setMaximumSize(QSize(463, 16777215))
        self.exceptionLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.verticalLayout_2.addWidget(self.exceptionLabel)
        self.exceptionScrollArea.setWidget(self.exceptionScrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.exceptionScrollArea)

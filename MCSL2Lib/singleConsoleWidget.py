from PyQt5.QtWidgets import QFrame, QWidget, QSizePolicy, QGridLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import LineEdit, PlainTextEdit, PrimaryToolButton, FluentIcon as FIF


class singleConsoleWidget(QWidget):
    def __init__(self):
        super().__init__()

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.serverOutput = PlainTextEdit(self)
        self.serverOutput.setFrameShape(QFrame.NoFrame)
        self.serverOutput.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.serverOutput.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.gridLayout.addWidget(self.serverOutput, 0, 0, 1, 2)

        self.commandLineEdit = LineEdit(self)
        self.gridLayout.addWidget(self.commandLineEdit, 1, 0, 1, 1)

        self.sendCommandButton = PrimaryToolButton(FIF.SEND, self)
        self.sendCommandButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.gridLayout.addWidget(self.sendCommandButton, 1, 1, 1, 1)

        self.commandLineEdit.setPlaceholderText("在此输入指令，回车或点击右边按钮发送，不需要加/")
        self.sendCommandButton.setEnabled(False)
        self.commandLineEdit.textChanged.connect(
            lambda: self.sendCommandButton.setEnabled(self.commandLineEdit.text() != "")
        )
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.serverOutput.setReadOnly(True)
        self.sendCommandButton.clicked.connect(
            lambda: self.parent().parent().parent().sendCommand(command=self.commandLineEdit.text())
        )
        self.commandLineEdit.returnPressed.connect(
            lambda: self.parent().parent().parent().sendCommand(command=self.commandLineEdit.text())
        )

        # self.setObjectName("singleConsoleWidget")
        # self.serverOutput.setObjectName("serverOutput")
        # self.commandLineEdit.setObjectName("commandLineEdit")
        # self.sendCommandButton.setObjectName("sendCommandButton")

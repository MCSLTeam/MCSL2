from MCSL2Lib.ServerController.windowCreator import ServerWindow
from qfluentwidgets import HeaderCardWidget, CommandBar, Action, FluentIcon as FIF
from PyQt5.QtCore import QSize, Qt


class RunningServerHeaderCardWidget(HeaderCardWidget):
    def __init__(self, serverName: str, serverConsole: ServerWindow, parent=None):
        super().__init__(parent)
        self.setTitle(serverName)
        self.headerView.setFixedHeight(44)
        self.setFixedSize(QSize(245, 135))

        self.name = serverName
        self.console = serverConsole

        self.viewLayout.addWidget(_RunningServerCommandBar(self))


class _RunningServerCommandBar(CommandBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.openPrompt = Action(icon=FIF.COMMAND_PROMPT.icon(), text="终端窗口", parent=self)
        self.closeServer = Action(icon=FIF.CLOSE.icon(), text="一键关服", parent=self)
        self.completeActions()

    def parent(self) -> RunningServerHeaderCardWidget:
        return super().parent()

    def completeActions(self):
        # self.openPrompt.triggered.connect(self.parent().console.show)
        # self.closeServer.triggered.connect(self.parent().console.close)
        self.addActions([self.openPrompt, self.closeServer])

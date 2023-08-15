from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import QWidget, QSizePolicy, QGridLayout
from qfluentwidgets import BodyLabel, ComboBox, LineEdit, StrongBodyLabel


class playersController(QWidget):
    def __init__(self):

        super().__init__()
        
        self.setObjectName("playersController")

        self.playersControllerMainWidget = QWidget(self)
        self.playersControllerMainWidget.setGeometry(QRect(20, 20, 350, 241))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersControllerMainWidget.sizePolicy().hasHeightForWidth())
        self.playersControllerMainWidget.setSizePolicy(sizePolicy)
        self.playersControllerMainWidget.setMinimumSize(QSize(350, 210))
        self.playersControllerMainWidget.setObjectName("playersControllerMainWidget")

        self.gridLayout = QGridLayout(self.playersControllerMainWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.mode = ComboBox(self.playersControllerMainWidget)
        self.mode.setObjectName("mode")

        self.gridLayout.addWidget(self.mode, 0, 1, 1, 1)
        self.who = LineEdit(self.playersControllerMainWidget)
        self.who.setObjectName("who")

        self.gridLayout.addWidget(self.who, 0, 0, 1, 1)
        self.targetSelectorTip = BodyLabel(self.playersControllerMainWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targetSelectorTip.sizePolicy().hasHeightForWidth())
        self.targetSelectorTip.setSizePolicy(sizePolicy)
        self.targetSelectorTip.setObjectName("targetSelectorTip")

        self.gridLayout.addWidget(self.targetSelectorTip, 2, 0, 1, 2)
        self.playersTipTitle = StrongBodyLabel(self.playersControllerMainWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersTipTitle.sizePolicy().hasHeightForWidth())
        self.playersTipTitle.setSizePolicy(sizePolicy)
        self.playersTipTitle.setObjectName("playersTipTitle")

        self.gridLayout.addWidget(self.playersTipTitle, 3, 0, 1, 2)
        self.playersTip = BodyLabel(self.playersControllerMainWidget)
        self.playersTip.setObjectName("playersTip")

        self.gridLayout.addWidget(self.playersTip, 4, 0, 1, 2)
        self.targetSelectorTipTitle = StrongBodyLabel(self.playersControllerMainWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targetSelectorTipTitle.sizePolicy().hasHeightForWidth())
        self.targetSelectorTipTitle.setSizePolicy(sizePolicy)
        self.targetSelectorTipTitle.setObjectName("targetSelectorTipTitle")

        self.gridLayout.addWidget(self.targetSelectorTipTitle, 1, 0, 1, 2)

        self.who.setPlaceholderText("填写玩家名或目标选择器")
        self.targetSelectorTip.setText("@p - 最近的玩家(在控制台可能无法使用)\n"
                                       "@r - 随机玩家\n"
                                       "@a - 所有玩家\n"
                                       "@e - 所有实体(不包括死亡实体)\n"
                                       "@s - 命令执行者(控制台不可用)")
        self.playersTipTitle.setText("当前在线玩家：(可能不准确)")
        self.targetSelectorTipTitle.setText("目标选择器提示:")
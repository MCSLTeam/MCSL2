#     Copyright 2023, MCSL Team, mailto:lxhtt@vip.qq.com
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
"""
Settings page.
"""
from datetime import datetime
from platform import system as systemType
import sys
from typing import Union

from PyQt5.QtCore import QSize, Qt, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSizePolicy,
    QSpacerItem,
    QFrame,
    QAbstractScrollArea,
    QHBoxLayout,
    QVBoxLayout,
    QSlider,
    QApplication,
)
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    CheckBox,
    ComboBox,
    HyperlinkButton,
    PrimaryPushButton,
    RadioButton,
    Slider,
    StrongBodyLabel,
    SwitchButton,
    TitleLabel,
    ColorPickerButton,
    PushButton,
    MessageBox,
    InfoBarPosition,
    InfoBar,
    FluentIcon as FIF,
    setThemeColor,
    SmoothScrollBar
)

from MCSL2Lib import MCSL2VERSION
from MCSL2Lib.Controllers.settingsController import SettingsController
from MCSL2Lib.Controllers.updateController import (
    CheckUpdateThread,
    FetchUpdateIntroThread,
    MCSL2FileUpdater,
)
from MCSL2Lib.Controllers.logController import genSysReport
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import SettingsVariables
from MCSL2Lib.utils import MCSL2Logger
from MCSL2Lib.Widgets.myScrollArea import MySmoothScrollArea
settingsController = SettingsController()
settingsVariables = SettingsVariables()


@Singleton
class SettingsPage(QWidget):
    """设置页"""

    settingsChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tmpParent = self
        self.gridLayout_3 = QGridLayout(self)
        self.gridLayout_3.setObjectName("gridLayout_3")

        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.gridLayout_2 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayout_2.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.subTitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.gridLayout_2.addWidget(self.subTitleLabel, 2, 0, 1, 1)
        self.saveSettingsBtnWidget = QWidget(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.saveSettingsBtnWidget.sizePolicy().hasHeightForWidth()
        )
        self.saveSettingsBtnWidget.setSizePolicy(sizePolicy)
        self.saveSettingsBtnWidget.setObjectName("saveSettingsBtnWidget")

        self.horizontalLayout = QHBoxLayout(self.saveSettingsBtnWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.saveBtn = PrimaryPushButton(self.saveSettingsBtnWidget)
        self.saveBtn.setObjectName("saveBtn")

        self.horizontalLayout.addWidget(self.saveBtn)
        self.giveUpBtn = PushButton(self.saveSettingsBtnWidget)
        self.giveUpBtn.setObjectName("giveUpBtn")

        self.horizontalLayout.addWidget(self.giveUpBtn)
        self.gridLayout_2.addWidget(self.saveSettingsBtnWidget, 0, 1, 2, 1)
        self.gridLayout_3.addWidget(self.titleLimitWidget, 1, 1, 1, 2)
        self.settingsChanged.connect(self.saveSettingsBtnWidget.setVisible)
        self.saveBtn.clicked.connect(self.saveSettings)
        self.giveUpBtn.clicked.connect(self.giveUpSettings)
        self.setObjectName("settingInterface")
        
        self.isChanged = 1
        self.initReal()

    def initReal(self):
        if not self.isChanged:
            return
        if self.isChanged == 1:
            self.settingsSmoothScrollArea = MySmoothScrollArea(self)
            self.settingsSmoothScrollArea.setFrameShape(QFrame.NoFrame)
            self.settingsSmoothScrollArea.setFrameShadow(QFrame.Plain)
            self.settingsSmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.settingsSmoothScrollArea.setSizeAdjustPolicy(
                QAbstractScrollArea.AdjustToContents
            )
            self.settingsSmoothScrollArea.setWidgetResizable(True)
            self.settingsSmoothScrollArea.setObjectName("settingsSmoothScrollArea")

            self.settingsScrollAreaWidgetContents = QWidget()
            self.settingsScrollAreaWidgetContents.setGeometry(QRect(0, 0, 653, 1625))
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                self.settingsScrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
            )
            self.settingsScrollAreaWidgetContents.setSizePolicy(sizePolicy)
            self.settingsScrollAreaWidgetContents.setObjectName(
                "settingsScrollAreaWidgetContents"
            )

            self.verticalLayout = QVBoxLayout(self.settingsScrollAreaWidgetContents)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setObjectName("verticalLayout")
        self.serverSettings = CardWidget(self.settingsScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.serverSettings.sizePolicy().hasHeightForWidth()
        )
        self.serverSettings.setSizePolicy(sizePolicy)
        self.serverSettings.setMinimumSize(QSize(630, 250))
        self.serverSettings.setMaximumSize(QSize(16777215, 250))
        self.serverSettings.setObjectName("serverSettings")

        self.gridLayout_7 = QGridLayout(self.serverSettings)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.serverSettingsTitle = StrongBodyLabel(self.serverSettings)
        self.serverSettingsTitle.setObjectName("serverSettingsTitle")

        self.gridLayout_7.addWidget(self.serverSettingsTitle, 0, 2, 1, 1)
        self.serverSettingsIndicator = PrimaryPushButton(self.serverSettings)
        self.serverSettingsIndicator.setMinimumSize(QSize(3, 20))
        self.serverSettingsIndicator.setMaximumSize(QSize(3, 20))
        self.serverSettingsIndicator.setObjectName("serverSettingsIndicator")

        self.gridLayout_7.addWidget(self.serverSettingsIndicator, 0, 1, 1, 1)
        self.autoRunLastServer = QWidget(self.serverSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.autoRunLastServer.sizePolicy().hasHeightForWidth()
        )
        self.autoRunLastServer.setSizePolicy(sizePolicy)
        self.autoRunLastServer.setObjectName("autoRunLastServer")

        self.horizontalLayout_6 = QHBoxLayout(self.autoRunLastServer)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.autoRunLastServerTitle = BodyLabel(self.autoRunLastServer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.autoRunLastServerTitle.sizePolicy().hasHeightForWidth()
        )
        self.autoRunLastServerTitle.setSizePolicy(sizePolicy)
        self.autoRunLastServerTitle.setObjectName("autoRunLastServerTitle")

        self.horizontalLayout_6.addWidget(self.autoRunLastServerTitle)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.autoRunLastServerSwitchBtn = SwitchButton(self.autoRunLastServer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.autoRunLastServerSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.autoRunLastServerSwitchBtn.setSizePolicy(sizePolicy)
        self.autoRunLastServerSwitchBtn.setChecked(False)
        self.autoRunLastServerSwitchBtn.setObjectName("autoRunLastServerSwitchBtn")

        self.horizontalLayout_6.addWidget(self.autoRunLastServerSwitchBtn)
        self.gridLayout_7.addWidget(self.autoRunLastServer, 1, 0, 1, 4)
        self.acceptAllMojangEula = QWidget(self.serverSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.acceptAllMojangEula.sizePolicy().hasHeightForWidth()
        )
        self.acceptAllMojangEula.setSizePolicy(sizePolicy)
        self.acceptAllMojangEula.setObjectName("acceptAllMojangEula")

        self.horizontalLayout_7 = QHBoxLayout(self.acceptAllMojangEula)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.acceptAllMojangEulaTitle = BodyLabel(self.acceptAllMojangEula)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.acceptAllMojangEulaTitle.sizePolicy().hasHeightForWidth()
        )
        self.acceptAllMojangEulaTitle.setSizePolicy(sizePolicy)
        self.acceptAllMojangEulaTitle.setObjectName("acceptAllMojangEulaTitle")

        self.horizontalLayout_7.addWidget(self.acceptAllMojangEulaTitle)
        spacerItem3 = QSpacerItem(311, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.acceptAllMojangEulaSwitchBtn = SwitchButton(self.acceptAllMojangEula)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.acceptAllMojangEulaSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.acceptAllMojangEulaSwitchBtn.setSizePolicy(sizePolicy)
        self.acceptAllMojangEulaSwitchBtn.setObjectName("acceptAllMojangEulaSwitchBtn")

        self.horizontalLayout_7.addWidget(self.acceptAllMojangEulaSwitchBtn)
        self.gridLayout_7.addWidget(self.acceptAllMojangEula, 2, 0, 1, 4)
        self.sendStopInsteadOfKill = QWidget(self.serverSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sendStopInsteadOfKill.sizePolicy().hasHeightForWidth()
        )
        self.sendStopInsteadOfKill.setSizePolicy(sizePolicy)
        self.sendStopInsteadOfKill.setObjectName("sendStopInsteadOfKill")

        self.horizontalLayout_8 = QHBoxLayout(self.sendStopInsteadOfKill)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")

        self.sendStopInsteadOfKillTitle = BodyLabel(self.sendStopInsteadOfKill)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sendStopInsteadOfKillTitle.sizePolicy().hasHeightForWidth()
        )
        self.sendStopInsteadOfKillTitle.setSizePolicy(sizePolicy)
        self.sendStopInsteadOfKillTitle.setObjectName("sendStopInsteadOfKillTitle")

        self.horizontalLayout_8.addWidget(self.sendStopInsteadOfKillTitle)
        spacerItem4 = QSpacerItem(239, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.sendStopInsteadOfKillSwitchBtn = SwitchButton(self.sendStopInsteadOfKill)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sendStopInsteadOfKillSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.sendStopInsteadOfKillSwitchBtn.setSizePolicy(sizePolicy)
        self.sendStopInsteadOfKillSwitchBtn.setChecked(True)
        self.sendStopInsteadOfKillSwitchBtn.setObjectName(
            "sendStopInsteadOfKillSwitchBtn"
        )

        self.horizontalLayout_8.addWidget(self.sendStopInsteadOfKillSwitchBtn)
        self.gridLayout_7.addWidget(self.sendStopInsteadOfKill, 3, 0, 1, 4)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem5, 0, 3, 1, 1)
        self.restartServerWhenCrashed = QWidget(self.serverSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.restartServerWhenCrashed.sizePolicy().hasHeightForWidth()
        )
        self.restartServerWhenCrashed.setSizePolicy(sizePolicy)
        self.restartServerWhenCrashed.setObjectName("restartServerWhenCrashed")

        self.horizontalLayout_9 = QHBoxLayout(self.restartServerWhenCrashed)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")

        self.restartServerWhenCrashedTitle = BodyLabel(self.restartServerWhenCrashed)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.restartServerWhenCrashedTitle.sizePolicy().hasHeightForWidth()
        )
        self.restartServerWhenCrashedTitle.setSizePolicy(sizePolicy)
        self.restartServerWhenCrashedTitle.setObjectName(
            "restartServerWhenCrashedTitle"
        )

        self.horizontalLayout_9.addWidget(self.restartServerWhenCrashedTitle)
        spacerItem6 = QSpacerItem(311, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem6)
        self.restartServerWhenCrashedSwitchBtn = SwitchButton(
            self.restartServerWhenCrashed
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.restartServerWhenCrashedSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.restartServerWhenCrashedSwitchBtn.setSizePolicy(sizePolicy)
        self.restartServerWhenCrashedSwitchBtn.setObjectName(
            "restartServerWhenCrashedSwitchBtn"
        )

        self.horizontalLayout_9.addWidget(self.restartServerWhenCrashedSwitchBtn)
        self.gridLayout_7.addWidget(self.restartServerWhenCrashed, 4, 0, 1, 4)
        self.verticalLayout.addWidget(self.serverSettings)
        self.configureSettings = CardWidget(self.settingsScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.configureSettings.sizePolicy().hasHeightForWidth()
        )
        self.configureSettings.setSizePolicy(sizePolicy)
        self.configureSettings.setMinimumSize(QSize(630, 210))
        self.configureSettings.setMaximumSize(QSize(16777215, 210))
        self.configureSettings.setObjectName("configureSettings")

        self.gridLayout_15 = QGridLayout(self.configureSettings)
        self.gridLayout_15.setObjectName("gridLayout_15")

        self.clearAllNewServerConfigInProgram = QWidget(self.configureSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.clearAllNewServerConfigInProgram.sizePolicy().hasHeightForWidth()
        )
        self.clearAllNewServerConfigInProgram.setSizePolicy(sizePolicy)
        self.clearAllNewServerConfigInProgram.setObjectName(
            "clearAllNewServerConfigInProgram"
        )

        self.horizontalLayout_65 = QHBoxLayout(self.clearAllNewServerConfigInProgram)
        self.horizontalLayout_65.setObjectName("horizontalLayout_65")

        self.clearAllNewServerConfigInProgramTitle = BodyLabel(
            self.clearAllNewServerConfigInProgram
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.clearAllNewServerConfigInProgramTitle.sizePolicy().hasHeightForWidth()
        )
        self.clearAllNewServerConfigInProgramTitle.setSizePolicy(sizePolicy)
        self.clearAllNewServerConfigInProgramTitle.setObjectName(
            "clearAllNewServerConfigInProgramTitle"
        )

        self.horizontalLayout_65.addWidget(self.clearAllNewServerConfigInProgramTitle)
        spacerItem6 = QSpacerItem(321, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_65.addItem(spacerItem6)
        self.clearAllNewServerConfigInProgramSwitchBtn = SwitchButton(
            self.clearAllNewServerConfigInProgram
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.clearAllNewServerConfigInProgramSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.clearAllNewServerConfigInProgramSwitchBtn.setSizePolicy(sizePolicy)
        self.clearAllNewServerConfigInProgramSwitchBtn.setObjectName(
            "clearAllNewServerConfigInProgramSwitchBtn"
        )

        self.horizontalLayout_65.addWidget(
            self.clearAllNewServerConfigInProgramSwitchBtn
        )
        self.gridLayout_15.addWidget(self.clearAllNewServerConfigInProgram, 3, 0, 1, 4)
        self.configureSettingsTitle = StrongBodyLabel(self.configureSettings)
        self.configureSettingsTitle.setObjectName("configureSettingsTitle")

        self.gridLayout_15.addWidget(self.configureSettingsTitle, 0, 2, 1, 1)
        self.configureSettingsIndicator = PrimaryPushButton(self.configureSettings)
        self.configureSettingsIndicator.setMinimumSize(QSize(3, 20))
        self.configureSettingsIndicator.setMaximumSize(QSize(3, 20))
        self.configureSettingsIndicator.setText("")
        self.configureSettingsIndicator.setObjectName("configureSettingsIndicator")

        self.gridLayout_15.addWidget(self.configureSettingsIndicator, 0, 1, 1, 1)
        spacerItem7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_15.addItem(spacerItem7, 0, 3, 1, 1)
        self.newServerType = QWidget(self.configureSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.newServerType.sizePolicy().hasHeightForWidth()
        )
        self.newServerType.setSizePolicy(sizePolicy)
        self.newServerType.setObjectName("newServerType")

        self.horizontalLayout_64 = QHBoxLayout(self.newServerType)
        self.horizontalLayout_64.setObjectName("horizontalLayout_64")

        self.newServerTypeTitle = BodyLabel(self.newServerType)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.newServerTypeTitle.sizePolicy().hasHeightForWidth()
        )
        self.newServerTypeTitle.setSizePolicy(sizePolicy)
        self.newServerTypeTitle.setObjectName("newServerTypeTitle")

        self.horizontalLayout_64.addWidget(self.newServerTypeTitle)
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_64.addItem(spacerItem8)
        self.newServerTypeComboBox = ComboBox(self.newServerType)
        self.newServerTypeComboBox.setObjectName("newServerTypeComboBox")

        self.horizontalLayout_64.addWidget(self.newServerTypeComboBox)
        self.gridLayout_15.addWidget(self.newServerType, 1, 0, 1, 4)
        self.onlySaveGlobalServerConfig = QWidget(self.configureSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.onlySaveGlobalServerConfig.sizePolicy().hasHeightForWidth()
        )
        self.onlySaveGlobalServerConfig.setSizePolicy(sizePolicy)
        self.onlySaveGlobalServerConfig.setObjectName("onlySaveGlobalServerConfig")

        self.horizontalLayout_63 = QHBoxLayout(self.onlySaveGlobalServerConfig)
        self.horizontalLayout_63.setObjectName("horizontalLayout_63")

        self.onlySaveGlobalServerConfigTitle = BodyLabel(
            self.onlySaveGlobalServerConfig
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.onlySaveGlobalServerConfigTitle.sizePolicy().hasHeightForWidth()
        )
        self.onlySaveGlobalServerConfigTitle.setSizePolicy(sizePolicy)
        self.onlySaveGlobalServerConfigTitle.setObjectName(
            "onlySaveGlobalServerConfigTitle"
        )

        self.horizontalLayout_63.addWidget(self.onlySaveGlobalServerConfigTitle)
        spacerItem9 = QSpacerItem(321, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_63.addItem(spacerItem9)
        self.onlySaveGlobalServerConfigSwitchBtn = SwitchButton(
            self.onlySaveGlobalServerConfig
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.onlySaveGlobalServerConfigSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.onlySaveGlobalServerConfigSwitchBtn.setSizePolicy(sizePolicy)
        self.onlySaveGlobalServerConfigSwitchBtn.setObjectName(
            "onlySaveGlobalServerConfigSwitchBtn"
        )

        self.horizontalLayout_63.addWidget(self.onlySaveGlobalServerConfigSwitchBtn)
        self.gridLayout_15.addWidget(self.onlySaveGlobalServerConfig, 2, 0, 1, 4)
        self.verticalLayout.addWidget(self.configureSettings)
        self.downloadSettings = CardWidget(self.settingsScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.downloadSettings.sizePolicy().hasHeightForWidth()
        )
        self.downloadSettings.setSizePolicy(sizePolicy)
        self.downloadSettings.setMinimumSize(QSize(630, 245))
        self.downloadSettings.setMaximumSize(QSize(16777215, 245))
        self.downloadSettings.setObjectName("downloadSettings")

        self.gridLayout_10 = QGridLayout(self.downloadSettings)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.downloadSettingsTitle = StrongBodyLabel(self.downloadSettings)
        self.downloadSettingsTitle.setObjectName("downloadSettingsTitle")

        self.gridLayout_10.addWidget(self.downloadSettingsTitle, 0, 2, 1, 1)
        self.alwaysAskSaveDirectory = QWidget(self.downloadSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alwaysAskSaveDirectory.sizePolicy().hasHeightForWidth()
        )
        self.alwaysAskSaveDirectory.setSizePolicy(sizePolicy)
        self.alwaysAskSaveDirectory.setMinimumSize(QSize(0, 60))
        self.alwaysAskSaveDirectory.setMaximumSize(QSize(16777215, 60))
        self.alwaysAskSaveDirectory.setObjectName("alwaysAskSaveDirectory")

        self.gridLayout_14 = QGridLayout(self.alwaysAskSaveDirectory)
        self.gridLayout_14.setObjectName("gridLayout_14")

        spacerItem10 = QSpacerItem(317, 39, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_14.addItem(spacerItem10, 0, 1, 2, 1)
        self.alwaysAskSaveDirectoryInfo = BodyLabel(self.alwaysAskSaveDirectory)
        self.alwaysAskSaveDirectoryInfo.setObjectName("alwaysAskSaveDirectoryInfo")

        self.gridLayout_14.addWidget(self.alwaysAskSaveDirectoryInfo, 1, 0, 1, 1)
        self.alwaysAskSaveDirectoryCheckBox = CheckBox(self.alwaysAskSaveDirectory)
        self.alwaysAskSaveDirectoryCheckBox.setObjectName(
            "alwaysAskSaveDirectoryCheckBox"
        )

        self.gridLayout_14.addWidget(self.alwaysAskSaveDirectoryCheckBox, 0, 0, 1, 1)
        self.gridLayout_10.addWidget(self.alwaysAskSaveDirectory, 2, 0, 1, 4)
        self.aria2Thread = QWidget(self.downloadSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aria2Thread.sizePolicy().hasHeightForWidth())
        self.aria2Thread.setSizePolicy(sizePolicy)
        self.aria2Thread.setObjectName("aria2Thread")

        self.horizontalLayout_55 = QHBoxLayout(self.aria2Thread)
        self.horizontalLayout_55.setObjectName("horizontalLayout_55")

        self.aria2ThreadTitle = BodyLabel(self.aria2Thread)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.aria2ThreadTitle.sizePolicy().hasHeightForWidth()
        )
        self.aria2ThreadTitle.setSizePolicy(sizePolicy)
        self.aria2ThreadTitle.setObjectName("aria2ThreadTitle")

        self.horizontalLayout_55.addWidget(self.aria2ThreadTitle)
        spacerItem11 = QSpacerItem(321, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_55.addItem(spacerItem11)
        self.aria2ThreadSlider = Slider(self.aria2Thread)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.aria2ThreadSlider.sizePolicy().hasHeightForWidth()
        )
        self.aria2ThreadSlider.setSizePolicy(sizePolicy)
        self.aria2ThreadSlider.setFixedSize(QSize(200, 24))
        self.aria2ThreadSlider.setFocusPolicy(Qt.NoFocus)
        self.aria2ThreadSlider.setMinimum(1)
        self.aria2ThreadSlider.setMaximum(
            128 if "windows" in systemType().lower() else 16
        )
        self.aria2ThreadSlider.setSliderPosition(1)
        self.aria2ThreadSlider.setOrientation(Qt.Horizontal)
        self.aria2ThreadSlider.setInvertedAppearance(False)
        self.aria2ThreadSlider.setInvertedControls(False)
        self.aria2ThreadSlider.setTickPosition(QSlider.NoTicks)
        self.aria2ThreadSlider.setTickInterval(1)
        self.aria2ThreadSlider.setObjectName("aria2ThreadSlider")

        self.horizontalLayout_55.addWidget(self.aria2ThreadSlider)
        self.aria2ThreadNum = BodyLabel(self.aria2Thread)
        self.aria2ThreadNum.setObjectName("aria2ThreadNum")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.aria2ThreadNum.sizePolicy().hasHeightForWidth()
        )
        self.aria2ThreadNum.setSizePolicy(sizePolicy)
        self.aria2ThreadNum.setFixedSize(QSize(30, 19))

        self.horizontalLayout_55.addWidget(self.aria2ThreadNum)
        self.gridLayout_10.addWidget(self.aria2Thread, 3, 1, 1, 3)
        self.saveSameFileException = QWidget(self.downloadSettings)
        self.saveSameFileException.setObjectName("saveSameFileException")

        self.horizontalLayout_4 = QHBoxLayout(self.saveSameFileException)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.saveSameFileExceptionTitle = BodyLabel(self.saveSameFileException)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.saveSameFileExceptionTitle.sizePolicy().hasHeightForWidth()
        )
        self.saveSameFileExceptionTitle.setSizePolicy(sizePolicy)
        self.saveSameFileExceptionTitle.setObjectName("saveSameFileExceptionTitle")

        self.horizontalLayout_4.addWidget(self.saveSameFileExceptionTitle)
        spacerItem12 = QSpacerItem(235, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem12)
        self.saveSameFileExceptionToAsk = RadioButton(self.saveSameFileException)
        self.saveSameFileExceptionToAsk.setChecked(True)
        self.saveSameFileExceptionToAsk.setObjectName("saveSameFileExceptionToAsk")

        self.horizontalLayout_4.addWidget(self.saveSameFileExceptionToAsk)
        self.saveSameFileExceptionToOverwrite = RadioButton(self.saveSameFileException)
        self.saveSameFileExceptionToOverwrite.setObjectName(
            "saveSameFileExceptionToOverwrite"
        )

        self.horizontalLayout_4.addWidget(self.saveSameFileExceptionToOverwrite)
        self.saveSameFileExceptionToStop = RadioButton(self.saveSameFileException)
        self.saveSameFileExceptionToStop.setObjectName("saveSameFileExceptionToStop")

        self.horizontalLayout_4.addWidget(self.saveSameFileExceptionToStop)
        self.gridLayout_10.addWidget(self.saveSameFileException, 4, 1, 1, 3)
        self.downloadSource = QWidget(self.downloadSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.downloadSource.sizePolicy().hasHeightForWidth()
        )
        self.downloadSource.setSizePolicy(sizePolicy)
        self.downloadSource.setObjectName("downloadSource")

        self.horizontalLayout_56 = QHBoxLayout(self.downloadSource)
        self.horizontalLayout_56.setObjectName("horizontalLayout_56")

        self.downloadSourceTitle = BodyLabel(self.downloadSource)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.downloadSourceTitle.sizePolicy().hasHeightForWidth()
        )
        self.downloadSourceTitle.setSizePolicy(sizePolicy)
        self.downloadSourceTitle.setObjectName("downloadSourceTitle")

        self.horizontalLayout_56.addWidget(self.downloadSourceTitle)
        spacerItem13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_56.addItem(spacerItem13)
        self.downloadSourceComboBox = ComboBox(self.downloadSource)
        self.downloadSourceComboBox.setObjectName("downloadSourceComboBox")

        self.horizontalLayout_56.addWidget(self.downloadSourceComboBox)
        self.gridLayout_10.addWidget(self.downloadSource, 1, 0, 1, 4)
        self.downloadSettingsIndicator = PrimaryPushButton(self.downloadSettings)
        self.downloadSettingsIndicator.setMinimumSize(QSize(3, 20))
        self.downloadSettingsIndicator.setMaximumSize(QSize(3, 20))
        self.downloadSettingsIndicator.setText("")
        self.downloadSettingsIndicator.setObjectName("downloadSettingsIndicator")

        self.gridLayout_10.addWidget(self.downloadSettingsIndicator, 0, 1, 1, 1)
        spacerItem14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem14, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.downloadSettings)
        self.consoleSettings = CardWidget(self.settingsScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.consoleSettings.sizePolicy().hasHeightForWidth()
        )
        self.consoleSettings.setSizePolicy(sizePolicy)
        self.consoleSettings.setMinimumSize(QSize(630, 260))
        self.consoleSettings.setMaximumSize(QSize(16777215, 260))
        self.consoleSettings.setObjectName("consoleSettings")

        self.gridLayout_9 = QGridLayout(self.consoleSettings)
        self.gridLayout_9.setObjectName("gridLayout_9")

        self.consoleSettingsTitle = StrongBodyLabel(self.consoleSettings)
        self.consoleSettingsTitle.setObjectName("consoleSettingsTitle")

        self.gridLayout_9.addWidget(self.consoleSettingsTitle, 0, 2, 1, 1)
        self.inputDeEncoding = QWidget(self.consoleSettings)
        self.inputDeEncoding.setObjectName("inputDeEncoding")

        self.horizontalLayout_5 = QHBoxLayout(self.inputDeEncoding)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.inputDeEncodingTitle = BodyLabel(self.inputDeEncoding)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inputDeEncodingTitle.sizePolicy().hasHeightForWidth()
        )
        self.inputDeEncodingTitle.setSizePolicy(sizePolicy)
        self.inputDeEncodingTitle.setObjectName("inputDeEncodingTitle")

        self.horizontalLayout_5.addWidget(self.inputDeEncodingTitle)
        spacerItem15 = QSpacerItem(272, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem15)
        self.inputDeEncodingComboBox = ComboBox(self.inputDeEncoding)
        self.inputDeEncodingComboBox.setObjectName("inputDeEncodingComboBox")

        self.horizontalLayout_5.addWidget(self.inputDeEncodingComboBox)
        self.gridLayout_9.addWidget(self.inputDeEncoding, 2, 0, 1, 4)
        self.outputDeEncoding = QWidget(self.consoleSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.outputDeEncoding.sizePolicy().hasHeightForWidth()
        )
        self.outputDeEncoding.setSizePolicy(sizePolicy)
        self.outputDeEncoding.setObjectName("outputDeEncoding")

        self.horizontalLayout_54 = QHBoxLayout(self.outputDeEncoding)
        self.horizontalLayout_54.setObjectName("horizontalLayout_54")

        self.outputDeEncodingTitle = BodyLabel(self.outputDeEncoding)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.outputDeEncodingTitle.sizePolicy().hasHeightForWidth()
        )
        self.outputDeEncodingTitle.setSizePolicy(sizePolicy)
        self.outputDeEncodingTitle.setObjectName("outputDeEncodingTitle")

        self.horizontalLayout_54.addWidget(self.outputDeEncodingTitle)
        spacerItem16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_54.addItem(spacerItem16)
        self.outputDeEncodingComboBox = ComboBox(self.outputDeEncoding)
        self.outputDeEncodingComboBox.setObjectName("outputDeEncodingComboBox")

        self.horizontalLayout_54.addWidget(self.outputDeEncodingComboBox)
        self.gridLayout_9.addWidget(self.outputDeEncoding, 1, 0, 1, 4)
        spacerItem17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem17, 0, 3, 1, 1)
        self.quickMenu = QWidget(self.consoleSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quickMenu.sizePolicy().hasHeightForWidth())
        self.quickMenu.setSizePolicy(sizePolicy)
        self.quickMenu.setObjectName("quickMenu")

        self.horizontalLayout_53 = QHBoxLayout(self.quickMenu)
        self.horizontalLayout_53.setObjectName("horizontalLayout_53")

        self.quickMenuTitle = BodyLabel(self.quickMenu)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.quickMenuTitle.sizePolicy().hasHeightForWidth()
        )
        self.quickMenuTitle.setSizePolicy(sizePolicy)
        self.quickMenuTitle.setObjectName("quickMenuTitle")

        self.horizontalLayout_53.addWidget(self.quickMenuTitle)
        spacerItem18 = QSpacerItem(321, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_53.addItem(spacerItem18)
        self.quickMenuSwitchBtn = SwitchButton(self.quickMenu)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.quickMenuSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.quickMenuSwitchBtn.setSizePolicy(sizePolicy)
        self.quickMenuSwitchBtn.setChecked(True)
        self.quickMenuSwitchBtn.setObjectName("quickMenuSwitchBtn")

        self.horizontalLayout_53.addWidget(self.quickMenuSwitchBtn)
        self.gridLayout_9.addWidget(self.quickMenu, 4, 0, 1, 4)
        self.consoleSettingsIndicator = PrimaryPushButton(self.consoleSettings)
        self.consoleSettingsIndicator.setMinimumSize(QSize(3, 20))
        self.consoleSettingsIndicator.setMaximumSize(QSize(3, 20))
        self.consoleSettingsIndicator.setText("")
        self.consoleSettingsIndicator.setObjectName("consoleSettingsIndicator")

        self.gridLayout_9.addWidget(self.consoleSettingsIndicator, 0, 1, 1, 1)
        self.clearConsoleWhenStopServer = QWidget(self.consoleSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.clearConsoleWhenStopServer.sizePolicy().hasHeightForWidth()
        )
        self.clearConsoleWhenStopServer.setSizePolicy(sizePolicy)
        self.clearConsoleWhenStopServer.setObjectName("clearConsoleWhenStopServer")

        self.horizontalLayout_57 = QHBoxLayout(self.clearConsoleWhenStopServer)
        self.horizontalLayout_57.setObjectName("horizontalLayout_57")

        self.clearConsoleWhenStopServerTitle = BodyLabel(
            self.clearConsoleWhenStopServer
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.clearConsoleWhenStopServerTitle.sizePolicy().hasHeightForWidth()
        )
        self.clearConsoleWhenStopServerTitle.setSizePolicy(sizePolicy)
        self.clearConsoleWhenStopServerTitle.setObjectName(
            "clearConsoleWhenStopServerTitle"
        )

        self.horizontalLayout_57.addWidget(self.clearConsoleWhenStopServerTitle)
        spacerItem19 = QSpacerItem(321, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_57.addItem(spacerItem19)
        self.clearConsoleWhenStopServerSwitchBtn = SwitchButton(
            self.clearConsoleWhenStopServer
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.clearConsoleWhenStopServerSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.clearConsoleWhenStopServerSwitchBtn.setSizePolicy(sizePolicy)
        self.clearConsoleWhenStopServerSwitchBtn.setChecked(False)
        self.clearConsoleWhenStopServerSwitchBtn.setObjectName(
            "clearConsoleWhenStopServerSwitchBtn"
        )

        self.horizontalLayout_57.addWidget(self.clearConsoleWhenStopServerSwitchBtn)
        self.gridLayout_9.addWidget(self.clearConsoleWhenStopServer, 5, 0, 1, 4)
        self.verticalLayout.addWidget(self.consoleSettings)
        self.softwareSettings = CardWidget(self.settingsScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.softwareSettings.sizePolicy().hasHeightForWidth()
        )
        self.softwareSettings.setSizePolicy(sizePolicy)
        self.softwareSettings.setMinimumSize(QSize(630, 250))
        self.softwareSettings.setMaximumSize(QSize(16777215, 250))
        self.softwareSettings.setObjectName("softwareSettings")

        self.gridLayout_13 = QGridLayout(self.softwareSettings)
        self.gridLayout_13.setObjectName("gridLayout_13")

        spacerItem18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem18, 0, 3, 1, 1)
        self.startOnStartup = QWidget(self.softwareSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.startOnStartup.sizePolicy().hasHeightForWidth()
        )
        self.startOnStartup.setSizePolicy(sizePolicy)
        self.startOnStartup.setObjectName("startOnStartup")

        self.horizontalLayout_61 = QHBoxLayout(self.startOnStartup)
        self.horizontalLayout_61.setObjectName("horizontalLayout_61")

        self.startOnStartupTitle = BodyLabel(self.startOnStartup)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.startOnStartupTitle.sizePolicy().hasHeightForWidth()
        )
        self.startOnStartupTitle.setSizePolicy(sizePolicy)
        self.startOnStartupTitle.setObjectName("startOnStartupTitle")

        self.horizontalLayout_61.addWidget(self.startOnStartupTitle)
        spacerItem19 = QSpacerItem(321, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_61.addItem(spacerItem19)
        self.startOnStartupSwitchBtn = SwitchButton(self.startOnStartup)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.startOnStartupSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.startOnStartupSwitchBtn.setSizePolicy(sizePolicy)
        self.startOnStartupSwitchBtn.setObjectName("startOnStartupSwitchBtn")

        self.horizontalLayout_61.addWidget(self.startOnStartupSwitchBtn)
        self.gridLayout_13.addWidget(self.startOnStartup, 5, 0, 1, 4)
        self.softwareSettingsIndicator = PrimaryPushButton(self.softwareSettings)
        self.softwareSettingsIndicator.setMinimumSize(QSize(3, 20))
        self.softwareSettingsIndicator.setMaximumSize(QSize(3, 20))
        self.softwareSettingsIndicator.setText("")
        self.softwareSettingsIndicator.setObjectName("softwareSettingsIndicator")

        self.gridLayout_13.addWidget(self.softwareSettingsIndicator, 0, 1, 1, 1)
        self.softwareSettingsTitle = StrongBodyLabel(self.softwareSettings)
        self.softwareSettingsTitle.setObjectName("softwareSettingsTitle")

        self.gridLayout_13.addWidget(self.softwareSettingsTitle, 0, 2, 1, 1)
        self.theme = QWidget(self.softwareSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.theme.sizePolicy().hasHeightForWidth())
        self.theme.setSizePolicy(sizePolicy)
        self.theme.setObjectName("theme")

        self.horizontalLayout_62 = QHBoxLayout(self.theme)
        self.horizontalLayout_62.setObjectName("horizontalLayout_62")

        self.themeTitle = BodyLabel(self.theme)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.themeTitle.sizePolicy().hasHeightForWidth())
        self.themeTitle.setSizePolicy(sizePolicy)
        self.themeTitle.setObjectName("themeTitle")

        self.horizontalLayout_62.addWidget(self.themeTitle)
        spacerItem20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_62.addItem(spacerItem20)
        self.themeComboBox = ComboBox(self.theme)
        self.themeComboBox.setObjectName("themeComboBox")

        self.horizontalLayout_62.addWidget(self.themeComboBox)
        self.gridLayout_13.addWidget(self.theme, 1, 0, 1, 4)
        self.themeColor = QWidget(self.softwareSettings)
        self.themeColor.setObjectName("themeColor")

        self.horizontalLayout_14 = QHBoxLayout(self.themeColor)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")

        self.themeColorTitle = BodyLabel(self.themeColor)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.themeColorTitle.sizePolicy().hasHeightForWidth()
        )
        self.themeColorTitle.setSizePolicy(sizePolicy)
        self.themeColorTitle.setObjectName("themeColorTitle")

        self.horizontalLayout_14.addWidget(self.themeColorTitle)
        spacerItem21 = QSpacerItem(449, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem21)
        self.selectThemeColorBtn = ColorPickerButton(
            QColor(str(settingsController.fileSettings["themeColor"])),
            "主题颜色",
            self.themeColor,
            enableAlpha=False,
        )
        self.selectThemeColorBtn.setObjectName("selectThemeColorBtn")

        self.horizontalLayout_14.addWidget(self.selectThemeColorBtn)
        self.gridLayout_13.addWidget(self.themeColor, 3, 0, 1, 4)
        self.alwaysRunAsAdministrator = QWidget(self.softwareSettings)
        self.alwaysRunAsAdministrator.setObjectName("alwaysRunAsAdministrator")

        self.horizontalLayout_15 = QHBoxLayout(self.alwaysRunAsAdministrator)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")

        self.alwaysRunAsAdministratorTitle = BodyLabel(self.alwaysRunAsAdministrator)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alwaysRunAsAdministratorTitle.sizePolicy().hasHeightForWidth()
        )
        self.alwaysRunAsAdministratorTitle.setSizePolicy(sizePolicy)
        self.alwaysRunAsAdministratorTitle.setObjectName(
            "alwaysRunAsAdministratorTitle"
        )

        self.horizontalLayout_15.addWidget(self.alwaysRunAsAdministratorTitle)
        spacerItem22 = QSpacerItem(355, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem22)
        self.alwaysRunAsAdministratorSwitchBtn = SwitchButton(
            self.alwaysRunAsAdministrator
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alwaysRunAsAdministratorSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.alwaysRunAsAdministratorSwitchBtn.setSizePolicy(sizePolicy)
        self.alwaysRunAsAdministratorSwitchBtn.setObjectName(
            "alwaysRunAsAdministratorSwitchBtn"
        )

        self.horizontalLayout_15.addWidget(self.alwaysRunAsAdministratorSwitchBtn)
        self.gridLayout_13.addWidget(self.alwaysRunAsAdministrator, 4, 1, 1, 3)
        self.verticalLayout.addWidget(self.softwareSettings)
        self.updateSettings = CardWidget(self.settingsScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.updateSettings.sizePolicy().hasHeightForWidth()
        )
        self.updateSettings.setSizePolicy(sizePolicy)
        self.updateSettings.setMinimumSize(QSize(630, 150))
        self.updateSettings.setMaximumSize(QSize(16777215, 150))
        self.updateSettings.setObjectName("updateSettings")

        self.gridLayout_6 = QGridLayout(self.updateSettings)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.currentVer = QWidget(self.updateSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currentVer.sizePolicy().hasHeightForWidth())
        self.currentVer.setSizePolicy(sizePolicy)
        self.currentVer.setObjectName("currentVer")

        self.horizontalLayout_48 = QHBoxLayout(self.currentVer)
        self.horizontalLayout_48.setObjectName("horizontalLayout_48")

        self.currentVerTitle = BodyLabel(self.currentVer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.currentVerTitle.sizePolicy().hasHeightForWidth()
        )
        self.currentVerTitle.setSizePolicy(sizePolicy)
        self.currentVerTitle.setObjectName("currentVerTitle")

        self.horizontalLayout_48.addWidget(self.currentVerTitle)
        self.currentVerLabel = BodyLabel(self.currentVer)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.currentVerLabel.sizePolicy().hasHeightForWidth()
        )
        self.currentVerLabel.setSizePolicy(sizePolicy)
        self.currentVerLabel.setObjectName("currentVerLabel")

        self.horizontalLayout_48.addWidget(self.currentVerLabel)
        spacerItem23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_48.addItem(spacerItem23)
        self.checkUpdateBtn = PrimaryPushButton(self.currentVer)
        self.checkUpdateBtn.setObjectName("checkUpdateBtn")

        self.horizontalLayout_48.addWidget(self.checkUpdateBtn)
        self.gridLayout_6.addWidget(self.currentVer, 2, 0, 1, 4)
        self.checkUpdateOnStart = QWidget(self.updateSettings)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.checkUpdateOnStart.sizePolicy().hasHeightForWidth()
        )
        self.checkUpdateOnStart.setSizePolicy(sizePolicy)
        self.checkUpdateOnStart.setObjectName("checkUpdateOnStart")

        self.horizontalLayout_47 = QHBoxLayout(self.checkUpdateOnStart)
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")

        self.checkUpdateOnStartTitle = BodyLabel(self.checkUpdateOnStart)
        self.checkUpdateOnStartTitle.setObjectName("checkUpdateOnStartTitle")

        self.horizontalLayout_47.addWidget(self.checkUpdateOnStartTitle)
        spacerItem24 = QSpacerItem(321, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_47.addItem(spacerItem24)
        self.checkUpdateOnStartSwitchBtn = SwitchButton(self.checkUpdateOnStart)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.checkUpdateOnStartSwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.checkUpdateOnStartSwitchBtn.setSizePolicy(sizePolicy)
        self.checkUpdateOnStartSwitchBtn.setObjectName("checkUpdateOnStartSwitchBtn")

        self.horizontalLayout_47.addWidget(self.checkUpdateOnStartSwitchBtn)
        self.gridLayout_6.addWidget(self.checkUpdateOnStart, 3, 0, 1, 4)
        self.updateSettingsTitle = StrongBodyLabel(self.updateSettings)
        self.updateSettingsTitle.setObjectName("updateSettingsTitle")

        self.gridLayout_6.addWidget(self.updateSettingsTitle, 0, 2, 1, 1)
        self.updateSettingsIndicator = PrimaryPushButton(self.updateSettings)
        self.updateSettingsIndicator.setMinimumSize(QSize(3, 20))
        self.updateSettingsIndicator.setMaximumSize(QSize(3, 20))
        self.updateSettingsIndicator.setText("")
        self.updateSettingsIndicator.setObjectName("updateSettingsIndicator")

        self.gridLayout_6.addWidget(self.updateSettingsIndicator, 0, 1, 1, 1)
        spacerItem25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem25, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.updateSettings)
        self.about = CardWidget(self.settingsScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about.sizePolicy().hasHeightForWidth())
        self.about.setSizePolicy(sizePolicy)
        self.about.setMinimumSize(QSize(630, 250))
        self.about.setMaximumSize(QSize(16777215, 250))
        self.about.setObjectName("about")

        self.gridLayout_5 = QGridLayout(self.about)
        self.gridLayout_5.setObjectName("gridLayout_5")

        spacerItem29 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem29, 0, 3, 1, 1)
        self.aboutContentWidget = QWidget(self.about)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.aboutContentWidget.sizePolicy().hasHeightForWidth()
        )
        self.aboutContentWidget.setSizePolicy(sizePolicy)
        self.aboutContentWidget.setObjectName("aboutContentWidget")

        self.gridLayout = QGridLayout(self.aboutContentWidget)
        self.gridLayout.setObjectName("gridLayout")

        self.openOfficialWeb = HyperlinkButton(
            "https://mcsl.com.cn", "打开官网", self.aboutContentWidget, FIF.LINK
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.openOfficialWeb.sizePolicy().hasHeightForWidth()
        )
        self.openOfficialWeb.setSizePolicy(sizePolicy)
        self.openOfficialWeb.setObjectName("openOfficialWeb")

        self.gridLayout.addWidget(self.openOfficialWeb, 1, 1, 1, 1)
        self.openSourceCodeRepo = HyperlinkButton(
            "https://www.github.com/MCSLTeam/MCSL2",
            "打开源码仓库",
            self.aboutContentWidget,
            FIF.LINK,
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.openSourceCodeRepo.sizePolicy().hasHeightForWidth()
        )
        self.openSourceCodeRepo.setSizePolicy(sizePolicy)
        self.openSourceCodeRepo.setObjectName("openSourceCodeRepo")

        self.gridLayout.addWidget(self.openSourceCodeRepo, 1, 2, 1, 1)
        self.aboutContent = BodyLabel(self.aboutContentWidget)
        self.aboutContent.setObjectName("aboutContent")

        self.gridLayout.addWidget(self.aboutContent, 0, 0, 1, 7)
        self.joinQQGroup = HyperlinkButton(
            "https://jq.qq.com/?_wv=1027&k=x2ISlviQ",
            "加入官方群聊",
            self.aboutContentWidget,
            FIF.LINK,
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.joinQQGroup.sizePolicy().hasHeightForWidth())
        self.joinQQGroup.setSizePolicy(sizePolicy)
        self.joinQQGroup.setObjectName("joinQQGroup")

        self.gridLayout.addWidget(self.joinQQGroup, 1, 0, 1, 1)
        self.generateSysReport = PrimaryPushButton(self.aboutContentWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.generateSysReport.sizePolicy().hasHeightForWidth()
        )
        self.generateSysReport.setSizePolicy(sizePolicy)
        self.generateSysReport.setObjectName("generateSysReport")

        self.gridLayout.addWidget(self.generateSysReport, 1, 4, 1, 1)
        spacerItem30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem30, 1, 5, 1, 2)
        self.sponsorsBtn = HyperlinkButton(
            "https://github.com/MCSLTeam/MCSL2/blob/master/Sponsors.md", "赞助者列表", self.aboutContentWidget, FIF.PEOPLE
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sponsorsBtn.sizePolicy().hasHeightForWidth()
        )
        self.sponsorsBtn.setSizePolicy(sizePolicy)
        self.sponsorsBtn.setObjectName("augSponsorsBtn")

        self.gridLayout.addWidget(self.sponsorsBtn, 1, 3, 1, 1)
        self.gridLayout_5.addWidget(self.aboutContentWidget, 2, 0, 1, 4)
        self.aboutIndicator = PrimaryPushButton(self.about)
        self.aboutIndicator.setFixedSize(QSize(3, 20))
        self.aboutIndicator.setObjectName("aboutIndicator")

        self.gridLayout_5.addWidget(self.aboutIndicator, 0, 1, 1, 1)
        self.aboutTitle = StrongBodyLabel(self.about)
        self.aboutTitle.setObjectName("aboutTitle")

        self.gridLayout_5.addWidget(self.aboutTitle, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.about)
        self.spacerItem31 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.spacerItem31)
        self.settingsSmoothScrollArea.setWidget(self.settingsScrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.settingsSmoothScrollArea, 2, 1, 1, 1)

        self.titleLabel.setText(self.tr("设置"))
        self.subTitleLabel.setText(self.tr("自定义你的MCSL2。"))
        self.autoRunLastServerTitle.setText(self.tr("启动时自动运行上次运行的服务器"))
        self.serverSettingsTitle.setText(self.tr("服务器设置"))
        self.acceptAllMojangEulaTitle.setText(self.tr("创建时自动同意服务器的Eula"))
        self.sendStopInsteadOfKillTitle.setText(self.tr("安全关闭服务器而不是结束进程（慎点）"))
        self.restartServerWhenCrashedTitle.setText(self.tr("当前开启的服务器崩溃自动重启"))
        self.onlySaveGlobalServerConfigTitle.setText(self.tr("只保存全局服务器设置"))
        self.configureSettingsTitle.setText(self.tr("新建服务器设置"))
        self.newServerTypeTitle.setText(self.tr("新建服务器引导方式"))
        self.downloadSettingsTitle.setText(self.tr("下载设置"))
        self.alwaysAskSaveDirectoryInfo.setText(self.tr("          不勾选，则保存到MCSL2/Downloads文件夹。"))
        self.alwaysAskSaveDirectoryCheckBox.setText(self.tr("总是询问保存路径"))
        self.aria2ThreadTitle.setText(
            self.tr("Aria2下载引擎线程数 (不建议大于64)")
            if "windows" in systemType().lower()
            else self.tr("Aria2下载引擎线程数")
        )
        self.saveSameFileExceptionTitle.setText(self.tr("保存路径存在同名文件的处理"))
        self.saveSameFileExceptionToAsk.setText(self.tr("询问"))
        self.saveSameFileExceptionToOverwrite.setText(self.tr("覆盖"))
        self.saveSameFileExceptionToStop.setText(self.tr("停止"))
        self.downloadSourceTitle.setText(self.tr("下载源"))
        self.quickMenuTitle.setText(self.tr("快捷菜单"))
        self.consoleSettingsTitle.setText(self.tr("终端设置"))
        self.inputDeEncodingTitle.setText(self.tr("指令输入编码（优先级低于服务器配置设置）"))
        self.outputDeEncodingTitle.setText(self.tr("控制台输出编码（优先级低于服务器配置设置）"))
        self.startOnStartupTitle.setText(self.tr("开机自启动"))
        self.softwareSettingsTitle.setText(self.tr("软件设置"))
        self.themeTitle.setText(self.tr("主题"))
        self.themeColorTitle.setText(self.tr("主题颜色"))
        self.selectThemeColorBtn.setText(self.tr("选取颜色"))
        self.alwaysRunAsAdministratorTitle.setText(self.tr("总是以管理员身份运行"))
        self.currentVerTitle.setText(self.tr("当前版本："))
        self.currentVerLabel.setText(MCSL2VERSION)
        self.checkUpdateBtn.setText(self.tr("检查更新"))
        self.checkUpdateOnStartTitle.setText(self.tr("启动时自动检查更新"))
        self.updateSettingsTitle.setText(self.tr("更新"))
        self.generateSysReport.setText(self.tr("系统报告"))
        self.sponsorsBtn.setText(self.tr("赞助者名单"))
        self.aboutContent.setText(
            self.tr("MCSL2是一个开源非营利性项目，遵循GNU General Public License Version 3.0开源协议。\n")
            + self.tr("任何人皆可使用MCSL2的源码进行再编译、修改以及发行，\n")
            + self.tr("但必须在相关源代码中以及软件中给出声明，并且二次分发版本的项目名称应与“MCSL2”有\n")
            + self.tr("明显辨识度。\n")
            + self.tr("\n")
            + self.tr("Copyright ©MCSL Team. All right reserved.\n")
            + self.tr("")
        )
        self.aboutTitle.setText(self.tr("关于"))
        self.aria2ThreadSlider.setValue(8)
        self.newServerTypeComboBox.addItems([self.tr("初始（简易+进阶+导入）"), self.tr("简易模式"), self.tr("进阶模式"), self.tr("导入")])
        self.newServerTypeComboBox.setCurrentIndex(0)
        self.downloadSourceComboBox.addItems([self.tr("FastMirror"), self.tr("MCSLAPI")])
        self.downloadSourceComboBox.setCurrentIndex(0)
        self.aria2ThreadNum.setText(str(self.aria2ThreadSlider.value()))
        self.aria2ThreadSlider.valueChanged.connect(
            lambda: self.aria2ThreadNum.setText(str(self.aria2ThreadSlider.value()))
        )
        self.outputDeEncodingComboBox.addItems([self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI(推荐)")])
        self.outputDeEncodingComboBox.setCurrentIndex(0)
        self.inputDeEncodingComboBox.addItems([self.tr("跟随控制台输出"), self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI(推荐)")])
        self.inputDeEncodingComboBox.setCurrentIndex(0)
        self.themeComboBox.addItems([self.tr("自动"), self.tr("深色"), self.tr("浅色")])
        self.saveBtn.setText(self.tr("保存"))
        self.giveUpBtn.setText(self.tr("放弃"))
        self.saveSettingsBtnWidget.setVisible(False)
        self.clearAllNewServerConfigInProgramTitle.setText(self.tr("*(强迫症)新建服务器后立刻清空相关设置项"))
        self.clearConsoleWhenStopServerTitle.setText(self.tr("*(强迫症)关闭服务器后立刻清空终端"))

        self.alwaysAskSaveDirectoryCheckBox.setEnabled(False)
        self.alwaysRunAsAdministratorSwitchBtn.setEnabled(False)
        self.startOnStartupSwitchBtn.setEnabled(False)

        self.checkUpdateBtn.setIcon(FIF.UPDATE)
        self.generateSysReport.setIcon(FIF.COPY)
        self.sponsorsBtn.setIcon(FIF.PEOPLE)
        self.disconn()
        self.conn()
        self.isChanged = 0

    @pyqtSlot(int)
    def onPageChangedRefresh(self, currentChanged):
        if currentChanged == 6:
            self.initReal()
        else:
            try:
                self.disconn()
                self.isChanged = 2
                self.verticalLayout.removeItem(self.spacerItem31)
                self.about.deleteLater()
                self.updateSettings.deleteLater()
                self.softwareSettings.deleteLater()
                self.consoleSettings.deleteLater()
                self.downloadSettings.deleteLater()
                self.configureSettings.deleteLater()
                self.serverSettings.deleteLater()
                # self.verticalLayout.deleteLater()
                # self.settingsSmoothScrollArea.verticalScrollBar().deleteLater()
            except Exception:
                pass
            MCSL2Logger.info("性能优化：释放设置页内存")

    def conn(self):
        # serverSettings
        self.autoRunLastServerSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "autoRunLastServer", self.autoRunLastServerSwitchBtn.isChecked()
            )
        )
        self.acceptAllMojangEulaSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "acceptAllMojangEula", self.acceptAllMojangEulaSwitchBtn.isChecked()
            )
        )
        self.sendStopInsteadOfKillSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "sendStopInsteadOfKill", self.sendStopInsteadOfKillSwitchBtn.isChecked()
            )
        )
        self.restartServerWhenCrashedSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "restartServerWhenCrashed",
                self.restartServerWhenCrashedSwitchBtn.isChecked(),
            )
        )

        # configureSettings
        self.newServerTypeComboBox.currentIndexChanged.connect(
            lambda: self.changeSettings(
                "newServerType",
                settingsVariables.newServerTypeList[
                    self.newServerTypeComboBox.currentIndex()
                ],
            )
        )
        self.onlySaveGlobalServerConfigSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "onlySaveGlobalServerConfig",
                self.onlySaveGlobalServerConfigSwitchBtn.isChecked(),
            )
        )
        self.clearAllNewServerConfigInProgramSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "clearAllNewServerConfigInProgram",
                self.clearAllNewServerConfigInProgramSwitchBtn.isChecked(),
            )
        )

        # downloadSettings
        self.downloadSourceComboBox.currentIndexChanged.connect(
            lambda: self.changeSettings(
                "downloadSource",
                settingsVariables.downloadSourceList[
                    self.downloadSourceComboBox.currentIndex()
                ],
            )
        )
        self.alwaysAskSaveDirectoryCheckBox.clicked.connect(
            lambda: self.changeSettings(
                "alwaysAskSaveDirectory",
                self.alwaysAskSaveDirectoryCheckBox.isChecked(),
            )
        )
        self.aria2ThreadSlider.valueChanged.connect(
            lambda: self.changeSettings("aria2Thread", self.aria2ThreadSlider.value())
        )
        self.saveSameFileExceptionToAsk.clicked.connect(
            lambda: self.changeSettings(
                "saveSameFileException", settingsVariables.saveSameFileExceptionList[0]
            )
        )
        self.saveSameFileExceptionToOverwrite.clicked.connect(
            lambda: self.changeSettings(
                "saveSameFileException", settingsVariables.saveSameFileExceptionList[1]
            )
        )
        self.saveSameFileExceptionToStop.clicked.connect(
            lambda: self.changeSettings(
                "saveSameFileException", settingsVariables.saveSameFileExceptionList[2]
            )
        )

        # consoleSettings
        self.outputDeEncodingComboBox.currentIndexChanged.connect(
            lambda: self.changeSettings(
                "outputDeEncoding",
                settingsVariables.outputDeEncodingList[
                    self.outputDeEncodingComboBox.currentIndex()
                ],
            )
        )
        self.inputDeEncodingComboBox.currentIndexChanged.connect(
            lambda: self.changeSettings(
                "inputDeEncoding",
                settingsVariables.inputDeEncodingList[
                    self.inputDeEncodingComboBox.currentIndex()
                ],
            )
        )
        self.quickMenuSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "quickMenu", self.quickMenuSwitchBtn.isChecked()
            )
        )
        self.quickMenuSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "quickMenu", self.quickMenuSwitchBtn.isChecked()
            )
        )
        self.clearConsoleWhenStopServerSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "clearConsoleWhenStopServer",
                self.clearConsoleWhenStopServerSwitchBtn.isChecked(),
            )
        )

        # softwareSettings
        self.themeComboBox.currentIndexChanged.connect(
            lambda: self.changeSettings(
                "theme", settingsVariables.themeList[self.themeComboBox.currentIndex()]
            )
        )
        self.selectThemeColorBtn.colorChanged.connect(
            lambda: self.changeSettings(
                "themeColor", str(self.selectThemeColorBtn.color.name())
            )
        )
        self.alwaysRunAsAdministratorSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "alwaysRunAsAdministrator",
                self.alwaysRunAsAdministratorSwitchBtn.isChecked(),
            )
        )
        self.startOnStartupSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "startOnStartup", self.startOnStartupSwitchBtn.isChecked()
            )
        )

        # updateSettings
        self.checkUpdateOnStartSwitchBtn.checkedChanged.connect(
            lambda: self.changeSettings(
                "checkUpdateOnStart", self.checkUpdateOnStartSwitchBtn.isChecked()
            )
        )

        self.selectThemeColorBtn.colorChanged.connect(setThemeColor)

        self.checkUpdateBtn.clicked.connect(lambda: self.checkUpdate(parent=self))

        self.generateSysReport.clicked.connect(self.generateSystemReport)
        self.refreshSettingsInterface()

    def disconn(self):
        try:
            # serverSettings
            self.autoRunLastServerSwitchBtn.checkedChanged.disconnect()
            self.acceptAllMojangEulaSwitchBtn.checkedChanged.disconnect()
            self.sendStopInsteadOfKillSwitchBtn.checkedChanged.disconnect()
            self.restartServerWhenCrashedSwitchBtn.checkedChanged.disconnect()

            # configureSettings
            self.newServerTypeComboBox.currentIndexChanged.disconnect()
            self.onlySaveGlobalServerConfigSwitchBtn.checkedChanged.disconnect()
            self.clearAllNewServerConfigInProgramSwitchBtn.checkedChanged.disconnect()

            # downloadSettings
            self.downloadSourceComboBox.currentIndexChanged.disconnect()
            self.alwaysAskSaveDirectoryCheckBox.clicked.disconnect()
            self.aria2ThreadSlider.valueChanged.disconnect()
            self.saveSameFileExceptionToAsk.clicked.disconnect()
            self.saveSameFileExceptionToOverwrite.clicked.disconnect()
            self.saveSameFileExceptionToStop.clicked.disconnect()

            # consoleSettings
            self.outputDeEncodingComboBox.currentIndexChanged.disconnect()
            self.inputDeEncodingComboBox.currentIndexChanged.disconnect()
            self.quickMenuSwitchBtn.checkedChanged.disconnect()
            self.quickMenuSwitchBtn.checkedChanged.disconnect()
            self.clearConsoleWhenStopServerSwitchBtn.checkedChanged.disconnect()

            # softwareSettings
            self.themeComboBox.currentIndexChanged.disconnect()
            self.selectThemeColorBtn.colorChanged.disconnect()
            self.alwaysRunAsAdministratorSwitchBtn.checkedChanged.disconnect()
            self.startOnStartupSwitchBtn.checkedChanged.disconnect()

            # updateSettings
            self.checkUpdateOnStartSwitchBtn.checkedChanged.disconnect()

            self.selectThemeColorBtn.colorChanged.disconnect()
            
            self.checkUpdateBtn.clicked.disconnect()

            self.generateSysReport.clicked.disconnect()
        except TypeError:
            pass
        except RuntimeError:
            pass

    def readSettings(self, firstLoad):
        """
        (此处为了保证拓展性而移植)\n
        重新将文件中的配置强制覆盖到程序中，不管是否保存了
        """
        settingsController._readSettings(firstLoad)

    def changeSettings(self, Setting: str, Status: Union[bool, str, int]):
        """
        更改设置触发器。\n
        会将更改后的设置临时保存但不写入文件
        """
        settingsController._changeSettings({Setting: Status})
        self.settingsChanged.emit(
            settingsController.unSavedSettings != settingsController.fileSettings
        )
        MCSL2Logger.info(f"修改设置：{str({Setting: Status})}")

    def giveUpSettings(self):
        """放弃所有未保存的设置"""
        self.refreshSettingsInterface()
        settingsController._giveUpSettings()
        self.settingsChanged.emit(False)
        MCSL2Logger.info("放弃了设置更改")

    def saveSettings(self):
        """保存设置"""
        settingsController._saveSettings()
        self.refreshSettingsInterface()
        self.settingsChanged.emit(False)
        InfoBar.success(
            title=self.tr("已保存"),
            content=self.tr("部分设置需要重启生效。"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self,
        )
        MCSL2Logger.info("保存设置到文件")

    def refreshSettingsInterface(self):
        """刷新设置页"""
        self.readSettings(firstLoad=False)

        # serverSettings
        self.autoRunLastServerSwitchBtn.setChecked(
            settingsController.fileSettings["autoRunLastServer"]
        )
        self.acceptAllMojangEulaSwitchBtn.setChecked(
            settingsController.fileSettings["acceptAllMojangEula"]
        )
        self.sendStopInsteadOfKillSwitchBtn.setChecked(
            settingsController.fileSettings["sendStopInsteadOfKill"]
        )
        self.restartServerWhenCrashedSwitchBtn.setChecked(
            settingsController.fileSettings["restartServerWhenCrashed"]
        )

        # configureSettings
        self.newServerTypeComboBox.setCurrentIndex(
            settingsVariables.newServerTypeList.index(
                settingsController.fileSettings["newServerType"]
            )
        )
        self.onlySaveGlobalServerConfigSwitchBtn.setChecked(
            settingsController.fileSettings["onlySaveGlobalServerConfig"]
        )
        self.clearAllNewServerConfigInProgramSwitchBtn.setChecked(
            settingsController.fileSettings["clearAllNewServerConfigInProgram"]
        )

        # downloadSettings
        self.downloadSourceComboBox.setCurrentIndex(
            settingsVariables.downloadSourceList.index(
                settingsController.fileSettings["downloadSource"]
            )
        )
        self.alwaysAskSaveDirectoryCheckBox.setChecked(
            settingsController.fileSettings["alwaysAskSaveDirectory"]
        )
        self.aria2ThreadSlider.setValue(settingsController.fileSettings["aria2Thread"])
        self.saveSameFileExceptionRadioBtnList = [
            self.saveSameFileExceptionToAsk,
            self.saveSameFileExceptionToOverwrite,
            self.saveSameFileExceptionToStop,
        ]
        self.saveSameFileExceptionRadioBtnList[
            settingsVariables.saveSameFileExceptionList.index(
                settingsController.fileSettings["saveSameFileException"]
            )
        ].setChecked(True)

        # consoleSettings
        self.outputDeEncodingComboBox.setCurrentIndex(
            settingsVariables.outputDeEncodingList.index(
                settingsController.fileSettings["outputDeEncoding"]
            )
        )
        self.inputDeEncodingComboBox.setCurrentIndex(
            settingsVariables.inputDeEncodingList.index(
                settingsController.fileSettings["inputDeEncoding"]
            )
        )
        self.quickMenuSwitchBtn.setChecked(settingsController.fileSettings["quickMenu"])
        self.clearConsoleWhenStopServerSwitchBtn.setChecked(
            settingsController.fileSettings["clearConsoleWhenStopServer"]
        )

        # softwareSettings
        self.themeComboBox.setCurrentIndex(
            settingsVariables.themeList.index(settingsController.fileSettings["theme"])
        )
        self.selectThemeColorBtn.setColor(settingsController.fileSettings["themeColor"])
        self.alwaysRunAsAdministratorSwitchBtn.setChecked(
            settingsController.fileSettings["alwaysRunAsAdministrator"]
        )
        self.startOnStartupSwitchBtn.setChecked(
            settingsController.fileSettings["startOnStartup"]
        )

        # updateSettings
        self.checkUpdateOnStartSwitchBtn.setChecked(
            settingsController.fileSettings["checkUpdateOnStart"]
        )

    def checkUpdate(self, parent):
        """
        检查更新触发器\n
        返回：\n
        1.是否需要更新\n
            1为需要\n
            0为不需要\n
            -1出错\n
        2.新版更新链接\n
        3.新版更新介绍\n
        """
        self.checkUpdateBtn.setEnabled(False)  # 防止爆炸
        if parent != self:
            title = self.tr("触发自定义设置-开始检查更新...")
        else:
            title = self.tr("开始检查更新...")
        InfoBar.info(
            title=title,
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=parent,
        )
        self.tmpParent = parent
        self.thread_checkUpdate = CheckUpdateThread(self)
        self.thread_checkUpdate.isUpdate.connect(self.showUpdateMsg)
        self.thread_checkUpdate.start()

    @pyqtSlot(list)
    def showUpdateMsg(self, latestVerInfo):
        """如果需要更新，显示弹窗；不需要则弹出提示"""
        if latestVerInfo[0] == "true":  # 需要更新
            title = self.tr("发现新版本：") + latestVerInfo[4]
            w = MessageBox(title, self.tr("更新介绍加载中..."), parent=self.tmpParent)
            w.contentLabel.setTextFormat(Qt.MarkdownText)
            w.yesButton.setText(self.tr("更新"))
            w.cancelButton.setText(self.tr("关闭"))
            self.thread_fetchUpdateIntro = FetchUpdateIntroThread(self)
            self.thread_fetchUpdateIntro.content.connect(w.contentLabel.setText)
            self.thread_fetchUpdateIntro.start()
            w.yesSignal.connect(lambda: self.window().switchTo(self))
            w.yesSignal.connect(MCSL2FileUpdater(self).downloadUpdate)
            w.exec()
        elif latestVerInfo[0] == "false":  # 已是最新版
            InfoBar.success(
                title=self.tr("无需更新"),
                content=self.tr("已是最新版本"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2500,
                parent=self.tmpParent,
            )
        else:
            InfoBar.error(
                title=self.tr("检查更新失败"),
                content=self.tr("尝试自己检查一下网络？"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2500,
                parent=self.tmpParent,
            )

        self.checkUpdateBtn.setEnabled(True)

    def generateSystemReport(self):
        """创建系统报告"""
        InfoBar.info(
            title=self.tr("开始生成系统报告..."),
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=1500,
            parent=self,
        )
        report = (
            self.tr("MCSL2系统报告：\n")
            + self.tr("生成时间：")
            + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            + "\n"
            + genSysReport()
        )

        title = self.tr("MC Server Launcher 2系统报告")
        w = MessageBox(
            title, report + self.tr("\n----------------------------\n点击复制按钮以复制到剪贴板。"), self
        )
        w.yesButton.setText(self.tr("复制"))
        w.cancelButton.setText(self.tr("关闭"))
        w.yesSignal.connect(lambda: QApplication.clipboard().setText(report))
        w.yesSignal.connect(
            lambda: InfoBar.success(
                title=self.tr("成功"),
                content=self.tr("已复制到剪贴板"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2500,
                parent=self,
            )
        )
        w.exec()

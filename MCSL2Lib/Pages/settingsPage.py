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

from PyQt5.QtCore import QSize, Qt, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSizePolicy,
    QSpacerItem,
    QFrame,
    QAbstractScrollArea,
    QVBoxLayout,
    QApplication,
)
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    HyperlinkButton,
    PrimaryPushButton,
    StrongBodyLabel,
    TitleLabel,
    setTheme,
    CustomColorSettingCard,
    SwitchSettingCard,
    OptionsSettingCard,
    SettingCardGroup,
    ComboBoxSettingCard,
    PrimaryPushSettingCard,
    RangeSettingCard,
    MessageBox,
    InfoBarPosition,
    InfoBar,
    FluentIcon as FIF,
    setThemeColor,
)

from MCSL2Lib import MCSL2VERSION
from MCSL2Lib.Controllers.aria2ClientController import Aria2BootThread, Aria2Controller
from MCSL2Lib.Controllers.settingsController import cfg
from MCSL2Lib.Controllers.updateController import (
    CheckUpdateThread,
    MCSL2FileUpdater,
    cmpVersion,
)
from MCSL2Lib.Controllers.logController import genSysReport
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import GlobalMCSL2Variables, SettingsVariables
from MCSL2Lib.Controllers.interfaceController import MySmoothScrollArea
from MCSL2Lib.verification import generateUniqueCode

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

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLimitWidget.sizePolicy().hasHeightForWidth())
        self.titleLimitWidget.setSizePolicy(sizePolicy)

        self.gridLayout_2 = QGridLayout(self.titleLimitWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_3.addWidget(self.titleLimitWidget)

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
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.gridLayout_2.addWidget(self.subTitleLabel, 2, 0, 1, 1)
        self.setObjectName("settingInterface")

        self.settingsWidget = MySmoothScrollArea(self)
        self.settingsWidget.setFrameShape(QFrame.NoFrame)
        self.settingsWidget.setFrameShadow(QFrame.Plain)
        self.settingsWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.settingsWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.settingsWidget.setWidgetResizable(True)
        self.settingsWidget.setObjectName("settingsSmoothScrollArea")

        self.settingsScrollAreaWidgetContents = QWidget()
        self.settingsScrollAreaWidgetContents.setGeometry(QRect(0, 0, 653, 1625))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.settingsScrollAreaWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.settingsScrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.settingsScrollAreaWidgetContents.setObjectName("settingsScrollAreaWidgetContents")

        self.settingsLayout = QVBoxLayout(self.settingsScrollAreaWidgetContents)
        self.settingsLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsLayout.setObjectName("settingsLayout")

        # Server
        self.serverSettingsGroup = SettingCardGroup(self.tr("服务器设置"), self.settingsWidget)
        self.autoRunLastServer = SwitchSettingCard(
            icon=FIF.ROBOT,
            title=self.tr("自动开服"),
            content=self.tr("启动MCSL2时自动运行上次运行的服务器。"),
            configItem=cfg.autoRunLastServer,
            parent=self.serverSettingsGroup,
        )
        self.acceptAllMojangEula = SwitchSettingCard(
            icon=FIF.ACCEPT,
            title=self.tr("自动同意EULA"),
            content=self.tr("创建时自动同意服务器的Minecraft Eula。"),
            configItem=cfg.acceptAllMojangEula,
            parent=self.serverSettingsGroup,
        )
        self.sendStopInsteadOfKill = SwitchSettingCard(
            icon=FIF.VPN,
            title=self.tr("安全关闭服务器"),
            content=self.tr('向服务器发送"stop"以安全地关闭服务器。'),
            configItem=cfg.sendStopInsteadOfKill,
            parent=self.serverSettingsGroup,
        )
        self.restartServerWhenCrashed = SwitchSettingCard(
            icon=FIF.HISTORY,
            title=self.tr("崩溃自动重启"),
            content=self.tr("自动重启非正常关闭的服务器。"),
            configItem=cfg.restartServerWhenCrashed,
            parent=self.serverSettingsGroup,
        )
        self.serverSettingsGroup.addSettingCard(self.autoRunLastServer)
        self.serverSettingsGroup.addSettingCard(self.acceptAllMojangEula)
        self.serverSettingsGroup.addSettingCard(self.sendStopInsteadOfKill)
        self.serverSettingsGroup.addSettingCard(self.restartServerWhenCrashed)
        self.settingsLayout.addWidget(self.serverSettingsGroup)

        # Configure server
        self.configureServerSettingsGroup = SettingCardGroup(
            self.tr("新建服务器设置"), self.settingsWidget
        )
        self.newServerType = ComboBoxSettingCard(
            configItem=cfg.newServerType,
            icon=FIF.FILTER,
            title=self.tr("新建服务器引导方式"),
            content=self.tr("有三种方式供你选择。"),
            texts=[
                self.tr("初始（简易+进阶+导入）"),
                self.tr("简易模式"),
                self.tr("进阶模式"),
                self.tr("导入"),
            ],
            parent=self.configureServerSettingsGroup,
        )
        self.onlySaveGlobalServerConfig = SwitchSettingCard(
            icon=FIF.PASTE,
            title=self.tr("只保存全局服务器设置"),
            content=self.tr("这可能会导致迁移服务器有些许麻烦。"),
            configItem=cfg.onlySaveGlobalServerConfig,
            parent=self.configureServerSettingsGroup,
        )
        self.clearAllNewServerConfigInProgram = SwitchSettingCard(
            icon=FIF.REMOVE_FROM,
            title=self.tr("新建服务器后立刻清空相关设置项"),
            content=self.tr("强迫症患者福音啊，好好好。"),
            configItem=cfg.clearAllNewServerConfigInProgram,
            parent=self.configureServerSettingsGroup,
        )
        self.configureServerSettingsGroup.addSettingCard(self.newServerType)
        self.configureServerSettingsGroup.addSettingCard(self.onlySaveGlobalServerConfig)
        self.configureServerSettingsGroup.addSettingCard(self.clearAllNewServerConfigInProgram)
        self.settingsLayout.addWidget(self.configureServerSettingsGroup)

        # Download
        self.downloadSettingsGroup = SettingCardGroup(self.tr("下载设置"), self.settingsWidget)
        self.downloadSource = OptionsSettingCard(
            configItem=cfg.downloadSource,
            icon=FIF.IOT,
            title=self.tr("下载源"),
            content=self.tr("随你所好。"),
            texts=[
                self.tr("FastMirror镜像站"),
                self.tr("MCSLAPI"),
                self.tr("极星·镜像站"),
                self.tr("Akira Cloud镜像站"),
            ],
            parent=self.downloadSettingsGroup,
        )
        self.alwaysAskSaveDirectory = SwitchSettingCard(
            icon=FIF.CHAT,
            title=self.tr("总是询问保存路径"),
            content=self.tr("不勾选则保存到MCSL2/Downloads文件夹。"),
            configItem=cfg.alwaysAskSaveDirectory,
            parent=self.downloadSettingsGroup,
        )
        self.aria2Thread = RangeSettingCard(
            configItem=cfg.aria2Thread,
            icon=FIF.SPEED_HIGH,
            title=self.tr("Aria2下载引擎线程数"),
            content=self.tr("太高可不好哦。"),
            parent=self.downloadSettingsGroup,
        )
        self.saveSameFileException = OptionsSettingCard(
            configItem=cfg.saveSameFileException,
            icon=FIF.SAVE_COPY,
            title=self.tr("保存路径存在同名文件的处理"),
            content=self.tr("省事又高效。"),
            texts=[self.tr("询问"), self.tr("覆盖"), self.tr("停止")],
            parent=self.downloadSettingsGroup,
        )
        self.alwaysAskSaveDirectory.setEnabled(False)
        self.aria2Thread.valueChanged.connect(self.restartAria2)
        self.downloadSettingsGroup.addSettingCard(self.downloadSource)
        self.downloadSettingsGroup.addSettingCard(self.alwaysAskSaveDirectory)
        self.downloadSettingsGroup.addSettingCard(self.aria2Thread)
        self.downloadSettingsGroup.addSettingCard(self.saveSameFileException)
        self.settingsLayout.addWidget(self.downloadSettingsGroup)

        # Console
        self.consoleSettingsGroup = SettingCardGroup(self.tr("终端设置"), self.settingsWidget)
        self.outputDeEncoding = ComboBoxSettingCard(
            configItem=cfg.outputDeEncoding,
            icon=FIF.CODE,
            title=self.tr("控制台输出编码"),
            content=self.tr("优先级低于服务器配置设置。"),
            texts=[self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI(推荐)")],
            parent=self.consoleSettingsGroup,
        )
        self.inputDeEncoding = ComboBoxSettingCard(
            configItem=cfg.inputDeEncoding,
            icon=FIF.CODE,
            title=self.tr("指令输入编码"),
            content=self.tr("优先级低于服务器配置设置。"),
            texts=[
                self.tr("跟随控制台输出"),
                self.tr("UTF-8"),
                self.tr("GB18030"),
                self.tr("ANSI(推荐)"),
            ],
            parent=self.consoleSettingsGroup,
        )
        self.quickMenu = SwitchSettingCard(
            icon=FIF.LAYOUT,
            title=self.tr("快捷菜单"),
            content=self.tr("特色功能！"),
            configItem=cfg.quickMenu,
            parent=self.consoleSettingsGroup,
        )
        self.clearConsoleWhenStopServer = SwitchSettingCard(
            icon=FIF.REMOVE_FROM,
            title=self.tr("关闭服务器后立刻清空终端"),
            content=self.tr("强迫症患者福音啊，好好好。"),
            configItem=cfg.clearConsoleWhenStopServer,
            parent=self.consoleSettingsGroup,
        )
        self.consoleSettingsGroup.addSettingCard(self.outputDeEncoding)
        self.consoleSettingsGroup.addSettingCard(self.inputDeEncoding)
        self.consoleSettingsGroup.addSettingCard(self.quickMenu)
        self.consoleSettingsGroup.addSettingCard(self.clearConsoleWhenStopServer)
        self.settingsLayout.addWidget(self.consoleSettingsGroup)

        # Software
        self.programSettingsGroup = SettingCardGroup("程序设置", self.settingsWidget)
        self.themeMode = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            title="主题",
            content="本程序也要花里胡哨捏~",
            texts=["浅色", "深色", "跟随系统"],
            parent=self.programSettingsGroup,
        )
        self.themeColor = CustomColorSettingCard(
            configItem=cfg.themeColor,
            icon=FIF.PALETTE,
            title="主题色",
            content="本程序也要花里胡哨捏~",
            parent=self.programSettingsGroup,
        )
        self.alwaysRunAsAdministrator = SwitchSettingCard(
            icon=FIF.PEOPLE,
            title=self.tr("总是以管理员身份运行"),
            content=self.tr("好像还做不到啊，我也不推荐。"),
            configItem=cfg.alwaysRunAsAdministrator,
            parent=self.consoleSettingsGroup,
        )
        self.startOnStartup = SwitchSettingCard(
            icon=FIF.POWER_BUTTON,
            title=self.tr("开机自启动"),
            content=self.tr("好像还做不到啊。"),
            configItem=cfg.startOnStartup,
            parent=self.consoleSettingsGroup,
        )
        self.alwaysRunAsAdministrator.setEnabled(False)
        self.startOnStartup.setEnabled(False)
        self.themeColor.colorChanged.connect(setThemeColor)
        self.themeMode.optionChanged.connect(lambda ci: setTheme(cfg.get(ci)))
        # self.themeMode.optionChanged.connect(self.showNeedRestartMsg)
        self.programSettingsGroup.addSettingCard(self.themeMode)
        self.programSettingsGroup.addSettingCard(self.themeColor)
        self.programSettingsGroup.addSettingCard(self.alwaysRunAsAdministrator)
        self.programSettingsGroup.addSettingCard(self.startOnStartup)
        self.settingsLayout.addWidget(self.programSettingsGroup)

        # Update
        self.updateSettingsGroup = SettingCardGroup("更新设置", self.settingsWidget)
        self.checkUpdateSetting = PrimaryPushSettingCard(
            icon=FIF.SYNC,
            text=self.tr("检查更新"),
            title=self.tr("检查更新"),
            content=self.tr("当前版本：") + MCSL2VERSION,
            parent=self.updateSettingsGroup,
        )
        self.checkUpdateOnStart = SwitchSettingCard(
            icon=FIF.SPEED_MEDIUM,
            title=self.tr("启动时自动检查更新"),
            content=self.tr("可确保你的MCSL2最新。"),
            configItem=cfg.checkUpdateOnStart,
            parent=self.consoleSettingsGroup,
        )
        self.checkUpdateSetting.clicked.connect(lambda: self.checkUpdate(parent=self))
        self.updateSettingsGroup.addSettingCard(self.checkUpdateSetting)
        self.updateSettingsGroup.addSettingCard(self.checkUpdateOnStart)
        self.settingsLayout.addWidget(self.updateSettingsGroup)

        # Other
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
        sizePolicy.setHeightForWidth(self.aboutContentWidget.sizePolicy().hasHeightForWidth())
        self.aboutContentWidget.setSizePolicy(sizePolicy)
        self.aboutContentWidget.setObjectName("aboutContentWidget")

        self.gridLayout = QGridLayout(self.aboutContentWidget)
        self.gridLayout.setObjectName("gridLayout")

        self.openOfficialWeb = HyperlinkButton(
            "https://mcsl.com.cn", "打开官网", self.aboutContentWidget, FIF.HOME
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openOfficialWeb.sizePolicy().hasHeightForWidth())
        self.openOfficialWeb.setSizePolicy(sizePolicy)
        self.openOfficialWeb.setObjectName("openOfficialWeb")

        self.gridLayout.addWidget(self.openOfficialWeb, 1, 1, 1, 1)
        self.openSourceCodeRepo = HyperlinkButton(
            "https://www.github.com/MCSLTeam/MCSL2",
            "打开源码仓库",
            self.aboutContentWidget,
            FIF.GITHUB,
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openSourceCodeRepo.sizePolicy().hasHeightForWidth())
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
            FIF.HELP,
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.joinQQGroup.sizePolicy().hasHeightForWidth())
        self.joinQQGroup.setSizePolicy(sizePolicy)
        self.joinQQGroup.setObjectName("joinQQGroup")

        self.gridLayout.addWidget(self.joinQQGroup, 1, 0, 1, 1)
        self.generateSysReport = PrimaryPushButton(
            icon=FIF.DICTIONARY, text="系统报告", parent=self.aboutContentWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generateSysReport.sizePolicy().hasHeightForWidth())
        self.generateSysReport.setSizePolicy(sizePolicy)
        self.generateSysReport.setObjectName("generateSysReport")

        self.gridLayout.addWidget(self.generateSysReport, 1, 5, 1, 1)
        self.uniqueCodeBtn = PrimaryPushButton(icon=FIF.PASTE, text="复制识别码", parent=self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uniqueCodeBtn.sizePolicy().hasHeightForWidth())
        self.uniqueCodeBtn.setSizePolicy(sizePolicy)
        self.uniqueCodeBtn.setObjectName("uniqueCodeBtn")

        self.gridLayout.addWidget(self.uniqueCodeBtn, 1, 6, 1, 1)
        spacerItem30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem30, 1, 6, 1, 2)
        self.sponsorsBtn = HyperlinkButton(
            "https://github.com/MCSLTeam/MCSL2/blob/master/Sponsors.md",
            "赞助者列表",
            self.aboutContentWidget,
            FIF.PEOPLE,
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sponsorsBtn.sizePolicy().hasHeightForWidth())
        self.sponsorsBtn.setSizePolicy(sizePolicy)
        self.sponsorsBtn.setObjectName("sponsorsBtn")

        self.donateBtn = HyperlinkButton(
            "https://afdian.net/a/MCSLTeam",
            "赞助此项目",
            self.aboutContentWidget,
            FIF.CAFE,
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.donateBtn.sizePolicy().hasHeightForWidth())
        self.donateBtn.setSizePolicy(sizePolicy)
        self.donateBtn.setObjectName("donateBtn")

        self.gridLayout.addWidget(self.sponsorsBtn, 1, 3, 1, 1)
        self.gridLayout.addWidget(self.donateBtn, 1, 4, 1, 1)
        self.gridLayout_5.addWidget(self.aboutContentWidget, 2, 0, 1, 4)
        self.aboutIndicator = PrimaryPushButton(self.about)
        self.aboutIndicator.setFixedSize(QSize(3, 20))
        self.aboutIndicator.setObjectName("aboutIndicator")

        self.gridLayout_5.addWidget(self.aboutIndicator, 0, 1, 1, 1)
        self.aboutTitle = StrongBodyLabel(self.about)
        self.aboutTitle.setObjectName("aboutTitle")

        self.gridLayout_5.addWidget(self.aboutTitle, 0, 2, 1, 1)
        self.settingsLayout.addWidget(self.about)
        # self.spacerItem31 = QSpacerItem(
        #     20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        # )
        # self.settingsLayout.addItem(self.spacerItem31)
        self.settingsWidget.setWidget(self.settingsScrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.settingsWidget, 2, 1, 1, 1)

        self.titleLabel.setText(self.tr("设置"))
        self.subTitleLabel.setText(self.tr("自定义你的MCSL2。"))
        self.aboutContent.setText(
            self.tr(
                "MCSL2是一个开源非营利性项目，遵循GNU General Public License Version 3.0开源协议。\n"
            )
            + self.tr("任何人皆可使用MCSL2的源码进行再编译、修改以及发行，\n")
            + self.tr(
                "但必须在相关源代码中以及软件中给出声明，并且二次分发版本的项目名称应与“MCSL2”有\n"
            )
            + self.tr("明显辨识度。\n")
            + self.tr("\n")
            + self.tr("Copyright ©MCSL Team. All right reserved.\n")
            + self.tr("")
        )
        self.aboutTitle.setText(self.tr("关于"))
        self.generateSysReport.clicked.connect(self.generateSystemReport)
        self.uniqueCodeBtn.clicked.connect(self.copyUniqueCode)

    def copyUniqueCode(self):
        QApplication.clipboard().setText(generateUniqueCode())
        InfoBar.success(
            title=self.tr("已复制"),
            content=self.tr("妥善保存，请勿泄露。"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self,
        )

    def showNeedRestartMsg(self):
        InfoBar.success(
            title=self.tr("已修改"),
            content=self.tr("该配置将在重启MCSL2后生效"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self,
        )

    def restartAria2(self):
        Aria2Controller.shutDown()
        bootThread = Aria2BootThread(self)
        bootThread.loaded.connect(self.onAria2Reloaded)
        bootThread.finished.connect(bootThread.deleteLater)
        bootThread.start()

    @pyqtSlot(bool)
    def onAria2Reloaded(self, flag: bool):
        if flag:
            InfoBar.success(
                title=self.tr("Aria2下载引擎重启成功。"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        else:
            InfoBar.error(
                title=self.tr("Aria2下载引擎重启失败"),
                content=self.tr("请检查是否安装了Aria2。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
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
        self.checkUpdateSetting.button.setEnabled(False)  # 防止爆炸
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

    @pyqtSlot(dict)
    def showUpdateMsg(self, latestVerInfo):
        """如果需要更新，显示弹窗；不需要则弹出提示"""
        if not len(latestVerInfo["latest"]):
            InfoBar.error(
                title=self.tr("检查更新失败"),
                content=self.tr("尝试自己检查一下网络？"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2500,
                parent=self.tmpParent,
            )
            self.checkUpdateSetting.button.setEnabled(True)
            return
        if cmpVersion(latestVerInfo["latest"]):
            title = self.tr("发现新版本：") + latestVerInfo["latest"]
            w = MessageBox(title, latestVerInfo["update-log"], parent=self.tmpParent)
            w.contentLabel.setTextFormat(Qt.MarkdownText)
            w.yesButton.setText(self.tr("更新"))
            w.cancelButton.setText(self.tr("关闭"))
            if not GlobalMCSL2Variables.devMode:
                w.yesSignal.connect(lambda: self.window().switchTo(self))
                w.yesSignal.connect(MCSL2FileUpdater(self).downloadUpdate)
            else:
                w.yesSignal.connect(
                    lambda: InfoBar.error(
                        title=self.tr("不行"),
                        content=self.tr("开发过程中更新会把你Python删掉的"),
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        duration=2500,
                        parent=self.tmpParent,
                    )
                )
            w.exec()
        else:
            InfoBar.success(
                title=self.tr("无需更新"),
                content=self.tr("已是最新版本"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2500,
                parent=self.tmpParent,
            )

        self.checkUpdateSetting.button.setEnabled(True)

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
            + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            + "\n"
            + genSysReport()
        )

        title = self.tr("MC Server Launcher 2系统报告")
        w = MessageBox(
            title,
            report + self.tr("\n----------------------------\n点击复制按钮以复制到剪贴板。"),
            self,
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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QApplication

from qfluentwidgets import (
    NavigationBar, 
    NavigationItemPosition, 
    isDarkTheme,
    FluentIcon as FIF,
    Theme,
    setTheme,
    setThemeColor
)
from qframelesswindow import FramelessWindow, TitleBar

from MCSL2Lib.interfaceController import StackedWidget
from MCSL2Lib.configurePage import _ConfigurePage
from MCSL2Lib.downloadPage import _DownloadPage
from MCSL2Lib.homePage import _HomePage
from MCSL2Lib.variables import MCSL2Version
from MCSL2Lib.icons import *  # noqa: F401

# 标题栏
class CustomTitleBar(TitleBar):

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # 图标
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 20)
        self.hBoxLayout.insertWidget(
            1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # 标题
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(
            2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))

    def resizeEvent(self, e):
        pass

# 窗口
class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        setTheme(Theme.DARK)

        setThemeColor('#0078d4')

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self.stackWidget = StackedWidget(self)

        # 定义子页面
        HomePage = _HomePage()
        ConfigurePage = _ConfigurePage()
        DownloadPage = _DownloadPage()
        self.homeInterface = HomePage
        self.configureInterface = ConfigurePage
        self.downloadInterface = DownloadPage

        # 初始化布局
        self.initLayout()

        # 初始化导航栏
        self.initNavigation()

        self.initWindow()

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationBar)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME,
                             '主页', selectedIcon=FIF.HOME_FILL)
        self.addSubInterface(self.configureInterface, FIF.ADD_TO, '新建')
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, '下载')
        # self.addSubInterface(self.consoleInterface, FIF.ALIGNMENT, '终端')
        # self.addSubInterface(self.pluginsInterface, FIF.APPLICATION, '插件')
        # self.addSubInterface(self.settingsInterface,
        #                      FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.navigationBar.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(765, 620)
        self.setWindowIcon(QIcon(':/MCSL2_Icon/MCSL2_Icon.png'))
        self.setWindowTitle(f'MCSL {MCSL2Version}')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, selectedIcon=None):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationBar.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            selectedIcon=selectedIcon,
            position=position,
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationBar.setCurrentItem(widget.objectName())
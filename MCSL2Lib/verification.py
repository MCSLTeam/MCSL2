#     Copyright 2024, MCSL Team, mailto:lxhtt@vip.qq.com
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
import sys
from qfluentwidgets import (
    MessageBox,
    InfoBar,
    FluentWindow,
    InfoBarPosition,
)
from MCSL2Lib.ProgramControllers.networkController import MCSLNetworkSession
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, pyqtSignal
from os import getlogin, name as osname, getenv
from platform import system as sysType, processor
from hashlib import md5

from MCSL2Lib.utils import openWebUrl


class VerifyFluentWindowBase(FluentWindow):
    passSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.testNotPassFlag = True
        self.testVerifyBox = MessageBox(
            "提示",
            "这是一个内部测试版本，请确保你有内测权限，不要试图绕过此验证。本程序内测资格一机一码。\n(提示：参加本程序内测为完全自愿行为，不收取任何费用)",
            parent=self,
        )
        self.testVerifyBox.cancelButton.clicked.connect(sys.exit)
        self.testVerifyBox.yesButton.clicked.disconnect()
        self.testVerifyBox.yesButton.clicked.connect(self.checkTestPassword)
        self.testVerifyBox.cancelButton.setText("退出程序")
        self.testVerifyBox.yesButton.setText("验证内测权限")
        self.testVerifyBox.hide()

    def checkTestPassword(self):
        self.testVerifyBox.hide()  # type: ignore
        if checkPreviewPermission():
            self.testVerifyBox.show()  # type: ignore
            self.testVerifyBox.close()  # type: ignore
            try:
                self.testVerifyBox.deleteLater()  # type: ignore
                self.testVerifyBox = None
            except Exception:
                pass
            self.testNotPassFlag = bool(self.testVerifyBox is not None)
            self.navigationInterface.setEnabled(True)
            self.stackedWidget.setEnabled(True)
            InfoBar.success(
                title="提示",
                content="验证成功",
                duration=2000,
                position=InfoBarPosition.TOP,
                parent=self,
            )
            self.passSignal.emit()
        else:
            timer = QTimer(self)
            timer.timeout.connect(self.testVerifyBox.cancelButton.click)  # type: ignore
            self.testVerifyBox.show()  # type: ignore
            self.testVerifyBox.contentLabel.setText(  # type: ignore
                f"你并没有内测资格。请先使用你的识别码请求内测权限。\n(点击下方按钮复制识别码并前往资格申请页面)：\n\n{generateUniqueCode()}\n"
            )
            self.testVerifyBox.yesButton.clicked.disconnect()  # type: ignore
            self.testVerifyBox.yesButton.setText("点击复制")  # type: ignore
            self.testVerifyBox.yesButton.clicked.connect(  # type: ignore
                lambda: QApplication.clipboard().setText(generateUniqueCode())
            )
            self.testVerifyBox.yesButton.clicked.connect(  # type: ignore
                lambda: self.testVerifyBox.yesButton.setText("已复制  √")  # type: ignore
            )
            self.testVerifyBox.yesButton.clicked.connect(  # type: ignore
                lambda: openWebUrl("https://mcsl.com.cn/join-preview.html")
            )
            self.testVerifyBox.yesButton.clicked.connect(  # type: ignore
                lambda: self.testVerifyBox.yesButton.setEnabled(False)  # type: ignore
            )
            self.testVerifyBox.yesButton.clicked.connect(  # type: ignore
                lambda: self.testVerifyBox.contentLabel.setText(  # type: ignore
                    f"你并没有内测资格。请联系分发测试版的开发组人员，并提供以下识别码(点击下方按钮复制)：\n\n{generateUniqueCode()}\n\n已复制，程序即将退出。"
                )
            )
            self.testVerifyBox.yesButton.clicked.connect(lambda: timer.start(1000))  # type: ignore

    def switchTo(self, interface: QWidget):
        if self.testNotPassFlag:
            timer = QTimer(self)
            timer.timeout.connect(sys.exit)
            timer.start(2000)
            for i in range(0, 11):
                InfoBar.error(
                    title="警告",
                    content="你绕过了测试版本验证器。程序即将退出。",
                    duration=-1,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                    parent=self,
                )
                InfoBar.error(
                    title="警告",
                    content="你绕过了测试版本验证器。程序即将退出。",
                    duration=-1,
                    isClosable=False,
                    position=InfoBarPosition.TOP_LEFT,
                    parent=self,
                )
                InfoBar.error(
                    title="警告",
                    content="你绕过了测试版本验证器。程序即将退出。",
                    duration=-1,
                    isClosable=False,
                    position=InfoBarPosition.TOP_RIGHT,
                    parent=self,
                )
        else:
            return super().switchTo(interface)


def getAnnouncement():
    header = __AuthorizationHeaders.copy()
    header.update(MCSLNetworkSession.MCSLNetworkHeaders)
    return MCSLNetworkSession().get("https://api.mcsl.com.cn/getAnnouncement", headers=header).text


def checkUpdate():
    header = __AuthorizationHeaders.copy()
    header.update(MCSLNetworkSession.MCSLNetworkHeaders)
    return MCSLNetworkSession().get("https://api.mcsl.com.cn/checkUpdate", headers=header).json()


def countUserAPI():
    header = __AuthorizationHeaders.copy()
    header.update(MCSLNetworkSession.MCSLNetworkHeaders)
    return (
        MCSLNetworkSession()
        .post(
            f"https://api.mcsl.com.cn/countUser?Identification={generateUniqueCode()}",
            headers=header,
        )
        .text
    )


def checkPreviewPermission():
    return (
        MCSLNetworkSession()
        .get(
            f"https://api.mcsl.com.cn/checkPreviewAvailable?Identification={generateUniqueCode()}",
            headers=MCSLNetworkSession.MCSLNetworkHeaders,
        )
        .json()["available"]
    )


# fmt: off
def generateUniqueCode():
    return "-".join([md5(f"{getlogin() if osname == 'nt' else getenv('USER')}{processor()}{sysType()}".encode()).hexdigest()[i:i + 4].upper() for i in range(0, 16, 4)])  # noqa: E501
# fmt: on


__AuthorizationHeaders = {
    "x-mcsl2-client-private-header": "8f528e4214fe0142c301f0b92a7abea204a309fe5149f783765e9ab287c08367"  # noqa: E501
}

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
Sponsor Widget.
"""
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap
from qfluentwidgets import BodyLabel, HyperlinkLabel, ImageLabel, SubtitleLabel
from MCSL2Lib.Resources.sponsorsImage import *  # noqa: F401

class MCSL2Sponsors(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(340, 330))

        self.gridLayout = QGridLayout(self)

        self.shuaibao = HyperlinkLabel(self)
        self.shuaibao.setUrl(
            QUrl("https://afdian.net/u/55c079ea268611eb9a4852540025c377")
        )
        self.gridLayout.addWidget(self.shuaibao, 3, 4, 1, 1)

        self.shuaibaoImage = ImageLabel(self)
        self.shuaibaoImage.setPixmap(QPixmap(":/MCSL2_Sponsors/shuaibao.png"))
        self.gridLayout.addWidget(self.shuaibaoImage, 4, 4, 1, 1)

        self.skwImage = ImageLabel(self)
        self.skwImage.setPixmap(QPixmap(":/MCSL2_Sponsors/skw.jpg"))
        self.gridLayout.addWidget(self.skwImage, 6, 0, 1, 1)

        spacerItem = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 3, 4, 1)

        self.pgPINGImage = ImageLabel(self)
        self.pgPINGImage.setPixmap(QPixmap(":/MCSL2_Sponsors/pgPING.jpg"))
        self.gridLayout.addWidget(self.pgPINGImage, 4, 0, 1, 1)

        self.pgPING = HyperlinkLabel(self)
        self.pgPING.setUrl(QUrl("https://afdian.net/a/PingGai"))
        self.gridLayout.addWidget(self.pgPING, 3, 0, 1, 1)

        self.washtileImage = ImageLabel(self)
        self.washtileImage.setPixmap(QPixmap(":/MCSL2_Sponsors/washtile.jpg"))
        self.gridLayout.addWidget(self.washtileImage, 6, 2, 1, 1)

        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 1, 4, 1)

        self.thanksLabel = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thanksLabel.sizePolicy().hasHeightForWidth())
        self.thanksLabel.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.thanksLabel, 1, 0, 1, 6)

        self.afdTitle = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.afdTitle.sizePolicy().hasHeightForWidth())
        self.afdTitle.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.afdTitle, 0, 0, 1, 6)

        self.qqysqImage = ImageLabel(self)
        self.qqysqImage.setPixmap(QPixmap(":/MCSL2_Sponsors/qqysq.jpg"))
        self.gridLayout.addWidget(self.qqysqImage, 4, 2, 1, 1)

        self.qqysq = HyperlinkLabel(self)
        self.qqysq.setUrl(QUrl("https://afdian.net/a/yaosiqian"))
        self.gridLayout.addWidget(self.qqysq, 3, 2, 1, 1)

        self.skw = HyperlinkLabel(self)
        self.skw.setUrl(QUrl("https://afdian.net/a/skwstudios"))
        self.gridLayout.addWidget(self.skw, 5, 0, 1, 1)

        self.washtile = HyperlinkLabel(self)
        self.washtile.setUrl(QUrl("https://afdian.net/a/XZQAQ"))
        self.gridLayout.addWidget(self.washtile, 5, 2, 1, 1)

        self.shuaibao.setText("帅宝")
        self.pgPING.setText("瓶盖PING")
        self.thanksLabel.setText("非常感谢你们对MCSL2开发的鼓励与支持！")
        self.afdTitle.setText("爱发电 - 8月赞助者名单")
        self.qqysq.setText("谦谦yaosiqian")
        self.skw.setText("SKWStudios")
        self.washtile.setText("Washtile645")

        self.shuaibaoImage.setFixedSize(QSize(72, 72))
        self.skwImage.setFixedSize(QSize(72, 72))
        self.pgPINGImage.setFixedSize(QSize(72, 72))
        self.washtileImage.setFixedSize(QSize(72, 72))
        self.qqysqImage.setFixedSize(QSize(72, 72))
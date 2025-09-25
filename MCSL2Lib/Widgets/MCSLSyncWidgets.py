#     Copyright 2024, MCSL Team, mailto:services@mcsl.com.cn
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
MCSL-Sync Download Widgets.
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QWidget, QVBoxLayout
from qfluentwidgets import (
    CardWidget,
    StrongBodyLabel,
    PrimaryToolButton,
    FluentIcon as FIF,
    ToggleButton,
    BodyLabel,
)


class MCSLSyncVersionButton(ToggleButton):
    """MC版本按钮"""
    def __init__(self, version, slot, parent=None):
        super().__init__(parent)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(140, 45))
        self.setText(version)
        self.clicked.connect(slot)
        self.setProperty("version", version)


class MCSLSyncCorePushButton(ToggleButton):
    """核心类型按钮"""
    def __init__(self, core_name, slot, parent=None):
        super().__init__(parent)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(150, 45))
        self.setText(core_name)
        self.setProperty("core_name", core_name)
        self.clicked.connect(slot)


class MCSLSyncBuildListWidget(CardWidget):
    """构建列表Widget"""
    def __init__(self, build_name, sync_time, download_url, btnSlot, parent=None):
        super().__init__(parent)

        self.setObjectName("buildListWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(284, 85))
        self.setMaximumSize(QSize(16777215, 85))
        
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(15, 10, 15, 10)
        
        # 构建信息区域
        self.infoWidget = QWidget(self)
        self.infoWidget.setObjectName("infoWidget")
        self.infoLayout = QVBoxLayout(self.infoWidget)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.setSpacing(4)
        
        # 构建名称（主要信息）
        self.buildNameLabel = StrongBodyLabel(self.infoWidget)
        self.buildNameLabel.setObjectName("buildNameLabel")
        self.buildNameLabel.setText(build_name)
        self.infoLayout.addWidget(self.buildNameLabel)
        
        # 同步时间（次要信息）
        self.syncTimeLabel = BodyLabel(self.infoWidget)
        self.syncTimeLabel.setObjectName("syncTimeLabel")
        self.syncTimeLabel.setText(f"同步时间: {sync_time}")
        self.syncTimeLabel.setStyleSheet("color: #666666;")
        self.infoLayout.addWidget(self.syncTimeLabel)
        
        # 下载状态标签（可选）
        self.statusLabel = BodyLabel(self.infoWidget)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setText("可下载")
        self.statusLabel.setStyleSheet("color: #10B981; font-size: 12px;")
        self.infoLayout.addWidget(self.statusLabel)
        
        self.horizontalLayout.addWidget(self.infoWidget)
        
        # 下载按钮
        self.downloadBtn = PrimaryToolButton(FIF.CLOUD_DOWNLOAD, self)
        self.downloadBtn.setFixedSize(QSize(50, 50))
        self.downloadBtn.setObjectName("downloadBtn")
        self.downloadBtn.setToolTip(f"下载 {build_name}")
        self.horizontalLayout.addWidget(self.downloadBtn)

        # 设置按钮属性和连接
        self.downloadBtn.clicked.connect(btnSlot)
        self.downloadBtn.setProperty("download_url", download_url)
        self.downloadBtn.setProperty("build_name", build_name)
        
        # 验证下载链接
        if not download_url or download_url == "":
            self.downloadBtn.setEnabled(False)
            self.statusLabel.setText("暂不可用")
            self.statusLabel.setStyleSheet("color: #EF4444; font-size: 12px;")
            self.downloadBtn.setToolTip("下载链接不可用")

    def setDownloadStatus(self, status):
        """设置下载状态"""
        status_styles = {
            "available": ("可下载", "#10B981"),
            "downloading": ("下载中", "#F59E0B"),
            "completed": ("已完成", "#6B7280"),
            "failed": ("下载失败", "#EF4444"),
            "unavailable": ("暂不可用", "#EF4444")
        }
        
        if status in status_styles:
            text, color = status_styles[status]
            self.statusLabel.setText(text)
            self.statusLabel.setStyleSheet(f"color: {color}; font-size: 12px;")
            
            # 根据状态调整按钮
            if status in ["downloading", "completed", "unavailable"]:
                self.downloadBtn.setEnabled(False)
            else:
                self.downloadBtn.setEnabled(True)
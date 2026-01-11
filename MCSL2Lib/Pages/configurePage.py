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
Configure new server page.
"""

import os
import shutil
from json import loads, dumps
from os import getcwd, mkdir, remove, path as osp
import platform
from shutil import copy, rmtree
from typing import List, Optional
from zipfile import ZipFile

from PyQt5.QtCore import Qt, QSize, QRect, pyqtSlot, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QHBoxLayout,
    QFrame,
    QFileDialog,
    QStackedWidget,
)
from qfluentwidgets import (
    ComboBox,
    LineEdit,
    PlainTextEdit,
    PrimaryPushButton,
    PushButton,
    StrongBodyLabel,
    SubtitleLabel,
    TitleLabel,
    TransparentToolButton,
    FluentIcon as FIF,
    Dialog,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    HyperlinkButton,
    StateToolTip,
    HeaderCardWidget,
    CardWidget,
)

from MCSL2Lib.ProgramControllers import javaDetector
from MCSL2Lib.ProgramControllers.interfaceController import ChildStackedWidget
from MCSL2Lib.ProgramControllers.interfaceController import MySmoothScrollArea
from MCSL2Lib.ProgramControllers.serverValidator import ServerValidator
from MCSL2Lib.ProgramControllers.settingsController import cfg
from MCSL2Lib.ServerControllers.processCreator import _MinecraftEULA
from MCSL2Lib.ServerControllers.serverInstaller import ForgeInstaller, NeoForgeInstaller
from MCSL2Lib.Widgets.DownloadEntryViewerWidget import DownloadEntryBox
from MCSL2Lib.Widgets.ForgeInstaller.DownloadView import ForgeInstallerDownloadView
from MCSL2Lib.Widgets.ForgeInstaller.ForgeInstallProgressWidget import ForgeInstallerProgressBox
from MCSL2Lib.Widgets.exceptionWidget import ExceptionWidget
from MCSL2Lib.Widgets.importServerWidgets import (
    ImportPageWidget,
    ConfirmArgumentsWidget,
    ImportFileFolderWidget,
    ImportSingleWidget,
    MyListWidget,
    MyTreeWidget,
    SaveWidget,
)
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.utils import MCSL2Logger, readFile, writeFile
from MCSL2Lib.variables import (
    ConfigureServerVariables,
    ServerVariables,
    SettingsVariables,
)

configureServerVariables = ConfigureServerVariables()
settingsVariables = SettingsVariables()
serverVariables = ServerVariables()


class ExtractModpackThread(QThread):
    """解压整合包并检测jar文件的后台线程"""

    success = pyqtSignal(str, list)  # serverPath, jarFiles
    failed = pyqtSignal(str)

    def __init__(self, zip_file: str, server_path: str, parent=None):
        super().__init__(parent)
        self.zip_file = zip_file
        self.server_path = server_path

    def run(self):
        try:
            # 解压整合包
            with ZipFile(self.zip_file, "r") as zip_ref:
                zip_ref.extractall(self.server_path)

            # 检查是否只有一个子目录(常见的整合包结构)
            dirs = [
                d
                for d in os.listdir(self.server_path)
                if os.path.isdir(os.path.join(self.server_path, d))
            ]
            if (
                len(dirs) == 1
                and len([
                    f
                    for f in os.listdir(self.server_path)
                    if os.path.isfile(os.path.join(self.server_path, f))
                ])
                == 0
            ):
                # 如果只有一个子目录且没有其他文件，将其内容移到上层
                sub_dir = os.path.join(self.server_path, dirs[0])
                for item in os.listdir(sub_dir):
                    shutil.move(os.path.join(sub_dir, item), os.path.join(self.server_path, item))
                os.rmdir(sub_dir)

            # 检测jar文件
            jar_files = [
                f
                for f in os.listdir(self.server_path)
                if f.endswith(".jar") and os.path.isfile(os.path.join(self.server_path, f))
            ]

            self.success.emit(self.server_path, jar_files)
        except Exception as e:
            self.failed.emit(str(e))


class JavaServerSaveThread(QThread):
    """执行Java版服务器保存的后台线程"""

    success = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(
        self,
        server_config: dict,
        core_path: str,
        core_file_name: str,
        extra_data: dict,
        only_save_global: bool,
        auto_accept_eula: bool,
        exit0_msg: str,
        exit1_msg: str,
        exists_error_msg: str,
        parent=None,
    ):
        super().__init__(parent)
        self.server_config = server_config
        self.core_path = core_path
        self.core_file_name = core_file_name
        self.extra_data = extra_data or {}
        self.only_save_global = only_save_global
        self.auto_accept_eula = auto_accept_eula
        self.exit0_msg = exit0_msg
        self.exit1_msg = exit1_msg
        self.exists_error_msg = exists_error_msg

    def run(self):
        server_name = self.server_config["name"]
        folder_created = False
        global_config_written = False

        # 新建文件夹
        try:
            mkdir(f"./Servers/{server_name}")
            folder_created = True
        except FileExistsError:
            self.failed.emit(self.exists_error_msg)
            return
        except Exception as e:
            self.failed.emit(self.exit1_msg + f"\n{e}")
            return

        # 写入全局配置
        try:
            global_server_list = loads(readFile(r"MCSL2/MCSL2_ServerList.json"))
            global_server_list["MCSLServerList"].append(self.server_config)
            writeFile(r"MCSL2/MCSL2_ServerList.json", dumps(global_server_list, indent=4))
            global_config_written = True
        except Exception as e:
            # 回滚：删除已创建的文件夹
            if folder_created:
                try:
                    rmtree(f"./Servers/{server_name}")
                except:
                    pass
            self.failed.emit(self.exit1_msg + f"\n{e}")
            return

        # 写入单独配置
        try:
            if not self.only_save_global:
                writeFile(
                    f"./Servers/{server_name}/MCSL2ServerConfig.json",
                    dumps(self.server_config, indent=4),
                )
        except Exception as e:
            # 回滚：删除全局配置和文件夹
            if global_config_written:
                try:
                    global_server_list = loads(readFile(r"MCSL2/MCSL2_ServerList.json"))
                    # 找到刚添加的配置并删除
                    for i, srv in enumerate(global_server_list["MCSLServerList"]):
                        if srv["name"] == server_name:
                            global_server_list["MCSLServerList"].pop(i)
                            break
                    writeFile(r"MCSL2/MCSL2_ServerList.json", dumps(global_server_list, indent=4))
                except:
                    pass
            if folder_created:
                try:
                    rmtree(f"./Servers/{server_name}")
                except:
                    pass
            self.failed.emit(self.exit1_msg + f"\n{e}")
            return

        # 复制核心
        try:
            if self.extra_data.get("extracted_from_zip") and self.extra_data.get("temp_dir"):
                from shutil import copytree, rmtree
                import os

                temp_dir = self.extra_data["temp_dir"]
                target_dir = f"./Servers/{server_name}"

                for item in os.listdir(temp_dir):
                    src_path = os.path.join(temp_dir, item)
                    dst_path = os.path.join(target_dir, item)
                    if os.path.isdir(src_path):
                        copytree(src_path, dst_path, dirs_exist_ok=True)
                    else:
                        copy(src_path, dst_path)

                # 强制同步到磁盘
                try:
                    import subprocess

                    if os.name == "posix":  # Linux/Mac
                        subprocess.run(["sync"], check=False, timeout=5)
                except:
                    pass

                rmtree(temp_dir, ignore_errors=True)
            else:
                # 单文件复制
                copy(self.core_path, f"./Servers/{server_name}/{self.core_file_name}")
        except Exception as e:
            # 回滚：删除全局配置、单独配置和文件夹
            if global_config_written:
                try:
                    global_server_list = loads(readFile(r"MCSL2/MCSL2_ServerList.json"))
                    for i, srv in enumerate(global_server_list["MCSLServerList"]):
                        if srv["name"] == server_name:
                            global_server_list["MCSLServerList"].pop(i)
                            break
                    writeFile(r"MCSL2/MCSL2_ServerList.json", dumps(global_server_list, indent=4))
                except:
                    pass
            if folder_created:
                try:
                    rmtree(f"./Servers/{server_name}")
                except:
                    pass
            self.failed.emit(self.exit1_msg + f"\n{e}")
            return

        # 自动同意Mojang Eula
        if self.auto_accept_eula:
            try:
                _MinecraftEULA(server_name).acceptEula()
            except Exception as e:
                # Eula失败不影响服务器创建
                pass

        self.success.emit(self.exit0_msg)


class BedrockServerSaveThread(QThread):
    """执行基岩版服务器保存的后台线程"""

    success = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(
        self,
        server_config: dict,
        core_path: str,
        core_file_name: str,
        extra_data: dict,
        only_save_global: bool,
        exit0_msg: str,
        exit1_msg: str,
        exists_error_msg: str,
        parent=None,
    ):
        super().__init__(parent)
        self.server_config = server_config
        self.core_path = core_path
        self.core_file_name = core_file_name
        self.extra_data = extra_data or {}
        self.only_save_global = only_save_global
        self.exit0_msg = exit0_msg
        self.exit1_msg = exit1_msg
        self.exists_error_msg = exists_error_msg

    def run(self):
        server_name = self.server_config["name"]

        try:
            mkdir(f"./Servers/{server_name}")
        except FileExistsError:
            self.failed.emit(self.exists_error_msg)
            return
        except Exception as e:
            self.failed.emit(self.exit1_msg + f"\n{e}")
            return

        try:
            global_server_list = loads(readFile(r"MCSL2/MCSL2_ServerList.json"))
            global_server_list["MCSLServerList"].append(self.server_config)
            writeFile(r"MCSL2/MCSL2_ServerList.json", dumps(global_server_list, indent=4))
        except Exception as e:
            self.failed.emit(self.exit1_msg + f"\n{e}")
            return

        try:
            if not self.only_save_global:
                writeFile(
                    f"./Servers/{server_name}/MCSL2ServerConfig.json",
                    dumps(self.server_config, indent=4),
                )
        except Exception as e:
            self.failed.emit(self.exit1_msg + f"\n{e}")
            return

        try:
            if self.extra_data.get("extracted_from_zip") and self.extra_data.get("temp_dir"):
                from shutil import copytree, rmtree
                import os

                temp_dir = self.extra_data["temp_dir"]
                target_dir = f"./Servers/{server_name}"

                for item in os.listdir(temp_dir):
                    src_path = os.path.join(temp_dir, item)
                    dst_path = os.path.join(target_dir, item)
                    if os.path.isdir(src_path):
                        copytree(src_path, dst_path, dirs_exist_ok=True)
                    else:
                        copy(src_path, dst_path)

                rmtree(temp_dir, ignore_errors=True)
            else:
                copy(self.core_path, f"./Servers/{server_name}/{self.core_file_name}")
        except Exception as e:
            self.failed.emit(self.exit1_msg + f"\n{e}")
            return

        self.success.emit(self.exit0_msg)


class BedrockCoreImportThread(QThread):
    """解析/解压基岩版核心的后台线程"""

    success = pyqtSignal(dict)
    failed = pyqtSignal(str)

    def __init__(self, file_path: str, system: str, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.system = system

    def run(self):
        try:
            path = self.file_path
            if path.lower().endswith(".zip"):
                from zipfile import ZipFile
                from tempfile import mkdtemp
                from shutil import rmtree
                import os
                import stat

                temp_dir = mkdtemp(prefix="mcsl2_bedrock_")
                with ZipFile(path, "r") as zip_ref:
                    zip_ref.extractall(temp_dir)

                bedrock_exe = None
                if self.system == "windows":
                    bedrock_exe = osp.join(temp_dir, "bedrock_server.exe")
                else:
                    bedrock_exe = osp.join(temp_dir, "bedrock_server")

                if not osp.exists(bedrock_exe):
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            if file == "bedrock_server.exe" or file == "bedrock_server":
                                bedrock_exe = osp.join(root, file)
                                break
                        if bedrock_exe and osp.exists(bedrock_exe):
                            break

                if not osp.exists(bedrock_exe):
                    rmtree(temp_dir, ignore_errors=True)
                    self.failed.emit("压缩包中未找到bedrock_server可执行文件！")
                    return

                if self.system != "windows":
                    os.chmod(bedrock_exe, os.stat(bedrock_exe).st_mode | stat.S_IEXEC)

                self.success.emit({
                    "core_path": temp_dir,
                    "core_file_name": osp.basename(bedrock_exe),
                    "extra_data": {
                        "edition": "bedrock",
                        "extracted_from_zip": True,
                        "temp_dir": temp_dir,
                    },
                })
            else:
                self.success.emit({
                    "core_path": path,
                    "core_file_name": osp.basename(path),
                    "extra_data": {"edition": "bedrock"},
                })
        except Exception as e:
            self.failed.emit(str(e))


class ServerTypeHeaderCardWidget(HeaderCardWidget):
    """服务器类型选择卡片基类"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.headerView.setFixedHeight(44)

        # 创建内容标签
        self.contentLabel = StrongBodyLabel(self)
        self.contentLabel.setWordWrap(True)
        self.viewLayout.addWidget(self.contentLabel)

        # 添加选择按钮
        self.selectButton = PrimaryPushButton(self.tr("选择"), self)
        self.selectButton.setFixedSize(QSize(100, 32))
        self.viewLayout.addWidget(self.selectButton)

    def connectSlot(self, slot):
        """连接按钮点击事件"""
        self.selectButton.clicked.connect(slot)


class NoobServerCardWidget(ServerTypeHeaderCardWidget):
    """简易模式卡片"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.tr("简易模式"))
        self.contentLabel.setText(self.tr("适合新手的简化配置流程"))
        self.selectButton.setIcon(FIF.GAME)


class ExtendedServerCardWidget(ServerTypeHeaderCardWidget):
    """进阶模式卡片"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.tr("进阶模式"))
        self.contentLabel.setText(self.tr("更多自定义选项和高级功能"))
        self.selectButton.setIcon(FIF.GAME)


class BedrockServerCardWidget(ServerTypeHeaderCardWidget):
    """基岩版卡片"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.tr("基岩版"))
        self.contentLabel.setText(self.tr("创建 Minecraft 基岩版服务器"))
        self.selectButton.setIcon(FIF.GAME)


class ImportServerCardWidget(ServerTypeHeaderCardWidget):
    """导入服务器卡片"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.tr("导入服务器"))
        self.contentLabel.setText(self.tr("导入整合包(Modpack)"))
        self.selectButton.setIcon(FIF.FOLDER_ADD)


@Singleton
class ConfigurePage(QWidget):
    """新建服务器页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.installerLogViewer = None
        self.installerDownloadView = None

        self.javaFindWorkThreadFactory = javaDetector.JavaFindWorkThreadFactory()
        self.javaFindWorkThreadFactory.fSearch = True
        self.javaFindWorkThreadFactory.signalConnect = self.autoDetectJavaFinished
        self.javaFindWorkThreadFactory.finishSignalConnect = self.onJavaFindWorkThreadFinished
        self.javaFindWorkThreadFactory.create().start()

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.titleLimitWidget = QWidget(self)
        self.titleLimitWidget.setObjectName("titleLimitWidget")

        self.verticalLayout = QVBoxLayout(self.titleLimitWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.titleLabel = TitleLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.subTitleLabel = StrongBodyLabel(self.titleLimitWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subTitleLabel.sizePolicy().hasHeightForWidth())
        self.subTitleLabel.setSizePolicy(sizePolicy)
        self.subTitleLabel.setTextFormat(Qt.MarkdownText)
        self.subTitleLabel.setObjectName("subTitleLabel")

        self.verticalLayout.addWidget(self.subTitleLabel)
        self.gridLayout.addWidget(self.titleLimitWidget, 1, 2, 1, 1)
        # spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        # self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.newServerStackedWidget = ChildStackedWidget(self)
        self.newServerStackedWidget.setObjectName("newServerStackedWidget")

        self.guideNewServerPage = QWidget()
        self.guideNewServerPage.setObjectName("guideNewServerPage")

        self.guideNewServerGridLayout = QGridLayout(self.guideNewServerPage)
        self.guideNewServerGridLayout.setObjectName("guideNewServerGridLayout")
        self.guideNewServerGridLayout.setSpacing(15)

        self.noobNewServerWidget = NoobServerCardWidget(self.guideNewServerPage)
        self.noobNewServerWidget.setObjectName("noobNewServerWidget")
        self.guideNewServerGridLayout.addWidget(self.noobNewServerWidget, 0, 0, 1, 1)

        self.extendedNewServerWidget = ExtendedServerCardWidget(self.guideNewServerPage)
        self.extendedNewServerWidget.setObjectName("extendedNewServerWidget")
        self.guideNewServerGridLayout.addWidget(self.extendedNewServerWidget, 0, 1, 1, 1)

        self.bedrockNewServerWidget = BedrockServerCardWidget(self.guideNewServerPage)
        self.bedrockNewServerWidget.setObjectName("bedrockNewServerWidget")
        self.guideNewServerGridLayout.addWidget(self.bedrockNewServerWidget, 1, 0, 1, 1)

        self.importNewServerWidget = ImportServerCardWidget(self.guideNewServerPage)
        self.importNewServerWidget.setObjectName("importNewServerWidget")
        self.guideNewServerGridLayout.addWidget(self.importNewServerWidget, 1, 1, 1, 1)

        self.newServerStackedWidget.addWidget(self.guideNewServerPage)
        self.noobNewServerPage = QWidget()
        self.noobNewServerPage.setObjectName("noobNewServerPage")

        self.noobNewServerGridLayout = QGridLayout(self.noobNewServerPage)
        self.noobNewServerGridLayout.setObjectName("noobNewServerGridLayout")

        self.noobNewServerScrollArea = MySmoothScrollArea(self.noobNewServerPage)
        self.noobNewServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.noobNewServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.noobNewServerScrollArea.setWidgetResizable(True)
        self.noobNewServerScrollArea.setObjectName("noobNewServerScrollArea")
        self.noobNewServerScrollArea.setFrameShape(QFrame.NoFrame)

        self.noobNewServerScrollAreaContents = QWidget()
        self.noobNewServerScrollAreaContents.setGeometry(QRect(0, -100, 586, 453))
        self.noobNewServerScrollAreaContents.setObjectName("noobNewServerScrollAreaContents")

        self.noobNewServerScrollAreaVerticalLayout = QVBoxLayout(
            self.noobNewServerScrollAreaContents
        )
        self.noobNewServerScrollAreaVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.noobNewServerScrollAreaVerticalLayout.setObjectName(
            "noobNewServerScrollAreaVerticalLayout"
        )

        self.noobSetJavaWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSetJavaWidget.sizePolicy().hasHeightForWidth())
        self.noobSetJavaWidget.setSizePolicy(sizePolicy)
        self.noobSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.noobSetJavaWidget.setObjectName("noobSetJavaWidget")

        self.gridLayout_3 = QGridLayout(self.noobSetJavaWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.noobJavaSubtitleLabel = SubtitleLabel(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobJavaSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.noobJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobJavaSubtitleLabel.setObjectName("noobJavaSubtitleLabel")

        self.gridLayout_3.addWidget(self.noobJavaSubtitleLabel, 0, 0, 1, 1)
        self.noobJavaInfoLabel = SubtitleLabel(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobJavaInfoLabel.sizePolicy().hasHeightForWidth())
        self.noobJavaInfoLabel.setSizePolicy(sizePolicy)
        self.noobJavaInfoLabel.setObjectName("noobJavaInfoLabel")

        self.gridLayout_3.addWidget(self.noobJavaInfoLabel, 0, 1, 1, 1)
        self.noobSetJavaBtnWidget = QWidget(self.noobSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSetJavaBtnWidget.sizePolicy().hasHeightForWidth())
        self.noobSetJavaBtnWidget.setSizePolicy(sizePolicy)
        self.noobSetJavaBtnWidget.setObjectName("noobSetJavaBtnWidget")

        self.horizontalLayout_6 = QHBoxLayout(self.noobSetJavaBtnWidget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.noobDownloadJavaPrimaryPushBtn = PrimaryPushButton(self.noobSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobDownloadJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobDownloadJavaPrimaryPushBtn.setObjectName("noobDownloadJavaPrimaryPushBtn")

        self.horizontalLayout_6.addWidget(self.noobDownloadJavaPrimaryPushBtn)
        self.noobManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(self.noobSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobManuallyAddJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobManuallyAddJavaPrimaryPushBtn.setObjectName("noobManuallyAddJavaPrimaryPushBtn")

        self.horizontalLayout_6.addWidget(self.noobManuallyAddJavaPrimaryPushBtn)
        self.noobAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(self.noobSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobAutoDetectJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobAutoDetectJavaPrimaryPushBtn.setObjectName("noobAutoDetectJavaPrimaryPushBtn")

        self.horizontalLayout_6.addWidget(self.noobAutoDetectJavaPrimaryPushBtn)
        self.noobJavaListPushBtn = PushButton(self.noobSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobJavaListPushBtn.sizePolicy().hasHeightForWidth())
        self.noobJavaListPushBtn.setSizePolicy(sizePolicy)
        self.noobJavaListPushBtn.setMinimumSize(QSize(90, 0))
        self.noobJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.noobJavaListPushBtn.setObjectName("noobJavaListPushBtn")

        self.horizontalLayout_6.addWidget(self.noobJavaListPushBtn)
        spacerItem4 = QSpacerItem(127, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.gridLayout_3.addWidget(self.noobSetJavaBtnWidget, 1, 0, 1, 2)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetJavaWidget)
        self.noobSetMemWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSetMemWidget.sizePolicy().hasHeightForWidth())
        self.noobSetMemWidget.setSizePolicy(sizePolicy)
        self.noobSetMemWidget.setObjectName("noobSetMemWidget")

        self.gridLayout_4 = QGridLayout(self.noobSetMemWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")

        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem5, 1, 5, 1, 1)
        self.noobMinMemLineEdit = LineEdit(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobMinMemLineEdit.sizePolicy().hasHeightForWidth())
        self.noobMinMemLineEdit.setSizePolicy(sizePolicy)
        self.noobMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noobMinMemLineEdit.setObjectName("noobMinMemLineEdit")

        self.gridLayout_4.addWidget(self.noobMinMemLineEdit, 1, 1, 1, 1)
        self.noobMemUnitLabel = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobMemUnitLabel.sizePolicy().hasHeightForWidth())
        self.noobMemUnitLabel.setSizePolicy(sizePolicy)
        self.noobMemUnitLabel.setObjectName("noobMemUnitLabel")

        self.gridLayout_4.addWidget(self.noobMemUnitLabel, 1, 4, 1, 1)
        self.noobMaxMemLineEdit = LineEdit(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobMaxMemLineEdit.sizePolicy().hasHeightForWidth())
        self.noobMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.noobMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.noobMaxMemLineEdit.setObjectName("noobMaxMemLineEdit")

        self.gridLayout_4.addWidget(self.noobMaxMemLineEdit, 1, 3, 1, 1)
        self.noobToSymbol = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobToSymbol.sizePolicy().hasHeightForWidth())
        self.noobToSymbol.setSizePolicy(sizePolicy)
        self.noobToSymbol.setObjectName("noobToSymbol")

        self.gridLayout_4.addWidget(self.noobToSymbol, 1, 2, 1, 1)
        self.noobMemSubtitleLabel = SubtitleLabel(self.noobSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobMemSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.noobMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobMemSubtitleLabel.setObjectName("noobMemSubtitleLabel")

        self.gridLayout_4.addWidget(self.noobMemSubtitleLabel, 0, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetMemWidget)
        self.noobSetCoreWidget = QWidget(self.noobNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSetCoreWidget.sizePolicy().hasHeightForWidth())
        self.noobSetCoreWidget.setSizePolicy(sizePolicy)
        self.noobSetCoreWidget.setObjectName("noobSetCoreWidget")

        self.gridLayout_5 = QGridLayout(self.noobSetCoreWidget)
        self.gridLayout_5.setObjectName("gridLayout_5")

        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem6, 1, 3, 1, 1)
        self.noobDownloadCorePrimaryPushBtn = PrimaryPushButton(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobDownloadCorePrimaryPushBtn.setObjectName("noobDownloadCorePrimaryPushBtn")

        self.gridLayout_5.addWidget(self.noobDownloadCorePrimaryPushBtn, 1, 2, 1, 1)
        self.noobManuallyAddCorePrimaryPushBtn = PrimaryPushButton(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobManuallyAddCorePrimaryPushBtn.setObjectName("noobManuallyAddCorePrimaryPushBtn")

        self.gridLayout_5.addWidget(self.noobManuallyAddCorePrimaryPushBtn, 1, 1, 1, 1)

        self.noobAddCoreFromDownloadedPrimaryPushBtn = PrimaryPushButton(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobAddCoreFromDownloadedPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobAddCoreFromDownloadedPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobAddCoreFromDownloadedPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.noobAddCoreFromDownloadedPrimaryPushBtn.setObjectName(
            "noobAddCoreFromDownloadedPrimaryPushBtn"
        )

        self.gridLayout_5.addWidget(self.noobAddCoreFromDownloadedPrimaryPushBtn, 1, 3, 1, 1)

        self.noobCoreSubtitleLabel = SubtitleLabel(self.noobSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobCoreSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.noobCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobCoreSubtitleLabel.setObjectName("noobCoreSubtitleLabel")

        self.gridLayout_5.addWidget(self.noobCoreSubtitleLabel, 0, 1, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetCoreWidget)
        self.noobSetServerNameWidget = QWidget(self.noobNewServerScrollAreaContents)
        self.noobSetServerNameWidget.setObjectName("noobSetServerNameWidget")

        self.verticalLayout_4 = QVBoxLayout(self.noobSetServerNameWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.noobServerNameSubtitleLabel = SubtitleLabel(self.noobSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobServerNameSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.noobServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobServerNameSubtitleLabel.setObjectName("noobServerNameSubtitleLabel")

        self.verticalLayout_4.addWidget(self.noobServerNameSubtitleLabel)
        self.noobServerNameLineEdit = LineEdit(self.noobSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobServerNameLineEdit.sizePolicy().hasHeightForWidth())
        self.noobServerNameLineEdit.setSizePolicy(sizePolicy)
        self.noobServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.noobServerNameLineEdit.setObjectName("noobServerNameLineEdit")

        self.verticalLayout_4.addWidget(self.noobServerNameLineEdit)
        self.noobSaveServerPrimaryPushBtn = PrimaryPushButton(self.noobSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noobSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.noobSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.noobSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.noobSaveServerPrimaryPushBtn.setObjectName("noobSaveServerPrimaryPushBtn")

        self.verticalLayout_4.addWidget(self.noobSaveServerPrimaryPushBtn)
        self.noobNewServerScrollAreaVerticalLayout.addWidget(self.noobSetServerNameWidget)
        spacerItem7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.noobNewServerScrollAreaVerticalLayout.addItem(spacerItem7)
        self.noobNewServerScrollArea.setWidget(self.noobNewServerScrollAreaContents)
        self.noobNewServerGridLayout.addWidget(self.noobNewServerScrollArea, 2, 2, 1, 1)
        self.noobTitleWidget = QWidget(self.noobNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobTitleWidget.sizePolicy().hasHeightForWidth())
        self.noobTitleWidget.setSizePolicy(sizePolicy)
        self.noobTitleWidget.setObjectName("noobTitleWidget")

        self.horizontalLayout_4 = QHBoxLayout(self.noobTitleWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.noobBackToGuidePushButton = TransparentToolButton(FIF.PAGE_LEFT, self.noobTitleWidget)
        self.noobBackToGuidePushButton.setObjectName("noobBackToGuidePushButton")

        self.horizontalLayout_4.addWidget(self.noobBackToGuidePushButton)
        self.noobSubtitleLabel = SubtitleLabel(self.noobTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noobSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.noobSubtitleLabel.setSizePolicy(sizePolicy)
        self.noobSubtitleLabel.setObjectName("noobSubtitleLabel")

        self.horizontalLayout_4.addWidget(self.noobSubtitleLabel)
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.noobNewServerGridLayout.addWidget(self.noobTitleWidget, 0, 1, 2, 2)
        spacerItem9 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.noobNewServerGridLayout.addItem(spacerItem9, 0, 0, 3, 1)
        self.newServerStackedWidget.addWidget(self.noobNewServerPage)

        self.extendedNewServerPage = QWidget()
        self.extendedNewServerPage.setObjectName("extendedNewServerPage")

        self.gridLayout_2 = QGridLayout(self.extendedNewServerPage)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.extendedTitleWidget = QWidget(self.extendedNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedTitleWidget.sizePolicy().hasHeightForWidth())
        self.extendedTitleWidget.setSizePolicy(sizePolicy)
        self.extendedTitleWidget.setObjectName("extendedTitleWidget")

        self.horizontalLayout_5 = QHBoxLayout(self.extendedTitleWidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.extendedBackToGuidePushButton = TransparentToolButton(
            FIF.PAGE_LEFT, self.extendedTitleWidget
        )
        self.extendedBackToGuidePushButton.setObjectName("extendedBackToGuidePushButton")

        self.horizontalLayout_5.addWidget(self.extendedBackToGuidePushButton)
        self.extendedSubtitleLabel = SubtitleLabel(self.extendedTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.extendedSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedSubtitleLabel.setObjectName("extendedSubtitleLabel")

        self.horizontalLayout_5.addWidget(self.extendedSubtitleLabel)
        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem10)
        self.gridLayout_2.addWidget(self.extendedTitleWidget, 0, 1, 1, 1)
        self.extendedNewServerScrollArea = MySmoothScrollArea(self.extendedNewServerPage)
        self.extendedNewServerScrollArea.setFrameShape(QFrame.NoFrame)
        self.extendedNewServerScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.extendedNewServerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.extendedNewServerScrollArea.setWidgetResizable(True)
        self.extendedNewServerScrollArea.setObjectName("extendedNewServerScrollArea")

        self.extendedNewServerScrollAreaContents = QWidget()
        self.extendedNewServerScrollAreaContents.setGeometry(QRect(0, 0, 594, 734))
        self.extendedNewServerScrollAreaContents.setObjectName(
            "extendedNewServerScrollAreaContents"
        )

        self.noobNewServerScrollAreaVerticalLayout_2 = QVBoxLayout(
            self.extendedNewServerScrollAreaContents
        )
        self.noobNewServerScrollAreaVerticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.noobNewServerScrollAreaVerticalLayout_2.setObjectName(
            "noobNewServerScrollAreaVerticalLayout_2"
        )

        self.extendedSetJavaWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSetJavaWidget.sizePolicy().hasHeightForWidth())
        self.extendedSetJavaWidget.setSizePolicy(sizePolicy)
        self.extendedSetJavaWidget.setMinimumSize(QSize(0, 120))
        self.extendedSetJavaWidget.setObjectName("extendedSetJavaWidget")

        self.gridLayout_6 = QGridLayout(self.extendedSetJavaWidget)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.extendedJavaSubtitleLabel = SubtitleLabel(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedJavaSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedJavaSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedJavaSubtitleLabel.setObjectName("extendedJavaSubtitleLabel")

        self.gridLayout_6.addWidget(self.extendedJavaSubtitleLabel, 0, 0, 1, 1)
        self.extendedJavaInfoLabel = SubtitleLabel(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedJavaInfoLabel.sizePolicy().hasHeightForWidth())
        self.extendedJavaInfoLabel.setSizePolicy(sizePolicy)
        self.extendedJavaInfoLabel.setObjectName("extendedJavaInfoLabel")

        self.gridLayout_6.addWidget(self.extendedJavaInfoLabel, 0, 1, 1, 1)
        self.extendedSetJavaBtnWidget = QWidget(self.extendedSetJavaWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSetJavaBtnWidget.sizePolicy().hasHeightForWidth())
        self.extendedSetJavaBtnWidget.setSizePolicy(sizePolicy)
        self.extendedSetJavaBtnWidget.setObjectName("extendedSetJavaBtnWidget")

        self.horizontalLayout_7 = QHBoxLayout(self.extendedSetJavaBtnWidget)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.extendedDownloadJavaPrimaryPushBtn = PrimaryPushButton(self.extendedSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedDownloadJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedDownloadJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedDownloadJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedDownloadJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.extendedDownloadJavaPrimaryPushBtn.setObjectName("extendedDownloadJavaPrimaryPushBtn")

        self.horizontalLayout_7.addWidget(self.extendedDownloadJavaPrimaryPushBtn)
        self.extendedManuallyAddJavaPrimaryPushBtn = PrimaryPushButton(
            self.extendedSetJavaBtnWidget
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedManuallyAddJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedManuallyAddJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedManuallyAddJavaPrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedManuallyAddJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.extendedManuallyAddJavaPrimaryPushBtn.setObjectName(
            "extendedManuallyAddJavaPrimaryPushBtn"
        )

        self.horizontalLayout_7.addWidget(self.extendedManuallyAddJavaPrimaryPushBtn)
        self.extendedAutoDetectJavaPrimaryPushBtn = PrimaryPushButton(self.extendedSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedAutoDetectJavaPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedAutoDetectJavaPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedAutoDetectJavaPrimaryPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.extendedAutoDetectJavaPrimaryPushBtn.setObjectName(
            "extendedAutoDetectJavaPrimaryPushBtn"
        )

        self.horizontalLayout_7.addWidget(self.extendedAutoDetectJavaPrimaryPushBtn)
        self.extendedJavaListPushBtn = PushButton(self.extendedSetJavaBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedJavaListPushBtn.sizePolicy().hasHeightForWidth())
        self.extendedJavaListPushBtn.setSizePolicy(sizePolicy)
        self.extendedJavaListPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedJavaListPushBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.extendedJavaListPushBtn.setObjectName("extendedJavaListPushBtn")

        self.horizontalLayout_7.addWidget(self.extendedJavaListPushBtn)
        spacerItem11 = QSpacerItem(127, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem11)
        self.gridLayout_6.addWidget(self.extendedSetJavaBtnWidget, 1, 0, 1, 2)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetJavaWidget)
        self.extendedSetMemWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSetMemWidget.sizePolicy().hasHeightForWidth())
        self.extendedSetMemWidget.setSizePolicy(sizePolicy)
        self.extendedSetMemWidget.setObjectName("extendedSetMemWidget")

        self.gridLayout_7 = QGridLayout(self.extendedSetMemWidget)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.extendedMinMemLineEdit = LineEdit(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedMinMemLineEdit.sizePolicy().hasHeightForWidth())
        self.extendedMinMemLineEdit.setSizePolicy(sizePolicy)
        self.extendedMinMemLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedMinMemLineEdit.setObjectName("extendedMinMemLineEdit")

        self.gridLayout_7.addWidget(self.extendedMinMemLineEdit, 1, 1, 1, 1)
        self.extendedMemSubtitleLabel = SubtitleLabel(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedMemSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.extendedMemSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedMemSubtitleLabel.setObjectName("extendedMemSubtitleLabel")

        self.gridLayout_7.addWidget(self.extendedMemSubtitleLabel, 0, 1, 1, 1)
        self.extendedMaxMemLineEdit = LineEdit(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedMaxMemLineEdit.sizePolicy().hasHeightForWidth())
        self.extendedMaxMemLineEdit.setSizePolicy(sizePolicy)
        self.extendedMaxMemLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedMaxMemLineEdit.setObjectName("extendedMaxMemLineEdit")

        self.gridLayout_7.addWidget(self.extendedMaxMemLineEdit, 1, 3, 1, 1)
        self.extendedToSymbol = SubtitleLabel(self.extendedSetMemWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedToSymbol.sizePolicy().hasHeightForWidth())
        self.extendedToSymbol.setSizePolicy(sizePolicy)
        self.extendedToSymbol.setObjectName("extendedToSymbol")

        self.gridLayout_7.addWidget(self.extendedToSymbol, 1, 2, 1, 1)
        spacerItem12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem12, 1, 5, 1, 1)
        self.extendedMemUnitComboBox = ComboBox(self.extendedSetMemWidget)
        self.extendedMemUnitComboBox.setObjectName("extendedMemUnitComboBox")

        self.gridLayout_7.addWidget(self.extendedMemUnitComboBox, 1, 4, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetMemWidget)
        self.extendedSetCoreWidget = QWidget(self.extendedNewServerScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extendedSetCoreWidget.sizePolicy().hasHeightForWidth())
        self.extendedSetCoreWidget.setSizePolicy(sizePolicy)
        self.extendedSetCoreWidget.setObjectName("extendedSetCoreWidget")

        self.gridLayout_8 = QGridLayout(self.extendedSetCoreWidget)
        self.gridLayout_8.setObjectName("gridLayout_8")

        spacerItem13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem13, 1, 3, 1, 1)
        self.extendedDownloadCorePrimaryPushBtn = PrimaryPushButton(self.extendedSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedDownloadCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedDownloadCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedDownloadCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedDownloadCorePrimaryPushBtn.setObjectName("extendedDownloadCorePrimaryPushBtn")

        self.gridLayout_8.addWidget(self.extendedDownloadCorePrimaryPushBtn, 1, 2, 1, 1)
        self.extendedManuallyAddCorePrimaryPushBtn = PrimaryPushButton(self.extendedSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(90, 0))
        self.extendedManuallyAddCorePrimaryPushBtn.setObjectName(
            "extendedManuallyAddCorePrimaryPushBtn"
        )

        self.gridLayout_8.addWidget(self.extendedManuallyAddCorePrimaryPushBtn, 1, 1, 1, 1)
        self.extendedCoreSubtitleLabel = SubtitleLabel(self.extendedSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedCoreSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedCoreSubtitleLabel.setObjectName("extendedCoreSubtitleLabel")

        self.gridLayout_8.addWidget(self.extendedCoreSubtitleLabel, 0, 1, 1, 1)
        self.extendedAddCoreFromDownloadedPrimaryPushBtn = PrimaryPushButton(
            self.extendedSetCoreWidget
        )
        self.extendedAddCoreFromDownloadedPrimaryPushBtn.setObjectName(
            "extendedAddCoreFromDownloadedPrimaryPushBtn"
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedAddCoreFromDownloadedPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedAddCoreFromDownloadedPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.gridLayout_8.addWidget(self.extendedAddCoreFromDownloadedPrimaryPushBtn, 1, 3, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetCoreWidget)
        self.extendedSetDeEncodingWidget = QWidget(self.extendedNewServerScrollAreaContents)
        self.extendedSetDeEncodingWidget.setObjectName("extendedSetDeEncodingWidget")

        self.gridLayout_9 = QGridLayout(self.extendedSetDeEncodingWidget)
        self.gridLayout_9.setObjectName("gridLayout_9")

        self.extendedOutputDeEncodingComboBox = ComboBox(self.extendedSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.extendedOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.extendedOutputDeEncodingComboBox.setObjectName("extendedOutputDeEncodingComboBox")

        self.gridLayout_9.addWidget(self.extendedOutputDeEncodingComboBox, 2, 1, 1, 1)
        self.extendedDeEncodingSubtitleLabel = SubtitleLabel(self.extendedSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedDeEncodingSubtitleLabel.setObjectName("extendedDeEncodingSubtitleLabel")

        self.gridLayout_9.addWidget(self.extendedDeEncodingSubtitleLabel, 0, 0, 1, 1)
        self.extendedInputDeEncodingComboBox = ComboBox(self.extendedSetDeEncodingWidget)
        self.extendedInputDeEncodingComboBox.setText("")
        self.extendedInputDeEncodingComboBox.setObjectName("extendedInputDeEncodingComboBox")

        self.gridLayout_9.addWidget(self.extendedInputDeEncodingComboBox, 3, 1, 1, 1)
        self.extendedOutputDeEncodingLabel = StrongBodyLabel(self.extendedSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.extendedOutputDeEncodingLabel.setObjectName("extendedOutputDeEncodingLabel")

        self.gridLayout_9.addWidget(self.extendedOutputDeEncodingLabel, 2, 0, 1, 1)
        self.extendedInputDeEncodingLabel = StrongBodyLabel(self.extendedSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.extendedInputDeEncodingLabel.setObjectName("extendedInputDeEncodingLabel")

        self.gridLayout_9.addWidget(self.extendedInputDeEncodingLabel, 3, 0, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetDeEncodingWidget)
        self.extendedSetJVMArgWidget = QWidget(self.extendedNewServerScrollAreaContents)
        self.extendedSetJVMArgWidget.setObjectName("extendedSetJVMArgWidget")

        self.gridLayout_10 = QGridLayout(self.extendedSetJVMArgWidget)
        self.gridLayout_10.setObjectName("gridLayout_10")

        self.extendedJVMArgSubtitleLabel = SubtitleLabel(self.extendedSetJVMArgWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedJVMArgSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedJVMArgSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedJVMArgSubtitleLabel.setObjectName("extendedJVMArgSubtitleLabel")

        self.gridLayout_10.addWidget(self.extendedJVMArgSubtitleLabel, 0, 0, 1, 1)
        self.JVMArgPlainTextEdit = PlainTextEdit(self.extendedSetJVMArgWidget)
        self.JVMArgPlainTextEdit.setObjectName("JVMArgPlainTextEdit")

        self.gridLayout_10.addWidget(self.JVMArgPlainTextEdit, 1, 0, 1, 1)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetJVMArgWidget)
        self.extendedSetServerNameWidget = QWidget(self.extendedNewServerScrollAreaContents)
        self.extendedSetServerNameWidget.setObjectName("extendedSetServerNameWidget")

        self.verticalLayout_5 = QVBoxLayout(self.extendedSetServerNameWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.extendedServerNameSubtitleLabel = SubtitleLabel(self.extendedSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedServerNameSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.extendedServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.extendedServerNameSubtitleLabel.setObjectName("extendedServerNameSubtitleLabel")

        self.verticalLayout_5.addWidget(self.extendedServerNameSubtitleLabel)
        self.extendedServerNameLineEdit = LineEdit(self.extendedSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.extendedServerNameLineEdit.setSizePolicy(sizePolicy)
        self.extendedServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.extendedServerNameLineEdit.setObjectName("extendedServerNameLineEdit")

        self.verticalLayout_5.addWidget(self.extendedServerNameLineEdit)
        self.extendedSaveServerPrimaryPushBtn = PrimaryPushButton(self.extendedSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extendedSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.extendedSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.extendedSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.extendedSaveServerPrimaryPushBtn.setObjectName("extendedSaveServerPrimaryPushBtn")

        self.verticalLayout_5.addWidget(self.extendedSaveServerPrimaryPushBtn)
        self.noobNewServerScrollAreaVerticalLayout_2.addWidget(self.extendedSetServerNameWidget)
        spacerItem14 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.noobNewServerScrollAreaVerticalLayout_2.addItem(spacerItem14)
        self.extendedNewServerScrollArea.setWidget(self.extendedNewServerScrollAreaContents)
        self.gridLayout_2.addWidget(self.extendedNewServerScrollArea, 1, 1, 1, 1)
        spacerItem15 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem15, 0, 0, 2, 1)
        self.newServerStackedWidget.addWidget(self.extendedNewServerPage)

        # ========== 基岩版服务器页面 ==========
        self.bedrockNewServerPage = QWidget()
        self.bedrockNewServerPage.setObjectName("bedrockNewServerPage")

        self.bedrockGridLayout = QGridLayout(self.bedrockNewServerPage)
        self.bedrockGridLayout.setObjectName("bedrockGridLayout")

        self.bedrockTitleWidget = QWidget(self.bedrockNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bedrockTitleWidget.sizePolicy().hasHeightForWidth())
        self.bedrockTitleWidget.setSizePolicy(sizePolicy)
        self.bedrockTitleWidget.setObjectName("bedrockTitleWidget")

        self.bedrockTitleHorizontalLayout = QHBoxLayout(self.bedrockTitleWidget)
        self.bedrockTitleHorizontalLayout.setObjectName("bedrockTitleHorizontalLayout")

        self.bedrockBackToGuidePushButton = TransparentToolButton(
            FIF.PAGE_LEFT, self.bedrockTitleWidget
        )
        self.bedrockBackToGuidePushButton.setObjectName("bedrockBackToGuidePushButton")
        self.bedrockTitleHorizontalLayout.addWidget(self.bedrockBackToGuidePushButton)

        self.bedrockSubtitleLabel = SubtitleLabel(self.bedrockTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bedrockSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.bedrockSubtitleLabel.setSizePolicy(sizePolicy)
        self.bedrockSubtitleLabel.setObjectName("bedrockSubtitleLabel")
        self.bedrockTitleHorizontalLayout.addWidget(self.bedrockSubtitleLabel)

        spacerItem_bedrock1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.bedrockTitleHorizontalLayout.addItem(spacerItem_bedrock1)
        self.bedrockGridLayout.addWidget(self.bedrockTitleWidget, 0, 1, 1, 1)

        self.bedrockScrollArea = MySmoothScrollArea(self.bedrockNewServerPage)
        self.bedrockScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.bedrockScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.bedrockScrollArea.setWidgetResizable(True)
        self.bedrockScrollArea.setObjectName("bedrockScrollArea")
        self.bedrockScrollArea.setFrameShape(QFrame.NoFrame)

        self.bedrockScrollAreaContents = QWidget()
        self.bedrockScrollAreaContents.setGeometry(QRect(0, 0, 600, 600))
        self.bedrockScrollAreaContents.setObjectName("bedrockScrollAreaContents")

        self.bedrockScrollAreaVerticalLayout = QVBoxLayout(self.bedrockScrollAreaContents)
        self.bedrockScrollAreaVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.bedrockScrollAreaVerticalLayout.setObjectName("bedrockScrollAreaVerticalLayout")

        # 核心选择部分
        self.bedrockSetCoreWidget = QWidget(self.bedrockScrollAreaContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bedrockSetCoreWidget.sizePolicy().hasHeightForWidth())
        self.bedrockSetCoreWidget.setSizePolicy(sizePolicy)
        self.bedrockSetCoreWidget.setObjectName("bedrockSetCoreWidget")

        self.bedrockCoreGridLayout = QGridLayout(self.bedrockSetCoreWidget)
        self.bedrockCoreGridLayout.setObjectName("bedrockCoreGridLayout")

        self.bedrockCoreSubtitleLabel = SubtitleLabel(self.bedrockSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bedrockCoreSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.bedrockCoreSubtitleLabel.setSizePolicy(sizePolicy)
        self.bedrockCoreSubtitleLabel.setObjectName("bedrockCoreSubtitleLabel")
        self.bedrockCoreGridLayout.addWidget(self.bedrockCoreSubtitleLabel, 0, 0, 1, 1)

        self.bedrockManuallyAddCorePrimaryPushBtn = PrimaryPushButton(self.bedrockSetCoreWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bedrockManuallyAddCorePrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.bedrockManuallyAddCorePrimaryPushBtn.setSizePolicy(sizePolicy)
        self.bedrockManuallyAddCorePrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.bedrockManuallyAddCorePrimaryPushBtn.setObjectName(
            "bedrockManuallyAddCorePrimaryPushBtn"
        )
        self.bedrockCoreGridLayout.addWidget(self.bedrockManuallyAddCorePrimaryPushBtn, 1, 0, 1, 1)

        spacerItem_bedrock_core = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.bedrockCoreGridLayout.addItem(spacerItem_bedrock_core, 1, 1, 1, 1)
        self.bedrockScrollAreaVerticalLayout.addWidget(self.bedrockSetCoreWidget)

        # 编码设置部分
        self.bedrockSetDeEncodingWidget = QWidget(self.bedrockScrollAreaContents)
        self.bedrockSetDeEncodingWidget.setObjectName("bedrockSetDeEncodingWidget")

        self.bedrockDeEncodingGridLayout = QGridLayout(self.bedrockSetDeEncodingWidget)
        self.bedrockDeEncodingGridLayout.setObjectName("bedrockDeEncodingGridLayout")

        self.bedrockDeEncodingSubtitleLabel = SubtitleLabel(self.bedrockSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bedrockDeEncodingSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.bedrockDeEncodingSubtitleLabel.setSizePolicy(sizePolicy)
        self.bedrockDeEncodingSubtitleLabel.setObjectName("bedrockDeEncodingSubtitleLabel")
        self.bedrockDeEncodingGridLayout.addWidget(self.bedrockDeEncodingSubtitleLabel, 0, 0, 1, 1)

        self.bedrockOutputDeEncodingLabel = StrongBodyLabel(self.bedrockSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bedrockOutputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.bedrockOutputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.bedrockOutputDeEncodingLabel.setObjectName("bedrockOutputDeEncodingLabel")
        self.bedrockDeEncodingGridLayout.addWidget(self.bedrockOutputDeEncodingLabel, 1, 0, 1, 1)

        self.bedrockOutputDeEncodingComboBox = ComboBox(self.bedrockSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bedrockOutputDeEncodingComboBox.sizePolicy().hasHeightForWidth()
        )
        self.bedrockOutputDeEncodingComboBox.setSizePolicy(sizePolicy)
        self.bedrockOutputDeEncodingComboBox.setObjectName("bedrockOutputDeEncodingComboBox")
        self.bedrockDeEncodingGridLayout.addWidget(self.bedrockOutputDeEncodingComboBox, 1, 1, 1, 1)

        self.bedrockInputDeEncodingLabel = StrongBodyLabel(self.bedrockSetDeEncodingWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bedrockInputDeEncodingLabel.sizePolicy().hasHeightForWidth()
        )
        self.bedrockInputDeEncodingLabel.setSizePolicy(sizePolicy)
        self.bedrockInputDeEncodingLabel.setObjectName("bedrockInputDeEncodingLabel")
        self.bedrockDeEncodingGridLayout.addWidget(self.bedrockInputDeEncodingLabel, 2, 0, 1, 1)

        self.bedrockInputDeEncodingComboBox = ComboBox(self.bedrockSetDeEncodingWidget)
        self.bedrockInputDeEncodingComboBox.setText("")
        self.bedrockInputDeEncodingComboBox.setObjectName("bedrockInputDeEncodingComboBox")
        self.bedrockDeEncodingGridLayout.addWidget(self.bedrockInputDeEncodingComboBox, 2, 1, 1, 1)
        self.bedrockScrollAreaVerticalLayout.addWidget(self.bedrockSetDeEncodingWidget)

        # 服务器名称部分
        self.bedrockSetServerNameWidget = QWidget(self.bedrockScrollAreaContents)
        self.bedrockSetServerNameWidget.setObjectName("bedrockSetServerNameWidget")

        self.bedrockServerNameVerticalLayout = QVBoxLayout(self.bedrockSetServerNameWidget)
        self.bedrockServerNameVerticalLayout.setObjectName("bedrockServerNameVerticalLayout")

        self.bedrockServerNameSubtitleLabel = SubtitleLabel(self.bedrockSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bedrockServerNameSubtitleLabel.sizePolicy().hasHeightForWidth()
        )
        self.bedrockServerNameSubtitleLabel.setSizePolicy(sizePolicy)
        self.bedrockServerNameSubtitleLabel.setObjectName("bedrockServerNameSubtitleLabel")
        self.bedrockServerNameVerticalLayout.addWidget(self.bedrockServerNameSubtitleLabel)

        self.bedrockServerNameLineEdit = LineEdit(self.bedrockSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bedrockServerNameLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.bedrockServerNameLineEdit.setSizePolicy(sizePolicy)
        self.bedrockServerNameLineEdit.setMinimumSize(QSize(0, 30))
        self.bedrockServerNameLineEdit.setObjectName("bedrockServerNameLineEdit")
        self.bedrockServerNameVerticalLayout.addWidget(self.bedrockServerNameLineEdit)

        self.bedrockSaveServerPrimaryPushBtn = PrimaryPushButton(self.bedrockSetServerNameWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bedrockSaveServerPrimaryPushBtn.sizePolicy().hasHeightForWidth()
        )
        self.bedrockSaveServerPrimaryPushBtn.setSizePolicy(sizePolicy)
        self.bedrockSaveServerPrimaryPushBtn.setMinimumSize(QSize(130, 0))
        self.bedrockSaveServerPrimaryPushBtn.setObjectName("bedrockSaveServerPrimaryPushBtn")
        self.bedrockServerNameVerticalLayout.addWidget(self.bedrockSaveServerPrimaryPushBtn)
        self.bedrockScrollAreaVerticalLayout.addWidget(self.bedrockSetServerNameWidget)

        spacerItem_bedrock2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.bedrockScrollAreaVerticalLayout.addItem(spacerItem_bedrock2)
        self.bedrockScrollArea.setWidget(self.bedrockScrollAreaContents)
        self.bedrockGridLayout.addWidget(self.bedrockScrollArea, 1, 1, 1, 1)

        spacerItem_bedrock3 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.bedrockGridLayout.addItem(spacerItem_bedrock3, 0, 0, 2, 1)
        self.newServerStackedWidget.addWidget(self.bedrockNewServerPage)
        # ========== 基岩版服务器页面结束 ==========

        self.importNewServerPage = QWidget()
        self.importNewServerPage.setObjectName("importNewServerPage")

        self.gridLayout_21 = QGridLayout(self.importNewServerPage)
        self.gridLayout_21.setObjectName("gridLayout_21")

        self.importTitleWidget = QWidget(self.importNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importTitleWidget.sizePolicy().hasHeightForWidth())
        self.importTitleWidget.setSizePolicy(sizePolicy)
        self.importTitleWidget.setObjectName("importTitleWidget")

        self.horizontalLayout_10 = QHBoxLayout(self.importTitleWidget)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.importBackToGuidePushButton = TransparentToolButton(
            FIF.PAGE_LEFT, self.importTitleWidget
        )
        self.importBackToGuidePushButton.setObjectName("importBackToGuidePushButton")

        self.horizontalLayout_10.addWidget(self.importBackToGuidePushButton)
        self.importSubtitleLabel = SubtitleLabel(self.importTitleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importSubtitleLabel.sizePolicy().hasHeightForWidth())
        self.importSubtitleLabel.setSizePolicy(sizePolicy)
        self.importSubtitleLabel.setObjectName("importSubtitleLabel")
        self.horizontalLayout_10.addWidget(self.importSubtitleLabel)

        self.horizontalLayout_10.addWidget(self.importSubtitleLabel)
        spacerItem16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem16)
        self.gridLayout_21.addWidget(self.importTitleWidget, 0, 1, 1, 1)
        spacerItem19 = QSpacerItem(20, 406, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.gridLayout_21.addItem(spacerItem19, 0, 0, 2, 1)
        self.importNewServerStackWidget = ChildStackedWidget(self.importNewServerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.importNewServerStackWidget.sizePolicy().hasHeightForWidth()
        )
        self.importNewServerStackWidget.setSizePolicy(sizePolicy)
        self.importNewServerStackWidget.setObjectName("importNewServerStackWidget")
        self.gridLayout_21.addWidget(self.importNewServerStackWidget, 1, 1, 1, 1)
        self.newServerStackedWidget.addWidget(self.importNewServerPage)
        self.gridLayout.addWidget(self.newServerStackedWidget, 2, 2, 1, 1)

        self.setObjectName("ConfigureInterface")

        self.noobNewServerScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.extendedNewServerScrollArea.setAttribute(Qt.WA_StyledBackground)
        self.bedrockScrollArea.setAttribute(Qt.WA_StyledBackground)

        # 引导页
        self.titleLabel.setText(self.tr("新建服务器"))
        self.subTitleLabel.setText(self.tr("有 4 种方式供你选择。"))

        # 简易模式
        self.noobJavaSubtitleLabel.setText(self.tr("Java "))
        self.noobJavaInfoLabel.setText(self.tr("[选择的 Java 的信息]"))
        self.noobDownloadJavaPrimaryPushBtn.setText(self.tr("下载 Java"))
        self.noobManuallyAddJavaPrimaryPushBtn.setText(self.tr("手动导入"))
        self.noobAutoDetectJavaPrimaryPushBtn.setText(self.tr("自动查找 Java"))
        self.noobJavaListPushBtn.setText(self.tr("Java 列表"))
        self.noobMemUnitLabel.setText(self.tr("M"))
        self.noobToSymbol.setText(self.tr("~"))
        self.noobMemSubtitleLabel.setText(self.tr("内存"))
        self.noobDownloadCorePrimaryPushBtn.setText(self.tr("下载核心"))
        self.noobManuallyAddCorePrimaryPushBtn.setText(self.tr("手动导入"))
        self.noobAddCoreFromDownloadedPrimaryPushBtn.setText(self.tr("从下载的核心中导入"))
        self.noobCoreSubtitleLabel.setText(self.tr("核心"))
        self.noobServerNameSubtitleLabel.setText(self.tr("服务器名称"))
        self.noobSaveServerPrimaryPushBtn.setText(self.tr("保存！"))
        self.noobSubtitleLabel.setText(self.tr("简易模式"))
        self.noobMinMemLineEdit.setPlaceholderText(self.tr("整数"))
        self.noobMaxMemLineEdit.setPlaceholderText(self.tr("整数"))
        self.noobServerNameLineEdit.setPlaceholderText(self.tr("不能包含非法字符"))

        # 进阶模式
        self.extendedSubtitleLabel.setText(self.tr("进阶模式"))
        self.extendedJavaSubtitleLabel.setText(self.tr("Java "))
        self.extendedJavaInfoLabel.setText(self.tr("[选择的 Java 的信息]"))
        self.extendedDownloadJavaPrimaryPushBtn.setText(self.tr("下载 Java"))
        self.extendedManuallyAddJavaPrimaryPushBtn.setText(self.tr("手动导入"))
        self.extendedAutoDetectJavaPrimaryPushBtn.setText(self.tr("自动查找 Java"))
        self.extendedJavaListPushBtn.setText(self.tr("Java 列表"))
        self.extendedMemSubtitleLabel.setText(self.tr("内存"))
        self.extendedToSymbol.setText("~")
        self.extendedDownloadCorePrimaryPushBtn.setText(self.tr("下载核心"))
        self.extendedManuallyAddCorePrimaryPushBtn.setText(self.tr("手动导入"))
        self.extendedAddCoreFromDownloadedPrimaryPushBtn.setText(self.tr("从下载的核心中导入"))
        self.extendedCoreSubtitleLabel.setText(self.tr("核心"))
        self.extendedDeEncodingSubtitleLabel.setText(self.tr("编码设置"))
        self.extendedOutputDeEncodingLabel.setText(self.tr("控制台输出编码 (优先级高于全局设置)"))
        self.extendedInputDeEncodingLabel.setText(self.tr("指令输入编码 (优先级高于全局设置)"))
        self.extendedJVMArgSubtitleLabel.setText(self.tr("JVM 参数"))
        self.JVMArgPlainTextEdit.setPlaceholderText(self.tr("可选，用一个空格分组"))
        self.extendedServerNameSubtitleLabel.setText(self.tr("服务器名称"))
        self.extendedSaveServerPrimaryPushBtn.setText(self.tr("保存！"))
        self.extendedMinMemLineEdit.setPlaceholderText(self.tr("整数"))
        self.extendedMaxMemLineEdit.setPlaceholderText(self.tr("整数"))
        self.extendedServerNameLineEdit.setPlaceholderText(self.tr("不能包含非法字符"))
        self.extendedOutputDeEncodingComboBox.addItems(
            [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI")]
            if platform.system().lower() == "windows"
            else [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030")]
        )
        self.extendedOutputDeEncodingComboBox.setCurrentIndex(0)
        self.extendedInputDeEncodingComboBox.addItems(
            [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI")]
            if platform.system().lower() == "windows"
            else [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030")]
        )
        self.extendedInputDeEncodingComboBox.setCurrentIndex(0)
        self.extendedMemUnitComboBox.addItems(["M", "G"])
        self.extendedMemUnitComboBox.setCurrentIndex(0)

        # 基岩版模式
        self.bedrockSubtitleLabel.setText(self.tr("基岩版服务器"))
        self.bedrockCoreSubtitleLabel.setText(self.tr("服务器核心"))
        self.bedrockManuallyAddCorePrimaryPushBtn.setText(self.tr("选择服务器可执行文件"))
        self.bedrockDeEncodingSubtitleLabel.setText(self.tr("编码设置"))
        self.bedrockOutputDeEncodingLabel.setText(self.tr("控制台输出编码"))
        self.bedrockInputDeEncodingLabel.setText(self.tr("指令输入编码"))
        self.bedrockServerNameSubtitleLabel.setText(self.tr("服务器名称"))
        self.bedrockSaveServerPrimaryPushBtn.setText(self.tr("创建服务器！"))
        self.bedrockServerNameLineEdit.setPlaceholderText(self.tr("不能包含非法字符"))
        self.bedrockOutputDeEncodingComboBox.addItems(
            [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI")]
            if platform.system().lower() == "windows"
            else [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030")]
        )
        self.bedrockOutputDeEncodingComboBox.setCurrentIndex(0)
        self.bedrockInputDeEncodingComboBox.addItems(
            [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI")]
            if platform.system().lower() == "windows"
            else [self.tr("跟随全局"), self.tr("UTF-8"), self.tr("GB18030")]
        )
        self.bedrockInputDeEncodingComboBox.setCurrentIndex(0)

        # 导入
        self.importSubtitleLabel.setText(self.tr("导入整合包(Modpack)"))
        # 引导页绑定 - 使用 HeaderCardWidget 的 connectSlot 方法
        self.noobNewServerWidget.connectSlot(self.newServerStackedWidgetNavigation)
        self.extendedNewServerWidget.connectSlot(self.newServerStackedWidgetNavigation)
        # macOS下禁用基岩版服务器创建
        if platform.system().lower() == "darwin":

            def show_bedrock_macos_not_supported():
                InfoBar.error(
                    title=self.tr("不支持"),
                    content=self.tr("macOS 暂不支持创建基岩版服务器"),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=4000,
                    parent=self.parent() or self,
                )

            self.bedrockNewServerWidget.connectSlot(show_bedrock_macos_not_supported)
        else:
            self.bedrockNewServerWidget.connectSlot(self.newServerStackedWidgetNavigation)
        self.importNewServerWidget.connectSlot(self.newServerStackedWidgetNavigation)

        # 简易模式绑定
        self.noobBackToGuidePushButton.clicked.connect(
            lambda: self.newServerStackedWidget.setCurrentIndex(0)
        )
        self.noobManuallyAddJavaPrimaryPushBtn.clicked.connect(self.addJavaManually)
        self.noobAutoDetectJavaPrimaryPushBtn.clicked.connect(self.autoDetectJava)
        self.noobManuallyAddCorePrimaryPushBtn.clicked.connect(self.addCoreManually)
        self.noobAddCoreFromDownloadedPrimaryPushBtn.clicked.connect(self.showDownloadEntries)
        self.noobSaveServerPrimaryPushBtn.clicked.connect(self.finishNewServer)

        # 进阶模式绑定
        self.extendedBackToGuidePushButton.clicked.connect(
            lambda: self.newServerStackedWidget.setCurrentIndex(0)
        )
        self.extendedManuallyAddJavaPrimaryPushBtn.clicked.connect(self.addJavaManually)
        self.extendedAutoDetectJavaPrimaryPushBtn.clicked.connect(self.autoDetectJava)
        self.extendedManuallyAddCorePrimaryPushBtn.clicked.connect(self.addCoreManually)
        self.extendedAddCoreFromDownloadedPrimaryPushBtn.clicked.connect(self.showDownloadEntries)
        self.extendedSaveServerPrimaryPushBtn.clicked.connect(self.finishNewServer)

        # 基岩版模式绑定
        self.bedrockBackToGuidePushButton.clicked.connect(
            lambda: self.newServerStackedWidget.setCurrentIndex(0)
        )
        self.bedrockManuallyAddCorePrimaryPushBtn.clicked.connect(self.addBedrockCoreManually)
        self.bedrockSaveServerPrimaryPushBtn.clicked.connect(self.finishBedrockServer)

        # 导入法绑定
        self.importBackToGuidePushButton.clicked.connect(self._importerBackToGuide)

        self.javaVersionLabelItems = [
            None,
            self.noobJavaInfoLabel,
            self.extendedJavaInfoLabel,
            None,
        ]

        self.settingsRunner_newServerType()
        self._initModPackImporter()

    def settingsRunner_newServerType(self):
        self.newServerStackedWidget.setCurrentIndex(
            settingsVariables.newServerTypeList.index(cfg.get(cfg.newServerType))
        )

    def newServerStackedWidgetNavigation(self):
        """决定新建服务器的方式"""
        # 通过发送者的父级（HeaderCardWidget）来确定索引
        sender = self.sender()
        if hasattr(sender, "parent") and callable(sender.parent):
            card_widget = sender.parent().parent()
            if isinstance(card_widget, NoobServerCardWidget):
                self.newServerStackedWidget.setCurrentIndex(1)
            elif isinstance(card_widget, ExtendedServerCardWidget):
                self.newServerStackedWidget.setCurrentIndex(2)
            elif isinstance(card_widget, BedrockServerCardWidget):
                self.newServerStackedWidget.setCurrentIndex(3)
            elif isinstance(card_widget, ImportServerCardWidget):
                self.newServerStackedWidget.setCurrentIndex(4)

    def _importerBackToGuide(self):
        """返回引导页，同时清理解压的文件"""
        self._importerCleanupServerPath()
        self.newServerStackedWidget.setCurrentIndex(0)

    def addJavaManually(self):
        """手动添加Java"""
        selectedJavaPath = str(
            QFileDialog.getOpenFileName(
                self,
                self.tr("选择 java.exe 程序"),
                getcwd(),
                self.tr("Java 主程序 (java.exe)"),
            )[0]
        )
        if selectedJavaPath != "":
            if v := javaDetector.getJavaVersion(selectedJavaPath):
                currentJavaPaths = configureServerVariables.javaPath
                if javaDetector.Java(selectedJavaPath, v) not in currentJavaPaths:
                    currentJavaPaths.append(javaDetector.Java(selectedJavaPath, v))
                    javaDetector.sortJavaList(currentJavaPaths)
                    InfoBar.success(
                        title=self.tr("已添加"),
                        content=self.tr("Java路径: ")
                        + selectedJavaPath
                        + self.tr("\n版本: ")
                        + v
                        + self.tr("\n但你还需要继续到 Java 列表中选取。"),
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self,
                    )
                else:
                    InfoBar.warning(
                        title=self.tr("未添加"),
                        content=self.tr(
                            "此 Java 已被添加过，也有可能是自动查找 Java 时已经搜索到了。请检查 Java 列表。"  # noqa: E501
                        ),
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=4848,
                        parent=self,
                    )
                javaDetector.saveJavaList(currentJavaPaths)
            else:
                InfoBar.error(
                    title=self.tr("添加失败"),
                    content=self.tr("此 Java 无效！"),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
        else:
            InfoBar.warning(
                title=self.tr("未添加"),
                content=self.tr("你并没有选择 Java。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def autoDetectJava(self):
        """自动查找Java"""
        # 防止同时多次运行worker线程
        self.noobAutoDetectJavaPrimaryPushBtn.setEnabled(False)
        self.extendedAutoDetectJavaPrimaryPushBtn.setEnabled(False)
        # 同时禁用importer的按钮（如果存在）
        if hasattr(self, "importer_confirmWidget") and self.importer_confirmWidget:
            self.importer_confirmWidget.autoDetectJavaBtn.setEnabled(False)
        self.javaFindWorkThreadFactory.create().start()

    @pyqtSlot(list)
    def autoDetectJavaFinished(self, _JavaPaths: list):
        """自动查找Java结果处理"""
        if osp.exists("./MCSL2/AutoDetectJavaHistory.txt"):
            remove("./MCSL2/AutoDetectJavaHistory.txt")
        if osp.exists("./MCSL2/AutoDetectJavaHistory.json"):
            remove("./MCSL2/AutoDetectJavaHistory.json")

        savedJavaList = javaDetector.loadJavaList()
        invaildJavaList = []
        javaList = javaDetector.combineJavaList(savedJavaList, _JavaPaths, invaild=invaildJavaList)
        javaDetector.sortJavaList(javaList, reverse=False)
        configureServerVariables.javaPath = javaList
        javaDetector.saveJavaList(javaList)
        for java in invaildJavaList:
            InfoBar.error(
                title=self.tr("Java ") + str(java.version) + self.tr(" 已失效"),
                content=self.tr("位于 ")
                + str(java.path)
                + self.tr(" 的 ")
                + str(java.version)
                + self.tr(" 已失效"),
                parent=self.window(),
                duration=3000,
            )

    @pyqtSlot(int)
    def onJavaFindWorkThreadFinished(self, sequenceNumber):
        """自动查找Java结束后的处理"""
        if sequenceNumber > 1:
            InfoBar.success(
                title=self.tr("查找完毕"),
                content=self.tr("一共搜索到了")
                + str(len(configureServerVariables.javaPath))
                + self.tr("个 Java。\n请单击「Java 列表」按钮查看、选择。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

            self.noobAutoDetectJavaPrimaryPushBtn.setEnabled(True)
            self.extendedAutoDetectJavaPrimaryPushBtn.setEnabled(True)
            # 同时启用importer的按钮
            if hasattr(self, "importer_confirmWidget") and self.importer_confirmWidget:
                self.importer_confirmWidget.autoDetectJavaBtn.setEnabled(True)

    def addCoreManually(self):
        """手动添加服务器核心"""
        # 根据操作系统决定文件过滤器
        system = platform.system().lower()
        if system == "windows":
            file_filter = self.tr(
                "服务器核心 (*.jar *.exe);;Java 可执行文件 (*.jar);;"
                "基岩版服务器 (*.exe);;所有文件 (*)"
            )
        elif system == "darwin":  # macOS
            file_filter = self.tr(
                "服务器核心 (*.jar *);;Java 可执行文件 (*.jar);;基岩版服务器;;所有文件 (*)"
            )
        else:  # Linux
            file_filter = self.tr(
                "服务器核心 (*.jar *);;Java 可执行文件 (*.jar);;基岩版服务器;;所有文件 (*)"
            )

        tmpCorePath = str(
            QFileDialog.getOpenFileName(
                self,
                self.tr("选择服务器核心文件"),
                getcwd(),
                file_filter,
            )[0]
        )

        if tmpCorePath != "":
            configureServerVariables.corePath = tmpCorePath
            configureServerVariables.coreFileName = tmpCorePath.split("/")[-1]

            # 检测是否为基岩版服务器
            fileName = configureServerVariables.coreFileName.lower()
            if (
                fileName.startswith("bedrock")
                or fileName == "bedrock_server"
                or fileName == "bedrock_server.exe"
                or "bedrock" in fileName
            ):
                configureServerVariables.serverType = "bedrock"
                configureServerVariables.extraData = {"edition": "bedrock"}
                InfoBar.success(
                    title=self.tr("已添加基岩版服务器"),
                    content=(
                        self.tr("核心文件名: ")
                        + configureServerVariables.coreFileName
                        + self.tr("\n类型: 基岩版")
                    ),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
            else:
                # Java版服务器
                InfoBar.success(
                    title=self.tr("已添加"),
                    content=self.tr("核心文件名: ") + configureServerVariables.coreFileName,
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
        else:
            InfoBar.warning(
                title=self.tr("未添加"),
                content=self.tr("你并没有选择服务器核心。\n当前核心: ")
                + (self.tr("未添加") if not (a := configureServerVariables.coreFileName) else a),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def addBedrockCoreManually(self):
        """手动添加基岩版服务器核心 (子线程执行重操作)"""
        system = platform.system().lower()
        if system == "windows":
            file_filter = self.tr(
                "基岩版服务器 (*.zip *.exe);;压缩包 (*.zip);;可执行文件 (*.exe);;所有文件 (*)"
            )
        else:
            file_filter = self.tr("基岩版服务器 (*.zip *);;压缩包 (*.zip);;所有文件 (*)")

        tmpPath = str(
            QFileDialog.getOpenFileName(
                self,
                self.tr("选择基岩版服务器压缩包或可执行文件"),
                getcwd(),
                file_filter,
            )[0]
        )

        if not tmpPath:
            InfoBar.warning(
                title=self.tr("未添加"),
                content=self.tr("你并没有选择服务器核心。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            return

        self.addingBedrockCoreStateToolTip = StateToolTip(
            self.tr("解析基岩版核心"), self.tr("请稍后，正在处理..."), self
        )
        self.addingBedrockCoreStateToolTip.move(self.addingBedrockCoreStateToolTip.getSuitablePos())
        self.addingBedrockCoreStateToolTip.show()

        self.bedrockManuallyAddCorePrimaryPushBtn.setEnabled(False)

        self.bedrockCoreImportThread = BedrockCoreImportThread(tmpPath, system, self)
        self.bedrockCoreImportThread.success.connect(self._onBedrockCoreImportSuccess)
        self.bedrockCoreImportThread.failed.connect(self._onBedrockCoreImportFailed)
        self.bedrockCoreImportThread.finished.connect(self._cleanupBedrockCoreImportThread)
        self.bedrockCoreImportThread.start()

    @pyqtSlot(dict)
    def _onBedrockCoreImportSuccess(self, result: dict):
        configureServerVariables.corePath = result.get("core_path", "")
        configureServerVariables.coreFileName = result.get("core_file_name", "")
        configureServerVariables.serverType = "bedrock"
        configureServerVariables.extraData = result.get("extra_data", {"edition": "bedrock"})

        if getattr(self, "addingBedrockCoreStateToolTip", None):
            self.addingBedrockCoreStateToolTip.setContent(self.tr("已添加基岩版服务器核心"))
            self.addingBedrockCoreStateToolTip.setState(True)
            self.addingBedrockCoreStateToolTip = None

        if configureServerVariables.extraData.get("extracted_from_zip"):
            InfoBar.success(
                title=self.tr("已添加基岩版服务器核心"),
                content=(
                    self.tr("已从压缩包解压\n")
                    + self.tr("核心文件: ")
                    + configureServerVariables.coreFileName
                    + self.tr("\n类型: 基岩版")
                ),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        else:
            InfoBar.success(
                title=self.tr("已添加基岩版服务器核心"),
                content=(
                    self.tr("核心文件: ")
                    + configureServerVariables.coreFileName
                    + self.tr("\n类型: 基岩版")
                ),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    @pyqtSlot(str)
    def _onBedrockCoreImportFailed(self, err: str):
        if getattr(self, "addingBedrockCoreStateToolTip", None):
            self.addingBedrockCoreStateToolTip.setContent(self.tr("处理失败！"))
            self.addingBedrockCoreStateToolTip.setState(False)
            self.addingBedrockCoreStateToolTip = None

        InfoBar.error(
            title=self.tr("解压失败"),
            content=self.tr("无法处理核心文件: ") + str(err),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self,
        )

    def _cleanupBedrockCoreImportThread(self):
        self.bedrockManuallyAddCorePrimaryPushBtn.setEnabled(True)
        self.bedrockCoreImportThread = None

    def showDownloadEntries(self):
        """显示下载条目"""
        self.downloadEntry = DownloadEntryBox(self)
        self.downloadEntry.accepted.connect(self.onDownloadEntryClosed)
        self.downloadEntry.rejected.connect(self.onDownloadEntryClosed)
        self.downloadEntry.show()
        self.downloadEntry.raise_()
        self.downloadEntry.asyncGetEntries()

    def onDownloadEntryClosed(self):
        entries = self.downloadEntry.lastSelection
        if entries:
            coreName, coreType, mcVersion, buildVersion = [
                e.text() for e in self.downloadEntry.entryView.selectedItems()
            ]
            configureServerVariables.corePath = osp.join("MCSL2", "Downloads", coreName)
            configureServerVariables.coreFileName = coreName
            configureServerVariables.serverType = coreType.lower()
            configureServerVariables.extraData = {
                "mc_version": mcVersion,
                "build_version": buildVersion,
            }
            InfoBar.success(
                title=self.tr("已添加"),
                content=self.tr("核心文件名: ")
                + str(configureServerVariables.coreFileName)
                + self.tr("\n类型: ")
                + str(coreType)
                + self.tr("\nMC 版本: ")
                + str(mcVersion)
                + self.tr("\n构建版本: ")
                + str(buildVersion),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
        else:
            InfoBar.warning(
                title=self.tr("未添加"),
                content=self.tr("你并没有选择服务器核心。\n当前核心: ")
                + (
                    self.tr("未添加")
                    if not (a := configureServerVariables.coreFileName)
                    else str(a)
                ),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def setJavaPath(self, selectedJavaPath):
        """选择Java后处理Java路径"""
        configureServerVariables.selectedJavaPath = selectedJavaPath
        if self.newServerStackedWidget.currentIndex() <= 3:
            pass
        else:
            self.javaVersionLabelItems[self.newServerStackedWidget.currentIndex()].setPlainText(
                selectedJavaPath
            )

    def setJavaVer(self, selectedJavaVer):
        """选择Java后处理Java版本"""
        configureServerVariables.selectedJavaVersion = selectedJavaVer
        if self.newServerStackedWidget.currentIndex() <= 3:
            self.javaVersionLabelItems[self.newServerStackedWidget.currentIndex()].setText(
                self.tr("已选择，版本: ") + str(selectedJavaVer)
            )

    def finishNewServer(self):
        """完成新建服务器的检查触发器"""
        # 定义
        currentNewServerType = self.newServerStackedWidget.currentIndex()

        # 判断是否从importer调用（检查是否已经设置了数据）
        isFromImporter = (
            hasattr(self, "importer_serverPath")
            and self.importer_serverPath
            and configureServerVariables.minMem
            and configureServerVariables.serverName
        )

        # 如果不是从importer调用，设置memUnit
        if not isFromImporter:
            configureServerVariables.memUnit = (
                configureServerVariables.memUnitList[0]
                if currentNewServerType == 1
                else configureServerVariables.memUnitList[
                    self.extendedMemUnitComboBox.currentIndex()
                ]
            )

        # 检查：如果从importer调用，直接使用configureServerVariables中的值
        if isFromImporter:
            check = ServerValidator().check(
                v=configureServerVariables,
                minMem=str(configureServerVariables.minMem),
                maxMem=str(configureServerVariables.maxMem),
                name=configureServerVariables.serverName,
                jvmArg="",
            )
        else:
            check = ServerValidator().check(
                v=configureServerVariables,
                minMem=(
                    self.noobMinMemLineEdit.text()
                    if currentNewServerType == 1
                    else self.extendedMinMemLineEdit.text()
                ),
                maxMem=(
                    self.noobMaxMemLineEdit.text()
                    if currentNewServerType == 1
                    else self.extendedMaxMemLineEdit.text()
                ),
                name=(
                    self.noobServerNameLineEdit.text()
                    if currentNewServerType == 1
                    else self.extendedServerNameLineEdit.text()
                ),
                jvmArg=(
                    self.JVMArgPlainTextEdit.toPlainText() if currentNewServerType == 2 else ""
                ),
            )
        # 如果出错
        if check[1] != 0:
            title = self.tr("创建服务器失败！存在 ") + str(check[1]) + self.tr(" 个问题。")
            detail_text = self.tr(check[0]) + self.tr(
                "\n----------------------------\n请根据上方提示，修改后再尝试保存。\n如果确认自己填写的没有问题，请联系开发者。"
            )
            dialog = Dialog(title, self.tr("详细信息如下："), self)
            dialog.titleBar.show()
            dialog.setTitleBarVisible(False)
            dialog.yesButton.setText(self.tr("确认"))
            dialog.cancelButton.setParent(None)
            dialog.cancelButton.deleteLater()
            del dialog.cancelButton
            detail_widget = ExceptionWidget(detail_text)
            dialog.textLayout.addWidget(detail_widget.exceptionScrollArea)
            dialog.exec()
        else:
            totalJVMArg: str = "\n".join(configureServerVariables.jvmArg)
            title = self.tr("请再次检查你设置的参数是否有误: ")

            # 基岩版服务器显示不同的内容
            if configureServerVariables.serverType == "bedrock":
                content = (
                    self.tr("服务器核心: ")
                    + configureServerVariables.corePath
                    + "\n"
                    + self.tr("服务器核心文件名: ")
                    + configureServerVariables.coreFileName
                    + "\n"
                    + self.tr("服务器类型: 基岩版")
                    + "\n"
                )
                # 只有在进阶模式下才显示编码设置
                if currentNewServerType == 2:
                    content += (
                        self.tr("输出编码设置: ")
                        + self.extendedOutputDeEncodingComboBox.itemText(
                            configureServerVariables.consoleDeEncodingList.index(
                                configureServerVariables.consoleOutputDeEncoding
                            )
                        )
                        + "\n"
                        + self.tr("输入编码设置: ")
                        + self.extendedInputDeEncodingComboBox.itemText(
                            configureServerVariables.consoleDeEncodingList.index(
                                configureServerVariables.consoleInputDeEncoding
                            )
                        )
                        + "\n"
                    )
                content += self.tr("服务器名称: ") + configureServerVariables.serverName
            else:
                content = (
                    self.tr("Java: ")
                    + configureServerVariables.selectedJavaPath
                    + "\n"
                    + self.tr("Java版本: ")
                    + configureServerVariables.selectedJavaVersion
                    + "\n"
                    + self.tr("内存: ")
                    + str(configureServerVariables.minMem)
                    + configureServerVariables.memUnit
                    + "~"
                    + str(configureServerVariables.maxMem)
                    + configureServerVariables.memUnit
                    + "\n"
                    + self.tr("服务器核心: ")
                    + configureServerVariables.corePath
                    + "\n"
                    + self.tr("服务器核心文件名: ")
                    + configureServerVariables.coreFileName
                    + "\n"
                    + self.tr("输出编码设置: ")
                    + self.extendedOutputDeEncodingComboBox.itemText(
                        configureServerVariables.consoleDeEncodingList.index(
                            configureServerVariables.consoleOutputDeEncoding
                        )
                    )
                    + "\n"
                    + self.tr("输入编码设置: ")
                    + self.extendedInputDeEncodingComboBox.itemText(
                        configureServerVariables.consoleDeEncodingList.index(
                            configureServerVariables.consoleInputDeEncoding
                        )
                    )
                    + "\n"
                    + self.tr("JVM参数: \n")
                    + "    "
                    + totalJVMArg
                    + "\n"
                    + self.tr("服务器名称: ")
                    + configureServerVariables.serverName
                )
            w = MessageBox(title, "", self)
            w.yesButton.setText(self.tr("无误，添加"))
            w.yesSignal.connect(self.preNewServerDispatcher)
            w.cancelButton.setText(self.tr("我再看看"))
            detail_widget = ExceptionWidget(content)
            w.textLayout.addWidget(detail_widget.exceptionScrollArea)
            w.contentLabel.setParent(None)
            w.contentLabel.deleteLater()
            w.exec()

    def finishBedrockServer(self):
        """完成基岩版服务器的创建"""
        # 检查核心文件
        if not configureServerVariables.coreFileName:
            InfoBar.error(
                title=self.tr("创建失败"),
                content=self.tr("请先选择基岩版服务器可执行文件！"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            return

        # 检查服务器名称
        serverName = self.bedrockServerNameLineEdit.text().strip()
        nameCheck = ServerValidator().checkServerNameSet(serverName, configureServerVariables)
        if nameCheck[1] != 0:  # 如果检查出错
            InfoBar.error(
                title=self.tr("创建失败"),
                content=nameCheck[0],  # 显示具体的错误信息
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            return

        configureServerVariables.serverName = serverName

        # 设置编码
        configureServerVariables.consoleOutputDeEncoding = (
            configureServerVariables.consoleDeEncodingList[
                self.bedrockOutputDeEncodingComboBox.currentIndex()
            ]
        )
        configureServerVariables.consoleInputDeEncoding = (
            configureServerVariables.consoleDeEncodingList[
                self.bedrockInputDeEncodingComboBox.currentIndex()
            ]
        )

        # 设置服务器类型
        configureServerVariables.serverType = "bedrock"
        if not configureServerVariables.extraData:
            configureServerVariables.extraData = {}
        configureServerVariables.extraData["edition"] = "bedrock"

        # 基岩版不需要Java和内存设置
        configureServerVariables.selectedJavaPath = ""
        configureServerVariables.selectedJavaVersion = ""
        configureServerVariables.minMem = 0
        configureServerVariables.maxMem = 0
        configureServerVariables.memUnit = "M"
        configureServerVariables.jvmArg = []

        # 显示确认对话框
        content = (
            self.tr("服务器核心: ")
            + configureServerVariables.corePath
            + "\n"
            + self.tr("服务器核心文件名: ")
            + configureServerVariables.coreFileName
            + "\n"
            + self.tr("服务器类型: 基岩版")
            + "\n"
            + self.tr("输出编码设置: ")
            + self.bedrockOutputDeEncodingComboBox.currentText()
            + "\n"
            + self.tr("输入编码设置: ")
            + self.bedrockInputDeEncodingComboBox.currentText()
            + "\n"
            + self.tr("服务器名称: ")
            + configureServerVariables.serverName
        )

        w = MessageBox(self.tr("请再次检查你设置的参数是否有误: "), "", self)
        w.yesButton.setText(self.tr("无误，创建"))
        w.yesSignal.connect(self.saveNewServer)
        w.cancelButton.setText(self.tr("我再看看"))
        detail_widget = ExceptionWidget(content)
        w.textLayout.addWidget(detail_widget.exceptionScrollArea)
        w.contentLabel.setParent(None)
        w.contentLabel.deleteLater()
        w.exec()

    def preNewServerDispatcher(self):
        """
        在self.saveNewServer() >>前<< (pre)，处理不同serverType而引起的差异性!
        """
        serverType = configureServerVariables.serverType

        # 如果 serverType 是空的，尝试自动检测 Forge/NeoForge installer
        if not serverType or serverType == "":
            # Check for NeoForge first
            detectedServerType = None
            versionInfo = None

            if (
                t := NeoForgeInstaller.isPossibleNeoForgeInstaller(
                    configureServerVariables.corePath
                )
            ) is not None:
                detectedServerType = "neoforge"
                mcVersion, version = t
                versionInfo = (mcVersion, version, "NeoForge")
            # Then check for Forge
            elif (
                t := ForgeInstaller.isPossibleForgeInstaller(configureServerVariables.corePath)
            ) is not None:
                detectedServerType = "forge"
                mcVersion, version = t
                versionInfo = (mcVersion, version, "Forge")

            # Show confirmation dialog if installer detected
            if versionInfo is not None:
                mcVersion, version, typeName = versionInfo
                w = MessageBox(
                    self.tr(f"这是否为一个 {typeName} 服务器？"),
                    self.tr("检测到可能为 ")
                    + str(mcVersion)
                    + self.tr(f" 版本的 {typeName}: ")
                    + version,
                    self,
                )
                w.yesButton.setText(self.tr("是"))
                w.cancelButton.setText(self.tr("不是"))
                # 如果选yes，设置 serverType；如果选no，保持为空
                if w.exec() == 1:
                    configureServerVariables.serverType = detectedServerType
                    serverType = detectedServerType
                else:
                    # 用户选择"不是"，确保 serverType 为空
                    configureServerVariables.serverType = ""
                    serverType = ""

        # serverType dispatcher: 总的处理关于serverType不同而引起的新建服务器前的差异性!
        if serverType == "forge":  # case 1
            # 尝试获取版本信息
            versionInfo = ForgeInstaller.isPossibleForgeInstaller(configureServerVariables.corePath)
            if versionInfo:
                mcVersion, forgeVersion = versionInfo
                w = MessageBox(
                    self.tr("这是 Forge 安装器"),
                    self.tr("检测到 Forge 版本：\nMinecraft: ")
                    + str(mcVersion)
                    + self.tr("\nForge: ")
                    + forgeVersion
                    + self.tr("\n\n是否需要自动安装 Forge 服务端？"),
                    self,
                )
            else:
                w = MessageBox(
                    self.tr("这是 Forge 安装器"),
                    self.tr("是否需要自动安装 Forge 服务端？"),
                    self,
                )
            w.yesButton.setText(self.tr("需要"))
            w.cancelButton.setText(self.tr("不需要"))
            # 如果选no
            if w.exec() == 0:
                configureServerVariables.serverType = ""
                configureServerVariables.extraData = {}

        elif serverType == "neoforge":
            # 尝试获取版本信息
            versionInfo = NeoForgeInstaller.isPossibleNeoForgeInstaller(
                configureServerVariables.corePath
            )
            if versionInfo:
                mcVersion, neoforgeVersion = versionInfo
                w = MessageBox(
                    self.tr("这是 NeoForge 安装器"),
                    self.tr("检测到 NeoForge 版本：\nMinecraft: ")
                    + str(mcVersion)
                    + self.tr("\nNeoForge: ")
                    + neoforgeVersion
                    + self.tr("\n\n是否需要自动安装 NeoForge 服务端？"),
                    self,
                )
            else:
                w = MessageBox(
                    self.tr("这是 NeoForge 安装器"),
                    self.tr("是否需要自动安装 NeoForge 服务端？"),
                    self,
                )
            w.yesButton.setText(self.tr("需要"))
            w.cancelButton.setText(self.tr("不需要"))
            # 如果选no
            if w.exec() == 0:
                configureServerVariables.serverType = ""
                configureServerVariables.extraData = {}

        elif serverType == "bedrock":  # case: bedrock edition
            # 基岩版服务器不需要额外处理
            pass

        elif serverType == "vanilla":  # case 2
            pass

        self.saveNewServer()  # 真正执行保存服务器

    def postNewServerDispatcher(self, exit0Msg=""):
        """
        在self.saveNewServer() >>后<< (post)，处理不同serverType而引起的差异性!
        其实通常是在self.saveNewServer()复制完核心后执行的，用于处理类似forge安装等
        """
        if configureServerVariables.serverType == "neoforge":
            self.installingForgeStateToolTip = StateToolTip(
                self.tr("安装 NeoForge"), self.tr("请稍后，正在安装..."), self
            )
            self.installingForgeStateToolTip.move(self.installingForgeStateToolTip.getSuitablePos())
            self.installingForgeStateToolTip.show()
            try:
                neoforge_server_path = f"./Servers/{configureServerVariables.serverName}"
                neoforge_core_file = configureServerVariables.coreFileName

                self.neoforgeInstaller = NeoForgeInstaller(
                    serverPath=neoforge_server_path,
                    file=neoforge_core_file,
                    java=configureServerVariables.selectedJavaPath,
                    logDecode=cfg.get(cfg.outputDeEncoding),
                )

                configureServerVariables.extraData["neoforge_version"] = (
                    self.neoforgeInstaller.neoforgeVersion
                )
                self.neoforgeInstaller.installFinished.connect(self.afterInstallingNeoForge)

                # init installerLogViewer
                self.installerLogViewer = ForgeInstallerProgressBox(
                    self.neoforgeInstaller.installerLogOutput,
                    self,
                    title=self.tr("NeoForge 安装器 (正在安装...)"),
                )
                self.installerLogViewer.cancelButton.clicked.connect(
                    self.neoforgeInstaller.cancelInstall
                )
                self.installerLogViewer.yesButton.clicked.connect(self.hideForgeInstallerHelper)
                self.installerLogViewer.setModal(True)
                self.installerLogViewer.hide()

                self.installerDownloadView = ForgeInstallerDownloadView(
                    self, title=self.tr("NeoForge Installer")
                )
                self.installerDownloadView.cancelButton.clicked.connect(
                    self.neoforgeInstaller.cancelInstall
                )
                self.installerDownloadView.yesButton.setEnabled(False)
                self.installerDownloadView.setModal(True)
                self.neoforgeInstaller.downloadInfo.connect(self.installerDownloadView.onProgress)
                self.installerDownloadView.allDone.connect(self.afterInstallerDownloadDone)
                self.installerDownloadView.show()

                self.neoforgeInstaller.asyncInstall()
            except Exception as e:
                self.afterInstallingNeoForge(False, str(e))
        elif configureServerVariables.serverType == "forge":
            self.installingForgeStateToolTip = StateToolTip(
                self.tr("安装 Forge"), self.tr("请稍后，正在安装..."), self
            )
            self.installingForgeStateToolTip.move(self.installingForgeStateToolTip.getSuitablePos())
            self.installingForgeStateToolTip.show()
            try:
                forge_server_path = f"./Servers/{configureServerVariables.serverName}"
                forge_core_file = configureServerVariables.coreFileName

                self.forgeInstaller = ForgeInstaller(
                    serverPath=forge_server_path,
                    file=forge_core_file,
                    java=configureServerVariables.selectedJavaPath,
                    logDecode=cfg.get(cfg.outputDeEncoding),
                )

                configureServerVariables.extraData["forge_version"] = (
                    self.forgeInstaller.forgeVersion
                )
                self.forgeInstaller.installFinished.connect(self.afterInstallingForge)

                # init installerLogViewer
                self.installerLogViewer = ForgeInstallerProgressBox(
                    self.forgeInstaller.installerLogOutput, self
                )
                self.installerLogViewer.cancelButton.clicked.connect(
                    self.forgeInstaller.cancelInstall
                )
                self.installerLogViewer.yesButton.clicked.connect(self.hideForgeInstallerHelper)
                self.installerLogViewer.setModal(True)
                self.installerLogViewer.hide()

                self.installerDownloadView = ForgeInstallerDownloadView(self)
                self.installerDownloadView.cancelButton.clicked.connect(
                    self.forgeInstaller.cancelInstall
                )
                self.installerDownloadView.yesButton.setEnabled(False)
                self.installerDownloadView.setModal(True)
                self.forgeInstaller.downloadInfo.connect(self.installerDownloadView.onProgress)
                self.installerDownloadView.allDone.connect(self.afterInstallerDownloadDone)
                self.installerDownloadView.show()

                self.forgeInstaller.asyncInstall()
            except Exception as e:
                self.afterInstallingForge(False, str(e))
        else:
            InfoBar.success(
                title=self.tr("成功"),
                content=exit0Msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def _clearNewServerInputs(self):
        # 无论用户设置如何，都要清除 serverType 和 extraData
        # 这些是临时的安装状态，不应该保留到下一次创建服务器
        configureServerVariables.serverType = ""
        configureServerVariables.extraData = {}
        
        # 清理importer相关的解压文件和状态
        if hasattr(self, 'importer_serverPath') and self.importer_serverPath:
            self._importerCleanupServerPath()

        if not cfg.get(cfg.clearAllNewServerConfigInProgram):
            return

        configureServerVariables.resetToDefault()
        if self.newServerStackedWidget.currentIndex() == 1:
            self.noobJavaInfoLabel.setText(self.tr("[选择的 Java 信息]"))
            self.noobMinMemLineEdit.setText("")
            self.noobMaxMemLineEdit.setText("")
            self.noobServerNameLineEdit.setText("")
        elif self.newServerStackedWidget.currentIndex() == 2:
            self.extendedJavaInfoLabel.setText(self.tr("[选择的 Java 信息]"))
            self.extendedMinMemLineEdit.setText("")
            self.extendedMaxMemLineEdit.setText("")
            self.extendedServerNameLineEdit.setText("")
            self.extendedOutputDeEncodingComboBox.setCurrentIndex(0)
            self.extendedInputDeEncodingComboBox.setCurrentIndex(0)
            self.JVMArgPlainTextEdit.setPlainText("")

        InfoBar.info(
            title=self.tr("功能提醒"),
            content=self.tr(
                "「新建服务器后立刻清空相关设置项」已被开启。\n这是一个强迫症功能。如果需要关闭，请转到设置页。"
            ),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self,
        )

    def _onSaveSuccess(self, exit0Msg: str, serverVariables=None, isEditing=False):
        """在保存成功后调用 postNewServerDispatcher"""
        self.postNewServerDispatcher(exit0Msg=exit0Msg)

    def saveNewServer(self):
        """保存服务器的分发器"""
        self.saveServer(configureServerVariables, isEditing=False)

    def saveServer(self, serverVariables, isEditing=False):
        """
        通用保存服务器方法
        Args:
            serverVariables: 服务器配置变量对象 (configureServerVariables 或 editServerVariables)
            isEditing: 是否为编辑模式
        """
        if serverVariables.serverType == "bedrock":
            self._saveBedrockServerAsync(serverVariables, isEditing)
        else:
            self._saveJavaServerAsync(serverVariables, isEditing)

    def _saveJavaServerAsync(self, serverVariables, isEditing=False):
        """异步保存Java版服务器"""
        exit0Msg = (
            self.tr("添加服务器「") + serverVariables.serverName + self.tr("」成功！")
            if not isEditing
            else self.tr("编辑服务器「") + serverVariables.serverName + self.tr("」成功！")
        )
        exit1Msg = (
            self.tr("添加服务器「") + serverVariables.serverName + self.tr("」失败！")
            if not isEditing
            else self.tr("编辑服务器「") + serverVariables.serverName + self.tr("」失败！")
        )
        exists_error_msg = self.tr("已存在同名服务器！请更改服务器名。")

        # 提前检查是否存在同名服务器 (仅新建时检查)
        if not isEditing and osp.exists(f"./Servers/{serverVariables.serverName}"):
            InfoBar.error(
                title=self.tr("失败"),
                content=exists_error_msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            return

        # 检查JVM参数防止意外无法启动服务器
        for arg in list(serverVariables.jvmArg):
            if arg == "" or arg == " ":
                serverVariables.jvmArg.remove(arg)

        extra_data = dict(serverVariables.extraData) if serverVariables.extraData else {}

        serverConfig = {
            "name": serverVariables.serverName,
            "core_file_name": serverVariables.coreFileName,
            "java_path": serverVariables.selectedJavaPath,
            "min_memory": serverVariables.minMem,
            "max_memory": serverVariables.maxMem,
            "memory_unit": serverVariables.memUnit,
            "jvm_arg": list(serverVariables.jvmArg),
            "output_decoding": serverVariables.consoleOutputDeEncoding,
            "input_encoding": serverVariables.consoleInputDeEncoding,
            "icon": "Grass.png",
            "server_type": serverVariables.serverType,
            "extra_data": extra_data,
        }

        # 是否显示Eula提示 (仅新建时显示)
        auto_accept_eula = cfg.get(cfg.acceptAllMojangEula) if not isEditing else False
        if auto_accept_eula:
            MinecraftEulaInfoBar = InfoBar(
                icon=FIF.INFO,
                title=self.tr("功能提醒"),
                content=self.tr(
                    "您开启了「创建时自动同意服务器的Eula」功能。\n如需要查看 Minecraft Eula，请点击右边的按钮。"
                ),
                orient=Qt.Horizontal,
                isClosable=True,
                duration=10000,
                position=InfoBarPosition.TOP,
                parent=self,
            )
            MinecraftEulaInfoBar.setCustomBackgroundColor("white", "#202020")
            MinecraftEulaInfoBar.addWidget(
                HyperlinkButton(
                    url="https://aka.ms/MinecraftEULA",
                    text="Eula",
                    parent=MinecraftEulaInfoBar,
                    icon=FIF.LINK,
                )
            )
            MinecraftEulaInfoBar.show()

        # 创建并启动保存线程
        self.javaSaveThread = JavaServerSaveThread(
            server_config=serverConfig,
            core_path=serverVariables.corePath,
            core_file_name=serverVariables.coreFileName,
            extra_data=extra_data,
            only_save_global=cfg.get(cfg.onlySaveGlobalServerConfig),
            auto_accept_eula=auto_accept_eula,
            exit0_msg=exit0Msg,
            exit1_msg=exit1Msg,
            exists_error_msg=exists_error_msg,
            parent=self,
        )
        self.javaSaveThread.success.connect(
            lambda msg: self._onJavaSaveSuccess(msg, serverVariables, isEditing)
        )
        self.javaSaveThread.failed.connect(self._onJavaSaveFailed)
        self.javaSaveThread.finished.connect(self._cleanupJavaSaveThread)
        self.javaSaveThread.start()

    @pyqtSlot(str)
    def _onJavaSaveSuccess(self, exit0Msg: str, serverVariables=None, isEditing=False):
        """Java版服务器保存成功回调"""
        if cfg.get(cfg.onlySaveGlobalServerConfig):
            InfoBar.info(
                title=self.tr("功能提醒"),
                content=self.tr(
                    "您在设置中开启了「只保存全局服务器设置」。\n将不会保存单独服务器设置。\n这有可能导致服务器迁移较为繁琐。"
                ),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

        self._onSaveSuccess(exit0Msg, serverVariables, isEditing)

    @pyqtSlot(str)
    def _onJavaSaveFailed(self, exit1Msg: str):
        """Java版服务器保存失败回调"""
        InfoBar.error(
            title=self.tr("失败"),
            content=exit1Msg,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self,
        )

    def _cleanupJavaSaveThread(self):
        """清理Java版保存线程"""
        self.javaSaveThread = None

    def _saveBedrockServerAsync(self, serverVariables, isEditing=False):
        """异步保存基岩版服务器"""
        exit0Msg = (
            self.tr("添加服务器「") + serverVariables.serverName + self.tr("」成功！")
            if not isEditing
            else self.tr("编辑服务器「") + serverVariables.serverName + self.tr("」成功！")
        )
        exit1Msg = (
            self.tr("添加服务器「") + serverVariables.serverName + self.tr("」失败！")
            if not isEditing
            else self.tr("编辑服务器「") + serverVariables.serverName + self.tr("」失败！")
        )
        exists_error_msg = self.tr("已存在同名服务器！请更改服务器名。")

        if not isEditing and osp.exists(f"./Servers/{serverVariables.serverName}"):
            InfoBar.error(
                title=self.tr("失败"),
                content=exists_error_msg,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            return

        extra_data = dict(serverVariables.extraData) if serverVariables.extraData else {}

        serverConfig = {
            "name": serverVariables.serverName,
            "core_file_name": serverVariables.coreFileName,
            "java_path": serverVariables.selectedJavaPath,
            "min_memory": serverVariables.minMem,
            "max_memory": serverVariables.maxMem,
            "memory_unit": serverVariables.memUnit,
            "jvm_arg": list(serverVariables.jvmArg),
            "output_decoding": serverVariables.consoleOutputDeEncoding,
            "input_encoding": serverVariables.consoleInputDeEncoding,
            "icon": "Grass.png",
            "server_type": serverVariables.serverType,
            "extra_data": extra_data,
        }

        if not isEditing:
            self.creatingBedrockStateToolTip = StateToolTip(
                self.tr("创建基岩版服务器"), self.tr("请稍后，正在创建..."), self
            )
            self.creatingBedrockStateToolTip.move(self.creatingBedrockStateToolTip.getSuitablePos())
            self.creatingBedrockStateToolTip.show()

            if hasattr(self, "bedrockSaveServerPrimaryPushBtn"):
                self.bedrockSaveServerPrimaryPushBtn.setEnabled(False)

        self.bedrockSaveThread = BedrockServerSaveThread(
            server_config=serverConfig,
            core_path=serverVariables.corePath,
            core_file_name=serverVariables.coreFileName,
            extra_data=extra_data,
            only_save_global=cfg.get(cfg.onlySaveGlobalServerConfig),
            exit0_msg=exit0Msg,
            exit1_msg=exit1Msg,
            exists_error_msg=exists_error_msg,
            parent=self,
        )
        self.bedrockSaveThread.success.connect(
            lambda msg: self._onBedrockSaveSuccess(msg, serverVariables, isEditing)
        )
        self.bedrockSaveThread.failed.connect(lambda msg: self._onBedrockSaveFailed(msg, isEditing))
        self.bedrockSaveThread.finished.connect(lambda: self._cleanupBedrockSaveThread(isEditing))
        self.bedrockSaveThread.start()

    @pyqtSlot(str)
    def _onBedrockSaveSuccess(self, exit0Msg: str, serverVariables=None, isEditing=False):
        """基岩版服务器保存成功回调"""
        if (
            not isEditing
            and hasattr(self, "creatingBedrockStateToolTip")
            and self.creatingBedrockStateToolTip
        ):
            self.creatingBedrockStateToolTip.setContent(self.tr("创建成功！"))
            self.creatingBedrockStateToolTip.setState(True)
            self.creatingBedrockStateToolTip = None

        if cfg.get(cfg.onlySaveGlobalServerConfig):
            InfoBar.info(
                title=self.tr("功能提醒"),
                content=self.tr(
                    "您在设置中开启了「只保存全局服务器设置」。\n将不会保存单独服务器设置。\n这有可能导致服务器迁移较为繁琐。"
                ),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

        self._onSaveSuccess(exit0Msg, serverVariables, isEditing)

    @pyqtSlot(str)
    def _onBedrockSaveFailed(self, exit1Msg: str, isEditing=False):
        """基岩版服务器保存失败回调"""
        if (
            not isEditing
            and hasattr(self, "creatingBedrockStateToolTip")
            and self.creatingBedrockStateToolTip
        ):
            self.creatingBedrockStateToolTip.setContent(self.tr("创建失败！"))
            self.creatingBedrockStateToolTip.setState(False)
            self.creatingBedrockStateToolTip = None

        InfoBar.error(
            title=self.tr("失败"),
            content=exit1Msg,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self,
        )

    def _cleanupBedrockSaveThread(self, isEditing=False):
        """清理基岩版保存线程"""
        if not isEditing and hasattr(self, "bedrockSaveServerPrimaryPushBtn"):
            self.bedrockSaveServerPrimaryPushBtn.setEnabled(True)
        self.bedrockSaveThread = None

    def addNewServerRollback(self, serverName):
        """新建服务器失败后的回滚"""
        if osp.exists(serverDir := f"./Servers/{serverName}/"):
            # 删除文件夹
            try:
                rmtree(serverDir)
            except Exception as e:
                MCSL2Logger.error(f"删除服务器文件夹失败: {e}")

            # 删除全局配置（通过服务器名精确查找）
            try:
                globalServerList = loads(readFile(r"./MCSL2/MCSL2_ServerList.json"))
                for i, srv in enumerate(globalServerList["MCSLServerList"]):
                    if srv["name"] == serverName:
                        globalServerList["MCSLServerList"].pop(i)
                        MCSL2Logger.info(f"已从全局配置中删除服务器: {serverName}")
                        break
                writeFile(r"./MCSL2/MCSL2_ServerList.json", dumps(globalServerList, indent=4))
            except Exception as e:
                MCSL2Logger.error(f"删除全局配置失败: {e}")

    def afterInstallerDownloadDone(self):
        if self.installerDownloadView is not None:
            self.installerDownloadView.hide()
            self.installerDownloadView.close()
            self.installerDownloadView.deleteLater()
            self.installerDownloadView = None

        self.installerLogViewer.show()

    @pyqtSlot(bool, str)
    def afterInstallingForge(self, installFinished, message=""):
        if self.installerLogViewer:
            self.installerLogViewer.hide()
            self.installerLogViewer.close()
            self.installerLogViewer.deleteLater()

        if self.installerDownloadView is not None:
            self.installerDownloadView.hide()
            self.installerDownloadView.close()
            self.installerDownloadView.deleteLater()
            self.installerDownloadView = None

        if installFinished:
            self.installingForgeStateToolTip.setContent(self.tr("安装成功！"))
            self.installingForgeStateToolTip.setState(True)
            self.installingForgeStateToolTip = None
        else:
            print("Forge 安装失败: " + message)
            self.installingForgeStateToolTip.setContent(self.tr("怪，安装失败！" + message))
            self.installingForgeStateToolTip.setState(True)
            # self.installingForgeStateToolTip = None
            self.addNewServerRollback(configureServerVariables.serverName)
            MCSL2Logger.warning(f"{self.__class__.__name__} 回滚")
        if hasattr(
            self, "forgeInstaller"
        ):  # 有可能创建forgeInstaller就抛出了异常(如invalid forge installer等),故需要判断是否初始化
            del self.forgeInstaller
        self._clearNewServerInputs()

    def hideForgeInstallerHelper(self):
        self.installingForgeInfoBar = InfoBar(
            icon=FIF.DEVELOPER_TOOLS,
            title=self.tr("已隐藏安装 Forge 窗口"),
            content=self.tr("仍在安装中，点击按钮恢复窗口..."),
            orient=Qt.Horizontal,
            isClosable=False,
            duration=-1,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self,
        )
        self.installingForgeInfoBar.setCustomBackgroundColor("white", "#202020")
        showForgeInstallMsgBoxBtn = PushButton()
        showForgeInstallMsgBoxBtn.setText(self.tr("恢复"))
        showForgeInstallMsgBoxBtn.clicked.connect(self.installerLogViewer.show)
        showForgeInstallMsgBoxBtn.clicked.connect(self.installingForgeInfoBar.close)
        self.installingForgeInfoBar.addWidget(showForgeInstallMsgBoxBtn)
        self.installingForgeInfoBar.show()

    def afterInstallingNeoForge(self, installFinished, message=""):
        """Handle NeoForge installation completion"""
        if self.installerLogViewer:
            self.installerLogViewer.hide()
            self.installerLogViewer.close()
            self.installerLogViewer.deleteLater()

        if self.installerDownloadView is not None:
            self.installerDownloadView.hide()
            self.installerDownloadView.close()
            self.installerDownloadView.deleteLater()
            self.installerDownloadView = None

        if installFinished:
            self.installingForgeStateToolTip.setContent(self.tr("安装成功！"))
            self.installingForgeStateToolTip.setState(True)
            self.installingForgeStateToolTip = None
        else:
            print("NeoForge 安装失败: " + message)
            self.installingForgeStateToolTip.setContent(self.tr("怪，安装失败！" + message))
            self.installingForgeStateToolTip.setState(True)
            self.addNewServerRollback(configureServerVariables.serverName)
            MCSL2Logger.warning(f"{self.__class__.__name__} 回滚")
        if hasattr(self, "neoforgeInstaller"):
            del self.neoforgeInstaller
        self._clearNewServerInputs()

    # ==================== ModPack Importer Methods ====================

    def _initModPackImporter(self):
        """初始化ModPackImporter相关变量和UI"""
        # Importer相关变量
        self.importer_selectedZipFile: str = ""
        self.importer_selectedCore: str = ""
        self.importer_serverPath: str = ""
        self.importer_jarFiles: List[str] = []
        self.importer_needForgeInstall: bool = False
        self.importer_forgeInstallerCore: Optional[str] = None
        self.importer_extractThread: Optional[ExtractModpackThread] = None
        self.importer_stateTooltip: Optional[StateToolTip] = None
        self.importer_totalStep = 0

        # 创建UI页面
        self._initImporterUI()

    def _initImporterUI(self):
        """初始化Importer的UI步骤"""
        # 创建ImportPageWidget
        self.importer_pageWidget = ImportPageWidget(self.importNewServerStackWidget)
        self.importNewServerStackWidget.addWidget(self.importer_pageWidget)

        # Step 1: 选择整合包压缩文件
        self.importer_totalStep += 1
        self.importer_importWidget = ImportSingleWidget(
            self.importer_totalStep, "选择整合包压缩文件 (.zip)", "选择文件"
        )
        if self.importer_totalStep > 1:
            self.importer_importWidget.setEnabled(False)
        self.importer_pageWidget.typeWidgetLayout.addWidget(self.importer_importWidget)

        # Step 2: 配置服务器参数
        self.importer_totalStep += 1
        self.importer_confirmWidget = ConfirmArgumentsWidget(
            self.importer_totalStep, "设置服务器参数"
        )
        if self.importer_totalStep > 1:
            self.importer_confirmWidget.setEnabled(False)
        self.importer_pageWidget.typeWidgetLayout.addWidget(self.importer_confirmWidget)

        # Step 3: 保存配置
        self.importer_totalStep += 1
        self.importer_saveWidget = SaveWidget(self.importer_totalStep)
        if self.importer_totalStep > 1:
            self.importer_saveWidget.setEnabled(False)
        self.importer_pageWidget.typeWidgetLayout.addWidget(self.importer_saveWidget)

        # 连接信号槽
        self._connectImporterSlots()

        # 直接显示ModPackImporter页面
        self.importNewServerStackWidget.setCurrentIndex(0)

    def _connectImporterSlots(self):
        """连接Importer的信号槽"""
        # Step 1 完成后，解压并检测jar文件
        self.importer_importWidget.fileImportedSignal.connect(self._importerOnZipFileSelected)

        # 连接各步骤的完成信号
        self.importer_importWidget.finishSignal.connect(self._importerOnImportWidgetFinished)
        self.importer_confirmWidget.finishSignal.connect(self.importer_saveWidget.setEnabled)

        # 连接Java相关按钮
        self.importer_confirmWidget.selectJavaPrimaryPushBtn.clicked.connect(
            self._importerAddJavaManually
        )
        self.importer_confirmWidget.autoDetectJavaBtn.clicked.connect(self._importerAutoDetectJava)
        self.importer_confirmWidget.javaListBtn.clicked.connect(self._importerShowJavaList)

        # 连接输入框的文本变化信号
        self.importer_confirmWidget.javaTextEdit.textChanged.connect(
            self._importerCheckConfirmWidgetCompletion
        )
        self.importer_confirmWidget.minMemLineEdit.textChanged.connect(
            self._importerCheckConfirmWidgetCompletion
        )
        self.importer_confirmWidget.maxMemLineEdit.textChanged.connect(
            self._importerCheckConfirmWidgetCompletion
        )

        # 连接保存按钮
        self.importer_saveWidget.saveSaveServerBtn.clicked.connect(self._importerFinishSave)
        self.javaVersionLabelItems.append(self.importer_confirmWidget.javaTextEdit)

    def _importerShowJavaList(self):
        """显示Java列表选择页面"""
        self.noobJavaListPushBtn.click()

    @pyqtSlot(str)
    def _importerOnJavaSelected(self, java_path: str):
        """当选择了Java后"""
        self.importer_confirmWidget.javaTextEdit.setPlainText(java_path)
        # 检查是否可以完成此步骤
        self._importerCheckConfirmWidgetCompletion()

    def _importerCheckConfirmWidgetCompletion(self):
        """检查配置参数是否完成"""
        # 检查Java路径是否已填写
        java_text = self.importer_confirmWidget.javaTextEdit.toPlainText().strip()
        # 检查内存是否已填写
        min_mem = self.importer_confirmWidget.minMemLineEdit.text().strip()
        max_mem = self.importer_confirmWidget.maxMemLineEdit.text().strip()

        # 如果所有必要项都已填写，则标记为完成
        if java_text and min_mem and max_mem:
            try:
                # 验证内存是数字且合理
                min_mem_int = int(min_mem)
                max_mem_int = int(max_mem)
                # 检查内存值合理性：最小内存不为0，最大内存>=最小内存
                if min_mem_int > 0 and max_mem_int >= min_mem_int:
                    self.importer_confirmWidget.setFinished()
            except ValueError:
                pass

    def _importerAddJavaManually(self):
        """手动添加Java"""
        selectedJavaPath = str(
            QFileDialog.getOpenFileName(
                self,
                self.tr("选择 java.exe 程序"),
                getcwd(),
                self.tr("Java 主程序 (java.exe)"),
            )[0]
        )
        if selectedJavaPath != "":
            if v := javaDetector.getJavaVersion(selectedJavaPath):
                currentJavaPaths = configureServerVariables.javaPath
                if javaDetector.Java(selectedJavaPath, v) not in currentJavaPaths:
                    currentJavaPaths.append(javaDetector.Java(selectedJavaPath, v))
                    javaDetector.sortJavaList(currentJavaPaths)
                    # 自动设置到javaTextEdit
                    self.importer_confirmWidget.javaTextEdit.setPlainText(selectedJavaPath)
                    InfoBar.success(
                        title=self.tr("已添加"),
                        content=self.tr("Java路径: ")
                        + selectedJavaPath
                        + self.tr("\n版本: ")
                        + v
                        + self.tr("\n但你还需要继续到 Java 列表中选取。"),
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self,
                    )
                else:
                    InfoBar.warning(
                        title=self.tr("未添加"),
                        content=self.tr(
                            "此 Java 已被添加过，也有可能是自动查找 Java 时已经搜索到了。请检查 Java 列表。"  # noqa: E501
                        ),
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=4848,
                        parent=self,
                    )
                javaDetector.saveJavaList(currentJavaPaths)
            else:
                InfoBar.error(
                    title=self.tr("添加失败"),
                    content=self.tr("此 Java 无效！"),
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self,
                )
        else:
            InfoBar.warning(
                title=self.tr("未添加"),
                content=self.tr("你并没有选择 Java。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )

    def _importerAutoDetectJava(self):
        """自动查找Java（直接调用共用方法）"""
        self.autoDetectJava()

    def _importerOnImportWidgetFinished(self, finished: bool):
        """当导入Widget完成时，不自动启用下一步，等待解压完成"""
        pass

    @pyqtSlot(str)
    def _importerOnZipFileSelected(self, zipFilePath: str):
        """当用户选择了整合包文件后"""
        try:
            # 如果之前有解压的文件，先清理
            if self.importer_serverPath:
                self._importerCleanupServerPath()
            
            self.importer_selectedZipFile = zipFilePath
            # 显示提示信息
            msgBox = MessageBox(
                self.tr("提示"),
                self.tr(
                    "请注意：\n"
                    "1. 目前仅支持 .zip 格式的整合包文件\n"
                    "2. 如果是模组整合包，请确保下载的是服务器专用包(ServerPack)\n"
                    "3. 整合包将被解压到自动生成的服务器目录\n\n"
                    "继续导入吗？"
                ),
                self,
            )
            if msgBox.exec():
                # 用户点击确定，开始解压和检测
                self._importerStartExtractModpack()
            else:
                # 用户取消，重置状态
                self.importer_importWidget.setNotFinished()
        except Exception as e:
            MessageBox(
                self.tr("错误"), self.tr("处理整合包时出错: {0}").format(str(e)), self
            ).exec()
            self.importer_importWidget.setNotFinished()

    def _importerStartExtractModpack(self):
        """开始解压整合包(异步)"""
        # 生成服务器目录
        self.importer_serverPath = self._importerGenerateServerPath()

        # 显示状态提示
        self.importer_stateTooltip = StateToolTip(
            self.tr("解压整合包"), self.tr("正在解压整合包并检测核心文件..."), self
        )
        self.importer_stateTooltip.move(self.importer_stateTooltip.getSuitablePos())
        self.importer_stateTooltip.show()

        # 创建并启动后台线程
        self.importer_extractThread = ExtractModpackThread(
            self.importer_selectedZipFile, self.importer_serverPath
        )
        self.importer_extractThread.success.connect(self._importerOnExtractSuccess)
        self.importer_extractThread.failed.connect(self._importerOnExtractFailed)
        self.importer_extractThread.finished.connect(self._importerCleanupExtractThread)
        self.importer_extractThread.start()

    @pyqtSlot(str, list)
    def _importerOnExtractSuccess(self, server_path: str, jar_files: list):
        """解压成功后的处理"""
        self.importer_jarFiles = jar_files

        # 关闭状态提示
        if self.importer_stateTooltip:
            self.importer_stateTooltip.setContent(self.tr("解压完成 ✓"))
            self.importer_stateTooltip.setState(True)
            self.importer_stateTooltip = None

        if len(self.importer_jarFiles) == 0:
            MessageBox(
                self.tr("提示"),
                self.tr("未在整合包中找到核心文件(.jar)。\n\n")
                + self.tr("整合包已解压到: ")
                + self.importer_serverPath
                + "\n\n"
                + self.tr("请稍后手动下载核心文件或选择已有核心。\n")
                + self.tr("核心版本需要与整合包对应的游戏版本一致。"),
                self,
            ).exec()
            # 即使没有jar文件，也允许继续
            self.importer_confirmWidget.setEnabled(True)

        elif len(self.importer_jarFiles) == 1:
            # 只有一个jar文件，自动选择
            self.importer_selectedCore = self.importer_jarFiles[0]
            MessageBox(
                self.tr("检测到核心文件"),
                self.tr(
                    "在整合包中自动检测到核心文件:\n{0}\n\n将使用此文件作为服务器核心。"
                ).format(self.importer_jarFiles[0]),
                self,
            ).exec()
            self._importerCheckForgeInstaller()

        else:
            # 多个jar文件，选择第一个并提示
            self.importer_selectedCore = self.importer_jarFiles[0]
            jar_list = "\n".join([f"  • {jar}" for jar in self.importer_jarFiles])
            MessageBox(
                self.tr("检测到多个jar文件"),
                self.tr("在整合包中检测到以下jar文件:\n\n{0}\n\n").format(jar_list)
                + self.tr("将自动选择第一个文件 '{0}' 作为服务器核心。\n").format(
                    self.importer_jarFiles[0]
                )
                + self.tr("如需更换，请在服务器目录中手动修改。"),
                self,
            ).exec()
            self._importerCheckForgeInstaller()

        # 启用配置参数阶段
        self.importer_confirmWidget.setEnabled(True)

    @pyqtSlot(str)
    def _importerOnExtractFailed(self, error_msg: str):
        """解压失败后的处理"""
        # 关闭状态提示
        if self.importer_stateTooltip:
            self.importer_stateTooltip.setContent(self.tr("解压失败 ✗"))
            self.importer_stateTooltip.setState(False)
            self.importer_stateTooltip = None

        MessageBox(
            self.tr("错误"), self.tr("解压整合包时出错:\n{0}").format(error_msg), self
        ).exec()
        # 出错时清理已创建的目录
        self._importerCleanupServerPath()
        self.importer_importWidget.setNotFinished()

    def _importerCleanupExtractThread(self):
        """清理解压线程"""
        if self.importer_extractThread:
            self.importer_extractThread.deleteLater()
            self.importer_extractThread = None

    def _importerCleanupServerPath(self):
        """清理解压的服务器目录"""
        if self.importer_serverPath and os.path.exists(self.importer_serverPath):
            try:
                shutil.rmtree(self.importer_serverPath)
                MCSL2Logger.info(f"Cleaned up importer server path: {self.importer_serverPath}")
            except Exception as e:
                MCSL2Logger.warning(f"Failed to cleanup importer server path: {e}")
        # 重置相关变量
        self.importer_serverPath = ""
        self.importer_selectedCore = ""
        self.importer_jarFiles = []
        self.importer_needForgeInstall = False
        self.importer_forgeInstallerCore = None

    def _importerGenerateServerPath(self) -> str:
        """生成服务器目录路径"""
        base_path = "Servers\\Server"
        counter = 1

        # 检查Servers目录是否存在
        if not os.path.exists("Servers"):
            os.makedirs("Servers", exist_ok=True)

        while True:
            if counter == 1:
                path = base_path
            else:
                path = f"{base_path}{counter}"

            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                return path
            elif len(os.listdir(path)) == 0:
                return path
            counter += 1

    def _importerCheckForgeInstaller(self):
        """检查是否为Forge/NeoForge安装器"""
        core_path = os.path.join(self.importer_serverPath, self.importer_selectedCore)

        # 检查NeoForge安装器(优先检查，因为NeoForge也可能被Forge检测识别)
        neoforge_result = NeoForgeInstaller.isPossibleNeoForgeInstaller(core_path)
        if neoforge_result:
            msgBox = MessageBox(
                self.tr("检测到NeoForge安装器"),
                self.tr("您选择的服务端疑似是NeoForge安装器\n\n")
                + self.tr("MC版本: ")
                + str(neoforge_result[0])
                + "\n"
                + self.tr("NeoForge版本: ")
                + str(neoforge_result[1])
                + "\n\n"
                + self.tr("是否展开安装？\n")
                + self.tr("注意: 如果不展开安装，服务器可能无法正常启动！"),
                self,
            )
            if msgBox.exec():
                self.importer_needForgeInstall = True
                self.importer_forgeInstallerCore = self.importer_selectedCore
                # 设置serverType
                configureServerVariables.serverType = "neoforge"
                MessageBox(
                    self.tr("提示"),
                    self.tr("NeoForge自动安装将在您完成服务器配置后执行。\n请继续配置服务器参数。"),
                    self,
                ).exec()
            # 无论用户是否选择安装，都启用下一步
            self.importer_confirmWidget.setEnabled(True)
            return

        # 检查Forge安装器
        forge_result = ForgeInstaller.isPossibleForgeInstaller(core_path)
        if forge_result:
            msgBox = MessageBox(
                self.tr("检测到Forge安装器"),
                self.tr("您选择的服务端疑似是Forge安装器\n\n")
                + self.tr("MC版本: ")
                + str(forge_result[0])
                + "\n"
                + self.tr("Forge版本: ")
                + str(forge_result[1])
                + "\n\n"
                + self.tr("是否展开安装？\n")
                + self.tr("注意: 如果不展开安装，服务器可能无法正常启动！"),
                self,
            )
            if msgBox.exec():
                self.importer_needForgeInstall = True
                self.importer_forgeInstallerCore = self.importer_selectedCore
                # 设置serverType
                configureServerVariables.serverType = "forge"
                MessageBox(
                    self.tr("提示"),
                    self.tr("Forge自动安装将在您完成服务器配置后执行。\n请继续配置服务器参数。"),
                    self,
                ).exec()

        # 启用下一步
        self.importer_confirmWidget.setEnabled(True)

    def _importerFinishSave(self):
        """完成importer的保存，将数据转换到configureServerVariables并调用共用逻辑"""
        # 先检查服务器名称合法性
        serverName = self.importer_saveWidget.saveServerNameLineEdit.text().strip()
        nameCheck = ServerValidator().checkServerNameSet(serverName, configureServerVariables)
        if nameCheck[1] != 0:  # 如果检查出错
            InfoBar.error(
                title=self.tr("保存失败"),
                content=nameCheck[0],
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self,
            )
            return

        # 将importer的数据转换到configureServerVariables
        configureServerVariables.selectedJavaPath = (
            self.importer_confirmWidget.javaTextEdit.toPlainText().strip()
        )
        configureServerVariables.minMem = self.importer_confirmWidget.minMemLineEdit.text().strip()
        configureServerVariables.maxMem = self.importer_confirmWidget.maxMemLineEdit.text().strip()
        configureServerVariables.memUnit = "M"  # importer默认使用M
        configureServerVariables.serverName = serverName
        configureServerVariables.corePath = (
            osp.abspath(os.path.join(self.importer_serverPath, self.importer_selectedCore))
            if self.importer_selectedCore
            else ""
        )
        configureServerVariables.coreFileName = self.importer_selectedCore
        configureServerVariables.jvmArg = (
            self.importer_confirmWidget.jvmArgPlainTextEdit.toPlainText().strip().split(" ")
        )  # noqa: E501
        outputIndex = self.importer_confirmWidget.outputComboBox.currentIndex()
        inputIndex = self.importer_confirmWidget.inputComboBox.currentIndex()
        configureServerVariables.consoleOutputDeEncoding = (
            configureServerVariables.consoleDeEncodingList[outputIndex + 1]
        )
        configureServerVariables.consoleInputDeEncoding = (
            configureServerVariables.consoleDeEncodingList[inputIndex + 1]
        )

        # 设置extraData，标记这是从整合包导入的
        configureServerVariables.extraData = {
            "extracted_from_zip": True,
            "temp_dir": self.importer_serverPath,
        }

        # 调用共用的finishNewServer逻辑
        # 模拟noob模式（currentNewServerType = 1）
        self.finishNewServer()

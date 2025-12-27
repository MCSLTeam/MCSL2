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
Schedule Tasks Page - 定时任务页面
支持服务器输出匹配响应和Cron定时任务
"""

import json
import re
from datetime import datetime
from os import path as osp
from typing import Dict, List, Optional

from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QFileDialog,
)
from qfluentwidgets import (
    PushButton,
    PrimaryPushButton,
    LineEdit,
    ComboBox,
    StrongBodyLabel,
    SubtitleLabel,
    SimpleCardWidget,
    BodyLabel,
    TransparentPushButton,
    SwitchButton,
    ToolButton,
    SpinBox,
    CheckBox,
    FluentIcon as FIF,
    InfoBar,
    InfoBarPosition,
    MessageBox,
)

from MCSL2Lib.ProgramControllers.interfaceController import MySmoothScrollArea
from MCSL2Lib.utils import MCSL2Logger, readFile, writeFile
from MCSL2Lib.variables import ServerVariables
from croniter import croniter


class CronGeneratorDialog(MessageBox):
    """Cron表达式生成器对话框"""

    def __init__(self, parent=None, current_cron: str = ""):
        super().__init__("Cron表达式生成器", "", parent)
        self.current_cron = current_cron
        self.generated_cron = ""
        self.setupUI()

    def setupUI(self):
        self.textLayout.setSpacing(12)

        # 模式切换
        modeLayout = QHBoxLayout()
        modeLayout.addWidget(StrongBodyLabel("生成模式:", self))
        self.modeCombo = ComboBox(self)
        self.modeCombo.addItems(["简易模式", "专业模式"])
        self.modeCombo.currentIndexChanged.connect(self.onModeChanged)
        modeLayout.addWidget(self.modeCombo, 1)
        self.textLayout.addLayout(modeLayout)

        # 简易模式容器
        self.simpleWidget = QWidget(self)
        simpleLayout = QVBoxLayout(self.simpleWidget)
        simpleLayout.setContentsMargins(0, 0, 0, 0)
        simpleLayout.setSpacing(8)

        # 预设选项
        presetLayout = QHBoxLayout()
        presetLayout.addWidget(StrongBodyLabel("时间间隔:", self))
        self.presetCombo = ComboBox(self)
        self.presetCombo.addItems([
            "自定义",
            "每分钟",
            "每5分钟",
            "每15分钟",
            "每30分钟",
            "每小时",
            "每2小时",
            "每6小时",
            "每12小时",
            "每天",
            "每周",
            "每月",
        ])
        self.presetCombo.currentIndexChanged.connect(self.onPresetChanged)
        presetLayout.addWidget(self.presetCombo, 1)
        simpleLayout.addLayout(presetLayout)

        # 自定义时间选项（默认隐藏）
        self.customTimeWidget = QWidget(self)
        customTimeLayout = QGridLayout(self.customTimeWidget)
        customTimeLayout.setContentsMargins(0, 0, 0, 0)

        customTimeLayout.addWidget(StrongBodyLabel("每隔:", self), 0, 0)
        self.intervalSpin = SpinBox(self)
        self.intervalSpin.setRange(1, 999)
        self.intervalSpin.setValue(1)
        customTimeLayout.addWidget(self.intervalSpin, 0, 1)

        self.unitCombo = ComboBox(self)
        self.unitCombo.addItems(["分钟", "小时", "天"])
        customTimeLayout.addWidget(self.unitCombo, 0, 2)

        self.customTimeWidget.setVisible(False)
        simpleLayout.addWidget(self.customTimeWidget)

        # 特定时间（用于每天/每周）
        self.specificTimeWidget = QWidget(self)
        specificTimeLayout = QHBoxLayout(self.specificTimeWidget)
        specificTimeLayout.setContentsMargins(0, 0, 0, 0)

        specificTimeLayout.addWidget(StrongBodyLabel("在:", self))
        self.hourSpin = SpinBox(self)
        self.hourSpin.setRange(0, 23)
        self.hourSpin.setValue(0)
        specificTimeLayout.addWidget(self.hourSpin)
        specificTimeLayout.addWidget(BodyLabel("时", self))

        self.minuteSpin = SpinBox(self)
        self.minuteSpin.setRange(0, 59)
        self.minuteSpin.setValue(0)
        specificTimeLayout.addWidget(self.minuteSpin)
        specificTimeLayout.addWidget(BodyLabel("分", self))
        specificTimeLayout.addStretch(1)

        self.specificTimeWidget.setVisible(False)
        simpleLayout.addWidget(self.specificTimeWidget)

        # 星期选择（用于每周）
        self.weekdayWidget = QWidget(self)
        weekdayLayout = QVBoxLayout(self.weekdayWidget)
        weekdayLayout.setContentsMargins(0, 0, 0, 0)

        weekdayLayout.addWidget(StrongBodyLabel("星期:", self))
        weekdayCheckLayout = QHBoxLayout()
        self.weekdayChecks = []
        for day in ["一", "二", "三", "四", "五", "六", "日"]:
            check = CheckBox(day, self)
            self.weekdayChecks.append(check)
            weekdayCheckLayout.addWidget(check)
        weekdayLayout.addLayout(weekdayCheckLayout)

        self.weekdayWidget.setVisible(False)
        simpleLayout.addWidget(self.weekdayWidget)

        self.textLayout.addWidget(self.simpleWidget)

        # 专业模式容器
        self.advancedWidget = QWidget(self)
        advancedLayout = QVBoxLayout(self.advancedWidget)
        advancedLayout.setContentsMargins(0, 0, 0, 0)
        advancedLayout.setSpacing(8)

        advancedLayout.addWidget(BodyLabel("Cron格式: 分 时 日 月 周", self))

        # 分钟
        minLayout = QHBoxLayout()
        minLayout.addWidget(StrongBodyLabel("分钟:", self))
        self.minEdit = LineEdit(self)
        self.minEdit.setPlaceholderText("0-59 或 * 或 */5")
        minLayout.addWidget(self.minEdit, 1)
        advancedLayout.addLayout(minLayout)

        # 小时
        hourLayout = QHBoxLayout()
        hourLayout.addWidget(StrongBodyLabel("小时:", self))
        self.hourEdit = LineEdit(self)
        self.hourEdit.setPlaceholderText("0-23 或 * 或 */2")
        hourLayout.addWidget(self.hourEdit, 1)
        advancedLayout.addLayout(hourLayout)

        # 日
        dayLayout = QHBoxLayout()
        dayLayout.addWidget(StrongBodyLabel("日期:", self))
        self.dayEdit = LineEdit(self)
        self.dayEdit.setPlaceholderText("1-31 或 *")
        dayLayout.addWidget(self.dayEdit, 1)
        advancedLayout.addLayout(dayLayout)

        # 月
        monthLayout = QHBoxLayout()
        monthLayout.addWidget(StrongBodyLabel("月份:", self))
        self.monthEdit = LineEdit(self)
        self.monthEdit.setPlaceholderText("1-12 或 *")
        monthLayout.addWidget(self.monthEdit, 1)
        advancedLayout.addLayout(monthLayout)

        # 周
        weekLayout = QHBoxLayout()
        weekLayout.addWidget(StrongBodyLabel("星期:", self))
        self.weekEdit = LineEdit(self)
        self.weekEdit.setPlaceholderText("0-6 (0=周日) 或 *")
        weekLayout.addWidget(self.weekEdit, 1)
        advancedLayout.addLayout(weekLayout)

        # 专业模式帮助文本
        helpText = BodyLabel(
            "提示: * 表示任意值 | */n 表示每n单位 | 1,3,5 表示列表 | 1-5 表示范围",
            self
        )
        helpText.setWordWrap(True)
        advancedLayout.addWidget(helpText)

        self.advancedWidget.setVisible(False)
        self.textLayout.addWidget(self.advancedWidget)

        # 预览
        previewLayout = QVBoxLayout()
        previewLayout.addWidget(StrongBodyLabel("生成的表达式:", self))
        self.previewEdit = LineEdit(self)
        self.previewEdit.setReadOnly(True)
        self.previewEdit.setPlaceholderText("表达式将在这里显示")
        previewLayout.addWidget(self.previewEdit)
        self.textLayout.addLayout(previewLayout)

        # 生成按钮
        generateBtn = PrimaryPushButton("生成并应用", self)
        generateBtn.clicked.connect(self.generateCron)
        self.textLayout.addWidget(generateBtn)

        self.widget.setFixedWidth(600)

        # 如果有当前表达式，尝试解析
        if self.current_cron:
            self.previewEdit.setText(self.current_cron)

    def onModeChanged(self, index: int):
        """模式切换"""
        is_simple = index == 0
        self.simpleWidget.setVisible(is_simple)
        self.advancedWidget.setVisible(not is_simple)

    def onPresetChanged(self, index: int):
        """预设选项改变"""
        preset_map = {
            0: None,  # 自定义
            1: "* * * * *",  # 每分钟
            2: "*/5 * * * *",  # 每5分钟
            3: "*/15 * * * *",  # 每15分钟
            4: "*/30 * * * *",  # 每30分钟
            5: "0 * * * *",  # 每小时
            6: "0 */2 * * *",  # 每2小时
            7: "0 */6 * * *",  # 每6小时
            8: "0 */12 * * *",  # 每12小时
            9: "0 0 * * *",  # 每天
            10: "0 0 * * 0",  # 每周
            11: "0 0 1 * *",  # 每月
        }

        # 显示/隐藏自定义选项
        self.customTimeWidget.setVisible(index == 0)
        self.specificTimeWidget.setVisible(index in [9, 10])
        self.weekdayWidget.setVisible(index == 10)

        if index in preset_map and preset_map[index]:
            self.previewEdit.setText(preset_map[index])
        elif index == 0:
            self.updateCustomCron()

    def updateCustomCron(self):
        """更新自定义Cron表达式"""
        interval = self.intervalSpin.value()
        unit = self.unitCombo.currentIndex()

        if unit == 0:  # 分钟
            cron = f"*/{interval} * * * *"
        elif unit == 1:  # 小时
            cron = f"0 */{interval} * * *"
        else:  # 天
            cron = f"0 0 */{interval} * *"

        self.previewEdit.setText(cron)

    def generateCron(self):
        """生成Cron表达式"""
        if self.modeCombo.currentIndex() == 0:
            # 简易模式
            preset_index = self.presetCombo.currentIndex()

            if preset_index == 0:  # 自定义
                self.updateCustomCron()
            elif preset_index == 9:  # 每天
                hour = self.hourSpin.value()
                minute = self.minuteSpin.value()
                cron = f"{minute} {hour} * * *"
                self.previewEdit.setText(cron)
            elif preset_index == 10:  # 每周
                hour = self.hourSpin.value()
                minute = self.minuteSpin.value()
                days = []
                for i, check in enumerate(self.weekdayChecks):
                    if check.isChecked():
                        days.append(str((i + 1) % 7))  # 转换为0-6格式
                if not days:
                    InfoBar.warning("", "请至少选择一天", parent=self, isClosable=False)
                    return
                cron = f"{minute} {hour} * * {','.join(days)}"
                self.previewEdit.setText(cron)

            self.generated_cron = self.previewEdit.text()
        else:
            # 专业模式
            minute = self.minEdit.text().strip() or "*"
            hour = self.hourEdit.text().strip() or "*"
            day = self.dayEdit.text().strip() or "*"
            month = self.monthEdit.text().strip() or "*"
            week = self.weekEdit.text().strip() or "*"

            cron = f"{minute} {hour} {day} {month} {week}"
            self.previewEdit.setText(cron)
            self.generated_cron = cron

        # 验证表达式
        try:
            croniter(self.generated_cron)
            InfoBar.success(
                "生成成功",
                f"Cron表达式: {self.generated_cron}",
                parent=self,
                isClosable=False,
                duration=2000,
            )
            self.accept()
        except Exception as e:
            InfoBar.error(
                "表达式无效",
                f"{str(e)}",
                parent=self,
                isClosable=False,
                duration=3000,
            )

    def getCronExpression(self) -> str:
        """获取生成的Cron表达式"""
        return self.generated_cron


class TaskCardWidget(SimpleCardWidget):
    """单个任务卡片"""

    editRequested = pyqtSignal(dict)
    deleteRequested = pyqtSignal(str)
    toggleRequested = pyqtSignal(str, bool)

    def __init__(self, task_data: dict, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.task_id = task_data.get("id", "")
        self.setupUI()

    def setupUI(self):
        self.setMinimumHeight(120)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # 标题行
        titleLayout = QHBoxLayout()
        titleLayout.setSpacing(10)

        self.nameLabel = SubtitleLabel(self.task_data.get("name", "未命名任务"), self)
        titleLayout.addWidget(self.nameLabel)

        self.enableSwitch = SwitchButton(self)
        self.enableSwitch.setChecked(self.task_data.get("enabled", True))
        self.enableSwitch.checkedChanged.connect(
            lambda checked: self.toggleRequested.emit(self.task_id, checked)
        )
        titleLayout.addWidget(self.enableSwitch)

        titleLayout.addStretch(1)
        layout.addLayout(titleLayout)

        # 信息行
        infoLayout = QVBoxLayout()
        infoLayout.setSpacing(4)

        task_type = self.task_data.get("type", "pattern")
        if task_type == "pattern":
            pattern = self.task_data.get("pattern", "")
            self.infoLabel1 = BodyLabel(f"类型: 输出匹配 | 模式: {pattern}", self)
        else:
            cron = self.task_data.get("cron", "")
            self.infoLabel1 = BodyLabel(f"类型: Cron定时 | 表达式: {cron}", self)

        action = self.task_data.get("action", "command")
        action_text = {
            "command": "发送指令",
            "save": "保存存档",
            "stop": "关闭服务器",
            "start": "开启服务器",
        }.get(action, action)
        action_value = self.task_data.get("value", "")
        self.infoLabel2 = BodyLabel(f"动作: {action_text} | 参数: {action_value}", self)

        infoLayout.addWidget(self.infoLabel1)
        infoLayout.addWidget(self.infoLabel2)
        layout.addLayout(infoLayout)

        # 按钮行
        btnLayout = QHBoxLayout()
        btnLayout.setSpacing(8)
        btnLayout.addStretch(1)

        self.editBtn = TransparentPushButton(FIF.EDIT, "编辑", self)
        self.editBtn.clicked.connect(lambda: self.editRequested.emit(self.task_data))
        btnLayout.addWidget(self.editBtn)

        self.deleteBtn = TransparentPushButton(FIF.DELETE, "删除", self)
        self.deleteBtn.clicked.connect(lambda: self.deleteRequested.emit(self.task_id))
        btnLayout.addWidget(self.deleteBtn)

        layout.addLayout(btnLayout)


class TaskEditorDialog(MessageBox):
    """任务编辑对话框"""

    def __init__(self, parent=None, task_data: Optional[dict] = None):
        self.task_data = task_data or {}
        self.is_edit_mode = task_data is not None
        self.cron_info_bar = None

        title = "编辑任务" if self.is_edit_mode else "新建任务"
        super().__init__(title, "", parent)

        self.setupUI()
        self.loadTaskData()
        
        # 绑定关闭信号，确保InfoBar随对话框关闭
        self.finished.connect(self._onDialogClose)

    def setupUI(self):
        # 清空默认内容
        self.textLayout.setSpacing(12)

        # 任务名称
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(StrongBodyLabel("任务名称:", self))
        self.nameEdit = LineEdit(self)
        self.nameEdit.setPlaceholderText("输入任务名称")
        nameLayout.addWidget(self.nameEdit, 1)
        self.textLayout.addLayout(nameLayout)

        # 任务类型
        typeLayout = QHBoxLayout()
        typeLayout.addWidget(StrongBodyLabel("任务类型:", self))
        self.typeCombo = ComboBox(self)
        self.typeCombo.addItems(["输出匹配", "Cron定时"])
        self.typeCombo.currentIndexChanged.connect(self.onTypeChanged)
        typeLayout.addWidget(self.typeCombo, 1)
        self.textLayout.addLayout(typeLayout)

        # 匹配模式/Cron表达式（动态切换）
        self.triggerLayout = QHBoxLayout()
        self.triggerLabel = StrongBodyLabel("匹配模式:", self)
        self.triggerLayout.addWidget(self.triggerLabel)
        self.triggerEdit = LineEdit(self)
        self.triggerEdit.setPlaceholderText("支持正则表达式，如: Player.*joined")
        self.triggerLayout.addWidget(self.triggerEdit, 1)

        # Cron生成器按钮（初始隐藏）
        self.cronGeneratorBtn = ToolButton(FIF.CALENDAR, self)
        self.cronGeneratorBtn.setToolTip("打开Cron表达式生成器")
        self.cronGeneratorBtn.clicked.connect(self.openCronGenerator)
        self.cronGeneratorBtn.setVisible(False)
        self.triggerLayout.addWidget(self.cronGeneratorBtn)

        self.textLayout.addLayout(self.triggerLayout)

        # 执行动作
        actionLayout = QHBoxLayout()
        actionLayout.addWidget(StrongBodyLabel("执行动作:", self))
        self.actionCombo = ComboBox(self)
        self.actionCombo.addItems(["发送指令", "保存存档", "关闭服务器", "开启服务器"])
        self.actionCombo.currentIndexChanged.connect(self.onActionChanged)
        actionLayout.addWidget(self.actionCombo, 1)
        self.textLayout.addLayout(actionLayout)

        # 动作参数
        self.valueLayout = QHBoxLayout()
        self.valueLabel = StrongBodyLabel("指令内容:", self)
        self.valueLayout.addWidget(self.valueLabel)
        self.valueEdit = LineEdit(self)
        self.valueEdit.setPlaceholderText("输入要发送的指令，如: say 服务器将在5分钟后重启")
        self.valueLayout.addWidget(self.valueEdit, 1)
        self.textLayout.addLayout(self.valueLayout)

        # 设置对话框大小
        self.widget.setFixedWidth(600)

    def loadTaskData(self):
        """加载任务数据到编辑器"""
        if not self.is_edit_mode:
            return

        self.nameEdit.setText(self.task_data.get("name", ""))

        task_type = self.task_data.get("type", "pattern")
        self.typeCombo.setCurrentIndex(0 if task_type == "pattern" else 1)

        if task_type == "pattern":
            self.triggerEdit.setText(self.task_data.get("pattern", ""))
        else:
            self.triggerEdit.setText(self.task_data.get("cron", ""))

        action = self.task_data.get("action", "command")
        action_index = {"command": 0, "save": 1, "stop": 2, "start": 3}.get(action, 0)
        self.actionCombo.setCurrentIndex(action_index)

        self.valueEdit.setText(self.task_data.get("value", ""))

    def onTypeChanged(self, index: int):
        """任务类型改变"""
        is_cron = index == 1
        self.triggerLabel.setText("Cron表达式:" if is_cron else "匹配模式:")
        self.triggerEdit.setPlaceholderText(
            "例: 0 */6 * * * (每6小时执行)" if is_cron else "支持正则表达式，如: Player.*joined"
        )
        self.cronGeneratorBtn.setVisible(is_cron)
        # 当选择Cron类型时，显示帮助提示
        if is_cron:
            self.cron_info_bar = InfoBar.info(
                "Cron表达式格式",
                "格式: 分 时 日 月 周 | 例: 0 */6 * * * (每6小时) | * * * * * (每分钟) | 0 0 * * * (每天0点)",
                parent=self,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=-1,
            )
        else:
            # 切换回输出匹配模式时，关闭InfoBar
            if self.cron_info_bar:
                self.cron_info_bar.close()
                self.cron_info_bar = None

    def openCronGenerator(self):
        """打开Cron生成器"""
        current_cron = self.triggerEdit.text().strip()
        dialog = CronGeneratorDialog(self, current_cron)
        if dialog.exec():
            cron_expr = dialog.getCronExpression()
            if cron_expr:
                self.triggerEdit.setText(cron_expr)

    def onActionChanged(self, index: int):
        """执行动作改变"""
        if index == 0:  # 发送指令
            self.valueLabel.setText("指令内容:")
            self.valueLabel.setVisible(True)
            self.valueEdit.setVisible(True)
            self.valueEdit.setPlaceholderText("输入要发送的指令")
        elif index == 1:  # 保存存档
            self.valueLabel.setText("备注:")
            self.valueLabel.setVisible(True)
            self.valueEdit.setVisible(True)
            self.valueEdit.setPlaceholderText("可选，如: 定时备份")
        else:  # 关闭服务器 / 开启服务器
            self.valueLabel.setVisible(False)
            self.valueEdit.setVisible(False)

    def getTaskData(self) -> Optional[dict]:
        """获取任务数据"""
        name = self.nameEdit.text().strip()
        if not name:
            InfoBar.warning("", "请输入任务名称", parent=self)
            return None

        task_type_index = self.typeCombo.currentIndex()
        task_type = "pattern" if task_type_index == 0 else "cron"

        trigger_value = self.triggerEdit.text().strip()
        if not trigger_value:
            InfoBar.warning("", "请输入匹配模式或Cron表达式", parent=self)
            return None

        # 验证正则表达式或Cron表达式
        if task_type == "pattern":
            try:
                re.compile(trigger_value)
            except re.error as e:
                InfoBar.error("", f"正则表达式无效: {str(e)}", parent=self)
                return None
        else:
            try:
                croniter(trigger_value)
            except Exception as e:
                InfoBar.error(
                    "",
                    f"Cron表达式无效: {str(e)}",
                    parent=self,
                    isClosable=False,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                )
                return None

        action_index = self.actionCombo.currentIndex()
        action = ["command", "save", "stop", "start"][action_index]

        value = self.valueEdit.text().strip()
        if action == "command" and not value:
            InfoBar.warning("", "请输入要发送的指令", parent=self)
            return None

        task_data = {
            "id": self.task_data.get("id", f"task_{datetime.now().timestamp()}"),
            "name": name,
            "type": task_type,
            "enabled": self.task_data.get("enabled", True),
            "action": action,
            "value": value,
        }

        if task_type == "pattern":
            task_data["pattern"] = trigger_value
        else:
            task_data["cron"] = trigger_value
            task_data["last_run"] = self.task_data.get("last_run", 0)

        return task_data
    
    def _onDialogClose(self):
        """对话框关闭时清理InfoBar"""
        if self.cron_info_bar:
            self.cron_info_bar.close()
            self.cron_info_bar = None


class SchedulerPage(QWidget):
    """定时任务页面"""

    def __init__(self, serverConfig: ServerVariables, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.serverConfig = serverConfig
        self.tasks: List[dict] = []
        self.task_cards: Dict[str, TaskCardWidget] = {}
        self.config_file = osp.join("Servers", serverConfig.serverName, "scheduler_config.json")

        # Cron任务执行器
        self.cron_timer = QTimer(self)
        self.cron_timer.timeout.connect(self.checkCronTasks)
        self.cron_timer.setInterval(60000)  # 每分钟检查一次

        # 服务器输出监听
        self.server_output_handler = None
        self.server_start_handler = None

        self.setupUI()
        self.loadTasks()
        self.startCronScheduler()

    def setupUI(self):
        """设置UI"""
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 顶部按钮栏
        btnLayout = QHBoxLayout()
        btnLayout.setSpacing(8)

        self.addTaskBtn = PrimaryPushButton(FIF.ADD, "添加任务", self)
        self.addTaskBtn.clicked.connect(self.addTask)
        btnLayout.addWidget(self.addTaskBtn)

        self.importBtn = PushButton(FIF.FOLDER_ADD, "导入配置", self)
        self.importBtn.clicked.connect(self.importConfig)
        btnLayout.addWidget(self.importBtn)

        self.exportBtn = PushButton(FIF.SAVE, "导出配置", self)
        self.exportBtn.clicked.connect(self.exportConfig)
        btnLayout.addWidget(self.exportBtn)

        btnLayout.addStretch(1)

        # 滚动区域
        self.scrollArea = MySmoothScrollArea(self)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(8)
        self.scrollLayout.setAlignment(Qt.AlignTop)

        self.scrollArea.setWidget(self.scrollWidget)

        # 空状态提示
        self.emptyHintWidget = QWidget(self.scrollWidget)
        emptyLayout = QVBoxLayout(self.emptyHintWidget)
        emptyLayout.setAlignment(Qt.AlignCenter)
        emptyLayout.setSpacing(12)

        emptyLabel = SubtitleLabel("暂无任务", self.emptyHintWidget)
        emptyLabel.setAlignment(Qt.AlignCenter)
        emptyLayout.addWidget(emptyLabel)

        emptyTip = BodyLabel("点击上方'添加任务'按钮创建新的定时任务", self.emptyHintWidget)
        emptyTip.setAlignment(Qt.AlignCenter)
        emptyLayout.addWidget(emptyTip)

        self.scrollLayout.addWidget(self.emptyHintWidget)

        # 添加到主布局
        topWidget = QWidget(self)
        topWidget.setLayout(btnLayout)

        self.layout.addWidget(topWidget, 0, 0, 1, 1)
        self.layout.addWidget(self.scrollArea, 1, 0, 1, 1)

    def loadTasks(self):
        """从配置文件加载任务"""
        try:
            if osp.exists(self.config_file):
                content = readFile(self.config_file)
                data = json.loads(content)
                self.tasks = data.get("tasks", [])
                self.refreshTaskCards()
            else:
                self.tasks = []
                self.updateEmptyState()
        except Exception as e:
            MCSL2Logger.error(f"加载定时任务配置失败: {e}")
            InfoBar.error(
                "加载失败",
                f"无法加载定时任务配置: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000,
            )

    def saveTasks(self):
        """保存任务到配置文件"""
        try:
            data = {"tasks": self.tasks}
            content = json.dumps(data, indent=2, ensure_ascii=False)
            writeFile(self.config_file, content)
        except Exception as e:
            MCSL2Logger.error(f"保存定时任务配置失败: {e}")
            InfoBar.error(
                "保存失败",
                f"无法保存定时任务配置: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000,
            )

    def refreshTaskCards(self):
        """刷新任务卡片显示"""
        # 清除现有卡片
        for card in list(self.task_cards.values()):
            self.scrollLayout.removeWidget(card)
            card.deleteLater()
        self.task_cards.clear()

        # 创建新卡片
        for task in self.tasks:
            card = TaskCardWidget(task, self.scrollWidget)
            card.editRequested.connect(self.editTask)
            card.deleteRequested.connect(self.deleteTask)
            card.toggleRequested.connect(self.toggleTask)

            self.scrollLayout.insertWidget(self.scrollLayout.count() - 1, card)
            self.task_cards[task["id"]] = card

        self.updateEmptyState()

    def updateEmptyState(self):
        """更新空状态显示"""
        has_tasks = len(self.tasks) > 0
        self.emptyHintWidget.setVisible(not has_tasks)

    def addTask(self):
        """添加新任务"""
        dialog = TaskEditorDialog(self)
        if dialog.exec():
            task_data = dialog.getTaskData()
            if task_data:
                self.tasks.append(task_data)
                self.saveTasks()
                self.refreshTaskCards()
                InfoBar.success(
                    "添加成功",
                    f"任务 '{task_data['name']}' 已添加",
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                )

    def editTask(self, task_data: dict):
        """编辑任务"""
        dialog = TaskEditorDialog(self, task_data)
        if dialog.exec():
            new_data = dialog.getTaskData()
            if new_data:
                # 更新任务
                for i, task in enumerate(self.tasks):
                    if task["id"] == new_data["id"]:
                        self.tasks[i] = new_data
                        break
                self.saveTasks()
                self.refreshTaskCards()
                InfoBar.success(
                    "保存成功",
                    f"任务 '{new_data['name']}' 已更新",
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                )

    def deleteTask(self, task_id: str):
        """删除任务"""
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            return

        box = MessageBox("确认删除", f"确定要删除任务 '{task['name']}' 吗？", self)
        if box.exec():
            self.tasks = [t for t in self.tasks if t["id"] != task_id]
            self.saveTasks()
            self.refreshTaskCards()
            InfoBar.info(
                "已删除",
                f"任务 '{task['name']}' 已删除",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=2000,
            )

    def toggleTask(self, task_id: str, enabled: bool):
        """切换任务启用状态"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["enabled"] = enabled
                break
        self.saveTasks()

    def importConfig(self):
        """导入配置"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择配置文件", "", "JSON Files (*.json)")
        if file_path:
            try:
                content = readFile(file_path)
                data = json.loads(content)
                self.tasks = data.get("tasks", [])
                self.saveTasks()
                self.refreshTaskCards()
                InfoBar.success(
                    "导入成功",
                    f"已导入 {len(self.tasks)} 个任务",
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                )
            except Exception as e:
                MCSL2Logger.error(f"导入配置失败: {e}")
                InfoBar.error(
                    "导入失败",
                    str(e),
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                )

    def exportConfig(self):
        """导出配置"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存配置文件",
            f"{self.serverConfig.serverName}_scheduler.json",
            "JSON Files (*.json)",
        )
        if file_path:
            try:
                data = {"tasks": self.tasks}
                content = json.dumps(data, indent=2, ensure_ascii=False)
                writeFile(file_path, content)
                InfoBar.success(
                    "导出成功",
                    "配置已保存",
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                )
            except Exception as e:
                MCSL2Logger.error(f"导出配置失败: {e}")
                InfoBar.error(
                    "导出失败",
                    str(e),
                    parent=self,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                )

    def startCronScheduler(self):
        """启动Cron调度器"""
        self.cron_timer.start()
        MCSL2Logger.info("Cron调度器已启动")

    def stopCronScheduler(self):
        """停止Cron调度器"""
        self.cron_timer.stop()

    def checkCronTasks(self):
        """检查Cron任务是否需要执行"""
        current_time = datetime.now()
        current_timestamp = current_time.timestamp()

        for task in self.tasks:
            if not task.get("enabled", True):
                continue

            if task.get("type") != "cron":
                continue

            try:
                cron_expr = task.get("cron", "")
                last_run = task.get("last_run", 0)

                cron = croniter(
                    cron_expr, datetime.fromtimestamp(last_run) if last_run > 0 else current_time
                )
                next_run = cron.get_next(datetime)

                # 如果下一次执行时间已经过了，执行任务
                if next_run <= current_time:
                    self.executeTask(task)
                    task["last_run"] = current_timestamp
                    self.saveTasks()

            except Exception as e:
                MCSL2Logger.error(f"检查Cron任务失败: {e}")

    def setServerOutputHandler(self, handler):
        """设置服务器输出处理器"""
        self.server_output_handler = handler

    def setServerStartHandler(self, handler):
        """设置服务器启动处理器"""
        self.server_start_handler = handler

    def handleServerOutput(self, output: str):
        """处理服务器输出，检查是否匹配任务模式"""
        for task in self.tasks:
            if not task.get("enabled", True):
                continue

            if task.get("type") != "pattern":
                continue

            try:
                pattern = task.get("pattern", "")
                if re.search(pattern, output):
                    MCSL2Logger.info(f"匹配到任务模式: {task['name']}")
                    self.executeTask(task)
            except Exception as e:
                MCSL2Logger.error(f"匹配任务模式失败: {e}")

    def executeTask(self, task: dict):
        """执行任务"""
        action = task.get("action")
        value = task.get("value", "")

        try:
            if action == "command":
                # 发送指令到服务器
                if self.server_output_handler:
                    self.server_output_handler(value)
                    MCSL2Logger.info(f"执行任务 '{task['name']}': 发送指令 '{value}'")
            elif action == "save":
                # 保存存档
                if self.server_output_handler:
                    self.server_output_handler("save-all")
                    MCSL2Logger.info(f"执行任务 '{task['name']}': 保存存档")
            elif action == "stop":
                # 关闭服务器
                if self.server_output_handler:
                    self.server_output_handler("stop")
                    MCSL2Logger.info(f"执行任务 '{task['name']}': 关闭服务器")
            elif action == "start":
                # 开启服务器
                if self.server_start_handler:
                    self.server_start_handler()
                    MCSL2Logger.info(f"执行任务 '{task['name']}': 开启服务器")
                else:
                    MCSL2Logger.warning(f"执行任务 '{task['name']}': 开启服务器失败，未设置启动处理器")
        except Exception as e:
            MCSL2Logger.error(f"执行任务失败: {e}")

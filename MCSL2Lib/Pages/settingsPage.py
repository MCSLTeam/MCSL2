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
Settings page.
"""

from datetime import datetime
import json
import platform
from typing import Optional

from PyQt5.QtCore import QSize, Qt, QRect, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QSizePolicy,
    QSpacerItem,
    QFrame,
    QAbstractScrollArea,
    QVBoxLayout,
    QApplication,
    QLineEdit,
)
from qfluentwidgets import (
    BodyLabel,
    SimpleCardWidget,
    HyperlinkButton,
    PrimaryPushButton,
    PushButton,
    TransparentToolButton,
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
    MessageBoxBase,
    SubtitleLabel,
    InfoBarPosition,
    InfoBar,
    ComboBox,
    EditableComboBox,
    LineEdit,
    PlainTextEdit,
    FluentIcon as FIF,
    setThemeColor,
    qconfig,
)

from MCSL2Lib import MCSL2VERSION
from MCSL2Lib.ProgramControllers.promptController import (
    get_default_ai_analyze_prompt,
    get_ai_analyze_user_prompt,
    set_ai_analyze_prompt,
)
from MCSL2Lib.ProgramControllers.settingsController import cfg
from MCSL2Lib.ProgramControllers.startupController import is_start_on_startup_enabled
from MCSL2Lib.ProgramControllers.startupController import set_start_on_startup
from MCSL2Lib.ProgramControllers.updateController import (
    CheckUpdateThread,
    MCSL2FileUpdater,
    compareVersion,
)
from MCSL2Lib.ProgramControllers.logController import genSysReport
from MCSL2Lib.singleton import Singleton
from MCSL2Lib.variables import GlobalMCSL2Variables, SettingsVariables
from MCSL2Lib.ProgramControllers.interfaceController import MySmoothScrollArea

from MCSL2Lib.verification import generateUniqueCode

settingsVariables = SettingsVariables()

AI_ANALYZE_PROVIDERS = {
    "OpenAI": "https://api.openai.com/v1",
    "Claude": "https://api.anthropic.com/v1",
    "Gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
    "Qwen": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    "GLM": "https://open.bigmodel.cn/api/paas/v4",
    "DeepSeek": "https://api.deepseek.com/v1",
    "硅基流动": "https://api.siliconflow.cn/v1",
    "Kimi": "https://api.moonshot.cn/v1",
    "自定义API": "",
}

AI_ANALYZE_PROVIDER_DOCS = {
    "OpenAI": "https://platform.openai.com/api-keys",
    "Claude": "https://platform.claude.com/docs/en/api/openai-sdk",
    "Gemini": "https://aistudio.google.com/app/api-keys",
    "Qwen": "https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.fd545e97tIJXk0&tab=model#/api-key",
    "GLM": "https://bigmodel.cn/usercenter/proj-mgmt/apikeys",
    "DeepSeek": "https://platform.deepseek.com/api_keys",
    "硅基流动": "http://cloud.siliconflow.cn/me/account/ak",
    "Kimi": "https://platform.moonshot.cn/console/account",
    "自定义API": "",
}

AI_ANALYZE_PROVIDER_MODELS = {
    "OpenAI": [
        "gpt-5.2",
        "gpt-5.1",
        "gpt-5",
        "gpt-4.1",
        "gpt-4o",
        "gpt-5-mini",
        "gpt-4o-mini",
    ],
    "Claude": [
        "claude-4.5-opus",
        "claude-4.5-sonnet",
        "claude-4.5-haiku",
    ],
    "Gemini": [
        "gemini-3-pro-preview",
        "gemini-3-flash-preview",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
    ],
    "Qwen": [
        "qwen3-max",
        "qwen-plus",
        "qwen-flash",
        "qwen-turbo",
    ],
    "GLM": [
        "glm-4.7",
        "glm-4.6",
        "glm-4.5-flash",
    ],
    "DeepSeek": [
        "deepseek-chat",
        "deepseek-reasoner",
    ],
    "硅基流动": [],
    "Kimi": [
        "kimi-k2-0905-preview",
        "kimi-k2-turbo-preview",
        "moonshot-v1-128k",
    ],
    "自定义API": [],
}


def _normalize_base_url(url: str) -> str:
    u = (url or "").strip()
    while u.endswith("/"):
        u = u[:-1]
    return u


class AIConfigTestThread(QThread):
    resultSignal = pyqtSignal(bool, str)

    def __init__(self, base_url: str, api_key: str, model: str, parent=None):
        super().__init__(parent)
        self.base_url = _normalize_base_url(base_url)
        self.api_key = api_key.strip()
        self.model = model.strip()

    def run(self):
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=15)
            resp = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=8,
                temperature=0,
            )
            if not getattr(resp, "choices", None):
                raise RuntimeError("服务端返回空响应")
            self.resultSignal.emit(True, "")
        except Exception as e:
            self.resultSignal.emit(False, str(e))


class AIAnalyzeSettingsBox(MessageBoxBase):
    savedSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr("AI 报错分析设置"), self)
        self.viewLayout.addWidget(self.titleLabel)

        self.formWidget = QWidget(self)
        self.formLayout = QGridLayout(self.formWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.providerLabel = StrongBodyLabel(self.tr("服务商"), self.formWidget)
        self.providerCombo = ComboBox(self.formWidget)
        self.providerCombo.addItems(list(AI_ANALYZE_PROVIDERS.keys()))

        self.baseUrlLabel = StrongBodyLabel(self.tr("API Base URL"), self.formWidget)
        self.baseUrlEdit = LineEdit(self.formWidget)

        self.modelLabel = StrongBodyLabel(self.tr("模型"), self.formWidget)
        self.modelCombo = EditableComboBox(self.formWidget)

        self.apiKeyLabel = StrongBodyLabel(self.tr("API Key"), self.formWidget)
        self.apiKeyEdit = LineEdit(self.formWidget)
        self.apiKeyEdit.setEchoMode(QLineEdit.Password)

        self.docsLabel = StrongBodyLabel(self.tr("API 文档"), self.formWidget)
        self.docsButton = HyperlinkButton(
            "",
            self.tr("打开"),
            self.formWidget,
            FIF.LINK,
        )

        self.statusLabel = StrongBodyLabel("", self.formWidget)

        self.formLayout.addWidget(self.providerLabel, 0, 0, 1, 1)
        self.formLayout.addWidget(self.providerCombo, 0, 1, 1, 1)
        self.formLayout.addWidget(self.docsLabel, 1, 0, 1, 1)
        self.formLayout.addWidget(self.docsButton, 1, 1, 1, 1)
        self.formLayout.addWidget(self.baseUrlLabel, 2, 0, 1, 1)
        self.formLayout.addWidget(self.baseUrlEdit, 2, 1, 1, 1)
        self.formLayout.addWidget(self.modelLabel, 3, 0, 1, 1)
        self.formLayout.addWidget(self.modelCombo, 3, 1, 1, 1)
        self.formLayout.addWidget(self.apiKeyLabel, 4, 0, 1, 1)
        self.formLayout.addWidget(self.apiKeyEdit, 4, 1, 1, 1)
        self.formLayout.addWidget(self.statusLabel, 5, 0, 1, 2)

        self.viewLayout.addWidget(self.formWidget)

        self.yesButton.setText(self.tr("检测并保存"))
        self.cancelButton.setText(self.tr("取消"))

        self._api_keys_by_model = self._load_api_keys()
        self._legacy_api_key = (cfg.get(cfg.aiAnalyzeApiKey) or "").strip()
        self._last_model = ""

        self.providerCombo.currentTextChanged.connect(self._on_provider_changed)
        self.modelCombo.currentTextChanged.connect(self._on_model_changed)
        try:
            self.yesButton.clicked.disconnect()
        except Exception:
            pass
        self.yesButton.clicked.connect(self._test_and_save)

        self._load_from_config()
        self._sync_provider()
        self._sync_api_key_for_current_model(allow_legacy=True)

        self.widget.setMinimumWidth(560)

        self.testThread: Optional[AIConfigTestThread] = None

    def _load_api_keys(self) -> dict:
        raw = (cfg.get(cfg.aiAnalyzeApiKeys) or "").strip()
        if not raw:
            return {}
        try:
            obj = json.loads(raw)
            return obj if isinstance(obj, dict) else {}
        except Exception:
            return {}

    def _dump_api_keys(self, api_keys: dict) -> str:
        try:
            return json.dumps(api_keys, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        except Exception:
            return "{}"

    def _stash_api_key_for_last_model(self):
        model = (self._last_model or "").strip()
        if not model:
            return
        api_key = self.apiKeyEdit.text().strip()
        if api_key:
            self._api_keys_by_model[model] = api_key
            return
        if model in self._api_keys_by_model:
            self._api_keys_by_model.pop(model, None)

    def _sync_api_key_for_current_model(self, allow_legacy: bool):
        model = self.modelCombo.currentText().strip()
        api_key = (self._api_keys_by_model.get(model) or "").strip()
        if not api_key and allow_legacy:
            saved_model = (cfg.get(cfg.aiAnalyzeModel) or "").strip()
            if (
                model
                and model == saved_model
                and self._legacy_api_key
                and not self._api_keys_by_model
            ):
                api_key = self._legacy_api_key
        self.apiKeyEdit.setText(api_key)
        self._last_model = model

    def _on_provider_changed(self, _text: str):
        self._stash_api_key_for_last_model()
        self._sync_provider()
        self._sync_api_key_for_current_model(allow_legacy=False)

    def _on_model_changed(self, _text: str):
        self._stash_api_key_for_last_model()
        self._sync_api_key_for_current_model(allow_legacy=False)

    def _load_from_config(self):
        provider = cfg.get(cfg.aiAnalyzeProvider)
        base_url = cfg.get(cfg.aiAnalyzeBaseUrl)
        model = cfg.get(cfg.aiAnalyzeModel)

        idx = self.providerCombo.findText(provider)
        if idx != -1:
            self.providerCombo.setCurrentIndex(idx)
        self.baseUrlEdit.setText(base_url or "")
        self.modelCombo.setCurrentText(model or "")

        self.baseUrlEdit.setPlaceholderText(self.tr("例如：https://api.openai.com/v1"))
        self.modelCombo.setPlaceholderText(self.tr("选择或填写模型名"))
        self.apiKeyEdit.setPlaceholderText(self.tr("填写您的 API 秘钥"))

    def _sync_provider(self):
        current_model = self.modelCombo.currentText().strip()
        provider = self.providerCombo.currentText()
        default_url = AI_ANALYZE_PROVIDERS.get(provider, "")
        docs_url = AI_ANALYZE_PROVIDER_DOCS.get(provider, "")
        models = AI_ANALYZE_PROVIDER_MODELS.get(provider, [])
        if provider == "自定义API":
            self.baseUrlEdit.setReadOnly(False)
            if not self.baseUrlEdit.text().strip():
                self.baseUrlEdit.setText(default_url)
        else:
            self.baseUrlEdit.setReadOnly(True)
            self.baseUrlEdit.setText(default_url)
        if docs_url:
            self.docsButton.setEnabled(True)
            self.docsButton.setText(self.tr("打开"))
            self.docsButton.setUrl(docs_url)
        else:
            self.docsButton.setEnabled(False)
            self.docsButton.setText(self.tr("无默认链接"))
            self.docsButton.setUrl("")

        try:
            self.modelCombo.blockSignals(True)
            self.modelCombo.clear()
            if models:
                self.modelCombo.addItems(models)
            if current_model:
                self.modelCombo.setCurrentText(current_model)
            elif provider == "硅基流动":
                self.modelCombo.setCurrentText("deepseek-ai/DeepSeek-V3")
            elif provider == "Kimi" and models:
                self.modelCombo.setCurrentText(models[0])
        finally:
            try:
                self.modelCombo.blockSignals(False)
            except Exception:
                pass

    def _test_and_save(self):
        self._stash_api_key_for_last_model()
        provider = self.providerCombo.currentText().strip()
        base_url = _normalize_base_url(self.baseUrlEdit.text())
        api_key = self.apiKeyEdit.text().strip()
        model = self.modelCombo.currentText().strip()

        if not base_url:
            self.statusLabel.setText(self.tr("请填写 API Base URL"))
            return
        if not (base_url.startswith("http://") or base_url.startswith("https://")):
            self.statusLabel.setText(self.tr("API Base URL 格式不正确"))
            return
        if not api_key:
            self.statusLabel.setText(self.tr("请填写 API Key"))
            return
        if not model:
            self.statusLabel.setText(self.tr("请填写模型名/ID"))
            return

        self.statusLabel.setText(self.tr("正在检测，请稍候..."))
        self.yesButton.setEnabled(False)

        self.testThread = AIConfigTestThread(
            base_url=base_url,
            api_key=api_key,
            model=model,
            parent=self,
        )
        api_keys = dict(self._api_keys_by_model)
        if api_key:
            api_keys[model] = api_key
        else:
            api_keys.pop(model, None)
        api_keys_json = self._dump_api_keys(api_keys)

        def _handle_result(ok: bool, err: str):
            self._on_test_finished(ok, err, provider, base_url, model, api_keys_json)

        self.testThread.resultSignal.connect(_handle_result)
        self.testThread.start()

    def _on_test_finished(
        self, ok: bool, err: str, provider: str, base_url: str, model: str, api_keys_json: str
    ):
        self.yesButton.setEnabled(True)
        if not ok:
            self.statusLabel.setText(self.tr("检测失败：") + (err or ""))
            return

        cfg.set(cfg.aiAnalyzeProvider, provider)
        cfg.set(cfg.aiAnalyzeBaseUrl, base_url)
        cfg.set(cfg.aiAnalyzeModel, model)
        cfg.set(cfg.aiAnalyzeApiKeys, api_keys_json)
        cfg.set(cfg.aiAnalyzeApiKey, "")
        qconfig.save()
        self._api_keys_by_model = self._load_api_keys()
        self._legacy_api_key = ""
        self.statusLabel.setText(self.tr("检测成功，已保存"))
        self.savedSignal.emit()
        self.close()


class AIPromptSettingsBox(MessageBoxBase):
    savedSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr("AI 提示词设置"), self)
        self.viewLayout.addWidget(self.titleLabel)

        self.tipTitleLabel = StrongBodyLabel(self.tr("规范提示"), self)
        self.tipBodyLabel = BodyLabel(
            self.tr(
                "建议在提示词中明确：角色/目标、输入边界、输出格式、失败兜底。\n"
                "AI 分析器输出会被强制为纯文本（不允许 Markdown/JSON）。\n"
                "请不要在提示词中要求输出 Markdown/JSON。"
            ),
            self,
        )
        self.tipBodyLabel.setWordWrap(True)
        self.tipLink = HyperlinkButton(
            "https://help.aliyun.com/zh/model-studio/prompt-engineering-guide",
            self.tr("查看提示词工程指南"),
            self,
            FIF.LINK,
        )

        self.templateLabel = StrongBodyLabel(self.tr("模板"), self)
        self.templateCombo = ComboBox(self)
        self.templateCombo.addItems([self.tr("已保存提示词"), self.tr("默认提示词")])

        self.viewLayout.addWidget(self.tipTitleLabel)
        self.viewLayout.addWidget(self.tipBodyLabel)
        self.viewLayout.addWidget(self.tipLink)
        self.viewLayout.addSpacing(8)

        self.viewLayout.addWidget(self.templateLabel)
        self.viewLayout.addWidget(self.templateCombo)

        self.promptEdit = PlainTextEdit(self)
        self.promptEdit.setPlainText(get_ai_analyze_user_prompt())
        self.promptEdit.setMinimumHeight(260)
        self.viewLayout.addWidget(self.promptEdit)

        self.restoreDefaultButton = PushButton(self.tr("恢复默认"), self)
        self.buttonLayout.insertWidget(0, self.restoreDefaultButton)

        self.yesButton.setText(self.tr("保存"))
        self.cancelButton.setText(self.tr("取消"))
        try:
            self.yesButton.clicked.disconnect()
        except Exception:
            pass
        self.yesButton.clicked.connect(self._save)
        self.restoreDefaultButton.clicked.connect(self._restore_default)
        self.templateCombo.currentIndexChanged.connect(self._on_template_changed)

        self.widget.setMinimumWidth(680)
        self._load_template_state()

    def _load_template_state(self):
        saved = get_ai_analyze_user_prompt().strip()
        if saved and saved != get_default_ai_analyze_prompt().strip():
            self.templateCombo.setCurrentIndex(0)
            self.promptEdit.setPlainText(saved)
        else:
            self.templateCombo.setCurrentIndex(1)
            self.promptEdit.setPlainText(get_default_ai_analyze_prompt())

    def _on_template_changed(self, _index: int):
        if self.templateCombo.currentIndex() == 0:
            saved = get_ai_analyze_user_prompt().strip()
            self.promptEdit.setPlainText(
                saved if saved and saved != get_default_ai_analyze_prompt().strip() else ""
            )
        else:
            self.promptEdit.setPlainText(get_default_ai_analyze_prompt())

    def _restore_default(self):
        self.templateCombo.setCurrentIndex(1)
        self.promptEdit.setPlainText(get_default_ai_analyze_prompt())

    def _save(self):
        set_ai_analyze_prompt(self.promptEdit.toPlainText())
        qconfig.save()
        self.savedSignal.emit()
        self.close()


class AutoStartServersDialog(MessageBoxBase):
    """自动启动服务器列表配置对话框"""

    savedSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        from MCSL2Lib.utils import readGlobalServerConfig
        from MCSL2Lib.ProgramControllers.interfaceController import MySmoothScrollArea
        from qfluentwidgets import CheckBox

        self.titleLabel = SubtitleLabel(self.tr("自动启动服务器"), self)
        self.viewLayout.addWidget(self.titleLabel)

        self.tipLabel = BodyLabel(self.tr("勾选需要在 MCSL2 启动时自动运行的服务器。"), self)
        self.tipLabel.setWordWrap(True)
        self.viewLayout.addWidget(self.tipLabel)

        # 创建滚动区域
        self.scrollArea = MySmoothScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumHeight(300)

        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setSpacing(12)
        self.scrollArea.setWidget(self.scrollWidget)

        # 读取全局服务器配置
        self.globalConfig = readGlobalServerConfig()
        self.checkboxes = {}

        # 读取当前自动启动列表
        import json

        auto_start_list = json.loads(cfg.get(cfg.autoStartServers) or "[]")

        # 为每个服务器创建复选框
        for server_cfg in self.globalConfig:
            server_name = server_cfg.get("name", "")
            if server_name:
                checkbox = CheckBox(server_name, self.scrollWidget)
                checkbox.setChecked(server_name in auto_start_list)
                self.checkboxes[server_name] = checkbox
                self.scrollLayout.addWidget(checkbox)

        if not self.checkboxes:
            noServerLabel = BodyLabel(self.tr("没有可用的服务器"), self.scrollWidget)
            self.scrollLayout.addWidget(noServerLabel)

        self.scrollLayout.addStretch()
        self.viewLayout.addWidget(self.scrollArea)

        self.yesButton.setText(self.tr("保存"))
        self.cancelButton.setText(self.tr("取消"))

        try:
            self.yesButton.clicked.disconnect()
        except Exception:
            pass
        self.yesButton.clicked.connect(self._save)

        self.widget.setMinimumWidth(500)

    def _save(self):
        """保存自动启动服务器列表"""
        import json

        # 收集选中的服务器
        selected_servers = [
            name for name, checkbox in self.checkboxes.items() if checkbox.isChecked()
        ]

        # 保存到配置
        cfg.set(cfg.autoStartServers, json.dumps(selected_servers, ensure_ascii=False))
        qconfig.save()

        self.savedSignal.emit()
        self.close()


@Singleton
class SettingsPage(QWidget):
    """设置页"""

    settingsChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tmpParent = self
        self._handling_start_on_startup = False
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
            title=self.tr("自动启动 MCSL2 时自动运行上次运行的服务器"),
            content=self.tr("启用后，请点击下一项的按钮完成配置。"),
            configItem=cfg.autoRunLastServer,
            parent=self.serverSettingsGroup,
        )
        self.autoStartServersBtn = PrimaryPushSettingCard(
            text=self.tr("配置"),
            icon=FIF.PLAY,
            title=self.tr("自动启动服务器列表"),
            content=self.tr("设置 MCSL2 启动时自动运行的服务器。"),
            parent=self.serverSettingsGroup,
        )
        self.acceptAllMojangEula = SwitchSettingCard(
            icon=FIF.ACCEPT,
            title=self.tr("自动同意 EULA"),
            content=self.tr("创建时自动同意服务器的 Minecraft Eula。"),
            configItem=cfg.acceptAllMojangEula,
            parent=self.serverSettingsGroup,
        )
        self.sendStopInsteadOfKill = SwitchSettingCard(
            icon=FIF.VPN,
            title=self.tr("总是向服务器发送「stop」以安全地关闭服务器"),
            content=self.tr("此项因为安全性已被永久禁止更改。"),
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
        self.sendStopInsteadOfKill.setEnabled(False)
        self.autoStartServersBtn.clicked.connect(self.showAutoStartServersDialog)
        self.serverSettingsGroup.addSettingCard(self.autoRunLastServer)
        self.serverSettingsGroup.addSettingCard(self.autoStartServersBtn)
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
                self.tr("初始 (简易 + 进阶 + 导入)"),
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
                self.tr("FastMirror 镜像站"),
                self.tr("MCSL-Sync"),
                self.tr("极星·镜像站"),
                self.tr("雨云镜像站"),
            ],
            parent=self.downloadSettingsGroup,
        )
        self.useBMCLAPI = SwitchSettingCard(
            icon=FIF.CLOUD,
            title=self.tr("使用 BMCLAPI 镜像"),
            content=self.tr("使用国内镜像加速下载游戏核心和库文件（推荐）。"),
            configItem=cfg.useBMCLAPI,
            parent=self.downloadSettingsGroup,
        )
        self.alwaysAskSaveDirectory = SwitchSettingCard(
            icon=FIF.CHAT,
            title=self.tr("总是询问保存路径"),
            content=self.tr("不勾选则保存到 MCSL2/Downloads 文件夹。"),
            configItem=cfg.alwaysAskSaveDirectory,
            parent=self.downloadSettingsGroup,
        )
        self.downloadThreads = RangeSettingCard(
            configItem=cfg.downloadThreads,
            icon=FIF.SPEED_HIGH,
            title=self.tr("下载线程数"),
            content=self.tr("太高可不好哦。"),
            parent=self.downloadSettingsGroup,
        )
        self.forceParallelDownload = SwitchSettingCard(
            icon=FIF.TILES,
            title=self.tr("强制使用多线程下载"),
            content=self.tr("即使服务器不支持分块下载也使用多线程下载（可能会失败）。"),
            configItem=cfg.forceParallelDownload,
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
        self.downloadSettingsGroup.addSettingCard(self.downloadSource)
        self.downloadSettingsGroup.addSettingCard(self.useBMCLAPI)
        self.downloadSettingsGroup.addSettingCard(self.alwaysAskSaveDirectory)
        self.downloadSettingsGroup.addSettingCard(self.downloadThreads)
        self.downloadSettingsGroup.addSettingCard(self.forceParallelDownload)
        self.downloadSettingsGroup.addSettingCard(self.saveSameFileException)
        self.settingsLayout.addWidget(self.downloadSettingsGroup)

        # Console
        self.consoleSettingsGroup = SettingCardGroup(self.tr("终端设置"), self.settingsWidget)
        self.outputDeEncoding = ComboBoxSettingCard(
            configItem=cfg.outputDeEncoding,
            icon=FIF.CODE,
            title=self.tr("控制台输出编码"),
            content=self.tr("优先级低于服务器配置设置。"),
            texts=[self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI")]
            if platform.system().lower() == "windows"
            else [self.tr("UTF-8"), self.tr("GB18030")],
            parent=self.consoleSettingsGroup,
        )
        self.inputDeEncoding = ComboBoxSettingCard(
            configItem=cfg.inputDeEncoding,
            icon=FIF.CODE,
            title=self.tr("指令输入编码"),
            content=self.tr("优先级低于服务器配置设置。"),
            texts=[self.tr("跟随控制台输出"), self.tr("UTF-8"), self.tr("GB18030"), self.tr("ANSI")]
            if platform.system().lower() == "windows"
            else [self.tr("UTF-8"), self.tr("GB18030")],
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

        # AI Analyzer
        self.aiAnalyzerSettingsGroup = SettingCardGroup(self.tr("AI 分析器"), self.settingsWidget)
        self.aiAnalyzerApiSetting = PrimaryPushSettingCard(
            icon=FIF.ROBOT,
            text=self.tr("配置"),
            title=self.tr("AI 报错分析 API"),
            content=self.tr("配置服务商、Base URL、模型与 API Key。"),
            parent=self.aiAnalyzerSettingsGroup,
        )
        self.aiAnalyzerApiInfoButton = TransparentToolButton(
            getattr(FIF, "WARNING", FIF.INFO), self.aiAnalyzerApiSetting
        )
        self.aiAnalyzerApiInfoButton.setFixedSize(QSize(32, 32))
        self.aiAnalyzerApiInfoButton.setToolTip(self.tr("说明"))
        self.aiAnalyzerApiInfoButton.clicked.connect(self.showAiApiInfo)
        if hasattr(self.aiAnalyzerApiSetting, "hBoxLayout"):
            layout = self.aiAnalyzerApiSetting.hBoxLayout
            idx = -1
            if hasattr(self.aiAnalyzerApiSetting, "button"):
                idx = layout.indexOf(self.aiAnalyzerApiSetting.button)
            insert_idx = idx if idx >= 0 else max(layout.count() - 1, 0)
            layout.insertWidget(insert_idx, self.aiAnalyzerApiInfoButton)
        else:
            self.aiAnalyzerApiSetting.layout().addWidget(self.aiAnalyzerApiInfoButton)
        self.aiAnalyzerPromptSetting = PrimaryPushSettingCard(
            icon=FIF.CODE,
            text=self.tr("编辑"),
            title=self.tr("提示词"),
            content=self.tr("自定义 AI 分析提示词。"),
            parent=self.aiAnalyzerSettingsGroup,
        )
        self.aiAnalyzerApiSetting.clicked.connect(self.openAIAnalyzerSettings)
        self.aiAnalyzerPromptSetting.clicked.connect(self.openAIAnalyzerPromptSettings)
        self.aiAnalyzerSettingsGroup.addSettingCard(self.aiAnalyzerApiSetting)
        self.aiAnalyzerSettingsGroup.addSettingCard(self.aiAnalyzerPromptSetting)
        self.settingsLayout.addWidget(self.aiAnalyzerSettingsGroup)

        # Software
        self.programSettingsGroup = SettingCardGroup(self.tr("程序设置"), self.settingsWidget)
        self.themeMode = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            title=self.tr("主题"),
            content=self.tr("本程序也要花里胡哨捏~"),
            texts=["浅色", "深色", "跟随系统"],
            parent=self.programSettingsGroup,
        )
        self.themeColor = CustomColorSettingCard(
            configItem=cfg.themeColor,
            icon=FIF.PALETTE,
            title=self.tr("强调色"),
            content=self.tr("本程序也要花里胡哨捏~"),
            parent=self.programSettingsGroup,
        )
        self.startOnStartup = SwitchSettingCard(
            icon=FIF.POWER_BUTTON,
            title=self.tr("开机自启动"),
            content=self.tr("随系统启动自动打开 MCSL2。")
            if platform.system().lower() == "windows"
            else self.tr("当前系统暂不支持。"),
            configItem=cfg.startOnStartup,
            parent=self.programSettingsGroup,
        )
        if platform.system().lower() == "windows":
            self._bind_start_on_startup()
        else:
            self.startOnStartup.setEnabled(False)
        self.themeColor.colorChanged.connect(lambda cl: setThemeColor(color=cl, lazy=True))
        self.themeMode.optionChanged.connect(lambda ci: setTheme(cfg.get(ci), lazy=True))
        self.programSettingsGroup.addSettingCard(self.themeMode)
        self.programSettingsGroup.addSettingCard(self.themeColor)
        self.programSettingsGroup.addSettingCard(self.startOnStartup)
        self.settingsLayout.addWidget(self.programSettingsGroup)

        # Update
        self.updateSettingsGroup = SettingCardGroup(self.tr("更新设置"), self.settingsWidget)
        self.checkUpdateSetting = PrimaryPushSettingCard(
            icon=FIF.SYNC,
            text=self.tr("检查更新"),
            title=self.tr("检查更新"),
            content=self.tr("当前版本: ") + MCSL2VERSION,
            parent=self.updateSettingsGroup,
        )
        self.checkUpdateOnStart = SwitchSettingCard(
            icon=FIF.SPEED_MEDIUM,
            title=self.tr("启动时自动检查更新"),
            content=self.tr("可确保你的 MCSL2 最新。"),
            configItem=cfg.checkUpdateOnStart,
            parent=self.consoleSettingsGroup,
        )
        self.checkUpdateSetting.clicked.connect(lambda: self.checkUpdate(parent=self))
        self.updateSettingsGroup.addSettingCard(self.checkUpdateSetting)
        self.updateSettingsGroup.addSettingCard(self.checkUpdateOnStart)
        self.settingsLayout.addWidget(self.updateSettingsGroup)

        # Other
        self.about = SimpleCardWidget(self.settingsScrollAreaWidgetContents)
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
            "https://mcsl.com.cn",
            self.tr("打开官网"),
            self.aboutContentWidget,
            FIF.HOME,
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
            self.tr("打开源码仓库"),
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
            self.tr("加入官方QQ群"),
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
            icon=FIF.DICTIONARY,
            text=self.tr("系统报告"),
            parent=self.aboutContentWidget,
        )
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generateSysReport.sizePolicy().hasHeightForWidth())
        self.generateSysReport.setSizePolicy(sizePolicy)
        self.generateSysReport.setObjectName("generateSysReport")

        self.gridLayout.addWidget(self.generateSysReport, 1, 5, 1, 1)
        self.uniqueCodeBtn = PrimaryPushButton(
            icon=FIF.PASTE, text=self.tr("复制识别码"), parent=self
        )
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
            self.tr("赞助者列表"),
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
            "https://afdian.com/a/lxhtt",
            self.tr("赞助此项目"),
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
        self.subTitleLabel.setText(self.tr("自定义你的 MCSL2。"))
        self.aboutContent.setText(
            self.tr(
                "MCServerLauncher 2 是一个开源非营利性项目，遵循 GNU General Public License 3.0 开源协议。\n任何人皆可使用 MCSL2 的源码进行再编译、修改以及发行，\n但必须在相关源代码中以及软件中给出声明，并且二次分发版本的项目名称应与 “MCSL2” 有明显辨识度。\n“MCServerLauncher 2 软件” 已进行中华人民共和国计算机软件著作权登记，一切侵权行为将依法追究。\n计算机软件著作权登记号: 2024SR0343868\n\n© 2022 - 2024 MCSL开发组 保留所有权利。\n"  # noqa : E501
            )
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

    def _bind_start_on_startup(self):
        actual = is_start_on_startup_enabled()
        desired = bool(cfg.get(cfg.startOnStartup))
        if actual != desired:
            try:
                set_start_on_startup(desired)
            except Exception:
                self._handling_start_on_startup = True
                try:
                    cfg.set(cfg.startOnStartup, actual)
                    qconfig.save()
                finally:
                    self._handling_start_on_startup = False

        signal = getattr(self.startOnStartup, "checkedChanged", None)
        if signal is None:
            inner = getattr(self.startOnStartup, "switchButton", None)
            if inner is None:
                inner = getattr(self.startOnStartup, "switch", None)
            signal = getattr(inner, "checkedChanged", None) if inner is not None else None

        if signal is not None:
            try:
                signal.connect(self._on_start_on_startup_changed)
            except Exception:
                pass

    def _on_start_on_startup_changed(self, checked: bool):
        if self._handling_start_on_startup:
            return

        self._handling_start_on_startup = True
        try:
            set_start_on_startup(bool(checked))
            cfg.set(cfg.startOnStartup, bool(checked))
            qconfig.save()
            InfoBar.success(
                title=self.tr("已保存"),
                content=self.tr("开机自启动已开启") if checked else self.tr("开机自启动已关闭"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self,
            )
        except Exception as e:
            cfg.set(cfg.startOnStartup, not bool(checked))
            qconfig.save()
            InfoBar.error(
                title=self.tr("设置失败"),
                content=str(e),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=4000,
                parent=self,
            )
        finally:
            self._handling_start_on_startup = False

    def openAIAnalyzerSettings(self):
        try:
            __import__("openai")
        except Exception:
            InfoBar.error(
                title=self.tr("缺少依赖"),
                content=self.tr("未安装 openai 库，无法使用 AI 分析。"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=4000,
                parent=self,
            )
            return

        box = AIAnalyzeSettingsBox(self)
        box.savedSignal.connect(
            lambda: InfoBar.success(
                title=self.tr("成功"),
                content=self.tr("AI 配置已保存"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self,
            )
        )
        box.exec()

    def openAIAnalyzerPromptSettings(self):
        box = AIPromptSettingsBox(self)
        box.savedSignal.connect(
            lambda: InfoBar.success(
                title=self.tr("成功"),
                content=self.tr("提示词已保存"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self,
            )
        )
        box.exec()

    def showAiApiInfo(self):
        info_text = (
            "目前AI需要有用户自行提供API秘钥，建议使用DeepSeek-Chat（DeepSeek V3.2）模型价格便宜，生成质量特别好。"
            "目前能够完美适配的Kimi，DeepSeek，其他模型返回均有一定的结构问题"
        )
        w = MessageBox(self.tr("AI 分析器提示"), info_text, parent=self)
        w.exec()

    def showAutoStartServersDialog(self):
        """显示自动启动服务器配置对话框"""
        box = AutoStartServersDialog(self)
        box.savedSignal.connect(
            lambda: InfoBar.success(
                title=self.tr("成功"),
                content=self.tr("自动启动服务器列表已保存"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self,
            )
        )
        box.exec()

    def showNeedRestartMsg(self):
        InfoBar.success(
            title=self.tr("已修改"),
            content=self.tr("该配置将在重启 MCSL2 后生效"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
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
        if compareVersion(latestVerInfo["latest"]):
            title = self.tr("发现新版本: ") + latestVerInfo["latest"]
            w = MessageBox(title, latestVerInfo["update-log"], parent=self.tmpParent)
            w.contentLabel.setTextFormat(Qt.MarkdownText)
            w.yesButton.setText(self.tr("更新"))
            w.cancelButton.setText(self.tr("关闭"))
            if not GlobalMCSL2Variables.devMode:
                w.yesSignal.connect(lambda: self.window().switchTo(self))  # type: ignore
                w.yesSignal.connect(MCSL2FileUpdater(self).downloadUpdate)
            else:
                w.yesSignal.connect(
                    lambda: InfoBar.error(
                        title=self.tr("不行"),
                        content=self.tr("开发模式下更新会把 Python 删掉的"),
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
        report = (
            self.tr("生成时间: ")
            + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            + "\n"
            + genSysReport()
        )

        title = self.tr("MCServerLauncher 2 系统报告")
        w = MessageBox(
            title,
            report + self.tr("\n\n点击复制按钮以复制到剪贴板。"),
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

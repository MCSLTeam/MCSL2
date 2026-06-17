import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtGui import QPixmap  # noqa: E402
from PyQt5.QtWidgets import QApplication, QSizePolicy  # noqa: E402
from qfluentwidgets import FlowLayout  # noqa: E402

from MCSL2Lib.Pages.configurePage import ServerTypeHeaderCardWidget  # noqa: E402
from MCSL2Lib.Pages.settingsPage import SettingsPage  # noqa: E402
from MCSL2Lib.Widgets.selectJavaWidget import SingleSelectJavaWidget  # noqa: E402
from MCSL2Lib.Widgets.serverManagerWidget import SingleServerManager  # noqa: E402


def _app():
    return QApplication.instance() or QApplication([])


def _safe_label_height(label, lines=1, padding=4):
    return label.fontMetrics().lineSpacing() * lines + padding * 2


class CardTextLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = _app()

    def test_settings_about_text_reserves_vertical_padding(self):
        page = SettingsPage()

        self.assertTrue(page.aboutContent.wordWrap())
        self.assertLessEqual(page.about.minimumWidth(), 360)
        lines = page.aboutContent.text().count("\n") + 1
        self.assertGreaterEqual(
            page.aboutContent.minimumHeight(),
            _safe_label_height(page.aboutContent, lines=lines),
        )

    def test_settings_about_buttons_use_non_animated_flow_layout(self):
        page = SettingsPage()

        self.assertIsInstance(page.aboutButtonsLayout, FlowLayout)
        self.assertFalse(page.aboutButtonsLayout.needAni)
        self.assertEqual(
            page.aboutButtonsWidget.sizePolicy().verticalPolicy(),
            QSizePolicy.Preferred,
        )
        self.assertGreater(page.aboutButtonsWidget.maximumHeight(), 1000)
        for button in (
            page.joinQQGroup,
            page.openOfficialWeb,
            page.openSourceCodeRepo,
            page.sponsorsBtn,
            page.donateBtn,
            page.generateSysReport,
        ):
            self.assertIs(button.parent(), page.aboutButtonsWidget)

    def test_server_type_card_text_reserves_vertical_padding(self):
        widget = ServerTypeHeaderCardWidget()

        self.assertTrue(widget.contentLabel.wordWrap())
        self.assertGreaterEqual(
            widget.contentLabel.minimumHeight(),
            _safe_label_height(widget.contentLabel),
        )

    def test_select_java_card_labels_reserve_vertical_padding(self):
        widget = SingleSelectJavaWidget(
            "finishSelectJavaBtn0",
            lambda: None,
            lambda: None,
            "java",
            "21",
        )

        for label in (widget.javaVerTitle, widget.javaPathTitle):
            self.assertGreaterEqual(label.minimumHeight(), _safe_label_height(label))

    def test_server_manager_card_labels_reserve_vertical_padding(self):
        widget = SingleServerManager(
            mem="1024M",
            coreFileName="server.jar",
            javaPath="/opt/java/bin/java",
            serverName="Example Server",
            icon=QPixmap(70, 70),
            btnSlot=lambda: None,
            i=0,
        )

        labels = (
            widget.serverName,
            widget.coreFileNameTitle,
            widget.memTitle,
            widget.mem,
            widget.coreFileName,
            widget.javaPathTitle,
            widget.javaPath,
        )
        for label in labels:
            self.assertGreaterEqual(label.minimumHeight(), _safe_label_height(label))


if __name__ == "__main__":
    unittest.main()

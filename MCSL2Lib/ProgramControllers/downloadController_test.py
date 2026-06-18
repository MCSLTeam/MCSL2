import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from PyQt5.QtCore import QCoreApplication, QTimer

from MCSL2Lib.ProgramControllers.downloadController import DownloadTask


class FinishedPypdl:
    headers = {}
    segments = 1
    current_size = 1
    size = 1
    speed = 0
    time_left = 0

    def start(self, **_):
        return None

    def stop(self):
        return None


class DownloadTaskTest(unittest.TestCase):
    def setUp(self):
        self.app = QCoreApplication.instance() or QCoreApplication(sys.argv)

    def test_emits_finished_when_worker_thread_completes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            task = DownloadTask(
                "https://example.com/file.jar",
                file_path=temp_dir,
                file_name="file.jar",
            )
            finished = []
            progress = []
            task.taskFinished.connect(lambda: finished.append(True))
            task.workerInfoChanged.connect(lambda info: progress.append(info))

            with patch(
                "MCSL2Lib.ProgramControllers.downloadController.Pypdl",
                return_value=FinishedPypdl(),
            ):
                task.start_download()

            deadline = time.monotonic() + 2
            while time.monotonic() < deadline and not finished:
                self.app.processEvents()
                time.sleep(0.01)

            self.assertEqual(finished, [True])
            self.assertEqual(progress[-1][0]["downloaded"], 1)
            self.assertEqual(progress[-1][0]["total"], 1)
            self.assertTrue(task.is_finished)
            self.assertEqual(Path(temp_dir, "file.jar").resolve(), task.full_path)

    def test_worker_completion_does_not_depend_on_thread_local_qtimer(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            task = DownloadTask(
                "https://example.com/file.jar",
                file_path=temp_dir,
                file_name="file.jar",
            )
            finished = []
            task.taskFinished.connect(lambda: finished.append(True))

            main_thread = threading.current_thread()
            original_single_shot = QTimer.singleShot

            def single_shot_only_from_main_thread(*args):
                if threading.current_thread() is not main_thread:
                    return None
                return original_single_shot(*args)

            with patch(
                "MCSL2Lib.ProgramControllers.downloadController.Pypdl",
                return_value=FinishedPypdl(),
            ), patch(
                "MCSL2Lib.ProgramControllers.downloadController.QTimer.singleShot",
                side_effect=single_shot_only_from_main_thread,
            ):
                task.start_download()

            deadline = time.monotonic() + 2
            while time.monotonic() < deadline and not finished:
                self.app.processEvents()
                time.sleep(0.01)

            self.assertEqual(finished, [True])


if __name__ == "__main__":
    unittest.main()

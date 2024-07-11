import time
from io import BytesIO
from pathlib import Path

from .post_processors import PostProcessors
from .progress_callback import ProgressCallback
from ..download_utils import DownloadUtils
from ..json.installV1 import InstallV1
from ..json.util import Util
from ..json.version import Version


class Action:
    profile: InstallV1
    monitor: ProgressCallback
    processors: PostProcessors
    version: Version

    def __init__(
        self, profile: InstallV1, monitor: ProgressCallback, installer: Path, isClient: bool
    ):
        self.profile = profile
        self.monitor = monitor
        self.processors = PostProcessors(profile, isClient, monitor)
        self.installer = installer
        self.installerDataBuf = BytesIO(installer.read_bytes())
        self.version = Util.loadVersion(
            DownloadUtils.readFileInZip(self.installerDataBuf, Path(profile.getJson())).decode(
                "utf-8"
            )
        )

    def error(self, message: str):
        self.monitor.stage(message)

    def __del__(self):
        self.installerDataBuf.close()




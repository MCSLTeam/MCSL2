from .post_processors import PostProcessors
from .progress_callback import ProgressCallback
from ..json.installV1 import InstallV1
from ..json.util import Util
from ..json.version import Version


class Action:
    profile: InstallV1
    monitor: ProgressCallback
    processors: PostProcessors
    version: Version

    def __init__(self, profile: InstallV1, monitor: ProgressCallback, isClient: bool):
        self.profile = profile
        self.monitor = monitor
        self.processors = PostProcessors(profile, isClient, monitor)
        self.version = Util.loadVersion(profile)

    def checkCancel(self):
        ...


class ActionCanceledException(Exception):
    def __init__(self):
        super().__init__()

import traceback
import zipfile
from io import BytesIO
from pathlib import Path
from queue import Queue

from .actions.progress_callback import TO_STD_OUT, ProgressCallback
from .actions.server_install import ServerInstall
from .json.util import Util


class SimpleInstaller:
    # TODO 使镜像源下载生效
    mirror = "https://bmclapi2.bangbang93.com/maven/"

    LIBRARIES_MAX_CONCURRENT = 4

    def __init__(self, detailed: bool = False, infoQueue: Queue = None):
        self.detailed = detailed
        if detailed:
            self.infoQueue = infoQueue or Queue(32)

    async def installServer(
            self, installer: Path, targetDir: Path, monitor: ProgressCallback, java: Path = None,
    ) -> bool:
        if self.detailed:
            monitor.setInfoQueue(self.infoQueue)

        installerBuf = BytesIO(installer.read_bytes())
        try:
            with zipfile.ZipFile(installerBuf) as archive:
                text = archive.read("install_profile.json").decode("utf-8")
                profile = Util.loadInstallProfile(text)
        except Exception as e:
            traceback.print_exc()
            monitor.stage(f"Failed to load install profile: {e}")
            return False
        serverInstaller = ServerInstall(profile, installer, monitor)
        run = await serverInstaller.run(targetDir, java, self.detailed)
        installerBuf.close()
        return run

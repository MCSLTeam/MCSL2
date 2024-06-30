import traceback
import zipfile
from io import BytesIO
from pathlib import Path

from .actions.progress_callback import TO_STD_OUT, ProgressCallback
from .actions.server_install import ServerInstall
from .json.util import Util


class SimpleInstaller:
    # TODO 使镜像源下载生效
    mirror = "https://bmclapi2.bangbang93.com/maven/"

    LIBRARIES_MAX_CONCURRENT = 4
    @staticmethod
    async def installServer(
        installer: Path, targetDir: Path, monitor: ProgressCallback = TO_STD_OUT, java: Path = None
    ) -> bool:
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
        run = await serverInstaller.run(targetDir, java)
        installerBuf.close()
        return run

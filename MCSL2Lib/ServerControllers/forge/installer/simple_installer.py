import traceback
import zipfile
from io import BytesIO
from pathlib import Path

from .actions.progress_callback import TO_STD_OUT
from .actions.server_install import ServerInstall
from .json.util import Util


class SimpleInstaller:
    mirror = None

    @staticmethod
    def installServer(installer: Path, targetDir: Path) -> bool:
        monitor = TO_STD_OUT

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
        run = serverInstaller.run(targetDir)
        installerBuf.close()
        return run

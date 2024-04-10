import traceback
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Dict

from .action import Action
from .progress_callback import ProgressCallback
from ..download_utils import DownloadUtils
from ..java2python import Supplier
from ..json.installV1 import InstallV1
from ..json.util import Util


class ServerInstall(Action):
    def __init__(self, profile: InstallV1, monitor: ProgressCallback):

        super().__init__(profile, monitor, False)

    def run(self, target: Path, installer: Path) -> bool:
        installerDataBuf = BytesIO(installer.read_bytes())

        if target.exists() and not target.is_dir():
            self.monitor.error("There is a file at this location, the server cannot be installed here!")
            return False

        librariesDir = Path(target).joinpath("libraries")
        if not target.exists():
            target.mkdir(parents=True)
        librariesDir.mkdir(parents=True)
        self.checkCancel()

        # Extract main executable jar
        contained = self.profile.getPath()
        if contained is not None:
            self.monitor.stage("Extracting main jar:")
            if not DownloadUtils.extractFile(contained, target / contained.getFilename()):
                self.monitor.error(f"  Failed to extract main jar: {contained.getFilename()}")
                return False
            else:
                self.monitor.stage("  Extracted successfully")
        self.checkCancel()

        # Download MC Server jar
        self.monitor.stage("Considering minecraft server jar")
        tokens: Dict[str, Supplier[str]] = {
            "ROOT": Supplier.of(lambda: str(target.absolute())),
            "MINECRAFT_VERSION": Supplier.of(self.profile.getMinecraft),
            "LIBRARY_DIR": Supplier.of(lambda: str(librariesDir.absolute()))
        }

        path = Util.replaceTokens(tokens, self.profile.getServerJarPath())
        serverTarget = Path(path)

    def downloadVanilla(self, target: Path, installerDataBuf: BytesIO, side: str):
        if not target.exists():
            parent = target.parent
            if not parent.exists():
                parent.mkdir(parents=True)

            res = "cache/vanilla/" + side + ".jar"
            with zipfile.ZipFile(installerDataBuf, "r") as installer:
                try:
                    target.write_bytes(installer.read(res))
                except Exception as e:
                    traceback.print_exception(e)
                    self.error("Failed to download version manifest, can not find " + side + " jar URL.")
                    return False

            Util.getVanillaVersion(self.profile.getMinecraft())

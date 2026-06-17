import importlib
from io import BytesIO
import sys
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))


def _stub_neoforge_package():
    package_name = "MCSL2Lib.ServerControllers.neoforge"
    if package_name in sys.modules:
        return

    package = types.ModuleType(package_name)
    package.__path__ = [str(Path(__file__).resolve().parent)]
    sys.modules[package_name] = package


_stub_neoforge_package()

server_install = importlib.import_module(
    "MCSL2Lib.ServerControllers.neoforge.installer.actions.server_install"
)
artifact_module = importlib.import_module(
    "MCSL2Lib.ServerControllers.neoforge.installer.json.artifact"
)
version_module = importlib.import_module(
    "MCSL2Lib.ServerControllers.neoforge.installer.json.version"
)

Artifact = artifact_module.Artifact
Library = version_module.Library
ServerInstall = server_install.ServerInstall


class LibrarySource:
    def __init__(self, libraries):
        self.libraries = libraries

    def getLibraries(self):
        return self.libraries


def library(descriptor, sha1):
    artifact = Artifact.from_(descriptor)
    return Library.of({
        "name": descriptor,
        "downloads": {
            "artifact": {
                "path": artifact.getPath(),
                "sha1": sha1,
                "size": 1,
                "url": "https://example.invalid/" + artifact.getFilename(),
            }
        },
    })


class ServerInstallLibraryTests(unittest.TestCase):
    def test_get_libraries_skips_duplicate_artifact_paths(self):
        first_sponge_mixin = library(
            "net.fabricmc:sponge-mixin:0.16.5+mixin.0.8.7",
            "eae828308dd20567b42f66a59595f3dc3afb328e",
        )
        duplicate_sponge_mixin = library(
            "net.fabricmc:sponge-mixin:0.16.5+mixin.0.8.7",
            "80fc3a9f592673cea87f4cd702f87991c6c9fe4d",
        )
        other_library = library("net.neoforged:bus:8.0.5", "abc123")

        installer = object.__new__(ServerInstall)
        installer.version = LibrarySource([first_sponge_mixin, other_library])
        installer.processors = LibrarySource([duplicate_sponge_mixin])
        installer.installerDataBuf = BytesIO()

        libraries = installer.getLibraries()

        self.assertEqual([first_sponge_mixin, other_library], libraries)


if __name__ == "__main__":
    unittest.main()

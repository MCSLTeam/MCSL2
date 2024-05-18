from pathlib import Path

from installer.simple_installer import SimpleInstaller


# def test():
#     from installer.json.util import Util
#     with open("./install_profile.json", "r", encoding="utf-8") as f:
#         text = f.read()
#     profile = Util.loadInstallProfile(text)
#     print(profile)


if __name__ == '__main__':
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #
    # print(os.getcwd())
    # test()
    # art = Artifact.from_("net.minecraftforge:forge:1.20.4-49.0.26:shim")
    # print(art)
    # version = Version.of(json.loads(Path("version.json").read_text()))
    # print(version)
    SimpleInstaller.installServer(
        Path("./Server/Forge-1.20.4-49.0.26.jar"), Path("./Server/")
    )

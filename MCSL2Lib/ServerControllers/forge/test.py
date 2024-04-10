import os

from installer.json.util import Util


def test():
    with open("./install_profile.json", "r", encoding="utf-8") as f:
        text = f.read()
    profile = Util.loadInstallProfile(text)
    print(profile)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print(os.getcwd())
    test()

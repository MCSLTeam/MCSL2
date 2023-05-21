from shutil import which
from subprocess import CalledProcessError, check_output, Popen

from aria2p import Client, API
from platform import system
from os import path as ospath

MCSL2_Aria2Client = API(Client(host="http://localhost", port=6800, secret=""))


def LinuxCheckPackageExists(PackageName):
    try:
        check_output(["which", PackageName])
        return True
    except CalledProcessError:
        return False



def LinuxInstallAria2():
    if which("apt"):
        cmd = ["apt", "install", "-y", "aria2"]
    elif which("pacman"):
        cmd = ["pacman", "-Sy", "--noconfirm", "aria2"]
    elif which("yum"):
        cmd = ["yum", "install", "-y", "aria2"]
    else:
        return "No"
    try:
        Popen(cmd, check=True)
    except CalledProcessError:
        return "InstallFailed"

    return "Installed"


def CheckMCSL2Aria2IsExist():
    CurrentSystem = system().lower()
    if 'windows' in CurrentSystem:
        if not ospath.exists(r"MCSL2/Aria2/aria2c.exe"):
            return 1
        else:
            return 0
    elif 'Linux' in CurrentSystem:
        LinuxCheckPackageExists('aria2')


class Aria2Controller():
    pass

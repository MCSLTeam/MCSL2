import sys
from MCSL2Lib.Controllers.networkController import MCSLNetworkSession
from os import getlogin, name as osname, getenv
from platform import system as sysType, processor
from hashlib import md5


def getAnnouncement():
    return (
        MCSLNetworkSession()
        .get("https://api.mcsl.com.cn/getAnnouncement", headers=__AuthorizationHeaders)
        .text
    )


def checkUpdate():
    return (
        MCSLNetworkSession()
        .get("https://api.mcsl.com.cn/checkUpdate", headers=__AuthorizationHeaders)
        .json()
    )


def countUserAPI():
    pass


# fmt: off
def generateUniqueCode():
    return "-".join([md5(f"{getlogin() if osname == 'nt' else getenv('USER')}{processor()}{sysType()}".encode()).hexdigest()[i:i+4].upper() for i in range(0, 16, 4)])
# fmt: on

__AuthorizationHeaders = {
    "x-mcsl2-client-private-header": next(
        (arg.split("=")[1] for arg in sys.argv[1:] if arg.startswith("--verified-header")), None
    )
}

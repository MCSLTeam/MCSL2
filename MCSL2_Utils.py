from json import loads
from os import mkdir
from os import path as ospath

from PyQt5.QtWidgets import QDialog
from requests import get

from MCSL2_AskDialog import *  # noqa: F403
from MCSL2_Dialog import *  # noqa: F403


# Customize dialogs
class MCSL2Dialog(QDialog, Ui_MCSL2_Dialog):
    def __init__(self, Tip):
        super(MCSL2Dialog, self).__init__()
        self.setupUi(self)
        self.Dialog_label.setText(Tip)


class MCSL2AskDialog(QDialog, Ui_MCSL2_AskDialog):
    def __init__(self, Tip):
        super(MCSL2AskDialog, self).__init__()
        self.setupUi(self)
        self.Dialog_label.setText(Tip)


# The function of calling MCSL2 Dialog
def CallMCSL2Dialog(Tip, isNeededTwoButtons):
    if isNeededTwoButtons == 0:
        MCSL2Dialog(Tip).exec()
    elif isNeededTwoButtons == 1:
        MCSL2AskDialog(Tip).exec()
    else:
        pass


def InitMCSL():
    if not ospath.exists(r"MCSL2"):
        mkdir(r"MCSL2")
        CallMCSL2Dialog(Tip="请注意：\n\n本程序无法在125%的\n\nDPI缩放比下正常运行。\n(本提示仅在首次启动出现)",
                        isNeededTwoButtons=0)
        mkdir(r"MCSL2/Aria2")
        with open(r"./MCSL2/MCSL2_Config.json", "w+", encoding="utf-8") as InitConfig:
            ConfigTemplate = ""
            InitConfig.write(ConfigTemplate)
            InitConfig.close()
        with open(
                r"./MCSL2/MCSL2_ServerList.json", "w+", encoding="utf-8"
        ) as InitServerList:
            ServerListTemplate = '{\n  "MCSLServerList": [\n    {\n      "name": "MCSLReplacer",\n      ' \
                                 '"core_file_name": "MCSLReplacer",\n      "java_path": "MCSLReplacer",' \
                                 '\n      "min_memory": "MCSLReplacer",\n      "max_memory": "MCSLReplacer"\n    }\n  ' \
                                 ']\n} '
            InitServerList.write(ServerListTemplate)
            InitServerList.close()
        if not ospath.exists(r"Servers"):
            mkdir(r"./Servers")

        pass
    else:
        if not ospath.exists(r"Servers"):
            mkdir(r"./Servers")
        pass


def ParseDownloaderAPIUrl(DownloadSource, DownloadType):
    UrlPrefix = "https://raw.iqiq.io/LxHTT/MCSLDownloaderAPI/master/"
    SourceSuffix = ["SharePoint", "Gitee", "luoxisCloud", "GHProxy", "GitHub"]
    TypeSuffix = [
        "/JavaDownloadInfo.json",
        "/SpigotDownloadInfo.json",
        "/PaperDownloadInfo.json",
        "/BungeeCordDownloadInfo.json",
        "/OfficialCoreDownloadInfo.json",
    ]
    DownloadAPIUrl = UrlPrefix + SourceSuffix[DownloadSource] + TypeSuffix[DownloadType]
    DecodeDownloadJsonsSS = DecodeDownloadJsons(DownloadAPIUrl)
    SubWidgetNames = DecodeDownloadJsonsSS[0]
    DownloadUrls = DecodeDownloadJsonsSS[1]
    FileNames = DecodeDownloadJsonsSS[2]
    FileFormats = DecodeDownloadJsonsSS[3]
    return SubWidgetNames, DownloadUrls, FileNames, FileFormats


def DecodeDownloadJsons(RefreshUrl):
    SubWidgetNames = []
    DownloadUrls = []
    FileFormats = []
    FileNames = []
    try:
        DownloadJson = get(RefreshUrl).text
    except:
        Tip = "无法连接MCSLAPI，\n\n请检查网络或系统代理设置"
        CallMCSL2Dialog(Tip, isNeededTwoButtons=0)
        return -1, -1, -1, -1
    try:
        PyDownloadList = loads(DownloadJson)["MCSLDownloadList"]
        for i in PyDownloadList:
            SubWidgetName = i["name"]
            SubWidgetNames.insert(0, SubWidgetName)
            DownloadUrl = i["url"]
            DownloadUrls.insert(0, DownloadUrl)
            FileFormat = i["format"]
            FileFormats.insert(0, FileFormat)
            FileName = i["filename"]
            FileNames.insert(0, FileName)
        return SubWidgetNames, DownloadUrls, FileNames, FileFormats
    except:
        print(DownloadJson)
        Tip = "可能解析api内容失败\n\n请检查网络或自己的节点设置"
        CallMCSL2Dialog(Tip, isNeededTwoButtons=0)
        return -1, -1, -1, -1


# def GetFileVersion(File):
#     FileVersionInfo = GetFileVersionInfo(File, sep)
#     FileVersionMS = FileVersionInfo['FileVersionMS']
#     FileVersionLS = FileVersionInfo['FileVersionLS']
#     Version = '%d.%d.%d.%04d' % (
#         HIWORD(FileVersionMS), LOWORD(FileVersionMS), HIWORD(FileVersionLS), LOWORD(FileVersionLS))
#     return Version
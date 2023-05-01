from requests import get
from MCSL2_Libs.MCSL2_Dialog import CallMCSL2Dialog

class Updater:
    def __init__(self, Version):
        self.CheckUpdateUrlPrefix = "http://api.2018k.cn/checkVersion?id=BCF5D58B4AE6471E98CFD5A56604560B&version="
        self.CheckUpdateUrl = self.CheckUpdateUrlPrefix + Version

    def GetLatestVersionInformation(self):
        LatestVersionInformation = get(self.CheckUpdateUrl).text.split("|")
        if LatestVersionInformation[0] == "true":
            Arg = self.GetMoreInformation(LatestVersionInformation)
            return 1, Arg
        elif LatestVersionInformation[0] == "false":
            CallMCSL2Dialog("ProgramVersionIsUpToDate",OtherTextArg=None, isNeededTwoButtons=0, ButtonArg=None)
            return [0]
        else:
            pass

    def GetMoreInformation(self, LatestVersionInformation):
        UpdateDownloadUrl = LatestVersionInformation[3]
        GetUpdateContentsUrl = "http://api.2018k.cn/getExample?id=BCF5D58B4AE6471E98CFD5A56604560B&data=remark"
        WhatInLatestVersion = get(GetUpdateContentsUrl).text
        LatestVersionNumber = LatestVersionInformation[4]
        return LatestVersionNumber, WhatInLatestVersion

    def GetNoticeText(self):
        GetNoticeUrl = "http://api.2018k.cn/getExample?id=BCF5D58B4AE6471E98CFD5A56604560B&data=notice"
        GetTodayUserCountUrl = "http://api.2018k.cn/today?id=BCF5D58B4AE6471E98CFD5A56604560B"
        Notice = get(GetNoticeUrl).text
        return Notice
#     Copyright 2023, MCSL Team, mailto:lxhtt@mcsl.com.cn
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
'''
A function for communicatng with MCSLAPI.
'''

from json import loads
from typing import Callable
from random import randint
from PyQt5.QtCore import pyqtSignal, QThread

from MCSL2Lib.networkController import Session
import os 
import json

def get_mcslapicon():
    '''获得配置'''
    if not os.path.exists('./mcslapi.json'):
        with open('./mcslapi.json','w') as f:
            data = {
                'node_url':'https://hardbin.com/ipns/mcslapiipfs.x-xh.cn/',
                'equilibriumList':'Gitee'
            }
            f.write(json.dumps(data))
            return data
    else:
        with open('./mcslapi.json','r') as f:
            return json.loads(f.read())

def change_mcslapicon(node_url = False , equilibriumList = False):
    '''更改配置'''
    data = {}
    with open('./mcslapi.json','r') as j:
        try:
            data = json.dumps(j.read())
        except:
            j.close()
    with open('./mcslapi.json','w') as f:
        try:
            if node_url :
                data['node_url'] = node_url
            elif equilibriumList:
                data['equilibriumList'] = equilibriumList
        except:
            data = {
                'node_url':'https://hardbin.com/ipns/mcslapiipfs.x-xh.cn/',
                'equilibriumList':'Gitee'
            }
            if node_url :
                data['node_url'] = node_url
            elif equilibriumList:
                data['equilibriumList'] = equilibriumList
        f.write(json.dumps(data))
    
        return True


class MCSLAPIDownloadURLParser:
    """URL设定器"""


    def __init__(self):
        pass

    @staticmethod
    def parseDownloaderAPIUrl():
        #  ["SharePoint", "Gitee"]
        con = get_mcslapicon()
        equilibriumList = con['equilibriumList']
        UrlArg = f"{con['node_url']}{equilibriumList}"
        TypeArg = [
            "/JavaDownloadInfo.json",
            "/SpigotDownloadInfo.json",
            "/PaperDownloadInfo.json",
            "/BungeeCordDownloadInfo.json",
            "/OfficialCoreDownloadInfo.json",
        ]
        rv = {}
        for i in range(len(TypeArg)):
            DownloadAPIUrl = UrlArg + TypeArg[i]
            (
                downloadFileTitles,
                downloadFileURLs,
                downloadFileNames,
                downloadFileFormats,
            ) = MCSLAPIDownloadURLParser.decodeDownloadJsons(DownloadAPIUrl)
            rv.update(
                {
                    i: dict(
                        zip(
                            (
                                "downloadFileTitles",
                                "downloadFileURLs",
                                "downloadFileNames",
                                "downloadFileFormats",
                            ),
                            (
                                downloadFileTitles,
                                downloadFileURLs,
                                downloadFileNames,
                                downloadFileFormats,
                            ),
                        )
                    )
                }
            )
        return rv

    @staticmethod
    def decodeDownloadJsons(RefreshUrl):
        downloadFileTitles = []
        downloadFileURLs = []
        downloadFileFormats = []
        downloadFileNames = []
        try:
            DownloadJson = Session.get(RefreshUrl).text
        except Exception as e:
            return -2, -2, -2, -2
        try:
            PyDownloadList = loads(DownloadJson)["MCSLDownloadList"]
            for i in PyDownloadList:
                downloadFileTitle = i["name"]
                downloadFileTitles.insert(0, downloadFileTitle)
                downloadFileURL = i["url"]
                downloadFileURLs.insert(0, downloadFileURL)
                downloadFileFormat = i["format"]
                downloadFileFormats.insert(0, downloadFileFormat)
                downloadFileName = i["filename"]
                downloadFileNames.insert(0, downloadFileName)
            return (
                downloadFileTitles,
                downloadFileURLs,
                downloadFileNames,
                downloadFileFormats,
            )
        except:
            return -1, -1, -1, -1


class FetchMCSLAPIDownloadURLThread(QThread):
    """
    用于获取网页内容的线程
    结束时发射fetchSignal信号，参数为url和data组成的元组
    """

    fetchSignal = pyqtSignal(dict)

    def __init__(self, FinishSlot: Callable = ...):
        super().__init__()
        self._id = None
        self.Data = None
        if FinishSlot is not ...:
            self.fetchSignal.connect(FinishSlot)

    def getURL(self):
        return self.url

    def run(self):
        self.fetchSignal.emit(MCSLAPIDownloadURLParser.parseDownloaderAPIUrl())

    def getData(self):
        return self.Data


class FetchMCSLAPIDownloadURLThreadFactory:
    def __init__(self):
        self.singletonThread = None

    def create(self, _singleton=False, finishSlot=...) -> FetchMCSLAPIDownloadURLThread:
        if _singleton:
            if self.singletonThread is not None and self.singletonThread.isRunning():
                return self.singletonThread
            else:
                thread = FetchMCSLAPIDownloadURLThread(finishSlot)
                self.singletonThread = thread
                return thread
        else:
            return FetchMCSLAPIDownloadURLThread(finishSlot)

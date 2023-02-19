from json import loads
from requests import get


def ParseDownloaderAPIUrl(DownloadSource, DownloadType):
    UrlPrefix = 'https://jsd.cdn.zzko.cn/gh/LxHTT/MCSLDownloaderAPI@master/'
    SourceSuffix = ['SharePoint', 'Gitee', 'luoxisCloud', 'GHProxy', 'GitHub']
    TypeSuffix = ['/JavaDownloadInfo.json', '/SpigotDownloadInfo.json', '/PaperDownloadInfo.json',
                  '/BungeeCordDownloadInfo.json']
    DownloadAPIUrl = UrlPrefix + SourceSuffix[DownloadSource] + TypeSuffix[DownloadType]
    DecodeDownloadJsons(DownloadAPIUrl)


def DecodeDownloadJsons(RefreshUrl):
    SubWidgetNames = []
    DownloadUrls = []
    FileFormats = []
    FileNames = []
    DownloadJson = get(RefreshUrl).text
    PyDownloadList = loads(DownloadJson)['MCSLDownloadList']
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

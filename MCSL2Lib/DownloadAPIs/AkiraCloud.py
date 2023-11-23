from MCSL2Lib.Controllers.networkController import (
    MCSLNetworkSession,
    MCSLNetworkHeaders,
)
import re
from html.parser import HTMLParser


class AkiraHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inTable = False
        self.inTd = False
        self.currentData = []
        self.allList = []

    def handle_starttag(self, tag):
        if tag == "table":
            self.inTable = True
        elif self.inTable and tag == "td":
            self.inTd = True

    def handle_data(self, data):
        if self.inTd:
            self.currentData.append(data.strip())

    def handle_endtag(self, tag):
        if tag == "table":
            self.inTable = False
        elif tag == "td":
            self.inTd = False
            if self.currentData:
                self.allList.append(self.currentData[-1])
                self.currentData = []

    def feed(self, data: str) -> list:
        super().feed(data)
        if "Parent Directory" in self.allList:
            self.allList.remove("Parent Directory")
        if "常用工具" in self.allList:
            self.allList.remove("常用工具")
        if "mirror.akiracloud.net" in self.allList:
            self.allList.remove("mirror.akiracloud.net")
        return self.allList


class AkiraCloudDownloadURLParser:

    def __init__(self) -> None:
        pass

    @classmethod
    def getDownloadTypeList(cls) -> list:
        return cls._parseHTML(cls._getAPI("/"))
    
    @classmethod
    def getDownloadCoreList(cls, coreType: str) -> list:
        return cls._parseHTML(cls._getAPI(f"/{coreType}"))

    @classmethod
    def _getAPI(APIPath: str) -> str:
        return (
            MCSLNetworkSession()
            .get(
                url=f"https://mirror.akiracloud.net{APIPath}",
                headers=MCSLNetworkHeaders,
            )
            .text
        )

    @classmethod
    def _parseHTML(htmlContent: str):
        parsedList = AkiraHTMLParser().feed(htmlContent)

        return list(
            [
                item
                for item in parsedList
                if not re.search(
                    re.compile(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}|\d+\sKB"), item
                )
            ]
        )

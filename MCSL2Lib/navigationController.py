# from importlib import import_module
# naviPage = import_module("MCSL2Lib.windowInterface")

# Change into the following thing:
from MCSL2Lib.lazyLoader import LazyLoader
naviPage = LazyLoader("windowInterface", globals(), "MCSL2Lib.windowInterface")

def switchToHomePage():
    naviPage.Window().switchTo(naviPage.Window().homeInterface)

def switchToConfigurePage():
    naviPage.Window().switchTo(naviPage.Window().configureInterface)

def switchToDownloadPage():
    naviPage.Window().switchTo(naviPage.Window().downloadInterface)
    # naviPage.Window().switchTo(naviPage.Window().downloadInterface)
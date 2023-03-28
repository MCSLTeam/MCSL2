from pyperclip import copy
def ParseUrl():
    Url = input().split("/")
    ShareIdSplitter = Url[7].split("?")
    ShareId = ShareIdSplitter[0]
    NewUrl = "https://" + Url[2] + "/" + Url[5] + "/" + Url[6] + "/_layouts/52/download.aspx?share=" + ShareId
    print(NewUrl)
    print("--------------------------------------------------------------------------------")
    copy(NewUrl)


while True:
    ParseUrl()
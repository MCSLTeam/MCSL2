from pyperclip import copy
def ParseUrl():
    Url = input().split("/")
    NewUrl = f"https://{Url[2]}/{Url[5]}/{Url[6]}/_layouts/52/download.aspx?share={Url[7].split('?')[0]}"
    print(f"结果：\n{NewUrl}\n--------------------------------------------------------------------------------")
    copy(NewUrl)


while True:
    ParseUrl()
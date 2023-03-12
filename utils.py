import os
import re

FUZZY_SEARCH = True
search_set = {"users", "java", "jdk", "env", "环境", "run", "软件", "jre", "bin", "mc", "software", "cache", "temp",
              "corretto", "roaming", "users", "craft", "program", "世界", "net", "游戏", "oracle", "game", "file",
              "data", "jvm", "服务", "server", "客户", "client", "整合", "应用", "运行", "前置", "mojang", "官启",
              "新建文件夹", "eclipse", "microsoft", "hotspot", "runtime", "x86", "x64", "forge", "原版", "optifine",
              "官方", "启动", "hmcl", "mod", "高清", "download", "launch", "程序", "path", "国服", "网易", "ext",
              "netease", "1.", "启动"}

#搜索Java文件
def fine_str(s):
    for _s in search_set:
        if _s in s:
            return True
    return False

java_list = []

# 递归遍历
def search_file(path,file_key,file_ext):
    if FUZZY_SEARCH:
        for file in os.listdir(path):
            try:
                if os.path.isfile(path + '/' + file):
                    name, ext = os.path.splitext(file)
                    if(re.match(f".*?bin/{file_key}.{file_ext}",path+"/"+file)):
                        java_list.append(path+"/"+file)
                elif fine_str(file.lower()):
                    search_file(path + '/' + file,file_key,file_ext)
            except PermissionError:
                pass


def FindJava():
    java_list.clear()
    # 检查A-Z:/下的所有文件夹
    for i in range(65, 91):
        path = chr(i) + ':/'
        if os.path.exists(path):
            search_file(path,"java","exe")


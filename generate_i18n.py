#     Copyright 2024, MCSL Team, mailto:services@mcsl.com.cn
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
from os import listdir, makedirs, system, remove
from shutil import move, rmtree
import sys


class InternationalizationGenerator:
    def __init__(self, lang: str = "en_US", delete_old: bool = False):  # or zh_CN
        self.d = delete_old
        self.lang = lang
        self.generatedList = []
        self.ControllerPath = "MCSL2Lib/ProgramControllers/"
        self.ServerControllersPath = "MCSL2Lib/ServerControllers/"
        self.PagesPath = "MCSL2Lib/Pages/"
        self.WidgetsPath = "MCSL2Lib/Widgets/"

        self.excludeItem = [
            "MCSL2Lib/__pycache__",
            "MCSL2Lib/Controllers/__pycache__",
            "MCSL2Lib/ProgramControllers/__pycache__",
            "MCSL2Lib/Pages/__pycache__",
            "MCSL2Lib/Widgets/__pycache__",
            "MCSL2Lib/Resources/__pycache__",
            "MCSL2Lib/Resources/icons.py",
            "MCSL2Lib/ProgramControllers/__init__.py",
            "MCSL2Lib/ProgramControllers/aria2ClientController.py",
            "MCSL2Lib/ProgramControllers/interfaceController.py",
            "MCSL2Lib/ProgramControllers/javaDetector.py",
            "MCSL2Lib/ProgramControllers/logController.py",
            "MCSL2Lib/ProgramControllers/networkController.py",
            "MCSL2Lib/ProgramControllers/serverImporter.py",
            "MCSL2Lib/ProgramControllers/ServerSettingController.py",
            "MCSL2Lib/ProgramControllers/settingsController.py",
            "MCSL2Lib/ProgramControllers/DownloadAPI",
            "MCSL2Lib/ProgramControllers/DownloadAPI/__init__.py",
            "MCSL2Lib/ProgramControllers/DownloadAPI/AkiraCloud.py",
            "MCSL2Lib/ProgramControllers/DownloadAPI/FastMirrorAPI.py",
            "MCSL2Lib/ProgramControllers/DownloadAPI/MCSLAPI.py",
            "MCSL2Lib/ProgramControllers/DownloadAPI/PolarsAPI.py",
            "MCSL2Lib/ServerControllers/processCreator.py",
            "MCSL2Lib/ServerControllers/serverUtils.py",
            "MCSL2Lib/ServerControllers/serverErrorHandler.py",
            "MCSL2Lib/Pages/selectNewJavaPage.py",
            "MCSL2Lib/Pages/selectImportJavaPage.py",
            "MCSL2Lib/Pages/selectNewJavaPage.py",
            "MCSL2Lib/Widgets/FastMirrorWidgets.py",
            "MCSL2Lib/Widgets/exceptionWidget.py",
            "MCSL2Lib/Widgets/myScrollArea.py",
            "MCSL2Lib/Widgets/pluginWidget.py",
            "MCSL2Lib/Widgets/PolarsWidgets.py",
            "MCSL2Lib/Widgets/singleMCSLAPIDownloadWidget.py",
            "MCSL2Lib/__init__.py",
            "MCSL2Lib/noVerification.py",
            "MCSL2Lib/singleton.py",
            "MCSL2Lib/utils.py",
            "MCSL2Lib/variables.py",
        ]
        self.Controller = listdir(self.ControllerPath)
        self.ServerControllers = listdir(self.ServerControllersPath)
        self.Pages = listdir(self.PagesPath)
        self.Widgets = listdir(self.WidgetsPath)
        self.find()

    def find(self):
        # fmt: off
        for i in range(len(self.Controller)):
            self.Controller[i] = self.ControllerPath + self.Controller[i]
        for i in range(len(self.ServerControllers)):
            self.ServerControllers[i] = self.ServerControllersPath + self.ServerControllers[i]
        for i in range(len(self.Pages)):
            self.Pages[i] = self.PagesPath + self.Pages[i]
        for i in range(len(self.Widgets)):
            self.Widgets[i] = self.WidgetsPath + self.Widgets[i]
        # fmt: on
        self.totalFileList = sorted(
            list(set(self.Controller + self.ServerControllers + self.Pages + self.Widgets)),
            key=lambda x: (x.split("/")[1][0], x.split("/")[-1][0]),
        )
        self.totalFileList = [
            file
            for file in self.totalFileList
            if file.endswith(".py") and file not in self.excludeItem
        ]
        self.totalFileList.append("MCSL2Lib/windowInterface.py")
        print(self.totalFileList, "\n")
        self.generate()

    def gather(self):
        print("Gathering file...\n\n", self.generatedList, "\n")
        with open(file=f"i18n/{self.lang}.ts", mode="w+", encoding="utf-8") as f:
            f.write(
                f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE TS>\n<TS version="2.1" language="{self.lang}" sourcelanguage="zh_CN">\n<context>\n'
            )
        for file in self.generatedList:
            with open(file=file, mode="r", encoding="utf-8") as f:
                c = f.read()
            remove(file)
            with open(file=f"i18n/{self.lang}.ts", mode="a", encoding="utf-8") as f2:
                f2.write(c)
        with open(file=f"i18n/{self.lang}.ts", mode="a", encoding="utf-8") as f2:
            f2.write("\n</context>\n</TS>")
        print(f"Successfully created {self.lang}.ts\n")

    def generate(self):
        # fmt: off
        for file in self.totalFileList:
            if file.endswith(".py") and file not in self.excludeItem:
                try:
                    try:
                        remove(file.replace('.py', '.ts'))
                    except FileNotFoundError:
                        pass
                    # Delete old translation(if needed)
                    if self.d:
                        try:
                            remove(f"i18n/{file.replace('.py', '.ts')}")
                        except FileNotFoundError:
                            pass
                    # Generate new translation
                    system(f"pylupdate5 {file} -ts {file.replace('.py', '.ts')}")
                    # Move to `i18n` folder
                    move(file.replace(".py", ".ts"), f"i18n/{file.replace('.py', '.ts')}")
                    with open(file=f"i18n/{file.replace('.py', '.ts')}", mode="r", encoding="utf-8") as f:
                        c = f.read()
                    c = c.replace(file.split("/")[-1], file).replace('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE TS>\n<TS version="2.1">\n<context>\n', "").replace("\n</context>\n</TS>", "")  # noqa: E501
                    with open(file=f"i18n/{file.replace('.py', '.ts')}", mode="w", encoding="utf-8") as f2:
                        f2.write(c)
                    print(f"Success! | {file} --> i18n/{file.replace('.py', '.ts')}\n")
                    self.generatedList.append(f"i18n/{file.replace('.py', '.ts')}")
                except Exception:
                    print(f"Error! | {file} -x-> i18n/{file.replace('.py', '.ts')}\n")
                    pass

        print("-------------------------------------------\nGenerate file done!\n")
        self.gather()
        # fmt: on


folderList = [
    "i18n",
    "i18n/MCSL2Lib",
    "i18n/MCSL2Lib/ProgramControllers",
    "i18n/MCSL2Lib/ServerControllers",
    "i18n/MCSL2Lib/Pages",
    "i18n/MCSL2Lib/Widgets",
]
for folder in folderList:
    makedirs(folder, exist_ok=True)
InternationalizationGenerator(sys.argv[-1])
rmtree("i18n/MCSL2Lib", ignore_errors=True)

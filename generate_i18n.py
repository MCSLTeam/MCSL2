from os import listdir, makedirs, system, remove
from shutil import move


class InternationalizationGenerator:
    def __init__(self, delete_old: bool = False):
        self.d = delete_old
        self.ControllerPath = "MCSL2Lib/Controllers/"
        self.ImportServerTypesPath = "MCSL2Lib/ImportServerTypes/"
        self.PagesPath = "MCSL2Lib/Pages/"
        self.WidgetsPath = "MCSL2Lib/Widgets/"
        self.excludeItem = [
            "MCSL2Lib/Controllers/ServerSettingController.py",
            "MCSL2Lib/Controllers/__pycache__",
            "MCSL2Lib/Controllers/aria2ClientController.py",
            "MCSL2Lib/Controllers/interfaceController.py",
            "MCSL2Lib/Controllers/javaDetector.py",
            "MCSL2Lib/Controllers/logController.py",
            "MCSL2Lib/Controllers/networkController.py",
            "MCSL2Lib/Controllers/settingsController.py",
            "MCSL2Lib/ImportServerTypes/__pycache__",
            "MCSL2Lib/Pages/__pycache__",
            "MCSL2Lib/Pages/selectNewJavaPage.py",
            "MCSL2Lib/Widgets/FastMirrorWidgets.py",
            "MCSL2Lib/Widgets/__pycache__",
            "MCSL2Lib/Widgets/exceptionWidget.py",
            "MCSL2Lib/Widgets/myScrollArea.py",
            "MCSL2Lib/Widgets/pluginWidget.py",
        ]
        self.Controller = listdir(self.ControllerPath)
        self.ImportServerTypes = listdir(self.ImportServerTypesPath)
        self.Pages = listdir(self.PagesPath)
        self.Widgets = listdir(self.WidgetsPath)
        self.gennerateList()

    def gennerateList(self):
        # fmt: off
        for i in range(len(self.Controller)):
            self.Controller[i] = self.ControllerPath + self.Controller[i]
        for i in range(len(self.ImportServerTypes)):
            self.ImportServerTypes[i] = self.ImportServerTypesPath + self.ImportServerTypes[i]
        for i in range(len(self.Pages)):
            self.Pages[i] = self.PagesPath + self.Pages[i]
        for i in range(len(self.Widgets)):
            self.Widgets[i] = self.WidgetsPath + self.Widgets[i]
        # fmt: on
        self.totalFileList = sorted(
            list(set(self.Controller + self.ImportServerTypes + self.Pages + self.Widgets)),
            key=lambda x: (x.split("/")[1][0], x.split("/")[-1][0]),
        )
        self.totalFileList.append("MCSL2Lib/windowInterface.py")
        print(self.totalFileList)
        print("-------------------------------------------\nGenerate list done!\n")
        self.generate()

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
                    print(f"Success! | {file} --> i18n/{file.replace('.py', '.ts')}\n")
                except Exception:
                    print(f"Error! | {file} -x-> i18n/{file.replace('.py', '.ts')}\n")
                    pass
        print("-------------------------------------------\nGenerate file done!\n")
        # fmt: on


folderList = [
    "i18n",
    "i18n/MCSL2Lib",
    "i18n/MCSL2Lib/Controllers",
    "i18n/MCSL2Lib/ImportServerTypes",
    "i18n/MCSL2Lib/Pages",
    "i18n/MCSL2Lib/Widgets",
]
for folder in folderList:
    makedirs(folder, exist_ok=True)
InternationalizationGenerator()

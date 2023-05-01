from datetime import datetime

LogColor = ['\033[92m', '\033[93m', '\033[91m', '\033[1;91m']
LogType = ['INFO', 'WARN', 'FAIL', 'ERR!']
ColorSuffix = "\033[0m"
HH = "\n"


class MCSL2Logger:
    def __init__(self, Msg, MsgArg, MsgLevel, LogFilesCount):
        """
        :param Msg - What you want to show.
        :param MsgLevel
                1 - INFO , means normal output.
                2 - WARN , means something not recommended.
                3 - FAIL , means the program has some trouble but has been known.
                4 - ERR! , means the program has some trouble but unexpected.
        """
        if MsgArg is None:
            MsgArg = ""
        else:
            pass
        try:
            self.Msg = getattr(LoggerMsg(), Msg) + MsgArg
        except AttributeError:
            self.Msg = Msg + MsgArg
        self.MsgLevel = MsgLevel
        self.LogFilesCountN = int(LogFilesCount) + 1

    def Log(self):
        Time = datetime.now().strftime('%H:%M:%S')
        ConsoleLog = f"{Time}  [ {LogColor[self.MsgLevel]}{LogType[self.MsgLevel]}{ColorSuffix} ]  {self.Msg}"
        FileLog = f"{Time}  [ {LogType[self.MsgLevel]} ]  {self.Msg}{HH}"
        with open(f'MCSL2/Logs/Log{self.LogFilesCountN}.txt', 'a') as WriteLog:
            WriteLog.write(f"{FileLog}")
        print(ConsoleLog)


def InitNewLogFile(LogFilesCount):
    LogFilesCount += 1
    with open(f'MCSL2/Logs/Log{LogFilesCount}.txt', 'w+') as GenerateNewLogFile:
        GenerateNewLogFile.write("")
        GenerateNewLogFile.close()


class LoggerMsg:
    def __init__(self):
        self.InitMCSL = "检查程序完整性..."
        self.InitUI = "初始化UI界面..."
        self.ReadConfig = "读取配置 MCSL2/MCSL2_Config.json"
        self.InitFunctionsBind = "初始化功能绑定..."
        self.FinishStarting = "程序启动完成！"
        self.Close_ButtonPressed = "Close_PushButton 被按下..."
        self.MCSLExit = "程序退出"
        self.Minimize_PushButtonPressed = "Minimize_PushButton 被按下..."
        self.WindowMinimize = "程序窗口最小化"
        self.RefreshBlue = "刷新各个Blue控件"
        self.ToHomePage = "FunctionsStackedWidget切换至HomePage"
        self.ToConfigPage = "FunctionsStackedWidget切换至ConfigPage"
        self.ToDownloadPage = "FunctionsStackedWidget切换至DownloadPage"
        self.ToConsolePage = "FunctionsStackedWidget切换至HomePage"
        self.ToToolsPage = "FunctionsStackedWidget切换至ConfigPage"
        self.ToSettingsPage = "FunctionsStackedWidget切换至DownloadPage"
        self.ChangeCurrentVersionLabel = "自动更新显示当前版本的Label组件..."
        self.Choose_Server_PushButtonPressed = "Choose_Server_PushButton 被按下..."
        self.ToChooseServerPage = "FunctionsStackedWidget切换至ChooseServerPage"
        self.TryToGetGlobalServerList = "尝试读取全局服务器列表..."
        self.NoServerCanBeFound = "服务器列表为空！"
        self.ShowDialog = "唤起MCSL2Dialog，类型为"
        self.Start_PushButtonPressed = "Start_PushButton被按下..."
        self.TryToGetServerConfig = "尝试获取服务器配置..."
        self.ToChooseJavaPage = "FunctionsStackedWidget切换至ChooseJavaPage"
        self.StartInitSelectJavaSubWidget = "刷新ChooseJavaScrollArea"
        self.ChangeDownloadSource = "切换MCSLAPI下载源至："
        self.StartManuallySelectJava = "手动导入Java..."
        self.ShowQFileDialog = "唤起QFileDialog"
        self.ChooseJavaOK = "手动导入Java - 导入成功"
        self.ChooseJavaNothing = "手动导入Java - 取消选择/未选择"
        self.ChooseJavaInvalid = "手动导入Java - 无效Java"
        self.StartManuallySelectCore = "手动导入核心..."
        self.ChooseCoreOK = "手动导入核心 - 导入成功"
        self.ChooseCoreNothing = "手动导入核心 - 取消选择/未选择"
        self.StartSaveMinecraftServer = "尝试创建服务器..."
        self.AllConfigIsOK = "各参数齐全！"
        self.AddServerSuccess = "创建服务器成功！"
        self.AddServerFailed = "创建服务器失败：缺失参数"
        self.AddServerUnexpectedFailed = "创建服务器失败：未知错误"
        self.ConfigPageNoServerCore = "无服务器核心"
        self.ConfigPageNoJava = "无Java"
        self.ConfigPageNoJavaAndServerCore = "无Java和服务器核心"
        self.ConfigPageNoServerName = "无服务器名称"
        self.ConfigPageNoServerNameAndServerCore = "无服务器名称和服务器核心"
        self.ConfigPageNoServerNameAndJava = "无服务器名称和Java"
        self.ConfigPageOnlyMinMemoryAndMaxMemory = "仅设置内存"
        self.ConfigPageNoMaxMemory = "无最大内存"
        self.ConfigPageNoMaxMemoryAndServerCore = "无最大内存和服务器核心"
        self.ConfigPageNoMaxMemoryAndJava = "无最大内存和Java"
        self.ConfigPageNoServerCoreAndJavaAndMaxMemory = "无服务器核心、Java和最大内存"
        self.ConfigPageNoServerNameAndMaxMemory = "无服务器名称和最大内存"
        self.ConfigPageNoServerCodeAndServerNameAndMaxMemory = "无服务器核心、服务器名称和最大内存"
        self.ConfigPageNoJavaAndServerNameAndMaxMemory = "无Java、服务器名称和最大内存"
        self.ConfigPageOnlyMinMemory = "仅设置最小内存"
        self.ConfigPageNoMinMemory = "无最小内存"
        self.ConfigPageNoServerCoreAndMinMemory = "无服务器核心和最小内存"
        self.ConfigPageNoJavaAndMinMemory = "无Java和最小内存"
        self.ConfigPageNoServerCoreAndJavaAndMinMemory = "无服务器核心、Java和最小内存"
        self.ConfigPageNoServerNameAndMinMemory = "无服务器名称和最小内存"
        self.ConfigPageNoServerCoreAndServerNameAndMinMemory = "无服务器核心、服务器名称和最小内存"
        self.ConfigPageNoJavaAndServerNameAndMinMemory = "无Java、服务器名称和最小内存"
        self.ConfigPageOnlyMaxMemory = "仅设置最大内存"
        self.ConfigPageNoMinMemoryAndMaxMemory = "无内存"
        self.ConfigPageNoServerCoreAndMinMemoryAndMaxMemory = "无服务器核心和内存"
        self.ConfigPageNoJavaAndMinMemoryAndMaxMemory = "无Java和内存"
        self.ConfigPageOnlyServerName = "仅设置服务器名称"
        self.ConfigPageNoServerNameAndMinMemoryAndMaxMemory = "无服务器名称和内存"
        self.ConfigPageOnlyJava = "仅设置Java"
        self.ConfigPageOnlyServerCore = "仅设置服务器核心"
        self.ConfigPageNothing = "什么都没设置"
        self.StartAutoDetectJava = "开始自动搜索Java..."
        self.FinishedAutoDetectJava = "搜索结束。结果：\n"
        self.ManuallySkipChooseGotJava = "Choose_Java_Back_PushButton 被按下，FunctionsStackedWidget切换至ConfigPage"
        self.GoToDownloadJava = "Download_Java_PushButton 被按下，FunctionsStackedWidget切换至DownloadPage"
        self.SelectJavaDownload = "DownloadSwitcher_TabWidget切换至JavaTab"
        self.SelectSpigotDownload = "DownloadSwitcher_TabWidget切换至SpigotTab"
        self.SelectPaperDownload = "DownloadSwitcher_TabWidget切换至PaperTab"
        self.SelectBungeeCordTabDownload = "DownloadSwitcher_TabWidget切换至BungeeCordTabTab"
        self.SelectOfficialCoreTabDownload = "DownloadSwitcher_TabWidget切换至OfficialCoreTabTab"
        self.TryRefreshDownloadType = "尝试刷新下载页面..."
        self.StartRefreshDownloadType = "开始从MCSLAPI获取最新链接以刷新下载页面..."
        self.NoNeedToRefreshDownloadType = "存在DownloadSource且不为空，不再重新获取MCSLAPI"
        self.StartInitDownloadSubWidget = "刷新下载页面"
        self.StartInitSelectJavaSubWidget = "刷新选择Java页面"
        self.StartInitSelectServerSubWidget = "刷新选择服务器页面"
        self.GotServerInfo = "获取到服务器配置信息"
        self.RunParseSrollAreaItemButtons = "检测信号发送Button的objectName中，当前FunctionsStackedWidget.currentIndex()为"
        self.ChoseJava = "选择列表中的Java完毕"
        self.ChoseServer = "选择服务器完毕"
        self.CheckUpdate = "开始检查更新..."
        self.NewVersionAvailable = "有新版本：v"
        self.UpdateContent = "更新内容："
        self.ToUpdatePage = "FunctionsStackedWidget切换至UpdatePage"
        self.GetNotice = "获取公告中..."
        self.ChangeConfig = "改变设置："

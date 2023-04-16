from datetime import datetime

LogColor = ['\033[92m', '\033[93m', '\033[91m', '\033[1;91m']
LogType = ['INFO', 'WARN', 'FAIL', 'ERR!']
Logs = []


class MCSL2Logger:
    def __init__(self, Msg, MsgLevel, LogFilesCount):
        self.Msg = Msg
        self.MsgLevel = MsgLevel  # Can be 0 , 1 , 2 , 3
        self.LogFilesCount = LogFilesCount

    def PrintLog(self, Mode):
        global Logs
        '''
        Info --> MsgLevel = 1
        Warning --> MsgLevel = 2
        Fail --> MsgLevel = 3
        UnexpectedFail --> MsgLevel = 4
        '''
        Time = datetime.now().strftime('%H:%M:%S')
        Log = Time + "  [ " + LogColor[self.MsgLevel] + LogType[self.MsgLevel] + "\033[0m ]  " + self.Msg
        if Mode == 0:  # Normally allocate
            print(Log)
            Logs.append(Log)
            if len(Logs) >= 30:
                self.SaveLog()
        elif Mode == 1:  # Standalone run
            print(Log)

    def SaveLog(self):
        global Logs
        LogFile = "MCSL2/Logs/Log%d" % self.LogFilesCount
        with open(LogFile, "a+", encoding='utf-8') as WriteLog:
            for i in range(len(Logs)):
                WriteLog.write(Logs[i])
                WriteLog.close()

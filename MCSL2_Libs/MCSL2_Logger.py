from datetime import datetime

LogColor = ['\033[92m', '\033[93m', '\033[91m', '\033[1;91m']
LogType = ['INFO', 'WARN', 'FAIL', 'ERR!']

class MCSL2LogPrinter(object):
    def __init__(self, Msg, MsgLevel):
        self.Msg = Msg
        self.MsgLevel = MsgLevel # Can be 0 , 1 , 2 , 3
    
    def PrintLogToConsole(self):
        '''
        Info --> MsgLevel = 1
        Warning --> MsgLevel = 2
        Fail --> MsgLevel = 3
        UnexpectedFail --> MsgLevel = 4
        '''
        Time = datetime.now().strftime('%H:%M:%S')
        print(Time + "  [ " + LogColor[self.MsgLevel] + LogType[self.MsgLevel] + "\033[0m ]  " + self.Msg)

'''
示例

MCSL2LogPrinter(Msg="An \"INFO\" Log", MsgLevel=0).PrintLogToConsole()
MCSL2LogPrinter(Msg="A \"Warning\" Log", MsgLevel=1).PrintLogToConsole()
MCSL2LogPrinter(Msg="A \"Fail\" Log", MsgLevel=2).PrintLogToConsole()
MCSL2LogPrinter(Msg="An \"Error\" Log", MsgLevel=3).PrintLogToConsole()

'''
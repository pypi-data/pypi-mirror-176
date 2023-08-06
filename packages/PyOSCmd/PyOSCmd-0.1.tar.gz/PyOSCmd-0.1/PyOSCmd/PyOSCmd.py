class ParseCommand:
    def IsParseCmd(self, _CmdTable:dict, _ParseCmd):
        for CmdValue in _CmdTable.keys():
            # print(_ParseCmd.split("="))
            if CmdValue == _ParseCmd:
                return _CmdTable[CmdValue]
            elif len(_ParseCmd.split("=")) >= 2:
                return [_ParseCmd.split("=")[0]+"=", _ParseCmd.split("=")[-1]]
        return False

class PyOSCmd(ParseCommand):
    def __init__(
            self,
            _CmdTable:dict,
            _ParseCmdData:list,
            _PrintObj=False,
            _PrintStyle=False
    ):
        super(PyOSCmd, self).__init__()
        self.CommandTalbe = _CmdTable
        self.ParseCmdData = _ParseCmdData
        self.PrintObj = _PrintObj
        self.PrintStyle = _PrintStyle

    def Print(self, data):
        if self.PrintObj:
            if self.PrintStyle == False:
                self.PrintObj().Print(data)
            else:
                self.PrintObj().Print(data, self.PrintStyle)
        else:
            print(data)

    def start(self):
        for ParseCmdValue in self.ParseCmdData:
            ParseLog = self.IsParseCmd(self.CommandTalbe, ParseCmdValue)
            if ParseLog:
                try:
                    ParseLog()
                except TypeError:
                    if type(ParseLog) == list:
                        try:
                            self.CommandTalbe[ParseLog[0]](ParseLog[-1])
                        except TypeError:
                            self.Print(self.CommandTalbe[ParseLog[0]])
                    else:
                        self.Print(ParseLog)
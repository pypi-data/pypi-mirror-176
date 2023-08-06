import ctypes

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12
FOREGROUND_BLACK = 0x00 # black.
FOREGROUND_DARKBLUE = 0x01 # dark blue. 暗蓝色
FOREGROUND_DARKGREEN = 0x02 # dark green. 暗绿色
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue. 暗天蓝色
FOREGROUND_DARKRED = 0x04 # dark red. 暗红色
FOREGROUND_DARKPINK = 0x05 # dark pink. 暗粉红色
FOREGROUND_DARKYELLOW = 0x06 # dark yellow. 暗黄色
FOREGROUND_DARKWHITE = 0x07 # dark white. 暗白色
FOREGROUND_DARKGRAY = 0x08 # dark gray. 暗灰色
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_SKYBLUE = 0x0b # skyblue.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_PINK = 0x0d # pink.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_WHITE = 0x0f # white.
BACKGROUND_BLUE = 0x10 # dark blue.
BACKGROUND_GREEN = 0x20 # dark green.
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
BACKGROUND_DARKRED = 0x40 # dark red.
BACKGROUND_DARKPINK = 0x50 # dark pink.
BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
BACKGROUND_DARKWHITE = 0x70 # dark white.
BACKGROUND_DARKGRAY = 0x80 # dark gray.
BACKGROUND_BLUE = 0x90 # blue.
BACKGROUND_GREEN = 0xa0 # green.
BACKGROUND_SKYBLUE = 0xb0 # skyblue.
BACKGROUND_RED = 0xc0 # red.
BACKGROUND_PINK = 0xd0 # pink.
BACKGROUND_YELLOW = 0xe0 # yellow.
BACKGROUND_WHITE = 0xf0 # white.

class OutWindowFontColor:
    def __init__(self, _StdOutHandle: int = STD_OUTPUT_HANDLE):
        self.StdOutHandle = ctypes.windll.kernel32.GetStdHandle(_StdOutHandle)

    def SetCmdColor(self, color):
        return ctypes.windll.kernel32.SetConsoleTextAttribute(self.StdOutHandle, color)

    def ResetColor(self):
        return self.SetCmdColor(FOREGROUND_DARKWHITE | FOREGROUND_BLACK)

    def Print(self, data, color: int = FOREGROUND_WHITE):
        self.SetCmdColor(color)
        print(data)
        self.ResetColor()

    def PrintRed(self, data):
        self.SetCmdColor(FOREGROUND_RED)
        print(data)
        self.ResetColor()

    def PrintWhite(self, data):
        self.SetCmdColor(FOREGROUND_WHITE)
        print(data)
        self.ResetColor()

    def PrintBlack(self, data):
        self.SetCmdColor(FOREGROUND_BLACK)
        print(data)
        self.ResetColor()

    def PrintBlue(self, data):
        self.SetCmdColor(FOREGROUND_BLUE)
        print(data)
        self.ResetColor()

    def PrintYellow(self, data):
        self.SetCmdColor(FOREGROUND_YELLOW)
        print(data)
        self.ResetColor()

    def PrintPink(self, data):
        self.SetCmdColor(FOREGROUND_PINK)
        print(data)
        self.ResetColor()

    def PrintGreek(self, data):
        self.SetCmdColor(FOREGROUND_GREEN)
        print(data)
        self.ResetColor()

LINUX_HEADER = '\033[95m'
LINUX_OKBLUE = '\033[94m'
LINUX_OKGREEN = '\033[92m'
LINUX_WARNING = '\033[93m'
LINUX_FAIL = '\033[91m'
LINUX_ENDC = '\033[0m'
LINUX_BOLD = '\033[1m'
LINUX_UNDERLINE = '\033[4m'
LINUX_ERROR = "\033[31m"

class OutLinuxFontColor:
    def Print(self, data, config = LINUX_BOLD):
        if type(config) == list:
            print(f"\033[{config[0]};{config[1]};{config[-1]}m{data}\033[0m")
        else:
            print(f"{config}{data}\033[0m")

# if __name__ == '__main__':
#     Out = OutWindowFontColor()
#     Out.Print("Hello", FOREGROUND_BLUE)
#     Out.PrintRed("Red")
#     Out.PrintWhite("White")
#     Out.PrintBlack("Black")
#     Out.PrintBlue("Blue")
#     Out.PrintYellow("Yellow")
#     Out.PrintPink("Pink")
#     Out.PrintGreek("Greek")
#       LinuxOut = OutLinuxFontColor()
#       LinuxOut.Print("Linux Font", LINUX_ERROR)
# PyOSCmd
___

    PyOSCmd是一个用于开发终端命令行的第三方库，简单，易用。

___
- Color.py


<p>
STD_INPUT_HANDLE = -10 <br>
STD_OUTPUT_HANDLE= -11 <br>
STD_ERROR_HANDLE = -12 <br>
FOREGROUND_BLACK = 0x00 # black. <br>
FOREGROUND_DARKBLUE = 0x01 # dark blue. 暗蓝色 <br>
FOREGROUND_DARKGREEN = 0x02 # dark green. 暗绿色 <br>
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue. 暗天蓝色 <br>
FOREGROUND_DARKRED = 0x04 # dark red. 暗红色 <br>
FOREGROUND_DARKPINK = 0x05 # dark pink. 暗粉红色 <br>
FOREGROUND_DARKYELLOW = 0x06 # dark yellow. 暗黄色 <br>
FOREGROUND_DARKWHITE = 0x07 # dark white. 暗白色 <br>
FOREGROUND_DARKGRAY = 0x08 # dark gray. 暗灰色 <br>
FOREGROUND_BLUE = 0x09 # blue. <br>
FOREGROUND_GREEN = 0x0a # green. <br>
FOREGROUND_SKYBLUE = 0x0b # skyblue. <br>
FOREGROUND_RED = 0x0c # red. <br>
FOREGROUND_PINK = 0x0d # pink. <br>
FOREGROUND_YELLOW = 0x0e # yellow. <br>
FOREGROUND_WHITE = 0x0f # white. <br>
BACKGROUND_BLUE = 0x10 # dark blue. <br>
BACKGROUND_GREEN = 0x20 # dark green. <br>
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue. <br>
BACKGROUND_DARKRED = 0x40 # dark red. <br>
BACKGROUND_DARKPINK = 0x50 # dark pink. <br>
BACKGROUND_DARKYELLOW = 0x60 # dark yellow. <br>
BACKGROUND_DARKWHITE = 0x70 # dark white. <br>
BACKGROUND_DARKGRAY = 0x80 # dark gray. <br>
BACKGROUND_BLUE = 0x90 # blue. <br>
BACKGROUND_GREEN = 0xa0 # green. <br>
BACKGROUND_SKYBLUE = 0xb0 # skyblue. <br>
BACKGROUND_RED = 0xc0 # red. <br>
BACKGROUND_PINK = 0xd0 # pink. <br>
BACKGROUND_YELLOW = 0xe0 # yellow. <br>
BACKGROUND_WHITE = 0xf0 # white. <br>
</p>

| 显示方式 | 效果     | 前景色 | 背景色 | 颜色描述 |
|------|--------|-----|-----|------|
| 0    | 终端默认设置 | 30  | 40  | 黑色   |
| 1    | 高亮显示   | 31  | 41  | 红色   |
| 4    | 使用下划线  | 34  | 42  | 绿色   |
| 5    | 闪烁     | 33  | 43  | 黄色   |
| 7    | 反白显示   | 34  | 44  | 蓝色   |
| 8    | 不可见    | 35  | 45  | 紫红色  |
| 22   | 非高亮显示  | 36  | 46  | 青蓝色  |
| 24   | 去下划线   | 37  | 47  | 白色   |
| 25   | 去闪烁    |     |     |      |
| 27   | 非反白显示  |     |     |      |
| 28   | 可见     |     |     |      |

___

```python
import PyOSCmd

# OutWindowsFontColor
PyOSCmd.OutWindowFontColor().Print(data="Hello PySysCmd", color=PyOSCmd.LINUX_BOLD)
# Out Hello PySysCmd

# OurLinuxFontColor
PyOSCmd.OutLinuxFontColor().Print(data="Hello Linux!", config=[1, 31, 47])
PyOSCmd.OutLinuxFontColor().Print(data="Hello Linux!", config=PyOSCmd.LINUX_WARNING)

# Out Hello Linux!

```

- 使用事例

```python
import PyOSCmd
import sys

def text():
    print("Test!")

PyOSCmd.PyOSCmd(
    {
        "-h":"--help",
        "-t":text
    },
    sys.argv[0:],
    PyOSCmd.OutWindowFontColor,
    PyOSCmd.FOREGROUND_YELLOW
)
```

QQ:2097632843
QQ群：706128290
mail：mc2005wj@163.com

[Kuko](https://www.kuko.icu/)
# 监听键盘

import pythoncom
import PyHook3
import win32clipboard
import os, sys

print("键盘按下组合键Ctrl+M后，剪贴板内的内容就可以保存到本地文件")

path = os.getcwd()
file_save = path + os.path.sep + "keyboard.txt"


def OnKeyboardEvent(event):
    # 检测击键是否常规按键（非组合键等）
    if event.Ascii > 32 and event.Ascii < 127:
        print(event.Key)
    else:
        # 如果发现键盘按下组合键<Ctrl+M>事件，就把粘贴板内容保存到本地文件中
        if event.Key == "M":
            win32clipboard.OpenClipboard()
            paste_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print()
            print("剪贴板内容已经保存到文件 " + file_save)
            print("-" * 32)
            print(paste_value)
            print("-" * 32)
            print()
            with open(file_save, "a") as f:
                f.writelines("\n" + paste_value + "\n")
    # 循环监听下一个击键事件
    return True


# 创建并注册hook管理器
kl = PyHook3.HookManager()  #
kl.KeyDown = OnKeyboardEvent

# 注册hook并执行
kl.HookKeyboard()
pythoncom.PumpMessages()
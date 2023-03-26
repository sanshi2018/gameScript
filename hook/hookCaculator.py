import ctypes
import ctypes.wintypes
import win32gui
import win32process

# 定义Windows API函数
user32 = ctypes.windll.user32
callback_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))


WH_KEYBOARD_LL = 13
# 定义KBDLLHOOKSTRUCT结构体
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", ctypes.wintypes.DWORD),
        ("scanCode", ctypes.wintypes.DWORD),
        ("flags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]

# 获取计算器窗口句柄
calculator_hwnd = win32gui.FindWindow(None, "计算器")

# 获取计算器进程ID和句柄
_, process_id = win32process.GetWindowThreadProcessId(calculator_hwnd)
calculator_handle = ctypes.windll.kernel32.OpenProcess(
    ctypes.wintypes.DWORD(0x1F0FFF), False, process_id
)

# 定义钩子回调函数
def hook_callback(nCode, wParam, lParam):
    if nCode == 0:
        # 提取键盘事件信息
        event = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        if wParam == user32.WM_KEYDOWN:
            # 输出按下的键的名称和虚拟键码
            print("Key down: ", event.vkCode)
        elif wParam == user32.WM_KEYUP:
            # 输出释放的键的名称和虚拟键码
            print("Key up: ", event.vkCode)
    # 调用下一个钩子
    return user32.CallNextHookEx(hook_id, nCode, wParam, lParam)

# 设置钩子
hook_callback = callback_type(hook_callback)


hook_id = user32.SetWindowsHookExA(WH_KEYBOARD_LL, ctypes.cast(hook_callback, ctypes.c_void_p), calculator_handle, 0)

# 开始消息循环
msg = ctypes.wintypes.MSG()
while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
    user32.TranslateMessage(ctypes.byref(msg))
    user32.DispatchMessageW(ctypes.byref(msg))

# 卸载钩子
user32.UnhookWindowsHookEx(hook_id)

# 关闭计算器进程句柄
ctypes.windll.kernel32.CloseHandle(calculator_handle)

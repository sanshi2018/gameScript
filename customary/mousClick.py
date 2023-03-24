import pywinauto
import win32gui
import win32con
import win32api
from PIL import ImageGrab, Image
import numpy as np
import cv2
# import cv2
# 运行一个计算器程序
calc = pywinauto.application.Application().start('calc.exe')

# 进入计算器窗口
# calc_dialog = calc['Calculator']
# calc_handle = app['计算器'].handle
# 查找计算器窗口
calc_handle = win32gui.FindWindow(None, '计算器')
# 进入计算器窗口
# calc_dialog = calc['计算器']
if calc_handle == 0:
    print('没有找到计算器窗口')
else:
    # 通过calc_handle获取指定窗口image
    calc_dialog = pywinauto.controls.hwndwrapper.HwndWrapper(calc_handle)
    # 截图计算器窗口并转换为 Image 对象
    # calc_image = Image.frombytes('RGB', calc_dialog.capture_as_image().size, calc_dialog.capture_as_image().tobytes())

    # 打开 equal.png 并转换为像素数组
    equal_image = Image.open('./img/equal.png')
    equal_data = np.array(equal_image.convert('RGB'))

    Main_image = Image.open('./img/Main.png')
    Main_data = np.array(equal_image.convert('RGB'))

    # 将计算器截图转换为 numpy 数组
    # calc_data = np.array(calc_image)

    # 在计算器截图中搜索 equal.png 图片的位置
    res = cv2.matchTemplate(Main_data, equal_data, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        x, y = loc[1][0] + equal_image.width // 2, loc[0][0] + equal_image.height // 2
        # 在这个handle内发送鼠标点击事件
        # win32gui.SendMessage(calc_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
        # 计算器的屏幕坐标
        rect = win32gui.GetWindowRect(calc_handle)
        win32api.SetCursorPos((rect[2] - 10, rect[1] + 10))
        # 计算器的客户区坐标
        # client_rect = win32gui.GetClientRect(calc_handle)
        #
        # # 根据x , y 计算出相对于客户区的坐标
        # x = x - rect[0]
        # y = y - rect[1]
        # # 根据客户区坐标计算出相对于屏幕的坐标
        # x = x + (rect[2] - rect[0] - client_rect[2]) // 2
        # y = y + (rect[3] - rect[1] - client_rect[3]) // 2
        # # 鼠标点击 x y
        # win32api.SetCursorPos((x, y))
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        # lParam = win32api.MAKELONG(x, y)
        # win32gui.SendMessage(calc_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        # win32gui.SendMessage(calc_handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

        # 在calc_handle窗口内相对坐标发送后台鼠标点击事件


        #
        # 模拟输入数字“1”
        # win32api.keybd_event(win32con.VK_NUMPAD1, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        # win32api.keybd_event(win32con.VK_NUMPAD1, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
    else:
        print('没有找到 equal.png 图片')

    # 获取这个handle的右上角位置
    # rect = win32gui.GetWindowRect(calc_handle)
    # 发送后台鼠标命令点击右上角
    # win32api.SetCursorPos((rect[2] - 10, rect[1] + 10))
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, rect[2] - 10, rect[1] + 10, 0, 0)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, rect[2] - 10, rect[1] + 10, 0, 0)




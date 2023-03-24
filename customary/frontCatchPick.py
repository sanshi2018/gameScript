import win32gui
import win32ui
import win32api
import win32con
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
from PIL import ImageGrab, Image
import numpy as np

"""
    截图  只能游戏前台时候才能截取
"""
def photo_capture(hwnd: HWND):

    # hwnd = win32gui.FindWindow(None, handle)  # 获取窗口的句柄
    # hwnd = 265204  # 或设置窗口句柄

    # 如果使用高 DPI 显示器（或 > 100% 缩放尺寸），添加下面一行，否则注释掉
    windll.user32.SetProcessDPIAware()

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # 根据您是想要整个窗口还是只需要 client area 来更改下面的行。
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    # left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)  # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 根据窗口的DC获取mfcDC
    saveDC = mfcDC.CreateCompatibleDC()  # mfcDC创建可兼容的DC

    saveBitMap = win32ui.CreateBitmap()  # 创建bitmap准备保存图片
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)  # 为bitmap开辟空间

    saveDC.SelectObject(saveBitMap)  # 高度saveDC，将截图保存到saveBitmap中


    # 选择合适的 window number，如0，1，2，3，直到截图从黑色变为正常画面
    # 不同的程序运行在不同的桌面，这里的窗口指的是显示器的窗口而不是程序的窗口。
    # 通常，这个数字会随着是否使用外接显示器来改变。
    # 你可以从零开始依次尝试，大多数人只需要尝试 0，1，2，3，4。我的是3，因为我使用笔记本外接显示器。
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

    # 截图是BGRA排列，因此总元素个数需要乘以4

    bmpstr = saveBitMap.GetBitmapBits(True)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        # return im  # 返回图片
        return np.frombuffer(bmpstr, dtype=np.uint8).reshape(h, w, 4)
    else:
        return None




if __name__ == "__main__":
    import cv2
    # handle = windll.user32.FindWindowW(None, "微信")
    # 获取桌面上全部窗口的句柄
    # win32gui.
    handle = win32gui.FindWindow(None, '计算器')
    image = photo_capture(handle)

    # cv2.imshow("Capture Test", image)
    # cv2.waitKey()

    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # 读取图片，并保留Alpha通道
    template = cv2.imread('./img/number1.png', cv2.IMREAD_UNCHANGED)
    # 取出Alpha通道 透明通道在3，RGB在0，1，2 透明通道为0的地方不参与匹配, 255为完全参与匹配
    alpha = template[:,:,2]
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
    # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
    result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED, mask=alpha)
    # 获取结果中最大值和最小值以及他们的坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = top_left[0] + w, top_left[1] + h
    # 在窗口截图中匹配位置画红色方框
    cv2.rectangle(image, top_left, bottom_right, (0,0,255), 2)

    # 获取handle的绝对位置
    rect = win32gui.GetWindowRect(handle)
    win32api.SetCursorPos((rect[0], rect[1]))
    # 根据相对位置top_left 计算出绝对位置
    top_left1 = rect[0] + int((top_left[0] + w)/2), int((top_left[1] + h)/2) + rect[1]


    # 鼠标移动到这个位置并且点击
    # x++ 👉 , y++ 👇
    win32api.SetCursorPos((top_left1[0], top_left1[1]))
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    # cv2.imshow('Match Template', image)
    # cv2.waitKey()
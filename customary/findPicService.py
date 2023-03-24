from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np
import time


if __name__ == "__main__":
    import cv2
    # 截图时要保证游戏窗口的客户区大小是1334×750
    image = capture(handle)        
    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # 读取图片，并保留Alpha通道
    template = cv2.imread('transparent_activity_btn.png', cv2.IMREAD_UNCHANGED)
    # 取出Alpha通道
    alpha = template[:,:,3]
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
    cv2.imshow('Match Template', image)
    cv2.waitKey()
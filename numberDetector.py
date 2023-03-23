from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np
import time

# 窗口操作请看https://zhuanlan.zhihu.com/p/363599118
from freezeWindow import resize_client
# 截图操作请看https://zhuanlan.zhihu.com/p/361569101
from gameScream import capture

if __name__ == "__main__":
    import cv2
    handle = windll.user32.FindWindowW(None, "寻仙 - 修仙l - 元婴l : 版本号3.5.66.1")
    # resize_client(handle, 3840, 2160)
    # 加载数字模板
    temps = []
    for i in range(10):
        temps.append(cv2.imread(f'./img/npc.png', cv2.IMREAD_GRAYSCALE))

    # 按下任意键退出识别
    while cv2.waitKey(delay=100) == -1:
        im = capture(handle)
        # im = im[157:655, 355:1148]     
        # 提取指定画面中的数字轮廓   
        gray = cv2.cvtColor(im, cv2.COLOR_BGRA2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
        contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        result = []
        for cnt in contours:
            [x,y,w,h] = cv2.boundingRect(cnt)
            # 按照高度筛选
            if 50 > h > 40:
                result.append([x,y,w,h])

        result.sort(key=lambda x:x[0])

        for x, y, w, h in result:
            # 在画面中标记识别的结果                
            cv2.rectangle(im, (x,y),(x+w,y+h),(0,0,255),1)
            digit = cv2.resize(thresh[y:y+h, x:x+w], (14, 20))
            res = []
            for i, t in enumerate(temps):
                score = cv2.matchTemplate(digit, t, cv2.TM_CCORR_NORMED)
                res.append((i, score[0]))
            # res.sort(key=lambda x:x[1])
            cv2.putText(im, str(f"{res[-1][0]}"), (x, y+35), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.imshow('Digits OCR Test', im)
# -*- coding: utf-8 -*-
# https://www.cnblogs.com/lqerio/p/12106771.html
"""
Created on Wed Dec 25 11:33:41 2019
@author: erio
"""
import PyHook3
# USB 接口的键盘鼠标
import pythoncom
import PyHook3 as pyHook
import win32api
import time

# path = 'D://records.log'


def onMouseEvent(event):
    # with open(path, 'a+') as f:
    #     f.write("-----Mouse Event Start-----\n")
    #     # 监听鼠标事件
    #     print ("MessageName:", event.MessageName)
    #     print ("WindowName:", event.WindowName)
    #     print ("Position:", event.Position)
    #     print ("Wheel:", event.Wheel)
    #     print ("---")
    #     # 返回 True 以便将事件传给其它处理程序
    #     # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    #     t = time.localtime()
    #     t = time.asctime(t)
    #     result = "Time : " + t + "\n" + "MessageName: "+ str(event.MessageName)+'\n'+"WindowName: " + str(event.WindowName) + \
    #             "\n" +"Position: "+str(event.Position)+'\n'+"Wheel: " +str(event.Wheel)+'\n'
    #     f.write(result)
    #     f.write("-----Mouse Event End-----\n\n\n")
    # f.close()
    return True


def onKeyboardEvent(event):
    # 监听键盘事件
    print("MessageName:", event.MessageName)
    print("Message:", event.Message)
    print("Window", event.Window)
    print("WindowName:", event.WindowName)
    print("Ascii:", event.Ascii, chr(event.Ascii))
    print("Key:", event.Key)
    print("ScanCode:", event.ScanCode)
    print("Alt", event.Alt)
    print("---")
    if event.Key == 'Q':  # 按下F12后终止adsw
        win32api.PostQuitMessage()
    return True


def start():
    # 创建一个“钩子”管理对象aaavv  q
    hm = pyHook.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()
    # 监听所有鼠标事件
    # hm.MouseAll = onMouseEvent
    # 设置鼠标“钩子”
    # hm.HookMouse()
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()

import tkinter as tk
from pynput import mouse
import win32gui

class Window:
    def __init__(self):
        self.root = tk.Tk()                                 # 创建一个Tkinter的根窗口
        self.root.geometry("200x200")                       # 设置窗口大小
        self.start_button = tk.Button(self.root, text="开始选定", command=self.start_listening)    # 创建一个按钮，点击后会调用start_listening函数
        self.start_button.pack()                            # 添加按钮到窗口中
        self.listbox = tk.Listbox(self.root)                 # 创建一个Listbox，用于显示窗口标题和句柄
        self.listbox.pack()                                 # 添加Listbox到窗口中
        self.root.mainloop()                                # 开始主循环，显示窗口
        self.listener
        
    def start_listening(self):
        self.listener = mouse.Listener(on_click=self.get_window_by_mouse)   # 创建一个鼠标监听器，点击时调用get_window_by_mouse函数
        self.listener.start()                               # 开始监听
    def get_window_by_mouse(self, x, y, button, pressed):  # 定义鼠标点击时调用的函数
        if button == mouse.Button.left and pressed :        # 判断是否是左键点击
            handle = win32gui.WindowFromPoint((x, y))      # 获取鼠标点击的窗口的句柄
            title = win32gui.GetWindowText(handle)         # 获取窗口标题
            self.listbox.insert(tk.END, title)              # 将窗口标题添加到Listbox中
            self.listbox.insert(tk.END, handle)             # 将窗口句柄添加到Listbox中
            self.listener.stop()                            # 停止监听
            
if __name__ == "__main__":
    Window()
from PyQt5.QtWidgets import QApplication
import win32gui
import sys

hwnd = win32gui.FindWindow(None, '桌面')
# hwnd = 329824
app = QApplication(sys.argv)
screen = QApplication.primaryScreen()
img = screen.grabWindow(hwnd).toImage()
img.save("screenshot.jpg")
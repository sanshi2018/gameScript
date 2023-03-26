import os
import win32api
import win32con
import win32process

# DLL文件路径
dll_path = "./dllmain.dll"

# 计算器进程名称
process_name = "Calculator.exe"

# 获取计算器进程ID
calc_pid = win32api.GetCurrentProcessId();
# calc_pid = pids[0].pid

# 在计算器进程中打开一个线程
kernel32 = win32api.GetModuleHandle("kernel32.dll")
thread_id, _ = win32process.Getthread
remote_thread = kernel32.CreateRemoteThreadEx(win32process.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, calc_pid),
                                               None,
                                               0,
                                               kernel32.LoadLibraryW,
                                               os.path.abspath(dll_path),
                                               0,
                                               None)

# 等待远

from job import Job

job = Job()
from ctypes import CDLL
from sys import stdout
import os
#load the shared object file
# cprint = CDLL('./so/cprint.so')
# cprint.test()

# import win32gui
# import win32console
# hwnd = win32gui.FindWindow(None, None)
# print(hwnd)
# win32console.CreateConsoleScreenBuffer()
# cursor = win32gui.GetCursor()
# print(cursor)
# win32gui.SetCursor()

import win32console, win32con, time
myConsole = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1) # create screen buffer
myConsole.SetConsoleActiveScreenBuffer() # set this buffer to be active
os.system('cls')
print(111111111111111111)
for i in range(50):
    print(111111111111111111)
    myConsole.WriteConsoleOutputCharacter(Characters="Hello WorldHello World!%s\0" % i, WriteCoord=win32console.PyCOORDType(0,0)) # Print at coordinates
    time.sleep(0.5)

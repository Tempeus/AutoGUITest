# directkeys.py
# http://stackoverflow.com/questions/13564851/generate-keyboard-events
# msdn.microsoft.com/en-us/library/dd375731

import ctypes
from ctypes import wintypes
import time
import os

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

# https://msdn.microsoft.com/ru-RU/library/windows/desktop/ms646273%28v=vs.85%29.aspx
MOUSEEVENTF_MOVE = 0x0001	#Movement occurred
MOUSEEVENTF_LEFTDOWN = 0x0002	#The left button was pressed.
MOUSEEVENTF_LEFTUP = 0x0004 #The left button was released
MOUSEEVENTF_ABSOLUTE = 0x8000

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# List of all codes for keys:
# # msdn.microsoft.com/en-us/library/dd375731
UP = 0x26
DOWN = 0x28
A = 0x41

# C struct definitions

PUL = ctypes.POINTER(ctypes.c_ulong)


EVENT_LIST = []

class RapEvent:
    def __init__(self, msgid, paramL, paramH, time):
        self.msgid = msgid
        self.paramL = paramL
        self.paramH = paramH
        self.time = time

class MouseInput(ctypes.Structure):
    _fields_ = [("dx",          ctypes.c_long),
                ("dy",          ctypes.c_long),
                ("mouseData",   ctypes.c_ulong),
                ("dwFlags",     ctypes.c_ulong),
                ("time",        ctypes.c_long),
                ("dwExtraInfo", PUL)]

class KeyBdInput(ctypes.Structure):
    _fields_ = (("wVk",         ctypes.c_ushort),
                ("wScan",       ctypes.c_ushort),
                ("dwFlags",     ctypes.c_ulong),
                ("time",        ctypes.c_ulong),
                ("dwExtraInfo", PUL))

class HardwareInput(ctypes.Structure):
    _fields_ = (("uMsg",    ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort))

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]


LPINPUT = ctypes.POINTER(Input)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def MoveMouse(x,y):
    x = 1 + int(x * 65536./1920.)
    y = 1 + int(y * 65536./1080.)

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, (MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE), 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

def PressMouse():
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseMouse():
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def TranslateRapFile(rapfile):
    f = open("rapfiles/" + rapfile, "r")
    lines = f.readlines()
    #Split the csv
    for line in lines:
        line_split = line.split(",")

        msgid = ""
        paramL = 0
        paramH = 0
        time = 0

        for var in line_split:
            temp = var.split('=')
            if(temp[0] == "msgid"):
                msgid = temp[1]
            elif(temp[0] == "paramL"):
                paramL = int(temp[1])
            elif(temp[0] == "paramH"):
                paramH = int(temp[1])
            elif(temp[0] == "time"):
                time = int(temp[1])
    
        if msgid:
            #make sure all variables are assigned to something, else error
            EVENT_LIST.append(RapEvent(msgid, paramL, paramH, time))


if __name__ == "__main__":
    TranslateRapFile("test.txt")
    systemtime = EVENT_LIST[0].time
    for event in EVENT_LIST:
        wait_time = (event.time - systemtime) / 1000
        if "WM_LBUTTONDOWN" in event.msgid:
            print("Wait time: " + str(wait_time))
            time.sleep(wait_time)
            MoveMouse(event.paramL, event.paramH)
            PressMouse()
            systemtime = event.time

        elif "WM_LBUTTONUP" in event.msgid:
            print("Wait time: " + str(wait_time))
            time.sleep(wait_time)
            MoveMouse(event.paramL, event.paramH)
            ReleaseMouse()
            systemtime = event.time

        elif "WM_KEYDOWN" in event.msgid:
            print("Wait time: " + str(wait_time))
            time.sleep(wait_time)
            PressKey(event.paramL)
            systemtime = event.time

        elif "WM_KEYUP" in event.msgid:
            print("Wait time: " + str(wait_time))
            time.sleep(wait_time)
            ReleaseKey(event.paramL)
            systemtime = event.time

    print("success")

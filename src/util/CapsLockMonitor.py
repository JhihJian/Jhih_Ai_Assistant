import asyncio
import logging
import threading
import time
from datetime import datetime

import keyboard

from function.FunctionController import FunctionController

import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB = 0x09
VK_MENU = 0x12
VK_CAPITAL = 0x14
# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))


LPINPUT = ctypes.POINTER(INPUT)


def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT,  # nInputs
                             LPINPUT,  # pInputs
                             ctypes.c_int)  # cbSize


# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def AltTab():
    """Press Alt+Tab and hold Alt key for 2 seconds
    in order to see the overlay.
    """
    PressKey(VK_MENU)  # Alt
    PressKey(VK_TAB)  # Tab
    ReleaseKey(VK_TAB)  # Tab~
    time.sleep(2)
    ReleaseKey(VK_MENU)  # Alt~


def pressCapsLock():
    PressKey(VK_CAPITAL)


def releaseCapsLock():
    ReleaseKey(VK_CAPITAL)


def press_and_release_CapsLock():
    PressKey(VK_CAPITAL)
    ReleaseKey(VK_CAPITAL)


# 按下大写锁定键不放时,触发hook,begin_event_hook,结束后触发 finish_event_hook
class CapsLockMonitor:
    wait_time = 10 * 1000  # 设置监听缓存时间，长按300毫秒后开始
    __on_running = False  # 是否已经开始运行
    is_trigger_down = False  # 是否之前按下了CapsLock键
    trigger_down_time = datetime.now()  # 刚开始按下的时间

    def __init__(self, begin_event_hook=None, finish_event_hook=None):
        self.__beginEventHook = begin_event_hook
        self.__finishEventHook = finish_event_hook

    def run(self):
        keyboard.hook_key('caps lock', self.__trick_hook_key)

    def __trick_hook_key(self, event):

        if event.event_type == "down":
            # 已经在运行就不触发
            if self.__on_running:
                return

            # 只记录第一个down的时间
            if not self.is_trigger_down:
                self.trigger_down_time = datetime.now()
                self.is_trigger_down = True
                return

            # 一定是第二个down才考虑触发事件，即使是第二个down,也要看和第一个down相差的时间是否足够,
            if self.is_trigger_down:
                diff = (datetime.now() - self.trigger_down_time).microseconds
                if diff < self.wait_time:
                    print("时间没到不运行 {}".format(diff))
                    return
            try:
                self.__on_running = True
                print("Begin CapsLock Event")
                if self.__beginEventHook:
                    try:
                        self.__beginEventHook()
                    except Exception as e:
                        print("error from begin_event_hook {}: {}".format(self.__beginEventHook, e))

            except Exception as e:
                print('process 启动失败 error :{}'.format(e))

        elif event.event_type == "up":
            self.is_trigger_down = False
            if not self.__on_running:
                return
            self.__on_running = False

            if self.__finishEventHook:
                print("Finish CapsLock Event")
                try:
                    self.__finishEventHook()
                except Exception as e:
                    print("error from finishEventHook {}: {}".format(self.__finishEventHook, e))
            # 取消大写
            # print("取消大写")
            keyboard.press_and_release('caps lock')

        else:
            print(event.event_type)

    def stop(self):
        keyboard.unhook(self.__trick_hook_key)

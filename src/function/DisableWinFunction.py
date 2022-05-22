import logging
import multiprocessing
import threading
import time

from pynput import keyboard
from datetime import datetime
import keyboard as kb

from function.BaseFunction import *

# 当检测到游戏进程开始时，自动禁用按键
from function.QueryProcess import QueryProcess


class DisableWinFunction(BaseFunction):
    function_name = "DisableWinFunction"
    wait_time = 150 * 1000  # 在1000ms 内连按两次ctrl 屏蔽之

    def __init__(self):
        self.m_process = None
        self.check_process = None
        self.on_playing_lol = False
        self.last_time = datetime.now()
        self.pre_event = 257
        self.logger = logging.getLogger("MianWindows")

    def register(self):
        pass

    def start(self):
        self.function_status = FunctionStatus.STARTING
        self.m_process = multiprocessing.Process(target=self.__run__)
        self.check_process = multiprocessing.Process(target=self.__checkGamingStatus__)
        self.m_process.start()
        self.check_process.start()
        self.function_status = FunctionStatus.RUNNING
        logging.getLogger("MainWindows")

    def quit(self):
        if self.m_process.is_alive():
            self.m_process.terminate()
        if self.check_process.is_alive():
            self.check_process.terminate()
        self.function_status = FunctionStatus.STOP
        pass

    def __checkGamingStatus__(self):
        q = QueryProcess()
        while True:
            is_playing_lol = q.IsPlayingLol()
            if self.on_playing_lol != is_playing_lol:
                if is_playing_lol:
                    self.logger.info("禁用Win辅助服务：检测到LOL窗口为激活状态")
                else:
                    self.logger.info("禁用Win辅助服务：检测到LOL窗口非激活状态")
            self.on_playing_lol = is_playing_lol
            time.sleep(10)

    def __run__(self):
        # Collect events until released
        with keyboard.Listener(
                win32_event_filter=self.__win32_event_filter__) as self.listener:
            self.listener.join()

    def __win32_event_filter__(self, msg, data):
        if not self.on_playing_lol:
            return
        # win key ,disable win
        if data.vkCode == 0x5B:
            # Suppress x
            self.listener.suppress_event()
        # msg 256 按下，msg 257 抬起
        # 1秒内连按两下left crtl 屏蔽第二下,257指按下
        if data.vkCode == 0xa2:
            print(msg)
            if msg == 256 and self.pre_event == 257:
                diff = (datetime.now() - self.last_time).microseconds
                print(diff)
                if diff < self.wait_time:
                    print("suppress_event")
                    self.pre_event = msg
                    self.listener.suppress_event()
            if msg == 257:
                self.last_time = datetime.now()
                self.pre_event = msg


def test():
    last_time = datetime.now()
    print(last_time)
    time.sleep(1)
    now = datetime.now()
    print(now)
    diff = (now - last_time).microseconds
    print(diff)


if __name__ == '__main__':
    d = DisableWinFunction()
    d.start()
    kb.wait()

import asyncio
import logging
import threading
import time

from pynput import keyboard
from datetime import datetime

from function.BaseFunction import *

# 当检测到游戏进程开始时，自动禁用按键
# 失败 在开始lol游戏之后 ,按键过滤无效，功能被lol屏蔽了
from util.QueryProcess import QueryProcess


# 内部工作，同时需要一个线程和一个异步任务
class DisableWinFunction(BaseFunction):
    function_name = "DisableWinFunction"
    wait_time = 150 * 1000  # 在1000ms 内连按两次ctrl 屏蔽之

    def __init__(self, function_controller):
        super().__init__(function_controller)
        # self.m_process = None
        self.listener = None
        self.async_task = None
        self.on_playing_lol = False
        self.last_time = datetime.now()
        self.pre_event = 257

    def register(self):
        pass

    def start(self):
        self.function_status = FunctionStatus.STARTING
        self.logger.info("禁用Win辅助服务：启动中...")
        # self.m_process = multiprocessing.Process(target=self.__run__)
        # self.m_process = threading.Thread(target=self.__run__)
        self.listener = keyboard.Listener(
            win32_event_filter=self.__win32_event_filter__)
        self.listener.start()
        # self.task = self.loop.create_task(self.__checkGamingStatus__())
        self.async_task = self.function_controller.append_async_task(self.__checkGamingStatus__)
        self.function_status = FunctionStatus.RUNNING

    def quit(self):
        try:
            if self.listener:
                self.listener.stop()
            self.function_controller.stop_task(self.__checkGamingStatus__)
        except Exception as e:
            self.logger.error("quit disable win function failed:{}".format(e))
        self.function_status = FunctionStatus.STOP

    async def __checkGamingStatus__(self):
        q = QueryProcess()
        self.logger.info("禁用Win辅助服务：启动完成")
        while True:
            is_playing_lol = q.IsPlayingLol()
            # 检查到状态变换才显示
            if self.on_playing_lol != is_playing_lol:
                self.logger.info("禁用Win辅助服务：检测到LOL窗口为激活状态" if is_playing_lol else "禁用Win辅助服务：检测到LOL窗口非激活状态")
            self.on_playing_lol = is_playing_lol
            # time.sleep(10)
            await asyncio.sleep(10)

    # def __run__(self):
    # Collect events until released

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
            if msg == 256 and self.pre_event == 257:
                diff = (datetime.now() - self.last_time).microseconds
                if diff < self.wait_time:
                    self.pre_event = msg
                    self.listener.suppress_event()
            if msg == 257:
                self.last_time = datetime.now()
                self.pre_event = msg


if __name__ == '__main__':
    df = DisableWinFunction(None)
    df.on_playing_lol = True
    with keyboard.Listener(
            win32_event_filter=df.__win32_event_filter__) as listener:
        df.listener = listener
        listener.join()
    print("main finish")

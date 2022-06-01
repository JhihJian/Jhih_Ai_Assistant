import time
import unittest

import keyboard

from util import LoggerConfig
from util.CapsLockMonitor import *
from util.RecoderVoice import *
import win32api, win32con


class Test_CapsLockMonitor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LoggerConfig.logger_config(None)

    def test_normal(self):
        # 如果状态是on复位
        caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
        if caps_status == 1:
            press_and_release_CapsLock()

        begin_result = []
        finish_result = []
        # monitor = CapsLockMonitor(begin_event_hook=lambda: print("begin event hook"),
        #                           finish_event_hook=lambda: finish_result.append(True))
        monitor = CapsLockMonitor(begin_event_hook=lambda: begin_result.append(True),
                                  finish_event_hook=lambda: finish_result.append(True))
        th = threading.Thread(target=monitor.run)
        th.start()
        # 按下时间太短，不进行hook
        time.sleep(1)
        print("测试超时不触发")
        pressCapsLock()
        pressCapsLock()
        self.assertEqual(0, len(begin_result))
        self.assertEqual(0, len(finish_result))
        releaseCapsLock()
        # assert CapsLock is ON
        caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
        self.assertEqual(1, caps_status)
        press_and_release_CapsLock()
        # assert CapsLock is OFF
        caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
        self.assertEqual(0, caps_status)
        print("连测两次 第一次")
        pressCapsLock()
        time.sleep(0.1)
        pressCapsLock()
        self.assertEqual(1, len(begin_result))
        self.assertEqual(0, len(finish_result))
        self.assertEqual(True, begin_result[0])
        releaseCapsLock()
        # time.sleep(0.1)
        self.assertEqual(1, len(finish_result))
        self.assertEqual(True, finish_result[0])
        time.sleep(1)

        # assert CapsLock is OFF
        caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
        self.assertEqual(0, caps_status)
        # 连测两次
        print("连测两次 第二次")
        pressCapsLock()
        time.sleep(0.1)
        pressCapsLock()

        self.assertEqual(2, len(begin_result))
        self.assertEqual(1, len(finish_result))
        self.assertEqual(True, begin_result[1])
        releaseCapsLock()
        # time.sleep(0.1)
        self.assertEqual(2, len(finish_result))
        self.assertEqual(True, finish_result[1])
        # assert CapsLock is OFF
        time.sleep(1)

        caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
        print(caps_status)
        self.assertEqual(0, caps_status)
        # 测试monitor 已停止
        print("测试已停止不触发")
        begin_result = []
        finish_result = []

        monitor.stop()
        print("monitor stop")
        #
        # time.sleep(1)
        pressCapsLock()
        time.sleep(0.1)
        pressCapsLock()
        time.sleep(0.1)
        self.assertEqual(0, len(begin_result))
        self.assertEqual(0, len(finish_result))
        releaseCapsLock()
        self.assertEqual(0, len(finish_result))
        press_and_release_CapsLock()

    def test_function_controller_stop(self):
        # 如果状态是on复位
        caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
        if caps_status == 1:
            press_and_release_CapsLock()

        function_controller = FunctionController(None)
        function_controller.start()
        begin_result = []
        finish_result = []
        # monitor = CapsLockMonitor(begin_event_hook=lambda: print("begin event hook"),
        #                           finish_event_hook=lambda: finish_result.append(True))
        monitor = CapsLockMonitor(begin_event_hook=lambda: begin_result.append(True),
                                  finish_event_hook=lambda: finish_result.append(True))
        function_controller.append_sync_task(monitor.run)
        # 按下时间太短，不进行hook
        time.sleep(1)
        print("测试超时不触发")
        pressCapsLock()
        pressCapsLock()
        self.assertEqual(0, len(begin_result))
        self.assertEqual(0, len(finish_result))
        releaseCapsLock()
        # assert CapsLock is ON
        caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
        self.assertEqual(1, caps_status)
        press_and_release_CapsLock()
        # assert CapsLock is OFF
        caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
        self.assertEqual(0, caps_status)
        print("连测两次 第一次")
        pressCapsLock()
        time.sleep(0.1)
        pressCapsLock()
        self.assertEqual(1, len(begin_result))
        self.assertEqual(0, len(finish_result))
        self.assertEqual(True, begin_result[0])
        releaseCapsLock()
        # time.sleep(0.1)
        self.assertEqual(1, len(finish_result))
        self.assertEqual(True, finish_result[0])
        time.sleep(1)

        # assert CapsLock is OFF
        caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
        self.assertEqual(0, caps_status)
        # 连测两次
        print("连测两次 第二次")
        pressCapsLock()
        time.sleep(0.1)
        pressCapsLock()

        self.assertEqual(2, len(begin_result))
        self.assertEqual(1, len(finish_result))
        self.assertEqual(True, begin_result[1])
        releaseCapsLock()
        # time.sleep(0.1)
        self.assertEqual(2, len(finish_result))
        self.assertEqual(True, finish_result[1])
        # assert CapsLock is OFF
        time.sleep(1)

        caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
        print(caps_status)
        self.assertEqual(0, caps_status)
        # 测试monitor 已停止
        print("测试已停止不触发")
        begin_result = []
        finish_result = []

        monitor.stop()
        function_controller.stop()
        print("monitor stop")
        #
        # time.sleep(1)
        pressCapsLock()
        time.sleep(0.1)
        pressCapsLock()
        time.sleep(0.1)
        self.assertEqual(0, len(begin_result))
        self.assertEqual(0, len(finish_result))
        releaseCapsLock()
        self.assertEqual(0, len(finish_result))
        press_and_release_CapsLock()

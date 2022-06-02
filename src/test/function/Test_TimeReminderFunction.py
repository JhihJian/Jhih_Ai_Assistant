import time
import unittest

from function.FunctionController import FunctionController
from function.TimeReminderFunction import TimeReminderFunction, hourToSecond, minuteToSecond, chineseToTime
from util import LoggerConfig


class Fake_MonitorQQFunction:
    def __init__(self):
        self.send_ids = []
        self.send_messages = []

    def send_message(self, target_id, message):
        self.send_ids.append(target_id)
        self.send_messages.append(message)


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LoggerConfig.logger_config(None)

    def test_mainEntry(self):
        fc = FunctionController()
        fc.start()
        monitorQQ = Fake_MonitorQQFunction()
        timeReminder = TimeReminderFunction(fc, monitorQQ)
        self.assertEqual(True, timeReminder.mainEntry("嗨谷雨半分钟之后提醒我泡面好了"))  # add assertion here
        self.assertEqual(1, len(monitorQQ.send_messages))
        self.assertEqual(1, len(monitorQQ.send_ids))
        self.assertEqual("设定提醒： 半分钟 之后，提醒：泡面好了", monitorQQ.send_messages[0])
        self.assertEqual(980858153, monitorQQ.send_ids[0])
        time.sleep(27)
        self.assertEqual(1, len(monitorQQ.send_messages))
        self.assertEqual(1, len(monitorQQ.send_ids))
        time.sleep(3)
        self.assertEqual(2, len(monitorQQ.send_messages))
        self.assertEqual(2, len(monitorQQ.send_ids))

        self.assertEqual("提醒：已到 半分钟 之后，提醒：泡面好了", monitorQQ.send_messages[1])
        self.assertEqual(980858153, monitorQQ.send_ids[1])
        fc.stop()

    def test_hourToSecond(self):
        self.assertEqual(5 * 3600, hourToSecond("五"))
        self.assertEqual(15 * 3600, hourToSecond("十五"))
        self.assertEqual(20 * 3600, hourToSecond("二十"))
        self.assertEqual(25 * 3600, hourToSecond("二十五"))
        self.assertEqual(0.5 * 3600, hourToSecond("半"))
        self.assertEqual(1.5 * 3600, hourToSecond("一个半"))

    def test_minuteToSecond(self):
        self.assertEqual(5 * 60, minuteToSecond("五"))
        self.assertEqual(15 * 60, minuteToSecond("十五"))
        self.assertEqual(20 * 60, minuteToSecond("二十"))
        self.assertEqual(25 * 60, minuteToSecond("二十五"))
        self.assertEqual(0.5 * 60, minuteToSecond("半"))

    def test_chineseToTime(self):
        self.assertEqual(5 * 60, chineseToTime("五分钟"))
        self.assertEqual(15 * 60, chineseToTime("十五分钟"))
        self.assertEqual(20 * 60, chineseToTime("二十分钟"))
        self.assertEqual(25 * 60, chineseToTime("二十五分钟"))
        self.assertEqual(0.5 * 60, chineseToTime("半分钟"))
        self.assertEqual(5 * 3600, chineseToTime("五小时"))
        self.assertEqual(15 * 3600, chineseToTime("十五小时"))
        self.assertEqual(20 * 3600, chineseToTime("二十小时"))
        self.assertEqual(25 * 3600, chineseToTime("二十五小时"))
        self.assertEqual(0.5 * 3600, chineseToTime("半小时"))
        self.assertEqual(1.5 * 3600, chineseToTime("一个半小时"))
        self.assertEqual(3600 + 5 * 60, chineseToTime("一小时五分钟"))
        self.assertEqual(3600 + 15 * 60, chineseToTime("一小时十五分钟"))
        self.assertEqual(3600 + 20 * 60, chineseToTime("一小时二十分钟"))
        self.assertEqual(3600 + 25 * 60, chineseToTime("一小时二十五分钟"))
        self.assertEqual(3600 + 5 * 60, chineseToTime("一个小时五分钟"))
        self.assertEqual(3600 + 15 * 60, chineseToTime("一个小时十五分钟"))
        self.assertEqual(3600 + 20 * 60, chineseToTime("一个小时二十分钟"))
        self.assertEqual(3600 + 25 * 60, chineseToTime("一个小时二十五分钟"))


if __name__ == '__main__':
    unittest.main()

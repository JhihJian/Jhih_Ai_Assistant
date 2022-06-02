import asyncio
import time
from contextlib import suppress

from function.BaseFunction import BaseFunction

import re

chinese_dict = {
    "一": 1,
    '二': 2,
    "三": 3,
    "四": 4,
    '五': 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10
}


# 五分钟 十五分钟 二十五分钟 半小时 1小时十分钟 一小时20分钟
def chineseToTime(time_str):
    time_list = re.findall(r"^(.+?)个小时(.+?)分钟", time_str)
    if time_list:
        time_list = time_list[0]
        return hourToSecond(time_list[0]) + minuteToSecond(time_list[1])
    time_list = re.findall(r"^(.+?)小时(.+?)分钟", time_str)
    if time_list:
        time_list = time_list[0]
        return hourToSecond(time_list[0]) + minuteToSecond(time_list[1])
    time_list = re.findall(r"(.+?)小时", time_str)
    if time_list:
        return hourToSecond(time_list[0])
    time_list = re.findall(r"(.+?)分钟", time_str)
    if time_list:
        return minuteToSecond(time_list[0])
    return 0


# minute = 一 五 十 十五 二十 二十五
def minuteToSecond(minute):
    with suppress(ValueError):
        minute_int = int(minute)
        return minute_int * 60
    if minute == "半":
        return 0.5 * 60
    time_list = re.findall(r"(.+?)十(.+?)", minute)
    if time_list:
        time_list = time_list[0]
        return (chinese_dict[time_list[0]] * 10 + chinese_dict[time_list[1]]) * 60
    time_list = re.findall(r"十(.+?)", minute)
    if time_list:
        return (10 + chinese_dict[time_list[0]]) * 60
    time_list = re.findall(r"(.+?)十", minute)
    if time_list:
        return (10 * chinese_dict[time_list[0]]) * 60
    return chinese_dict[minute] * 60


# hour = 五 十五 二十 二十五 半 一个半
def hourToSecond(hour):
    with suppress(ValueError):
        hour_int = int(hour)
        return hour_int * 3600
    time_list = re.findall(r"(.+?)个半", hour)
    if time_list:
        return (chinese_dict[time_list[0]] + 0.5) * 3600
    if hour == "半":
        return 0.5 * 3600
    time_list = re.findall(r"(.+?)十(.+?)", hour)
    if time_list:
        time_list = time_list[0]
        return (chinese_dict[time_list[0]] * 10 + chinese_dict[time_list[1]]) * 3600
    time_list = re.findall(r"十(.+?)", hour)
    if time_list:
        return (10 + chinese_dict[time_list[0]]) * 3600
    time_list = re.findall(r"(.+?)十", hour)
    if time_list:
        return (10 * chinese_dict[time_list[0]]) * 3600
    return chinese_dict[hour] * 3600


if __name__ == '__main__':
    chineseToTime("五分钟")
    chineseToTime("十五分钟")
    chineseToTime("二十五分钟")
    chineseToTime("半小时")
    chineseToTime("1小时十分钟")
    chineseToTime("一小时20分钟")
    hourToSecond("半")


# 嗨谷雨五分钟之后提醒我泡面好了
# hi谷雨五分钟之后提醒我泡面好了
# 嗨谷雨五分钟之后提醒我要去做核酸了
# 用正则提取关键词 (.+?)
class TimeReminderFunction(BaseFunction):
    def __init__(self, function_controller, monitor_qq_function):
        super().__init__(function_controller)
        self.monitor_qq_function = monitor_qq_function

    def mainEntry(self, message):
        if not self.monitor_qq_function:
            self.logger.info("时间提醒功能：monitor qq 未启动")
            return False
        result = re.findall(r"谷雨(.+?)之后提醒我(.+?)$", message)
        if not result:
            return False
        result = result[0]
        wait_second = chineseToTime(result[0])
        current_message = f"设定提醒： {result[0]} 之后，提醒：{result[1]}"
        reminder_message = f"提醒：已到 {result[0]} 之后，提醒：{result[1]}"
        self.function_controller.append_async_task(self.__waitToReminder, wait_second, reminder_message)
        self.monitor_qq_function.send_message(980858153, current_message)
        return True

    async def __waitToReminder(self, wait_second, reminder_message):
        self.logger.info(f"wait {wait_second}s to reminder:{reminder_message}")
        await asyncio.sleep(wait_second)
        self.monitor_qq_function.send_message(980858153, reminder_message)

    def start(self):
        super().start()

    def quit(self):
        super().quit()

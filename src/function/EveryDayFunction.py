import asyncio
from urllib import request

from function import QQSocket
from function.BaseFunction import BaseFunction, FunctionStatus
from datetime import date, datetime

LAST_RUN_DAY_KEY = "LAST_RUN_DAY"

Know_library_Page_Url = "https://jhihjian.github.io/JhihJian-Know-Library/"


async def libraryPageIsOnline():
    try:
        contents = request.urlopen(Know_library_Page_Url).read()
        if contents:
            await QQSocket.send_message_alone(980858153, "每日任务：检查jhihjian.github.io博客，已完成，运行正常")
            return True
        else:
            await QQSocket.send_message_alone(980858153, "每日任务：检查jhihjian.github.io博客，已完成，运行有误")
            return False
    except Exception as e:
        await QQSocket.send_message_alone(980858153, f"每日任务：检查jhihjian.github.io博客，无法完成，{e}")
        return False


def isNewDay(db):
    today = str(date.today())
    last_run_day = db.get_str_by_key(LAST_RUN_DAY_KEY)
    is_new_day = False
    if not last_run_day:
        is_new_day = True
    else:
        if last_run_day != today:
            is_new_day = True

    if is_new_day:
        db.store_str_by_key(LAST_RUN_DAY_KEY, today)

    return is_new_day


class EveryDayFuntion(BaseFunction):

    def __init__(self, function_controller, run_functions):
        super().__init__(function_controller)
        self.run_functions = run_functions

    # 用于run异步回调退出，不主动调用
    def quit(self, f):
        # super().quit()
        self.logger.info("每日任务已完成")
        self.function_status = FunctionStatus.STOP

    def start(self):
        self.function_status = FunctionStatus.STARTING
        self.logger.info("开始每日任务...")
        task = self.function_controller.append_sync_task(self.run)
        task.add_done_callback(self.quit)

    # 运行每日任务
    def run(self):
        self.function_status = FunctionStatus.RUNNING
        tasks_dict = {}
        for function in self.run_functions:
            try:
                pre = datetime.now()
                self.logger.info(f"开始 {function.__name__} 任务...")
                if asyncio.iscoroutinefunction(function):
                    # asyncio.run(libraryPageIsOnline())
                    task = self.function_controller.append_async_task(function)
                    tasks_dict[task] = function

                else:
                    function()
                    self.logger.info(f"完成 {function.__name__} 任务 耗时:{datetime.now() - pre}.")
            except Exception as e:
                self.logger.info(f"{function.__name__} 任务,出现异常,已结束,{e}")
        for task, function in tasks_dict.items():
            pre = datetime.now()
            # 用于等待异步任务(asyncio.Future)完成,超市15s
            result = task.result(15)
            self.logger.info(f"等待完成 {function.__name__} 异步任务 耗时:{datetime.now() - pre}.")

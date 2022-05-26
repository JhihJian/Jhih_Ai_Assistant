import logging
import time
from asyncio import futures
from datetime import datetime

from contextlib import suppress
from threading import Thread
import asyncio

from util import AppSetting


class FunctionController(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(AppSetting.APP_LOG_NAME)
        self.loop = None
        self.tasks_dict = {}

    # 停止任务
    def stop_task(self, function_hook):
        if function_hook not in self.tasks_dict:
            return False
        task = self.tasks_dict[function_hook]
        task.cancel()
        self.logger.info(f"remove async task {function_hook.__name__} current tasks size {len(self.tasks_dict)}")
        # 为什么这里不要调用 run_until_complete 再退出呢？
        return True

    # 运行异步任务
    def run_async_task_wait(self, function_hook, *args):
        pre = datetime.now()
        task = asyncio.run_coroutine_threadsafe(function_hook(*args), self.loop)
        self.tasks_dict[function_hook] = task

        # 完成后删除
        def _on_completion(f):
            if self.loop.is_running():
                for key, value in dict(self.tasks_dict).items():
                    if value == f:
                        del self.tasks_dict[key]

        task.add_done_callback(_on_completion)
        # 阻塞进程等待完成
        result = task.result(15)

        self.logger.info(f"run async task {function_hook.__name__} wait {datetime.now() - pre}")
        return task

    # 运行异步任务
    def append_async_task(self, function_hook, *args):
        task = asyncio.run_coroutine_threadsafe(function_hook(*args), self.loop)
        self.tasks_dict[function_hook] = task

        # 完成后删除
        def _on_completion(f):
            if self.loop.is_running():
                for key, value in dict(self.tasks_dict).items():
                    if value == f:
                        del self.tasks_dict[key]

        task.add_done_callback(_on_completion)

        self.logger.info(f"append async task {function_hook.__name__} current tasks size {len(self.tasks_dict)}")
        return task

    def append_sync_task(self, function_hook, *args):
        self.logger.info(f"append sync task {function_hook.__name__} ")
        task = self.loop.run_in_executor(None, function_hook, *args)
        self.tasks_dict[function_hook] = task
        return task

    # This method will raise a RuntimeError if called more than once on the same thread object.
    def run(self):
        self.loop = asyncio.new_event_loop()
        loop = self.loop

        asyncio.set_event_loop(loop)
        try:
            # run loop:
            loop.run_forever()
            # 关闭异步迭代器
            loop.run_until_complete(loop.shutdown_asyncgens())
            # cancel task:
            for task in self.tasks_dict.values():
                task.cancel()
            # 调用 cancel 后，会在task的下个循环中，抛出CancelledError ，所以需要以下内容
            # https://stackoverflow.com/questions/40897428/please-explain-task-was-destroyed-but-it-is-pending-after-cancelling-tasks
            # 这里运行即退出 无需多做一次循环内容
            with suppress(asyncio.CancelledError):
                # run_coroutine_threadsafe 返回的是concurrent.futures
                # run_until_complete 类型不匹配报错,类型是concurrent.futures  期望是 An asyncio.Future, a coroutine or an awaitable
                # 不能使用 asyncio.wrap_future 转换，因为会生成新的task ,导致loop中有两个task ?????
                # 使用 asyncio.ensure_future(task) 转换,无法转换 类型不支持
                for task in self.tasks_dict.values():
                    if not futures.isfuture(task):
                        task = asyncio.wrap_future(task)
                    loop.run_until_complete(task)
        finally:
            self.logger.info(f"function controller close loop {datetime.now()}")
            loop.close()

    def stop(self):
        # 这里调用是异步的，语句结束后，不一定存在任何变化
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.join()


if __name__ == '__main__':
    async def test_print():
        while True:
            await asyncio.sleep(1)
            print(f"{datetime.now()}")


    fc = FunctionController()
    fc.start()
    time.sleep(1)

    fc.append_async_task(test_print)
    time.sleep(2)
    fc.stop_task(test_print)
    print(f"join finish tasks size:{len(fc.tasks_dict)}")
    fc.stop()
    print("all to stop")
    time.sleep(5)

import logging
from enum import Enum


class FunctionStatus(Enum):
    RUNNING = "RUNNING"
    STOP = "STOP"
    STARTING = "STARTING"
    WAIT = "WAIT"  # 准备好运行了，等待触发条件


class BaseFunction:
    function_name = "BaseFunction"
    function_status = FunctionStatus.STOP

    def __init__(self):
        self.logger = logging.getLogger("MainWindow")

    def register(self):
        pass

    def start(self):
        self.function_status = FunctionStatus.STARTING

        self.function_status = FunctionStatus.RUNNING
        pass

    def quit(self):
        self.function_status = FunctionStatus.STOP
        pass

    def isOnline(self):
        return self.function_status == FunctionStatus.RUNNING

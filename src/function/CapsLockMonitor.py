import threading
from datetime import datetime

import keyboard


class CapsLockMonitor:
    wait_time = 300 * 1000  # 设置监听缓存时间，长按300毫秒后开始
    __on_running = False  # 是否已经开始运行
    is_trigger_down = False  # 是否之前按下了CapsLock键
    trigger_down_time = datetime.now()  # 刚开始按下的时间

    def __init__(self, begin_event_hook=None, finish_event_hook=None):
        self.__beginEventHook = begin_event_hook
        self.__finishEventHook = finish_event_hook

    def run(self):
        threading.Thread(target=self.__monitor).start()

    def __monitor(self):
        # 开始监听大写锁定键()
        keyboard.hook_key('caps lock', self.__trick_hook_key)

    def __trick_hook_key(self, event):
        if event.event_type == "down":
            if self.is_trigger_down:
                diff = (datetime.now() - self.trigger_down_time).microseconds
                if diff < self.wait_time:
                    print("时间没到不运行 {}".format(diff))
                    return
            else:
                self.trigger_down_time = datetime.now()
                self.is_trigger_down = True
                return
            try:
                # 已经在运行就不触发
                if self.__on_running:
                    # print("已经在运行就不触发")
                    pass
                else:
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
            print("Finish CapsLock Event")
            self.__on_running = False

            if self.__finishEventHook:
                try:
                    self.__finishEventHook()
                except Exception as e:
                    print("error from finishEventHook {}: {}".format(self.__finishEventHook, e))
        else:
            print(event.event_type)
            pass

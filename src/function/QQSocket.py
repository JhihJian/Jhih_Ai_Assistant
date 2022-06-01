#!/usr/bin/env python

import asyncio
import json
import logging
import threading
import time
from datetime import datetime

import websockets

from function.BaseFunction import BaseFunction, FunctionStatus
from function.FunctionController import FunctionController
from function.MessageHandle import MessageHandle
from util import LoggerConfig
from util.DbHelper import DbHelper
from util.QueryProcess import QueryProcess

logger = logging.getLogger("MainWindow")
SEND_MESSAGE_TEMPLATE = """
{
    "action": "send_private_msg",
    "params": {
        "user_id": 980858153,
        "message": "ddd"
    },
    "echo": "123"
}
"""


def on_message(msg):
    print(msg)


# def handle_message(websocket, sender_id, message):
#     reply_message = ""
#     if message == "哥哥在打游戏吗":
#         query_process = QueryProcess()
#         if query_process.IsPlayingLol():
#             reply_message = "在，游戏客户端开始时间:{}".format(query_process.IsPlayingLol())
#         else:
#             reply_message = "没，我也不知道他在干嘛"
#     elif message == "查询仔仔分数":
#         db = DbHelper()
#         score = db.get_zz_score()
#         reply_message = "仔仔当前分数为:{}".format(score)
#     elif message == "查询仔仔分数原因":
#         db = DbHelper()
#         reasons = db.get_zz_score_reasons()
#         reply_message = "仔仔当前分数原因为:\n{}".format(reasons)
#     elif message.startswith("更新仔仔分数") and str(sender_id) == "980858153":
#         try:
#             infos = message.split(",")
#             db = DbHelper()
#             db.update_zz_score(int(infos[1]), infos[2])
#             reply_message = "更新成功"
#         except Exception as e:
#             reply_message = "更新失败，{}".format(e)
#     elif message == "查询健健分数":
#         db = DbHelper()
#         score = db.get_jj_score()
#         reply_message = "健健当前分数为:{}".format(score)
#     elif message == "查询健健分数原因":
#         db = DbHelper()
#         reasons = db.get_jj_score_reasons()
#         reply_message = "健健当前分数原因为:\n{}".format(reasons)
#     elif message.startswith("更新健健分数") and str(sender_id) == "980858153":
#         try:
#             infos = message.split(",")
#             db = DbHelper()
#             db.update_jj_score(int(infos[1]), infos[2])
#             reply_message = "更新成功"
#         except Exception as e:
#             reply_message = "更新失败，{}".format(e)
#     else:
#         reply_message = "hello {},what's {}".format(sender_id, message)
#
#     data = json.loads(SEND_MESSAGE_TEMPLATE)
#     data["params"]["user_id"] = sender_id
#     data["params"]["message"] = reply_message
#     print("data:{}".format(data))
#     asyncio.create_task(send_message(websocket, json.dumps(data)))


async def send_message(websocket, data):
    await websocket.send(data)


#
# async def send_message_alone(target_id, message):
#     sender_id = target_id
#     data = json.loads(SEND_MESSAGE_TEMPLATE)
#     data["params"]["user_id"] = sender_id
#     data["params"]["message"] = message
#     async with websockets.connect("ws://localhost:6700/api") as websocket:
#         print(json.dumps(data))
#         await websocket.send(json.dumps(data))
#         # result = await websocket.recv()
#         # print(result)

qq_monitor_address_key = "qq_monitor_address_key"


class MonitorQQFunction(BaseFunction):
    function_name = "MonitorQQFunction"

    # async method on other threading loop run
    # 如何将异步函数传递给 Python 中的线程目标？

    def __init__(self, function_controller, db):
        super().__init__(function_controller)
        self.monitor_address = None
        self.websocket = None
        # self.monitor_address = monitor_address
        # self.logger.info(f"init qq monitor address:{self.monitor_address}")
        self.message_handle = MessageHandle(self)
        self.db = db

    def start(self):
        qq_monitor_address = self.db.get_str_by_key(qq_monitor_address_key)
        if not qq_monitor_address:
            self.logger.error("监控QQ功能:未配置监听地址，无法启动")
            return
        self.monitor_address = qq_monitor_address
        self.logger.info("监控QQ功能启动中...")
        self.function_status = FunctionStatus.STARTING
        self.function_controller.append_async_task(self.monitor_message)

    def quit(self):
        self.logger.info("监控QQ功能退出中...")
        if self.websocket:
            # 直接调用 self.websocket.close()
            # 报错 RuntimeWarning: coroutine 'WebSocketCommonProtocol.close' was never awaited
            # 改为以下
            self.function_controller.run_async_task_wait(self.websocket.close)

        self.function_controller.stop_task(self.monitor_message)
        # 这里调用结束了，不代表真的立刻STOP了
        self.function_status = FunctionStatus.STOP
        self.logger.info("监控QQ功能退出完成")

    def send_message_to_JJ(self, message):
        self.function_controller.append_async_task(self.__send_message, 980858153, message)

    def send_message_to_ZZ(self, message):
        self.function_controller.append_async_task(self.__send_message, 1600074410, message)

    def send_message_to_all(self, message):
        self.send_message_to_JJ(message)
        self.send_message_to_ZZ(message)

    def send_message(self, target_id, message):
        self.function_controller.append_async_task(self.__send_message, target_id, message)

    async def __send_message(self, target_id, message):
        sender_id = target_id
        data = json.loads(SEND_MESSAGE_TEMPLATE)
        data["params"]["user_id"] = sender_id
        data["params"]["message"] = message
        await self.websocket.send(json.dumps(data))

    # {"font":0,"message":"sad","message_id":24727482,"message_type":"private","post_type":"message","raw_message":"sad","self_id":1935912438,"sender":{"age":0,"nickname":"Jhih","sex":"unknown","user_id":980858153},"sub_type":"friend","target_id":1935912438,"time":1652083856,"user_id":980858153}
    # {"interval":5000,"meta_event_type":"heartbeat","post_type":"meta_event","self_id":1935912438,"status":{"app_enabled":true,"app_good":true,"app_initialized":true,"good":true,"online":true,"plugins_good":null,"stat":{"PacketReceived":178,"PacketSent":163,"PacketLost":0,"MessageReceived":3,"MessageSent":5,"LastMessageTime":1652083856,"DisconnectTimes":0,"LostTimes":0}},"time":1652083858}
    async def monitor_message(self):
        try:
            logger = self.logger
            async with websockets.connect(self.monitor_address, logger=logger) as self.websocket:
                self.function_status = FunctionStatus.RUNNING
                self.logger.info(f"监控QQ功能启动完成,监听地址:{self.monitor_address}")
                # 上线通知
                self.send_message_to_JJ("谷雨上线通知~")
                while True:
                    r_data = json.loads(await self.websocket.recv())
                    # 心跳测试
                    if "meta_event_type" in r_data and r_data["meta_event_type"] == "heartbeat":
                        continue
                    # 收到私信
                    elif "message_type" in r_data and r_data["message_type"] == "private":
                        try:
                            sender_id = r_data["sender"]["user_id"]
                            sender_nick_name = r_data["sender"]["nickname"]
                            message = r_data["message"]
                            logger.info(
                                "sender id:{} name:{} send message:{}".format(sender_id, sender_nick_name, message))
                        except Exception as e:
                            logger.error("load json data failed exception:{} data:{}".format(e, r_data))

                        try:
                            # handle_message(self.websocket, sender_id, message)
                            self.message_handle.mainEntry(sender_id, message)
                        except Exception as e:
                            logger.error(f"send data failed exception:{e}")
                    else:
                        logger.info(r_data)
        finally:
            self.logger.info("quit monitor_message")

#
# if __name__ == '__main__':
#     logger = LoggerConfig.logger_config(None)
#     fc = FunctionController()
#     fc.start()
#     time.sleep(1)
#     qq = MonitorQQFunction(fc, "ws://localhost:6700/api")
#     qq.start()
#     qq.send_message_to_JJ("测试")
#     time.sleep(3)
#     qq.quit()
#     time.sleep(1)
#     fc.stop()
#     print("主线程结束")

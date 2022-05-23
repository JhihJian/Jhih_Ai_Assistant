#!/usr/bin/env python

import asyncio
import json
import logging
import threading
import time

import websockets

from function.BaseFunction import BaseFunction, FunctionStatus
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


# {"font":0,"message":"sad","message_id":24727482,"message_type":"private","post_type":"message","raw_message":"sad","self_id":1935912438,"sender":{"age":0,"nickname":"Jhih","sex":"unknown","user_id":980858153},"sub_type":"friend","target_id":1935912438,"time":1652083856,"user_id":980858153}
# {"interval":5000,"meta_event_type":"heartbeat","post_type":"meta_event","self_id":1935912438,"status":{"app_enabled":true,"app_good":true,"app_initialized":true,"good":true,"online":true,"plugins_good":null,"stat":{"PacketReceived":178,"PacketSent":163,"PacketLost":0,"MessageReceived":3,"MessageSent":5,"LastMessageTime":1652083856,"DisconnectTimes":0,"LostTimes":0}},"time":1652083858}
async def monitor_message():
    async with websockets.connect("ws://localhost:6700/", logger=logger) as websocket:
        while True:
            r_data = json.loads(await websocket.recv())
            # 心跳测试
            if "meta_event_type" in r_data and r_data["meta_event_type"] == "heartbeat":
                continue
            # 收到私信
            elif "message_type" in r_data and r_data["message_type"] == "private":
                try:
                    sender_id = r_data["sender"]["user_id"]
                    sender_nick_name = r_data["sender"]["nickname"]
                    message = r_data["message"]
                    logger.info("sender id:{} name:{} send message:{}".format(sender_id, sender_nick_name, message))
                except Exception as e:
                    logger.error("load json data failed exception:{} data:{}".format(e, r_data))

                try:
                    handle_message(websocket, sender_id, message)
                except Exception as e:
                    logger.error("send data failed exception:{}".format(e))
            else:
                logger.info(r_data)


def handle_message(websocket, sender_id, message):
    reply_message = ""
    if message == "哥哥在打游戏吗":
        query_process = QueryProcess()
        if query_process.IsPlayingLol():
            reply_message = "在，游戏客户端开始时间:{}".format(query_process.IsPlayingLol())
        else:
            reply_message = "没，我也不知道他在干嘛"
    elif message == "查询仔仔分数":
        db = DbHelper()
        score = db.get_zz_score()
        reply_message = "仔仔当前分数为:{}".format(score)
    elif message == "查询仔仔分数原因":
        db = DbHelper()
        reasons = db.get_zz_score_reasons()
        reply_message = "仔仔当前分数原因为:\n{}".format(reasons)
    elif message.startswith("更新仔仔分数") and str(sender_id) == "980858153":
        try:
            infos = message.split(",")
            db = DbHelper()
            db.update_zz_score(int(infos[1]), infos[2])
            reply_message = "更新成功"
        except Exception as e:
            reply_message = "更新失败，{}".format(e)
    elif message == "查询健健分数":
        db = DbHelper()
        score = db.get_jj_score()
        reply_message = "健健当前分数为:{}".format(score)
    elif message == "查询健健分数原因":
        db = DbHelper()
        reasons = db.get_jj_score_reasons()
        reply_message = "健健当前分数原因为:\n{}".format(reasons)
    elif message.startswith("更新健健分数") and str(sender_id) == "980858153":
        try:
            infos = message.split(",")
            db = DbHelper()
            db.update_jj_score(int(infos[1]), infos[2])
            reply_message = "更新成功"
        except Exception as e:
            reply_message = "更新失败，{}".format(e)
    else:
        reply_message = "hello {},what's {}".format(sender_id, message)

    data = json.loads(SEND_MESSAGE_TEMPLATE)
    data["params"]["user_id"] = sender_id
    data["params"]["message"] = reply_message
    print("data:{}".format(data))
    asyncio.create_task(send_message(websocket, json.dumps(data)))


async def send_message(websocket, data):
    await websocket.send(data)


async def send_message_alone(target_id, message):
    sender_id = target_id
    data = json.loads(SEND_MESSAGE_TEMPLATE)
    data["params"]["user_id"] = sender_id
    data["params"]["message"] = message
    async with websockets.connect("ws://localhost:6700/api") as websocket:
        print(json.dumps(data))
        await websocket.send(json.dumps(data))
        result = await websocket.recv()
        print(result)


def call_send_entry(target_id, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_message_alone(target_id, message))
    loop.close()


class MonitorQQFunction(BaseFunction):
    function_name = "MonitorQQFunction"

    # async method on other threading loop run
    # 如何将异步函数传递给 Python 中的线程目标？

    def __init__(self):
        super().__init__()
        self.loop = None

    def start(self):
        self.function_status = FunctionStatus.STARTING
        self.loop = asyncio.new_event_loop()

        def call_monitor_entry(loop):
            asyncio.set_event_loop(loop)
            loop.create_task(monitor_message())
            loop.run_forever()
            loop.close()

        _thread = threading.Thread(target=call_monitor_entry, args=[self.loop])
        _thread.start()
        self.function_status = FunctionStatus.RUNNING
        pass

    def quit(self):
        self.loop.stop()
        while not self.loop.is_closed():
            time.sleep(0.1)
        self.function_status = FunctionStatus.STOP
        pass

    def send_message_to_JJ(self, message):
        _thread = threading.Thread(target=call_send_entry, args=[980858153, message])
        _thread.start()

    def send_message_to_ZZ(self, message):
        _thread = threading.Thread(target=call_send_entry, args=[1600074410, message])
        _thread.start()

    def send_message_to_all(self, message):
        self.send_message_to_JJ(message)
        self.send_message_to_ZZ(message)


if __name__ == '__main__':
    qq = MonitorQQFunction()
    qq.start()
    qq.send_message_to_JJ("测试")
    time.sleep(3)
    qq.quit()
    print("主线程继续执行")

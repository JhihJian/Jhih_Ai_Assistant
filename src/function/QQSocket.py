#!/usr/bin/env python

import asyncio
import json

import websockets

from function.QueryProcess import QueryProcess

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


# {"font":0,"message":"sad","message_id":24727482,"message_type":"private","post_type":"message","raw_message":"sad","self_id":1935912438,"sender":{"age":0,"nickname":"Jhih","sex":"unknown","user_id":980858153},"sub_type":"friend","target_id":1935912438,"time":1652083856,"user_id":980858153}
# {"interval":5000,"meta_event_type":"heartbeat","post_type":"meta_event","self_id":1935912438,"status":{"app_enabled":true,"app_good":true,"app_initialized":true,"good":true,"online":true,"plugins_good":null,"stat":{"PacketReceived":178,"PacketSent":163,"PacketLost":0,"MessageReceived":3,"MessageSent":5,"LastMessageTime":1652083856,"DisconnectTimes":0,"LostTimes":0}},"time":1652083858}
async def monitor_message():
    async with websockets.connect("ws://localhost:6700/") as websocket:
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
                    print("sender id:{} name:{} send message:{}".format(sender_id, sender_nick_name, message))
                except Exception as e:
                    print("load json data failed exception:{} data:{}".format(e, r_data))

                try:
                    handle_message(websocket, sender_id, message)
                except Exception as e:
                    print("send data failed exception:{}".format(e))
            else:
                print(r_data)


def handle_message(websocket, sender_id, message):
    reply_message = ""
    if message == "哥哥在打游戏吗":
        query_process = QueryProcess()
        if query_process.IsPlayingLol():
            reply_message = "在，游戏客户端开始时间:{}".format(query_process.IsPlayingLol())
        else:
            reply_message = "没，我也不知道他在干嘛"
    else:
        reply_message = "hello {},what's {}".format(sender_id, message)
    data = json.loads(SEND_MESSAGE_TEMPLATE)
    data["params"]["user_id"] = sender_id
    data["params"]["message"] = reply_message
    print("data:{}".format(data))
    asyncio.create_task(send_message(websocket, json.dumps(data)))


async def send_message(websocket, data):
    await websocket.send(data)


async def send_message_test():
    sender_id = 980858153
    reply_message = "hello 980858153,what's asda"
    data = json.loads(SEND_MESSAGE_TEMPLATE)
    data["params"]["user_id"] = sender_id
    data["params"]["message"] = reply_message
    async with websockets.connect("ws://localhost:6700/api") as websocket:
        print(json.dumps(data))
        await websocket.send(json.dumps(data))
        result = await websocket.recv()
        print(result)


if __name__ == '__main__':
    asyncio.run(monitor_message())

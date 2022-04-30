import threading

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

APPID = 'fc780f5a'
APISecret = 'NzQ2MzdiMDQwNTBlZWQ1NjNkYzY1OGU2'
APIKey = 'a8f61f43023fdebc164849cfbc22c9cb'


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo": 1, "vad_eos": 10000}

    # 生成url
    def create_url(self):
        url = 'wss://iat-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url

    def get_json_data(self, status, data):
        if status == STATUS_FIRST_FRAME:
            d = {"common": self.CommonArgs,
                 "business": self.BusinessArgs,
                 "data": {"status": 0, "format": "audio/L16;rate=16000",
                          "audio": str(base64.b64encode(data), 'utf-8'),
                          "encoding": "raw"}}
        elif status == STATUS_CONTINUE_FRAME:
            d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                          "audio": str(base64.b64encode(data), 'utf-8'),
                          "encoding": "raw"}}
        elif status == STATUS_LAST_FRAME:
            # 空白的结束标识
            d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                          "audio": str(base64.b64encode(data), 'utf-8'),
                          "encoding": "raw"}}
        # print("get_json_data:" + str(d))
        return json.dumps(d)


def on_message(self, ws, message):
    print("### on_message ###")


# 语音识别器
class VoiceRecognizer:
    data = []
    识别器准备就绪 = False
    status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧
    frameSize = 1024  # 每一帧的音频大小
    interval = 0.04  # 发送音频间隔(单位:s)
    resultText = ''

    # 收到websocket错误的处理
    def on_error(self, ws, error):
        print("### error:", error)

    # 收到websocket关闭的处理
    def on_close(self, ws, c1, c2):
        print("### closed ###")

    def on_open(self, ws):
        print("on_open")
        self.识别器准备就绪 = True

    def __init__(self):
        self.wsParam = Ws_Param(APPID=APPID, APISecret=APISecret,
                                APIKey=APIKey)
        websocket.enableTrace(False)
        wsUrl = self.wsParam.create_url()
        self.ws = websocket.WebSocketApp(wsUrl, on_error=self.on_error, on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.on_message = self.on_message
        print("init finish")

    def run(self):
        print("Run VoiceRecognizer")
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    # 发送识别的数据
    def send(self, data):
        time1 = datetime.now()
        time.sleep(0.04)
        while not self.识别器准备就绪:
            time.sleep(0.01)
        if self.status == STATUS_FIRST_FRAME:
            time2 = datetime.now()
            print("wait 识别器准备就绪 cost:" + str(time2 - time1))
        print("send data len:" + str(len(data)) + ",status:" + str(self.status))
        d = self.wsParam.get_json_data(self.status, data)
        self.ws.send(d)
        self.status = STATUS_CONTINUE_FRAME

    # 收到websocket消息的处理
    def on_message(self, ws, message):
        print("on_message")
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            if code != 0:
                errMsg = json.loads(message)["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

            else:
                data = json.loads(message)["data"]["result"]["ws"]
                print(json.loads(message))
                result = ""
                for i in data:
                    for w in i["cw"]:
                        result += w["w"]
                # print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))
            self.resultText += result
        except Exception as e:
            print("receive msg,but parse exception:", e)

    # 识别结束
    def finish(self):
        self.status = STATUS_LAST_FRAME
        self.send(b'')
        # 空白的结束标识
        # d = self.wsParam.get_json_data(self.status, b'')
        # self.ws.send(d)
        self.ws.close()
        print("resultText:" + self.resultText)


if __name__ == "__main__":
    t1 = datetime.now()
    AudioFile = 'K:/3-WorkSpace/2-Python-Projects/Jhih_Ai_Assistant/src/function/recordedFile.wav'
    # 测试时候在此处正确填写相关信息即可运行
    recognizer = VoiceRecognizer()
    threading.Thread(target=recognizer.run).start()

    with open(AudioFile, "rb") as fp:
        while True:
            buf = fp.read(1280)
            # 文件结束
            if not buf:
                recognizer.finish()
                time.sleep(1.5)
                break
            recognizer.send(buf)
            # 模拟音频采样间隔
            time.sleep(recognizer.interval)

    # print("resultText:" + recognizer.resultText)
    t2 = datetime.now()
    print(t2 - t1)

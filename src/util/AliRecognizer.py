import json
import time
import threading
import keyboard
import nls

URL = "wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1"


# 调用阿里云进行语音识别
class AliRecognizer:
    SEND_INTERVAL = 0.1  # 秒
    already_send = 0
    # 识别程序准备是否完成
    isRecognizerReady = False
    recognizer_callable = None  # 识别结果的回调函数

    # is_begin 说明录音开始
    # is_finish 说明录音结束
    # get_record_frames 实时获得录音帧，只要未结束不断调用
    # recognizer_callable 提交录音识别结果的回调
    def __init__(self, ak_id, ak_secret, app_key, get_record_frames, is_finish, is_begin=None,
                 recognizer_callable=None):
        self.is_nls_start = False
        self.__id = '__id'
        self.sr = nls.NlsSpeechRecognizer(
            url=URL,
            akid=ak_id,
            aksecret=ak_secret,
            appkey=app_key,
            on_start=self.test_on_start,
            on_result_changed=self.test_on_result_chg,
            on_completed=self.test_on_completed,
            on_error=self.test_on_error,
            on_close=self.test_on_close,
            callback_args=[self.__id]
        )
        if (get_record_frames is None) or (is_finish is None):
            raise Exception()
        self.get_record_frames = get_record_frames
        self.is_finish = is_finish
        self.is_begin = is_begin
        self.recognizer_callable = recognizer_callable

    def __continue_send(self):
        while not self.isRecognizerReady:
            time.sleep(0.01)
        frames = self.get_record_frames()
        while len(frames) == 0:
            time.sleep(0.01)
            frames = self.get_record_frames()
        # print("send frames size:{}".format(len(frames)))
        while (not self.is_finish()) or len(frames) > self.already_send:
            ready_to_send_frames = frames[self.already_send:]
            # print("self.already_send:" + str(self.already_send) + " ready_to_send_frames size:" + str(
            #     len(ready_to_send_frames)))

            for frame in ready_to_send_frames:
                self.send(frame)
                self.already_send += 1
                time.sleep(self.SEND_INTERVAL)
            frames = self.get_record_frames()
        # print("__continue_send finish")
        # self.finish()
        self.sr.stop()

    def run(self):
        self.is_nls_start = self.sr.start(aformat="pcm", ex={"hello": 123})
        self.already_send = 0
        self.__continue_send()

    def send(self, data):
        # print("send data")
        self.sr.send_audio(bytes(data))

    def finish(self):
        if self.sr:
            if self.is_nls_start:
                self.sr.stop()
            if self.isRecognizerReady:
                self.sr.shutdown()
            del self.sr
            self.sr = None
        # print("{}: sr stopped:{}".format(self.__id, r))
        print("识别结束")
        self.isRecognizerReady = False

    # def sendAll(self, data):
    #     r = self.sr.start(aformat="pcm", ex={"hello": 123})
    #     # zip(*[iter([1, 2, 3, 4, 5, 6, 7, 8, 9])] * 3)  # returns [(1,2,3),(4,5,6),(7,8,9)]
    #     self.__slices = zip(*(iter(data),) * 640)
    #     for i in self.__slices:
    #         self.sr.send_audio(bytes(i))
    #         time.sleep(0.01)
    #
    #     r = self.sr.stop()
    #     print("{}: sr stopped:{}".format(self.__id, r))

    def test_on_start(self, message, *args):
        print("test_on_start:{}".format(message))
        # print("on_start")
        self.isRecognizerReady = True

    def test_on_error(self, message, *args):
        print("on_error args=>{}".format(message))

    def test_on_close(self, *args):
        print("on_close: args=>{}".format(args))
        # print("on_close")

    def test_on_result_chg(self, message, *args):
        print("test_on_chg:{}".format(message))

    # {"header":{"namespace":"SpeechRecognizer","name":"RecognitionCompleted","status":20000000,"message_id":"a2af623fbfe84539b80b8f685e45c6fe","task_id":"d722ee7ddd2c44b9b65111a7d624c0c1","status_text":"Gateway:SUCCESS:Success."},"payload":{"result":"测试运输","duration":1088}}
    def test_on_completed(self, message, *args):
        print("on_completed:args=>{} message=>{}".format(args, message))
        self.resultText = json.loads(message)["payload"]["result"]
        print(self.resultText)
        self.recognizer_callable(self.resultText)

#
# if __name__ == '__main__':
#     # 设置打开日志输出
#     nls.enableTrace(True)
#     filename = '/recordedFile.wav'
#     with open(filename, "rb") as f:
#         data = f.read()
#     frames = list(zip(*(iter(data),) * 640))
#     aliRecognizer = AliRecognizer(get_record_frames=(lambda: frames), is_finish=(lambda: True))
#     aliRecognizer.run()
#     keyboard.wait()

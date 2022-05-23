import json
import time
import threading
import keyboard
import nls

URL = "wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1"
AKID = ""
AKKEY = ""
APPKEY = ""


class AliRecognizer:
    SEND_INTERVAL = 0.1  # 秒
    already_send = 0
    isReady = False
    recognizer_callalbe = None  # 识别结果的回调函数

    def __init__(self, get_record_frames, is_finish, recognizer_callalbe=None):
        self.__id = '__id'
        self.sr = nls.NlsSpeechRecognizer(
            url=URL,
            akid=AKID,
            aksecret=AKKEY,
            appkey=APPKEY,
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
        self.recognizer_callalbe = recognizer_callalbe

    def __continue_send(self):
        while not self.isReady:
            time.sleep(0.01)
        frames = self.get_record_frames()
        print("send frames size:{}".format(len(frames)))
        while not self.is_finish() or len(frames) > self.already_send:
            ready_to_send_frames = frames[self.already_send:]
            print("self.already_send:" + str(self.already_send) + " ready_to_send_frames size:" + str(
                len(ready_to_send_frames)))

            for frame in ready_to_send_frames:
                self.send(frame)
                self.already_send += 1
                time.sleep(self.SEND_INTERVAL)
            frames = self.get_record_frames()
        # print("__continue_send finish")
        self.finish()

    def run(self):
        self.r = self.sr.start(aformat="pcm", ex={"hello": 123})
        self.already_send = 0
        threading.Thread(target=self.__continue_send).start()

    def send(self, data):
        # print("send data")
        self.sr.send_audio(bytes(data))

    def finish(self):
        self.r = self.sr.stop()
        # print("{}: sr stopped:{}".format(self.__id, r))
        print("识别结束")
        self.isReady = False

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
        self.isReady = True

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
        self.recognizer_callalbe(self.resultText)


if __name__ == '__main__':
    # 设置打开日志输出
    nls.enableTrace(True)
    filename = 'K:/3-WorkSpace/2-Python-Projects/Jhih_Ai_Assistant/src/recordedFile.wav'
    with open(filename, "rb") as f:
        data = f.read()
    frames = list(zip(*(iter(data),) * 640))
    aliRecognizer = AliRecognizer(get_record_frames=(lambda: frames), is_finish=(lambda: True))
    aliRecognizer.run()
    keyboard.wait()

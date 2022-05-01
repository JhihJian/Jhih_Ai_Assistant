import threading
import time
from datetime import datetime

import keyboard

from src.function.AliRecognizer import AliRecognizer
from src.function.RecoderVoice import RecordVoice
from src.function.XunfeiRecognizer import VoiceRecognizer

if __name__ == '__main__':
    recordVoice = RecordVoice()
    # 开始监听大写锁定键()
    keyboard.hook_key('caps lock', recordVoice.trick_hook_key)
    recognizer = AliRecognizer()
    # threading.Thread(target=recognizer.run).start()
    recognizer.run()
    
    recordVoice.on_recording = recognizer.send
    recordVoice.on_finish = recognizer.finish
    # print("resultText" + recognizer.resultText)
    time.sleep(0.5)
    # 阻塞进程
    keyboard.wait()
    print("主进程结束")

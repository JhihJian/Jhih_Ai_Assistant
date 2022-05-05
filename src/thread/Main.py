import threading
import time
from datetime import datetime

import keyboard

from src.function.AliRecognizer import AliRecognizer
from src.function.RecoderVoice import RecordVoice
from src.function.XunfeiRecognizer import VoiceRecognizer

if __name__ == '__main__':
    recognizer = AliRecognizer()

    recordVoice = RecordVoice(on_begin=recognizer.run, on_recording=recognizer.send, on_finish=recognizer.run)
    # 开始监听大写锁定键()
    keyboard.hook_key('caps lock', recordVoice.trick_hook_key)
    # 阻塞进程
    keyboard.wait()
    print("主进程结束")

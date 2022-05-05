import threading
import time
from datetime import datetime

import keyboard

from src.function.AliRecognizer import AliRecognizer
from src.function.RecoderVoice import RecordVoice
from src.function.XunfeiRecognizer import VoiceRecognizer

if __name__ == '__main__':
    recordVoice = RecordVoice()
    recognizer = AliRecognizer(recordVoice.get_record_frames, recordVoice.is_recoder_finish)
    recordVoice.on_begin = recognizer.run
    # 开始监听大写锁定键()
    keyboard.hook_key('caps lock', recordVoice.trick_hook_key)
    # 阻塞进程
    keyboard.wait()
    print("主进程结束")

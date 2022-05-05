import pyaudio
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

import keyboard

from src.function.AliRecognizer import AliRecognizer
from src.function.RecoderVoice import RecordVoice

Form, Window = uic.loadUiType("./../../asserts/Guyu-Assistant.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

# ----------------------------------
recordVoice = RecordVoice()
recognizer = AliRecognizer(recordVoice.get_record_frames, recordVoice.is_recoder_finish)
recordVoice.on_begin = recognizer.run
# 开始监听大写锁定键()
keyboard.hook_key('caps lock', recordVoice.trick_hook_key)
# ----------------------------------


app.exec()
# recordVoice.audio.terminate()
print("app.exec()")

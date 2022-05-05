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
print("recognizer begin")
recognizer = AliRecognizer()
audio = pyaudio.PyAudio()
recordVoice = RecordVoice(audio=audio, on_begin=recognizer.run, on_recording=recognizer.send,
                          on_finish=recognizer.finish, is_ready=recognizer.is_ready)
# 开始监听大写锁定键()
keyboard.hook_key('caps lock', recordVoice.trick_hook_key)
# ----------------------------------


app.exec()
print("app.exec()")

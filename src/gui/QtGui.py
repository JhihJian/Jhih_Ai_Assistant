import pyaudio
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

import keyboard

from src.function.AliRecognizer import AliRecognizer
from src.function.CapsLockMonitor import CapsLockMonitor
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


def begin_hook():
    recordVoice.beginRecordVoice()
    recognizer.run()


# 监听大写锁定键()
monitor = CapsLockMonitor(begin_event_hook=begin_hook,
                          finish_event_hook=recordVoice.finishRecordVoice)
monitor.run()

# ----------------------------------


app.exec()
# recordVoice.audio.terminate()
print("app.exec()")

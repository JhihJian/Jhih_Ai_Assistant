import pyaudio
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

import keyboard

from src.function.AliRecognizer import AliRecognizer
from src.function.CapsLockMonitor import CapsLockMonitor
from src.function.RecoderVoice import RecordVoice

Form, Window = uic.loadUiType("./../../asserts/Guyu-Assistant.ui")
images_path = "./../../asserts/images/"

app = QApplication([])
app.setQuitOnLastWindowClosed(False)
window = Window()
form = Form()
form.setupUi(window)

# create icon
icon = QIcon(images_path + "icon.png")
tray_icon = QIcon(images_path + "tray_icon.png")
app.setWindowIcon(icon)
# create tray
tray = QSystemTrayIcon()
tray.setIcon(tray_icon)
tray.setVisible(True)
# create menu
menu = QMenu()
action = QAction("I'm Guyu")
menu.addAction(action)

# add show option
show = QAction("Show Windows")
show.triggered.connect(window.show)
menu.addAction(show)

# add quit option
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

# form = Form()
# form.setupUi(window)
# window.show()
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

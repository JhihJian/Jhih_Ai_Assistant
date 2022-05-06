import pyaudio
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel

import keyboard

from src.function.AliRecognizer import AliRecognizer
from src.function.CapsLockMonitor import CapsLockMonitor
from src.function.RecoderVoice import RecordVoice


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Guyu Assistant")
        self.__create_lable_widget()
        self.__create_tray_menu()

    def __create_lable_widget(self):
        self.lable_widget = QLabel("Hello")
        font = self.lable_widget.font()
        font.setPointSize(30)
        self.lable_widget.setFont(font)
        self.lable_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setCentralWidget(self.lable_widget)

    def update_text(self, text):
        if not self.isActiveWindow():
            keyboard.write(text)
        self.lable_widget.setText(text)

    def __create_tray_menu(self):
        # ---------__create_tray_menu--------------------------
        # create icon
        icon = QIcon(images_path + "icon.png")
        self.setWindowIcon(icon)
        tray_icon = QIcon(images_path + "tray_icon.png")
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
        show.triggered.connect(self.show)
        menu.addAction(show)

        # add quit option
        quit = QAction("Quit")
        quit.triggered.connect(app.quit)
        menu.addAction(quit)

        # Add the menu to the tray
        tray.setContextMenu(menu)
        # ---------__create_tray_menu--------------------------


images_path = "./../../asserts/images/"

app = QApplication([])
app.setQuitOnLastWindowClosed(False)
window = MainWindow()
window.show()

recordVoice = RecordVoice()
recognizer = AliRecognizer(recordVoice.get_record_frames, recordVoice.is_recoder_finish,
                           recognizer_callalbe=window.update_text)


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

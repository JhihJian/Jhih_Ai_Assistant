from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel

import keyboard

from function.AliRecognizer import AliRecognizer
from function.CapsLockMonitor import CapsLockMonitor
from function.RecoderVoice import RecordVoice

import sys, os

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = 'jhih.guyu.1.0.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Guyu Assistant")
        self.__create_lable_widget()

    # def __create_quit_button(self):
    # self.quit_button = QButton()

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


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()

    # ---------__create_tray_menu--------------------------
    # create icon
    icon = QIcon(os.path.join(basedir, 'misc', 'window_icon.png'))
    window.setWindowIcon(icon)
    tray_icon = QIcon(os.path.join(basedir, 'misc', 'tray_icon.png'))
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
    tray.show()
    # ---------__create_tray_menu--------------------------

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

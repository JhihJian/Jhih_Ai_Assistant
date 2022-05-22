from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel

import keyboard

from function import Curl
from function.AliRecognizer import AliRecognizer
from function.CapsLockMonitor import CapsLockMonitor
from util.DbHelper import DbHelper
from function.QQSocket import MonitorQQFunction
from function.RecoderVoice import RecordVoice

import os

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = 'jhih.guyu.1.0.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


# 配置日志


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
    window.show()
    # --------------监听大写锁定键进行录音--------------
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

    # --------------监听QQ消息--------------------
    qq = MonitorQQFunction()
    qq.start()
    qq.send_message_to_all("嘀嘀嘀，谷雨上线")
    # --------------进行每日任务---------------
    from datetime import date

    db = DbHelper()
    if db.get_db_day() != date.today():
        # 进行每日任务
        if Curl.git_doc_is_online():
            msg = "每日任务：检查jhihjian.github.io博客，已完成，运行正常"
            qq.send_message(msg)
        else:
            msg = "每日任务：检查jhihjian.github.io博客，已完成，运行错误"
            qq.send_message(msg)

        # 完成每日任务
        db.update_db_day()

    app.exec()
    # recordVoice.audio.terminate()
    print("app.exec()")
    qq.send_message_to_all("嘀嘀嘀，谷雨下线")

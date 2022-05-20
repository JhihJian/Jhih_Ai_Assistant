from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel

import keyboard

import logging

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
    window.show()
    app.exec()
    print("test")

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel

import keyboard

import logging

import sys, os

from gui import page_chage

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = 'jhih.guyu.1.0.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class QTextEditLogger(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        # self.widget = QtWidgets.QPlainTextEdit(parent)
        # self.widget.setReadOnly(True)
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class MainWindow(page_chage.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Guyu Assistant")
        # 设置切换页面按钮
        self.pushButton.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(0)))
        self.pushButton_2.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(1)))
        self.pushButton_3.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(2)))

        # 日志基本配置
        log_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger("MainWindow")
        logger.setLevel(logging.DEBUG)
        # 文件日志输出
        fh = logging.FileHandler('example.log')
        fh.setFormatter(log_format)
        # 界面日志输出
        logTextBox = QTextEditLogger(self.LogTextArea)
        logTextBox.setFormatter(log_format)
        logTextBox.setLevel(logging.INFO)
        logger.addHandler(logTextBox)
        # 控制台日志输出
        ch = logging.StreamHandler()
        ch.setFormatter(log_format)
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)

        logger.info('程序已启动')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    print("test")

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel, QWidget

import keyboard

import logging

import sys, os

from util.DbHelper import DbHelper
from function.DisableWinFunction import DisableWinFunction
from gui import Ui_MainWindows
from gui.FunctionItem import FunctionItem
from gui.Ui_FuntionItem import Ui_FunctionItem
from gui.Ui_MainWindows import Ui_MainWindow

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


def logger_config(log_text_area):
    # 日志基本配置
    log_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger("MainWindow")
    logger.setLevel(logging.DEBUG)
    # 文件日志输出
    fh = logging.FileHandler('MainWindow.log')
    fh.setFormatter(log_format)
    # 界面日志输出
    log_text_box = QTextEditLogger(log_text_area)
    log_text_box.setFormatter(log_format)
    log_text_box.setLevel(logging.INFO)
    logger.addHandler(log_text_box)
    # 控制台日志输出
    ch = logging.StreamHandler()
    ch.setFormatter(log_format)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.info('程序已启动')


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Guyu Assistant")
        db = DbHelper()

        # 设置日志
        logger_config(self.LogTextArea)

        # 设置切换页面按钮
        self.pushButton.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(0)))
        self.pushButton_2.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(1)))
        self.pushButton_3.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(2)))

        # 添加function 列表
        disable_win_function_item = FunctionItem()
        disable_win_function_item.function_button.setText("禁用Win")
        self.functionListLayout.addWidget(disable_win_function_item)
        disable_win_function = DisableWinFunction()

        if db.get_str_by_key("DisableWinFunction_ISOPEN") == "FALSE":
            # 如果默认为关闭状态
            pass
        else:
            disable_win_function.start()

        disable_win_function_item.start_button.clicked.connect(disable_win_function.start)
        disable_win_function_item.quit_button.clicked.connect(disable_win_function.quit)

        def update_online_icon():
            if disable_win_function.isOnline():
                disable_win_function_item.offline_icon.setVisible(False)
                disable_win_function_item.start_button.setVisible(False)
                disable_win_function_item.online_icon.setVisible(True)
                disable_win_function_item.quit_button.setVisible(True)
            else:
                disable_win_function_item.online_icon.setVisible(False)
                disable_win_function_item.quit_button.setVisible(False)
                disable_win_function_item.offline_icon.setVisible(True)
                disable_win_function_item.start_button.setVisible(True)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(update_online_icon)
        self.timer.start()

        # 功能1 qq监听


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Guyu-Assistant")
    window = MainWindow()
    window.show()
    app_name = QApplication.applicationName()
    print(app_name)
    app.exec()
    print("test")

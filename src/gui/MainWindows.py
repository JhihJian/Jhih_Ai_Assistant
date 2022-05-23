from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel, QWidget

import keyboard

import logging

import sys, os

from util import AutomaticStartup
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


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Guyu Assistant")
        db = DbHelper()
        self.logger = logging.getLogger("MainWindow")

        # 设置日志
        self.logger_config(self.LogTextArea)

        # 设置切换页面按钮
        self.pushButton.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(0)))
        self.function_button.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(1)))
        self.log_button.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(2)))
        self.setting_button.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(3)))

        # 设置开机自启功能
        if db.get_str_by_key(AutomaticStartup.AUTO_RUN_DB_KEY) == str(True):
            self.auto_start_checkbox.setChecked(True)
        else:
            self.auto_start_checkbox.setChecked(False)

        def auto_run_state_changed():
            if self.auto_start_checkbox.isChecked():
                db.store_str_by_key(AutomaticStartup.AUTO_RUN_DB_KEY, str(True))
                AutomaticStartup.SetAppAutoRun(True)
            else:
                db.store_str_by_key(AutomaticStartup.AUTO_RUN_DB_KEY, str(False))
                AutomaticStartup.SetAppAutoRun(False)

        self.auto_start_checkbox.stateChanged.connect(auto_run_state_changed)

        # 添加function 列表
        disable_win_function_item = FunctionItem()
        disable_win_function_item.function_button.setText("禁用Win")
        self.functionListLayout.addWidget(disable_win_function_item)
        self.disable_win_function = DisableWinFunction()

        if db.get_str_by_key("DisableWinFunction_ISOPEN") == "FALSE":
            # 如果默认为关闭状态
            pass
        else:
            self.disable_win_function.start()

        disable_win_function_item.start_button.clicked.connect(self.disable_win_function.start)
        disable_win_function_item.quit_button.clicked.connect(self.disable_win_function.quit)

        def update_online_icon():
            if self.disable_win_function.isOnline():
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

    def logger_config(self, log_text_area):
        # 日志基本配置
        log_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.logger.setLevel(logging.DEBUG)
        # 文件日志输出
        fh = logging.FileHandler('MainWindow.log')
        fh.setFormatter(log_format)
        self.logger.addHandler(fh)
        # 界面日志输出
        log_text_box = QTextEditLogger(log_text_area)
        log_text_box.setFormatter(log_format)
        log_text_box.setLevel(logging.INFO)
        self.logger.addHandler(log_text_box)
        # 控制台日志输出
        ch = logging.StreamHandler()
        ch.setFormatter(log_format)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
        self.logger.info('程序已启动')

    # Quit App Event
    def closeEvent(self, event):
        self.disable_win_function.quit()
        self.logger.info("closeEvent:{}".format(event))


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Guyu-Assistant")
    window = MainWindow()
    window.show()
    app_name = QApplication.applicationName()

    ret = app.exec()
    sys.exit(ret)

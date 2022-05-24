import threading

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel, QWidget

import keyboard

import logging

import sys, os

from util import AppSetting, AutomaticStartup
from util.AutoUpdate import AutoUpdate
from util.DbHelper import DbHelper
from function.DisableWinFunction import DisableWinFunction
from gui.FunctionItem import FunctionItem
from gui.Ui_MainWindows import Ui_MainWindow


# try:
#     from ctypes import windll  # Only exists on Windows.
#
#     myappid = 'jhih.guyu.1.0.0'
#     windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
# except ImportError:
#     pass


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
        self.setWindowTitle(AppSetting.APP_NAME)
        self.db = DbHelper()
        self.logger = logging.getLogger(AppSetting.APP_LOG_NAME)

        # 设置日志
        self.logger_config(self.LogTextArea)

        # 设置切换页面按钮
        self.pushButton.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(0)))
        self.function_button.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(1)))
        self.log_button.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(2)))
        self.setting_button.clicked.connect((lambda: self.stackedWidget.setCurrentIndex(3)))
        # 设置版本label
        self.version_label.setText(AppSetting.APP_VERSION)
        # 设置自动更新
        auto_update = AutoUpdate()

        def checkUpdate():
            if auto_update.checkForUpdate():
                button_text = "立即升级{}".format(auto_update.release_version)
                self.version_update_button.setText(button_text)
                self.version_update_button.setVisible(True)
                self.check_update_button.setVisible(False)
            else:
                self.check_update_button.setEnabled(False)
                self.check_update_button.setText("已为最新版本")

        def updateApp():
            button_text = "升级{}中...".format(auto_update.release_version)
            self.version_update_button.setText(button_text)
            self.version_update_button.setEnabled(False)
            auto_update.updateApp()
            self.version_update_button.setEnabled(True)
            self.version_update_button.setVisible(False)
            self.check_update_button.setVisible(True)

        def runUpdateApp():
            threading.Thread(target=updateApp).start()

        self.version_update_button.setVisible(False)
        self.check_update_button.clicked.connect(checkUpdate)
        self.version_update_button.clicked.connect(runUpdateApp)

        # 设置开机自启功能
        if self.db.get_str_by_key(AutomaticStartup.AUTO_RUN_DB_KEY) == str(True):
            self.auto_start_checkbox.setChecked(True)
        else:
            self.auto_start_checkbox.setChecked(False)

        def auto_run_state_changed():
            if self.auto_start_checkbox.isChecked():
                self.db.store_str_by_key(AutomaticStartup.AUTO_RUN_DB_KEY, str(True))
                AutomaticStartup.SetAppAutoRun(True)
            else:
                self.db.store_str_by_key(AutomaticStartup.AUTO_RUN_DB_KEY, str(False))
                AutomaticStartup.SetAppAutoRun(False)

        self.auto_start_checkbox.stateChanged.connect(auto_run_state_changed)

        # 添加function 列表
        disable_win_function_item = FunctionItem()
        disable_win_function_item.function_button.setText("禁用Win")
        self.functionListLayout.addWidget(disable_win_function_item)
        self.disable_win_function = DisableWinFunction()

        if self.db.get_str_by_key("DisableWinFunction_ISOPEN") == "FALSE":
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
        log_file_path = os.path.join(os.path.dirname(sys.executable), AppSetting.APP_LOG_NAME + '.log')
        print(log_file_path)
        fh = logging.FileHandler(log_file_path)
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
        del self.db
        self.logger.info("close disable_win_function ...")

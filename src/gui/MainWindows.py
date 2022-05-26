import threading

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QAction, QCloseEvent
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow, QLabel, QWidget

import logging

from function.EveryDayFunction import EveryDayFuntion, isNewDay, libraryPageIsOnline
from function.FunctionController import FunctionController
from function.QQSocket import MonitorQQFunction
from util import AppSetting, AutomaticStartup, LoggerConfig
from util.AutoUpdate import AutoUpdate
from util.DbHelper import DbHelper
from function.DisableWinFunction import DisableWinFunction
from gui.FunctionItem import FunctionItem
from gui.Ui_MainWindows import Ui_MainWindow
from concurrent.futures import ThreadPoolExecutor


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

    def __init__(self, quit_app_hook):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(AppSetting.APP_NAME)
        # 设置日志
        log_text_box = QTextEditLogger(self.LogTextArea)
        self.logger = LoggerConfig.logger_config(log_text_box)
        self.logger.info("init MainWindow")

        self.quit_app_hook = quit_app_hook
        # 设置线程池
        executor = ThreadPoolExecutor(max_workers=10)

        # 设置数据库
        self.db = DbHelper()

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

        def quit_app():
            closing = QCloseEvent()
            self.closeEvent(closing)
            self.quit_app_hook()

        def updateApp():
            button_text = "升级{}中...".format(auto_update.release_version)
            self.version_update_button.setText(button_text)
            self.version_update_button.setEnabled(False)
            auto_update.updateApp(quit_app)
            self.version_update_button.setEnabled(True)
            self.version_update_button.setVisible(False)
            self.check_update_button.setVisible(True)

        self.version_update_button.setVisible(False)
        self.check_update_button.clicked.connect(checkUpdate)
        self.version_update_button.clicked.connect(updateApp)

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

        # 函数控制器
        self.function_controller = FunctionController()
        self.function_controller.start()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        interval_functions = []

        def interval_updates():
            for function in interval_functions:
                function()

        self.timer.timeout.connect(interval_updates)

        # 添加function 列表

        # # 禁用Win
        disable_win_function_item = FunctionItem()
        disable_win_function_item.function_button.setText("禁用Win")
        self.functionListLayout.addWidget(disable_win_function_item)
        self.disable_win_function = DisableWinFunction(self.function_controller)

        if self.db.get_str_by_key("DisableWinFunction_ISOPEN") == "FALSE":
            # 如果默认为关闭状态
            pass
        else:
            self.disable_win_function.start()

        disable_win_function_item.start_button.clicked.connect(self.disable_win_function.start)
        disable_win_function_item.quit_button.clicked.connect(self.disable_win_function.quit)

        def update_disable_win_function():
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

        interval_functions.append(update_disable_win_function)

        # # QQ监听
        qq_monitor_function_item = FunctionItem()
        qq_monitor_function_item.function_button.setText("QQ监听")
        self.functionListLayout.addWidget(qq_monitor_function_item)
        self.qq_monitor_function = MonitorQQFunction(self.function_controller)

        if self.db.get_str_by_key("MonitorQQFunction_ISOPEN") == "FALSE":
            # 如果默认为关闭状态
            pass
        else:
            self.qq_monitor_function.start()

        qq_monitor_function_item.start_button.clicked.connect(self.qq_monitor_function.start)
        qq_monitor_function_item.quit_button.clicked.connect(self.qq_monitor_function.quit)

        def update_qq_monitor_function():
            if self.qq_monitor_function.isOnline():
                qq_monitor_function_item.offline_icon.setVisible(False)
                qq_monitor_function_item.start_button.setVisible(False)
                qq_monitor_function_item.online_icon.setVisible(True)
                qq_monitor_function_item.quit_button.setVisible(True)
            else:
                qq_monitor_function_item.online_icon.setVisible(False)
                qq_monitor_function_item.quit_button.setVisible(False)
                qq_monitor_function_item.offline_icon.setVisible(True)
                qq_monitor_function_item.start_button.setVisible(True)

        interval_functions.append(update_qq_monitor_function)

        # #每日任务
        if isNewDay(self.db):
            diary_functions = [libraryPageIsOnline]
            ed = EveryDayFuntion(self.function_controller, diary_functions)
            ed.start()
        self.timer.start()

    # Quit App Event
    def closeEvent(self, event):
        self.disable_win_function.quit()
        self.qq_monitor_function.quit()

        # 直接退出时 没报 connection is CLOSED，关闭任务时有
        self.function_controller.stop()
        del self.db
        self.logger.info("close disable_win_function ...")

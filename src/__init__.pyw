import logging
import multiprocessing
import os
import sys
import threading
import time
from multiprocessing import Process

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QCloseEvent

from gui.MainWindows import MainWindow
from util import AppSetting
from util.RunBat import runBat


def quit_app():
    app.shutdown()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication([])
    app.setApplicationName(AppSetting.APP_NAME)
    app.setApplicationVersion(AppSetting.APP_VERSION)
    window = MainWindow(quit_app)
    window.show()
    app_name = QApplication.applicationName()
    ret = app.exec()
    sys.exit(ret)

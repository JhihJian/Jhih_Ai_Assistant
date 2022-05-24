import sys

from PySide6.QtWidgets import QApplication

from gui.MainWindows import MainWindow
from util import AppSetting

if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName(AppSetting.APP_NAME)
    app.setApplicationVersion(AppSetting.APP_VERSION)
    window = MainWindow()
    window.show()
    app_name = QApplication.applicationName()
    ret = app.exec()
    sys.exit(ret)

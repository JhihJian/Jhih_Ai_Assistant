import logging

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

AUTO_RUN = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
AUTO_RUN_DB_KEY = "AUTO_RUN"


def SetAppAutoRun(is_auto_run):
    # settings = QSettings("HKEY_CURRENT_USER\\Software\\Microsoft\\Office", QSettings.NativeFormat)
    logger = logging.getLogger("MainWindow")
    app_name = QApplication.applicationName()
    settings = QSettings(AUTO_RUN, QSettings.NativeFormat)
    app_path = QApplication.applicationFilePath().replace("/", "\\")
    if is_auto_run:
        settings.setValue(app_name, app_path)
        logger.info("设置注册表,app name:{},app path:{}".format(app_name, app_path))
    else:
        settings.remove(app_name)
        logger.info("移除注册表,app name:{},app path:{}".format(app_name, app_path))


if __name__ == '__main__':
    logger = logging.getLogger("MainWindow")
    app_name = "test_app_name"
    settings = QSettings(AUTO_RUN, QSettings.NativeFormat)
    app_path = "D:\\test.exe"
    # settings.setValue(app_name, app_path)
    print("设置注册表,app name:{},app path:{}".format(app_name, app_path))
    v = settings.value("BaiduYunDetect")  # returns "Milkyway"
    print(v)

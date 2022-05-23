import logging

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

AUTO_RUN = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
AUTO_RUN_DB_KEY = "AUTO_RUN"


def SetAppAutoRun(is_auto_run):
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
    SetAppAutoRun(True)

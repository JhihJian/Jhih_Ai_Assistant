import logging

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

AUTO_RUN = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"


def SetAppAutoRun():
    logger = logging.getLogger("MainWindow")
    app_name = QApplication.applicationName()
    settings = QSettings(AUTO_RUN, QSettings.NativeFormat)
    app_path = QApplication.applicationFilePath().replace("/", "\\")
    logger.info("设置注册表,app name:{},app path:{}".format(app_name, app_path))
    settings.setValue(app_name, app_path)


if __name__ == '__main__':
    SetAppAutoRun()

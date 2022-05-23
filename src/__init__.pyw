import logging
import sys

from PySide6.QtWidgets import QApplication

import os

from gui.MainWindows import MainWindow

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = 'jhih.guyu.1.0.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Guyu-Assistant")
    app.setApplicationVersion("1.0.0")
    logging.getLogger("MainWindow").info(sys.argv)

    window = MainWindow()
    window.show()
    logging.getLogger("MainWindow").info(sys.argv)
    app_name = QApplication.applicationName()
    ret = app.exec()
    sys.exit(ret)

    # --------------进行每日任务---------------
    # from datetime import date
    #
    # db = DbHelper()
    # if db.get_db_day() != date.today():
    #     # 进行每日任务
    #     if Curl.git_doc_is_online():
    #         msg = "每日任务：检查jhihjian.github.io博客，已完成，运行正常"
    #         qq.send_message(msg)
    #     else:
    #         msg = "每日任务：检查jhihjian.github.io博客，已完成，运行错误"
    #         qq.send_message(msg)
    #
    #     # 完成每日任务
    #     db.update_db_day()
    #
    # app.exec()
    # # recordVoice.audio.terminate()
    # print("app.exec()")
    # qq.send_message_to_all("嘀嘀嘀，谷雨下线")

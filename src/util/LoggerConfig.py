import logging
import os
import sys

# TODO这里不好

from util import AppSetting


def logger_config(log_text_box):
    logger = logging.getLogger(AppSetting.APP_LOG_NAME)
    # 日志基本配置
    log_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)
    # 文件日志输出
    log_file_path = os.path.join(os.path.dirname(sys.executable), AppSetting.APP_LOG_NAME + '.log')
    fh = logging.FileHandler(log_file_path)
    fh.setFormatter(log_format)
    logger.addHandler(fh)
    # 界面日志输出
    if log_text_box:
        log_text_box.setFormatter(log_format)
        log_text_box.setLevel(logging.INFO)
        logger.addHandler(log_text_box)
    # 控制台日志输出
    ch = logging.StreamHandler()
    ch.setFormatter(log_format)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.info('程序已启动')
    return logger

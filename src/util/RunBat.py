import logging
import os
from datetime import datetime

from util import AppSetting
import subprocess


def runBat(filepath):
    # print("run bat begin on:{}".format(datetime.now()))
    return subprocess.Popen(filepath, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    # print("run bat pid:{} on:{}".format(p.pid, datetime.now()))
    # os.system('{}'.format(filepath))

import asyncio
import time
import unittest

from function.EveryDayFunction import *
from function.FunctionController import FunctionController
from util import LoggerConfig
from util.DbHelper import *


class Test_EveryDayFunction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        LoggerConfig.logger_config(None)

    def setUp(self):
        print("setUp start")

        DbHelper.DB_NAME = "test-db"
        self.db = DbHelper()
        print("setUp finish")

    def tearDown(self):
        print("setUp tearDown")

        self.db.test_del_db()
        print("tearDown finish")

    def test_isNewDay_True(self):
        self.assertEqual(True, isNewDay(self.db))

    #
    def test_isNewDay_False(self):
        self.db.store_str_by_key(LAST_RUN_DAY_KEY, str(date.today()))
        self.assertEqual(False, isNewDay(self.db))

    def test_EveryDayFuntion(self):
        do_job_finish = []

        def doJob():
            do_job_finish.append(True)

        fc = FunctionController()
        fc.start()

        ed = EveryDayFuntion(fc, [doJob])
        ed.start()

        fc.stop()

        self.assertEqual(True, do_job_finish[0])

    def test_EveryDayFuntion_async(self):
        do_job_finish = []

        async def doJob():
            print("do job start")
            do_job_finish.append(True)
            await asyncio.sleep(1)
            print("do job finish")

        fc = FunctionController()
        fc.start()

        ed = EveryDayFuntion(fc, [doJob])
        ed.start()
        while ed.function_status != FunctionStatus.STOP:
            time.sleep(0.5)
        fc.stop()
        self.assertEqual(True, do_job_finish[0])

    def test_libraryPageIsOnline(self):
        if asyncio.iscoroutinefunction(libraryPageIsOnline):
            self.assertEqual(True, asyncio.run(libraryPageIsOnline()))

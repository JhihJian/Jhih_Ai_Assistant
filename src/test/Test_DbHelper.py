import unittest

import function.DbHelper
from function.DbHelper import DbHelper


class Test_DbHelper(unittest.TestCase):
    def setUp(self):
        self.db_name = function.DbHelper.DB_NAME = "test_db"
        self.db = DbHelper()
        print("before test")

    def tearDown(self):
        self.db.__del__()
        DbHelper.test_del_db(self.db_name)
        print("after test")

    def test_jj_score(self):
        self.assertEqual(0, self.db.get_jj_score())
        self.assertEqual("", self.db.get_jj_score_reasons())
        self.db.update_jj_score(1, "test add 1")
        self.assertEqual(1, self.db.get_jj_score())
        self.assertEqual("test add 1\n", self.db.get_jj_score_reasons())
        self.db.update_jj_score(2, "test add 2")
        self.assertEqual(3, self.db.get_jj_score())
        self.assertEqual("test add 1\ntest add 2\n", self.db.get_jj_score_reasons())


if __name__ == '__main__':
    unittest.main()

import unittest

from function.MessageHandle import MessageHandle
from util import LoggerConfig
from util.DbHelper import DbHelper


class Fake_Websockets:
    def __init__(self):
        self.send_ids = []
        self.send_messages = []

    def send_message(self, target_id, message):
        self.send_ids.append(target_id)
        self.send_messages.append(message)


class Test_MessageHandle(unittest.TestCase):
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

    def test_notFoundFunction(self):
        websockets = Fake_Websockets()
        message_handle = MessageHandle(websockets)
        message_handle.mainEntry(980858153, "1")
        self.assertEqual(980858153, websockets.send_ids[0])
        self.assertEqual("没发现对应功能", websockets.send_messages[0])

    def test_queryScore(self):
        websockets = Fake_Websockets()
        message_handle = MessageHandle(websockets)
        message_handle.mainEntry(980858153, "查询分数")
        self.assertEqual(980858153, websockets.send_ids[0])
        self.assertEqual("当前仔仔分数:0\r\n当前健健分数:0", websockets.send_messages[0])

    def test_functionDisplay(self):
        websockets = Fake_Websockets()
        message_handle = MessageHandle(websockets)
        message_handle.mainEntry(980858153, "功能列表")
        self.assertEqual(980858153, websockets.send_ids[0])
        self.assertEqual("功能列表:\n\r1. 查询分数.\n\r2. 计时提醒.\n\r3. 事件提醒.\n\r", websockets.send_messages[0])

    def test_scoreTalk(self):
        websockets = Fake_Websockets()
        message_handle = MessageHandle(websockets)
        message_handle.mainEntry(980858153, "加分审核")
        self.assertEqual(980858153, websockets.send_ids[0])
        self.assertEqual("申请为自己增加多少分？", websockets.send_messages[0])
        message_handle.mainEntry(980858153, "0.1")
        self.assertEqual(980858153, websockets.send_ids[1])
        self.assertEqual("申请为自己加分原因？", websockets.send_messages[1])
        message_handle.mainEntry(980858153, "普普通通的原因")
        self.assertEqual(980858153, websockets.send_ids[2])
        self.assertEqual("正在发给对方审核确认，请稍等", websockets.send_messages[2])
        self.assertEqual(1600074410, websockets.send_ids[3])
        self.assertEqual("健健 申请增加分数 0.1 原因:普普通通的原因 请问是否同意?\r\n回复”同意“或”不同意“", websockets.send_messages[3])
        message_handle.mainEntry(1600074410, "同意")
        self.assertEqual(980858153, websockets.send_ids[4])
        self.assertEqual("对方已同意，加分成功", websockets.send_messages[4])
        self.assertEqual(0.1, self.db.get_jj_score())
        self.assertEqual("普普通通的原因\n", self.db.get_jj_score_reasons())

    def test_scoreTalk_refuse(self):
        websockets = Fake_Websockets()
        message_handle = MessageHandle(websockets)
        message_handle.mainEntry(980858153, "加分审核")
        self.assertEqual(980858153, websockets.send_ids[0])
        self.assertEqual("申请为自己增加多少分？", websockets.send_messages[0])
        message_handle.mainEntry(980858153, "0.1")
        self.assertEqual(980858153, websockets.send_ids[1])
        self.assertEqual("申请为自己加分原因？", websockets.send_messages[1])
        message_handle.mainEntry(980858153, "普普通通的原因")
        self.assertEqual(980858153, websockets.send_ids[2])
        self.assertEqual("正在发给对方审核确认，请稍等", websockets.send_messages[2])
        self.assertEqual(1600074410, websockets.send_ids[3])
        self.assertEqual("健健 申请增加分数 0.1 原因:普普通通的原因 请问是否同意?\r\n回复”同意“或”不同意“", websockets.send_messages[3])
        message_handle.mainEntry(1600074410, "不同意")
        self.assertEqual(980858153, websockets.send_ids[4])
        self.assertEqual("对方未同意，加分失败", websockets.send_messages[4])
        self.assertEqual(0, self.db.get_jj_score())
        self.assertEqual("", self.db.get_jj_score_reasons())


if __name__ == '__main__':
    unittest.main()

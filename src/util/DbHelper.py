import sys

import plyvel
import os
from datetime import date

ZZ_SCORE = "zz_score"
JJ_SCORE = "jj_score"
ADD_JJ_SCORE_REASONS = "add_jj_score_reasons"
ADD_ZZ_SCORE_REASONS = "add_zz_score_reasons"

DB_NAME = "guyu-db"


# 辅助进行db操作，单例
class DbHelper:
    def __init__(self):
        if not hasattr(DbHelper, "_first_init"):
            # 用basedir 报错，无法创建db

            self.db = plyvel.DB(os.path.join(os.path.dirname(sys.executable), DB_NAME), create_if_missing=True)
            DbHelper._first_init = True

    def __new__(cls):
        if not hasattr(DbHelper, "_instance"):
            DbHelper._instance = object.__new__(cls)
        return DbHelper._instance

    def get_str_by_key(self, key):
        result = self.db.get(key.encode())
        return result.decode() if result else ""

    def store_str_by_key(self, key, value):
        self.db.put(key.encode(), value.encode())

    # compare: today = date.today()
    def get_db_day(self):
        data = self.db.get(b'today')
        if data:
            db_date = date.fromisoformat(data.decode())
            return db_date
        else:
            return None

    def update_db_day(self):
        self.db.put(b'today', str(date.today()).encode())
        return True

    def __get_score(self, key):
        score = self.db.get(key.encode())
        return int.from_bytes(score, byteorder='big') if score else 0

    def __get_score_reasons(self, key):
        reasons = self.db.get(key.encode())
        return reasons.decode() if reasons else ""

    def __update_score(self, key_score, key_reasons, add_score, reason):
        # 更新分数
        score = self.db.get(key_score.encode())
        result_score = (int.from_bytes(score, byteorder='big') if score else 0) + add_score
        self.db.put(key_score.encode(), result_score.to_bytes(1, byteorder='big'))
        # 更新原因
        reason += '\n'
        pre_reasons = self.db.get(key_reasons.encode())
        pre_reasons = pre_reasons.decode() if pre_reasons else ""
        result_reasons = pre_reasons + reason
        self.db.put(key_reasons.encode(), result_reasons.encode())
        return True

    def get_jj_score(self):
        return self.__get_score(JJ_SCORE)

    def get_jj_score_reasons(self):
        return self.__get_score_reasons(ADD_JJ_SCORE_REASONS)

    def update_jj_score(self, add_score, reason):
        return self.__update_score(JJ_SCORE, ADD_JJ_SCORE_REASONS, add_score, reason)

    def get_zz_score(self):
        return self.__get_score(ZZ_SCORE)

    def get_zz_score_reasons(self):
        return self.__get_score_reasons(ADD_ZZ_SCORE_REASONS)

    def update_zz_score(self, add_score, reason):
        return self.__update_score(ZZ_SCORE, ADD_ZZ_SCORE_REASONS, add_score, reason)

    def __del__(self):
        self.db.close()

    def test_close(self):
        self.db.close()

    @classmethod
    def test_del_db(cls, db_name):
        plyvel.destroy_db(db_name)


# 单元测试
if __name__ == '__main__':
    db = DbHelper()
    db = DbHelper()
    db.update_db_day()
    print(db.get_db_day() == date.today())
    del db

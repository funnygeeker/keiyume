import os
import time as t
import threading

from core.sqlite import Sqlite
from . import config

plugin_path = os.path.dirname(__file__).replace("\\", "/")  # 自动获取当前插件所在的路径
lock = threading.RLock()


class DB:
    def __init__(self, path: str):
        self.path = path
        self.points_table_name = "points"
        self.history_table_name = "history"
        self.sql = Sqlite(path)
        self.sql.new(self.points_table_name, user_id='BIGINT', last_sign_in_date='BIGINT', points='BIGINT')
        self.sql.new(self.history_table_name, user_id='BIGINT', num='BIGINT', type='TEXT', event='TEXT', time='BIGINT')
        self.sql.close()

    def _create(self, user_id):
        """
        检查并创建用户
        """
        with lock:
            self.sql = Sqlite(self.path)
            if not self.sql.read('points', f'user_id={user_id}', 'last_sign_in_date'):
                self.sql.write('points', user_id=user_id, last_sign_in_date=0, points=config.start_points)

    def add(self, user_id: int, num, event='', time: int = None):
        """
        增加积分
        """
        with lock:
            self.sql = Sqlite(self.path)
            self._create(user_id)
            result = self.sql.read(self.points_table_name, f'user_id={user_id}', 'points')
            p = result[0][0] + num
            if p < 0:
                return False
            self.sql.update(self.points_table_name, condition=f'user_id={user_id}', points=p)
            if not time:
                time = int(t.time())
            self.write_history(user_id, num, 'add', event, time)
            self.sql.close()
            return True

    def reduce(self, user_id: int, num, event='', time: int = None):
        """
        减少积分
        """
        with lock:
            self.sql = Sqlite(self.path)
            self._create(user_id)
            result = self.sql.read(self.points_table_name, f'user_id={user_id}', 'points')
            p = result[0][0] - num
            if p < 0:
                return False
            self.sql.update(self.points_table_name, condition=f'user_id={user_id}', points=p)
            if not time:
                time = int(t.time())
            self.write_history(user_id, num, 'reduce', event, time)
            self.sql.close()
            return True

    def set(self, user_id: int, num, event='', time: int = None):
        """
        设置积分
        """
        with lock:
            self.sql = Sqlite(self.path)
            self._create(user_id)
            self.sql.update(self.points_table_name, condition=f'user_id={user_id}', points=num)
            if not time:
                time = int(t.time())
            self.write_history(user_id, num, 'set', event, time)
            self.sql.close()
            return True

    def query(self, user_id: int):
        """
        查询积分
        """
        with lock:
            self.sql = Sqlite(self.path)
            self._create(user_id)
            result = self.sql.read(self.points_table_name, f'user_id={user_id}', 'points')
            self.sql.close()
            return result[0][0]

    def write_history(self, user_id, num, type_, event, time):
        """
        写入历史记录
        """
        with lock:
            self.sql = Sqlite(self.path)
            self.sql.write(self.history_table_name, user_id=user_id, num=num, type=type_, event=event, time=time)
            self.sql.close()
            return True

    def read_history(self, user_id, num):
        """查询最近的几条积分历史记录

        Returns:
            List[Tuple[操作类型, 数量, 事件, 时间]]"""
        with lock:
            self.sql = Sqlite(self.path)
            self._create(user_id)
            result = self.sql.read(self.history_table_name, f"user_id={user_id} ORDER BY id DESC LIMIT {num}",
                                   'type', 'num', 'event', 'time')
            self.sql.close()
            return result

    def clear_history(self, num: int):
        """
        清除无效 QQ 号的数据，清理历史记录，保留历史记录中最新的 num 条数据

        Args:
            num: 保留的条数
        """
        with lock:
            self.sql = Sqlite(self.path)
            self.sql.cur.execute(f"DELETE FROM {self.points_table_name} WHERE user_id<=10000")
            self.sql.cur.execute(f"DELETE FROM {self.history_table_name} WHERE id NOT IN (SELECT id from"
                                 f" {self.history_table_name} ORDER BY id DESC LIMIT {num})")
            self.sql.commit()
            self.sql.close()

    def read_last_sign_in_date(self, user_id):
        with lock:
            self.sql = Sqlite(self.path)
            self._create(user_id)
            result = self.sql.read('points', f'user_id={user_id}', 'last_sign_in_date')[0][0]
            self.sql.close()
            return result

    def write_last_sign_in_date(self, user_id, last_sign_in_date):
        with lock:
            self.sql = Sqlite(self.path)
            self._create(user_id)
            self.sql.update('points', f'user_id={user_id}', last_sign_in_date=last_sign_in_date)
            self.sql.close()

import json
from typing import Optional, List

from core.sqlite import Sqlite
from plugins.keiyume_helper import config


class DB:
    def __init__(self, path: str):
        self.path = path
        self.msg_table_name = "msg"
        self.sql = Sqlite(path)
        self.sql.new(self.msg_table_name, data='JSON', group_id='BIGINT', user_id='BIGINT', time='BIGINT',
                     message_id='BIGINT', del_msg='INT')
        self.sql.close()

    def read_msg(self, num: int, group_id: Optional[int] = None, user_id: Optional[int] = None,
                 del_msg: bool = False) -> List[dict]:
        """
        读取数据库中的历史消息

        Args:
            num: 读取的条数
            group_id: 群聊 ID
            user_id: 用户 ID
            del_msg: 消息是否已经被撤回

        Returns:
            列表[字典]
        """
        with config.lock:
            self.sql = Sqlite(self.path)
            if user_id and group_id:
                condition = f" AND user_id={user_id} AND group_id={group_id}"
            elif user_id:
                condition = f" AND user_id={user_id}"
            elif group_id:
                condition = f" AND group_id={group_id}"
            else:
                condition = ""
            if del_msg:
                del_msg = "NOT "
            else:
                del_msg = ""
            result = self.sql.read(self.msg_table_name,
                                   f"del_msg IS {del_msg}NULL{condition} ORDER BY time DESC LIMIT {num}", 'data')
            self.sql.close()
            result_ = []
            for _ in result:
                result_.append(json.loads(_[0]))
        return result_

    def write_msg(self, data: dict) -> None:
        """
        向数据库写入历史消息
        （不包括元事件）

        Args:
            data: 原始消息
        """
        if data.get('post_type') == 'message':
            with config.lock:
                self.sql = Sqlite(self.path)
                group_id = data.get("group_id", None)
                user_id = data.get("user_id", None)
                self.sql.write(self.msg_table_name, data=json.dumps(data, indent=4, ensure_ascii=False),
                               group_id=group_id,
                               user_id=user_id, time=data['time'], message_id=data['message_id'])
                self.sql.close()

    def clear_msg(self, num: int):
        """
        清理数据库，保留数据库中最新的 num 条数据

        Args:
            num: 保留的条数
        """
        with config.lock:
            self.sql = Sqlite(self.path)
            self.sql.cur.execute(f"DELETE FROM {self.msg_table_name} WHERE time NOT IN (SELECT time from"
                                 f" {self.msg_table_name} ORDER BY time DESC LIMIT {num})")
            self.sql.commit()
            self.sql.close()

    def write_del_msg(self, message_id: int) -> None:
        """
        向数据库写入已撤回的消息 ID
        （不包括元事件）

        Args:
            message_id: 被撤回的消息 ID
        """
        with config.lock:
            self.sql = Sqlite(self.path)
            self.sql.update(self.msg_table_name, condition=f'message_id={message_id}', del_msg=1)
            self.sql.close()

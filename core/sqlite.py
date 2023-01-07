# -*- coding : utf-8-*-
# 溪梦框架：core/sqlite.py
# 简化后的数据库调用模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume
#
# 参考资料：
# CSDN - Python3 操作 sqlite3 查询数据、插入数据、更新数据、删除数据：https://blog.csdn.net/weixin_55488930/article/details/123437574


import os
import sqlite3
from typing import Optional, Any, List


class Sqlite:
    def __init__(self, database: str) -> None:
        """
        连接数据库

        Args:
            database: 数据库文件路径（字符串）

        Returns:
            None

        Example:
            sql = Sqlite(path = './test.db')
        """
        if not os.path.exists(os.path.dirname(database)):  # 若不存在路径，则自动创建
            os.makedirs(os.path.dirname(database))
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

    def new(self, table_name: str, **kwargs: Any) -> None:
        """
        新建数据表
        如果数据表不存在时新建（数据表含有id列）

        Args:
            table_name: 创建的数据表的名字（字符串）
            kwargs:
                column_name: 字段名（字段名）
                data_type:
                    INT:整数值
                    BIGINT:极大整数值
                    BLOB:二进制数据
                    TEXT:文本数据

        Returns:
            None

        Example:
            sql.new('数据表表名', info1 = 'INT', info2 = 'TEXT')
            sql.new('数据表表名', **{'info1': 'INT', 'info2': 'TEXT'})
        """
        execute = ''
        for key, value in kwargs.items():
            execute += f", {key} {value}"
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS `{table_name}` (
            id INTEGER PRIMARY KEY{execute})""")
        self.conn.commit()

    def read(self, table_name: str, condition: Optional[str] = '1', *args) -> List[tuple]:
        """
        根据条件查询数据库内容

        条件语句参考资料：https://blog.csdn.net/csucsgoat/article/details/115357650

        Args:
            table_name: 数据表表名（字符串）
            condition: 条件语句（字符串）
            args: 可选，需要查询的列名

        Returns:
            List: 查询结果（列表）

        Example:
            sql.read('数据表表名', 'id = 1' ,'info1', 'info2')
            sql.read('数据表表名', 'id = 1' ,*('info1', 'info2'))
        """
        if args == ():
            str_ = '*'
        else:
            str_ = ", ".join(args)
        return self.cur.execute(f"SELECT {str_} FROM `{table_name}` WHERE {condition}").fetchall()

    def write(self, table_name: str, commit: Optional[bool] = True, **kwargs: Any) -> None:
        """
        向数据库中新写入一行数据

        Args:
            table_name: 数据表名（字符串）
            commit: 是否提交（布尔值），批量写入建议全部更改完再提交
            kwargs: 可变参数：列名 数据（任意）

        Example:
            sql.write('数据表表名', info1 = '数据1', info2 = '数据2')
            sql.write('数据表表名', **{'info1': '测试', 'info2': '测试2'})
        """
        str_ = len(kwargs) * ", ?"
        self.cur.execute(
            f"REPLACE INTO `{table_name}` (id, {', '.join(kwargs.keys())}) VALUES(NULL{str_})", tuple(kwargs.values()))
        if commit:
            self.conn.commit()

    def delete(self, table_name: str, condition: str = '1', commit: Optional[bool] = True) -> None:
        """
        根据条件删除数据库内容

        Args:
            table_name: 数据表名（字符串）
            condition: 删除条件（字符串）
            commit: 是否提交（布尔值），批量删除建议全部更改完再提交

        Returns:
            None

        Example:
            sql.delete('数据表表名', 'info1="测试"')
        """
        self.cur.execute(f"DELETE FROM `{table_name}` WHERE {condition}")
        if commit:
            self.conn.commit()

    def update(self, table_name: str, condition: Optional[str] = '1', commit: Optional[bool] = True,
               **kwargs: Any) -> None:
        """
        根据条件更新数据库内容

        Args:
            table_name: 数据表名（字符串）
            condition: SQL语句条件（字符串），默认为全部
            kwargs: 可变参数：列名 数据（任意）
            commit: 是否提交（布尔值），批量写入建议全部更改完再提交

        Example:
            sql.update('数据表表名', info1 = "测试2")
            sql.update('数据表表名', {info1: "测试2"})
        """
        str_ = ''
        for key in kwargs.keys():
            str_ += f", {key} = ?"
        self.cur.execute(
            f"UPDATE `{table_name}` SET {str_.lstrip(', ')} WHERE {condition}", tuple(kwargs.values()))
        if commit:
            self.conn.commit()

    def auto_write(self, table_name: str, condition: Optional[str] = '', **kwargs) -> None:
        """
        根据条件智能写入数据库内容
        不存在则插入，存在则更新

        Args:
            table_name: 数据表名（字符串）
            condition: SQL语句条件（字符串），默认为全部
            kwargs: 可变参数：列名 数据（任意）

        Returns:
            None

        Example:
            sql.auto_write('数据表表名', 'id=2', info2 = "测试3")
            sql.auto_write('数据表表名', 'id=2', {info2: "测试3"})
        """
        result = self.read(table_name=table_name, condition=condition)
        if len(result) >= 1:
            self.update(table_name=table_name, condition=condition, **kwargs)
        elif len(result) == 0:
            self.write(table_name=table_name, **kwargs)

    def commit(self):
        """
        提交对数据库的更改

        示例：
            sql.commit()
        """
        self.conn.commit()

    def rollback(self):
        """
        撤销上次对数据库提交的更改

        示例：
            sql.rollback()
        """
        self.conn.rollback()

    def close(self):
        """
        断开与数据库的连接

        示例：
            sql.close()
        """
        self.conn.close()


if __name__ == '__main__':
    sql = Sqlite('./test.db')
    print('---- 新建表 ----')
    sql.new('数据表表名', **{'info1': 'INT', 'info2': 'TEXT'})
    print('---- 写入表 ----')
    sql.write('数据表表名', info1="测试")
    print(sql.read('数据表表名', 'info1="测试" OR id=1', *('info1', 'info2')))
    print(sql.read('数据表表名', 'info1="测试" OR id=1', 'info1'))
    print('---- 更新表 ----')
    sql.update('数据表表名', info1="测试2")
    print(sql.read('数据表表名'))
    print('---- 智能写入 ----')
    sql.auto_write('数据表表名', 'id=2', info2="测试3")
    print(sql.read('数据表表名'))
    sql.commit()
    sql.close()

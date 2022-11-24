#!/usr/bin/python3
# -*- coding: utf-8 -*-
# keiyume_2.0.0-beta.2
# 溪梦框架数据库模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker
# Python SQLite教程：https://blog.csdn.net/weixin_55488930/article/details/123437574
import sqlite3
from typing import Optional, Any, List


class Sqlite:
	# TODO: 应有__init__方法，用于初始化数据库连接
	def connect(self, file_path: str) -> None:
		"""连接数据库

		Args:
			file_path: 数据库文件路径（字符串）

		Returns:
			None

		Example:
			>>> Sqlite.connect(file_path = './data/test.db')
		"""
		self.conn = sqlite3.connect(file_path)
		self.cur = self.conn.cursor()

	def new(self, table_name: str, **kwargs: Any):
		"""新建数据表

		如果数据表不存在时新建（数据表含有id列）

		Args:
			table_name: 数据表名（字符串）
			kwargs:
				column_name: 字段名（字段名）
                data_type:
					INT:大整数值
					BIGINT:极大整数值
					BLOB:二进制数据
					TEXT:长文本数据

		Returns:
			None

		Example:
			>>> Sqlite.new(table_name = '数据表表名', info1 = 'INT', info2 = 'TEXT')
			>>> Sqlite.new(table_name = '数据表表名', **{'info1': 'INT', 'info2': 'TEXT'})
		"""
		execute = ''
		for key, value in kwargs.items():
			execute += f",{key} {value}"
		self.cur.execute(f"""CREATE TABLE IF NOT EXISTS `{table_name}` (
            id INTEGER PRIMARY KEY{execute})""")
		self.conn.commit()

	def read(self, table_name: str, keys: Optional[str] = '*', condition: Optional[str] = '1=1') -> List:
		"""根据条件查询数据库内容

		Args:
			table_name: 数据表名（字符串）
			keys: 查询的列名（列表）
			condition: 查询条件（字符串）

		Returns:
			List: 查询结果（列表）

		Example:
			>>> Sqlite.read(table_name = '数据表表名', keys = ['info1', 'info2'], condition = 'id = 1')
		"""
		if keys != '*':
			str_ = ''
			for key in keys:
				str_ += f", {key}"
			str_ = str_.lstrip(', ')
		else:
			str_ = '*'
		return self.cur.execute(f"SELECT {str_} FROM `{table_name}` WHERE {condition}").fetchall()

	def write(self, table_name: str, commit: Optional[bool] = True, **kwargs: Any) -> None:
		"""向数据库中新写入一行
		
		Args:
			table_name: 数据表名（字符串）
			commit: 是否提交（布尔值），批量写入建议全部更改完再提交
			kwargs: 可变参数：列名 数据（任意）
				
		Example:
			>> Sqlite.write(table_name = '数据表表名', info1 = '数据1', info2 = '数据2')
			>> Sqlite.write(table_name = '数据表表名', **{'info1': '测试', 'info2': '测试2'})
		"""
		key_ = ''
		str_ = len(kwargs) * ", ?"
		list_ = []
		for key, value in kwargs.items():
			key_ += f",{key}"
			list_.append(value)
		self.cur.execute(
			F"REPLACE INTO `{table_name}` (id{key_}) VALUES(NULL{str_})", list_)
		if commit:
			self.conn.commit()

	def delete(self, table_name: str, condition: str = '1=1') -> None:
		"""根据条件删除数据库内容

		Args:
			table_name: 数据表名（字符串）
			condition: 删除条件（字符串）

		Returns:
			None

		Example:
			>> Sqlite.delete(table_name = '数据表表名', condition = 'info1="测试"')
		"""
		self.cur.execute(f"DELETE FROM `{table_name}` WHERE {condition}")
		self.conn.commit()

	def update(self, table_name: str, condition: Optional[str] = '1=1', **kwargs: Any) -> None:
		"""根据条件更新数据库内容

		Args:
			table_name: 数据表名（字符串）
			condition: SQL语句条件（字符串），默认为全部
			kwargs: 可变参数：列名 数据（任意）

		Returns:
			None

		Example:
			>> Sqlite.update(table_name = '数据表表名', condition = '1=1', info1 = "测试2")
			>> Sqlite.update(table_name = '数据表表名', condition = '1=1', {info1: "测试2"})
		"""
		str_ = ''
		list_ = []
		for key, value in kwargs.items():
			str_ += f", {key} = ?"
			list_.append(value)
		str_ = str_.lstrip(', ')
		self.cur.execute(
			f"UPDATE `{table_name}` SET {str_} WHERE {condition}", list_)
		self.conn.commit()

	def auto_write(self, table_name: str, condition: Optional[str] = '1=1', **kwargs) -> None:
		"""根据条件智能写入数据库内容

		不存在则插入，存在则更新

		Args:
			table_name: 数据表名（字符串）
			condition: SQL语句条件（字符串），默认为全部
			kwargs: 可变参数：列名 数据（任意）

		Returns:
			None

		Example:
			>> Sqlite.auto_write(table_name = '数据表表名', condition = 'id=2', info2 = "测试3")
			>> Sqlite.auto_write(table_name = '数据表表名', condition = 'id=2', {info2: "测试3"})
		"""
		result = self.read(table_name=table_name, condition=condition)
		if len(result) >= 1:
			self.update(table_name=table_name,
			            condition=condition, **kwargs)
		elif len(result) == 0:
			self.write(table_name=table_name, **kwargs)

	def commit(self):
		"""
		提交对数据库的更改
		示例：
			sql.commit()
		"""
		self.conn.commit()

	def close(self):
		"""
		断开与数据库的连接
		示例：
			sql.close()
		"""
		self.conn.close()


if __name__ == '__main__':
	sql = Sqlite()
	sql.connect('./test.db')
	print('---- 新建表 ----')
	sql.new(table_name='数据表表名', **{'info1': 'INT', 'info2': 'TEXT'})
	print('---- 写入表 ----')
	sql.write(table_name='数据表表名', commit=True, info1="测试")
	print(sql.read(table_name='数据表表名', keys='info1', condition='info1="测试" OR id=1'))
	print('---- 更新表 ----')
	sql.update(table_name='数据表表名', condition='1=1', info1="测试2")
	print(sql.read(table_name='数据表表名'))
	print('---- 智能写入 ----')
	sql.auto_write(table_name='数据表表名', condition='id=2', info2="测试3")
	print(sql.read(table_name='数据表表名'))
	sql.commit()
	sql.close()

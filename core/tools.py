#!/usr/bin/python3
# -*- coding: utf-8 -*-
# keiyume_2.0.0-beta.2

# 溪梦框架工具模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832

# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker

import json
import sys
import time
from typing import List, Optional, Any

from .log import *


class Tools:

	# DEL
	@staticmethod
	def to_json(data: dict) -> Any:
		"""将dict转换为json

		Args:
			data (dict): dict数据

		Returns:
			Any: json数据
		"""
		return json.dumps(data, ensure_ascii=False, indent=4)

	# DEL
	@staticmethod
	def match_in_list(search_list: list, text: str) -> bool:
		"""逐一匹配列表中的值是否包含在字符串中

		Arg:
			search_list (list): 匹配列表
			text (str): 待匹配字符串

		Returns:
			bool: 匹配结果
		"""
		for i in search_list:  # 逐一匹配列表
			if str(i) in str(text):  # 如果文本在列表中
				return True
		else:
			return False

	# DEL
	@staticmethod
	def str_to_dict(data: str) -> Any:
		"""将str数据转换为dict形式并记录日志

		Args:
			data (str): str数据

		Returns:
			Any: dict数据
        """
		logger.debug(data)  # 日志记录原始结果
		try:
			return json.loads(data)
		except Exception as e:
			logger.warning(Log.Get_Error())
			logger.error(e)

	# DEL
	@staticmethod
	def convert_format(text: str, mode: Optional[str] = 'int', key: Optional[str] = ' ') -> List:
		"""格式转换

		将字符串转换每隔一个key拆分为列表
		mode 表示返回列表中值的类型：str/int

		Args:
			text (str): 待转换字符串
			mode (Optional[str], optional): 返回列表中值的类型. Defaults to 'int'.
			key (Optional[str], optional): 拆分字符串的key. Defaults to ' '.

		Returns:
			List: 转换后的列表

		Example:
			>>> Tools.convert_format('1 2 3 4')
			[1, 2, 3, 4]
		"""
		if text == '':
			return []
		text_list = str(text).strip(key).split(key)  # 先转为str形式以防配置为单数值时为int形式导致报错，除去两端的空格后进行分隔
		if mode == 'int':
			return list(map(int, text_list))  # 将列表中的值转换回数字
		return text_list

	# DEL
	@staticmethod
	def progress_bar(text: str = '', sleep: float = 1.0) -> None:
		"""进度条

		Args:
			text (str, optional): 进度条前的文本. Defaults to ''.
			sleep (float, optional): 进度条刷新间隔. Defaults to 1.0.

		Returns:
			None
		"""
		for i in range(1, 51):
			print("\r", end="")
			print(f"{text} {i * 2}%: ", "▋" * (i // 2), end="")
			sys.stdout.flush()
			time.sleep(sleep)

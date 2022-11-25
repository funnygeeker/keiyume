#!/usr/bin/python3
# -*- coding: utf-8 -*-
# keiyume_2.0.0-beta.2

# 溪梦框架文本操作模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker

# 参考资料：
# Python读大型文本：https://blog.csdn.net/potato012345/article/details/88728709
# chardet文本编码检测：https://blog.csdn.net/tianzhu123/article/details/8187470

import os
from typing import List, Optional, Dict

try:
	import chardet  # 文件编码检测，需安装
except ImportError:
	print('>> 检测到缺少 chardet 库，正在安装...')
	os.system('pip3 install chardet')
	import chardet


class Text:
	"""文本管理模块

	包含:
		文本编码检测
		文本以列表形式读取
		判断文本中包含的内容
		文本文件存在性检查
	"""

	@staticmethod
	def detect_encoding(file_path: str) -> str:
		"""文本编码检测

		无法识别则默认为"utf-8"编码

		Args:
			file_path: 文本文件路径

		Returns:
			str: 文本编码
		"""
		with open(file_path, 'rb') as file:
			result = chardet.detect(file.read(1048576))  # 最多读取1MB文件进行检测
			# print(result['confidence'])#
			if float(result['confidence']) >= 0.5:  # 如果置信度大于50%
				return result['encoding'].lower()
			else:
				# 无法识别则默认为"utf-8"编码
				return 'utf-8'

	@staticmethod
	def read_file_as_list(file_path: str, choose: Optional[str] = '', choose_mode: Optional[int] = 0,
	                      read_mode: Optional[int] = 0,
	                      encoding: Optional[str] = '') -> List:
		"""读取文本文件并以列表的形式输出

		Args:
			file_path: 文本文件路径
			choose: 选择包含的内容
			choose_mode: 选择模式
				0: 选择包含的内容
				1: 选择不包含的内容
			read_mode: 读取模式
				0: 读取全部内容
				1: 读取包含的内容
				2: 读取不包含的内容
			encoding: 文本编码

		Returns:
			list: 文本内容列表
		"""
		if encoding == '':  # 如果没有文本编码参数，则自动识别编码
			encoding = Text.detect_encoding(file_path)
		with open(file_path, "r", encoding=encoding) as all_text:
			if choose == '':  # 如果不需要排除或选择某字符串开头的文本行
				text_list = [text.strip("\n")
				             for text in all_text if text.strip("\n") != ""]
			else:  # 如果需要排除或选择某字符串开头的文本行
				if choose_mode == 1:  # 选择模式
					if read_mode == 1:  # 选择模式，从后选取
						text_list = [text.strip("\n") for text in all_text if text.strip(
							"\n") != "" and text.strip("\n")[-len(choose):] == str(choose)]
					else:  # 选择模式，从前选取
						text_list = [text.strip("\n") for text in all_text if text.strip(
							"\n") != "" and text.strip("\n")[0:len(choose)] == str(choose)]
				else:  # 排除模式
					if read_mode == 1:  # 排除模式，从后选取
						text_list = [text.strip("\n") for text in all_text if text.strip(
							"\n") != "" and text.strip("\n")[-len(choose):] != str(choose)]
					else:  # 排除模式，从前选取
						text_list = [text.strip("\n") for text in all_text if text.strip(
							"\n") != "" and text.strip("\n")[0:len(choose)] != str(choose)]
		return text_list

	@staticmethod
	def read_file_as_text(file_path: str, encoding: Optional[str] = '') -> str:
		"""读取文本并返回字符串

		Args:
			file_path: 文本文件路径
			encoding: 文本编码

		Returns:
			str: 文本内容字符串
		"""
		if encoding == '':  # 如果没有文本编码参数，则自动识别编码
			encoding = Text.detect_encoding(file_path)
		with open(file_path, "r", encoding=encoding) as all_text:
			return ''.join(all_text)

	@staticmethod
	def check_file_if_exists(file_path: str, text_to_write: str = '', encoding: str = 'utf-8') -> bool:
		"""检查文本文件是否存在

		不存在则可创建并写入内容

		Args:
			file_path: 文本文件路径
			text_to_write: 写入的文本内容
			encoding: 文本编码

		Returns:
			bool: 文本文件是否存在
		"""
		if os.path.isfile("./settings.txt"):  # 如果文件存在
			return True
		elif text_to_write != '':  # 如果要写入的内容不为空
			with open(file_path, 'w', encoding=encoding) as file:
				file.write(str(text_to_write))
				return False
		else:
			# 文件既不存在也不需要写入内容
			return False

	@staticmethod
	def read_file_in_folder(folder_path: str, file_extension: Optional[str] = '.txt', list_count: Optional[int] = 100,
	                        choose: Optional[str] = '', chose_mode: Optional[int] = 0, read_mode: Optional[int] = 0,
	                        return_mode: Optional[str] = 'list',
	                        encoding: Optional[str] = '') -> Optional[Dict, List]:
		"""读取文件夹下的指定文件类型的内容并返回列表

		不支持匹配换行符

		Args:
			folder_path : 文件夹路径
			file_extension : 文件后缀
			list_count: 最大读取的文件数限制，默认100个
			choose: 选择或排除的字符串
			chose_mode:
				0: 排除模式
				1: 选择模式
			read_mode:
				0: 从行头选择
				1: 从行尾选择
			return_mode: 返回模式
				'list': 返回列表
				'dict': 返回字典
			encoding: 文本编码

		Returns:
			list: 文件夹下的指定文件类型的内容列表
			dict: 文件夹下的指定文件类型的内容字典
		"""
		if folder_path[-1] == '/':  # 文件夹路径合法化
			folder_path = folder_path[:-1]
		files_name = os.listdir(folder_path)  # 获取文件夹下的所有文件和文件夹名称
		text_list = []
		list_dict = {}
		cycle_count = 0  # 用于计算读取的有效行数
		file_extension = file_extension.lower()  # 扩展名变为小写形式
		for file_name in files_name:  # 遍历文件夹
			# 判断是否为需要读取的后缀
			if ((os.path.splitext(file_name)[1]).lower() == file_extension or file_extension == '*') and os.path.isfile(
					f'{folder_path}/{file_name}'):
				# 判断是否为文件，小写处理文件扩展名，确定是否为需要读取的文件，并进行读取
				file_data = Text.read_file_as_list(
					file_path=f'{folder_path}/{file_name}',
					choose=choose,
					choose_mode=chose_mode,
					read_mode=read_mode,
					encoding=encoding
				)
				list_dict[os.path.splitext(file_name)[0]] = file_data
				text_list += file_data
				cycle_count += 1
				if list_count <= cycle_count:  # 如果超出文件读取数
					break
		if return_mode == 'dict':  # 返回模式为字典
			return list_dict
		else:  # 返回模式为列表
			return text_list

# if __name__ == '__main__':  # 代码测试
#     import time
#     time_start = time.time()
#     file_path = './tests/text/test.txt'
#     # print(Text_Mgt.Encoding_Detect(file_path))
#     # print(Text_Mgt.Read_Text(file_path='./core/log_mgt.py'))
#     # print(Text_Mgt.List_Read_Text(file_path='./core/log_mgt.py', choose='#',choose_mode=1, read_mode=0))
#     # print(Text_Mgt.Match_List(Text_Mgt.List_Read_Text(file_path),'#测试啊'))
#     # Text_Mgt.Text_Exists('./temp.txt', 'hello')
#     # print(Text_Mgt.List_Read_TXT_Under_Folder('./config/conf', '.ini',return_mode='dict'))
#     print(time.time()-time_start)

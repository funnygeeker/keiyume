#!/usr/bin/python3
# -*- coding: utf-8 -*-
# keiyume_2.0.0-beta.2

# 溪梦框架API模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832

# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker

import random

from .config import *  # 导入配置文件模块
from .tools import *  # 导入工具模块


class Api:
	def __init__(self) -> None:
		"""初始化

		"""
		pass

	# 基本函数 #
	@staticmethod
	def send_data(action: str, params: dict, echo: Optional[Any] = None) -> Dict:
		"""发送GO-CQ规范的API数据

		Args:
			action (str): API名称
			params (dict): API参数
			echo (Optional[Any], optional): echo. Defaults to None.

		Returns:
			Dict: 返回的数据
		"""
		if echo is None:  # 如果echo字段为空，则由Random_Echo管理echo字段的生成
			echo = Api.echo_randomly()
		event = threading.Event()  # 这里的event用于等待返回结果
		with lock:
			Connect.event_dict[echo] = {
				'object': event, 'result': None}  # 添加字典的一个键，用于存储对象和交换结果
		try:
			json_data = json.dumps({
				"action": action,
				"params": params,
				"echo": echo}, ensure_ascii=False, indent=4)  # 将数据转换为json格式
			logger.debug(f'正在发送：\n{json_data}\n')
			Connect.ws.send(json_data)  # 发送原始数据
			# 阻塞整个线程，等待返回结果，如果超时则继续执行，如果API无响应，会根据API的不同，[可能]报KeyError错误
			event.wait(timeout=10.0)
			with lock:
				result = Connect.event_dict[echo]['result']
				del Connect.event_dict[echo]
			return result
		except Exception as e:
			logger.error(e)
			logger.error(Log.Get_Error())  # 出现错误则记录错误日志

	@staticmethod
	def echo_randomly() -> int:
		"""生成一个随机且不重复的echo字段内容
		"""
		cycle_num = 0  # 循环计数
		while True:
			random_num = random.randint(-16777216, 16777216)  # 强迫症，随便定的随机范围
			cycle_num += 1
			if Connect.event_dict.get(random_num) is None:
				return random_num
			elif cycle_num >= 512:
				logger.critical(
					'【严重错误】随机数字生成出错，程序接收到的消息可能超过了设计的最大处理量，也可能是其他问题！')
				Connect.Exit()
				break

	# 消息管理 #
	@staticmethod
	def send_private_msg(user_id: int, message: str, group_id: int = 0, auto_escape: Optional[bool] = False,
	                     echo: Optional[None] = None):
		"""发送私聊消息

		Args:
			user_id (int): 用户QQ号
			message (str): 消息内容
			group_id (int, optional): 群号. Defaults to 0.
			auto_escape (Optional[bool], optional): 是否转义. Defaults to False.
			echo (Optional[None], optional): echo. Defaults to None.
			group_id (int, optional): 群ID. Defaults to 0.
			auto_escape (Optional[bool], optional): 是否转义. Defaults to False.

		Returns:
			Dict: 返回的数据
"""
		result = Api.send_data(action="send_private_msg", params={
			'user_id': user_id,
			'group_id': group_id,
			'message': message,
			'auto_escape': auto_escape
		}, echo=echo)
		try:
			logger.info(
				f"【信息】私聊 {user_id} 发送： {message} （消息ID：{result['data']['message_id']}）\n")  # 记录日志
		except:
			logger.error(
				f'【错误】{Log.Get_Error()}\n返回值：\n{Tools.to_json(result)}\n')
			return None
		return result

	def send_group_msg(group_id: int, message: str, auto_escape: bool = False, echo=None):
		'''【发送群消息】
		group_id:群号
		message:要发送的内容
		auto_escape:消息内容是否作为纯文本发送(即不解析CQ码),只在message字段是字符串时有效
		echo:回声, 如果指定了echo字段, 那么响应包也会同时包含一个echo字段, 它们会有相同的值
		返回: dict/None'''
		result = Api.send_data(action="send_group_msg", params={
			'group_id': group_id,
			'message': message,
			'auto_escape': auto_escape
		}, echo=echo)
		try:
			logger.info(
				f"【信息】群聊 {group_id} 发送： {message} （消息ID：{result['data']['message_id']}）\n")  # 记录日志
		except:
			logger.error(
				f'【错误】{Log.Get_Error()}\n返回值：\n{Tools.to_json(result)}\n')
			return None
		return result

	def delete_msg(message_id: int, echo=None):
		'''【撤回消息】
		message_id:消息ID
		echo:回声, 如果指定了echo字段, 那么响应包也会同时包含一个echo字段, 它们会有相同的值
		返回: dict/None'''
		result = Api.send_data(action="delete_msg", params={
			'message_id': message_id
		}, echo=echo)
		try:
			logger.info(
				f"【信息】尝试撤回消息 （消息ID：{message_id}）\n")  # 记录日志
		except:
			logger.error(
				f'【错误】{Log.Get_Error()}\n返回值：\n{Tools.to_json(result)}\n')
			return None
		return result

	# 群聊管理 #
	def set_group_anonymous_ban(group_id: int, anonymous: dict = {}, flag: str = '', duration: int = 30 * 60,
	                            echo=None):
		'''【群组匿名用户禁言】
		group_id:群号
		anonymous:可选,要禁言的匿名用户对象（群消息上报的 anonymous 字段）
		flag:可选,要禁言的匿名用户的 flag（需从群消息上报的数据中获得）
		duration:禁言时长,单位秒,无法取消匿名用户禁言
		返回: dict/None'''
		result = Api.send_data(action="set_group_anonymous_ban", params={
			'group_id': group_id,
			'anonymous': anonymous,
			'flag': flag,
			'duration': duration
		}, echo=echo)
		try:
			logger.info(
				f"【信息】群聊 {group_id} 禁言匿名用户：{anonymous['flag']['name']}，时长：{duration}秒（{duration / 60}分钟）\n")  # 记录日志
		except:
			logger.error(
				f'【错误】{Log.Get_Error()}\n返回值：\n{Tools.to_json(result)}\n')
			return None
		return result

	def set_group_ban(group_id: int, user_id: int, duration: int = 30 * 60, echo=None):
		'''【群组禁言】
		group_id:群号
		user_id:要禁言的QQ号
		duration:禁言时长,单位秒,0表示取消禁言
		返回: dict/None'''
		result = Api.send_data(action="set_group_ban", params={
			'group_id': group_id,
			'user_id': user_id,
			'duration': duration
		}, echo=echo)
		try:
			logger.info(
				f"【信息】群聊 {group_id} 禁言用户：{user_id}，时长：{duration}秒（{duration / 60}分钟）\n")  # 记录日志
		except:
			logger.error(
				f'【错误】{Log.Get_Error()}\n返回值：\n{Tools.to_json(result)}\n')
			return None
		return result

	def set_group_whole_ban(group_id: int, enable: bool, echo=None):
		'''【群组全体禁言】
		group_id:群号
		enable:是否禁言
		返回: dict/None'''
		result = Api.send_data(action="set_group_whole_ban", params={
			'group_id': group_id,
			'enable': enable
		}, echo=echo)
		try:
			if enable == True:
				enable = '启用'
			else:
				enable = '禁用'
			logger.info(
				f"【信息】群聊 {group_id} 全体禁言 已{enable}\n")  # 记录日志
		except:
			logger.error(
				f'【错误】{Log.Get_Error()}\n返回值：\n{Tools.to_json(result)}\n')
			return None
		return result

	def set_group_admin(group_id: int, user_id: int, enable: bool, echo=None):
		'''【群组设置管理员】
		group_id:群号
		user_id:要设置管理员的 QQ 号
		enable:True为设置,False为取消
		返回: dict/None'''
		result = Api.send_data(action="set_group_admin", params={
			'group_id': group_id,
			'user_id': user_id,
			'enable': enable
		}, echo=echo)
		try:
			if enable == True:
				enable = '启用'
			else:
				enable = '禁用'
			logger.info(
				f"【信息】群聊 {group_id} 将 {user_id} 的管理员身份设置为 {enable}\n")  # 记录日志
		except:
			logger.error(
				f'【错误】{Log.Get_Error()}\n返回值：\n{Tools.to_json(result)}\n')
			return None
		return result

	def set_group_add_request(flag: str, sub_type: str, approve: bool, reason: str = '', group_id: int = None,
	                          user_id: int = None, echo=None):
		'''【处理加群请求／邀请】
		flag:加群请求的 flag（需从上报的数据中获得）
		sub_type:add或invite,请求类型（需要和上报消息中的sub_type字段相符）
		approve:是否同意请求/邀请
		reason:拒绝理由（仅在拒绝时有效）

		可选参数：
		group_id:群号，用于控制台输出信息（一般为事件中的group_id）
		user_id:加群用户，用于控制台输出信息（一般为事件中的user_id）
		返回: dict/None'''
		result = Api.send_data(action="set_group_add_request", params={
			'flag': flag,
			'sub_type': sub_type,
			'approve': approve,
			'reason': reason
		}, echo=echo)
		try:
			if approve == True:
				approve = '同意'
			else:
				approve = '不同意'
			if group_id != None and user_id != None:
				logger.info(
					f"【信息】群聊 {group_id} 将 {user_id} 的加群申请设为 {approve}\n")  # 记录日志
			else:
				logger.info(
					f"【信息】已将加群申请设为 {approve}")  # 记录日志
		except:
			logger.error(
				f'【错误】{Log.Get_Error()}\n返回值：\n{Tools.to_json(result)}\n')
			return None
		return result

	def set_group_kick(group_id: int, user_id: int, reject_add_request: bool = False, echo=None):
		'''【群组踢人】
		group_id:群号
		user_id:要踢的QQ号
		reject_add_request:拒绝此人的加群请求
		返回: dict/None'''
		result = Api.send_data(action="set_group_kick", params={
			'group_id': group_id,
			'user_id': user_id,
			'reject_add_request': reject_add_request
		}, echo=echo)
		try:
			if reject_add_request == True:
				reject_add_request = '启用'
			else:
				reject_add_request = '禁用'
			logger.info(
				f"【信息】群聊 {group_id} 中，已踢出：{user_id}（屏蔽加群申请：{reject_add_request}）\n")  # 记录日志
		except:
			logger.error(
				f'【错误】{Log.Get_Error()}\n返回值：\n{Tools.to_json(result)}\n')
			return None
		return result

	def get_status(echo=None):
		'''【获取状态】
		常用返回的key值说明:
		online(表示BOT是否在线,bool)
		stat(运行统计,dict)
		返回: dict/None'''
		result = Api.send_data(action="get_status", echo=echo)
		try:
			logger.info(
				f"【信息】尝试获取CQ-HTTP状态...\n")  # 记录日志
		except:
			logger.error(
				f'【错误】{Log.Get_Error()}\n返回值：\n{Tools.to_json(result)}\n')
			return None
		return result


'''[CQ:face,id=174]表情
4酷 5哭 12调皮 13呲牙 14微笑 15难过 20偷笑 27尴尬 31骂 32疑问 33嘘 
39再见 97擦汗 174摊手 176皱眉 178斜眼笑 212托腮
更多参照：https://github.com/kyubotics/coolq-http-api/wiki/%E8%A1%A8%E6%83%85-CQ-%E7%A0%81-ID-%E8%A1%A8
语音[CQ:record,file=http://xxxx.com/1.mp3]
艾特[CQ:at,qq=user_id]踢了踢[CQ:poke,qq={}]
链接分享[CQ:share,url=http://baidu.com,title=百度]'''

if True:  # 这里加if True是避免格式化代码时将这部分放置在代码前段导致导入错误
	from .connect import Connect

	lock = Connect.lock

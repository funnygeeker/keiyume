import json
import random
import threading
from .tools import *
from .connect_mgr import Connect_Mgr
from .log_mgr import *  # 导入日志管理器
from .config_mgr import *  # 导入配置文件管理器

Lock = Connect_Mgr.lock


class Api():
    def __init__():
        pass

    # 基本函数 #
    def Send_Data(action: str, data: dict = {}, echo=None):
        '''【发送GO-CQ规范的API数据】'''
        if echo == None:  # 如果echo字段为空，则由Random_Echo管理echo字段的生成
            echo = Api.Random_Echo()
        event = threading.Event()  # 这里的event用于等待返回结果
        with Lock:
            Connect_Mgr.event_dict[echo] = {
                'object': event, 'result': None}  # 添加字典的一个键，用于存储对象和交换结果
        try:
            json_data = json.dumps({
                "action": action,
                "params": data,
                "echo": echo}, ensure_ascii=False, indent=4)  # 将数据转换为json格式
            logger.debug(f'正在发送：\n{json_data}\n')
            Connect_Mgr.ws.send(json_data)  # 发送原始数据
            event.wait(timeout=10.0)
            # 阻塞整个线程，等待返回结果，如果超时则继续执行，如果API无响应，会根据API的不同，[可能]报KeyError错误
            with Lock:
                result = Connect_Mgr.event_dict[echo]['result']
                del Connect_Mgr.event_dict[echo]
            return result
        except:
            logger.error(Log_Mgr.Get_Error())  # 出现错误则记录错误日志
            return None

    def Random_Echo() -> int:
        '''【用于生成一个随机且不重复的echo字段内容】'''
        cycle_num = 0
        while True:
            random_num = random.randint(-16777216, 16777216)
            cycle_num += 1
            if Connect_Mgr.event_dict.get(random_num) == None:
                return random_num
            elif cycle_num >= 512:
                logger.critical(
                    '【严重错误】随机数字生成出错，程序接收到的消息可能超过了设计的最大处理量，也可能是其他问题！')
                Connect_Mgr.Exit()
                break

    # 消息管理 #
    def send_private_msg(user_id: int, group_id: int = 0, message: str = '', auto_escape: bool = False, echo=None):
        '''【发送私聊消息】
        user_id:对方QQ号
        group_id:主动发起临时会话群号(机器人本身必须是管理员/群主)
        message:要发送的内容
        auto_escape:消息内容是否作为纯文本发送(即不解析CQ码),只在message字段是字符串时有效
        echo:回声, 如果指定了echo字段, 那么响应包也会同时包含一个echo字段, 它们会有相同的值
        返回: dict/None'''
        result = Api.Send_Data(action="send_private_msg", data={
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
                f'【错误】{Log_Mgr.Get_Error()}\n返回值：\n{Tools.To_Json(result)}\n')
            return None
        return result

    def send_group_msg(group_id: int, message: str = '', auto_escape: bool = False, echo=None):
        '''【发送群消息】
        group_id:群号
        message:要发送的内容
        auto_escape:消息内容是否作为纯文本发送(即不解析CQ码),只在message字段是字符串时有效
        echo:回声, 如果指定了echo字段, 那么响应包也会同时包含一个echo字段, 它们会有相同的值
        返回: dict/None'''
        result = Api.Send_Data(action="send_group_msg", data={
            'group_id': group_id,
            'message': message,
            'auto_escape': auto_escape
        }, echo=echo)
        try:
            logger.info(
                f"【信息】群聊 {group_id} 发送： {message} （消息ID：{result['data']['message_id']}）\n")  # 记录日志
        except:
            logger.error(
                f'【错误】{Log_Mgr.Get_Error()}\n返回值：\n{Tools.To_Json(result)}\n')
            return None
        return result

    def delete_msg(message_id: int, echo=None):
        '''【撤回消息】
        message_id:消息ID
        echo:回声, 如果指定了echo字段, 那么响应包也会同时包含一个echo字段, 它们会有相同的值
        返回: dict/None'''
        result = Api.Send_Data(action="delete_msg", data={
            'message_id': message_id
        }, echo=echo)
        try:
            logger.info(
                f"【信息】尝试撤回消息 （消息ID：{message_id}）\n")  # 记录日志
        except:
            logger.error(
                f'【错误】{Log_Mgr.Get_Error()}\n返回值：\n{Tools.To_Json(result)}\n')
            return None
        return result

    # 群聊管理 #
    def set_group_anonymous_ban(group_id: int, anonymous: dict = {}, flag: str = '', duration: int = 30*60, echo=None):
        '''【群组匿名用户禁言】
        group_id:群号
        anonymous:可选,要禁言的匿名用户对象（群消息上报的 anonymous 字段）
        flag:可选,要禁言的匿名用户的 flag（需从群消息上报的数据中获得）
        duration:禁言时长,单位秒,无法取消匿名用户禁言
        返回: dict/None'''
        result = Api.Send_Data(action="set_group_anonymous_ban", data={
            'group_id': group_id,
            'anonymous': anonymous,
            'flag': flag,
            'duration': duration
        }, echo=echo)
        try:
            logger.info(
                f"【信息】群聊 {group_id} 禁言匿名用户：{anonymous['flag']['name']}，时长：{duration}秒（{duration/60}分钟）\n")  # 记录日志
        except:
            logger.error(
                f'【错误】{Log_Mgr.Get_Error()}\n返回值：\n{Tools.To_Json(result)}\n')
            return None
        return result

    def set_group_ban(group_id: int, user_id: int, duration: int = 30*60, echo=None):
        '''【群组禁言】
        group_id:群号
        user_id:要禁言的QQ号
        duration:禁言时长,单位秒,0表示取消禁言
        返回: dict/None'''
        result = Api.Send_Data(action="set_group_ban", data={
            'group_id': group_id,
            'user_id': user_id,
            'duration': duration
        }, echo=echo)
        try:
            logger.info(
                f"【信息】群聊 {group_id} 禁言用户：{user_id}，时长：{duration}秒（{duration/60}分钟）\n")  # 记录日志
        except:
            logger.error(
                f'【错误】{Log_Mgr.Get_Error()}\n返回值：\n{Tools.To_Json(result)}\n')
            return None
        return result

    def set_group_whole_ban(group_id: int, enable: bool, echo=None):
        '''【群组全体禁言】
        group_id:群号
        enable:是否禁言
        返回: dict/None'''
        result = Api.Send_Data(action="set_group_whole_ban", data={
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
                f'【错误】{Log_Mgr.Get_Error()}\n返回值：\n{Tools.To_Json(result)}\n')
            return None
        return result

    def set_group_admin(group_id: int, user_id: int, enable: bool, echo=None):
        '''【群组设置管理员】
        group_id:群号
        user_id:要设置管理员的 QQ 号
        enable:True为设置,False为取消
        返回: dict/None'''
        result = Api.Send_Data(action="set_group_admin", data={
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
                f'【错误】{Log_Mgr.Get_Error()}\n返回值：\n{Tools.To_Json(result)}\n')
            return None
        return result

    def set_group_add_request(flag: str, sub_type: str, approve: bool, reason: str = '', group_id: int = None, user_id: int = None, echo=None):
        '''【处理加群请求／邀请】
        flag:加群请求的 flag（需从上报的数据中获得）
        sub_type:add或invite,请求类型（需要和上报消息中的sub_type字段相符）
        approve:是否同意请求/邀请
        reason:拒绝理由（仅在拒绝时有效）

        可选参数：
        group_id:群号，用于控制台输出信息（一般为事件中的group_id）
        user_id:加群用户，用于控制台输出信息（一般为事件中的user_id）
        返回: dict/None'''
        result = Api.Send_Data(action="set_group_add_request", data={
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
                f'【错误】{Log_Mgr.Get_Error()}\n返回值：\n{Tools.To_Json(result)}\n')
            return None
        return result

    def set_group_kick(group_id: int, user_id: int, reject_add_request: bool = False, echo=None):
        '''【群组踢人】
        group_id:群号
        user_id:要踢的QQ号
        reject_add_request:拒绝此人的加群请求
        返回: dict/None'''
        result = Api.Send_Data(action="set_group_kick", data={
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
                f'【错误】{Log_Mgr.Get_Error()}\n返回值：\n{Tools.To_Json(result)}\n')
            return None
        return result

    def get_status(echo=None):
        '''【获取状态】
        常用返回的key值说明:
        online(表示BOT是否在线,bool)
        stat(运行统计,dict)
        返回: dict/None'''
        result = Api.Send_Data(action="get_status", echo=echo)
        try:
            logger.info(
                f"【信息】尝试获取CQ-HTTP状态...\n")  # 记录日志
        except:
            logger.error(
                f'【错误】{Log_Mgr.Get_Error()}\n返回值：\n{Tools.To_Json(result)}\n')
            return None
        return result


'''[CQ:face,id=174]表情
4酷 5哭 12调皮 13呲牙 14微笑 15难过 20偷笑 27尴尬 31骂 32疑问 33嘘 
39再见 97擦汗 174摊手 176皱眉 178斜眼笑 212托腮
更多参照：https://github.com/kyubotics/coolq-http-api/wiki/%E8%A1%A8%E6%83%85-CQ-%E7%A0%81-ID-%E8%A1%A8
语音[CQ:record,file=http://xxxx.com/1.mp3]
艾特[CQ:at,qq=user_id]踢了踢[CQ:poke,qq={}]
链接分享[CQ:share,url=http://baidu.com,title=百度]'''

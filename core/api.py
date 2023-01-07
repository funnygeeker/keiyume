# -*- coding : utf-8-*-
# 溪梦框架：core/api.py
# 管理框架调用 go-cqhttp 的 api 接口
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume
#
# 参考资料：
# 知乎 - python 线程事件 Event：https://zhuanlan.zhihu.com/p/90850159
# go-cqhttp 文档 - 请求说明：https://docs.go-cqhttp.org/api/#%E5%9F%BA%E7%A1%80%E4%BC%A0%E8%BE%93

import json
import random
import traceback
import threading

from typing import (Dict, Union, Optional, Any)

from . import public

logger = public.logger


# 基本函数 #

def send_data(action: str, params: dict, echo: Any = None) -> Optional[Dict[str, Union[dict, str, int]]]:
    """
    向 go-cqhttp 发送 json 数据

    Args:
        action: 终结点名称, 例如 'send_group_msg'
        params: 所调用的 api 的参数，详见 go-cqhttp 文档
        echo: echo 字段的内容，一般不需要填写，由框架自动管理

    Returns:
        以字典形式返回的响应数据

    References:
        go-cqhttp 文档: https://docs.go-cqhttp.org/api
    """
    if public.connect.ws is not None:
        if echo is None:  # 如果 echo 字段为空，则由 _echo_randomly 管理 echo 字段的生成
            echo = _echo_randomly()
        event = threading.Event()  # 这里的 event 用于阻塞线程，等待返回结果
        with public.lock:
            public.connect.echo_dict[echo] = {
                'object': event, 'result': None}  # 该字典用于存储对象和交换请求的结果
        try:
            json_data = json.dumps({
                "action": action,
                "params": params,
                "echo": echo}, ensure_ascii=False, indent=4)  # 将数据转换为 JSON 格式
            logger.debug(f'发送数据：\n{json_data}')
            public.connect.ws.send(json_data)  # 发送原始数据
            # 阻塞整个线程，等待返回结果，如果超时则取消阻塞继续执行，如果无响应，可能会由于返回的值为 None 报 KeyError 错误
            event.wait(timeout=60.0)
            with public.lock:
                result = public.connect.echo_dict[echo]['result']
                del public.connect.echo_dict[echo]
            return result
        except Exception as error:
            logger.error(f"【错误】发送数据时出现错误 {error}：\n{traceback.format_exc()}")  # 出现错误则记录错误日志
    else:
        logger.warning(f"【警告】您还未连接 go-cqhttp，暂时无法正常使用任何 api！")


def _echo_randomly() -> int:
    """
    生成一个随机且不重复的 echo 字段

    Returns:
        随机的数字，介于 (-16777216, 16777216) 之间
    """
    cycle_num = 0  # 循环计数
    while True:
        random_num = random.randint(-16777216, 16777216)  # 强迫症，随便定的随机范围
        cycle_num += 1
        if public.connect.echo_dict.get(random_num) is None:
            return random_num
        elif cycle_num >= 256:
            logger.critical(
                '【严重错误】随机数字生成出错，可能是程序发送的的消息超过了设计的最大处理量！')
            public.connect.exit()
            break


def _to_json(data: dict) -> str:
    """
    将字典转换为 JSON 格式

    Returns:
        JSON 格式的数据
    """
    return json.dumps(data, ensure_ascii=False, indent=4)


# 消息管理 #

def send_private_msg(user_id: Union[int, str], message: str, group_id: Union[int, str] = 0, auto_escape: bool = False,
                     echo: Any = None) -> Optional[dict]:
    """
    发送私聊消息

    Args:
        user_id: 对方 QQ 号
        message: 要发送的内容
        group_id: 主动发起临时会话时的来源群号(可选, 机器人本身必须是管理员/群主)
        auto_escape: 消息内容是否作为纯文本发送 (即不解析 CQ 码)
        echo: echo 字段的内容，一般不需要填写，由框架自动管理

    Returns:
        以字典形式返回的响应数据，若失败则返回 None
    """
    result = send_data(action="send_private_msg", params={
        'user_id': user_id,
        'group_id': group_id,
        'message': message,
        'auto_escape': auto_escape
    }, echo=echo)
    try:
        logger.info(
            f"【信息】私聊 {user_id} 发送： {message} （消息ID：{result['data']['message_id']}）")  # 记录日志
    except TypeError:
        logger.error(
            f'【错误】消息发送失败或超时！\n{traceback.format_exc()}\n返回值：\n{_to_json(result)}')
        return None
    return result


def send_group_msg(group_id: Union[int, str], message: str, auto_escape: bool = False,
                   echo: Any = None) -> Optional[dict]:
    """
    发送群消息
    Args:
        group_id: 群号
        message: 要发送的内容
        auto_escape: 消息内容是否作为纯文本发送 (即不解析 CQ 码)
        echo: echo 字段的内容，一般不需要填写，由框架自动管理

    Returns:
        以字典形式返回的响应数据，若失败则返回 None
    """
    result = send_data(action="send_group_msg", params={
        'group_id': group_id,
        'message': message,
        'auto_escape': auto_escape
    }, echo=echo)
    try:
        logger.info(
            f"【信息】群聊 {group_id} 发送： {message} （消息ID：{result['data']['message_id']}）")  # 记录日志
    except TypeError:
        logger.error(
            f'【错误】消息发送失败或超时！\n{traceback.format_exc()}\n返回值：\n{_to_json(result)}')
        return None
    return result


def delete_msg(message_id: Union[int, str], echo: Any = None) -> Optional[dict]:
    """
    撤回消息

    message_id: 消息 ID
    echo: echo 字段的内容，一般不需要填写，由框架自动管理

    Returns:
        以字典形式返回的响应数据，若失败则返回 None
    """
    result = send_data(action="delete_msg", params={
        'message_id': message_id
    }, echo=echo)
    logger.info(f"【信息】正在撤回消息 （消息ID：{message_id}）")  # 记录日志
    try:
        if result['status'] != 'ok':
            error = result.get('wording')
            if error == "recall error: 1001 msg: No message meets the requirements":
                error = "没有找到符合要求的消息！"
            logger.error(
                f"【错误】消息撤回时出错！\n返回值：{error}")
            return None
    except TypeError:
        logger.error(
            f'【错误】撤回消息时出现错误！\n{traceback.format_exc()}\n返回值：\n{_to_json(result)}')
        return None
    return result


# 群聊管理 #
def set_group_anonymous_ban(group_id: Union[int, str], anonymous: Optional[dict] = None, flag: str = '',
                            duration: int = 30 * 60, echo: Any = None) -> Optional[dict]:
    """
    群组匿名用户禁言

    Args:
        group_id: 群号
        anonymous: 可选，要禁言的匿名用户对象（群消息上报的 anonymous 字段）
        flag: 可选，要禁言的匿名用户的 flag（需从群消息上报的数据中获得）
        duration: 禁言时长，单位秒，无法取消匿名用户禁言
        echo: echo 字段的内容，一般不需要填写，由框架自动管理
    Returns:
        以字典形式返回的响应数据，若失败则返回 None
    """
    result = send_data(action="set_group_anonymous_ban", params={
        'group_id': group_id,
        'anonymous': anonymous,
        'flag': flag,
        'duration': duration
    }, echo=echo)
    try:
        logger.info(
            f"【信息】群聊 {group_id} 禁言匿名用户：{anonymous['flag']['name']}，时长：{duration}秒（{duration / 60}分钟）")  # 记录日志
    except TypeError:
        logger.error(
            f'【错误】禁言匿名用户时发生错误！\n{traceback.format_exc()}\n返回值：\n{_to_json(result)}')
        return None
    return result


def set_group_ban(group_id: Union[int, str], user_id: Union[int, str], duration: int = 30 * 60,
                  echo: Any = None) -> Optional[dict]:
    """
    群组禁言

    Args:
        group_id: 群号
        user_id: 要禁言的 QQ 号
        duration: 禁言时长，单位秒，0 表示取消禁言
        echo: echo 字段的内容，一般不需要填写，由框架自动管理
    
    Returns:
        以字典形式返回的响应数据，若失败则返回 None
    """
    result = send_data(action="set_group_ban", params={
        'group_id': group_id,
        'user_id': user_id,
        'duration': duration
    }, echo=echo)
    try:
        logger.info(
            f"【信息】群聊 {group_id} 禁言用户：{user_id}，时长：{duration}秒（{duration / 60}分钟）")  # 记录日志
    except TypeError:
        logger.error(
            f'【错误】禁言匿名用户时发生错误！\n{traceback.format_exc()}\n返回值：\n{_to_json(result)}')
        return None
    return result


def set_group_whole_ban(group_id: Union[int, str], enable: bool,
                        echo: Any = None) -> Optional[dict]:
    """
    群组全体禁言

    Args:
        group_id: 群号
        enable: 是否禁言
        echo: echo 字段的内容，一般不需要填写，由框架自动管理

    Returns:
        以字典形式返回的响应数据，若失败则返回 None
    """
    result = send_data(action="set_group_whole_ban", params={
        'group_id': group_id,
        'enable': enable
    }, echo=echo)
    try:
        if enable:
            enable_ = '启用'
        else:
            enable_ = '禁用'
        logger.info(
            f"【信息】群聊 {group_id} 全体禁言 已{enable_}")  # 记录日志
    except TypeError:
        logger.error(
            f'【错误】执行全体禁言时发生错误！\n{traceback.format_exc()}\n返回值：\n{_to_json(result)}')
        return None
    return result


def set_group_admin(group_id: Union[int, str], user_id: Union[int, str], enable: bool,
                    echo: Any = None) -> Optional[dict]:
    """
    群组设置管理员

    Args:
        group_id: 群号
        user_id: 要设置管理员的 QQ 号
        enable: True 为设置，False 为取消
        echo: echo 字段的内容，一般不需要填写，由框架自动管理

    Returns:
        以字典形式返回的响应数据，若失败则返回 None
    """
    result = send_data(action="set_group_admin", params={
        'group_id': group_id,
        'user_id': user_id,
        'enable': enable
    }, echo=echo)
    try:
        if enable:
            enable = '启用'
        else:
            enable = '禁用'
        logger.info(
            f"【信息】群聊 {group_id} 将 {user_id} 的管理员身份设置为 {enable}")  # 记录日志
    except TypeError:
        logger.error(
            f'【错误】群组设置管理员时发生错误！{traceback.format_exc()}\n返回值：\n{_to_json(result)}')
        return None
    return result


def set_group_add_request(flag: str, sub_type: str, approve: bool, reason: str = '', group_id: Union[int, str] = None,
                          user_id: Union[int, str] = None, echo: Any = None) -> Optional[dict]:
    """
    处理加群请求／邀请

    Args:
        flag: 加群请求的 flag（需从上报的数据中获得）
        sub_type: add 或 invite，请求类型（需要和上报消息中的 sub_type 字段相符）
        approve: 是否同意请求/邀请
        reason: 拒绝理由（仅在拒绝时有效）
        group_id: 群号，可选，用于在日志中输出详细信息
        user_id: QQ 号，可选，用于在日志中输出详细信息
        echo: echo 字段的内容，一般不需要填写，由框架自动管理

    Returns:
        以字典形式返回的响应数据，若失败则返回 None
    """
    result = send_data(action="set_group_add_request", params={
        'flag': flag,
        'sub_type': sub_type,
        'approve': approve,
        'reason': reason
    }, echo=echo)
    try:
        if approve:
            approve = '同意'
        else:
            approve = '不同意'
        if group_id and user_id:  # 参数中是否存在群号和用户号
            logger.info(
                f"【信息】群聊 {group_id} 将 {user_id} 的加群申请设为 {approve}")  # 记录日志
        else:
            logger.info(
                f"【信息】已将加群申请设为 {approve}")  # 记录日志
    except TypeError:
        logger.error(
            f'【错误】处理加群请求时出现错误！\n{traceback.format_exc()}\n返回值：\n{_to_json(result)}')
        return None
    return result


def set_group_kick(group_id: Union[int, str], user_id: Union[int, str], reject_add_request: bool = False,
                   echo: Any = None) -> Optional[dict]:
    """
    群组踢人

    Args:
        group_id: 群号
        user_id: 要踢的 QQ 号
        reject_add_request: 拒绝此人的加群请求
        echo: echo 字段的内容，一般不需要填写，由框架自动管理

    Returns:
        以字典形式返回的响应数据，若失败则返回 None
    """
    result = send_data(action="set_group_kick", params={
        'group_id': group_id,
        'user_id': user_id,
        'reject_add_request': reject_add_request
    }, echo=echo)
    try:
        if reject_add_request:
            reject_add_request = '启用'
        else:
            reject_add_request = '禁用'
        logger.info(
            f"【信息】群聊 {group_id} 中，已踢出：{user_id}（屏蔽加群申请：{reject_add_request}）")  # 记录日志
    except TypeError:
        logger.error(
            f'【错误】群组踢人时出现错误!\n{traceback.format_exc()}\n返回值：\n{_to_json(result)}')
        return None
    return result


# 信息获取 #
def get_group_member_info(group_id: Union[int, str], user_id: Union[int, str], no_cache: bool = False,
                          echo: Any = None) -> Optional[dict]:
    """
    获取群成员信息

    Args:
        group_id: 群号
        user_id: QQ 号
        no_cache: 是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
        echo: echo 字段的内容，一般不需要填写，由框架自动管理

    Returns:
        以字典形式返回的响应数据，若失败则返回 None
    """
    result = send_data(action="get_group_member_info", params={
        'group_id': group_id,
        'user_id': user_id,
        'no_cache': no_cache
    }, echo=echo)
    try:
        logger.debug(
            f"【信息】尝试获取群 {group_id} 成员 {user_id} 的信息")  # 记录日志
    except TypeError:
        logger.error(
            f'【错误】获取群成员 {user_id} 信息失败！\n{traceback.format_exc()}\n返回值：\n{_to_json(result)}')
        return None
    return result


def get_status(echo: Any = None) -> Optional[dict]:
    """
    获取 go-cqhttp 状态

    Args:
        echo: echo 字段的内容，一般不需要填写，由框架自动管理

    Returns:
        以字典形式返回的响应数据，若失败则返回 None

    References:
        详情请参考 go-cqhttp 文档:
        https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%8A%B6%E6%80%81
    """
    result = send_data(action="get_status", params={}, echo=echo)
    logger.info(f"【信息】正在获取 go-cqhttp 状态...")  # 记录日志
    return result

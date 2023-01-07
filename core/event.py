# -*- coding : utf-8-*-
# 溪梦框架：core/event.py
# 对接收到的事件进行预处理
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume
#
# 参考资料：
# GitHub - FloatTech/voidbot：https://github.com/FloatTech/voidbot

from typing import (Optional, Union, List, Dict, Any)

from . import public


class Event:
    def __init__(self, data: dict = None) -> None:
        """
        将常用的消息字段代入self对象

        Args:
            data: 接收到的原始消息
        """
        if data is None:
            data = {}
        self.data: Dict[str, Any] = data
        '接收到的原始数据'
        if public.connect is not None:
            self.ws = public.connect.ws
            '连接的 Websocket 对象'
            self.self_user_id: int = public.connect.self_user_id
            '登录用户的ID'
        self.echo: Optional[int] = self.data.get('echo')
        'echo 字段内容，一般用不上'
        self.time: int = self.data.get('time')
        '时间'
        self.user_id: Optional[int] = self.data.get('user_id')
        '用户ID'
        self.msg: str = self.data.get('message')
        '消息内容'
        self.message: str = self.msg
        '消息内容'
        self.sub_type: Optional[str] = self.data.get('sub_type')
        '事件子类型'
        self.group_id: Optional[int] = self.data.get('group_id')
        '群聊ID'
        self.post_type: str = self.data.get('post_type')
        '事件类型'
        self.message_id: Optional[int] = self.data.get('message_id')
        '消息ID'
        self.cmd_body: str = ""
        '判断命令后返回的命令体'
        self.super_user: List[int] = public.config['admin']['super_user']
        '超级用户'
        self.super_admin: List[int] = public.config['admin']['super_admin']
        '超级管理员'

    # 基本事件类型 #
    def is_echo(self, echo: Optional[Union[str, int]] = None) -> bool:
        """
                判断事件是否为 api 调用的返回结果（即含echo字段）

                Args:
                    echo: 可选，指定 echo 内容是否一致，作为附加条件进行判断
                """
        if self.data.get('echo') is not None:
            if echo is None:
                return True
            else:
                return self.data['echo'] == echo
        return False

    def is_notice(self, notice_type: Optional[str] = None) -> bool:
        """
        判断事件是否为通知，可以用的类型有：
            group_upload(群文件上传)  group_admin(群管理员变更)  group_decrease(群成员减少)  group_increase(群成员增加)
            group_ban(群成员禁言)  friend_add(好友添加)  group_recall(群消息撤回)  friend_recall(好友消息撤回)
            group_card(群名片变更)  offline_file(离线文件上传)  client_status(客户端状态变更)  essence(精华消息)
            notify(系统通知)

        Args:
            notice_type: 可选，指定 notice_type 内容是否一致，作为附加条件进行判断
        """
        if self.data.get('post_type') == 'notice':
            if notice_type is None:
                return True
            else:
                return self.data['notice_type'] == notice_type
        return False

    def is_message(self, message_type: Optional[str] = None) -> bool:
        """
        判断事件是否为消息

        Args:
            message_type: 可选，指定 message_type 内容是否一致，作为附加条件进行判断，可以用的类型有：
                private(私聊消息)  group(群消息)
        """
        if self.data.get('post_type') == 'message':
            if message_type is None:
                return True
            else:
                return self.data['message_type'] == message_type
        return False

    def is_msg(self, message_type: Optional[str] = None) -> bool:
        """
        判断事件是否为消息

        Args:
            message_type: 可选，指定 message_type 内容是否一致，作为附加条件进行判断，可以用的类型有：
                private(私聊消息)  group(群消息)
        """
        return self.is_message(message_type)

    def is_request(self, request_type: Optional[str] = None) -> bool:
        """
        判断事件是否为请求

        Args:
            request_type: 可选，指定 request_type 内容是否一致，作为附加条件进行判断，可以用的类型有：
                friend(好友请求)  group(群请求)
        """
        if self.data.get('post_type') == 'request':
            if request_type is None:
                return True
            else:
                return self.data['request_type'] == request_type
        return False

    def is_meta_event(self, meta_event_type: Optional[str] = None) -> bool:
        """
        判断事件是否为元事件

        Args:
            meta_event_type: 可选，指定 meta_event_type 内容是否一致，作为附加条件进行判断，可以用的类型有：
                lifecycle(生命周期)  heartbeat(心跳包)
        """
        if self.data.get('post_type') == 'meta_event':
            if meta_event_type is None:
                return True
            else:
                return self.data['meta_event_type'] == meta_event_type
        return False

    def is_heartbeat(self) -> bool:
        """
        判断事件是否为元事件 - 心跳
        """
        return self.is_meta_event() and self.data.get('meta_event_type') == 'heartbeat'

    def is_connect(self) -> bool:
        """
        判断事件是否为元事件 - 连接
        """
        return self.is_meta_event() and self.data.get('sub_type') == 'connect'

    def is_sub_type(self, sub_type: str = None):
        """
        如果上报事件含消息子类型

        Args:
            sub_type: 可选，指定 meta_event_type 内容是否一致，作为附加条件进行判断，可以用的类型有：
                private(私聊消息)  group(群消息)
                group_upload(群文件上传)  group_admin(群管理员变更)  group_decrease(群成员减少)  group_increase(群成员增加)
                group_ban(群成员禁言)  friend_add(好友添加)  group_recall(群消息撤回)  friend_recall(好友消息撤回)
                group_card(群名片变更)  offline_file(离线文件上传)  client_status(客户端状态变更)  essence(精华消息)
                notify(系统通知)
        """
        if self.data.get('sub_type') is not None:
            if sub_type is None:
                return True
            else:
                return self.data['sub_type'] == sub_type
        return False

    def is_group_message(self, group_id: Optional[Union[str, int, List[Union[str, int]]]] = None):
        """
        判断事件是否为是否为群聊消息

        使用此函数则不需要再使用 is_message()

        但是您还需要注意 sub_type 字段，即使用 is_sub_type() 函数判断：
            normal(常规)、anonymous(匿名)、notice(通知)这三种消息

        Args:
            group_id: 可选，填写后将作为附加条件进行判断是否为这个群/这些群的消息
        """
        if self.data.get('message_type') == 'group':
            if group_id is None or group_id == '' or group_id == ['']:
                return True
            elif type(group_id) == list:
                for id_ in group_id:
                    if self.data['group_id'] == int(id_):
                        return True
            elif self.data['group_id'] == int(group_id):
                return True
        return False

    def is_group_msg(self, group_id: Optional[Union[str, int, List[Union[str, int]]]] = None):
        """
        判断事件是否为是否为群聊消息，效果同 is_group_message()

        使用此函数则不需要再使用 is_message()

        但是您还需要注意 sub_type 字段，即使用 is_sub_type() 函数判断：
            normal(常规)、anonymous(匿名)、notice(通知)这三种消息

        Args:
            group_id: 可选，填写后将作为附加条件进行判断是否为这个群/这些群的消息
        """
        return self.is_group_message(group_id)

    def is_group_request(self, group_id: Optional[Union[str, int, List[Union[str, int]]]] = None):
        """
        判断事件是否为是否为群聊请求

        使用此函数则不需要再使用 is_request()

        但是您还需要注意 sub_type 字段，即使用 is_sub_type() 函数判断：
            add(加群请求)、invite(邀请登录号入群)这两种消息

        Args:
            group_id: 可选，填写后将作为附加条件进行判断是否为这个群/这些群的请求
        """
        if self.data.get('request_type') == 'group':
            if group_id is None:
                return True
            elif type(group_id) == list:
                for id_ in group_id:
                    if self.data['group_id'] == int(id_):
                        return True
            elif self.data['group_id'] == int(group_id):
                return True
        return False

    def is_group_notice(self, notice_type: str, group_id: Optional[Union[str, int, List[Union[str, int]]]] = None):
        """
        判断事件是否为是否为群聊通知

        使用此函数则不需要再使用 is_notice()

        Args:
            notice_type: 判断是否为对应类型的群通知，可以用的类型有：
                group_upload(群文件上传)  group_admin(群管理员变更)  group_decrease(群成员减少)  group_increase(群成员增加)
                group_ban(群成员禁言)  group_recall(群消息撤回)  group_card(群名片变更)  essence(精华消息)

            group_id: 可选，填写后将作为附加条件进行判断是否为这个群/这些群的请求
        """
        if self.data.get('notice_type') == notice_type:
            if group_id is None:
                return True
            elif type(group_id) == list:
                for id_ in group_id:
                    if self.data['group_id'] == int(id_):
                        return True
            elif self.data['group_id'] == int(group_id):
                return True
        return False

    def is_private_message(self, user_id: Optional[Union[str, int, List[Union[str, int]]]] = None):
        """
        判断事件是否为是否为私聊消息

        使用此函数则不需要再使用 is_message()

        Args:
            user_id: 可选，填写后将作为附加条件进行判断是否来自这个用户/这些用户的私聊消息
        """
        if self.data.get('message_type') == 'private':
            if user_id is None or user_id == '' or user_id == ['']:
                return True
            elif type(user_id) == list:
                for id_ in user_id:
                    if self.data['user_id'] == int(id_):
                        return True
            elif self.data['user_id'] == int(user_id):
                return True
        return False

    def is_private_msg(self, user_id: Optional[Union[str, int, List[Union[str, int]]]] = None):
        """
        判断事件是否为是否为私聊消息，效果同 is_group_message()

        使用此函数则不需要再使用 is_message()

        Args:
            user_id: 可选，填写后将作为附加条件进行判断是否来自这个用户/这些用户的私聊消息
        """
        return self.is_private_message(user_id)

    # 消息匹配 #
    def full_match(self, text: Union[str, List[str]]) -> bool:
        """
        判断接收到的消息内容是否完全一致

        使用此函数则不需要再使用 is_message()，但是您还需要注意消息是来自群聊还是私聊，以及群聊的消息类型

        Args:
            text: 文本内容，可以用字符串表示，也可以用含有字符串的列表表示
        """
        if type(text) == list:
            for _ in text:
                if self.is_message() and _ == self.data['message']:
                    return True
            else:
                return False
        elif type(text) == str:
            return self.is_message() and text == self.data['message']

    def keyword_match(self, keyword: Union[str, List[str]]) -> bool:
        """
        判断接收到的消息内容是否包含对应关键词中任意一个

        使用此函数则不需要再使用 is_message()，但是您还需要注意消息是来自群聊还是私聊，以及群聊的消息类型

        Args:
            keyword: 关键词，可以用字符串表示，也可以用含有字符串的列表表示
        """
        if type(keyword) == list:
            for keyword_ in keyword:
                if self.is_message() and keyword_ in self.data['message']:
                    return True
            else:
                return False
        elif type(keyword) == str:
            return self.is_message() and keyword in self.data['message']

    def is_at_me(self):
        """
        判断登录的账号是否被艾特
        """
        return self.keyword_match(keyword=f'[CQ:at,qq={self.self_user_id}]')

    # 身份判断
    def is_super_admin(self):
        """
        判断发言的用户是否为超级管理员

        使用此函数则不需要再使用 is_message()
        """
        return self.is_message() and self.user_id in self.super_admin

    def is_super_user(self):
        """
        判断发言的用户是否为超级用户

        使用此函数则不需要再使用 is_message()
        """
        return self.is_message() and self.user_id in self.super_user

    def is_owner(self, group_id: Optional[Union[str, int, List[Union[str, int]]]] = None):
        """
        判断发言的用户是否为群主

        使用此函数则不需要再使用 is_group_msg()

        Args:
            group_id: 可选，填写后将作为附加条件进行判断是否为这个群/这些群的群主
        """
        return self.is_group_msg(group_id=group_id) and self.data['sender']['role'] == 'owner'

    def is_admin(self, group_id: Optional[Union[str, int, List[Union[str, int]]]] = None):
        """
        判断发言的用户是否为管理员

        使用此函数则不需要再使用 is_group_msg()

        Args:
            group_id: 可选，填写后将作为附加条件进行判断是否为这个群/这些群的管理员
        """
        return self.is_group_msg(group_id=group_id) and self.data['sender']['role'] == 'admin'

    def is_member(self, group_id: Optional[Union[str, int, List[Union[str, int]]]] = None):
        """
        判断发言的用户是否为成员

        使用此函数则不需要再使用 is_group_msg()

        Args:
            group_id: 可选，填写后将作为附加条件进行判断是否为这个群/这些群的成员
        """
        return self.is_group_msg(group_id=group_id) and self.data['sender']['role'] == 'member'

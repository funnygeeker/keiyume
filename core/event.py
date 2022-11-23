#!/usr/bin/python3
# -*- coding: utf-8 -*-
# keiyume_2.0.0-beta.2
# 溪梦框架事件判断模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker
# 参考资料：https://github.com/FloatTech/voidbot
class Event():
    def __init__(self, obj: object) -> None:
        '''将常用的消息字段代入self对象'''
        self.ws = obj.ws
        self.data = obj.data
        self.channel = obj.channel
        self.echo = self.data.get('echo')
        self.time = self.data.get('time')
        self.user_id = self.data.get('user_id')
        self.message = self.data.get('message')
        self.sub_type = self.data.get('sub_type')
        self.group_id = self.data.get('group_id')
        self.post_type = self.data.get('post_type')
        self.message_id = self.data.get('message_id')
        self.self_user_id = obj.self_user_id

    # 消息事件
    def on_echo(self, echo=None) -> bool:
        '【如果上报事件为API调用返回值(即含echo字段)，且echo字段参数一致，返回：真】'
        if self.data.get('echo') != None:
            if echo == None:
                return True
            else:
                return self.data['echo'] == echo
        return False

    def on_notice(self, notice_type: str = None) -> bool:
        '如果上报事件为通知，返回：真'
        if self.data.get('post_type') == 'notice':
            if notice_type == None:
                return True
            else:
                return self.data['notice_type'] == notice_type
        return False

    def on_message(self, message_type: str = None) -> bool:
        '如果上报事件为消息，返回：真'
        if self.data.get('post_type') == 'message':
            if message_type == None:
                return True
            else:
                return self.data['message_type'] == message_type
        return False

    def on_request(self, request_type: str = None) -> bool:
        '如果上报事件为请求，返回：真'
        if self.data.get('post_type') == 'request':
            if request_type == None:
                return True
            else:
                return self.data['request_type'] == request_type
        return False

    def on_meta_event(self, meta_event_type: str = None) -> bool:
        '如果上报事件为元事件，返回：真'
        if self.data.get('post_type') == 'meta_event':
            if meta_event_type == None:
                return True
            else:
                return self.data['meta_event_type'] == meta_event_type
        return False

    def on_heartbeat(self) -> bool:
        '如果上报事件为元事件-心跳，返回：真'
        return self.on_meta_event() and self.data.get('meta_event_type') == 'heartbeat'

    def on_connect(self) -> bool:
        '【如果上报事件为元事件-连接，返回：真】'
        return self.on_meta_event() and self.data.get('sub_type') == 'connect'

    # 消息类型
    def on_group_message(self, group_id=None):
        '''判断接收到的事件是否来自群聊消息(可指定群聊)
        使用此函数则不需要使用：on_message()
        但是您还需要注意：sub_type字段，即使用on_sub_type函数判断：
        normal(常规)、anonymous(匿名)、notice(通知)这三种消息
        group_id:list/str/int(自动判断)'''
        if self.data.get('message_type') == 'group':
            if group_id == None or group_id == '' or group_id == ['']:
                return True
            elif type(group_id) == list:
                for id in group_id:
                    if self.data['group_id'] == int(id):
                        return True
            elif self.data['group_id'] == int(group_id):
                return True
        return False

    def on_group_request(self, group_id=None):
        '''判断接收到的事件是否来自群聊请求(可指定群聊)
        使用此函数则不需要使用：on_request()
        但是您还需要注意：sub_type字段，即使用on_sub_type函数判断：
        add(加群请求)、invite(邀请登录号入群)这两种种消息
        group_id:list/str/int(自动判断)'''
        if self.data.get('request_type') == 'group':
            if group_id == None:
                return True
            elif type(group_id) == list:
                for id in group_id:
                    if self.data['group_id'] == int(id):
                        return True
            elif self.data['group_id'] == int(group_id):
                return True
        return False

    def on_group_notice(self, notice_type, group_id=None):
        '''判断接收到的事件是否来自群聊通知(可指定群聊)
        使用此函数则不需要使用：on_notice()
        但是您还需要注意：sub_type字段，即使用on_sub_type函数判断：
        lucky_king(红包运气王)、honor(群成员荣誉变更)等多种种消息
        group_id:list/str/int(自动判断)'''
        if self.data.get('notice_type') == notice_type:
            if group_id == None:
                return True
            elif type(group_id) == list:
                for id in group_id:
                    if self.data['group_id'] == int(id):
                        return True
            elif self.data['group_id'] == int(group_id):
                return True
        return False

    def on_private_message(self, user_id=None):
        '''判断接收到的事件是否来自私聊(可指定)
        user_id:list/str/int(自动判断)'''
        if self.data.get('message_type') == 'private':
            if user_id == None or user_id == '' or user_id == ['']:
                return True
            elif type(user_id) == list:
                for id in user_id:
                    if self.data['user_id'] == int(id):
                        return True
            elif self.data['user_id'] == int(user_id):
                return True
        return False

    # 消息子类型#
    def on_sub_type(self, sub_type: str = None):
        '如果上报事件含消息子类型，返回：真'
        if self.data.get('sub_type') != None:
            if sub_type == None:
                return True
            else:
                return self.data['sub_type'] == sub_type
        return False

    # 消息匹配#
    def on_full_match(self, keyword: str) -> bool:
        '判断接收到的消息内容是否完全一致'
        return self.on_message() and self.data['message'] == keyword

    def on_keywords_match(self, keywords: list) -> bool:
        '''判断接收到的消息内容是否包含对应关键词组中任意一个
        keyword:list/str(自动判断)'''
        if type(keywords) == list:
            for keyword in keywords:
                if self.on_message() and keyword in self.data['message']:
                    return True
            else:
                return False
        elif type(keywords) == str:
            return self.on_message() and keywords in self.data['message']

    def on_at_me(self):
        return self.on_keywords_match(keywords=f'[CQ:at,qq={self.self_user_id}]')

    # 身份判断
    def is_super_user(self):
        pass

    def is_admin_uesr(self):
        pass

    def is_group_owner(self, group_id=None):
        '''判断用户是否为群主(可指定群聊是否来自群聊列表中任意一个)
        group_id:list/str(自动判断)'''
        return self.on_message() and self.on_group_message(group_id=group_id) and self.data['sender']['role'] == 'owner'

    def is_group_admin(self, group_id=None):
        '''判断用户是否为群聊管理员(可指定群聊是否来自群聊列表中任意一个)
        group_id:list/str(自动判断)'''
        return self.on_message() and self.on_group_message(group_id=group_id) and self.data['sender']['role'] == 'admin'

    def is_group_member(self, group_id=None):
        '''判断用户是否为群聊成员(可指定群聊是否来自群聊列表中任意一个)
        group_id:list/str(自动判断)'''
        return self.on_message() and self.on_group_message(group_id=group_id) and self.data['sender']['role'] == 'member'

    # 结束
    def Result(self):
        '用于返回self的所有内容'
        return self

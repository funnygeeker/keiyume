# 由于赶工所以这里没有多少注释

import re
import time
import traceback

from core.keiyume import plugin, Event, frame, api
from plugins.keiyume_helper import config, tools

menu_text = f"""【溪梦群管助手】
「用户管理」
添加超级用户 | 添加超级管理员
删除超级用户 | 删除超级管理员
查询超级用户 | 查询超级管理员
「词库管理」
添加忽略词 | 删除忽略词
添加违禁词 | 删除违禁词
添加自动审批 | 删除自动审批
「回复管理」
添加随机回复 | 删除随机回复
添加入群欢迎 | 删除入群欢迎
添加违禁回复 | 删除违禁回复
「群聊管理」
撤回全体 | 撤回单人
「插件管理」
重载设置 |
框架：溪梦框架 {frame.get_version()}
版本：2.1"""


def send_result(self, name, success: bool):
    if success:
        if self.is_group_msg():
            api.send_group_msg(self.group_id, f'{name}成功！')
        elif self.is_private_msg():
            api.send_private_msg(self.user_id, f'{name}成功！')
    else:
        if self.is_group_msg():
            api.send_group_msg(self.group_id, f'{name}失败，可能是格式不正确！')
        elif self.is_private_msg():
            api.send_private_msg(self.user_id, f'{name}失败，可能是格式不正确！')


@plugin.reg('event', 768, '群管助手')
def helper_menu(self: Event):
    if self.is_super_admin() or self.is_super_user():
        if self.is_group_msg():
            api.send_group_msg(self.group_id, menu_text)
        elif self.is_private_msg():
            api.send_private_msg(self.user_id, menu_text)


@plugin.reg('event', 768, '添加超级用户')
def add_super_user(self: Event):
    if self.is_super_admin():
        try:
            frame.change_setting('add', 'super_user', int(re.findall(r'\d+', self.cmd_body)[0]))
            send_result(self, '添加', True)
        except:
            send_result(self, '添加', False)


@plugin.reg('event', 768, '删除超级用户')
def del_super_user(self: Event):
    if self.is_super_admin():
        try:
            frame.change_setting('del', 'super_user', int(re.findall(r'\d+', self.cmd_body)[0]))
            send_result(self, '删除', True)
        except:
            send_result(self, '删除', False)


@plugin.reg('event', 768, '添加超级管理员')
def add_super_admin(self: Event):
    if self.is_super_admin():
        try:
            frame.change_setting('add', 'super_admin', int(re.findall(r'\d+', self.cmd_body)[0]))
            send_result(self, '添加', True)
        except:
            send_result(self, '添加', False)


@plugin.reg('event', 768, '删除超级管理员')
def del_super_admin(self: Event):
    if self.is_super_admin():
        try:
            frame.change_setting('del', 'super_admin', int(re.findall(r'\d+', self.cmd_body)[0]))
            send_result(self, '删除', True)
        except:
            send_result(self, '删除', False)


@plugin.reg('event', 768, '查询超级用户')
def find_super_user(self: Event):
    if self.is_super_admin() or self.is_super_user():
        user = ""
        for _ in self.super_user:
            user += f"\n{_}"
        if self.is_group_msg():
            api.send_group_msg(self.group_id, f"超级用户有：{user}")
        elif self.is_private_msg():
            api.send_private_msg(self.user_id, f"超级用户有：{user}")


@plugin.reg('event', 768, '查询超级管理员')
def find_super_admin(self: Event):
    if self.is_super_admin() or self.is_super_user():
        user = ""
        for _ in self.super_admin:
            user += f"\n{_}"
        if self.is_group_msg():
            api.send_group_msg(self.group_id, f"超级管理员有：{user}")
        elif self.is_private_msg():
            api.send_private_msg(self.user_id, f"超级管理员有：{user}")


@plugin.reg('event', 768, '撤回单人')
def del_person_msg(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.is_group_msg():
        try:
            result = re.findall(r'\D*(\d+)\D+(\d+)\D*', self.cmd_body)[0]
            with config.lock:
                msgs = config.db.read_msg(num=int(result[1]), group_id=self.group_id, user_id=int(result[0]))
            if not msgs:
                api.send_group_msg(self.group_id, "没有需要撤回的消息呢！")
                return None
            else:
                if tools.get_role(self.group_id, self.self_user_id) > tools.get_role(self.group_id, int(result[0])):
                    api.send_group_msg(self.group_id, "开始撤回消息...")
                else:
                    api.send_group_msg(self.group_id, "我的权限不够呢！")
                    return None
                for _ in msgs:
                    config.db.write_del_msg(_['message_id'])  # 将对应的消息标记为已撤回
                for _ in msgs:
                    time.sleep(3.3)
                    api.delete_msg(_['message_id'])

            send_result(self, '单人撤回', True)
        except:
            send_result(self, '单人撤回', False)


@plugin.reg('event', 768, '撤回全体')
def del_whole_msg(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.is_group_msg():
        try:
            result = re.findall(r'\D*(\d+)\D*', self.cmd_body)[0][0]
            with config.lock:
                msgs = config.db.read_msg(num=int(result), group_id=self.group_id)
            if not msgs:
                api.send_group_msg(self.group_id, "没有需要撤回的消息呢！")
                return None
            else:
                role_dict = {}
                del_list = []
                self_role = tools.get_role(self.group_id, self.self_user_id)  # 获取自身身份
                for _ in msgs:
                    if not role_dict.get(_['user_id']):  # 如果没有在临时身份列表找到对应用户的身份
                        role_dict[_['user_id']] = tools.get_role(self.group_id, _['user_id'])  # 向 go-cqhttp 请求用户身份
                    if self_role > role_dict[_['user_id']]:
                        del_list.append(_['message_id'])  # 将消息id添加入消息撤回列表
                        config.db.write_del_msg(_['message_id'])  # 将对应的消息标记为已撤回
                for _ in del_list:
                    time.sleep(3.3)
                    api.delete_msg(_)

            send_result(self, '全体撤回', True)
        except:
            send_result(self, '全体撤回', False)


def settings(self, operation: str, path: str, name: str):
    try:
        result = config.change_rule_or_reply_setting(operation, path, [self.cmd_body])
        if self.is_group_msg():
            api.send_group_msg(self.group_id, result)
        elif self.is_private_msg():
            api.send_private_msg(self.user_id, result)
    except:
        send_result(self, name, False)
        print(traceback.format_exc())


# 随机回复的添加与删除
@plugin.reg('event', 768, '添加随机回复 ')
def add_random_reply(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'add', 'reply/random', '添加随机回复')


@plugin.reg('event', 768, '删除随机回复 ')
def del_random_reply(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'del', 'reply/random', '添加随机回复')


@plugin.reg('event', 768, '清除随机回复')
def clear_random_reply(self: Event):
    if self.is_super_admin() or self.is_super_user():
        settings(self, 'clear', 'reply/random', '清除随机回复')


# 入群欢迎的添加与删除
@plugin.reg('event', 768, '添加入群欢迎 ')
def add_welcome_reply(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'add', 'reply/welcome', '添加入群欢迎')


@plugin.reg('event', 768, '删除入群欢迎 ')
def del_welcome_reply(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'del', 'reply/welcome', '添加随机回复')


@plugin.reg('event', 768, '清除入群欢迎')
def clear_welcome_reply(self: Event):
    if self.is_super_admin() or self.is_super_user():
        settings(self, 'clear', 'reply/welcome', '清除入群欢迎')


# 违禁回复的添加与删除
@plugin.reg('event', 768, '添加违禁回复 ')
def add_ban_reply(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'add', 'reply/ban', '添加违禁回复')


@plugin.reg('event', 768, '删除违禁回复 ')
def del_ban_reply(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'del', 'reply/ban', '添加违禁回复')


@plugin.reg('event', 768, '清除违禁回复')
def clear_ban_reply(self: Event):
    if self.is_super_admin() or self.is_super_user():
        settings(self, 'clear', 'reply/ban', '清除违禁回复')


# 自动审批的添加与删除
@plugin.reg('event', 768, '添加自动审批 ')
def add_approval_rule(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'add', 'rule/approval', '添加自动审批')


@plugin.reg('event', 768, '删除自动审批 ')
def del_approval_rule(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'del', 'rule/approval', '添加自动审批')


@plugin.reg('event', 768, '清除自动审批')
def clear_approval_rule(self: Event):
    if self.is_super_admin() or self.is_super_user():
        settings(self, 'clear', 'rule/approval', '清除自动审批')


# 违禁词的添加与删除
@plugin.reg('event', 768, '添加自动审批 ')
def add_ban_rule(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'add', 'rule/ban', '添加违禁词')


@plugin.reg('event', 768, '删除自动审批 ')
def del_ban_rule(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'del', 'rule/ban', '添加违禁词')


@plugin.reg('event', 768, '清除自动审批')
def clear_ban_rule(self: Event):
    if self.is_super_admin() or self.is_super_user():
        settings(self, 'clear', 'rule/ban', '清除违禁词')


# 忽略词的添加与删除
@plugin.reg('event', 768, '添加忽略词 ')
def add_ignore_rule(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'add', 'rule/ignore', '添加忽略词')


@plugin.reg('event', 768, '删除忽略词 ')
def del_ignore_rule(self: Event):
    if self.is_super_admin() or self.is_super_user() and self.cmd_body:
        settings(self, 'del', 'rule/ignore', '添加忽略词')


@plugin.reg('event', 768, '清除忽略词')
def clear_ignore_rule(self: Event):
    if self.is_super_admin() or self.is_super_user():
        settings(self, 'clear', 'rule/ignore', '清除忽略词')


@plugin.reg('event', 768, '重载设置')
def add_reply_rule(self: Event):
    if self.is_super_admin() or self.is_super_user():
        config.load_conf()


@plugin.reg('shell', 768, 'reload_helper', cmd_help="reload_helper:     <无参数>\n    --从配置文件重新加载溪梦助手插件的设置")
def reload_helper(self: Event):
    if self.is_super_admin() or self.is_super_user():
        config.load_conf()

# 规则回复的添加与删除
# @plugin.reg('event', 768, '添加规则回复 ')
# def add_reply_rule(self: Event):
#     if self.is_super_admin() or self.is_super_user() and self.cmd_body:
#         rule = self.cmd_body.split(" ")
#         try:
#             result = config.change_reply_rule_setting('add', rule)
#             if self.is_group_msg():
#                 api.send_group_msg(self.group_id, result)
#             elif self.is_private_msg():
#                 api.send_private_msg(self.user_id, result)
#         except:
#             send_result(self, '添加规则回复', False)
#
#
# @plugin.reg('event', 768, '删除规则回复 ')
# def del_reply_rule(self: Event):
#     if self.is_super_admin() or self.is_super_user() and self.cmd_body:
#         try:
#             result = config.change_reply_rule_setting('del', [self.cmd_body])
#             if self.is_group_msg():
#                 api.send_group_msg(self.group_id, result)
#             elif self.is_private_msg():
#                 api.send_private_msg(self.user_id, result)
#         except:
#             send_result(self, '删除规则回复', False)
#             print(traceback.format_exc())
#
#
# @plugin.reg('event', 768, '清除规则回复')
# def clear_reply_rule(self: Event):
#     if self.is_super_admin() or self.is_super_user():
#         try:
#             result = config.change_reply_rule_setting('clear')
#             if self.is_group_msg():
#                 api.send_group_msg(self.group_id, result)
#             elif self.is_private_msg():
#                 api.send_private_msg(self.user_id, result)
#         except:
#             send_result(self, '清除规则回复', False)

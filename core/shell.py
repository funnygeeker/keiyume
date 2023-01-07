# -*- coding : utf-8-*-
# 溪梦框架：core/shell.py
# 用于管理框架命令行
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume
#
# 参考资料：
# 无

import os
import json
import traceback

from typing import Optional, List

from . import api, public
from . import plugin

logger = public.logger


class Shell:
    def __init__(self, cmd: str, separator: str = " "):
        logger.debug(f"本地命令行执行：\n{cmd}")
        self.raw_cmd: str = cmd
        '原始命令'
        cmd_: List[str] = self.raw_cmd.split(separator, 1)  # 将命令分割为主体和参数
        '分割后的原始命令'
        self.head: str = cmd_[0]
        '命令头'
        self.separator: str = separator
        '命令分隔符'
        self.body: Optional[List[str]] = None
        '命令体'
        if len(cmd_) == 2:  # 判断是否有参数
            self.raw_body: str = cmd_[1]
            '原始命令体'
        else:
            self.raw_body: str = ""
            '原始命令体'

    def builtin(self):
        try:
            if self.head == "help":  # 命令帮助
                print(cmd_help_builtin)
                input("按下回车以显示下一页...")
                if len(cmd_help_plugin) == 1:
                    cmd_help_plugin.append('没有找到添加了命令帮助的插件...')
                for cmd_help in cmd_help_plugin:
                    print(f"\n{cmd_help}")

            elif self.head == "cmd":  # 执行系统命令
                if self.check(1):
                    logger.info(f'命令已结束，状态码：{os.system(self.raw_body)}')

            elif self.head == "close":
                logger.warning('【警告】正在断开连接...')
                public.connect.ws.close()  # 断开连接

            elif self.head == "connect":
                if self.check(1):
                    logger.warning('【警告】正在更改服务器地址...')
                    public.connect.url = self.body[0]
                    if public.connect.connect_state:  # 如果已连接，则需要断开并重连
                        logger.warning('【警告】正在断开连接...')
                        public.connect.ws.close()  # 断开连接

            elif self.head == 'debug':
                logger.info(f"""
用户ID：{public.connect.self_user_id}
连接状态：{public.connect.connect_state}
阻塞中的消息线程：{public.connect.echo_dict}""")

            elif self.head == "del":
                if self.check(1):
                    api.delete_msg(message_id=self.body[0])

            elif self.head == "exit":
                public.connect.exit()

            elif self.head == 'send':
                if self.check(3):
                    if self.body[0] == 'g':
                        api.send_group_msg(group_id=self.body[1], message=self.body[2])
                    elif self.body[0] == 'p':
                        api.send_private_msg(user_id=self.body[1], message=self.body[2])
                    else:
                        logger.warning('【警告】参数错误：命令参数不正确！')

            elif self.head == 'raw_send':
                if self.check(1):
                    data = json.dumps(self.raw_body)
                    logger.info(f'【信息】正在发送原始数据：\n{self.raw_body}')
                    public.connect.ws.send(data)

            # elif self.head[0] == 'state':
            #     pass  # TODO

            elif self.head == 'plugin':
                if self.check(2, warn=False):
                    if self.body[0] == 'e':
                        if plugin.set_plugin_status(folder_name=self.body[1], enable=True):
                            logger.warning("【警告】找不到需要操作的插件！")
                    elif self.body[0] == 'd':
                        if plugin.set_plugin_status(folder_name=self.body[1], enable=False):
                            logger.warning("【警告】找不到需要操作的插件！")
                elif self.check(1):
                    if self.body[0] == 's':
                        print(
                            f"插件状态：{json.dumps(plugin.get_status(), ensure_ascii=False, indent=4)}\n")
                    elif self.body[0] == 'i':
                        print(
                            f"插件信息：{json.dumps(plugin.get_info(), ensure_ascii=False, indent=4)}\n")
            else:
                # logger.warning('【警告】您输入的命令不为内置命令或命令无效！')
                plugin.run('shell', cmd=self.raw_cmd)  # 运行命令插件

        except:
            logger.error(
                f'【错误】内置命令执行出错\n{traceback.format_exc()}')

    def check(self, num: int, warn: bool = True) -> Optional[List[str]]:
        self.body = self.raw_body.split(self.separator, num - 1)  # 根据输入的参数数量分割参数
        if self.body == [""]:
            len_ = 0
        else:
            len_ = len(self.body)  # 计算参数长度
        if len_ >= num:  # 检查参数长度是否符合要求
            return self.body
        else:
            if warn:
                logger.warning(f"【警告】参数缺失：您输入了 {len_} 个参数，但是需要 {num} 个参数才能执行此命令！")
            return None


cmd_help_builtin = '''
【命令帮助 - 内置】

输入格式：命令+空格+参数（每个参数使用空格分隔）（如：xxx xxx）

raw_cmd:    <1个参数：需要执行的命令>
    --在系统中执行对应命令，示例：raw_cmd shutdown -s -t 60
close:      <无参数>
    --断开与 go-cqhttp 的连接一次
connect:    <1个参数：新的 go-cqhttp 服务器所在的地址>
    --断开 go-cqhttp 的连接，并更换 go-cqhttp 所在的地址，示例：connect ws://127.0.0.1:8080
del:        <1个参数：消息id>
    --撤回指定消息id的消息，示例：del 654321
exit:       <无参数>
    --退出此程序
history:    <3个参数：群聊ID（若不限制群聊则为0） 用户ID（若不限制用户则为0） 查询条数>
    --查询最近的历史消息，示例：history 0 123456 10
send:       <3个参数：类型[g:群聊/p:私聊] 用户ID/群聊ID 消息内容>
    --发送消息，示例：send p 123456 你好！
raw_send:   <1个参数：数据(json)>
    --发送原始消息，示例：send_raw {"action": "send_group_msg","raw_body": 
        {'group_id': 123456,'message': '测试','auto_escape': False},"echo": ''}
plugin:     <1个参数：类型[s:插件状态/i:插件信息]；2个参数：类型[e:启用插件/d:禁用插件] 插件文件夹名>
    --启用或禁用插件，示例：plugin d keiyume_helper
'''

cmd_help_plugin: List[str] = ['【命令帮助 - 插件】\n\n输入格式：命令+空格+参数（每个参数使用空格分隔）（如：xxx xxx）']

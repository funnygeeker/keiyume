#!/usr/bin/python3
# -*- coding: utf-8 -*-
# keiyume_2.0.0-beta.2
# 溪梦框架命令执行模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker
import os
import json
from .log import *
from .plugin import Plugin


class Command_Mgr():
    def Send_Result(data, msg='【请求出错】'):
        # TODO 用于远程执行命令并返回结果
        if data != {}:
            pass

    def Cmd_Run(obj: object, cmd: str = '', data: dict = {}):
        '''cmd:命令
        data:传入数据'''
        cmd = cmd.split(' ', 1)  # 将命令分割为主体和参数
        cmd_body = cmd[0]
        if len(cmd) == 2:  # 判断是否有参数
            cmd_args = cmd[1]
        else:
            cmd_args = ''
        try:
            if cmd_body == "/help" or cmd_body == "/帮助":
                print('''
【命令手册】
输入格式：命令+空格+参数（每个参数使用空格分隔）（如：/xxx xxxx）

/cmd：         [1个参数]  命令内容[文本]  （在系统中执行命令）
 - 示例：/cmd shutdown -s -t 60
/close：       [无参数]  （断开与Go-Cqhttp的连接一次）
/del：         [1个参数]  消息id[数字]  （撤回指定消息id的消息）
 - 示例：/del 654321
/exit：        [无参数]  （完全退出程序）
/send:         [3个参数]  类型[g:群聊,p:私聊]  QQ号  消息内容  （发送聊天消息）
 - 示例：/send p 123456 你好！
/send_raw：    [1个参数]  数据[json]  （向连接的Websocket发送原始消息）
 - 示例：/send_raw {"action": "send_group_msg","params": {'group_id': 123456,'message': '测试','auto_escape': False},"echo": ''}
/plugin        [0-2个参数]  （插件相关内容）
''')
                Command_Mgr.Send_Result(data)

            elif cmd_body == "/cmd" or cmd_body == "/命令":
                if True:  # TODO 身份识别
                    result = os.system(cmd_args)
                    logger.info(f'状态码：{result}\n')
                    Command_Mgr.Send_Result(data, msg=result)

            elif cmd_body == "/close" or cmd_body == "/关闭":
                logger.warn('【警告】正在断开连接...\n')
                obj.ws.close()  # 断开连接

            elif cmd_body == '/debug':
                logger.warn(f'{Connect.event_dict}\n')

            elif cmd_body == "/del" or cmd_body == "/撤回":
                Api.delete_msg(message_id=cmd_args)

            elif cmd_body == "/exit" or cmd_body == "/退出":
                if True:  # TODO 身份识别
                    logger.warn('【警告】正在断开连接...\n')
                    obj.ws.close()  # 断开连接
                    logger.warn('【警告】正在退出程序...\n')
                    obj.exit_state = True  # 启用退出状态，下次不再重连
                    # _thread.interrupt_main()  # 结束Python程序

            elif cmd_body == '/send' or cmd_body == "/发送":
                cmd_args = cmd_args.split(' ', 2)  # 拆分为：发送对象的类型，QQ号，内容
                if cmd_args[0] == 'g':
                    Api.send_group_msg(
                        group_id=cmd_args[1], message=cmd_args[2])
                elif cmd_args[0] == 'p':
                    Api.send_private_msg(
                        user_id=cmd_args[1], message=cmd_args[2])
                else:
                    logger.warn('【警告】命令格式不正确！')

            elif cmd_body == '/send_raw':
                data = json.dumps(cmd_args)
                logger.info(f'【信息】正在发送数据(JSON)：\n{cmd_args}\n')
                obj.ws.send(data)

            elif cmd_body == '/state':
                pass  # TODO

            elif cmd_body == '/plugin':
                cmd_args = cmd_args.split(' ', 1)
                if cmd_args == ['']:
                    plugins = {}
                    for location in Plugin.plugins:
                        plugins[location] = []
                        for plugin in Plugin.plugins[location]:
                            plugin = plugin.copy()  # 如果不copy会影响原字典的
                            del plugin['object']
                            plugins[location].append(plugin)
                    print(
                        f"""插件加载状态：{json.dumps(plugins, ensure_ascii=False, indent=4)}

/piugin：       [2个参数]  类型[e:启用,d:禁用]  插件所在的文件夹名 （热启用禁用插件）
""")
                elif cmd_args[0] == 'e':
                    for location in Plugin.plugins:
                        for plugin in Plugin.plugins[location]:
                            if plugin['folder'] == cmd_args[1]:
                                plugin['enable'] = True
                                logger.info(
                                    f"【信息】已启用插件项：{cmd_args[1]} - {plugin['cls_name']}\n")
                elif cmd_args[0] == 'd':
                    for location in Plugin.plugins:
                        for plugin in Plugin.plugins[location]:
                            if plugin['folder'] == cmd_args[1]:
                                plugin['enable'] = False
                                logger.info(
                                    f"【信息】已禁用插件项：{cmd_args[1]} - {plugin['cls_name']}\n")

            else:
                logger.warn('【警告】您输入的命令不为内置命令或命令无效！\n')
                Plugin.Run_Plugin('cmd')  # 运行命令插件

        except:
            logger.error(
                f'【错误】\n{Log.Get_Error()}\n')


if True:  # 这里加if True是避免格式化代码时将这部分放置在代码前段导致导入错误
    from core.api import Api
    from core.connect import Connect

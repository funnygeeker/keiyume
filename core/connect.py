# -*- coding : utf-8-*-
# 溪梦框架：core/connect.py
# 管理框架与 go-cqhttp 服务的连接以及消息的基本处理
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume
#
# 参考资料
# 码农家园 - 将websocket客户端用作python中的类：https://www.codenong.com/26980966/
# 官方文档 - Websocket-Client ：https://websocket-client.readthedocs.io/en/latest/examples.html#customizing-opcode
# CSDN - Python websocket之 websocket-client 库的使用（有BUG）：https://blog.csdn.net/tz_zs/article/details/119363470


import os
import json
import time
import _thread
import threading
import traceback

from typing import Optional, Dict, Union

# Websocket 库
try:
    from websocket import WebSocketApp  # pip3 install websocket-client

except ImportError:
    print('>> 检测到缺少 websocket-client 库，正在安装...')
    os.system('pip3 install websocket-client -i https://mirrors.aliyun.com/pypi/simple/')
    from websocket import WebSocketApp
import websocket

# 计划任务库
try:
    from apscheduler.schedulers.background import BackgroundScheduler
except ImportError:
    print('>> 检测到缺少 apscheduler 库，正在安装...')
    os.system('pip3 install apscheduler -i https://mirrors.aliyun.com/pypi/simple/')
    from apscheduler.schedulers.background import BackgroundScheduler

from . import plugin
from . import public
from .event import Event
from .shell import Shell
from .public import logger


class Connect:
    """
    管理与 go-cqhttp 的连接
    """

    def __init__(self, url):
        self.ws: Optional["WebSocketApp"] = None
        'WebSocket 对象'
        self.url: str = url
        'WebSocket 连接的 URL'
        self.lock: threading.RLock = public.lock
        '线程锁'
        self.scheduler: BackgroundScheduler = BackgroundScheduler(timezone='Asia/Shanghai')
        '任务调度器'
        self.echo_dict: Dict[int, Dict[str, Union[None, dict, threading.Event]]] = {}
        """
        用于存储 api 调用后返回的 event 对象，调用时间，echo字段内容
        {echo(随机数字):{'object': object, 'result': Optional[Dict[str, Any]]（在接收到返回的数据前为None）}, ...}
        """
        self.exit_state = False
        '是否启用了退出状态，如果启用，那么断开连接后将不会重连'
        self.self_user_id = None
        '连接时获取到的登录用户的ID'
        self.connect_state = False
        '连接状态，表示是否正常连接'
        self.reconnect_num = 1
        '连接重试次数计数'
        self.scheduler.start()  # 启动定时任务调度器
        self.scheduler.pause()  # 暂停定时任务调度器

    def on_message(self, ws, message):
        """
        接收到消息时
        """
        threading.Thread(target=Connect._process, kwargs={'self': self, 'message': message}).start()  # 在新线程处理消息

    def on_error(self, ws, error):
        """
        连接出错时（之后会发生连接关闭事件on_close）
        """
        logger.debug(f'重连次数：{self.reconnect_num} 错误：{error}')

    def on_close(self, ws, close_status_code, close_msg):
        """
        连接关闭时
        """
        if self.connect_state:  # 如果是已连接状态下断开的（如果不是在已连接状态下断开的那么就是连接失败）
            self.self_user_id = None  # 清空登录用户的ID
            self.scheduler.pause()  # 暂停任务调度器
            self.connect_state = False  # 连接状态设定为否
            logger.warning(f'【警告】与 go-cqhttp 的连接已断开！')
            plugin.run(location='disconnect')  # 运行断开连接时插件
            # logger.warn(f'【警告】与Go-Cqhttp的连接已断开！ 状态码：{close_status_code} 消息：{close_msg}')
        self.ws = None

    def on_ping(self, message):
        logger.debug(f'接收到 Ping << {message}')

    def on_pong(self, message):
        logger.debug(f'返回 Pong >> {message}')

    def on_open(self, ws):
        """
        连接成功时
        """
        self.reconnect_num = 1  # 重置重新连接次数
        self.connect_state = True  # 连接状态设置为已连接
        logger.info(f'【信息】已成功连接到 go-cqhttp...')
        self.scheduler.resume()  # 恢复定时任务调度器
        plugin.run(location='connect')  # 运行连接时插件

    def command(self, *args):
        """
        运行命令输入功能
        """
        # time.sleep(1)  # 初始化完成后等待一秒显示，否则会影响排版布局，暂时弃用
        while True:
            # time.sleep(1)  # 一样的，也是避免影响排版布局，暂时弃用
            if not self.exit_state:  # 在没有启用退出程序之前一直可以正常输入命令
                try:
                    cmd = input("")

                    Shell(cmd=cmd).builtin()
                except UnicodeDecodeError:
                    self.exit()
            else:
                break  # 结束循环，关闭命令输入功能

    def start(self):
        logger.info(f'【信息】正在连接 go-cqhttp...')
        websocket.enableTrace(False)  # 开启运行状态追踪，debug 的时候可以打开，便于追踪定位问题。
        _thread.start_new_thread(self.command, ())  # 启动单独的命令输入线程
        while True:  # 如果不为退出状态则重新连接，否则立刻断开连接，退出程序
            self.ws = WebSocketApp(self.url,
                                   on_open=self.on_open,
                                   on_message=self.on_message,
                                   on_error=self.on_error,
                                   on_close=self.on_close,
                                   on_ping=self.on_ping,
                                   on_pong=self.on_pong)
            # self.ws.on_open = self.on_open  # 也可以先创建对象再这样指定回调函数。run_forever 之前指定回调函数即可，暂时弃用
            self.ws.run_forever()  # 开始连接（运行时阻塞，断开连接后继续）
            if self.exit_state:  # 如果重连时发现是状态为退出程序，则不进行重连，执行退出程序
                break
            time.sleep(15)  # 每十五秒尝试重新连接一次
            self.reconnect_num += 1  # 增加重新连接计数
            # logger.warn(f'【警告】正在尝试第 {Connect.num} 次重连...\n') # 暂时弃用
        # 退出程序
        logger.debug("正在执行退出前插件...")
        plugin.run(location='exit')  # 运行退出前插件
        logger.warning('【警告】正在退出程序...')
        logger.debug("正在关闭任务调度器...")
        self.scheduler.shutdown()  # 关闭定时任务调度器
        logger.debug("正在结束主线程...")
        _thread.interrupt_main()  # 结束主线程

    def exit(self):
        logger.warning('【警告】正在断开连接...')
        self.exit_state = True  # 启用退出状态，下次不再重连
        if self.ws is not None:
            self.ws.close()  # 断开连接

    def _process(self, message):
        try:
            data = json.loads(message)
            logger.debug(
                f'接收数据：\n{json.dumps(data, ensure_ascii=False, indent=4)}')
        except:
            data = None
            logger.error(
                f'【错误】数据错误 - 接收到的数据类型或格式不正确：\n{traceback.format_exc()}')

        event = Event(data=data)  # 这里用 event 代表消息内包含的事件
        # event = plugin.run(location='before', event=event)  # 运行基本消息识别前的插件，并返回处理后的对象，暂时弃用

        if event.is_message():  # 消息
            pass

        elif event.is_meta_event():  # 元事件
            if event.is_connect():  # 获取登录的机器人QQ号
                self.self_user_id = event.data['self_id']
                logger.info(f'当前登录的QQ号：{self.self_user_id}')

        elif event.is_echo():  # 含echo字段的事件，一般为调用api后的响应数据
            echo = event.data['echo']
            with self.lock:
                if self.echo_dict.get(echo) is not None:
                    self.echo_dict[echo]['result'] = event.data
                    self.echo_dict[echo]['object'].set()  # 取消阻塞调用的API函数

        elif event.is_notice():  # 通知
            pass

        elif event.is_request():  # 请求
            pass

        else:
            logger.error('【错误】无法识别的事件类型！')

        event = plugin.run(event=event, location='event')  # 运行消息处理后的插件，并返回处理后的对象

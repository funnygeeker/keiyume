import time
import _thread
try:
    from websocket import WebSocketApp  # pip3 install websocket-client
except ImportError:
    os.system('pip3 install websocket-client')
    from websocket import WebSocketApp
import websocket
from .event import *
from .tools import *
from .log_mgr import *
from .plugin_mgr import *
# 定时任务模块 pip3 install apscheduler
try:
    from apscheduler.schedulers.background import BackgroundScheduler
except ImportError:
    os.system('pip3 install apscheduler')
    from apscheduler.schedulers.background import BackgroundScheduler

# 参考资料（BUG）：https://blog.csdn.net/tz_zs/article/details/119363470
# DEBUG资料：https://www.codenong.com/26980966/


class Connect_Mgr():
    '''【管理与Go-Cqhttp的Websocket连接】
    使用Connect.start(url='ws://xxx.xxx.xxx.xxx')启动'''
    ws = None
    'websocket对象'
    url = 'ws://127.0.0.1:8080'
    'websocket连接的URL'
    event_dict = {}
    '''用于存储Api调用后event对象，调用时间，echo字段内容
    {echo:{'object':object,'result':dict（在接收到数据前为None）},...}'''
    exit_state = False
    '退出状态，若启用，则下次不再重连'
    self_user_id = None
    '自身QQ号（连接时获取）'
    reconnect_num = 1
    '连接重试次数'
    connecct_state = False
    '是否已连接'
    '''
    time_difference = 0
    '本机时间与服务器时间的时间差，用于实时运算服务器时间以减小误差'
    '''
    lock = threading.RLock()
    '线程锁对象'
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    '定时任务对象'

    def on_message(ws, message):
        '''接收到消息时'''
        # 在新线程处理消息
        threading.Thread(target=Connect_Mgr.Process, kwargs={
                         'message': message}).start()

    def on_error(ws, error):
        '''连接出错时（之后会发生连接关闭事件on_close）'''
        logger.debug(
            f'重连次数：{Connect_Mgr.reconnect_num}\n错误：{error}\n')
        # TODO 断线重连

    def on_close(ws, close_status_code, close_msg):
        '''连接关闭时'''
        Connect_Mgr.self_user_id = None  # 清空机器人QQ号
        scheduler.pause()  # 暂停定时任务调度器
        if Connect_Mgr.connecct_state == True:
            Connect_Mgr.connecct_state = False
            logger.warn(f'【警告】与Go-Cqhttp的连接已断开！\n')
        # logger.warn(f'【警告】与Go-Cqhttp的连接已断开！\n状态码：{close_status_code}\n消息：{close_msg}\n')

    def on_ping(ws, message):
        logger.debug(f'接收到Ping <-：\n{message}\n')

    def on_pong(ws, message):
        logger.debug(f'返回Pong ->：\n{message}\n')

    def on_open(ws):
        '''连接成功时'''
        Connect_Mgr.reconnect_num = 1
        Connect_Mgr.connecct_state = True
        logger.info(f'【信息】已成功连接到Go-Cqhttp...\n')
        scheduler.resume()  # 恢复定时任务调度器
        _thread.start_new_thread(Connect_Mgr.command, ())  # 启动命令输入线程

    def command(*args):
        '''运行命令输入功能'''
        while True:
            time.sleep(1)
            if Connect_Mgr.connecct_state == True:  # 获取连接状态以确定是否启用命令输入
                logger.debug(
                    'core/connect_mgr.py：\n命令输入线程等待输入...\n')
                cmd = input("请输入命令（输入 /help 以获取帮助）:\n>> ")
                if Connect_Mgr.connecct_state == True:
                    logger.debug(f'正在执行命令（控制台）：\n{cmd}\n')
                    Command_Mgr.Cmd_Run(obj=Connect_Mgr, cmd=cmd)
                else:
                    logger.debug(
                        'core/connect_mgr.py：\n命令输入线程已结束...\n')
                    _thread.exit()  # 结束线程
            else:
                logger.debug(
                    'core/connect_mgr.py：\n命令输入线程已结束...\n')
                _thread.exit()  # 结束线程

    def start(url=url):
        logger.info(f'【信息】正在连接Go-Cqhttp...\n')
        scheduler.start()  # 启动定时任务调度器
        scheduler.pause()  # 暂停定时任务调度器
        while 1:  # 此处循环用于自动重连
            # 运行状态追踪，对websocket进行debug的时候可以打开，便于追踪定位问题。
            websocket.enableTrace(False)
            Connect_Mgr.ws = WebSocketApp(url=url,
                                          on_open=Connect_Mgr.on_open,
                                          on_message=Connect_Mgr.on_message,
                                          on_error=Connect_Mgr.on_error,
                                          on_close=Connect_Mgr.on_close)
            # 也可以先创建对象再这样指定回调函数，run_forever之前指定回调函数即可。
            Connect_Mgr.ws.run_forever()  # 开始连接（运行时阻塞，断开连接后继续）
            time.sleep(5)  # 为快速退出，故sleep(5)
            if Connect_Mgr.exit_state == True:  # 如果启用了退出状态则不再重连
                break
            time.sleep(10)
            #logger.warn(f'【警告】正在尝试第 {Connect.num} 次重连...\n')
            Connect_Mgr.reconnect_num += 1
        Plugin_Mgr.Run_Plugin('exit')  # 运行退出前插件
        scheduler.shutdown()  # 退出定时任务调度器
        exit()  # 退出程序

    def Exit():
        '''【结束与Go-Cqhttp的连接】'''
        logger.warn('【警告】正在断开连接...\n')
        Connect_Mgr.ws.close()  # 断开连接
        logger.warn('【警告】正在退出程序...\n')
        Connect_Mgr.exit_state = True  # 启用退出状态，下次不再重连

    '''def Time() -> int:  # 通过获取远程服务器的时间与本地的时间计算出时差，用于计算服务器时间，以减少本地时间与服务器时间差异过大而导致的bug
        return int(time.time()) + Connect.time_difference'''

    def Process(message):
        try:
            data = json.loads(message)
            logger.debug(
                f'接收到：\n{json.dumps(data,ensure_ascii=False,indent=4)}\n')
        except:
            logger.error(
                f'【错误】数据类型或格式不正确：\n{Log_Mgr.Get_Error()}\n')

        obj = type('obj', (), {'ws': Connect_Mgr.ws,
                   'data': data, 'self_user_id': Connect_Mgr.self_user_id})  # 创建一个名为obj的对象，用于传递数据

        obj = Plugin_Mgr.Run_Plugin(
            location='before', obj=obj)  # 运行消息处理前的插件，并返回处理后的对象

        event = Event(obj=obj)  # 这里用event代表消息内包含的事件

        # 校准服务器与本地时差，以减少一些可能存在的错误
        if obj.data.get('time') != None:
            Connect_Mgr.time_difference = obj.data['time'] - int(time.time())

        if event.on_message():  # 消息
            pass

        elif event.on_meta_event():  # 元事件
            if event.on_connect():  # 获取登录的机器人QQ号
                Connect_Mgr.self_user_id = obj.data['self_id']
                logger.info(f'当前登录的QQ号：{Connect_Mgr.self_user_id}\n')

        elif event.on_echo():  # 含echo字段的事件，一般为调用api后的响应数据
            echo = obj.data['echo']
            with Lock:
                if Connect_Mgr.event_dict.get(echo) != None:
                    Connect_Mgr.event_dict[echo]['result'] = obj.data
                    Connect_Mgr.event_dict[echo]['object'].set()

        elif event.on_notice():  # 通知
            pass

        elif event.on_request():  # 请求
            pass

        else:
            logger.error('【错误】无法识别的消息格式！\n')

        obj = Plugin_Mgr.Run_Plugin(
            location='after', obj=obj)  # 运行消息处理后的插件，并返回处理后的对象


if True:  # 这里加if True是避免格式化代码时将这部分放置在代码前段导致导入错误
    scheduler = Connect_Mgr.scheduler
    from .command_mgr import *

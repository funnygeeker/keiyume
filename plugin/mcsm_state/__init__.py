# 导入框架模块
from core.keiyume import *

# 导入另外需要的模块
import json
import requests

# 插件名称
name = '通过MCSM面板查询系统状态'

# 插件作者
author = '稽术宅'

# 插件版本
version = '1.0.0_BETA2'

# 插件说明
description = '使用了MCSM面板的api，当前使用的是定制版（后续转通用版）'

# 兼容性标识（兼容的插件规范版本）
compatible = ['2.0.0-beta.2']


class Main(Event):
    config = {}
    '设置存储变量'
    group_id = []
    '接受命令的群聊'
    admin_user_id = []
    '实例管理员QQ号'

    def __init__(self, obj: object):
        super().__init__(obj)
        '''【符合规范的插件将从这里开始运行】'''
        if self.on_group_message(Main.group_id) and Main.Is_Admin(self):  # 如果上报类型为消息，且发言人为管理员
            # 匹配命令（这里的strip是为了减少某些人习惯性空格的影响）
            if self.message.lower() == '/mcsm 状态':
                # 如果配置了server_address和apikey
                if Main.config['mcsm']['server_address'].strip(' ') != '' and Main.config['mcsm']['apikey'].strip(' ') != '':
                    # 调用MCSM的API
                    result = requests.get(url=f"{Main.config['mcsm']['server_address'].strip(' ')}/api/service/remote_services_system", params={
                        'apikey': Main.config['mcsm']['apikey']})
                    result = json.loads(result.text)  # 将接收到的str转换为dict格式
                    logger.debug(
                        f'MCSM API返回：{json.dumps(result,ensure_ascii=False,indent=4)}\n')  # 记录日志
                    if result.get('status') == 200:  # 请求成功
                        result['data'][0]
                        send_msg = f"""【服务器状态】
CPU：{int(result['data'][0]['system']['cpuUsage']*100)}%
内存：{int(result['data'][0]['system']['memUsage']*100)}%
总内存：{round(int(result['data'][0]['system']['totalmem'])/1024/1024/1024,1)}GB
系统版本：{result['data'][0]['system']['release']}
系统类型：{result['data'][0]['system']['type']}"""
                        Api.send_group_msg(group_id=self.group_id,
                                           message=send_msg)  # 向对应群聊发送消息
                    else:  # 请求失败
                        send_msg = f"【请求出错】\n状态码：{result.get('status')}\n返回内容：{result.get('data')}"
                        Api.send_group_msg(group_id=self.group_id,
                                           message=send_msg)  # 向对应群聊发送消息
                else:
                    send_msg = '未配置服务器地址或API密钥，此功能无法使用！'
                    Api.send_group_msg(group_id=self.group_id,
                                       message=send_msg)  # 向对应群聊发送消息

            elif self.message.lower()[:8] == '/mcsm 查询':
                # 调用MC查询的API
                result = requests.get(url=f"https://motdbe.blackbe.xyz/api", params={
                    'host': self.message.lower()[8:].strip(' ')})
                result = json.loads(result.text)  # 将接收到的str转换为dict格式
                if result['status'] == 'online':
                    status = '在线'
                else:
                    status = '离线'
                send_msg = f"""【MC服务器】
主机：{result['host']}
服名：{result['motd']}
世界：{result['level_name']}
模式：{result['gamemode']}
版本：{result['version']}
延迟：{result['delay']}ms
人数：{result['online']}/{result['max']}
状态：{status}"""
                Api.send_group_msg(group_id=self.group_id,
                                   message=send_msg)  # 向对应群聊发送消息

            elif self.message.lower() == '/mcsm 帮助' or self.message.lower() == '/mcsm help':
                send_msg = """【MCSM指令说明】
/mcsm 开启：启动实例
/mcsm 关闭：关闭实例
/mcsm 重启：重启实例
/mcsm 终止：强制关闭实例
/mcsm 状态：查服务器资源占用
/mcsm 查询：查询MC服务器信息
示例：/mcsm 查询 6.6.6.6:19132
注意：除了查询以外的命令都需先设置配置文件"""
                Api.send_group_msg(group_id=self.group_id,
                                   message=send_msg)  # 向对应群聊发送消息
            # 如果需要执行的命令是下面的任意一种
            elif self.message.lower() == '/mcsm 开启' or self.message.lower() == '/mcsm 关闭' or self.message.lower() == '/mcsm 终止' or self.message.lower() == '/mcsm 重启':
                # 否则如果有设置实例控制以及配置了server_address和apikey
                if Main.config['mcsm']['remote_uuid'].strip(' ') != '' and Main.config['mcsm']['instance_uuid'].strip(' ') != '' and Main.config['mcsm']['server_address'].strip(' ') != '' and Main.config['mcsm']['apikey'].strip(' ') != '':
                    if self.message.lower() == '/mcsm 开启':
                        # 开启实例
                        Main.Instance_Control(
                            self, '/api/protected_instance/open')
                    elif self.message.lower() == '/mcsm 关闭':
                        # 关闭实例
                        Main.Instance_Control(
                            self, '/api/protected_instance/stop')
                    elif self.message.lower() == '/mcsm 终止':
                        # 终止实例
                        Main.Instance_Control(
                            self, '/api/protected_instance/kill')
                    elif self.message.lower() == '/mcsm 重启':
                        # 重启实例
                        Main.Instance_Control(
                            self, '/api/protected_instance/restart')
                else:
                    send_msg = '未完整填写配置文件，此功能无法使用！'
                    Api.send_group_msg(group_id=self.group_id,
                                       message=send_msg)  # 向对应群聊发送消息

    def Is_Admin(self):
        '判断是否为管理员'
        # 如果未设置管理员，则都可以管理
        if Main.admin_user_id == None:
            return True
        for user in Main.admin_user_id:
            if int(user) == self.user_id:
                return True
        return False

    def Instance_Control(self, address):  # 实例控制
        result = requests.get(url=f"{Main.config['mcsm']['server_address']}{address}", params={
            'uuid': Main.config['mcsm']['instance_uuid'],
            'remote_uuid': Main.config['mcsm']['remote_uuid'],
            'apikey': Main.config['mcsm']['apikey']})
        result = json.loads(result.text)  # 将接收到的str转换为dict格式
        logger.debug(
            f'MCSM API返回：{json.dumps(result,ensure_ascii=False,indent=4)}\n')  # 记录日志
        if result.get('status') == 200:  # 请求成功
            send_msg = '已发送请求！'
            Api.send_group_msg(group_id=self.group_id,
                               message=send_msg)  # 向对应群聊发送消息
        else:  # 请求失败
            send_msg = f"【请求出错】\n状态码：{result.get('status')}\n返回内容：{result.get('data')}"
            Api.send_group_msg(group_id=self.group_id,
                               message=send_msg)  # 向对应群聊发送消息


Main.config = Config.Read_Config('./plugin/mcsm_state/config/config.ini')
if Main.config['mcsm']['admin_user_id'].strip(' ').split(' ') == ['']:
    Main.admin_user_id = None
else:
    Main.admin_user_id = Main.config['mcsm']['admin_user_id'].strip(
        ' ').split(' ')
if Main.config['mcsm']['group_id'].strip(' ').split(' ') == ['']:
    Main.group_id = None
else:
    Main.group_id = Main.config['mcsm']['group_id'].strip(' ').split(' ')

Plugin.reg(cls=Main,location='after',sequence=2048)
# location
# 插件运行位置
# start 程序主体运行前
# before 每次消息识别处理前
# after 每次消息识别处理后

# sequence
# 运行优先级
# 用于区分加载顺序
# 数字越小越先执行
# 1024及以下被本框架开发者保留
# 无特殊需求请不要设置小于1024的值
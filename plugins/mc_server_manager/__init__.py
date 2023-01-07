# 导入需要的模块
import os
import json
import requests
# 导入框架模块
from core.keiyume import *
from core import config_tools

# 插件名称
name = 'MC服务管理器'
# 插件作者
author = '稽术宅'
# 插件版本
version = '1.1.0'
# 插件说明
description = '通过 MCSM 面板的 api，来管理 MC 服务器的启动与停止'
# 兼容性标识（兼容的插件规范版本）
compatible = ['2.0.0-beta.3-beta']

plugin_path = os.path.dirname(__file__).replace("\\", "/")  # 自动获取当前插件所在的路径
# 读取配置文件
conf = config_tools.read_ini(f"{plugin_path}/config.ini")

# 实例管理员用户ID
if type(conf['mcsm']['admin_user_id']) is str:  # 将字符串或者字符串列表的配置文件，转换为数字列表，并存入变量
    admin_user_id = [conf['mcsm']['admin_user_id']]
    if admin_user_id == ['']:
        admin_user_id = []
    admin_user_id = config_tools.list_type_convert(int, admin_user_id)
else:
    admin_user_id = config_tools.list_type_convert(int, conf['mcsm']['admin_user_id'])
# 接受命令的群聊
if type(conf['mcsm']['group_id']) is str:  # 将字符串或者字符串列表的配置文件，转换为数字列表，并存入变量
    group_id = [conf['mcsm']['group_id']]
    if group_id == ['']:
        group_id = []
    group_id = config_tools.list_type_convert(int, group_id)
    if not group_id:
        group_id = None
else:
    group_id = config_tools.list_type_convert(int, conf['mcsm']['group_id'])


@plugin.reg(location='event', priority=8192, cmd=["mcsm ", "MCSM "])
def main(self: Event):
    # print(self.is_group_msg(group_id), is_admin(self.user_id))
    if self.is_group_msg(group_id) and is_admin(self.user_id):  # 如果上报类型为消息，且发言人为管理员
        if self.cmd_body[:2] == '查询':
            host = self.cmd_body[2:].strip(' ')
            # 调用MC查询的API
            result = requests.get(url=f"https://motdbe.blackbe.xyz/api", params={'host': host})
            result = json.loads(result.text)  # 将接收到的 str 转换为 dict 格式
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
            api.send_group_msg(self.group_id, send_msg)  # 向对应群聊发送消息

        elif self.cmd_body == '帮助' or self.cmd_body == 'help':
            send_msg = """【MCSM指令说明】
/mcsm 开启：启动实例
/mcsm 关闭：关闭实例
/mcsm 重启：重启实例
/mcsm 终止：强制关闭实例
/mcsm 状态：查服务器资源占用
/mcsm 查询：查询MC服务器信息
示例：/mcsm 查询 6.6.6.6:19132
注意：除了查询以外的命令都需先设置配置文件"""
            api.send_group_msg(group_id=self.group_id,
                               message=send_msg)  # 向对应群聊发送消息
        # 如果需要执行的命令是下面的任意一种
        elif self.cmd_body in ['开启', '关闭', '终止', '重启']:
            # 如果有设置实例控制以及配置了 server_address 和 apikey
            if conf['mcsm']['remote_uuid'] and conf['mcsm']['instance_uuid'] and\
                    conf['mcsm']['server_address'] and conf['mcsm']['apikey']:
                if self.cmd_body == '状态':
                    # 查询状态
                    operate_instance(self, '/api/service/remote_services_system', '查询状态')
                elif self.cmd_body == '开启':
                    # 开启实例
                    operate_instance(self, '/api/protected_instance/open', '开启实例')
                elif self.cmd_body == '关闭':
                    # 关闭实例
                    operate_instance(self, '/api/protected_instance/stop', '关闭实例')
                elif self.cmd_body == '终止':
                    # 终止实例
                    operate_instance(self, '/api/protected_instance/kill', '终止实例')
                elif self.cmd_body == '重启实例':
                    # 重启实例
                    operate_instance(self, '/api/protected_instance/restart', '重启实例')
            else:
                send_msg = '未配置服务器地址或 api 密钥，此功能无法使用！'
                api.send_group_msg(self.group_id, send_msg)  # 向对应群聊发送消息


def is_admin(user_id: int):
    """判断是否为管理员"""
    # 如果未设置管理员，则都可以管理
    if not admin_user_id:
        return True
    return user_id in admin_user_id


def operate_instance(self, address, _type: str = None):  # 实例控制
    result = requests.get(url=f"{conf['mcsm']['server_address']}{address}", params={
        'uuid': conf['mcsm']['instance_uuid'],
        'remote_uuid': conf['mcsm']['remote_uuid'],
        'apikey': conf['mcsm']['apikey']})
    result = json.loads(result.text)  # 将接收到的str转换为dict格式
    logger.debug(
        f'MCSM API返回：{json.dumps(result, ensure_ascii=False, indent=4)}\n')  # 记录日志
    if result.get('status') == 200:  # 请求成功
        if _type == '查询状态':
            send_msg = f"""【服务器状态】
CPU：{int(result['data'][0]['system']['cpuUsage'] * 100)}%
内存：{int(result['data'][0]['system']['memUsage'] * 100)}%
总内存：{round(int(result['data'][0]['system']['totalmem']) / 1024 / 1024 / 1024, 1)}GB
系统版本：{result['data'][0]['system']['release']}
系统类型：{result['data'][0]['system']['type']}"""
        else:
            send_msg = f'已发送{_type}请求！'
        api.send_group_msg(self.group_id, send_msg)  # 向对应群聊发送消息
    else:  # 请求失败
        send_msg = f"【请求出错】\n状态码：{result.get('status')}\n返回内容：{result.get('data')}"
        api.send_group_msg(self.group_id, send_msg)  # 向对应群聊发送消息

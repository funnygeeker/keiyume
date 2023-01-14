import os
import json
import time
import requests
# 导入框架模块
from core.keiyume import *
from core import config_tools

# 插件名称
name = '每日早报'
# 插件作者
author = '稽术宅'
# 插件版本
version = '1.0.1'
# 插件说明
description = '''每天早上六点半，向群里发送当日的早报~
  超级用户和超级管理员都可以在群里或者私聊发送：“早报”命令来立刻获取早报'''
# 兼容性标识
compatible = ['2.0.0-beta.3-beta']
# API 来源：http://api.2xb.cn


plugin_path = os.path.dirname(__file__).replace("\\", "/")  # 自动获取当前插件所在的路径
# 读取配置文件
conf = config_tools.read_ini(f"{plugin_path}/config.ini")

if type(conf['post']['group_id']) is str:  # 对设置为空，或只有单个群聊的情况下，对数据类型进行处理
    enable_group_id = [conf['post']['group_id']]
    if enable_group_id == ['']:
        enable_group_id = []
else:
    enable_group_id = conf['post']['group_id']


@plugin.reg(location="event", priority=8192, cmd="早报")
def main(self: Event):
    if self.is_super_user() or self.is_super_admin():  # 如果是超级用户或者超级管理员
        if self.is_group_msg():  # 如果来自群聊，则向群聊发送早报
            api.send_group_msg(self.group_id, cq.image(get(), cache=0))
        elif self.is_private_msg():  # 如果来自私聊，则向私聊发送早报
            api.send_private_msg(self.user_id, cq.image(get(), cache=0))


def get():
    result = requests.get(url='http://api.2xb.cn/zaob')
    result = json.loads(result.text)  # 将接收到的 str 转换为 dict 格式
    logger.debug(f'早报API返回：{json.dumps(result, ensure_ascii=False, indent=4)}')  # 记录日志
    return result['imageUrl']


def post():
    img = get()  # 向启用了早报的每个群发送早报
    cache = 0
    for group_id in enable_group_id:
        api.send_group_msg(group_id, cq.image(img, cache=cache))
        cache = 1  # 不太希望给别人服务器增加太多负担，除了每天第一次请求，之后的都使用缓存
        time.sleep(5)  # 发那么快，你是想被风控吗?


if int(conf['post']['enable']):  # 如果启用了定时发送早报
    scheduler.add_job(func=post, trigger='cron', hour=6, minute=30, second=0, id='plugin_morning_post')

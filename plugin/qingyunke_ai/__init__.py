# 导入框架模块
from core.keiyume import *

# 导入另外需要的模块
import re
import json
import requests

# 插件名称
name = '智能聊天机器人'

# 插件作者
author = '稽术宅'

# 插件版本
version = '1.0.0'

# 插件说明
description = '使用了青云客网络的api'

# 兼容性标识（兼容的插件规范版本）
compatible = ['2.0.0-beta.2']


class Main(Event):
    def __init__(self, obj: object):
        super().__init__(obj)

        '''【符合规范的插件将从这里开始运行】'''

        if self.on_group_message() and self.on_at_me():
            msg=re.sub('\[CQ:(.*)\]','',self.message) # 去除所有CQ码
            msg=msg.lstrip() # 去除艾特后面可能有的空格
            if msg != '':#仅在消息不为空时处理消息
                # 调用青云客网络的API
                result = requests.get(url='http://api.qingyunke.com/api.php',params={'key':'free','appid':'0','msg':msg})
                result = json.loads(result.text) # 将接收到的str转换为dict格式
                logger.debug(f'青云客API返回：{json.dumps(result,ensure_ascii=False,indent=4)}\n')# 记录日志
                send_msg = result['content'].replace(f'菲菲','溪梦')
                send_msg = re.sub('{face:(.*)}','',send_msg) # 替换掉API返回的表情码
                send_msg = send_msg.replace('{br}','\n') # 替换掉API返回的换行符
                Api.send_group_msg(group_id=self.group_id,message=send_msg) # 向对应群聊发送消息

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
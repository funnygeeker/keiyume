# 导入需要的模块
import re
import json
import requests
# 导入框架模块
from core.keiyume import *

# 插件名称
name = '智障聊天机器人'
# 插件作者
author = '稽术宅'
# 插件版本
version = '1.1.0'
# 插件说明
description = '使用了青云客网络的 api 实现的智能聊天。'
# 兼容性标识
compatible = ['2.0.0-beta.3']


# 在此特别感谢“青云客网络”的 API：http://api.qingyunke.com/


@plugin.reg(location='event', priority=8192)
def main(self: Event):
    if self.is_group_msg() and self.is_at_me():
        msg = re.sub(r'\[CQ:(.*)]', '', self.message)  # 去除所有CQ码
        msg = msg.strip(' ')  # 去除文本左右可能有的空格
        if msg and '给我管理员' not in msg:  # 仅在处理后的消息不为空时继续处理消息
            # 调用青云客网络的API
            result = requests.get(url='http://api.qingyunke.com/api.php',
                                  params={'key': 'free', 'appid': '0', 'msg': msg})
            result = json.loads(result.text)  # 将接收到的 str 转换为 dict 格式
            logger.debug(f'青云客API返回：{json.dumps(result, ensure_ascii=False, indent=4)}')  # 记录日志
            send_msg = result['content'].replace(f'菲菲', '溪梦')  # 更改...机器人昵称，咳咳[doge]
            send_msg = re.sub('{face:(.*)}', '', send_msg)  # 替换掉API返回的表情码
            send_msg = send_msg.replace('{br}', '\n')  # 替换掉API返回的换行符
            api.send_group_msg(self.group_id, send_msg)  # 向对应群聊发送消息

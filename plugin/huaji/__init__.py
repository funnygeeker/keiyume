# 导入框架模块
from core.api import *
from core.event import *
from core.log_mgr import *

# 导入另外需要的模块

import time
from random import randint

# 插件名称
name = '滑稽'

# 插件作者
author = '稽术宅'

# 插件版本
version = '1.0.0'

# 运行优先级
# 用于区分加载顺序
# 数字越小越先执行
# 1024及以下被本框架开发者保留
# 无特殊需求请不要设置小于1024的值
sequence = 1024

# 插件说明
description = '禁止洗滑稽！！！'

# 插件运行位置
# start 程序主体运行前
# before 每次消息识别处理前
# after 每次消息识别处理后
# exit 程序正常退出后
# cmd 命令被识别为非内置/无效时
location = 'after'

# 兼容性标识（兼容的插件规范版本）
compatible = ['2.0.0_BETA1']


class Main(Event):
    def __init__(self, obj: object):
        super().__init__(obj)

    def Run(self, *args, **kwargs):
        '''【符合规范的插件将从这里开始运行】'''

        # 最简单插件例子
        '''if self.on_group_message(666666666) and self.on_keyword_match('你好'):
            #Api.send_group_message(666666666,'你好啊！')'''

        # 原始插件示例
        '''if self.data.get('raw_message') != None and self.data.get('group_id') == 666666666:
            if '你好' in self.data['raw_message']:
                self.ws.send(json.dumps({
                    "action": "send_group_msg",
                    "params": {
                        'group_id': 666666666,
                        'message': '你好啊！',
                        'auto_escape': False
                    },
                    "echo": ''}))'''

        # 标准插件示例
        if self.on_group_message() and self.on_keywords_match(['3cc6226a86ebdf691ff69e1432896720.image', 'bb4f5677543201c8f5b9a638a2534471.image']):
            logger.info(f'【收到来自群聊：{self.group_id} 的滑稽】\n')
            replys = ['禁止洗滑稽！', '滑稽已经很干净了，不需要洗了嘛！',
                      '洗什么洗，再洗就把你丢进洗衣机:(', '洗什么滑稽，还不快去洗一下你自己）', '洗完记得把滑稽晒干！']
            reply = replys[randint(0, len(replys)-1)]
            time.sleep(1)
            Api.send_group_msg(group_id=self.group_id, message=reply)

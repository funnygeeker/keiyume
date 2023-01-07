# 导入需要的模块
from random import randint
# 导入框架模块
from core.keiyume import *

# 插件名称
name = '禁止洗滑稽！'
# 插件作者
author = '稽术宅'
# 插件版本
version = '1.1.0'
# 插件说明
description = '当对方在群聊中发送洗滑稽的 GIF 图片时，将进行关于这个图片的随机回复。\n  目前只收录了部分的滑稽图片的文件名。'
# 兼容性标识
compatible = ['2.0.0-beta.3']


@plugin.reg(location='event', priority=8192)
def main(self: Event):
    if self.is_group_msg() and self.keyword_match(
            ['3cc6226a86ebdf691ff69e1432896720.image', 'bb4f5677543201c8f5b9a638a2534471.image']):
        logger.info(f'收到来自群聊：{self.group_id} 的洗滑稽图片')
        reply = ['禁止洗滑稽！（╯‵□′）╯︵┴─┴', '滑稽已经很干净了，不需要再洗了嘛！( ‘-ωก̀ )',
                 '洗什么洗，再洗就把你丢进洗衣机(￢_￢)', '这么闲着没事洗滑稽，还不快去洗一下你自己٩(๑`^´๑)۶',
                 '洗完记得把滑稽晒干！(*´∀`)',
                 '能不能不要洗滑稽呢(〟-_・)ﾝ?', '你竟敢洗滑稽，真是太过分了！(。・`ω´・)', '请不要洗滑稽，谢谢！(｡ì _ í｡)']
        reply = reply[randint(0, len(reply) - 1)]
        api.send_group_msg(self.group_id, reply)

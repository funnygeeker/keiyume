## 插件版本迁移

### 从2.0.0-beta.2 迁移至 2.0.0-beta.3
#### 迁移说明
- 由于更改的内容较多，请重新阅读文档并重新编写插件

#### 2.0.0-beta.3 插件示例
```
# 导入框架模块
from core.keiyume import plugin, api, Event
# 插件名称
name = '示例插件'
# 插件作者
author = '不想写文档的程序员'
# 插件版本
version = '1.0.0'
# 插件说明
description = '''鹦鹉学舌，你说什么他就回什么'''
# 兼容性标识（兼容的插件规范版本）
compatible = ['2.0.0-beta.3']

@plugin.reg(location='after',priority=4096)
def main(self: Event):
   if self.is_group_msg():  # 如果为群聊消息
      api.send_group_msg(self.group_id, self.msg)
   elif self.is_private_msg():  # 如果为私聊消息
      api.send_private_msg(self.user_id, self.msg)
```

### 从2.0.0-beta.1 迁移至 2.0.0-beta.2

#### 迁移说明
- 类名不再限制为 `Main` ，可以在格式允许范围内随意命名
- 原先的导入框架模块统一为一条：`from core.keiyume import *`
- 兼容性标识更改为 `['2.0.0-beta.2']` ，此版本不兼容 `2.0.0_BETA1` 的插件
- 将 `sequence` （运行优先级）和 `location` （运行位置）移动到插件注册函数了
- 现在需要在最后几行加上插件注册函数 `Plugin.reg(cls=类名,location=运行位置,sequence=运行优先级)` 以注册插件

?>详细内容请观察以下不同版本插件的变化：

#### 2.0.0-beta.2 插件示例
```
# 导入框架模块
from core.keiyume import *
# 导入另外需要的模块
import time
from random import randint
# 插件名称
name = '你好'
# 插件作者
author = '稽术宅'
# 插件版本
version = '1.0.0'
# 插件说明
description = '你好啊！'
# 兼容性标识（兼容的插件规范版本）
compatible = ['2.0.0-beta.2']
class Main(Event):
    def __init__(self, obj: object):
        super().__init__(obj)
        '''【符合规范的插件将从这里开始运行】'''
        if self.is_group_message() and self.on_keyword_match('你好'):
            Api.send_group_msg(self.group_id,'你好啊！')
Plugin.reg(cls=Main,location='after',sequence=1024)
```
#### 2.0.0-beta.1 插件示例
```
# 导入框架模块
from core.api import *
from core.event import *
from core.log_mgr import *
# 导入另外需要的模块
import time
from random import randint
# 插件名称
name = '你好'
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
description = '你好啊！'
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
        if self.on_group_message() and self.on_keyword_match('你好'):
            Api.send_group_msg(self.group_id,'你好啊！')
```
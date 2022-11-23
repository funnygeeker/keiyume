## 快速入门

### 前言
- 想要自己写一个插件吗？那就立刻开始行动吧！
- 如果您未完成 **Python** 语言的入门学习，请前往 [菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html) 完成基础教程的学习

### 注意事项
- 源码中大写开头的函数可能在后续版本中变动较大，或可能会影响框架运行，不是很建议使用


## 概念说明
### 运行位置
- 表示每个注册的插件类在处理消息时所在的运行位置，常用的是 `after`
- 目前版本支持以下运行位置：
- `start` 程序主体运行前
- `before` 每次消息识别处理前
- `after` 每次消息识别处理后

### 运行顺序
- 表示每个注册的插件类在对应运行位置的执行顺序
- 若插件运行顺序相等，则插件运行顺序可能不定
- 你可以在一个插件中注册两个不同的插件类，以实现获取中间的插件执行所用的时间
- 也可以将专门用于修改事件内容的插件放在前面，来达到特殊的效果
- 如果无特殊需求，请尽量不要将运行顺序设置为 `1024` 以下，`1024` 以下被框架开发者保留，可能在发布其他特殊插件时需要高优先级


## 创建插件
> 读完后记得再看看插件示例！

1. 您需要在 `plugin` 文件夹下命名一个：英文（可以用`_`连接），开头不为数字，不含空格的文件夹
2. 在您之前创建的文件夹中创建 `__init__.py` 文件
3. `__init__.py` 文件中使用 `from core.keiyume import *` 导入框架必备的模块
4. 设置必备变量如下：
```
name = '插件名'
author = '作者名'
version = '插件版本'
description = '插件说明'
compatible = ['2.0.0-beta.2']
```
4. 创建一个类，类名可以任意，该类需要继承 `Event` 类，并定义初始化函数 `__init__(self, obj)`
5. 初始化函数下加入 `super().__init__(obj)` 以在初始化时调用父类
6. 在 `super().__init__(obj)` 后面填写你的插件代码（注意缩进）
7. 使用 `Plugin.reg(cls=类名,location='运行位置',sequence=运行顺序)` 注册插件

### 2.0.0-beta.2 插件示例
```
# 导入框架模块
from core.keiyume import *
# 导入另外需要的模块
import time
from random import randint
# 插件名称
name = '滑稽'
# 插件作者
author = '稽术宅'
# 插件版本
version = '1.0.0'
# 插件说明
description = '禁止洗滑稽！！！'
# 兼容性标识（兼容的插件规范版本）
compatible = ['2.0.0-beta.2']
class Main(Event):
    def __init__(self, obj: object):
        super().__init__(obj)
        '''【符合规范的插件将从这里开始运行】'''
        # 最简单插件例子
        if self.on_group_message(666666666) and self.on_keyword_match('你好'):
            #Api.send_group_message(666666666,'你好啊！')
Plugin.reg(cls=Main,location='after',sequence=1024)
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
```

## 公开插件
- 您可以在 Github 发布您的插件，并在存储库的 About 中填入 `溪梦框架插件` 关键词
- 在当前版本中，您也可以 [加入QQ群](https://jq.qq.com/?_wv=1027&k=aCSDHr8h) 提交您的插件
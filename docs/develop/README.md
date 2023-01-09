## 快速入门

### 前言
- 想要自己写一个插件吗？那就立刻开始行动吧！
- 如果您未完成 **Python** 语言的入门学习，请前往 [菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html) 完成基础教程的学习


## 概念说明
!> 首先，您需要知道，由于当前的文档作者非常不会表述。因此，有些内容表达的可能非常不规范，请谅解。
### 运行位置（后续可能会改名为插件类型）
- 表示每个注册的插件类在处理消息时所在的运行位置，常用的是 `event`
- 目前版本支持以下运行位置：
- `exit` 程序因命令/错误退出之前
- `start` 连接 go-cqhttp 服务前
- `event` 每次接收到上报的事件之后
- `shell` 框架执行非内置控制台命令
- `connect` go-cqhttp 服务连接成功之后
- `disconnect` 断开 go-cqhttp 服务之后

> 需要注意的是，只有 `connect` 和 `event` 位置可以正常的调用 `api`，`shell` 位置仅在连接正常时可以调用 `api`。只有 `event` 位置可以获取到完整的事件上报，`shell` 位置仅可以获取 `self.cmd_body`

### 优先级
- 表示每个注册的插件在对应运行位置的优先级
- 若插件优先级相等，则插件运行优先级会根据插件实际的导入顺序排序
- 你可以在一个插件中注册两个不同的插件，通过调整不同的优先级，来实现不一样的效果，
- 比如：获取两个插件之间运行所消耗的时间。也可以将专门用于修改事件内容的插件放在前面，来达到特殊的效果
- 如果无特殊需求，请尽量不要将运行顺序设置为 `2048` 以下，`2048` 以下被框架开发者保留，可能在发布一些特殊插件时需要高优先级
- 一般的消息插件优先级请设置为 `4096` 及以后，一些需要高优先级的的特殊插件设置为 `2048` 到 `4095` 之间，这样的话可以预留一定的优先级空位，让一些特殊插件可以正常运行。

## 创建插件
> 读完后记得再看看插件示例！

1. 您需要在 `plugins` 文件夹下命名一个：英文（可以用`_`连接），开头不为数字，不含空格的文件夹，如：
    ```
   ./plugins/test
   
    keiyume (项目根目录)
    ├── core
    │   └── ...
    ├── plugins
    │   └── test
    └── main.py
    ```
2. 在您之前创建的文件夹中创建 `__init__.py` 文件，如：
   ```
   ./plugins/test/__init__.py
   
    keiyume (项目根目录)
    ├── core
    │   └── ...
    ├── plugins
    │   └── test
    │       └── __init__.py
    └── main.py
   ```
3. `__init__.py` 文件中使用 `from core.keiyume import *` 导入框架必备的模块
   >实际情况下，更建议您按需导入：如 `from core.keiyume import plugin, Event, logger`

4. 设置插件必须的变量如下：
   ```
   name = '插件名'
   author = '作者名'
   version = '插件版本'
   description = '插件说明'
   compatible = ['2.0.0-beta.3']
   ```

5. 创建一个函数，函数名可以任意，并添加一个变量作为参数 （建议命名为`self`或`event`），然后该参数的类型注释填 `Event`（在此之前请确保你导入了`core.keiyume`中的`Event`），如：
   ```
   def main(self: Event):
      pass
   ```

6. 使用 `@plugin.reg(location='运行位置',priority=运行优先级)` 这个装饰器，添加在函数前注册插件（在此之前请确保你导入了`core.keiyume`中的`plugin`）
   ```
   @plugin.reg(location='event',priority=4096)
   def main(self: Event):
      pass
   ```

7. 接下来你可以在刚刚创建的函数里完成你的代码了~


### 2.0.0-beta.3 插件示例
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

@plugin.reg(location='event',priority=4096)
def main(self: Event):
   if self.is_group_msg():  # 如果为群聊消息
      api.send_group_msg(self.group_id, self.msg)
   elif self.is_private_msg():  # 如果为私聊消息
      api.send_private_msg(self.user_id, self.msg)
```

## 运行位置
在框架中注册插件的函数时，你需要在注册插件的装饰器中添加一个运行位置，下面我们来讲解一下不同的位置有什么区别。
### start
示例：`@plugin.reg(location='start',priority=4096)`
- 在这个位置注册的插件：会在全部插件导入之后，连接 go-cqhttp 之前运行。仅运行一遍，适合在其他插件运行之前，向框架中注册依赖项。
- 又或者运行一些其他的前置功能，由于不是很常用，而且这是一个试验性的功能，所以这里不再详细描述。

### shell
示例：`@plugin.reg(location='shell',priority=4096, cmd='命令', cmd_help='命令帮助')`
- 在这个位置注册的插件：会在向框架控制台输入命令时，如果命令不为内致命令时，将会根据优先级，先后按顺序匹配并执行插件的命令
- 注册此插件时，需要传入参数 `cmd` 表示命令头，可选传入参数 `cmd_help` 表示命令帮助，命令帮助会在控制台运行命令 `help` 时，在输出的插件命令帮助中显示
- 当插件被触发运行时，可以通过 `self.cmd_body` 来获取输入的命令中，原始的命令删除命令头之后的命令体部分，示例如下：
插件：

```
from core.keiyume import plugin, Event
name = '控制台命令示例插件'
author = '不想写文档的程序员'
version = '1.0.0'
description = '''这是一个测试插件'''
compatible = ['2.0.0-beta.3']

@plugin.reg(location='shell', priority=4096, cmd='test')
def main(self: Event):
   print(self.cmd_body)
```
输入的命令：

```
test123abc
```
控制台的输出：

```
123abc
```
  
### connect
- 在这个位置注册的插件：会在每次连接 go-cqhttp 成功之后，接收事件开始前，根据优先级顺序运行一次。

### disconnect
- 在这个位置注册的插件：会在每次连接 go-cqhttp 从连接成功变为断开连接状态之后，根据优先级顺序运行一次
- 你可以在这个位置注册插件来实现登录的账号掉线，但是又没断网时的邮件告警等

### event
- 这是一个**最常用**的运行位置，会在每次接收到 go-cqhttp 上报的事件时根据优先级顺序运行一次插件
- 各种群管机器人，聊天机器人，api 调用和回复基本都在这里实现。
- 注册此插件时，**可选**传入参数 `cmd` 表示命令头，将其注册为消息命令插件。
- 需要注意的是，为了防止此类命令被误调用，您可以在框架配置文件中的 `cmd_prefix`（命令前缀）选项，为所有命令统一添加一个前缀。默认的前缀为 `/`
- 当插件被触发运行时，可以通过 `self.cmd_body` 来获取输入的命令中，原始的命令删除命令头之后的命令体部分，示例如下：
插件：

```
from core.keiyume import plugin, Event
name = '消息命令示例插件'
author = '不想写文档的程序员'
version = '1.0.0'
description = '''这是一个测试插件'''
compatible = ['2.0.0-beta.3']

@plugin.reg(location='event', priority=4096, cmd='test')
def main(self: Event):
   if self.is_group_msg():
      api.send_group_msg(self.group_id, self.cmd_body)
```
向群里发送的消息：

```
test123abc
```
在群里收到的消息：

```
123abc
```


## 进阶功能
### 修改事件
#### 说明
高优先级的插件通过修改传入的 `self.data` 或 `self.cmd_body`，将修改应用到低优先级的插件
#### 示例
```
from core.keiyume import plugin, Event
name = '修改事件示例插件'
author = '不想写文档的程序员'
version = '1.0.0'
description = '''这是一个测试插件'''
compatible = ['2.0.0-beta.3']

# 高优先级的插件
@plugin.reg(location='event', priority=2048)
   if self.is_msg():
      self.data['message'] == "114514"

# 低优先级的插件
@plugin.reg(location='event', priority=4096)
   if self.is_msg():
      print(self.msg)
```
向登录账号发送的消息：
`你好`

控制台输出的消息：
`114514`


### 传递数据
- 您可以在高优先级的插件中通过 `self.xxxx = 变量` 来为实例变量赋值
- 然后在低优先级的插件中通过 `self.xxxx` 来读取实例变量，
- 这样可以在同一运行位置的不同优先级插件之间传递数据，
- 这可以实现，如：处理一个消息需要的时间，等等
- 需要注意的是，有以下**保留字**不能用于命名：

|     self.data     |    self.ws    |   self.echo   | self.super_user | self.super_admin |
|:-----------------:|:-------------:|:-------------:|:---------------:|:----------------:|
| self.self_user_id |   self.time   | self.user_id  |    self.msg     |  self.cmd_body   |
|   self.message    | self.sub_type | self.group_id | self.post_type  | self.message_id  |


### 中断插件
- 在对应插件函数运行过程中，您可以通过 `return True` 或者返回非空内容，来对插件进行中断。
- 中断之后，本次将会跳过该运行位置中，更低优先级的插件
- 如果您仅需要立刻结束当前运行的插件，请 `return False` 或是 `return None`


### 日志记录
导入：`from core.keiyume import logger`
#### 说明
- 您可以可以使用：`logger.xxxxx("日志内容")` 来向日志文件中记录，并向控制台输出不同等级的日志
- 在框架默认设置中：信息等级以上的日志会在控制台输出，其余等级的日志均会记录到日志文件。
#### 示例
```
logger.debug("这是一个调试日志")
logger.info("这是一个信息日志")
logger.warning("这是一个警告日志")
logger.error("这是一个错误日志")
logger.critical("这是一个严重错误日志")
```


### 定时任务
#### 说明
框架使用 `APScheduler` 用于管理各种定时任务，您可以通过 `from core.keiyume import scheduler` 来导入已配置好的调度器

!>一般情况下不建议您重新创建一个调度器，也不建议对现有的调度器使用 `.resume()` `.start()` `.pause()` `.shutdown()` 函数
- 因为框架会对该调度器进行自动管理，比如：与 go-cqhttp 断开连接时自动暂停调度器，以免发生意外

#### 示例
添加一个每天 18点30分 调用指定函数的任务：
`scheduler.add_job(func=指定函数, trigger='cron', hour=18 ,minute=30 ,second=0 ,kwargs=（这里需要以字典的形式向需要调用的函数传入参数）, id='任务id')`

暂停上面的任务：
`scheduler.pause_job('任务id')`

恢复上面的任务：
`scheduler.resume_job('任务id')`

移除上面的任务：
`scheduler.remove_job('任务id')`

添加一个一次性（60秒后运行）的任务：
`scheduler.add_job(func=指定函数, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+60)), kwargs=（这里需要以字典的形式向需要调用的函数传入参数）,id='任务id')`

更多高级用法请阅读：[官方文档](https://apscheduler.readthedocs.io/en/3.x/)


## 注意事项
### 多线程
本框架是一个多线程框架，因此，在您使用的时候，部分功能可能无法在多线程下实现，或者需要额外进行处理。

比如：`Sqlite` 可能需要在每次插件运行的时候进行实例化，不可以将实例化后的对象留到下次调用。

### 保留字
保留字是 `溪梦框架` 中一些已经被赋予特定意义的单词，这就要求开发者在开发插件时，**尽量避免**使用这些保留字作为标识符给变量、函数、类、模板以及其他对象命名。
当前版本中所有的保留字如下所示：

|   x6   |   cq   |   api   |   frame   |
|:------:|:------:|:-------:|:---------:|
| plugin |  Log   |  Event  |  Sqlite   |
| logger | config | connect | scheduler |

## 公开插件
- 您可以在 Github 发布您的插件，并在存储库的 About 中填入 `溪梦框架插件` 关键词
- 在当前版本中，您也可以 [加入QQ群](https://jq.qq.com/?_wv=1027&k=aCSDHr8h) 提交您的插件

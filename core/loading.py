# -*- coding : utf-8-*-
# 溪梦框架：core/loading.py
# 用于管理框架运行的资源初始化
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume
# 生成控制台上符号组成的字母
# http://patorjk.com/software/taag/#p=display&h=1&f=Slant&t=Keiyume
# http://patorjk.com/software/taag/#p=display&h=1&f=Ivrit&t=Keiyume
import os
import sys
import time
from . import config_tools, public


def start():
    print(r'''
=======================【正在初始化】=======================

      _  __      _                                
     | |/ / ___ (_) _   _  _   _  _ __ ___    ___ 
     | ' / / _ \| || | | || | | || '_ ` _ \  / _ \
     | . \|  __/| || |_| || |_| || | | | | ||  __/
     |_|\_\\___||_| \__, | \__,_||_| |_| |_| \___|
                    |___/                         

        欢迎使用：溪梦框架 v2.0.0-beta.3 20230107

============================================================
''')


def info():
    print('''  在爱发电中支持一下作者：https://afdian.net/@funnygeeker
  Github地址：https://www.github.com/funnygeeker/keiyume
  Bilibili主页：https://b23.tv/b39RG2r
  溪梦社区：https://keiyume.com
  Python小白练手作品，大佬轻喷！
  框架交流QQ群：332568832

============================================================''')
    time.sleep(2)
    print('''
  【感谢捐助】
  还没有人捐助呢~

  【特别致谢】
  QQ：98252***0（基础技术指导）  QQ：31298***8（代码规范指导）

============================================================\n''')
    # 进度条，只是为了视觉效果
    for i in range(1, 51):
        print("\r", end="")
        print(f"{i * 2}%: ", "▋" * (i // 2), end="")
        sys.stdout.flush()
        time.sleep(0.01)
    print('\n\n============================================================\n')
    time.sleep(1)


def create_path(path):
    """
    创建一个插件目录

    Args:
        path: 插件目录所在的位置
    """
    if not os.path.exists(path):  # 若不存在路径，则自动创建
        os.makedirs(path)
        print(f"""   404 NOT FOUND - 哎呀，你的插件目录不见了！(；´ﾟωﾟ｀)   

        但是别担心，溪梦已经在 {path} 
        为你重新创建了一个干净的插件目录哦！(●ˇ∀ˇ●)
        小提示：框架需要和插件一起使用才能发挥出最佳效果呐~
        阁下可以退出程序，并在插件目录中添加需要的插件，然后再次启动框架哦！(●'◡'●)ﾉ♥
""")
        end = input("按下回车键退出...")
        exit()


def create_config():
    if not config_tools.create_file(file="./config.ini", text=config_file):
        print("""   404 NOT FOUND - 哎呀，你的配置文件不见了！(；´ﾟωﾟ｀)   

        但是别担心，溪梦已经在 ./config 这个文件夹里
        为你重新创建了一份名为 config.ini 的配置文件哦！(●ˇ∀ˇ●)
        别忘了根据需求修改这份配置文件，然后再次启动框架哦！(●'◡'●)ﾉ♥
""")
        end = input("按下回车键退出吧！")
        exit()


def wizard():
    """
    初次使用的向导函数
    """
    while True:
        result = input("""【 欢迎使用 keiyume - 溪梦框架 】
这是一份简单的声明，请仔细阅读，呐：

一切开发旨在学习，请勿用于非法用途
- keiyume 是完全免费且开放源代码的软件，仅供学习和娱乐用途使用
- keiyume 不会通过任何方式强制收取费用，或对使用者提出物质条件
- keiyume 由整个开源社区维护，并不是属于某个个体的作品，所有贡献者都享有其作品的著作权

keiyume 采用 AGPLv3 协议开源。为了整个社区的良性发展，我们强烈建议您做到以下几点：
- 不鼓励，不支持一切商业使用
- 鉴于项目的特殊性，开发团队可能在任何时间停止更新或删除项目。
- 间接接触（包括但不限于插件）到 keiyume 的软件使用 AGPLv3 开源

衍生软件需声明引用
若引用 keiyume 发布的软件包而不修改 keiyume，则衍生项目需在描述的任意部位提及使用 keiyume。
若修改 keiyume 源代码再发布，则衍生项目必须在文章首部或 keiyume 相关内容首次出现的位置明确声明来源于本仓库，不得扭曲或隐藏免费且开源的事实


若已认真阅读并同意此声明，请输入 yes 并按下回车：
>> """)

# 上述文案由 https://github.com/mamoe/mirai/blob/dev/README.md 修改
        if result == "yes":
            print("听我说谢谢你，因为有你，温暖了司机...\n哦，不对，念错台词了。ご利用いただきありがとうございます！さっそく始めましょう！\n")
            break
        else:
            print("===【哎呀，要认真阅读并同意此声明之后才能使用本框架哦！】===\n")
    # 同意则修改配置文件并写入
    public.config['info']['wizard'] = 0
    public.config.write()
    time.sleep(2)


config_file = """# 溪梦框架 - 配置文件 ./config/config.ini
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker


[admin]
# 超级用户的 QQ 号，超级用户拥有框架及插件管理的普通权限
# 每个超级用户用英文逗号（, ）分隔，不建议太多，不填则无超级用户
# 示例：super_user = 123456, 234567
super_user = 

# 管理员用户的 QQ 号，管理员用户用户拥有框架及插件管理的最高权限
# 每个管理员用户用英文逗号（, ）分隔，不建议太多，不填则无管理员用户
# 示例：super_admin = 123456, 234567
super_admin = 


[general]
# 快速启动：启动框架时跳过信息展示页面
# 提示：0为关闭，1为启用
fast_boot = 0

# go-cqhttp 服务器所在的 ip 地址和端口（正向Websocket），不明白则不需要修改
# 注意：go-cqhttp 服务不建议暴露在公网环境下使用
server_addr = ws://127.0.0.1:8080

# 此功能待开发 #
# 溪梦框架运行状态展示页端口，用于查看实时运行状态，不明白则不需要修改
# server_web_port = 8088


[plugin]
# 插件扩展相关设置，不明白则不需要修改
# 命令前缀，仅对消息类型的命令生效，不明白则不需要修改
# 可为所有注册了消息类型的命令插件添加一个前缀，以减少被误调用的情况
# 比如注册的命令是“你好”，设置了命令前缀“/”后，则需要“/你好”才可以触发命令
cmd_prefix = /

# 需要在哪些群聊启用插件，每个用英文逗号（, ）分隔，不填则默认在所有群聊启用插件
# 填写后只会在事件来自指定群聊时执行插件
# 示例：enable_group = 123456, 78910
enable_group = 

# 需要在哪些群聊禁用插件，每个用英文逗号（, ）分隔，不填则默认不在任何群聊禁用插件
# 填写后只会在事件来自指定群聊时不执行插件
# 填写后只会在启用的群聊执行插件，之后再从启用的群聊中判定禁用插件
# 示例：disable_group = 123456, 78910
disable_group = 

# 需要启用的插件，每个用英文逗号（, ）分隔，不填则默认加载所有插件
# 填写后只会加载填写的插件
# 示例：enable_plugin = keiyume_helper, test
enable_plugin = 

# 需要禁用的插件，每个用英文逗号（,）分隔，不填则默认加载所有插件
# 填写后只会加载填写启用的插件，之后再从启用的插件中判定禁用插件
# 示例：enable_plugin = keiyume_helper, test
disable_plugin = 


[log]
# 溪梦框架运行日志配置，不明白则不需要修改
# 文件日志等级(NOTICE=0,DEBUG=10,INFO=20,WARNING=30,ERROR=40,CRITICAL=50)
file_log_level = 10

# 控制台日志等级(NOTICE=0,DEBUG=10,INFO=20,WARNING=30,ERROR=40,CRITICAL=50)
console_log_level = 20

# 最大日志大小，这里默认为 2MB
# 单位：字节
max_byte = 2097152

# 日志拆分次数（不能为0，1为2份，2为3份，以此类推）
backup_count = 6


# 此功能待开发 #
# [module]
# module_path =


[info]
# 以下内容一般情况下请不要改动

# 是否运行向导
wizard = 1

# 配置文件版本
version = 2.0.0-beta.3
"""

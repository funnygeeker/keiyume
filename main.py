# -*- coding : utf-8-*-
# 溪梦框架：main.py
# 用于启动框架
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume


import os
import sys
import json
import traceback
from core import config_tools, public
from core import loading
from core.log import Log

try:
    import requests
except ImportError:
    print('>> 检测到缺少 requests 库，正在安装...')
    os.system('pip3 install requests -i https://mirrors.aliyun.com/pypi/simple/')
    import requests

#
#  更改工作路径
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))  # 更改程序工作路径为当前可文件执行所在目录

# 配置文件检查
#
loading.create_config()  # 检查配置文件是否被创建，如果没有被创建，则创建文件，并运行初次使用的向导

#
# 加载基本启动页面
loading.start()  # 加载基本启动页面

#
#  加载配置文件
try:
    config_tools.load_config()  # 加载框架配置文件
except:
    print(traceback.format_exc())
    abc = input("""\n【错误】哎呀，框架在加载配置文件的时候出了点问题！
你需要检查一下配置文件填写是否正确，或者试着删除配置文件，然后重新启动程序来生成一个新的配置文件~

按下回车键退出吧！""")
    exit()

#
# 初始化日志记录器和相关模块
global logger
try:
    logger = Log(name="keiyume",
                 console_log_level=int(public.config['log']['console_log_level']),
                 file_log_level=int(public.config['log']['file_log_level']),
                 max_bytes=int(public.config['log']['max_byte']),
                 backup_count=int(public.config['log']['backup_count'])
                 )  # 初始化默认日志配置
    public.logger = logger
    logger.debug("""
=====================【日志模块加载完成】====================
                __                           
               / /___  ____ _____ ____  _____
              / / __ \/ __ `/ __ `/ _ \/ ___/
             / / /_/ / /_/ / /_/ /  __/ /    
            /_/\____/\__, /\__, /\___/_/     
                    /____//____/             """)
    logger.debug(f"配置文件内容：\n{json.dumps(public.config, ensure_ascii=False, indent=4)}")
    #
    # 运行框架启动界面
    if not int(public.config['general']['fast_boot']):  # 如果启动了快速启动则不加载信息展示页
        logger.debug("正在运行框架启动界面...")
        loading.info()
    else:
        logger.debug("执行快速启动，不运行框架启动界面...")

except TypeError:
    print(traceback.format_exc())
    abc = input("""【错误】哎呀，配置文件填写的好像不规范呢！
请检查配置文件填写是否正确，或者试着删除配置文件，然后重新启动程序来生成一个新的配置文件

按下回车键退出吧！""")
    exit()

#
# 检查插件目录是否存在
loading.create_path("./plugins")  # 插件目录如果不存在则创建

#
# 检查是否需要运行初始化向导（当前版本的向导为：使用声明的同意）
if int(public.config['info']['wizard']):
    logger.debug("需要运行初始化向导...")
    loading.wizard()  # 运行初始化向导
else:
    logger.debug("不需要运行初始化向导，继续运行程序...")

#
# 加载插件和连接go-cqhttp的类（需要先完成日志记录器的初始化）
if True:
    from core.connect import Connect  # 这玩意被代码编辑器格式化到开头会出BUG的 :( 别动

    logger.debug("正在为连接 go-cqhttp 做准备...")
    public.connect = Connect(url=public.config['general']['server_addr'])  # 开始连接go-cqhttp服务
    from core import plugin

#
# 加载所有插件
logger.debug("读取设置：需要启用的插件...")
enable_plugin = public.config['plugin']['enable_plugin']  # 读取需要启用的插件
logger.debug("读取设置：需要禁用的插件...")
disable_plugin = public.config['plugin']['disable_plugin']  # 读取需要禁用的插件
logger.debug("正在加载：插件目录下的所有插件...")
plugin.load_from_path(path="./plugins", enable=enable_plugin,
                      disable=disable_plugin)  # 加载插件目录下的所有插件

#
# 运行前置插件
logger.debug("运行前置插件中...")
plugin.run(location='start')  # 运行启动前的插件

#
# 初始化完毕，准备启动程序
logger.info("【信息】初期化が終わりました、プログラムを起動します！")
public.connect.start()

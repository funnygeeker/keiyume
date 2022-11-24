#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 溪梦框架启动主程序
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker
# TODO:atexit库

# from core.connect import *  # 导入连接管理器
# from core.api import *  # 导入Api
# from core.log import *  # 导入日志管理器
# from core.tools import *  # 导入工具
# from core.config import *  # 导入配置管理器
# from core.module import *  # 导入插件可能用到的第三方库（仅针对pyinstaller打包）
# from core.plugin import *  # 导入插件管理器
from core.keiyume import *  # 导入框架模块
from core.loading import *  # 导入加载页面

'''
# 获取文件所在目录并更改程序工作路径
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
'''

Loading.Start()  # 加载基本启动页面
Config.Load_Config()  # 加载框架配置文件
Log.Log_Conf(log_file_name=Config.config['config']['log']['log_file_name'],  # 日志文件名
             file_log_level=int(
	             Config.config['config']['log']['file_log_level']),  # 日志文件记录等级
             console_log_level=int(
	             Config.config['config']['log']['console_log_level']),  # 控制台日志记录等级
             max_bytes=int(Config.config['config']
                           ['log']['max_byte']),  # 单个日志文件最大大小
             backup_count=int(Config.config['config']['log']['backup_count']))  # 日志文件拆分次数

# 重新设置需要连接go-cqhttp的的url
Connect.url = f"{Config.config['config']['server']['server_addr']}:{Config.config['config']['server']['server_port']}"
# 如果启动了快速启动则不加载信息展示页
if not int(Config.config['config']['general']['fast_boot']):
	Loading.Info()

# 读取需要启用的插件
enable_plugin = Tools.convert_format(
	text=Config.config['config']['plugin']['enable_plugin'], mode='str', key=' ')
# 读取需要禁用的插件
disable_plugin = Tools.convert_format(
	text=Config.config['config']['plugin']['disable_plugin'], mode='str', key=' ')

Plugin.Load_Plugin(path='./plugin', enable=enable_plugin,
                   disable=disable_plugin)  # 加载插件目录下的所有插件

Plugin.Run_Plugin(location='start')
if __name__ == '__main__':
	Connect.start()  # 开始连接go-cqhttp服务

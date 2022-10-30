#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 溪梦框架日志管理模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/
from core.connect_mgr import *  # 导入连接管理器
from core.config_mgr import *  # 导入配置管理器
from core.plugin_mgr import *  # 导入插件管理器
from core.log_mgr import *  # 导入日志管理器
from core.loading import *  # 导入加载页面
from core.api import *  # 导入Api
from core.tools import *  # 导入工具


'''
# 获取文件所在目录并更改程序工作路径
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
'''
Loading.Xi_Meng()  # 加载基本启动页面
Config_Mgr.Load_Config()  # 加载框架配置文件
Log_Mgr.Log_Conf(log_file_name=Config_Mgr.config['config']['log']['log_file_name'],
                 file_log_level=int(
                     Config_Mgr.config['config']['log']['file_log_level']),
                 console_log_level=int(
                     Config_Mgr.config['config']['log']['console_log_level']),
                 max_bytes=int(Config_Mgr.config['config']['log']['max_byte']),
                 backup_count=int(Config_Mgr.config['config']['log']['backup_count']))  # 初始化日志模块

# 重新设置需要连接的url
Connect_Mgr.url = f"ws://{Config_Mgr.config['config']['server']['server_addr']}:{Config_Mgr.config['config']['server']['server_port']}"
# 如果启动了快速启动则不加载信息展示页
if not int(Config_Mgr.config['config']['general']['fast_boot']):
    Loading.Info()

Plugin_Mgr.Load_All_Plugin()  # 加载所有插件

Plugin_Mgr.Run_Plugin('start')  # 运行前置插件

if __name__ == '__main__':
    Connect_Mgr.start()

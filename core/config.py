#!/usr/bin/python3
# -*- coding: utf-8 -*-
# keiyume_2.0.0-beta.2
# 溪梦框架配置文件管理模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker
import os
try:
    from configobj import ConfigObj
except ImportError:
    print('>> 检测到缺少 configobj 库，正在安装...')
    os.system('pip3 install configobj')
    from configobj import ConfigObj
from core.text_mgr import *
import threading
lock = threading.Lock()


class Config():
    '【存储设置变量及设置操作函数】'
    config = {}
    '溪梦框架配置'

    def Read_Config(file_path: str, encoding: str = '') -> dict:
        '''【读取单个设置文件】返回：dict（str）'''
        if encoding == '':  # 如果没有设置读取文件的编码
            encoding = Text.detect_encoding(file_path=file_path)
        return ConfigObj(file_path, encoding=encoding)

    def Load_Config():
        '''
        【读取框架运行需要的，./config下的所有配置文件】
        '''
        conf_folder_path = './config'
        file_names = os.listdir(conf_folder_path)  # 获取文件夹下的所有文件和文件夹名称
        for file_name in file_names:  # 遍历文件夹
            # 判断是否为需要读取的后缀
            if ((os.path.splitext(file_name)[1]).lower() == '.ini') and os.path.isfile(f'{conf_folder_path}/{file_name}'):
                # 读取所有.ini文件扩展名的文件，并以{文件名(str):内容(dict)}的形式载入字典
                Config.config[os.path.splitext(file_name)[0]] = dict(
                    Config.Read_Config(file_path=f'{conf_folder_path}/{file_name}'))
                # 判断是否为文件，小写处理文件扩展名，确定是否为需要读取的文件，并进行读取

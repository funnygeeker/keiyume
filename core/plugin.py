#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 溪梦框架插件模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker
import os
import sys
import json
import inspect
import importlib
from core.log import *
from core.tools import *
from core.config import *
from core.connect import *
'''
# 暂时弃用 #
# 获取程序所在目录并将插件所在的文件夹加入工sys.path目录
run_path = os.getcwd()  # 获取程序所在的工作目录
temp_path = os.path.dirname(os.path.realpath(sys.argv[0]))  # 获取pyc预编译文件所在目录

logger.debug(f'程序工作目录：{run_path}\n程序运行目录：{temp_path}')
sys.path.append(os.path.join(os.getcwd()))  # 将当前路径添加到Python模块搜索路径
'''


class Plugin():
    '''【插件管理器】'''
    plugins = {'start': [], 'before': [], 'after': [], 'end': [], 'cmd': []}
    '已注册的插件的列表'
    # plugins_info = {} TODO

    compatible = ['2.0.0-beta.2']

    def Import_Plugin(parent_folder_name: str, folder_name: str) -> None:
        '''
        导入Python模块搜索路目录下指定目录的单个插件
        参数：
            parent_folder_name：父文件夹名
            folder_name：文件夹名
        返回：
            None
        '''
        for keyword in ['.', ' ', '-']:  # 为了能让importlib.import_module()正常执行而进行的检测
            if keyword in folder_name:
                logger.error(
                    f'【错误】：文件夹 {folder_name} 不符合文件夹命名规范，插件将不予加载，请重命名文件夹后再试！\n')
                return None
        logger.debug(f'正在加载文件夹 {folder_name} 中的插件...\n')
        try:
            plugin_object = importlib.import_module(
                f'{parent_folder_name}.{folder_name}')  # 尝试导入插件
            logger.info(f"""++++++++++++++++++++++【正在加载插件】++++++++++++++++++++++
            
  名称：{plugin_object.name}
  位置：{folder_name}
  作者：{plugin_object.author}
  版本：{plugin_object.version}
  说明：{plugin_object.description}\n""")
            # 检查插件兼容性
            if list(set(Plugin.compatible) & set(plugin_object.compatible)) == []:  # 判断是否为兼容版本，若兼容则不警告
                logger.warn(
                    f'【警告】文件夹 {folder_name} 中的插件可能不兼容，请留意插件运行状况！\n')
        except:
            # 在运行列表中删除所有加载错误的插件
            logger.error(
                f'【错误】：文件夹 {folder_name} 下插件加载错误，请排除问题或禁用插件：\n\n{Log.Get_Error()}\n')
            #print('卸载前插件：', Plugin.plugins)
            with lock:
                for location in Plugin.plugins:  # 颠倒后迭代可以解决一些问题
                    for index, plugin in zip(reversed(range(len(Plugin.plugins[location]))), reversed(Plugin.plugins[location])):
                        if plugin['folder'] == folder_name:
                            del Plugin.plugins[location][index]
            #print('卸载后插件：', Plugin.plugins)

    def Load_Plugin(path: str, enable: list = [], disable: list = []) -> None:
        '''
        加载目录下的插件
        参数：
            path：文件夹路径（绝对相对都可）
            enable：仅启用的插件
            disable：禁用的插件
        返回：
            None
        '''
        logger.debug(f"正在加载 {path} 目录下的插件...\n")
        # 先相对路径转绝对路径，再将路径添加到Python模块搜索路径
        path = os.path.abspath(path)  # 相对路径转绝对路径 ./plugin => C:/ximeng/plugin
        # 求绝对路径的父路径 C:/ximeng/plugin => C:/ximeng
        parent_path = os.path.dirname(path)
        if sys.path[-1] != parent_path:
            sys.path.append(parent_path)  # 将插件加载父路径添加到Python模块搜索路径（且不重复添加）
        # 获取目录下可识别的插件
        plugin_folder_names = []  # 准备加载的插件的文件夹名
        folder_names = os.listdir(path)  # 获取目录下所有文件和文件夹名
        for folder_name in folder_names:
            if os.path.isfile(f'{path}/{folder_name}/__init__.py'):
                # 将所有可识别插件加入列表
                plugin_folder_names.append(folder_name)
        # 检查插件是否需要启用
        if enable != []:  # 如果仅启用某些插件
            plugin_folder_names = list(set(plugin_folder_names) & set(
                enable))  # 需要加载的插件列表为可识别且需要启用的插件的交集
        if disable != []:
            plugin_folder_names = list(set(plugin_folder_names) - set(disable))
        # 模块导入
        # 获取插件所在文件夹的文件夹名C:/ximeng/plugin => plugin
        plugin_folder_name_ = os.path.basename(path)
        for plugin_folder_name in plugin_folder_names:
            Plugin.Import_Plugin(
                parent_folder_name=plugin_folder_name_, folder_name=plugin_folder_name)
        # 去除字典中的对象后进行：日志记录-实际可用的插件
        plugins = {}
        for location in Plugin.plugins:
            plugins[location] = []
            for plugin in Plugin.plugins[location]:
                plugin = plugin.copy()  # 如果不copy会影响原字典的
                del plugin['object']
                plugins[location].append(plugin)
        logger.debug(
            f"插件加载完成：{json.dumps(plugins, ensure_ascii=False, indent=4)}\n")

    def Run_Plugin(location: str, obj: object = None, *args, **kwargs) -> object:
        '''
        运行插件
        参数：
            obj：传入的对象，包含：
                obj.ws（websocket对象）
                obj.data（接收到的原始数据）
                obj.self_user_id（自身QQ号）
                等...（详见event.py）
            location：执行一次对应位置的插件，目前支持使用：
                str：before，after，end
        返回：
            object：
                插件处理后的对象
        '''
        for plugin in Plugin.plugins[location]:
            try:
                if plugin['enable']:
                    obj = plugin['object'](obj=obj).Result()
            except:
                logger.error(
                    f"【错误】插件 {plugin['folder']} - {plugin['cls_name']} 运行时出错：\n\n{Log.Get_Error()}\n")
        return obj

    '''def cmd(func: function, command: str, user_id: int = None, group_id: int = None):
        pass'''

    def reg(cls: classmethod, location: str, sequence: int) -> bool:
        '''
        注册插件
        参数：
            cls：需要调用的插件类
            location：插件运行位置
            sequence：运行优先级（越小越先）
        返回：
            bool：
                成功：True，失败：Flase
            None：
                出错
        '''
        try:
            plugin_dict = {'folder': os.path.basename(os.path.dirname(inspect.getfile(cls))),  # 通过类获取文件路径再获取文件夹名
                           'cls_name': cls.__name__,  # 插件类类名
                           'sequence': sequence,  # 执插件执行顺序
                           'object': cls,  # 插件类的对象
                           'enable': True  # 插件是否启用
                           }
            # 对插件的加载顺序进行排序
            index = 0  # 列表读取位置索引
            try:
                with lock:  # 之后可能会开发插件热启用/热禁用，或者插件热加载，故在此加锁
                    for plugin in Plugin.plugins[location]:
                        if plugin == plugin_dict:  # 如果已有相同注册项，则不再注册
                            logger.debug(f"""
  【重复的注册项】
  插件位置：{plugin_dict['folder']}
  类的名称：{plugin_dict['cls_name']}
  运行位置：{location}
  运行顺序：{sequence}\n""")
                            return False
                        elif sequence <= plugin['sequence']:  # 顺序小于或等于则排在前面
                            Plugin.plugins[location].insert(
                                index, plugin_dict)  # 将函数加入执行列表
                            break
                        index += 1
                    else:  # 如果没有顺序比新加载插件小的也排到最后
                        Plugin.plugins[location].append(
                            plugin_dict)
                logger.debug(f"""
  【插件注册】
  插件位置：{plugin_dict['folder']}
  类的名称：{plugin_dict['cls_name']}
  运行位置：{location}
  运行顺序：{sequence}\n""")
            except:
                logger.error(
                    f"【错误】插件 {plugin_dict['folder']} 中，{cls.__name__} 函数加载出错！\n\n{Log.Get_Error()}\n")
                return False
        except:
            logger.error(f"【错误】插件注册-未知错误：\n{Log.Get_Error()}\n")
            return False

        return True

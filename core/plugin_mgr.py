import os
import sys
import json
#import shutil
import importlib
from core.tools import *

from core.config_mgr import *
from core.log_mgr import *
#from core.tools import *

# 获取程序所在目录并将插件所在的文件夹加入工作目录
run_path = os.getcwd()  # 获取程序所在的原始运行目录
temp_path = os.path.dirname(os.path.realpath(sys.argv[0]))  # 获取pyc预编译文件所在目录

'''print(f'运行目录：{run_path}')
print(f'临时目录：{temp_path}')'''

logger.debug(f'程序原始运行目录：{run_path}\n程序实际运行目录：{temp_path}')
sys.path.append(os.path.join(os.getcwd()))

'''print('sys.path：')
for i in sys.path:
    print(i)'''
'''if run_path != temp_path:  # 判断预编译文件是否与程序于同一目录，使pyinstaller打包程序后仍能正常加载插件
    logger.debug('原始目录与运行目录不符，开始拷贝文件...')
    input('copy')
    shutil.copytree(f'{run_path}/plugin', f'{temp_path}/plugin')'''


class Plugin_Mgr():
    '''【插件管理器】'''
    all_plugins = []
    '''所有可识别插件的对应文件夹名
    结构示例：['插件文件夹名1','插件文件夹名2'...]'''
    plugins = {}
    '''所有加载的插件信息及状态 结构示例：
    {{'插件文件夹名1':{'object': 模块本身(对象), 'enable': True}},{'插件文件夹名2':{'object': 模块本身(对象), 'enable': True}}...}'''
    plugins_run = {'start': [], 'before': [],
                   'after': [], 'exit': [], 'cmd': []}
    '''插件执行位置和顺序 结构示例：
    {'start': [{'name': 插件文件夹名1, 'sequence': 数字（代表执行顺序）}], 'before': [...], 'after': [...], 'end': [...]} '''

    compatible = ['2.0.0_BETA1']
    '''插件兼容标识符，目前版本兼容标识为：2.0.0_BETA1
    标识符会随溪梦框架主体更新，以达到提示用户存在插件不兼容的作用，
    一般来说如果程序主体无重大影响到规范的更新，
    溪梦框架程序插件标识符不会删减只会增加新的规范，如果旧规范被抛弃，
    则会删去旧规范的标识符。因此开发插件时需要正确填写插件对应版本的标识符，
    不要多填，插件发布前应做好兼容性测试
    举例：我在最新的溪梦框架插件规范为：2.0.0时，
    开发了一个2.1规范插件，经测试对在溪梦框架的2.0.0规范的（旧版）主程序下也运行正常，
    则在兼容标识中填入：['2.0.0','2.1.0']
    '''

    def Get_Plugin(path: str = './plugin') -> dict:
        '''【获取插件目录下的所有可被识别的插件并存储到Plugin_Mgt.all_plugin】
        返回：Plugin_Mgt.plugins'''
        Plugin_Mgr.all_plugins = []  # 清空所有插件列表
        Plugin_Mgr.plugins = {}  # 清空所有加载的插件信息及状态
        Plugin_Mgr.plugins_run = {
            'start': [], 'before': [], 'after': [], 'exit': [], 'cmd': []}  # 清空插件执行顺序
        files_name = os.listdir(path)  # 获取目录下所有文件和文件夹名
        for file_name in files_name:
            if os.path.isfile(f'./plugin/{file_name}/__init__.py'):
                # 将所有有效插件加入列表
                Plugin_Mgr.all_plugins.append(file_name)
        # 如果设置为启用所有插件（即完全空白）
        if Config_Mgr.config['config']['plugin']['enable_plugin_names'].strip(' ') == '':
            for plugin in Plugin_Mgr.all_plugins:  # 遍历所有可识别的插件
                Plugin_Mgr.plugins[plugin] = {
                    'object': None, 'enable': True}  # 登记插件
        else:  # 否则为启用指定插件
            for plugin in Plugin_Mgr.all_plugins:  # 遍历所有插件
                for enable in Tools.Format_Conversion(Config_Mgr.config['config']['plugin']['enable_plugin_names'], mode='str'):
                    # 遍历设置中已启用的插件
                    if plugin == enable:  # 如果插件被启用（即文件夹名与设置中的相同）
                        Plugin_Mgr.plugins[plugin] = {
                            'object': None, 'enable': True}  # 登记插件
        return Plugin_Mgr.plugins

    def Load_Plugin(plugin_folder_name: str) -> bool:
        '''【加载文件夹中的插件】
        plugin_folder_name:plugin文件夹下的二级文件夹名
        需要文件夹下含有:__init__.py'''
        for text in ['.', ' ', '-']:  # 为了能让importlib.import_module()正常执行而进行的检测
            if text in plugin_folder_name:
                logger.error(
                    f'【错误】：文件夹 plugin/{plugin_folder_name} 不符合文件夹命名规范，插件将不予加载，请重命名文件夹后再试！\n')
                return None
        logger.debug(f'正在加载文件夹 plugin/{plugin_folder_name} 中的插件...\n')
        Plugin_Mgr.plugins[plugin_folder_name] = {
            'object': None, 'enable': True}
        try:
            Plugin_Mgr.plugins[plugin_folder_name]['object'] = importlib.import_module(
                f'plugin.{plugin_folder_name}')  # 尝试导入插件
            plugin = Plugin_Mgr.plugins[plugin_folder_name]['object']

            # 检查插件兼容性
            if list(set(Plugin_Mgr.compatible) & set(plugin.compatible)) == []:  # 判断是否为兼容版本，若兼容则不警告
                logger.warn(
                    f'【警告】文件夹 plugin/{plugin_folder_name} 中的插件可能存在不兼容！\n')

            # 对插件执行顺序进行分类和加载顺序排序
            Plugin_Mgr.Plugin_Sorting(
                name=plugin_folder_name,
                location=plugin.location,
                obj=Plugin_Mgr.plugins[plugin_folder_name])
            logger.info(
                f'''+++++++++++++++++++++++【正在加载插件】+++++++++++++++++++++++\n\n  名称：{plugin.name}\n  位置：{plugin_folder_name}\n  作者：{plugin.author}\n  版本：{plugin.version}\n  说明：{plugin.description}\n''')
            logger.debug(
                f'''\n  运行顺序：{plugin.sequence}\n  运行位置：{plugin.location}\n  兼容性标识：{" ".join(str(i) for i in plugin.compatible)}\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n''')
            return True
        except:  # 加载出错
            logger.error(
                f'【错误】插件加载错误，请排除问题或禁用插件：plugins/{plugin_folder_name}\n\n{Log_Mgr.Get_Error()}\n')
            # 卸载插件 TODO RuntimeError: dictionary changed size during iteration
            del Plugin_Mgr.plugins[plugin_folder_name]
            return None

    def Plugin_Sorting(name: str, location: str, obj: dict):
        '''【对插件的执行顺序进行分类和排序】
        由Load_Plugin函数调用'''
        if Plugin_Mgr.plugins_run[location] != []:  # 如果对应加载位置的插件加载顺序不为空
            # 对插件的加载顺序进行排序
            sequence = 0  # 列表读取的当前位置计数
            for plugin in Plugin_Mgr.plugins_run[location]:
                if obj['object'].sequence <= plugin['sequence']:  # 顺序小于或等于则排在前面，否则排在最后
                    Plugin_Mgr.plugins_run[location].insert(
                        sequence, {'name': name, 'sequence': obj['object'].sequence})
                    break
                sequence += 1
            else:  # 如果没有顺序比新加载插件小的也排到最后
                Plugin_Mgr.plugins_run[location].append(
                    {'name': name, 'sequence': obj['object'].sequence})
        else:  # 如果对应加载位置的插件加载顺序为空
            Plugin_Mgr.plugins_run[location].append(
                {'name': name, 'sequence': obj['object'].sequence})
        return True

    def Load_All_Plugin():
        '''【按设置加载所有插件】
        注：使用前需要先加载设置和日志模块'''
        logger.debug(
            f'所有可识别的插件如下：\n{json.dumps(Plugin_Mgr.Get_Plugin(),ensure_ascii=False,indent=4)}\n')  # 获取所有插件，并记录日志
        for plugin in Plugin_Mgr.plugins.copy():
            Plugin_Mgr.Load_Plugin(plugin_folder_name=plugin)  # 加载所有插件
        # 日志记录实际可用的插件
        plugins = {}
        for plugin in Plugin_Mgr.plugins:
            plugins[plugin] = Plugin_Mgr.plugins[plugin]['enable']
        logger.debug(
            f'实际可用的插件如下：\n{json.dumps(plugins,ensure_ascii=False,indent=4)}\n')  # 获取所有插件，并记录日志

    def Run_Plugin(location: str, obj=None, *args, **kwargs):
        '''【运行插件】
        obj:传入的对象，包含：obj.ws(websocket对象),obj.data(接收到的原始数据),obj.self_user_id(自身QQ号)
        location:执行一次对应位置的插件,值:start/before/after/end'''
        for plugin in Plugin_Mgr.plugins_run[location]:
            try:
                PLUGIN = Plugin_Mgr.plugins[plugin['name']]['object'].Main(
                    obj=obj)
                PLUGIN.Run()
                obj = PLUGIN.Result()
            except:
                logger.error(f"【错误】插件出错：\n{Log_Mgr.Get_Error()}")
        return obj

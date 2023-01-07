# -*- coding : utf-8-*-
# 溪梦框架插件模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker
# 参考资料：
# python动态修改类方法和实例方法：https://blog.csdn.net/jerrism/article/details/107357541
#
# 这个版本确实是冗余代码非常多，我们会在下一个版本再次重构....（写完后才发现...）
import os
import sys
import json
import inspect
import traceback
import importlib
from types import MethodType
from typing import Union, Optional, Dict, List, Any

from . import shell, public
from .event import Event
from .public import logger, lock

plugins: Dict[str, List[Dict[str, Any]]] = {'start': [], 'connect': [],
                                            'event': [], 'disconnect': [],
                                            'shell': [], 'exit': []}
'已注册的插件的列表'

plugins_info: Dict[str, Any] = {}
'已加载的插件信息'

compatible = ['2.0.0-beta.3', '2.0.0-beta.3-beta']
'兼容性标识'


def load(parent_folder_name: str, folder_name: str) -> None:
    """
    导入Python模块搜索路目录下指定目录的单个插件 TODO
    参数：
        parent_folder_name：父文件夹名（这个函数要重构的）
        folder_name：文件夹名
    返回：
        None
    """
    for keyword in ['.', ' ', '-']:  # 为了能让importlib.import_module()正常执行而进行的检测
        if keyword in folder_name:
            logger.error(
                f'【错误】：文件夹 {folder_name} 不符合文件夹命名规范，插件将不予加载，请重命名文件夹后再试！')
            return None
    logger.debug(f'正在加载文件夹 {folder_name} 中的插件...')
    try:
        plugin_object = importlib.import_module(
            f'{parent_folder_name}.{folder_name}')  # 尝试导入插件
        logger.info(f"""++++++++++++++++++++++【正在加载插件】++++++++++++++++++++++
  名称：{plugin_object.name}
  位置：{folder_name}
  作者：{plugin_object.author}
  版本：{plugin_object.version}
  说明：{plugin_object.description}""")
        plugin_info = {'name': plugin_object.name,
                       'folder': folder_name,
                       'author': plugin_object.author,
                       'version': plugin_object.version,
                       'description': plugin_object.description,
                       'object': plugin_object}
        plugins_info[folder_name] = plugin_info
        # 检查插件兼容性
        if not list(set(compatible) & set(plugin_object.compatible)):  # 判断是否为兼容版本，若兼容则不警告
            logger.warning(
                f'【警告】文件夹 {folder_name} 里的插件好与框架的兼容标识符不一致，可能存在不兼容，记得留意一下插件是否正常运行哦！')
    except:
        # 在运行列表中删除所有加载错误的插件
        logger.error(
            f'【错误】文件夹 {folder_name} 下插件加载错误，请排除问题或禁用插件：{traceback.format_exc()}')
        with lock:
            for location in plugins:  # 颠倒后迭代可以解决一些问题
                for index, _plugin in zip(reversed(range(len(plugins[location]))),
                                          reversed(plugins[location])):
                    if _plugin['folder'] == folder_name:
                        del plugins[location][index]


def load_from_path(path: str, enable: Optional[Union[str, List[str]]] = None,
                   disable: Optional[Union[str, List[str]]] = None) -> None:
    """
    加载目录下的插件

    Args:
        path: 文件夹路径（绝对相对都可）
        enable: 仅启用的插件
        disable: 禁用的插件
    """
    logger.debug(f"正在加载 {path} 目录下的插件...")
    # 先相对路径转绝对路径，再将路径添加到Python模块搜索路径
    path = os.path.abspath(path)  # 相对路径转绝对路径 ./_plugin => C:/keiyume/_plugin
    # 求绝对路径的父路径 C:/keiyume/_plugin => C:/keiyume
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
    if enable:  # 如果仅启用某些插件
        if type(enable) is str:  # 如果变量为字符串则需要将字符串转化为列表
            enable = [enable]
        plugin_folder_names = list(set(plugin_folder_names) & set(
            enable))  # 需要加载的插件列表为可识别且需要启用的插件的交集
    if disable:
        if type(disable) is str:  # 如果变量为字符串则需要将字符串转化为列表
            disable = [disable]
        plugin_folder_names = list(set(plugin_folder_names) - set(disable))
    # 模块导入
    # 获取插件所在文件夹的文件夹名C:/keiyume/plugin => plugin
    plugin_folder_name_ = os.path.basename(path)
    for plugin_folder_name in plugin_folder_names:
        load(
            parent_folder_name=plugin_folder_name_, folder_name=plugin_folder_name)
    # 日志记录-实际可用的插件
    logger.debug(
        f"插件加载完成：{json.dumps(get_status(), ensure_ascii=False, indent=4)}")


def set_func_status(func, enable: bool) -> bool:
    """
    设置插件函数启用状态

    Args:
        func: 插件的函数
        enable: 是否启用插件

    Returns:
        True: 找不到插件
        False: 正常执行
    """
    global plugins
    result = True
    if enable:
        text = "启用"
    else:
        text = "禁用"
    for location in plugins:
        for _plugin in plugins[location]:
            if _plugin['func'] == func:
                _plugin['enable'] = enable
                logger.info(
                    f"【信息】已{text}插件项：{_plugin['folder']} - {_plugin['func_name']}")
                result = False
    return result


def set_plugin_status(folder_name: str, enable: bool) -> bool:
    """
    设置整个插件启用状态

    Args:
        folder_name: 插件所在的文件夹名
        enable: 是否启用插件

    Returns:
        True: 找不到插件
        False: 正常执行
    """
    global plugins
    result = True
    if enable:
        text = "启用"
    else:
        text = "禁用"
    for location in plugins:
        for _plugin in plugins[location]:
            if _plugin['folder'] == folder_name:
                _plugin['enable'] = enable
                logger.info(
                    f"【信息】已{text}插件项：{folder_name} - {_plugin['func_name']}")
                result = False
    return result


def get_status() -> dict:
    """
    获取插件状态
    """
    _plugins = {}
    for location in plugins:
        _plugins[location] = []
        for _plugin in plugins[location]:
            _plugin = _plugin.copy()  # 如果不copy会影响原字典的
            del _plugin['func']
            _plugins[location].append(_plugin)
    return _plugins


def get_info() -> dict:
    """
    获取插件信息
    Returns:
        dict

    """
    _plugins_info = {}
    for folder_name in plugins_info:
        _plugin_info = plugins_info[folder_name].copy()
        del _plugin_info['object']
        _plugins_info[folder_name] = _plugin_info
    return _plugins_info


def reg_(func, location: str, priority: int, cmd: Optional[Union[str, List[str]]] = None,
         cmd_help: Optional[str] = None, *args, **kwargs) -> bool:
    """
    注册插件
    参数：
        func：需要调用的插件函数
        location：插件运行位置
        priority：运行优先级（越小越先）
    返回：
        bool：
            成功：True，失败：False
        None：
            出错
    """
    global plugins
    if cmd:
        if type(cmd) is str:
            cmd = [cmd]
        cmd_ = []
        for _ in cmd:  # 如果插件类型不为 shell，添加命令前缀
            cmd_.append(f"{public.config['plugin']['cmd_prefix']}{_}")
        cmd = tuple(cmd_)
    try:
        plugin_info = {'folder': os.path.basename(os.path.dirname(inspect.getfile(func))),  # 通过函数获取文件路径再获取文件夹名
                       'func_name': func.__name__,  # 函数名
                       'cmd': cmd,  # 命令
                       'cmd_help': cmd_help,  # 命令帮助
                       'priority': priority,  # 执插件执行顺序
                       'func': func,  # 函数本身
                       'enable': True  # 插件是否启用
                       }
        # 对插件的加载顺序进行排序
        index = 0  # 列表读取位置索引
        try:
            # 如果插件注册的运行位置不存在则新建这个运行位置
            if plugins.get(location, None) is None:
                plugins[location] = []
                logger.debug(f"插件 {plugin_info['folder']} 新建了一个运行位置：{location}")
            with lock:  # 之后可能会开发插件热启用/热禁用，或者插件热加载，故在此加锁
                for _plugin in plugins[location]:
                    if _plugin == plugin_info:  # 如果已有相同注册项，则不再注册
                        logger.debug(f"""  【重复的注册项】
  插件位置：{plugin_info['folder']}
  函数名称：{plugin_info['func_name']}
  运行位置：{location}
  运行顺序：{priority}""")
                        return False
                    elif priority <= _plugin['priority']:  # 顺序小于或等于则排在前面
                        plugins[location].insert(
                            index, plugin_info)  # 将函数加入执行列表
                        break
                    index += 1
                else:  # 如果没有顺序比新加载插件小的也排到最后
                    # 将插件加入该运行位置对应的列表
                    plugins[location].append(
                        plugin_info)
            logger.debug(f"""  【插件注册】
  插件位置：{plugin_info['folder']}
  函数名称：{plugin_info['func_name']}
  运行位置：{location}
  运行顺序：{priority}""")
        except:
            logger.error(
                f"【错误】插件 {plugin_info['folder']} 中，{func.__name__} 函数加载出错了呢！\n{traceback.format_exc()}")
            return False
    except:
        logger.error(f"【错误】插件注册-未知错误：\n{traceback.format_exc()}")
        return False

    if cmd is not None and cmd_help is not None:
        shell.cmd_help_plugin.append(f"{cmd_help}")

    return True


def reg(location: str, priority: int, cmd: Union[None, str, List[str]] = None, cmd_help: Optional[str] = None,
        *args, **kwargs):
    """
    注册插件

    Args：
        location：插件运行位置
        priority：运行优先级（越小越先）
    Returns：
        bool：
            True: 成功
            False: 失败
        None：
            出错
    """

    def wrapper(func):
        reg_(func, location=location, priority=priority, cmd=cmd, cmd_help=cmd_help, *args, **kwargs)

    return wrapper


def run(location: str, event: Optional["Event"] = None, shell_cmd: Union[None, str] = None, *args, **kwargs) -> "Event":
    """
    运行插件
    参数：
        event：传入的实例，由core.event.Event实例化，包含：
            event.ws（websocket对象）
            event.data（接收到的原始数据）
            event.self_user_id（自身QQ号）
            等...（详见event.py）
        location：执行一次对应位置的插件，目前支持使用：
            before，after，end，exit，raw_cmd
    返回：
        event：
            插件处理后的实例
    """
    if event is None:
        event = Event()

    event.group_id = event.data.get('group_id')
    if event.group_id is not None:  # 如果为任何来自群聊的事件，即可以获取到群聊 ID
        if public.config['plugin']['enable_group'] and event.group_id not in \
                public.config['plugin']['enable_group']:  # 如果需要在哪些群聊启用插件，且对应的群聊不在需要启用插件的群聊内
            return event  # 立刻返回实例，结束本区域的插件调用
        if public.config['plugin']['disable_group'] and event.group_id in \
                public.config['plugin']['disable_group']:  # 如果需要在哪些群聊禁用插件，且对应的群聊在需要禁用插件的群聊内
            return event  # 立刻返回实例，结束本区域的插件调用

    for _plugin in plugins[location]:
        try:
            if _plugin['enable']:
                event.echo = event.data.get('echo')
                event.time = event.data.get('time')
                event.user_id = event.data.get('user_id')
                event.group_id = event.data.get('group_id')
                event.msg = event.data.get('message')
                event.message = event.msg
                event.sub_type = event.data.get('sub_type')
                event.post_type = event.data.get('post_type')
                event.message_id = event.data.get('message_id')
                if _plugin['cmd'] is None:  # 普通插件
                    event.run = MethodType(_plugin['func'], event)  # 为实例重新绑定函数
                    if event.run(*args, **kwargs):  # 如果后续的执行被中断，则不继续执行下一个插件
                        break
                else:  # 命令插件
                    if location == "shell" and shell_cmd is not None:  # shell 命令插件
                        for _ in _plugin['cmd']:
                            if shell_cmd.startswith(_):  # 命令匹配成功
                                result = shell_cmd.lstrip(_)  # 去除命令头
                                break
                        else:  # 命令匹配失败
                            result = None
                    elif event.is_message():  # 消息类型的命令插件
                        for _ in _plugin['cmd']:
                            if event.msg.startswith(_):  # 命令匹配成功
                                result = event.msg.lstrip(_)  # 去除命令头
                                break
                        else:  # 命令匹配失败
                            result = None
                    else:  # 未知情况
                        result = None

                    if result is not None:  # 如果值不为 None，即：成功匹配到了命令
                        event.cmd_body = result
                        event.run = MethodType(_plugin['func'], event)  # 为实例重新绑定函数
                        if event.run():  # 如果后续的执行被中断，则不继续执行下一个插件
                            break
        except:
            logger.error(
                f"【错误】插件 {_plugin['folder']} - {_plugin['func_name']} 运行时出错：\n{traceback.format_exc()}")
    return event

# -*- coding : utf-8-*-
# 溪梦框架：core/frame.py
# 用于管理插件与框架之间的直接交互
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume


from typing import (Optional, Union, List, TYPE_CHECKING)
from . import public

if TYPE_CHECKING:
    from .config_tools import ConfigObj


def change_setting(operation: str, keyword: str,
                   content: Optional[Union[str, int, List[int]]] = None) -> Union[None, bool]:
    """
    修改框架配置文件并立即应用当前设置

    Args:
        operation: 操作类型，可以用的类型有：
            add(添加指定值)、del(删除指定值)、clear(删除全部值)、change(修改指定值)
        keyword: 需要修改的设置，可以用的类型有：
            super_user(超级用户)、super_admin(超级管理员)、enable_group(启用插件的群聊)、disable_group(禁用插件的群聊)、
        content: 需要修改的内容，详细说明如下：
            如果操作类型为 add(添加指定值) 或 del(删除指定值) 只支持输入 str,int 类型的数字
            如果操作类型为 clear(删除全部值) 不需要输入此变量
            如果操作类型为 change(修改指定值) 需要输入一个内部数据均为整数的列表

    Returns:
        True: 操作成功
        False: 不需要执行操作
        None: 不支持的操作类型

    Examples:
        frame.change_setting("add", "super_user", 123456)
    """
    section = ''
    if keyword == "super_user":
        section = 'admin'
    elif keyword == "super_admin":
        section = 'admin'
    elif keyword == "enable_group":
        section = 'plugin'
    elif keyword == "disable_group":
        section = 'plugin'

    if operation == 'add':
        value: List[int] = public.config[section][keyword]
        for i in value:
            if i == content:
                return False
        else:
            value.append(int(content))

    elif operation == 'del':
        value: List[int] = public.config[section][keyword]
        new_value = []
        for i in value:
            if i != int(content):
                new_value.append(i)
        value = new_value

    elif operation == 'clear':
        value = []

    elif operation == 'change':
        value = content

    else:
        return None

    public.config[section][keyword] = value
    public.config.write()
    return True


def read_settings() -> "ConfigObj":
    """
    读取框架配置文件

    Returns:
        ConfigObj 对象，但是可以像字典一样，读取或者修改其中的值，修改值之后使用 .write() 将更改写入到配置文件
    """
    return public.config


def get_version() -> str:
    """
    获取框架版本

    Returns:
        当前的框架版本
    """
    return public.config['info']['version']


def disconnect() -> None:
    """
    使框架与 go-cqhttp 断开连接
    """
    return public.connect.ws.close()


def exit_frame() -> None:
    """
    断开连接并退出框架
    """
    return public.connect.exit()

# -*- coding : utf-8-*-
# 溪梦框架：core/event.py
# 为兼容 Clousx6 词库设计的模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume
#
# 参考资料：
# CSDN - 被调用函数中获取调用函数信息：https://blog.csdn.net/crazycui/article/details/52129716


import os
import time
import random
import _thread
import traceback
from typing import Optional, Union

from .public import logger
from .sqlite import Sqlite


def random_num(a: Union[int, str], b: Union[int, str]) -> int:
    """
    生成一个随机数，等效于 Clousx6 中的 %随机数(.*)-(.*)%

    Args:
        a: 随机范围中最小的数
        b: 随机范围中最大的数

    Returns:
        随机数

    Examples:
        x6.random_num(1, 7)
    """
    return random.randint(int(a), int(b))


def call(time_: Union[int, str], func, self) -> int:
    """
    等待一定时间调用一个函数，等效于 Clousx6 中的 $调用 (.*) (.*)$

    Args:
        time_: 在调用函数前等待的时间，单位：毫秒
        func: 需要调用函数
        self: 请传入表示当前的实例，由于与 Clousx6 结构不同，因此额外需要传入此变量，一般来说应该是框架中的 self 或者 event 变量

    Returns:
        返回线程标识符

    Examples:
        x6.call(1000, hello)
    """
    return _thread.start_new_thread(_call, **{"time_": time_, 'func': func, 'self': self})


def _call(time_: Union[str, int], func, self):
    """
    这是一个内部功能，请避免从外部调用
    """
    time.sleep(int(time_) / 1000)
    func(self)


def time_now(time_format: str, time_: Optional[int] = None) -> str:
    """
    以字符串的形式返回现在的时间，等效于 Clousx6 中的 %时间(.*)%

    Args:
        time_format: 需要格式化的时间格式
        time_: 需要传入时间以进行计算，一般需要传入 self.time

    Returns:
        字符串形式的时间

    Examples:
        x6.time_now('yy年MM月dd日HH:mm:ss', self.time)
    """
    if time_ is None:
        time_ = time.localtime(time.time())
    else:
        time_ = time.localtime(time_)
    time_format = time_format.replace('yy', '%Y')
    time_format = time_format.replace('MM', '%m')
    time_format = time_format.replace('dd', '%d')
    time_format = time_format.replace('HH', '%H')
    time_format = time_format.replace('mm', '%M')
    time_format = time_format.replace('ss', '%S')
    return time.strftime(time_format, time_)


def params(msg: str, num: Union[str, int]) -> str:
    """
    传入一个消息，按空格进行分割，之后返回指定序列的参数，等效于 Clousx6 中的 %参数(.*)%

    Args:
        msg: 传入的消息，一般为 self.msg
        num: 需要获取的序列，-1 则代表获取整个消息

    Returns:
        分割后的消息中指定序列的参数
    """
    if int(num) == -1:
        return msg
    return msg.split(' ')[int(num)]


def init_db(table: str = 'data') -> None:
    """
    如果需要读写数据，需要在读写前初始化数据库，一般在导入插件时运行
    """
    sql = Sqlite(f"{os.path.dirname(traceback.extract_stack()[-2][0])}/data.db")
    sql.new(table, path='TEXT', key='TEXT', value='TEXT')
    sql.close()


def write(path: Union[str, int], key: Union[str, int], value: Union[str, int], table: str = 'data') -> None:
    """
    向数据库中写入数据，等效于 Clousx6 中的 $写 (.*) (.*) (.*)$

    Args:
        path: 在 Clousx6 中为路径，在此框架中，你可以理解为数据的第一个值，读取时需要读取函数中第一个值和第二个值分别一致的时候才能成功读取原来写入的数据
        key: 在 Clousx6 中为数据的键，在此框架中，你可以理解为数据的第二个值，读取时需要读取函数中第一个值和第二个值分别一致的时候才能成功读取原来写入的数据
        value: 在 Clousx6 中为数据的值，在此框架中，你可以理解为数据的第三个值，读取时如果找到了对应的值将会返回这里的值，如果没有找到，就会返回设定的默认值
        table: 数据表的表名，如果不需要额外区分，则不用填写

    Examples:
        x6.write("开关/{self.group_id}/开关", "a", 1)
    """
    sql = Sqlite(f"{os.path.dirname(traceback.extract_stack()[-2][0])}/data.db")
    sql.auto_write(table,
                   f"WHERE path='{path}' AND key='{key}'",
                   **{'path': str(path),
                      'key': str(key),
                      'value': str(value)
                      })
    sql.close()


def read(path: Union[str, int], key: Union[str, int], default: Union[str, int],
         table: str = 'data') -> Union[str, int, None]:
    """
    从数据库中读取数据，等效于 Clousx6 中的 $读 (.*) (.*) (.*)$

    Args:
        path: 在 Clousx6 中为路径，在此框架中，你可以理解为数据的第一个值，读取时需要读取函数中第一个值和第二个值分别一致的时候才能成功读取原来写入的数据
        key: 在 Clousx6 中为数据的键，在此框架中，你可以理解为数据的第二个值，读取时需要读取函数中第一个值和第二个值分别一致的时候才能成功读取原来写入的数据
        default: 在 Clousx6 中为数据的默认值，读取时如果找到了对应的值将会返回读取出的值，如果没有找到对应的值，就会返回设定的默认值
        table: 数据表的表名，如果不需要额外区分，则不用填写

    Returns:
        读取时，如果可以转换为整数的数据，将会强制转换为整数，如果读取时出现错误，返回 None
    """
    sql = Sqlite(f"{os.path.dirname(traceback.extract_stack()[-2][0])}/data.db")
    result = sql.read(table, f"WHERE path='{path}' AND key='{key}'", 'value')
    sql.close()
    if len(result) == 0:  # 无查询到的结果
        if type(default) is str and default.isdigit():
            return int(default)
        return default
    elif len(result) == 1:  # 有一条查询到的结果
        if result[0][0].isdigit():  # 可转换为数字则提供数字
            return int(result[0][0])
        return result[0][0]
    else:
        logger.error('【错误】查询数据库时发现了过多的结果，可能是写入时发生了错误！')
        return None

# -*- coding : utf-8-*-
# 溪梦框架：core/log.py
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume
#
# 参考资料：
# 博客园 - Python 日期格式化知识：https://www.cnblogs.com/pyxiaomangshe/p/7918850.html
# 博客园 - Python Log文件大小设置及备份：https://www.cnblogs.com/xyztank/articles/13599165.html
# CSDN - python 中 logging 模块显示不同颜色的日志：https://blog.csdn.net/qq_36072270/article/details/105345562


import os
import logging
import traceback
from typing import Optional
from logging.handlers import RotatingFileHandler

# 控制台彩色日志显示
try:
    import colorlog
except ImportError:
    print('>> 检测到缺少 colorlog 库，正在安装...')
    os.system('pip3 install colorlog -i https://mirrors.aliyun.com/pypi/simple/')
    import colorlog


class Log(logging.Logger):
    def __init__(self, file: str = "./logs/Keiyume.log",
                 name: Optional[str] = None,
                 enable_console_handler: bool = True,
                 enable_file_handler: bool = True,
                 console_log_level: int = 20,
                 file_log_level: int = 10,
                 max_bytes: int = 2 * 1024 * 1024, backup_count: int = 6,
                 log_colors_config: Optional[dict] = None,
                 console_formatter: Optional[object] = None,
                 file_formatter: Optional[object] = None):
        """
        日志记录模块
        Args:
            file: 要保存的日志文件的名称及路径
            name: 为logging日志记录器创建一个名称
            enable_console_handler: 是否启用控制台日志输出
            enable_file_handler: 是否启用日志文件输出
            console_log_level: 控制台显示的最小日志等级
            file_log_level: 日志文件输出的最小日志等级
            max_bytes: 日志文件最大大小（单位：比特）
            backup_count: 日志文件切割次数（不应小于1）
            log_colors_config: 控制台日志颜色配置
            console_formatter: 控制台日志输出格式
            file_formatter: 日志文件输出格式
        """
        super().__init__(name)
        """if name is not None:
            self.logger_ = logging.getLogger()  # 创建一个根日志记录器
            self.logger_.setLevel(logging.NOTSET)  # 设置根记录器的日志等级
        self.logger = logging.getLogger(name)  # 创建一个日志记录器"""
        if not os.path.exists(os.path.dirname(file)):  # 若不存在日志路径，则自动创建
            os.makedirs(os.path.dirname(file))
        self.setLevel(logging.NOTSET)  # 设置记录器的日志等级

        if enable_console_handler:  # 如果启用控制台输出日志
            self.console_handler = logging.StreamHandler()  # 创建控制台的日志记录器
            if log_colors_config is None:  # 如果没有配置日志颜色
                # 终端输出日志颜色配置
                log_colors_config = {
                    'DEBUG': 'bold_cyan',
                    'INFO': 'white',
                    'WARNING': 'black,bg_yellow',
                    'ERROR': 'black,bg_red',
                    'CRITICAL': 'black,bg_purple',
                }
            # 控制台输出格式
            if console_formatter is None:
                if console_log_level <= 10:  # 只有日志等级在DEBUG以下时才在控制台输出详细的日志
                    console_formatter = colorlog.ColoredFormatter(
                        fmt='%(log_color)s[%(asctime)s.%(msecs)03d][%(levelname)s][%(threadName)s(%(thread)d) %('
                            'pathname)s %(module)s.%(funcName)s(%(lineno)d)]:\n%(message)s\n',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        log_colors=log_colors_config
                    )
                else:
                    console_formatter = colorlog.ColoredFormatter(
                        fmt='%(log_color)s[%(asctime)s.%(msecs)03d] [%(levelname)s]:\n%(message)s\n',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        log_colors=log_colors_config
                    )

            # 输出到控制台
            self.console_handler.setFormatter(console_formatter)
            self.console_handler.setLevel(console_log_level)  # 设置控制台的日志等级
            self.addHandler(self.console_handler)  # 添加控制台的日志记录器

        if enable_file_handler:  # 如果启用日志文件输出日志
            if backup_count < 1:  # 强制分割日志文件至少一次，防止日志文件大小无限制增加
                backup_count = 1
            self.file_handler = RotatingFileHandler(filename=file, maxBytes=max_bytes, backupCount=backup_count,
                                                    encoding='utf8')  # 创建日志文件的日志记录器
            if file_formatter is None:
                # 日志文件输出格式
                file_formatter = logging.Formatter(
                    fmt='[%(asctime)s.%(msecs)03d][%(levelname)s][%(threadName)s(%(thread)d) %(pathname)s %('
                        'module)s.%(funcName)s(%(lineno)d)]:\n%(message)s\n',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
            # 输出到文件
            self.file_handler.setFormatter(file_formatter)
            self.file_handler.setLevel(file_log_level)
            self.addHandler(self.file_handler)

    @staticmethod
    def get_error():
        """使用traceback获取捕获到的错误"""
        return traceback.format_exc()


if __name__ == "__main__":
    logger = Log(console_log_level=10)
    logger.console_handler.setLevel(20)
    logger.debug("OK")
    logger.info("OK")
    logger.warning("OK")
    logger.error("OK")
    logger.critical("OK")

'''
输出format参数中可能用到的格式化串：
%(name)s Logger的名字
%(levelno)s 数字形式的日志级别
%(levelname)s 文本形式的日志级别
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s 调用日志输出函数的模块名
%(funcName)s 调用日志输出函数的函数名
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d 输出日志信息时的，自Logger创建以来的毫秒数
%(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
%(message)s用户输出的消息
**注：1和3/4只设置一个就可以，如果同时设置了1和3，log日志中会出现一条记录存了两遍的问题。

格式化符号
python中时间日期格式化符号：
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12） 
%M 分钟数（00=59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身 
'''
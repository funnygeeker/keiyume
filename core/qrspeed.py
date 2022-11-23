#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 溪梦框架Alpha-QRSpeed/Clousx6/sqv8翻译python后的替代函数模块
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker
from .sqlite import *
from .log import *
import _thread
import random
import time


class QRSpeed():
    def random(num, num_):
        '''
        %随机数1-%变量%%
        (.*)%随机数(.*)-(.*)%(.*)
        {x.group(1)}X6.random(f"{x.group(2)}",f"{x.group(3)}"){x.group(4)}
        '''
        return random.randint(int(num), int(num_))

    def call(self, func: object, time_: str, message: str):
        '''
        $调用 1 xxx$
        '''
        _thread.start_new_thread(
            QRSpeed.call_, self=self, func=func, time_=time_, message=message)

    def call_(self, func: object, time_: str, message: str):
        time.sleep(int(time_)/1000)
        func(self, message)

    def time(time_format: str, time_: float) -> str:
        '''
        %时间yy年MM月dd日HH:mm:ss%
        '''
        if time_ == None:
            time_ = time.localtime(time.time())
        else:
            time_ = time.localtime(time_)
        time_format.replace('yy', '%Y')
        time_format.replace('MM', '%m')
        time_format.replace('dd', '%d')
        time_format.replace('HH', '%H')
        time_format.replace('mm', '%M')
        time_format.replace('ss', '%S')
        return time.strftime(time_format, time_)

    def parameter(message,num):
        if int(num) == -1:
            return message
        return message.split(' ')[int(num)]

class QRSpeed_DB():
    def __init__(self, path: str, table_name: str):
        self.sql = Sqlite()
        self.sql.connect(path)
        self.name = table_name

    def write(self, path: str, key: str, value: str):
        '''
        $写 xxx/yyy/zzz a %b%$
        (.*)\$写 (.*) (.*) (.*)\$(.*)
        {x.group(1)}db.write(f"{x.group(2)}", f"{x.group(3)}", f"{x.group(4)}") {x.group(5)}
        '''
        self.sql.auto_write(table_name=self.name,
                            condition=f"path='{path}' AND key='{key}'",
                            **{'path': path,
                               'key': key,
                               'value': value
                               })

    def read(self, path: str, key: str, default: str):
        '''
        $读 xxx/yyy/zzz a 0$
        (.*)\$读 (.*) (.*) (.*)\$(.*)
        {x.group(1)}db.read(f"{x.group(2)}", f"{x.group(3)}", f"{x.group(4)}") {x.group(5)}
        '''
        result = self.sql.read(table_name=self.name,
                               keys=['value'],
                               condition=f"path='{path}' AND key='{key}'")
        if len(result) == 0:
            if default.isdigit():
                return int(default)
            return default
        elif len(result) == 1:
            if result[0][0].isdigit():
                return int(result[0][0])
            return result[0][0]
        else:
            logger.error('【错误】过多的数据库查询返回值！\n')
            return None

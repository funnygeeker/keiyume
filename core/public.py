# -*- coding : utf-8-*-
# 溪梦框架公共变量模块
import threading
from typing import (Optional, TYPE_CHECKING, Union)
if TYPE_CHECKING:  # 仅用于类型检查
    from configobj import ConfigObj

    from .log import Log
    from . import keiyume  # 为了让 Pyinstaller 打包，勿删
    from .connect import Connect

# 用于存储各个模块之间公用的变量（暂时没想到更好地解决方案了）
lock: Optional["threading.RLock"] = threading.RLock()  # 线程锁
config: Union[dict, "ConfigObj"] = {}  # 配置文件
logger: Optional["Log"] = None  # 日志记录器
connect: Optional["Connect"] = None  # 连接 Websocket 的对象

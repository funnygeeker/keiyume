import re
from typing import Optional
from .config import config, rule


def base(msg: str, keywords: list) -> Optional[tuple]:
    """
    消息检测

    Args:
        msg: 传入的消息
        keywords: 传入的关键词

    Returns:
        Tuple[匹配引擎, 关键词]
    """
    msg = msg.lower()
    for word in keywords:  # 遍历各文件（列表）的值
        if word in msg:
            return '普通', word
    # 如果使用了匹配增强
    if int(config['detection']['plus']):
        # 使用正则表达式去除中英文外的字符
        msg = re.compile(
            '[^A-Z^a-z\u4e00-\u9fa5]').sub('', msg)
        for word in keywords:  # 遍历各文件（列表）的值
            if word in msg:
                return '正则', word
    return None


def img_ocr():
    pass

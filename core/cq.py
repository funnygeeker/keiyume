# -*- coding : utf-8-*-
# 溪梦框架：core/cq.py
# 以函数的形式存储常用的 CQ 码
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume
#
# 参考资料：
# go-cqhttp 帮助中心 - CQ 码：https://docs.go-cqhttp.org/cqcode


from typing import Union


def face(id_: Union[int, str]) -> str:
    """
    QQ表情，ID可能的值详见：
    https://github.com/richardchien/coolq-http-api/wiki/%E8%A1%A8%E6%83%85-CQ-%E7%A0%81-ID-%E8%A1%A8

    Args:
        id_:表情ID
    """
    return f"[CQ:face,id={id_}]"


def record(file: str, magic: int = 0) -> str:
    """
    语音，需要安装 ffmpeg！

    Args:
        file:文件来源，可以是网址，也可以是文件所在的路径
        magic:启用变声，默认 0，设置为 1 表示变声
    """
    return f"[CQ:record,file={file},magic={magic}]"


def at(qq: Union[int, str]) -> str:
    """
    @某人

    Args:
        qq: 要艾特的QQ号（all表示全体成员）
    """
    return f"[CQ:at,qq={qq}]"


def tts(text):
    """
    文本转语音
    通过TX的TTS接口, 采用的音源与登录账号的性别有关

    Args:
        text: 消息内容
    """
    return f"[CQ:tts,text={text}]"


# 经过测试，CQ 码不可用，暂时弃用
# def share(url: str, title: str, content: str = "", image: str = "") -> str:
#     """
#     链接分享
#
#     Args:
#         url: 链接URL
#         title: 标题
#         content: 可选，内容描述
#         image: 可选，图片 URL
#     """
#     return f"[CQ:share,url={url},title={title},content={content},image={image}]"


def music(type_: str, id_: Union[int, str] = "", url: str = "", audio: str = "", title: str = "", content: str = "",
          image_: str = ""):
    """
    音乐分享，需要安装 ffmpeg！

    Args:
        type_:
            custom: 表示音乐自定义分享，需要传入 url, audio, title
            qq: 使用QQ音乐，需要传入 id
            163: 使用网抑云音乐，需要传入 id
            xm: 使用虾米音乐，需要传入 id
        id_: 歌曲 ID
        url: 点击后跳转目标 URL
        audio: 音乐 URL
        title: 标题
        content: 可选，内容描述
        image_: 可选，图片 URL
    """
    return f"[CQ:music,type={type_},id={id_},url={url},audio={audio},title={title},content={content},image={image_}]"


def image(file: str, type_: str = '', cache: int = 1, id_: int = 40000):
    """
    图片

    Args:
        file: 文件来源，可以是网址，也可以是文件所在的路径
        type_: flash 表示闪照, show 表示秀图, 默认普通图片
        cache: 只在通过网络 URL 发送时有效, 表示是否使用已缓存的文件, 默认 1
        id_: 发送秀图时的特效id, 默认为40000
            可用的特效ID:
            40000(普通)  40001(幻影)  40002(抖动)
            40003(生日)  40004(爱你)  40005(征友)
    """
    return f"[CQ:image,file={file},type={type_},cache={cache},id={id_}]"

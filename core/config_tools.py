# -*- coding : utf-8-*-
# 溪梦框架：core/config.py
# 管理框架的配置文件读取与写入
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker/keiyume
#
# 参考资料：
# CSDN - Python 读取大型文本文件：https://blog.csdn.net/potato012345/article/details/88728709
# CSDN - python 模块 chardet（文本编码检测）：https://blog.csdn.net/tianzhu123/article/details/8187470
# 纯净天空 - Python typing.TYPE_CHECKING用法及代码示例：https://vimsky.com/examples/usage/python-typing.TYPE_CHECKING-py.html
import os

from typing import (Optional, Any, List, Union, Type)

try:
    import chardet  # 文件编码检测，需安装
except ImportError:
    print('>> 检测到缺少 chardet 库，正在安装...')
    os.system('pip3 install chardet -i https://mirrors.aliyun.com/pypi/simple/')
    import chardet
try:
    from configobj import ConfigObj
except ImportError:
    print('>> 检测到缺少 configobj 库，正在安装...')
    os.system('pip3 install configobj -i https://mirrors.aliyun.com/pypi/simple/')
    from configobj import ConfigObj

from . import public


def read_ini(file: str, encoding: Optional[str] = None) -> Any:
    """
    读取单个配置置设文件

    注：您可以对返回的对象修改后使用.write()进行写入操作

    Args:
        file (str): 文件所在的路径
        encoding (Optional[str]): 文件编码（可选）
    Returns:
        ConfigObj 对象，可以像字典一样修改和读取里面的值
    """
    if encoding is None:  # 如果没有设置读取文件的编码
        encoding = detect_encoding(file=file)
    return ConfigObj(file, encoding=encoding)


def read_file_as_text(file: str, encoding: Optional[str] = None) -> str:
    """
    读取文本并返回字符串

    Args:
        file: 文本文件路径
        encoding: 文本编码

    Returns:
        字符串形式的文本内容
    """
    if encoding is None:  # 如果没有文本编码参数，则自动识别编码
        encoding = detect_encoding(file)
    with open(file, "r", encoding=encoding) as all_text:
        return ''.join(all_text)


def read_file_as_list(file: str, keyword: Optional[str] = None, choose: bool = True,
                      front: bool = True, encoding: Optional[str] = None) -> List[str]:
    """
    读取文本文件，去除空行，并以列表的形式输出

    不支持匹配换行符

    Args:
        file: 文本文件路径
        keyword: 选择前（后）缀包含关键词的内容
        choose: 模式
            True: 选择包含前（后）缀的内容
            False: 排除包含前（后）缀的内容
        front: 读取模式
            True: 从文本前部分判断
            False: 从文本后部分判断
        encoding: 文本编码

    Returns:
        含有文本内容的列表，每行不含换行符
    """
    if encoding is None:  # 如果没有文本编码参数，则自动识别编码
        encoding = detect_encoding(file)
    with open(file, "r", encoding=encoding) as all_text:
        if keyword is None:  # 如果不需要排除或选择某字符串开头的文本行，则直接以列表形式返回文本
            text_list = [text.strip("\n") for text in all_text if text.strip("\n") != ""]
        else:  # 如果需要排除或选择某字符串开头的文本行
            if choose:  # 选择模式
                if front:  # 选择模式，从前选取
                    text_list = [text.strip("\n") for text in all_text if text.strip(
                        "\n") != "" and text.strip("\n")[0:len(keyword)] == keyword]

                else:  # 选择模式，从后选取
                    text_list = [text.strip("\n") for text in all_text if text.strip(
                        "\n") != "" and text.strip("\n")[-len(keyword):] == keyword]
            else:  # 排除模式
                if front:
                    # 排除模式，从前排除
                    text_list = [text.strip("\n") for text in all_text if text.strip(
                        "\n") != "" and text.strip("\n")[0:len(keyword)] != keyword]
                else:
                    # 排除模式，从后排除
                    text_list = [text.strip("\n") for text in all_text if text.strip(
                        "\n") != "" and text.strip("\n")[-len(keyword):] != keyword]
    return text_list


def read_file_in_folder(path: str,
                        extension: str = '.txt',
                        list_count: int = 100,
                        keyword: Optional[str] = None,
                        choose: bool = True,
                        front: bool = True,
                        return_type: str = 'list',
                        encoding: Optional[str] = None):
    """
    读取文件夹下的指定文件类型的内容并返回列表

    不支持匹配换行符

    Args:
        path: 文件夹路径
        extension: 文件扩展名
        list_count: 最大读取的文件数限制，默认100个
        keyword: 选择前（后）缀包含关键词的内容
        choose: 模式
            True: 选择包含前（后）缀的内容
            False: 排除包含前（后）缀的内容
        front: 读取模式
            True: 从文本前部分判断
            False: 从文本后部分判断
        encoding: 文本编码
        return_type: 返回类型
            'list': 返回列表
            'dict': 返回字典
        encoding: 文本编码

    Returns:
        list: 文件夹下的指定文件类型的内容列表，每行不含换行符
        dict: 文件夹下的指定文件类型的内容字典，每行不含换行符
    """
    path = path.replace("\\", "/")
    path = path.rstrip("/")  # 文件夹路径合法化
    file_names = os.listdir(path)  # 获取文件夹下的所有文件和文件夹名称
    text_list = []
    list_dict = {}
    cycle_count = 0  # 用于计算读取的有效行数
    extension = extension.lower()  # 扩展名变为小写形式
    for file_name in file_names:  # 遍历文件夹
        # 判断是否为需要读取的后缀
        if ((os.path.splitext(file_name)[1]).lower() == extension or extension == '*') \
                and os.path.isfile(f'{path}/{file_name}'):
            # 判断是否为文件，小写处理文件扩展名，确定是否为需要读取的文件，并进行读取
            data = read_file_as_list(file=f'{path}/{file_name}', keyword=keyword, choose=choose,
                                     front=front, encoding=encoding)
            list_dict[os.path.splitext(file_name)[0]] = data
            text_list += data
            cycle_count += 1
            if list_count <= cycle_count:  # 如果超出文件读取数
                break
    if return_type == 'dict':  # 返回模式为字典
        return list_dict
    else:  # 返回模式为列表
        return text_list


def create_file(file: str, text: str = '', encoding: str = 'utf-8') -> bool:
    """
    检查文本文件是否存在

    不存在则可创建并写入内容

    Args:
        file: 文本文件路径
        text: 需要写入的文本内容
        encoding: 文本编码

    Returns:
        bool: 文本文件是否已存在
    """
    if os.path.isfile(file):  # 如果文件存在
        return True
    if not os.path.exists(os.path.dirname(file)):  # 若不存在文件目录，则自动创建
        os.makedirs(os.path.dirname(file))
    with open(file, 'w', encoding=encoding) as file:
        file.write(text)
        return False


def detect_encoding(file: str) -> str:
    """
    文本编码检测

    无法识别则默认为"utf-8"编码

    Args:
        file: 文本文件路径

    Returns:
        文本编码
    """
    with open(file, 'rb') as file:
        result = chardet.detect(file.read(1048576))  # 最多读取1MB文件进行检测
        # print(result['confidence'])#
        if float(result['confidence']) >= 0.5:  # 如果置信度大于50%
            return result['encoding'].lower()
        else:
            # 无法识别则默认为"utf-8"编码
            return 'utf-8'


def list_type_convert(type_: Union[Type[str], Type[int], Type[float]],
                      obj: Union[str, List[str]]) -> List[Union[str, int, float]]:
    """
        读取框架运行需要的，./config 下的所有配置文件

        Args:
            type_: 需要转换成的类型
            obj: 需要转换的列表或字符串
        """
    if type(obj) is str:  # 如果为字符串则转换成列表
        if obj == '':  # 如果字符为空则返回空列表
            return []
        else:
            obj = [obj]

    return list(map(type_, obj))


def load_config(file: str = './config.ini') -> None:
    """
    读取框架运行需要的，./config 下的所有配置文件

    Args:
        file: 配置文件所在的路径
    """
    public.config = read_ini(file)
    # 判断是否为文件，小写处理文件扩展名，确定是否为需要读取的文件，并进行读取
    # 将部分数据全部转化为存储了整数的列表，用于读取
    public.config['admin']['super_user'] = \
        list_type_convert(int, public.config['admin']['super_user'])
    public.config['admin']['super_admin'] = \
        list_type_convert(int, public.config['admin']['super_admin'])
    public.config['plugin']['enable_group'] = \
        list_type_convert(int, public.config['plugin']['enable_group'])
    public.config['plugin']['disable_group'] = \
        list_type_convert(int, public.config['plugin']['disable_group'])

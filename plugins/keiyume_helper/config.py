import json
import os
import threading
from typing import Optional

from core import config_tools
from . import database

lock = threading.RLock()
'锁'
plugin_path = os.path.dirname(__file__).replace("\\", "/")  # 自动获取当前插件所在的路径
'插件所在的文件夹路径'
config = config_tools.read_ini(file=f'{plugin_path}/config/config.ini')
'所有设置'
if not os.path.exists(f"{plugin_path}/data"):  # 若不存在数据库路径，则自动创建
    os.makedirs(f"{plugin_path}/data")
db = database.DB(f"{plugin_path}/data/keiyume_helper.db")
'消息记录数据库'
reply = {}
'所有发送语句'
rule = {}
'所有词库'
role = {}
'机器人在各个群的身份'


def load_conf():
    """读取并加载配置文件到变量"""
    global config
    with lock:
        reply_read_rule = ['ban', 'random', 'rule', 'welcome']
        rule_read_rule = ['approval', 'ban', 'ignore']
        for folder_name in reply_read_rule:
            reply[folder_name] = config_tools.read_file_in_folder(path=f'{plugin_path}/config/reply/{folder_name}',
                                                                  keyword='#', choose=False)
        for folder_name in rule_read_rule:
            rule[folder_name] = config_tools.read_file_in_folder(path=f'{plugin_path}/config/rule/{folder_name}',
                                                                 keyword='#', choose=False)

        # 始化所有配置文件，将需要转化的配置转化为合适的值
        type_convert_rule = {'group': ['group_id', 'report_user_id'], 'punish': ['ban_time'],
                             'manage': ['timed_whole_ban']}
        # 将指定的配置转换为数字形式
        for section in type_convert_rule:
            for keyword in type_convert_rule[section]:
                config[section][keyword] = config_tools.list_type_convert(int, config[section][keyword])
        dirs_name = os.listdir(f"{plugin_path}/config/reply/rule")  # 获取文件夹下的所有文件和文件夹名称

        # 加载规则回复配置
        reply['rule'] = {}
        for file_name in dirs_name:  # 遍历文件夹
            if os.path.isfile(f'{plugin_path}/config/reply/rule/{file_name}') and \
                    os.path.splitext(file_name)[1].lower() == '.txt':  # 判断是否为文件
                # 读取目录下所有txt文件
                reply['rule'][file_name] = config_tools.read_file_as_text(
                    f'{plugin_path}/config/reply/rule/{file_name}')

        # 将规则回复进行分片处理
        all_rule = []
        for file in reply['rule']:
            reply['rule'][file] = reply['rule'][file].split('\n\n')  # 对规则进行分片
            part = [part.split("\n") for part in reply['rule'][file] if part.strip("\n") != ""]  # 去除多余的空行
            for _part in part:
                if _part[0] and _part[0][0] != '#':
                    all_rule.append(_part)
        reply['rule'] = all_rule
        # print(json.dumps(reply['rule'],ensure_ascii=False,indent=4))


def change_rule_or_reply_setting(operation: str, path: str, content: Optional[list] = None) -> Optional[str]:
    """
    修改由配置文件组成的词库设置

    Args:
        operation: 操作类型：add，del，clear
        path: 对应的配置文件夹的[部分路径]，如：reply/ban，reply/random，reply/welcome，rule/approval，rule/ban，rule/ignore
        content: 需要添加或者删除的内容

    Returns:
        操作结果
    """
    path = f"{plugin_path}/config/{path}"
    if content is None:
        content = []
    with lock:
        # 读取目录下所有txt文件
        if operation == 'add':
            conf = config_tools.read_file_in_folder(path=f'{path}', keyword='#', choose=False)
            content = list(set(content) - set(conf))
            if not content:
                return '添加失败：内容重复！'

            else:
                if os.path.isfile(f'{path}/add.txt'):  # 文件存在则识别编码
                    encoding = config_tools.detect_encoding(f'{path}/add.txt')
                else:
                    encoding = "utf-8"
                with open(f'{path}/add.txt', "a", encoding=encoding) as file:
                    content = "\n".join(content)
                    file.write(f"\n{content}")
                load_conf()
                return '添加成功！'

        elif operation == 'del':
            conf = config_tools.read_file_in_folder(path=f'{path}', keyword='#', choose=False, return_type='dict')
            note = config_tools.read_file_in_folder(path=f'{path}', keyword='#', return_type='dict')
            for file_name in conf:
                with open(f'{path}/{file_name}.txt', "w",
                          encoding=config_tools.detect_encoding(f'{path}/{file_name}.txt')) as file:
                    file.write(
                        "\n".join(note[file_name]) + "\n" + "\n".join(set(conf[file_name]) - set(content)))
            load_conf()
            return '删除成功！'

        elif operation == 'clear':
            note = config_tools.read_file_in_folder(path=f'{path}', keyword='#', return_type='dict')
            for file_name in note:
                with open(f'{path}/{file_name}.txt', "w",
                          encoding=config_tools.detect_encoding(f'{path}/{file_name}.txt')) as file:
                    file.write("\n".join(note[file_name]))
            load_conf()
            return '清除成功！'

        else:
            return None

# 功能弃用
# def change_reply_rule_setting(operation: str, content: Optional[list] = None):
#     """
#     修改由配置文件组成的回复规则
#
#     Args:
#         operation: 操作类型：add，del，clear
#         content: 需要添加或者删除的内容
#
#     Returns:
#         操作结果
#     """
#     path = f"{plugin_path}/config/reply/rule"
#     with lock:
#         note = config_tool.read_file_in_folder(path=path, keyword='#', return_type='dict')
#         conf = {}
#         file_names = os.listdir(path)  # 获取文件夹下的所有文件和文件夹名称
#         for file_name in file_names:  # 遍历文件夹
#             if os.path.isfile(f'{path}/{file_name}') and os.path.splitext(file_name)[1].lower() == '.txt':  # 判断是否为文件
#                 # 读取目录下所有txt文件
#                 conf[os.path.splitext(file_name)[0].lower()] = config_tool.read_file_as_text(f'{path}/{file_name}')
#
#         # 将规则回复进行分片处理
#         for file in conf:
#             conf[file] = conf[file].split('\n\n')  # 对规则进行分片
#             conf[file] = [part.strip("\n") for part in conf[file] if part.strip("\n") and part[0] != "#"]  # 去除多余的空行
#             for index, part in enumerate(conf[file]):
#                 conf[file][index] = conf[file][index].split("\n")
#         # 读取目录下所有txt文件
#         print(json.dumps(conf, ensure_ascii=False, indent=4))
#         if operation == 'add':
#             if len(content) > 1:
#                 for file_name in conf:
#                     for part in conf[file_name]:
#                         if part[0] == content[0]:
#                             return '你已经添加过了呐！'
#                 else:
#                     if os.path.isfile(f'{path}/add.txt'):  # 文件存在则识别编码
#                         encoding = config_tool.detect_encoding(f'{path}/add.txt')
#                     else:
#                         encoding = "utf-8"
#                     with open(f'{path}/add.txt', "a", encoding=encoding) as file:
#                         content = "\n".join(content)
#                         file.write(f"\n\n{content}")
#                         load_conf()
#                         return '回复规则添加成功！'
#             else:
#                 return '添加的问题没有指定回复语句哦！'
#
#         elif operation == 'del':
#             for file_name in conf:
#                 new_file = []
#                 for part in conf[file_name]:
#                     if part[0] != content[0]:
#                         new_file.append(part)
#                 with open(f'{path}/{file_name}.txt', "w",
#                           encoding=config_tool.detect_encoding(f'{path}/{file_name}.txt')) as file:
#                     print(json.dumps(note,ensure_ascii=False,indent=4))
#                     if not note[file_name]:
#                         note[file_name] = ['']
#                     file.write("\n".join(note[file_name]) + "\n\n" + "\n".join("\n".join(new_file)))
#             load_conf()
#             return '问题删除成功！'
#
#         elif operation == 'clear':
#             note = config_tool.read_file_in_folder(path=f'{path}', keyword='#', return_type='dict')
#             for file_name in note:
#                 with open(f'{path}/{file_name}.txt', "w",
#                           encoding=config_tool.detect_encoding(f'{path}/{file_name}.txt')) as file:
#                     file.write("\n".join(note[file_name]))
#             load_conf()
#             return '清除成功！'
#
#         else:
#             return None

# logger.debug(f'{json.dumps(XM_Config.all_config,ensure_ascii=False,indent=4)}')
# logger.debug(f'{json.dumps(XM_Config.all_words,ensure_ascii=False,indent=4)}')
# logger.debug(f'{json.dumps(XM_Config.all_send,ensure_ascii=False,indent=4)}')
# print(json.dumps(reply,indent=4,ensure_ascii=False))

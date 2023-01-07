from core.keiyume import logger, api

from . import tools
from . import config


def reply(self):
    """所有回复"""
    if not rule_reply(self):
        random_reply(self)


def rule_reply(self):
    """规则回复"""
    if int(config.config['reply']['rule']):  # 如果启用了规则回复
        if int(config.config['reply']['need_at']):  # 如果需要被艾特才能触发
            is_at = self.is_at_me()  # 检查是否被艾特
        else:
            is_at = 1  # 否则默认直接回复
        if is_at:
            for part in config.reply['rule']:
                if part[0] in self.message:
                    if len(part) < 2:
                        logger.warning(f'【溪梦助手】规则回复功能的配置文件存在缺失答案的问题，请补充答案！')
                        return False
                    part_ = part.copy()
                    del part_[0]
                    api.send_group_msg(self.group_id, tools.random_from_list(part_).replace(r'\n', '\n'))
                    return True
    return False


def random_reply(self):
    """随机回复"""
    if self.is_at_me() and int(config.config['reply']['random']) and config.reply['random']:  # 如果启用了随机回复，且随机回复的内容不为空
        send_msg = f"{tools.random_from_list(config.reply['random'])}"
        api.send_group_msg(self.group_id, send_msg.replace(r'\n', '\n'))

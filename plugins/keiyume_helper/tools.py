import random
from core.keiyume import api


def get_role(group_id, user_id):
    """
    获取用户在对应群聊中的身份

    Returns:
        数字越大，身份越高
    """
    role = api.get_group_member_info(group_id, user_id)['data']['role']
    if role == 'member':
        role = 0
    elif role == 'admin':
        role = 1
    elif role == 'owner':
        role = 2
    return role


def random_from_list(list_: list) -> str:
    """从列表中随机选取"""
    return list_[random.randint(0, len(list_) - 1)]

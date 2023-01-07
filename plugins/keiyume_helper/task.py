import time

from . import config
from core.keiyume import api, scheduler, logger

# def update_role():
#     """更新机器人在各个群中的身份"""
#     for group_id in config.config['group']['group_id']:
#         role = api.get_group_member_info(group_id, connect.self_user_id)['role']
#         if role == 'member':
#             role = 0
#         elif role == 'admin':
#             role = 1
#         elif role == 'owner':
#             role = 2
#         config.role[group_id] = role


# logger.debug('【溪梦助手】正在添加定时更新群聊身份计划任务...')
# scheduler.add_job(func=update_role, trigger='interval', minutes=5, id='keiyume_helper_update_role')


del_message_id = {}
'即将撤回的消息ID {message_id: 任务对象, ...}'


def timed_del_msg(message_id: int):
    """定时撤回消息"""
    del del_message_id[message_id]
    config.db.write_del_msg(message_id)  # 将对应的消息标记为已撤回
    api.delete_msg(message_id=message_id)


def send_report(user_id: list, message: str):
    """发送聊天报告"""
    for user in user_id:
        time.sleep(5)
        api.send_private_msg(user_id=user, message=message)


def whole_ban(group_id: list, enable: bool):
    """全体禁言"""
    global whole_ban_state
    if enable:
        task_type = '开始禁言'
    else:
        task_type = '解除禁言'
    logger.info(f'【溪梦助手】开始执行全体禁言计划任务：{task_type}')
    if enable and not whole_ban_state:
        # 如果需要禁言，且需要禁言禁言状态为否
        whole_ban_state = True
        for group in group_id:
            time.sleep(1)
            api.set_group_whole_ban(group_id=group, enable=True)
    elif not enable and whole_ban_state:
        # 如果不需要禁言，且需要禁言禁言状态为是
        whole_ban_state = False
        for group in group_id:
            time.sleep(1)
            api.set_group_whole_ban(group_id=group, enable=False)


whole_ban_state = False
'全体禁言状态'
punish_record = {}
"处罚记录 {(user_id, group_id):{'num': 0, 'ban_num': 0}, ...}"

# 全体禁言计划任务
if config.config['group']['group_id'] and len(config.config['manage']['timed_whole_ban']) == 2:
    logger.debug('【溪梦助手】正在添加定时全体禁言计划任务...')
    whole_ban_time = config.config['manage']['timed_whole_ban'][0]
    whole_unban_time = config.config['manage']['timed_whole_ban'][1]
    scheduler.add_job(func=whole_ban, trigger='cron', hour=whole_ban_time[:-2],
                      minute=whole_ban_time[-2:], second=0,
                      kwargs={'group_id': config.config['group']['group_id'], 'enable': True},
                      id='keiyume_helper_group_whole_ban')
    scheduler.add_job(func=whole_ban, trigger='cron', hour=whole_unban_time[:-2],
                      minute=whole_unban_time[-2:], second=0,
                      kwargs={'group_id': config.config['group']['group_id'],
                              'enable': False}, id='keiyume_helper_group_whole_unban')
else:
    logger.debug('【溪梦助手】全体禁言计划任务未启用...')


def clear_punish_record():
    """清空惩罚记录"""
    global punish_record
    punish_record = {}
    logger.info('【溪梦助手】已清空群聊惩罚计数...')


# 清空惩罚计数计划任务
if config.config['punish']['cycle']:
    logger.debug('【溪梦助手】正在添加定时清空惩罚计数计划任务...')
    scheduler.add_job(func=clear_punish_record, trigger='interval',
                      minutes=int(config.config['punish']['cycle']),
                      id='keiyume_helper_clear_punish_num')
else:
    logger.debug('【溪梦助手】定时清空惩罚计数计划任务未启用...')


def clear_sql_msg():
    """清理数据库中的消息"""
    config.db.clear_msg(20000)
    logger.debug('【溪梦助手】正在执行数据库清理...')


logger.debug('【溪梦助手】正在添加定时数据库清理计划任务...')
scheduler.add_job(func=clear_sql_msg, trigger='interval',
                  minutes=60,
                  id='keiyume_helper_clear_sql_msg')

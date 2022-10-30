import time
from .xm_config import *
from core.api import Api
from core.connect_mgr import *


class XM_Task():
    del_message_id={}
    '即将撤回的消息ID {message_id:任务对象,...}'
    group_whole_ban_state=False
    '全体禁言状态'
    group_punish_record=[]
    '''群聊处罚记录 [{'group_id': self.group_id, 'user_id': self.user_id, 'num': 0, 'ban_num': 0},...]'''
    def Del_Message(message_id:int):
        '定时撤回消息'
        del XM_Task.del_message_id[message_id]
        Api.delete_msg(message_id=message_id)

    def Group_Whole_Ban(group_id:list,enable:bool):
        '全体禁言'
        if enable:
            task_type='开始禁言'
        elif not enable:
            task_type='解除禁言'
        logger.info(f'【信息】开始执行全体禁言计划任务：{task_type}\n')
        if enable==True and XM_Task.group_whole_ban_state == False:
            # 如果需要禁言，且需要禁言禁言状态为否
            XM_Task.group_whole_ban_state=True
            for group in group_id:
                time.sleep(1)
                Api.set_group_whole_ban(group_id=group,enable=True)
        elif enable==False and XM_Task.group_whole_ban_state == True:
            # 如果不需要禁言，且需要禁言禁言状态为是
            XM_Task.group_whole_ban_state=False
            for group in group_id:
                time.sleep(1)
                Api.set_group_whole_ban(group_id=group,enable=False)

    def Clear_Punish_Record():
        '清空惩罚计数'
        XM_Task.group_punish_record=[]
        logger.info('【信息】已清空群聊惩罚计数...')

    def Send_Group_Report(user_id:list,message:str):
        for user in user_id:
            time.sleep(2)
            Api.send_private_msg(user_id=user,message=message)


# 全体禁言计划任务
if len(XM_Config.all_config['config']['groups_manage']['groups_manage']) != 0 and len(XM_Config.all_config['group']['group_function']['timed_whole_ban']) ==2:
    group_whole_ban_time =XM_Config.all_config['group']['group_function']['timed_whole_ban'][0]
    group_whole_unban_time =XM_Config.all_config['group']['group_function']['timed_whole_ban'][1]
    logger.debug('正在添加定时全体禁言计划任务...')
    scheduler.add_job(func=XM_Task.Group_Whole_Ban,trigger='cron',hour=group_whole_ban_time[:-2],minute=group_whole_ban_time[-2:],second=0,kwargs={'group_id':XM_Config.all_config['config']['groups_manage']['groups_manage'],'enable':True},id='group_whole_ban')
    scheduler.add_job(func=XM_Task.Group_Whole_Ban,trigger='cron',hour=group_whole_unban_time[:-2],minute=group_whole_unban_time[-2:],second=0,kwargs={'group_id':XM_Config.all_config['config']['groups_manage']['groups_manage'],'enable':False},id='group_whole_unban')
    #scheduler.add_job(func=XM_Task.Test,trigger='cron',hour='*',minute='*',second='*',id='test')
    #scheduler.add_job(func=XM_Task.Test,trigger='interval',seconds=5,id='test2')
else:
    logger.debug('全体禁言计划任务未启用...')

if XM_Config.all_config['group']['group_punish']['group_punish_cycle'] != '':
    logger.debug('正在添加定时清空惩罚计数计划任务...\n')
    scheduler.add_job(func=XM_Task.Clear_Punish_Record,trigger='interval',minutes=int(XM_Config.all_config['group']['group_punish']['group_punish_cycle']),id='clear_punish_num')
else:
    logger.debug('定时清空惩罚计数计划任务未启用...\n')

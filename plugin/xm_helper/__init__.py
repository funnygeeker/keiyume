# 导入框架模块
from core.api import *
from core.event import *
from core.log_mgr import *

# 导入另外需要的模块
from .xm_task import *
from .xm_tools import *
from .xm_reply import *
from .xm_config import *
from .xm_detection import *

# 插件名称
name = '【溪梦助手-群管2.0.0_BETA1】'

# 插件作者
author = '稽术宅'

# 插件版本
version = '2.0.0_BETA1'

# 运行优先级
# 用于区分加载顺序
# 数字越小越先执行
# 1024及以下被本框架开发者保留
# 无特殊需求请不要设置小于1024的值
sequence = 512

# 插件说明
description = '''溪梦框架的群聊管理插件：溪梦助手，让溪梦协助你更轻松的管理群聊~
  
  【特别致谢】
  句库补充：
  QQ：15140**011  汐酱'''

# 插件运行位置
# start 程序主体运行前
# before 消息识别处理前
# after 消息识别处理后
# exit 程序正常退出后
# cmd 命令被识别为非内置/无效时
location = 'after'

# 兼容性标识（兼容的溪梦框架版本）
compatible = ['2.0.0_BETA1']


class Main(Event):
    def __init__(self, obj: object):
        super().__init__(obj)

    def Run(self, *args, **kwargs):
        '''【符合规范的插件将从这里开始运行】'''
        # 消息处理 #
        # 如果事件为需要管理的群的消息
        if self.on_group_message(group_id=XM_Config.all_config['config']['groups_manage']['groups_manage']):
            '''if self.on_full_match('ban'):
                XM_Task.Group_Whole_Ban(XM_Config.all_config['config']['groups_manage']['groups_manage'],enable=True)
            elif self.on_full_match('unban'):
                XM_Task.Group_Whole_Ban(XM_Config.all_config['config']['groups_manage']['groups_manage'],enable=False)'''

            # 默认消息不是广告，不是脏话，无触发关键词，无关键词类型，无触发的检测引擎
            self.msg_status = {'ads': 0, 'bad': 0, 'ignore': 0,
                               'key_word': None, 'key_word_type': None, 'engine': None}
            # 如果启用了广告检测
            if int(XM_Config.all_config['group']['group_detection']['ads_detection']) == 1:
                # 检测广告
                XM_Detection.Base_Detection(
                    self=self, files=XM_Config.all_words['ads_words'], detection_type='ads', msg=self.message)
            # 如果启用了脏话检测
            if int(XM_Config.all_config['group']['group_detection']['bad_detection']) == 1:
                # 检测脏话
                XM_Detection.Base_Detection(
                    self=self, files=XM_Config.all_words['bad_words'], detection_type='bad', msg=self.message)

            # 如果是广告或违禁词，且启用了忽略词检测
            if int(XM_Config.all_config['group']['group_detection']['ignore_detection']) == 1:
                # 检测忽略词
                XM_Detection.Base_Detection(
                    self=self, files=XM_Config.all_words['ignore_words'], detection_type='ignore', msg=self.message)
            # 消息结算
            # logger.info(f"【检测结果】\n原文：{self.message}\n群聊：{self.group_id} 用户：{self.user_id}\n广告：{self.msg_status['ads']} 脏话：{self.msg_status['bad']} 忽略词：{self.msg_status['ignore']} 引擎：{self.msg_status['engine']} 关键词：{self.msg_status['key_word']} 关键词类型：{self.msg_status['key_word_type']}\n")
            if self.on_sub_type(sub_type='normal') and self.is_group_member():  # 如果是普通成员发的常规消息
                # 如果为不良消息，且不含忽略词
                if (self.msg_status['ads'] == 1 or self.msg_status['bad'] == 1) and self.msg_status['ignore'] == 0:
                    # 如果启用了撤回消息
                    if XM_Config.all_config['group']['group_punish']['del_msg_delay'] != '':
                        with Lock:
                            XM_Task.del_message_id[self.message_id] = scheduler.add_job(func=XM_Task.Del_Message, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                time.time()+2+int(XM_Config.all_config['group']['group_punish']['del_msg_delay']))), kwargs={'message_id': self.message_id}, id=str(self.message_id))

                    # 如果启用了广告提醒且为广告消息
                    if int(XM_Config.all_config['group']['group_tips']['ads_tips']) == 1 and self.msg_status['ads'] == 1:
                        tips_msg = f"[CQ:at,qq={self.user_id}] {XM_Tools.Random_List_Value_In_Dict(XM_Config.all_send['ads_tips'])}"
                        scheduler.add_job(func=Api.send_group_msg, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                            time.time()+2)), kwargs={'group_id': self.group_id, 'message': tips_msg.replace(r'\n', '\n')})
                    # 如果启用了违禁词提醒且为违禁消息
                    elif int(XM_Config.all_config['group']['group_tips']['bad_tips']) == 1 and self.msg_status['bad'] == 1:
                        tips_msg = f"[CQ:at,qq={self.user_id}] {XM_Tools.Random_List_Value_In_Dict(XM_Config.all_send['bad_tips'])}"
                        scheduler.add_job(func=Api.send_group_msg, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                            time.time()+2)), kwargs={'group_id': self.group_id, 'message': tips_msg.replace(r'\n', '\n')})

                    # 惩罚次数记录以及禁言踢出
                    punish_mode = '无'  # 惩罚方式默认为无
                    cycles_num = 0  # 重置循环数
                    for record in XM_Task.group_punish_record:  # 任务处理队列中匹配是否已有记录
                        # 如果已有记录
                        if self.group_id == record['group_id'] and self.user_id == record['user_id']:
                            # 添加惩罚次数记录
                            XM_Task.group_punish_record[cycles_num]['num'] += 1
                            # 如果有有效的踢出次数且犯错次数达到了移出群聊标准
                            if XM_Config.all_config['group']['group_punish']['kick_num'] != '' and XM_Task.group_punish_record[cycles_num]['num'] >= int(XM_Config.all_config['group']['group_punish']['kick_num']):
                                punish_mode = '移出群聊'  # 惩罚方式设置
                                # 计划任务添加踢出
                                scheduler.add_job(func=Api.set_group_kick, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                    time.time()+2)), kwargs={'group_id': self.group_id, 'user_id': self.user_id})
                            # 否则如果有有效的初次禁言触发禁言次数且犯错次数达到了禁言标准
                            elif XM_Config.all_config['group']['group_punish']['ban_num'] != '' and XM_Task.group_punish_record[cycles_num]['num'] >= int(XM_Config.all_config['group']['group_punish']['ban_num']):
                                # 如果禁言次数超过了预设的最大禁言次数
                                if len(XM_Config.all_config['group']['group_punish']['ban_time']) - 1 <= XM_Task.group_punish_record[-1]['ban_num']:
                                    # 惩罚方式设置
                                    punish_mode = f"禁言{XM_Config.all_config['group']['group_punish']['ban_time'][-1]}分钟"
                                    # 根据禁言设置规则中最后的时间禁言
                                    scheduler.add_job(func=Api.set_group_ban, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                        time.time()+2)), kwargs={'group_id': self.group_id, 'user_id': self.user_id, 'duration': 60*XM_Config.all_config['group']['group_punish']['ban_time'][-1]})
                                else:
                                    # 惩罚方式设置
                                    punish_mode = f"禁言{XM_Config.all_config['group']['group_punish']['ban_time'][XM_Task.group_punish_record[cycles_num]['ban_num']]}分钟"
                                    # 根据禁言设置规则禁言
                                    scheduler.add_job(func=Api.set_group_ban, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                        time.time()+2)), kwargs={'group_id': self.group_id, 'user_id': self.user_id, 'duration': 60*XM_Config.all_config['group']['group_punish']['ban_time'][XM_Task.group_punish_record[cycles_num]['ban_num']]})
                                # 记录已禁言次数
                                XM_Task.group_punish_record[cycles_num]['ban_num'] += 1
                            break
                        else:
                            cycles_num += 1
                    else:  # 如果没有记录
                        XM_Task.group_punish_record.append(
                            {'group_id': self.group_id, 'user_id': self.user_id, 'num': 0, 'ban_num': 0})  # 在队列末尾添加记录
                        # 添加惩罚次数记录
                        XM_Task.group_punish_record[cycles_num]['num'] += 1
                        # 如果有有效的踢出计数,且触发数为1
                        if XM_Config.all_config['group']['group_punish']['kick_num'] != '' and XM_Config.all_config['group']['group_punish']['kick_num'] == 1:
                            punish_mode = '移出群聊'  # 惩罚方式设置
                            scheduler.add_job(func=Api.set_group_kick, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                time.time()+4)), kwargs={'group_id': self.group_id, 'user_id': self.user_id})  # 将其移出群聊
                        # 否则如果有有效的初次禁言触发禁言数,且触发数为1
                        elif XM_Config.all_config['group']['group_punish']['ban_num'] != '' and XM_Config.all_config['group']['group_punish']['ban_num'] == 1:
                            # 惩罚方式设置
                            punish_mode = f"禁言{XM_Config.all_config['group']['group_punish']['ban_time'][0]}分钟"
                            scheduler.add_job(func=Api.set_group_ban, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                time.time()+2)), kwargs={'group_id': self.group_id, 'user_id': self.user_id, 'duration': 60*XM_Config.all_config['group']['group_punish']['ban_time'][0]})  # 根据设置规则禁言
                            # 记录已禁言次数
                            XM_Task.group_punish_record[-1]['ban_num'] = 1
                    # 如果启用了发送消息报告
                    if XM_Config.all_config['config']['admin']['groups_report_user_id'] != []:
                        scheduler.add_job(func=XM_Task.Send_Group_Report, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                            time.time()+4)), kwargs={'user_id': XM_Config.all_config['config']['admin']['groups_report_user_id'], 'message': f"【消息报告】\n群聊：{self.group_id}\n用户：{self.user_id}\n计数：{XM_Task.group_punish_record[cycles_num]['num']}\n时间：\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n匹配引擎：{self.msg_status['engine']}\n触发关键词：{self.msg_status['key_word']}\n关键词类型：{self.msg_status['key_word_type']}\n惩罚方式：{punish_mode}\n消息内容：\n{self.message[:300]}\n（只显示前300字）"})
                else:
                    # 问答/随机回复
                    XM_Reply.Reply(self=self)

            elif self.on_sub_type(sub_type='normal') and (self.is_group_admin() or self.is_group_owner()):  # 如果是群聊管理
                # 问答/随机回复
                XM_Reply.Reply(self=self)

                '''if self.on_sub_normal(): #如果是普通消息
                    if self.is_group_owner() or self.is_group_admin():
                        pass
                elif self.on_sub_anonymous(): #如果是匿名消息
                    pass'''

        # 如果事件为需要管理的群有成员加群
        elif self.on_group_notice(group_id=XM_Config.all_config['config']['groups_manage']['groups_manage'], notice_type='group_increase'):
            # 如果启用了入群欢迎
            if int(XM_Config.all_config['group']['group_tips']['welcome_tips']):
                tips_msg = f"[CQ:at,qq={self.user_id}] {XM_Tools.Random_List_Value_In_Dict(XM_Config.all_send['welcome_tips'])}"
                scheduler.add_job(func=Api.send_group_msg, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                    time.time()+2)), kwargs={'group_id': self.group_id, 'message': tips_msg})

        # 需要撤回的消息若被提前撤回则删除计划任务
        elif self.on_group_notice(notice_type='group_recall'):
            with Lock:
                if XM_Task.del_message_id.get(self.message_id) != None:
                    scheduler.remove_job(str(self.message_id))
                    logger.info(
                        f'【信息】消息ID：{self.message_id} 已在撤回计划任务前被撤回，已删除本次撤回任务！\n')
                    del XM_Task.del_message_id[self.message_id]

        # 如果事件为需要管理的群的请求
        elif self.on_group_request(group_id=XM_Config.all_config['config']['groups_manage']['groups_manage']):
            # 如果为入群申请，且开启了加群自动审批
            if self.on_sub_type(sub_type='add') or self.on_sub_type(sub_type='invite'):
                logger.info(
                    f"【信息】群聊 {self.group_id} 中 {self.user_id} 申请加群，验证消息：\n{self.data['comment']}\n")
                if int(XM_Config.all_config['group']['group_function']['group_approval']):
                    # 对申请进行处理
                    if ('问题：' in self.data['comment']) and ('\n答案：' in self.data['comment']):
                        comment = self.data['comment'].split('\n答案：')[-1]
                    # 忽略邀请加群
                    elif ('来自：' in self.data['comment']) and ('的邀请' in self.data['comment']):
                        comment = ''
                    else:
                        comment = ''
                    # 匹配关键词，通过符合要求的请求
                    for approval_word in XM_Tools.Splice_List(the_dict=XM_Config.all_words['group_approval']):
                        if approval_word in comment:
                            scheduler.add_job(func=Api.set_group_add_request, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                time.time()+2)), kwargs={'flag': self.data['flag'], 'sub_type': self.data['sub_type'], 'approve': True, 'group_id': self.group_id, 'user_id': self.user_id})
                            break


'''        elif self.on_notice('group_ban') and self.user_id == 0: # 全体禁言事件
            if self.sub_type == 'ban':
                XM_Task.group_whole_ban_state[self.group_id] == True
                print('开始全体禁言',XM_Task.group_whole_ban_state)
            elif self.sub_type == 'lift_ban':
                XM_Task.group_whole_ban_state[self.group_id] == False
                print('解除全体禁言',XM_Task.group_whole_ban_state)'''

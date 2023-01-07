# 导入需要的模块
import _thread
import time

# 导入框架模块
from core.keiyume import *
from .config import lock

from . import config, detection, database, reply, task, tools
from . import cmd

# 插件名称
name = '溪梦群管助手'
# 插件作者
author = '稽术宅'
# 插件版本
version = '2.1.0'
# 插件说明
description = '''溪梦群聊管理助手

  【特别致谢】
  句库补充：
  QQ：15140**011(汐酱)  ChatGPT'''
# 兼容性标识（兼容的溪梦框架版本）
compatible = ['2.0.0-beta.3-beta']

config.load_conf()  # 加载所有配置文件


@plugin.reg(location='event', priority=1024)
def keiyume_helper(self: Event):
    # 消息处理 #
    # 如果事件为需要管理的群的消息
    if self.is_group_msg(group_id=config.config['group']['group_id']):
        config.db.write_msg(self.data)  # 记录消息
        # 默认消息不含违禁词，无触发关键词，无关键词类型，无触发的检测引擎
        # 如果启用了违禁词检测
        ban_result = None
        if int(config.config['detection']['ban']):
            # 检测违禁词
            ban_result = detection.base(self.msg, config.rule['ban'])
        # 如果是广告或违禁词，且启用了忽略词检测
        ignore_result = None
        if int(config.config['detection']['ignore']) and ban_result:
            # 检测忽略词
            ignore_result = detection.base(self.message, config.rule['ignore'])
        # logger.info(
        #     f"【检测结果】\n原文：{self.msg}\n群聊：{self.group_id} 用户：{self.user_id} 违禁词：{ban_result}"
        #     f" 忽略词：{ignore_result}")
        # 消息结算
        if self.is_sub_type(sub_type='normal'):  # 如果是常规消息
            role = 0
            if self.is_admin():
                role = 1
            elif self.is_owner():
                role = 2
            # 只有对方发言内含有违禁词，且不包含忽略词，机器人身份高于说话人员时，才执行操作
            if ban_result and not ignore_result and role < tools.get_role(self.group_id, self.self_user_id):
                # 如果启用了撤回消息
                if config.config['punish']['del_delay']:
                    with lock:
                        task.del_message_id[self.message_id] = \
                            scheduler.add_job(func=task.timed_del_msg,
                                              trigger='date',
                                              run_date=time.strftime('%Y-%m-%d %H:%M:%S',
                                                                     time.localtime(time.time() + int(
                                                                         config.config['punish']['del_delay']))),
                                              kwargs={'message_id': self.message_id},
                                              id=f"keiyume_helper_del_msg_{self.message_id}")

                # 如果启用了违禁词提醒
                if int(config.config['reply']['ban']):
                    reply_msg = f"[CQ:at,qq={self.user_id}] {tools.random_from_list(config.reply['ban'])}"
                    api.send_group_msg(self.group_id, reply_msg.replace(r'\n', '\n'))

                # 惩罚次数记录以及禁言踢出
                punish = '无'  # 惩罚方式默认为无
                # print(task.punish_record[(self.group_id, self.user_id)])
                # 如果在处罚记录中已有记录
                if task.punish_record.get((self.group_id, self.user_id)):
                    task.punish_record[(self.group_id, self.user_id)]['num'] += 1  # 添加惩罚次数记录
                    # 如果有有效地踢出次数且犯错次数达到了移出群聊标准
                    if config.config['punish']['kick_num'] \
                            and task.punish_record[(self.group_id, self.user_id)]['num'] >= \
                            int(config.config['punish']['kick_num']):
                        punish = '移出群聊'  # 惩罚方式设置
                        # 计划任务添加踢出
                        api.set_group_kick(self.group_id, self.user_id)
                    # 否则如果有有效的初次禁言触发禁言次数且犯错次数达到了禁言标准
                    elif config.config['punish']['ban_num'] and\
                            task.punish_record.get((self.group_id, self.user_id)) and\
                            task.punish_record[(self.group_id, self.user_id)]['num'] >= int(
                                config.config['punish']['ban_num']):
                        # 如果禁言次数超过了预设的最大禁言次数
                        if len(config.config['punish']['ban_time']) - 1 <= \
                                task.punish_record[(self.group_id, self.user_id)]['ban_num']:
                            # 惩罚方式设置
                            punish = f"禁言{config.config['punish']['ban_time'][-1]}分钟"
                            # 根据禁言设置规则中最后的时间禁言
                            api.set_group_ban(self.group_id, self.user_id, 60 * config.config['punish']['ban_time'][-1])
                        else:
                            # 惩罚方式设置
                            punish = f"""禁言{config.config['punish']['ban_time']
                            [task.punish_record[(self.group_id, self.user_id)]['ban_num']]}分钟"""
                            # 根据禁言设置规则禁言
                            api.set_group_ban(self.group_id, self.user_id,
                                              60 * config.config['punish']['ban_time'][
                                                  task.punish_record[(self.group_id, self.user_id)]['ban_num']])
                            # 记录已禁言次数
                            task.punish_record[(self.group_id, self.user_id)]['ban_num'] += 1

                else:  # 如果没有记录
                    task.punish_record[(self.group_id, self.user_id)] = {'num': 1, 'ban_num': 0}  # 添加记录
                    # 如果有踢出惩罚触发数为 1
                    if config.config['punish']['kick_num'] == '1':
                        punish = '移出群聊'  # 惩罚方式设置
                        api.set_group_kick(self.group_id, self.user_id)  # 将其移出群聊
                    # 否则如果初次禁言触发数为 1
                    elif config.config['punish']['ban_num'] == '1':
                        # 惩罚方式设置
                        punish = f"禁言{config.config['punish']['ban_time'][0]}分钟"
                        api.set_group_ban(self.group_id, self.user_id, 60 * config.config[
                            'punish']['ban_time'][0])  # 根据设置规则禁言
                        # 记录已禁言次数
                        task.punish_record[(self.group_id, self.user_id)]['ban_num'] = 1
                # 如果启用了发送消息报告
                if config.config['group']['report_user_id']:
                    _thread.start_new_thread(task.send_report, (), {
                        'user_id': config.config['group']['report_user_id'],
                        'message': f"""【消息报告】
群聊：{self.group_id}
用户：{self.user_id}
次数：{task.punish_record[(self.group_id, self.user_id)]['num']}
时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}
匹配：{ban_result[0]}
惩罚：{punish}
关键词：{ban_result[1]}
消息内容：
{self.message[:300]}
（只显示前300字）"""})
                return True  # 中断后续运行的插件
            else:
                # 问答/随机回复
                reply.reply(self)

    # 如果事件为需要管理的群有成员加群
    elif self.is_group_notice(group_id=config.config['group']['group_id'],
                              notice_type='group_increase'):
        # 如果启用了入群欢迎
        if int(config.config['reply']['welcome']):
            send_msg = f"[CQ:at,qq={self.user_id}] {tools.random_from_list(config.reply['welcome'])}"
            api.send_group_msg(self.group_id, send_msg)

    # 需要撤回的消息若被提前撤回则删除计划任务
    elif self.is_group_notice(notice_type='group_recall'):
        with lock:
            config.db.write_del_msg(self.message_id)  # 将对应的消息标记为已撤回
            if task.del_message_id.get(self.message_id):
                scheduler.remove_job(f"keiyume_helper_del_msg_{self.message_id}")
                logger.info(
                    f'【信息】消息ID：{self.message_id} 已在撤回计划任务前被撤回，已删除本次撤回任务！\n')
                del task.del_message_id[self.message_id]

    # 如果事件为需要管理的群的请求
    elif self.is_group_request(group_id=config.config['group']['group_id']):
        # 如果为入群申请
        if self.is_sub_type(sub_type='add') or self.is_sub_type(sub_type='invite'):
            logger.info(
                f"【信息】群聊 {self.group_id} 中 {self.user_id} 申请加群，验证消息：{self.data['comment']}")
            if int(config.config['manage']['approval']):  # 如果启用了加群自动审批
                # 对申请进行处理
                if ('问题：' in self.data['comment']) and ('\n答案：' in self.data['comment']):
                    comment = self.data['comment'].split('\n答案：')[-1]
                # 忽略邀请加群
                elif ('来自：' in self.data['comment']) and ('的邀请' in self.data['comment']):
                    comment = ''
                else:
                    comment = ''
                # 匹配关键词，通过符合要求的请求
                for approval in config.rule['approval']:
                    if approval in comment:
                        api.set_group_add_request(flag=self.data['flag'],
                                                  sub_type=self.data['sub_type'],
                                                  approve=True,
                                                  group_id=self.group_id,
                                                  user_id=self.user_id)
                        break

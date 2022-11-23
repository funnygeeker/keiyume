from .xm_task import *
from .xm_tools import *


class XM_Reply():
    def Reply(self):
        '所有回复'
        if not XM_Reply.Self_Help_QA(self=self):
            XM_Reply.Random_Reply(self=self)

    def Self_Help_QA(self):
        '自助问答'
        if int(XM_Config.all_config['group']['group_reply']['qa_reply']):
            if int(XM_Config.all_config['group']['group_reply']['qa_reply_at']):
                on_at = self.on_at_me()
            else:
                on_at = 1
            if on_at:
                for file_name in XM_Config.all_send['self_help_qa']:
                    for line in XM_Config.all_send['self_help_qa'][file_name]:
                        if line[0] in self.message:
                            if len(line)<2:
                                logger.warn(f'【溪梦助手-警告】自助问答功能的配置文件存在：缺失答案的问题，请补充答案！\n')
                                return False
                            the_line=line.copy()
                            del the_line[0]
                            scheduler.add_job(func=Api.send_group_msg, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                                time.time()+2)), kwargs={'group_id': self.group_id, 'message': XM_Tools.Random_List_Value(the_list=the_line).replace(r'\n','\n')})
                            return True
        return False

    def Random_Reply(self):
        '随机回复'
        if self.on_at_me() and int(XM_Config.all_config['group']['group_reply']['random_reply']):
            tips_msg = f"{XM_Tools.Random_List_Value_In_Dict(XM_Config.all_send['random_reply'])}"
            scheduler.add_job(func=Api.send_group_msg, trigger='date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                time.time()+2)), kwargs={'group_id': self.group_id, 'message': tips_msg.replace(r'\n','\n')})

from .xm_config import *
import re
class XM_Detection():
    def Base_Detection(self, files: dict, detection_type: str, msg: str):
        '''消息检测
        files：含以文件夹名为键，文件字典为值的字典
        detection_type：需要检测的类型，用于修改self.message_status
        msg：传入的消息
        detection_plus：是否启用匹配增强
        '''
        # start_time=time.time()
        if detection_type == 'ads':
            key_word_type = '广告词'
        elif detection_type == 'bad':
            key_word_type = '违禁词'
        elif detection_type == 'ignore':
            key_word_type = '忽略词'
        msg = msg.lower()
        for file in files:  # 遍历字典中各文件（字典）的键
            for word in files[file]:  # 遍历各文件（列表）的值
                if word in msg:
                    self.msg_status['engine'] = '普通匹配'
                    self.msg_status['key_word'] = word
                    self.msg_status['key_word_type'] = key_word_type
                    self.msg_status[detection_type] = 1
                    # logger.debug(f'【用时】{time.time()-start_time}')
                    return True
        # 如果使用了匹配增强
        if int(XM_Config.all_config['group']['group_detection']['detection_plus']):
            # 使用正则表达式去除中英文外的字符
            msg = re.compile(
                '[^A-Z^a-z^\u4e00-\u9fa5]').sub('', self.message)
            for file in files:  # 遍历字典中各文件（字典）的键
                for word in files[file]:  # 遍历各文件（列表）的值
                    if word in msg:
                        self.msg_status['engine'] = '正则匹配'
                        self.msg_status['key_word'] = word
                        self.msg_status['key_word_type'] = key_word_type
                        self.msg_status[detection_type] = 1
                        # logger.debug(f'【用时】{time.time()-start_time}')
                        return True
        # 不是违规词也不是广告
        # logger.debug(f'【用时】{time.time()-start_time}')
        return False

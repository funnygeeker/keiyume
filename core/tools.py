import sys
import time
import json
from .log_mgr import *
class Tools():
    def To_Json(data:dict):
        return json.dumps(data, ensure_ascii=False, indent=4)

    def Match_List(list: list, text: str) -> bool:
        '''逐一匹配列表中的值是否包含在字符串中 返回:bool'''
        for i in list:  # 逐一匹配列表
            if str(i) in str(text):  # 如果文本在列表中
                return True
        else:
            return False
    
    def Data_To_Dict(data:str):
        '''【将str数据转换为dict形式并记录日志】
        返回:dict/None'''
        logger.debug(data) # 日志记录原始结果
        try:
            return json.loads(data)
        except:
            logger.warning(Log_Mgr.Get_Error())
            return None
    
    def Format_Conversion(text,mode:str='int',key=' ') -> list:
        '''【格式转换】将字符串转换每隔一个key拆分为列表
        mode表示返回列表中值的类型：str/int
        '1 2 3 4' => [1,2,3,4]
        返回：list'''
        if text == '':
            return []
        text = str(text).strip(key).split(key) # 先转为str形式以防配置为单数值时为int形式导致报错，除去两端的空格后进行分隔
        if mode == 'int':
            return [int(i) for i in text] # 将列表中的值转换回数字
        return text

    def Progress_Bar(text:str='',sleep:float=1) -> None:
        '''【进度条】'''
        for i in range(1, 51):
            print("\r", end="")
            print(f"{text} {i*2}%: ", "▋" * (i // 2), end="")
            sys.stdout.flush()
            time.sleep(sleep)



try:
    from configobj import ConfigObj
except ImportError:
    os.system('pip3 install configobj')
    from configobj import ConfigObj
from core.text_mgr import *
import threading
Lock = threading.Lock()


class Config_Mgr():
    '【存储设置变量及设置操作函数】'
    config = {}
    '溪梦框架配置'

    def Read_Config(file_path: str, encoding: str = '') -> dict:
        '''【读取设置文件】返回：dict（str）'''
        if encoding == '':  # 如果没有设置读取文件的编码
            encoding = Text_Mgt.Encodeing_Detect(file_path=file_path)
        return ConfigObj(file_path, encoding=encoding)

    def Load_Config():
        conf_folder_path = './config'
        file_names = os.listdir(conf_folder_path)  # 获取文件夹下的所有文件和文件夹名称
        for file_name in file_names:  # 遍历文件夹
            # 判断是否为需要读取的后缀
            if ((os.path.splitext(file_name)[1]).lower() == '.ini') and os.path.isfile(f'{conf_folder_path}/{file_name}'):
                # 读取所有.ini文件扩展名的文件，并以{文件名(str):内容(dict)}的形式载入字典
                Config_Mgr.config[os.path.splitext(file_name)[0]] = dict(
                    Config_Mgr.Read_Config(file_path=f'{conf_folder_path}/{file_name}'))
                # 判断是否为文件，小写处理文件扩展名，确定是否为需要读取的文件，并进行读取

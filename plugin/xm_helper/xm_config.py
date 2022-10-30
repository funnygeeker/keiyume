from core.connect_mgr import Connect_Mgr
from core.config_mgr import *
from core.tools import *
Lock=Connect_Mgr.lock

class XM_Config():
    all_config = {}
    '所有设置'
    all_send = {}
    '所有发送语句'
    all_words = {}
    '所有词库'
    message_id={}
    '''用于存储消息id：
    {group_id:[{message_id:user_id},...],...}
    '''
    groups_id_list=[]
    def Load_Config():
        '''【读取并加载配置文件到变量】'''
        # 读取ini配置文件
        conf_folder_path = './plugin/xm_helper/config/conf'
        files_name = os.listdir(conf_folder_path)  # 获取文件夹下的所有文件和文件夹名称
        with Lock:
            for file_name in files_name:  # 遍历文件夹
                # 判断是否为需要读取的后缀
                if ((os.path.splitext(file_name)[1]).lower() == '.ini') and os.path.isfile(f'{conf_folder_path}/{file_name}'):
                    # 读取所有.ini文件扩展名的文件，并以{文件名(str):内容(dict)}的形式载入字典
                    XM_Config.all_config[os.path.splitext(file_name)[0]] = dict(Config_Mgr.Read_Config(file_path=f'{conf_folder_path}/{file_name}'))
                    # 判断是否为文件，小写处理文件扩展名，确定是否为需要读取的文件，并进行读取
        # 读取txt配置文件(send文件夹)
        send_folder_path = './plugin/xm_helper/config/send'
        dirs_name = os.listdir(send_folder_path)  # 获取文件夹下的所有文件和文件夹名称
        with Lock:
            for dir_name in dirs_name:  # 遍历文件夹
                if os.path.isdir(f'{send_folder_path}/{dir_name}'): # 判断是否为目录
                    # 读取目录下所有txt文件
                    XM_Config.all_send[f'{dir_name}'] = Text_Mgt.List_Read_TXT_Under_Folder(folder_path=f'{send_folder_path}/{dir_name}',choose='#',chose_mode=0,return_mode='dict')
        # 读取txt配置文件(words文件夹)
        words_folder_path = './plugin/xm_helper/config/words'
        dirs_name = os.listdir(words_folder_path)  # 获取文件夹下的所有文件和文件夹名称
        with Lock:
            for dir_name in dirs_name:  # 遍历文件夹
                if os.path.isdir(f'{words_folder_path}/{dir_name}'): # 判断是否为目录
                    # 读取目录下所有txt文件
                    XM_Config.all_words[f'{dir_name}'] = Text_Mgt.List_Read_TXT_Under_Folder(folder_path=f'{words_folder_path}/{dir_name}',choose='#',chose_mode=0,return_mode='dict')

    def Init_Config():
        '始化所有配置文件，将需要转化的配置转化为合适的值'
        # 列表分割
        XM_Config.all_config['config']['groups_manage']['groups_manage']=Tools.Format_Conversion(text=XM_Config.all_config['config']['groups_manage']['groups_manage'],mode='int',key=' ')
        #XM_Config.all_config['config']['admin']['super_user_id']=Tools.Format_Conversion(text=XM_Config.all_config['config']['admin']['super_user_id'],mode='int',key=' ')
        #XM_Config.all_config['config']['admin']['admin_user_id']=Tools.Format_Conversion(text=XM_Config.all_config['config']['admin']['admin_user_id'],mode='int',key=' ')
        XM_Config.all_config['config']['admin']['groups_report_user_id']=Tools.Format_Conversion(text=XM_Config.all_config['config']['admin']['groups_report_user_id'],mode='int',key=' ')
        XM_Config.all_config['group']['group_punish']['ban_time']=Tools.Format_Conversion(text=XM_Config.all_config['group']['group_punish']['ban_time'],mode='int',key=' ')
        XM_Config.all_config['group']['group_function']['timed_whole_ban']=Tools.Format_Conversion(text=XM_Config.all_config['group']['group_function']['timed_whole_ban'],mode='str',key=' ')
        for file_name in XM_Config.all_send['self_help_qa']:
            for line in range(len(XM_Config.all_send['self_help_qa'][file_name])):
                XM_Config.all_send['self_help_qa'][file_name][line]=Tools.Format_Conversion(text=XM_Config.all_send['self_help_qa'][file_name][line],mode='str',key=' ')
        # 类型转换



XM_Config.Load_Config()  # 加载所有配置文件
XM_Config.Init_Config()  # 初始化所有配置文件
#logger.debug(f'{json.dumps(XM_Config.all_config,ensure_ascii=False,indent=4)}\n')
#logger.debug(f'{json.dumps(XM_Config.all_words,ensure_ascii=False,indent=4)}\n')
#logger.debug(f'{json.dumps(XM_Config.all_send,ensure_ascii=False,indent=4)}\n')

#TODO登陆掉线调度器问题
import random
class XM_Tools():
    def Splice_List(the_dict:dict):
        '拼接字典下各值的列表'
        the_list=[]
        for key in the_dict:
            the_list+=the_dict[key]
        return the_list

    def Random_List_Value(the_list:list) ->str:
        '随机返回列表中任意一项'
        return the_list[random.randint(0, len(the_list)-1)]
        
    def Random_List_Value_In_Dict(the_dict:dict) ->str:
        '拼接字典下各值的列表并随机返回列表中任意一项'
        return XM_Tools.Random_List_Value(the_list=XM_Tools.Splice_List(the_dict=the_dict))
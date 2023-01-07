import re
import traceback

from . import database
# 导入框架模块
from core.keiyume import *
from . import config
import time

# 插件名称
name = '溪梦积分助手'
# 插件作者
author = '稽术宅'
# 插件版本
version = '1.0.0'
# 插件说明
description = '用于管理群内的积分'
# 兼容性标识
compatible = ['2.0.0-beta.3']

plugin_path = database.plugin_path
points = database.DB(f"{plugin_path}/data.db")

points_menu = menu_text = f"""【溪梦积分助手】
「用户操作」
   签到   | 积分助手
支付积分 | 查询积分
积分记录 |
「管理操作」
设置积分 | 增加积分
减少积分 | 
框架：溪梦框架 {frame.get_version()}
版本：1.0"""


@plugin.reg(location='event', priority=2000)
def reg_points(self: Event):
    # 这是一个早期的临时方案，用于注册依赖，之后可能会开发专门地依赖管理器
    self.points = points


@plugin.reg(location='event', priority=2000, cmd='积分助手')
def sign_in(self: Event):
    if self.is_group_msg():
        api.send_group_msg(self.group_id, points_menu)


@plugin.reg(location='event', priority=2000, cmd='签到')
def sign_in(self: Event):
    if self.is_group_msg():
        if config.sign_in:  # 如果启用了签到功能
            if points.read_last_sign_in_date(self.user_id) < int(time.strftime("%Y%m%d", time.localtime(self.time))):
                if points.add(self.user_id, num=config.sign_in_add_points, event='每日签到', time=self.time):
                    points.write_last_sign_in_date(self.user_id,
                                                   int(time.strftime("%Y%m%d", time.localtime(self.time))))
                    api.send_group_msg(self.group_id,
                                       f"{cq.at(self.user_id)} 签到成功，积分增加 {config.sign_in_add_points}，"
                                       f"当前积分 {points.query(self.user_id)}")
                else:
                    api.send_group_msg(self.group_id, f"{cq.at(self.user_id)} 签到好像失败了呢...")
            else:
                api.send_group_msg(self.group_id, f"{cq.at(self.user_id)} 你今天已经签过到了，明天再来试试吧！")
        else:
            api.send_group_msg(self.group_id, f"签到功能没有被开启呢！")


@plugin.reg(location='event', priority=2000, cmd='查询积分')
def query_points(self: Event):
    if self.is_group_msg():
        if self.cmd_body:
            try:
                result = re.findall(r'\d+', self.cmd_body)[0]
                api.send_group_msg(self.group_id, f"{result} 当前拥有 {points.query(result)} 积分！")
            except IndexError:
                api.send_group_msg(self.group_id, "出错了，是不是命令格式不对呢？")
        else:
            api.send_group_msg(self.group_id, f"{cq.at(self.user_id)} 你当前拥有 {points.query(self.user_id)} 积分！")


@plugin.reg(location='event', priority=2000, cmd='积分记录')
def points_history(self: Event):
    if self.is_group_msg():
        result = points.read_history(self.user_id, 5)
        send = []
        if result:
            for _ in result:
                if _[0] == 'add':
                    type_ = '增加'
                elif _[0] == 'reduce':
                    type_ = '减少'
                elif _[0] == 'set':
                    type_ = '设置'
                else:
                    type_ = _[0]
                send.append(f"\n类型：{type_}\n数量：{_[1]}\n事件：{_[2]}\n"
                            f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(_[3]))}")
            send = '\n'.join(send)
            api.send_group_msg(self.group_id, f"{cq.at(self.user_id)} 最近的积分记录：{send}")
        else:
            api.send_group_msg(self.group_id, "哎呀，还没有积分记录呢！")


@plugin.reg(location='event', priority=2000, cmd='支付积分')
def pay_points(self: Event):
    if self.is_group_msg():
        try:
            result = re.findall(r'\D*(\d+)\D+(\d+)\D*', self.cmd_body)[0]
            if points.reduce(self.user_id, int(result[1]), f'主动支付给 {result[0]}', self.time):
                points.add(int(result[0]), int(result[1]), f'{result[0]} 支付的积分', self.time)
                api.send_group_msg(self.group_id, f"{cq.at(self.user_id)} 成功支付给 {result[0]} {result[1]} 积分！")
            else:
                api.send_group_msg(self.group_id, f"{cq.at(self.user_id)} 哎呀，你的积分好像不够呢！")
        except IndexError:
            api.send_group_msg(self.group_id, "出错了，是不是命令格式不对呢？")
            # print(traceback.format_exc())


@plugin.reg(location='event', priority=2000, cmd='设置积分 ')
def set_points(self: Event):
    if self.is_super_admin() or self.is_super_user():
        try:
            result = re.findall(r'\D*(\d+)\D+(\d+)\D*', self.cmd_body)[0]
            points.set(int(result[0]), int(result[1]), f'由管理员 {self.user_id} 设置', self.time)
            api.send_group_msg(self.group_id, f"成功设置 {result[0]} 的积分为 {result[1]}！")
        except IndexError:
            api.send_group_msg(self.group_id, "出错了，是不是命令格式不对呢？")


@plugin.reg(location='event', priority=2000, cmd='增加积分 ')
def add_points(self: Event):
    if self.is_super_admin() or self.is_super_user():
        try:
            result = re.findall(r'\D*(\d+)\D+(\d+)\D*', self.cmd_body)[0]
            if points.add(int(result[0]), int(result[1]), f'由管理员 {self.user_id} 增加', self.time):
                api.send_group_msg(self.group_id, f"成功增加 {result[0]}，{result[1]} 积分！")
            else:
                api.send_group_msg(self.group_id, f"增加积分失败了，怎么肥四？")
        except IndexError:
            api.send_group_msg(self.group_id, "出错了，是不是命令格式不对呢？")


@plugin.reg(location='event', priority=2000, cmd='减少积分 ')
def add_points(self: Event):
    if self.is_super_admin() or self.is_super_user():
        try:
            result = re.findall(r'\D*(\d+)\D+(\d+)\D*', self.cmd_body)[0]
            if points.reduce(int(result[0]), int(result[1]), f'由管理员 {self.user_id} 减少', self.time):
                api.send_group_msg(self.group_id, f"成功减少 {result[0]}，{result[1]} 积分！")
            else:
                api.send_group_msg(self.group_id, f"减少积分失败了，好像ta没有那么多积分呢！")
        except IndexError:
            api.send_group_msg(self.group_id, "出错了，是不是命令格式不对呢？")


logger.debug('【溪梦积分助手】正在添加定时数据库清理计划任务...')
scheduler.add_job(func=points.clear_history, trigger='interval',
                  minutes=180,
                  id='keiyume_points_clear_sql', kwargs={'num': 10000})

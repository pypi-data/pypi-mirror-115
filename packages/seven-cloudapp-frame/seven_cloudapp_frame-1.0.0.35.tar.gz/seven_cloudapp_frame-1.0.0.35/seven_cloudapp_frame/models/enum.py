# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2020-06-02 14:32:40
@LastEditTime: 2021-08-10 13:48:39
@LastEditors: HuangJianYi
:description: 枚举类
"""

from enum import Enum, unique

class OperationType(Enum):
    """
    :description: 用户操作日志类型
    """
    add = 1 #添加
    update = 2 #更新
    delete = 3 #删除
    review = 4 #还原

class TaskType(Enum):
    """
    docstring：任务类型 业务的自定义任务类型从1000起
    """
    # 新人有礼，格式：{"reward_value":0}
    new_user = 1
    # 每日签到，格式：{"reward_value":0}
    daily_sign = 2
    # 每周签到，格式：{"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}
    weekly_sign = 3
    # 邀请新用户，格式：{"reward_value":0,"user_limit":0}
    invite_new_user = 4
    # 关注店铺，格式：{"reward_value":0}
    favor_store = 5
    # 加入店铺会员，格式：{"reward_value":0}
    join_member = 6
    # 下单购买指定商品，格式：{"reward_value":0,"num_limit":0,"effective_date_start":'1900-01-01 00:00:00',"effective_date_end":'1900-01-01 00:00:00',"goods_ids":"","goods_list":[]}
    buy_goods = 7
    # 收藏商品，格式：{"reward_value":0,"num_limit":0,"goods_ids":"","goods_list":[]}
    collect_goods = 8
    # 浏览商品，格式：{"reward_value":0,"num_limit":0,"goods_ids":"","goods_list":[]}
    browse_goods = 9

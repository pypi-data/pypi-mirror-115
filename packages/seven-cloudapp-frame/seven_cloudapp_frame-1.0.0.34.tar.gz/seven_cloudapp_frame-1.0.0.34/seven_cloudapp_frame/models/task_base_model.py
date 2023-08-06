# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-10 10:41:13
@LastEditTime: 2021-08-10 10:48:53
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.act_base_model import *
from seven_cloudapp_frame.models.db_models.task.task_info_model import *


# class TaskBaseModel():
#     """
#     :description: 任务基类
#     """
#     def __init__(self, context):
#         self.context = context

#     def get_task_list(self,app_id,act_id,module_id,prize_name,ascription_type,is_del,page_size,page_index,is_cache=True):
#         """
#         :description: 获取活动奖品列表
#         :param app_id: 应用标识
#         :param act_id: 活动标识
#         :param module_id: 活动模块标识
#         :param prize_name: 奖品名称
#         :param ascription_type: 奖品归属类型（0-活动奖品1-任务奖品）
#         :param is_del：是否回收站1是0否
#         :param page_size: 条数
#         :param page_index: 页数
#         :param is_cache: 是否缓存
#         :return: 
#         :last_editors: HuangJianYi
#         """
#         order_by = "sort_index desc,id asc"
#         condition = "app_id=%s and act_id=%s"
#         params = [app_id,act_id]
#         if ascription_type !=-1:
#             condition += " and ascription_type=%s"
#             params.append(is_del)
#         if is_del !=-1:
#             condition += " and is_del=%s"
#             params.append(is_del)
#         if module_id !=-1:
#             condition += " and module_id=%s"
#             params.append(module_id)
#         if prize_name:
#             condition += " and prize_name=%s"
#             params.append(prize_name)
#         act_prize_model = ActPrizeModel(context=self.context)
#         if is_cache:
#             page_list = act_prize_model(field="*", page_index=page_index, page_size=page_size, where=condition, group_by="", order_by=order_by, params=params,dependency_key=f"act_prize_list:actid_{act_id}")
#         else:
#             page_list = act_prize_model.get_dict_page_list(field="*", page_index=page_index, page_size=page_size, where=condition, group_by="", order_by=order_by, params=params)    
#         return page_list, total
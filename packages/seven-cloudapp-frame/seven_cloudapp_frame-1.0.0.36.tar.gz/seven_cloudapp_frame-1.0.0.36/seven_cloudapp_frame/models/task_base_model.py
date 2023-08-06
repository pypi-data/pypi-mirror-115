# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-10 10:41:13
@LastEditTime: 2021-08-10 11:20:02
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.act_base_model import *
from seven_cloudapp_frame.models.db_models.task.task_info_model import *


class TaskBaseModel():
    """
    :description: 任务基类
    """
    def __init__(self, context):
        self.context = context

    def get_task_info_list(self,app_id,act_id,module_id,is_release,is_cache=True):
        """
        :description: 获取任务列表
        :param app_id: 应用标识
        :param act_id: 活动标识
        :param module_id: 活动模块标识
        :param is_release: 是否发布
        :param is_cache: 是否缓存
        :return: 
        :last_editors: HuangJianYi
        """
        order_by = "sort_index desc,id asc"
        condition = "app_id=%s and act_id=%s"
        params = [app_id,act_id]
        if is_release !=-1:
            condition += " and is_release=%s"
            params.append(is_release)
        if module_id !=-1:
            condition += " and module_id=%s"
            params.append(module_id)
        task_info_model = TaskInfoModel(context=self.context)
        if is_cache:
            dict_list = task_info_model.get_cache_dict_list(condition, group_by="", order_by=order_by, params=params,dependency_key=f"task_info_list:actid_{act_id}")
        else:
            dict_list = task_info_model.get_dict_list(condition, group_by="", order_by=order_by, params=params)
        for task_info in dict_list:
            task_info["task_config"] = SevenHelper.json_loads(task_info["task_config"]) if task_info["task_config"] else {}   
        return dict_list
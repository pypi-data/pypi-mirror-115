# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-10 10:05:38
@LastEditTime: 2021-08-10 10:36:42
@LastEditors: HuangJianYi
@Description: 
"""

from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.db_models.task.task_info_model import *

class TaskInfoListHandler(TaoBaseHandler):
    """
    :description: 获取任务列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 获取任务列表
        :param act_id：活动标识
        :param module_id：活动模块标识
        :return list
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_param("act_id", 0))
        module_id = int(self.get_param("module_id", 0))
        is_release = int(self.get_param("is_release", -1))
        condition = "act_id=%s"
        params = [act_id]
        if module_id >0:
            condition+=" and module_id=%s"
            params.append(module_id)
        if is_release !=-1:
            condition += " and is_release=%s"
            params.append(is_release)

        task_info_list_dict = TaskInfoModel(context=self).get_dict_list(condition, params=params,order_by="sort_index asc")
        for task_info in task_info_list_dict:
            task_info["task_config"] = SevenHelper.json_loads(task_info["task_config"]) if task_info["task_config"] else {}
        return self.reponse_json_success(task_info_list_dict)

class SaveTaskInfoHandler(TaoBaseHandler):
    """
    :description 保存任务
    """
    @filter_check_params("task_list,act_id,app_id")
    def post_async(self):
        """
        :description: 保存任务列表
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param task_list：任务列表
        :return reponse_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = int(self.get_param("act_id", 0))
        module_id = int(self.get_param("module_id", 0))
        task_list = self.get_param("task_list")
        try:
            task_list = SevenHelper.json_loads(task_list)
        except Exception as ex:
            task_list = []

        task_info_model = TaskInfoModel(context=self)
        for item in task_list:
            if not item.__contains__("task_type"):
                continue
            complete_type = int(item["complete_type"]) if item.__contains__("complete_type") else 1
            sort_index = int(item["sort_index"]) if item.__contains__("sort_index") else 0
            is_release = int(item["is_release"]) if item.__contains__("is_release") else 0
            task_config = SevenHelper.json_dumps(item["task_config"]) if item.__contains__("task_config") else {}
            if "id" in item.keys():
                task_info = task_info_model.get_entity_by_id(int(item["id"]))
                if task_info:
                    old_task_info = deepcopy(task_info)
                    task_info.task_type = int(item["task_type"])
                    task_info.modify_date = SevenHelper.get_now_datetime()
                    task_info.complete_type = complete_type
                    task_info.sort_index = sort_index
                    task_info.is_release = is_release
                    task_info.task_config = task_config
                    task_info_model.update_entity(task_info, "modify_date,complete_type,sort_index,is_release,task_config")
                    self.create_operation_log(OperationType.update.value, task_info.__str__(), "SaveTaskInfoHandler", SevenHelper.json_dumps(old_task_info.__dict__), SevenHelper.json_dumps(task_info.__dict__))
            else:
                task_info = TaskInfo()
                task_info.app_id = app_id
                task_info.act_id = act_id
                task_info.module_id = module_id
                task_info.task_type = int(item["task_type"])
                task_info.complete_type = complete_type
                task_info.task_config = task_config
                task_info.sort_index = sort_index
                task_info.is_release = is_release
                task_info.create_date = SevenHelper.get_now_datetime()
                task_info.modify_date = SevenHelper.get_now_datetime()
                task_info_model.add_entity(task_info)

                self.create_operation_log(OperationType.add.value, task_info.__str__(), "SaveTaskInfoHandler", None, SevenHelper.json_dumps(task_info))

        return self.reponse_json_success()
# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-02 14:03:12
@LastEditTime: 2021-08-02 14:08:05
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.app_base_model import *
from seven_cloudapp_frame.models.act_base_model import *



class ActInfoHandler(TaoBaseHandler):
    """
    :description: 获取活动信息
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 获取活动信息
        :param act_id：活动标识
        :return: 
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_param("act_id", 0))
        app_id = self.get_taobao_param().source_app_id
        app_base_model = AppBaseModel(context=self)
        act_base_model = ActBaseModel(context=self)
        app_info_dict = app_base_model.get_app_info_dict(app_id)
        if not app_info_dict:
            return self.response_json_error("error", "小程序不存在")
        act_info_dict = act_base_model.get_act_info_dict(act_id)
        if not act_info_dict:
            return self.response_json_error("error", "活动不存在")

        act_info_dict["seller_id"] = app_info_dict["seller_id"]
        act_info_dict["store_id"] = app_info_dict["store_id"]
        act_info_dict["store_name"] = app_info_dict["store_name"]
        act_info_dict["store_icon"] = app_info_dict["store_icon"]
        act_info_dict["app_icon"] = app_info_dict["app_icon"]
        return self.response_json_success(act_info_dict)
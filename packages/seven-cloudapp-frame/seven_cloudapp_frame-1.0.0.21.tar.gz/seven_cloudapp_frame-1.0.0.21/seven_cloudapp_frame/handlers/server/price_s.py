# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-02 14:25:02
@LastEditTime: 2021-08-04 12:02:43
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.price_base_model import *
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.db_models.price.price_gear_model import *


class SavePriceGearHandler(TaoBaseHandler):
    """
    :description: 保存价格档位信息
    """
    @filter_check_params("act_id,price")
    def get_async(self):
        """
        :description: 保存价格档位信息
        :param act_id：活动标识
        :param ip_id: ip标识
        :param ip_name：ip名称
        :param ip_pic：ip图片
        :param show_pic：展示图片
        :param sort_index：排序
        :param is_release：是否发布
        :return: reponse_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = int(self.get_param("act_id", 0))
        price_gear_id = int(self.get_param("price_gear_id", 0))
        relation_type = int(self.get_param("relation_type", 1))
        price = self.get_param("price")
        price_gear_name = self.get_param("price_gear_name")
        price_gear_pic = self.get_param("price_gear_pic")
        goods_id = self.get_param("goods_id")
        sku_id = self.get_param("sku_id")
        remark = self.get_param("remark")

        price_base_model = PriceBaseModel(context=self)
        invoke_result_data = price_base_model.save_price_gear(app_id, act_id, price_gear_id, relation_type, price_gear_name, price_gear_pic, price, goods_id, sku_id,remark)
        if invoke_result_data.success ==False:
            return self.reponse_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if invoke_result_data.data["is_add"] == True:
            # 记录日志
            self.create_operation_log(OperationType.add.value, invoke_result_data.data["new"].__str__(), "SavePriceGearHandler", None, self.json_dumps(invoke_result_data.data["new"]), self.get_taobao_param().open_id, self.get_taobao_param().user_nick)
        else:
            self.create_operation_log(OperationType.update.value, invoke_result_data.data["new"].__str__(), "SavePriceGearHandler", self.json_dumps(invoke_result_data.data["old"]), self.json_dumps(invoke_result_data.data["new"]), self.get_taobao_param().open_id, self.get_taobao_param().user_nick)

        self.reponse_json_success(invoke_result_data.data["new"].id)

class PriceGearListHandler(TaoBaseHandler):
    """
    :description: 获取价格档位列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 获取ip列表
        :param act_id：活动标识
        :param is_del：是否回收站1是0否
        :param page_index：页索引
        :param page_size：页大小
        :return: list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = int(self.get_param("act_id", 0))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))
        is_del = int(self.get_param("is_del", 0))

        self.reponse_json_success(PriceBaseModel(context=self).get_price_gear_list(app_id, act_id, page_size, page_index,is_del=is_del,is_cache=False))

class UpdatePriceGearStatusHandler(TaoBaseHandler):
    """
    :description: 删除或恢复价格档位
    """
    @filter_check_params("ip_id")
    def get_async(self):
        """
        :description: 删除或恢复价格档位
        :param act_id：活动标识
        :param ip_id: ip标识
        :return: reponse_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = int(self.get_param("act_id", 0))
        price_gear_id = int(self.get_param("price_gear_id", 0))
        is_del = int(self.get_param("is_del", 0))

        price_base_model = PriceBaseModel(context=self)
        invoke_result_data = price_base_model.update_price_gear_status(app_id, act_id, price_gear_id, is_del)
        if invoke_result_data.success == False:
            return self.reponse_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        self.reponse_json_success()

class CheckPriceGearHandler(TaoBaseHandler):
    """
    :description: 验证价格档位
    """
    @filter_check_params("act_id,goods_id")
    def get_async(self):
        """
        :description: 验证价格档位
        :param act_id：活动标识
        :param price_gear_id: ip标识
        :return: reponse_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = int(self.get_param("act_id", 0))
        price_gear_id = int(self.get_param("price_gear_id", 0))
        goods_id = self.get_param("goods_id")
        sku_id = self.get_param("sku_id")

        price_base_model = PriceBaseModel(context=self)
        invoke_result_data = price_base_model.check_price_gear(app_id, act_id, price_gear_id, goods_id, sku_id)
        if invoke_result_data.success == False:
            return self.reponse_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        self.reponse_json_success()

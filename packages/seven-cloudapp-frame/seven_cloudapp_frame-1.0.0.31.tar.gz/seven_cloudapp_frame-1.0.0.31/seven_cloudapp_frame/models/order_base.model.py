# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-09 09:24:43
@LastEditTime: 2021-08-09 10:07:54
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.seven_model import *

from seven_cloudapp_frame.models.db_models.prize.prize_order_model import *
from seven_cloudapp_frame.models.db_models.tao.tao_pay_order_model import *

class OrderBaseModel():
    """
    :description: 订单模块基类
    """
    def __init__(self, context):
        self.context = context

    def get_prize_order_list(self,app_id,act_id,user_id,user_open_id,nick_name,order_no,real_name,telephone,adress,order_status,create_date_start,create_date_end,page_size=20,page_index=0,order_by="id desc",field="*",is_cache=True):
        """
        :description: 用户奖品订单
        :param page_index：页索引
        :param page_size：页大小
        :param act_id：活动id
        :param order_no：订单号
        :param nick_name：用户昵称
        :param real_name：用户名字
        :param telephone：联系电话
        :param adress：收货地址
        :param order_status：订单状态（-1未付款-2付款中0未发货1已发货2不予发货3已退款4交易成功）
        :param create_date_start：订单创建时间开始
        :param create_date_end：订单创建时间结束
        :param page_size：页大小
        :param page_index：页索引
        :param order_by：排序
        :param field：查询字段
        :param is_cache：是否缓存
        :return: 列表
        :last_editors: HuangJingCan
        """
        condition = "app_id=%s and act_id=%s"
        params = [app_id,act_id]
        page_info = PageInfo(page_index, page_size, 0, [])
        
        if not app_id or not act_id:
            return page_info
        if order_no:
            condition += " AND order_no=%s"
            params.append(order_no)
        if nick_name:
            condition += " AND user_nick=%s"
            params.append(nick_name)
        if real_name:
            condition += " AND real_name=%s"
            params.append(real_name)
        if telephone:
            condition += " AND telephone=%s"
            params.append(telephone)
        if adress:
            adress = f"{adress}%"
            condition += " AND adress like %s"
            params.append(adress)
        if order_status !=-1:
            condition += " AND order_status=%s"
            params.append(order_status)
        if create_date_start:
            condition += " AND create_date>=%s"
            params.append(create_date_start)
        if create_date_end:
            condition += " AND create_date<=%s"
            params.append(create_date_end)

        page_list, total = PrizeOrderModel(context=self).get_dict_page_list(field, page_index, page_size, condition, "", order_by, params)
        page_info = PageInfo(page_index, page_size, total, page_list)
        return page_info

    def get_tao_pay_order_list(self,app_id,act_id,user_id,user_open_id,nick_name,pay_date_start,pay_date_end,page_size=20,page_index=0,field="*"):
        """
        :description: 获取淘宝支付订单列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户唯一标识
        :param user_open_id：open_id
        :param nick_name：用户昵称
        :param pay_date_start：订单支付时间开始
        :param pay_date_end：订单支付时间结束
        :param page_size：页大小
        :param page_index：页索引
        :param field：查询字段
        :return: PageInfo
        :last_editors: HuangJingCan
        """
        condition = "app_id=%s and act_id=%s"
        params = [app_id,act_id]
        page_info = PageInfo(page_index, page_size, 0, [])
        
        if not app_id or not act_id:
            return page_info
        if not user_id and not user_open_id:
            return page_info
        if user_id:
            condition += " AND user_id=%s"
            params.append(user_id)
        if user_open_id:
            condition += " AND open_id=%s"
            params.append(user_open_id)
        if nick_name:
            condition += " AND user_nick=%s"
            params.append(nick_name)
        if pay_date_start:
            condition += " AND pay_date>=%s"
            params.append(pay_date_start)
        if pay_date_end:
            condition += " AND pay_date<=%s"
            params.append(pay_date_end)
        page_list, total = TaoPayOrderModel(context=self).get_dict_page_list(field, page_index, page_size, condition, "", "pay_date desc", params)
        page_info = PageInfo(page_index, page_size, total, page_list)
        return page_info
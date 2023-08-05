# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-04 13:41:15
@LastEditTime: 2021-08-04 14:26:44
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.db_models.act.act_prize_model import *


class PrizeBaseModel():
    """
    :description: 奖品基类
    """
    def __init__(self, context):
        self.context = context
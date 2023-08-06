# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2020-06-02 14:32:40
@LastEditTime: 2021-08-03 18:16:25
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




# -*- coding:utf-8 -*-
from cdb import util

def increment_id(name, width, fill="0", skip=1, prefix=""):
    """
    :param prefix: 前缀
    :param name: 在cdb_counter表中的保存的计数器
    :param width: 固定长度
    :param fill: 以什么填充
    :param skip: 起始数字默认位0
    :return:
    """
    result = "{}{}".format(prefix, str(util.nextval(name)+skip).rjust(int(width), fill))
    return result

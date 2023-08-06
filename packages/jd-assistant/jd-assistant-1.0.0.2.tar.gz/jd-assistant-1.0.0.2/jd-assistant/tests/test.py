#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import OrderedDict
from jd_assistant import Assistant

if __name__ == '__main__':
    """
    重要提示：此处为示例代码之一，请移步下面的链接查看使用教程👇
    https://github.com/huaisha1224/jd-assistant/wiki/%E4%BA%AC%E4%B8%9C%E6%8A%A2%E8%B4%AD%E5%8A%A9%E6%89%8B
    """
    asst = Assistant()  # 初始化
    asst.login_by_QRcode()  # 扫码登陆
    asst.get_order_vercode()    #获取本地服务订单验证码及状态

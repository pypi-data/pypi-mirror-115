# JD-Assistant

[![version](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/download/releases/3.4.0/) 
[![status](https://img.shields.io/badge/status-stable-green.svg)](https://github.com/tychxn/jd-assistant)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![star, issue](https://img.shields.io/badge/star%2C%20issue-welcome-brightgreen.svg)](https://github.com/tychxn/jd-assistant)

## 主要功能

- 登陆京东商城（[www.jd.com](http://www.jd.com/)）
  - 手机扫码登录
  - 保存/加载登录cookies (可验证cookies是否过期)
- 商品查询操作
  - 提供完整的[`地址⇔ID`](./area_id/)对应关系
  - 根据商品ID和地址ID查询库存
  - 根据商品ID查询价格
- 购物车操作
  - 清空/添加购物车 (无货商品也可以加入购物车，预约商品无法加入)
  - 获取购物车商品详情
- 订单操作
  - 获取订单结算页面信息 (商品详情, 应付总额, 收货地址, 收货人等)
  - 提交订单（使用默认地址）
    - 直接提交
    - 有货提交
    - 定时提交
  - 查询订单 (可选择只显示未付款订单)
- 其他
  - 商品预约
  - 用户信息查询

## 运行环境

- [Python 3](https://www.python.org/)

## 第三方库

- [Requests](http://docs.python-requests.org/en/master/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [PyCryptodome](https://github.com/Legrandin/pycryptodome)

安装：

    pip install jd-assistant

或者

	pip install -r requirements.txt

## 初始化
	from jd_assistant import Assistant
	if __name__ == '__main__':
	asst = Assistant()  # 初始化
	asst.login_by_QRcode()  # 扫码登陆
	asst.get_order_vercode()    #获取本地服务订单验证码及状态	

## 直接提交订单示例
	from jd_assistant import Assistant

	if __name__ == '__main__':
	    asst = Assistant()      # 初始化
	    asst.login_by_QRcode()  # 扫码登陆
	    asst.clear_cart()       # 清空购物车（可选）
	    asst.add_item_to_cart(sku_ids='100001324422')  # 根据商品id添加购物车（可选）
	    asst.submit_order()     # 直接提交订单

## 定时提交订单示例（常用）
	from jd_assistant import Assistant

	if __name__ == '__main__':
	    asst = Assistant()      # 初始化
	    asst.login_by_QRcode()  # 扫码登陆
	    asst.clear_cart()       # 清空购物车（可选）
	    asst.add_item_to_cart(sku_ids='100001324422')  # 根据商品id添加购物车（可选）
	    asst.submit_order_by_time(buy_time='2020-02-16 01:17:59.500', retry=4, interval=5)  # 定时提交订单


## 有货提交订单示例
	from jd_assistant import Assistant

	if __name__ == '__main__':
	    sku_ids = '100001324422:1'  # 商品id
	    area = '1_72_4211'          # 区域id
	    asst = Assistant()          # 初始化
	    asst.login_by_QRcode()      # 扫码登陆
	    asst.buy_item_in_stock(sku_ids=sku_ids, area=area, wait_all=False, stock_interval=5)
		asst.buy_item_in_stock() 方法执行执行流程：

	

程序主入口在 `main.py`

👉 [使用教程请参看Wiki](https://github.com/huaisha1224/jd-assistant/wiki/%E4%BA%AC%E4%B8%9C%E6%8A%A2%E8%B4%AD%E5%8A%A9%E6%89%8B)


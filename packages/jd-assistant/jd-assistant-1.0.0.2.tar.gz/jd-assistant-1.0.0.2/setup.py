#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Learn more: https://github.com/huaisha1224/jd-assistant
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="jd-assistant",  # Replace with your own username
    version="1.0.0.2",
    author="sam.huang",
    author_email="sam.hxq@gmail.com",
    description="京东抢购助手：包含登录，查询商品库存/价格，添加/清空购物车，抢购商品，查询订单、查询本地生活服务订单验证码状态查询等",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huaisha1224/jd-assistant",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.4',
)

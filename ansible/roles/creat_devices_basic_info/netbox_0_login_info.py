# !/usr/bin/python3
# -*- coding=utf-8 -*-

# pip install "pynetbox"
import pynetbox


netbox_url = "http://192.168.219.41:8000"
netbox_token = "ad3d1d1a2104bef59c7e5b3e7af7475b0a9d7942"

# 产生NETBOX API连接实例
nb = pynetbox.api(url=netbox_url, token=netbox_token)

router_username = 'admin'
router_password = 'Cisc0123'

# 钉钉群通告机器人的webhook
qyt_webhook = ('https://oapi.dingtalk.com/robot/send?access_token=3957a042c05384519b4257656ff85e5055540ee4'
               'e0637b1272266ff894c90e83')



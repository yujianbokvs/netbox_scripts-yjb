# !/usr/bin/python3
# -*- coding=utf-8 -*-

# pip install "pynetbox"
import pynetbox


netbox_url = "http://192.168.219.42:8000"
netbox_token = "0123456789abcdef0123456789abcdef01234567"

# 产生NETBOX API连接实例
nb = pynetbox.api(url=netbox_url, token=netbox_token)

router_username = 'admin'
router_password = 'Cisc0123'

# 钉钉群通告机器人的webhook
qyt_webhook = ('https://oapi.dingtalk.com/robot/send?access_token=3957a042c05384519b4257656ff85e5055540ee4'
               'e0637b1272266ff894c90e83')


#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# pip3 install pynetbox
# pip3 install netmiko
from netbox_install.netbox_0_login_info import router_username, router_password
from netbox_install.tools.pynetbox_get_device_all import get_all_device
from netbox_install.tools.ssh_client_netmiko import netmiko_config_cred
from netbox_install.tools.pynetbox_get_render_config import get_device_render_config
from netbox_install.tools.get_ip_mask import get_ip_mask

# 协程相关
import asyncio
import os
import threading

# 协程任务循环
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


# 定义netmiko的携程函数
async def async_netmiko(task_id, ip, username, password, cmds_list):
    print(f'ID: {task_id} Started')
    print(os.getpid(), threading.current_thread().ident)
    result = await loop.run_in_executor(None, netmiko_config_cred, ip, username, password, cmds_list)
    print(f'ID: {task_id} Stopped')
    return result


# 循环任务计数号
task_no = 1

# 协程的任务清单
tasks = []

# 获取Region "China", Location "Beijing" 所有的路由器的信息
all_routers = get_all_device('china', 'beijing')

# 迭代每一台路由器的信息
for router in all_routers:
    # 每一个路由器最终配置命令的列表
    router_final_config_list = get_device_render_config(router.id).split('\n')

    # 提取路由器管理IP
    primary_ipv4 = router.primary_ip4
    router_ip = get_ip_mask(primary_ipv4).get('ip')

    # 设置登录用户名
    login_username = router_username
    # 设置登录密码
    login_password = router_password

    # 产生携程任务
    task = loop.create_task(async_netmiko(task_no, router_ip, login_username, login_password, router_final_config_list))
    # 把产生的携程任务放入任务列表
    tasks.append(task)
    # 任务号加1
    task_no += 1

# 执行携程任务列表
loop.run_until_complete(asyncio.wait(tasks))



#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# pip3 install dingtalkchatbot
# pip3 install 'pyats[full]'
from netbox_install.tools.pynetbox_get_device_all import get_all_device_info
from netbox_install.tools.pyats_verify_config_match import verify_interface_ip, verify_interface_enabled
from netbox_install.netbox_0_login_info import nb
from netbox_install.tools.pyats_get_info import interfaces_current, get_connect
from netbox_install.tools.dingding_notify import notify_team, fail_notification
from netbox_install.tools.dingding_message_template import message_interface_enabled_template
from netbox_install.tools.dingding_message_template import message_interface_ip_template
from netbox_install.tools.pyats_config import interface_enable_state_configure, interface_ip_configure
# platform 必须为iosxe
# netbox的主机名必须和设备的主机名保持一致

# 未解决Bug
# 1. Loopback不能no shutdown
# 2. 不能清空接口IP, 来匹配netbox未配置IP的接口

# 检查Region "China", Location "Beijing"的所有设备
for device in get_all_device_info('china', 'beijing'):
    # -------------------------逐个获取设备信息, 并且使用PyATS连接设备--------------------------------
    # 提取设备名称
    device_name = device['device_name']

    # 通知管理员已经开始对此设备进行检查
    notify_team(f"设备 {device_name} 正在被检查.")

    # 从netbox上获取设备详细信息, 新的SDK只需要传设备的名字即可
    nb_device_interfaces = nb.dcim.interfaces.filter(device=device_name)

    # pyats尝试连接设备, 如果失败尝试下一个设备
    try:
        pyats_connection = get_connect(device_name)
    except Exception:
        continue

    # --------------------------------检查接口状态--------------------------------------------
    # 通过pyats获取这个设备的所有接口信息
    pyats_interfaces = interfaces_current(pyats_connection)

    # 检查这个设备接口的激活状态
    interface_enabled_verify_result = verify_interface_enabled(nb_device_interfaces, pyats_interfaces)

    # 把接口激活状态检查失败的接口通知管理员
    fail_notification(interface_enabled_verify_result["FAIL"] + interface_enabled_verify_result["ERROR"],
                      message_interface_enabled_template)

    # --------------------------------检查接口IP--------------------------------------------
    # 再次获取设备的详细信息(使用后似乎就无效了, 需要重新获取), 新的SDK只需要传设备的名字即可
    nb_device_interfaces = nb.dcim.interfaces.filter(device=device_name)

    # 检查这个设备接口IP地址配置
    interface_ip_verify_result = verify_interface_ip(nb_device_interfaces, pyats_interfaces)

    # 把接口IP地址检查失败的接口通知管理员
    fail_notification(interface_ip_verify_result["FAIL"],
                      message_interface_ip_template)

    # --------------------------------修复接口状态--------------------------------------------
    # 如果存在接口激活状态检查失败的接口, 就修复接口激活状态
    if len(interface_enabled_verify_result["FAIL"]) > 0:
        interface_enable_state_configure(pyats_connection, interface_enabled_verify_result["FAIL"])
        notify_team(f"我正在更新{device_name}的接口激活状态.")

    # --------------------------------检查接口IP--------------------------------------------
    # 如果存在接口IP地址配置检查失败的接口, 就修复这个接口的IP地址配置
    if len(interface_ip_verify_result["FAIL"]) > 0:
        interface_ip_configure(pyats_connection, interface_ip_verify_result["FAIL"])
        notify_team(f"我正在更新{device_name}的接口IP地址配置.")

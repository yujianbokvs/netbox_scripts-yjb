# !/usr/bin/python3
# -*- coding=utf-8 -*-

from netbox_install.netbox_0_login_info import nb
from netbox_install.tools.get_ip_mask import get_ip_mask


# 获取所有设备信息
def get_all_device_info(region, location, rack=None):
    # 是否配置Rack, 调整过滤条件
    if rack:
        all_devices = nb.dcim.devices.filter(region=region, location=location, rack=rack)
    else:
        all_devices = nb.dcim.devices.filter(region=region, location=location)

    # 最终返回的设备列表
    devices_list = []

    # 迭代每一个设备, 构建device_dict字典, 并放入device_list列表
    for device in all_devices:
        device_dict = {}

        device_name = device.name

        # 写入设备名称
        device_dict['device_name'] = device_name

        # 写入设备平台
        device_dict['platform'] = str(device.platform)

        # 写入设备主IP(管理IP)
        primary_ipv4 = device.primary_ip4
        device_dict['mgmt_ip'] = get_ip_mask(primary_ipv4)

        # 写入设备的Config Context
        config_context = device.config_context
        device_dict['config_context'] = config_context

        # 设备接口列表
        interface_list = []

        # 找到设备的所有接口
        device_interfaces = nb.dcim.interfaces.filter(device=device_name)

        # 迭代设备的每一个接口, 产生interface_dict的字典, 放入interface_list的列表
        for interface in device_interfaces:
            # 接口名称
            interface_name = interface.name
            # 接口是否是管理接口
            mgmt_only = interface.mgmt_only
            # 接口是否激活 (no shutdown)
            interface_enabled = interface.enabled
            # 接口的IP地址
            ip_address = nb.ipam.ip_addresses.get(device=device_name, interface_id=interface.id)
            # 数据写入interface_dict字典
            interface_dict = {"interface_name": interface_name,
                              "mgmt_only": mgmt_only,
                              "interface_ip": get_ip_mask(ip_address),
                              "interface_enabled": interface_enabled
                              }
            # 每一个设备的interface_dict字典加入到interface_list列表
            interface_list.append(interface_dict)

        # 把接口信息的interface_list, 加入到device_dict
        device_dict['interface_list'] = interface_list
        # 把device_dict字典(设备的全部信息), 加入到devices_list列表
        devices_list.append(device_dict)

    return devices_list


# 获取特定名称的设备信息
def get_device_info(device_name):
    # 在netbox过滤特定设备的信息
    device = nb.dcim.devices.get(name=device_name)

    # 最终返回的包含这个设备所有信息的字典device_dict
    device_dict = {}

    # 写入设备名称
    device_name = device.name
    device_dict['device_name'] = device_name

    # 写入设备平台
    device_dict['platform'] = str(device.platform)

    # 写入设备主IP(管理IP)
    primary_ipv4 = device.primary_ip4
    device_dict['mgmt_ip'] = get_ip_mask(primary_ipv4)

    # 写入设备的Config Context
    config_context = device.config_context
    device_dict['config_context'] = config_context

    # 设备接口列表
    interface_list = []

    # 找到设备的所有接口
    device_interfaces = nb.dcim.interfaces.filter(device=device_name)

    # 迭代设备的每一个接口, 产生interface_dict的字典, 放入interface_list的列表
    for interface in device_interfaces:
        # 接口名称
        interface_name = interface.name
        # 接口是否是管理接口
        mgmt_only = interface.mgmt_only
        # 接口是否激活 (no shutdown)
        interface_enabled = interface.enabled
        # 接口的IP地址
        ip_address = nb.ipam.ip_addresses.get(device=device_name, interface_id=interface.id)
        # 数据写入interface_dict字典
        interface_dict = {"interface_name": interface_name,
                          "mgmt_only": mgmt_only,
                          "interface_ip": get_ip_mask(ip_address),
                          "interface_enabled": interface_enabled
                          }
        # 每一个设备的interface_dict字典加入到interface_list列表
        interface_list.append(interface_dict)

    # 把接口信息的interface_list, 加入到device_dict
    device_dict['interface_list'] = interface_list
    return device_dict


def get_all_device(region, location, rack=None):
    # 是否配置Rack, 调整过滤条件
    if rack:
        all_devices = nb.dcim.devices.filter(region=region, location=location, rack=rack)
    else:
        all_devices = nb.dcim.devices.filter(region=region, location=location)

    # 最终返回的设备列表
    devices_list = []

    # 迭代每一个设备, 构建device_dict字典, 并放入device_list列表
    for device in all_devices:
        devices_list.append(device)

    return devices_list


if __name__ == "__main__":
    from pprint import pprint
    # pprint(get_all_device_info('china', 'beijing'))
    pprint(get_device_info('C8Kv1'))
    # pprint(get_all_device('china', 'beijing'))

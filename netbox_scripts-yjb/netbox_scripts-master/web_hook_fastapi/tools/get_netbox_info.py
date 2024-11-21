from tools.basic_info import netbox_api_key, netbox_url
from tools.get_ip_mask import get_ip_mask
# from basic_info import netbox_api_key, netbox_url
# from get_ip_mask import get_ip_mask

import pynetbox


# 产生NETBOX API连接实例
nb = pynetbox.api(url=netbox_url, token=netbox_api_key)


def get_device_info(device_id):
    # 在netbox过滤特定设备的信息
    device = nb.dcim.devices.get(id=device_id)

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


def get_mgmt_ip(device_id):
    # 在netbox过滤特定设备的信息
    device = nb.dcim.devices.get(id=device_id)

    # netmiko_type
    netmiko_type = device.custom_fields.get('netmiko_type')

    # 写入设备主IP(管理IP)
    primary_ipv4 = device.primary_ip4
    mgmt_ip = get_ip_mask(primary_ipv4).get('ip')

    return {'netmiko_type': netmiko_type, 'mgmt_ip': mgmt_ip}


if __name__ == "__main__":
    # print(get_device_info(1))
    print(get_mgmt_ip(1))

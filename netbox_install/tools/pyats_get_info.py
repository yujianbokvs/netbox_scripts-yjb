from genie.testbed import load
from netbox_install.netbox_0_login_info import router_username, router_password
from netbox_install.tools.pynetbox_get_device_all import get_all_device_info
from pprint import pprint

device_details = {}

# 构建testbed数据结构
for device in get_all_device_info('china', 'beijing'):
    device_dict = {device["device_name"]: {
                                            "connections": {"cli": {"protocol": "ssh",
                                                                    "ssh_options": "-o StrictHostKeyChecking=no \
                                                                                    -o UserKnownHostsFile=/dev/null",
                                                                    'ip': device['mgmt_ip']['ip']}},

                                            "credentials": {"default": {"username": router_username,
                                                                        "password": router_password}},
                                            "os": device['platform'],
                                            "type": device['platform']
                                        }}
    device_details.update(device_dict)

testbed_device_details = {"devices": device_details}

# pprint(testbed_device_details)

# 加载testbed数据
testbed = load({"devices": device_details})


# 产生对设备的连接, 并且返回连接对象
def get_connect(device_name):
    device_connection = testbed.devices[device_name]

    device_connection.connect(learn_hostname=True,
                              log_stdout=False,
                              ssh_options='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null')
    return device_connection


# 获取设备平台详细信息
def platform_info(device_connection):
    return device_connection.learn("platform").to_dict()


# 提取设备当前接口信息
def interfaces_current(device_connection):
    interfaces = device_connection.learn("interface")
    return interfaces.info


# 提取设备当前OSPF信息
def ospf_current(device_connection):
    ospf = device_connection.learn("ospf")
    return ospf.to_dict()


if __name__ == "__main__":
    # platform 必须为iosxe
    # netbox的主机名必须和设备的主机名保持一致
    c8kv_1 = get_connect('C8Kv1')
    pprint(platform_info(c8kv_1))
    # pprint(interfaces_current(c8kv_1))
    # pprint(ospf_current(c8kv_1))

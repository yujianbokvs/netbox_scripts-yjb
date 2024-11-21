# pip install "pyats[full]"
from genie.libs.conf.interface import Interface
from genie.libs.conf.interface.ipv4addr import IPv4Address, IPv4Addr
from netbox_install.netbox_0_login_info import nb
from netbox_install.tools.pyats_get_info import interfaces_current
from netbox_install.tools.get_ip_mask import get_ip_mask


# 激活接口状态
# 参数1: device (pyats连接的设备)
# pyats_connection = get_connect(device_name)

# 参数2: netbox_interfaces (netbox查询的接口)
# nb_device_interfaces = nb.dcim.interfaces.filter(device=device_name)

def interface_enable_state_configure(device, netbox_interfaces):
    results = []
    # 迭代每一个netbox的接口
    for interface in netbox_interfaces:
        print(f"Setting Interface {interface.name} to enabled state {interface.enabled}")
        # 如果netbox的接口, 在pyats连接的设备也有
        if interface.name in interfaces_current(device).keys():
            # 创建配置接口对象, 准备配置
            config_interface = Interface(name=interface.name, device=device)
        # 如果netbox的接口, 在pyats连接的设备上没有, 只能略过配置下一个
        else:
            continue
        # 配置接口激活状态, 构建配置
        config_interface.enabled = interface.enabled
        output = config_interface.build_config()
        results.append(output)

    return results


# 激活接口IP
# 参数1: device (pyats连接的设备)
# pyats_connection = get_connect(device_name)

# 参数2: netbox_interfaces (netbox查询的接口)
# nb_device_interfaces = nb.dcim.interfaces.filter(device=device_name)

def interface_ip_configure(device, netbox_interfaces):
    results = []
    # 迭代每一个netbox的接口
    for interface in netbox_interfaces:
        # 如果netbox的接口, 在pyats连接的设备也有
        if interface.name in interfaces_current(device).keys():
            # 提取netbox上这个接口所配置IP地址
            try:
                nb_ip_address = nb.ipam.ip_addresses.get(interface_id=interface.id).address
            except Exception:
                nb_ip_address = None

            # 提取pyats在这个接口上学习到的IP地址
            try:
                pyats_ip_address = [ip for ip in interfaces_current(device)[interface.name]['ipv4'].keys()][0]
            except Exception:
                pyats_ip_address = None

            # 创建配置接口对象, 准备配置
            config_interface = Interface(name=interface.name, device=device)

            # 如果Netbox没有配置IP, 但是Pyats发现设备已经配置了IP, 那就清空IP地址配置
            if not nb_ip_address and pyats_ip_address:
                # 下面方法并不能清空IP地址, 有待后续研究
                ipv4_obj = IPv4Addr(device=device)
                ipv4_obj.ipv4 = pyats_ip_address.split('/')[0]
                ipv4_obj.prefix_length = pyats_ip_address.split('/')[1]
                config_interface.remove_ipv4addr(ipv4_obj)

            # 如果Netbox和Pyats都没有配置IP地址, 那就略过此接口, 开始下一个
            elif not nb_ip_address and not pyats_ip_address:
                continue

            # 其他情况, 例如:IP地址不匹配, 更正接口IP配置到Netbox上所配置的IP
            else:
                # 配置接口IP状态
                ip_mask = get_ip_mask(nb_ip_address)
                config_interface.ipv4 = ip_mask['ip']
                config_interface.ipv4.netmask = ip_mask['netmask']
            output = config_interface.build_config()
            results.append(output)

        # 如果netbox的接口, 在pyats连接的设备上没有, 只能略过配置下一个
        else:
            continue

    return results

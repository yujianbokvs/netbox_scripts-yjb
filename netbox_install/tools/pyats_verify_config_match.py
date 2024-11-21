# !/usr/bin/python3
# -*- coding=utf-8 -*-

from netbox_install.netbox_0_login_info import nb
from netbox_install.tools.pyats_get_info import interfaces_current, get_connect
from pprint import pprint


# 检查接口是否激活
def verify_interface_enabled(netbox_interfaces, pyats_interfaces):
    results = {
        "PASS": [],
        "FAIL": [],
        "ERROR": [],
    }

    # 迭代每一个netbox接口
    for interface in netbox_interfaces:
        # 如果netbox和pyats拥有相同的接口
        if interface.name in pyats_interfaces.keys():
            # 如果netbox的接口状态是激活的
            if interface.enabled:
                # pyats获取的接口配置状态是"enabled"(no shutdown) [测试1]
                if pyats_interfaces[interface.name]["enabled"]:
                    # pyats获取的接口操作状态是"UP"  [测试2]
                    # [测试1] and [测试2] 都通过, 表示接口"no shutdown", 并且状态也是"UP"的
                    if pyats_interfaces[interface.name]["oper_status"] == "up":
                        print(f"✅ {interface.name} 状态正确! 设备当前正处于 UP/UP 状态")
                        results["PASS"].append(interface)
                    # pyats获取的接口操作状态是"DOWN"  [测试2]
                    # [测试1] 通过 [测试2] 未通过, 表示接口"no shutdown", 但是状态是"DOWN"的
                    elif pyats_interfaces[interface.name]["oper_status"] == "down":
                        print(f"❌ {interface.name} 状态不正确! 设备当前正处于 UP/DOWN 状态")
                        results["ERROR"].append(interface)
                # pyats获取的接口配置状态没有"enabled"(shutdown) [测试1]
                elif not pyats_interfaces[interface.name]["enabled"]:
                    print(f"❌ {interface.name} 状态不正确! 设备当前正处于 DOWN/DOWN 状态")
                    results["FAIL"].append(interface)

            # 如果netbox的接口状态未被激活的
            elif not interface.enabled:
                # pyats获取的接口配置状态是"enabled"(no shutdown) [测试1]
                if pyats_interfaces[interface.name]["enabled"]:
                    # pyats获取的接口操作状态是"UP"  [测试2]
                    # [测试1] and [测试2] 都通过, 表示接口"no shutdown", 并且状态也是"UP"的
                    if pyats_interfaces[interface.name]["oper_status"] == "up":
                        # 打印错误因为netbox要求是shutdown, 但是pyats实际获取的状态是UP/UP
                        print(f"❌ {interface.name} 状态不正确! 设备当前正处于 UP/UP 状态")
                        results["FAIL"].append(interface)
                    else:
                        # 打印错误因为netbox要求是shutdown, 但是pyats实际获取的状态是UP/DOWN
                        print(f"❌ {interface.name} 状态不正确! 设备当前正处于 UP/DOWN 状态")
                        results["FAIL"].append(interface)

        else:
            print(f"❌ 设备上没有 {interface.name} 这个接口!")
            results["ERROR"].append(interface)

    return results


# 检查接口IP地址
def verify_interface_ip(netbox_interfaces, pyats_interfaces):
    results = {
        "PASS": [],
        "FAIL": [],
    }

    # 迭代每一个netbox接口
    for interface in netbox_interfaces:
        # 如果netbox和pyats拥有相同的接口
        if interface.name in pyats_interfaces.keys():
            # 提取netbox上这个接口所配置IP地址
            try:
                nb_ip_address = nb.ipam.ip_addresses.get(interface_id=interface.id).address
            except Exception:
                nb_ip_address = None

            # 提取pyats在这个接口上学习到的IP地址
            try:
                pyats_ip_address = [ip for ip in pyats_interfaces[interface.name]['ipv4'].keys()][0]
            except Exception:
                pyats_ip_address = None

            # 如果netbox配置了IP, 但是pyats没有发现这个接口的IP配置
            if nb_ip_address and not pyats_ip_address:
                print(f"❌ netbox配置了 {interface.name:<20} 这个接口的IP地址{nb_ip_address:<15}, \
                但是pyats发现接口没有配置IP地址")
                results["FAIL"].append(interface)
                continue

            # 如果netbox没有配置IP, 但是pyats发现这个接口的IP配置
            if not nb_ip_address and pyats_ip_address:
                print(f"❌ netbox没有配置 {interface.name:<20} 这个接口的IP地址, \
                但是pyats发现设备上配置了IP地址{pyats_ip_address:<15}")
                results["FAIL"].append(interface)
                continue

            # 如果netbox与pyats都没有IP配置
            if not nb_ip_address and not pyats_ip_address:
                print(f"✅ netbox与pyats均未配置 {interface.name:<20} 这个接口的IP地址")
                results["PASS"].append(interface)
                continue

            # 如果netbox与pyats配置的IP相同
            if nb_ip_address == pyats_ip_address:
                print(f"✅ {interface.name:<20} 在netbox配置的IP地址{nb_ip_address:<15}\
                与pyats采集到的实际配置的IP地址{pyats_ip_address}完全匹配!")
                results["PASS"].append(interface)
                continue

            # 如果netbox与pyats配置的IP不相同
            else:
                print(f"❌ {interface.name:<20} 在netbox配置的IP地址{nb_ip_address:<15}\
                与pyats采集到的实际配置的IP地址{pyats_ip_address}不匹配!")
                results["FAIL"].append(interface)
                continue

    return results


if __name__ == "__main__":
    verify_device = 'C8Kv1'
    nb_device_interfaces = nb.dcim.interfaces.filter(device=verify_device)
    pyats_connection = get_connect(verify_device)
    pyats_interfaces = interfaces_current(pyats_connection)
    print(verify_interface_enabled(nb_device_interfaces, pyats_interfaces))
    print(verify_interface_ip(nb_device_interfaces, pyats_interfaces))

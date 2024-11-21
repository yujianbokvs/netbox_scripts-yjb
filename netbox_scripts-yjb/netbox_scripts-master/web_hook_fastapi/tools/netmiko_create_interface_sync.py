from netmiko import Netmiko
import re
from tools.basic_info import username, password
from tools.get_netbox_info import get_mgmt_ip
from tools.get_netbox_info import nb
# from basic_info import username, password
# from get_netbox_info import get_mgmt_ip
# from get_netbox_info import nb


def netmiko_show_cred(host, username, password, cmd, device_type):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
    }
    try:
        net_connect = Netmiko(**device_info)
        result = net_connect.send_command(cmd,
                                          use_textfsm=True)
        net_connect.disconnect()
        return result

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


# 修订后的正则表达式，支持各种配置情况
pattern = re.compile(
    r"interface (?P<interface>\S+)\n"                           # 匹配 interface 行
    r"(?: description (?P<description>.+)\n)?"                  # 可选匹配 description 行
    r"(?: (?P<shutdown>shutdown)\n| undo shutdown\n)?"          # 匹配 shutdown 或 undo shutdown
    r"(?: port link-type (?P<link_type>\S+)\n)?"                # 可选匹配 port link-type
    r"(?:"
    r"(?: undo port trunk allow-pass vlan \d+\n)?"              # 可选匹配 undo port trunk allow-pass vlan
    r"(?: port trunk allow-pass vlan (?P<trunk_vlans>.+)\n)?"   # 可选匹配 port trunk allow-pass vlan
    r")?"
    r"(?: port default vlan (?P<access_vlan>\d+)\n)?"           # 可选匹配 port default vlan
    , re.MULTILINE
)


def get_if_info(show_result):
    # 去除命令提示符、空行和 'return' 等多余内容
    lines = show_result.strip().splitlines()
    interface_block = []
    in_interface_block = False
    for line in lines:
        if line.startswith('interface '):
            in_interface_block = True
        if in_interface_block:
            interface_block.append(line)
            if line.strip() == '#' or line.strip() == 'return':
                break
    interface_config = '\n'.join(interface_block)
    # 应用正则表达式进行匹配
    match = pattern.search(interface_config)
    if match:
        # 提取并处理接口信息
        interface_data = {
            "interface": match.group("interface"),
            "description": match.group("description") or "No description",
            "mode": None,  # 默认值
            "access_vlan": match.group("access_vlan"),
            "trunk_vlans": [],
            "shutdown": True if match.group('shutdown') == 'shutdown' else False,
        }
        link_type = match.group("link_type")
        trunk_vlans = match.group("trunk_vlans")

        # 确定模式
        if link_type == 'trunk':
            interface_data['mode'] = 'trunk'
            if trunk_vlans:
                # 处理 VLAN 列表
                vlan_list = trunk_vlans.strip()
                if vlan_list in ['all', '1 to 4094', '2 to 4094']:
                    interface_data['trunk_vlans'] = ['all']
                else:
                    interface_data['trunk_vlans'] = vlan_list.split()
            else:
                # 未指定时默认为 'all'
                interface_data['trunk_vlans'] = ['all']
        elif link_type == 'access':
            interface_data['mode'] = 'access'
        elif match.group("access_vlan"):
            interface_data['mode'] = 'access'
        else:
            interface_data['mode'] = None  # 未指定模式

        return interface_data
    else:
        return "未匹配到有效的接口配置！"


def sync_device_interface_info(device_id, interface_name):
    get_result = get_mgmt_ip(int(device_id))
    device_ip = get_result.get('mgmt_ip')
    netmiko_type = get_result.get('netmiko_type')
    realtime_result = (netmiko_show_cred(device_ip,
                                         username,
                                         password,
                                         f'display current-configuration interface {interface_name}',
                                         netmiko_type))
    # print(realtime_result)
    interface_mode_result = get_if_info(realtime_result)
    print(interface_mode_result)
    interface_obj = nb.dcim.interfaces.get(device_id=device_id, name=interface_name)
    print(interface_obj)
    interface_description = interface_mode_result.get('description')
    interface_enabled = not interface_mode_result.get('shutdown')
    if interface_mode_result.get('mode') == 'access':
        interface_obj.mode = 'access'
        vlan_id = int(interface_mode_result.get('access_vlan'))
        print(vlan_id)
        vlan_obj = nb.ipam.vlans.get(vid=vlan_id)
        print(vlan_obj)
        interface_obj.untagged_vlan = vlan_obj.id
        interface_obj.description = interface_description
        interface_obj.enabled = interface_enabled
        interface_obj.save()
    elif interface_mode_result.get('mode') == 'trunk':
        interface_obj.mode = 'tagged'
        interface_obj.description = interface_description
        interface_obj.enabled = interface_enabled
        interface_obj.save()


if __name__ == "__main__":
    # for i in range(1, 49):
    #     print(i)
    #     result = (netmiko_show_cred('10.1.1.254', 'qytang', 'Huawei@123',
    #                                 f'display current-configuration interface 10ge1/0/{i}',
    #                                 'huawei'))
    #     print(result)
    #     print(get_if_info(result))
    # result = (netmiko_show_cred('10.1.1.254', 'qytang', 'Huawei@123',
    #                             f'display current-configuration interface 10ge1/0/1',
    #                             'huawei'))
    # print(result)
    # print(get_if_info(result))
    sync_device_interface_info(1, '10GE1/0/6')

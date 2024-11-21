from tools.netmiko_3_config_1_basic import netmiko_config_cred
from tools.basic_info import username, password
from tools.get_netbox_info import get_mgmt_ip
# from netmiko_3_config_1_basic import netmiko_config_cred
# from basic_info import username, password
# from get_netbox_info import get_mgmt_ip


def change_interface_enabled(device_id, interface_name, enabled):
    cmds = [f'interface {interface_name}']
    if enabled:
        cmds.append('undo shutdown')
    else:
        cmds.append('shutdown')
    cmds.append('commit')
    print(cmds)

    get_result = get_mgmt_ip(int(device_id))

    config_results = netmiko_config_cred(get_result.get('mgmt_ip'),
                                         username,
                                         password,
                                         cmds,
                                         get_result.get('netmiko_type'),
                                         verbose=True)
    print(config_results)


if __name__ == '__main__':
    change_interface_enabled(1, "10GE1/0/6", 'true')

from netmiko import Netmiko


def netmiko_config_cred(host, username, password, cmds_list, device_type, verbose=False):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
                    'global_delay_factor': 2,  # 增加全局延迟因子
                    'session_log': 'session.log',  # 启用会话日志
    }
    try:
        net_connect = Netmiko(**device_info)

        if verbose:
            output = net_connect.send_config_set(cmds_list)
            return output
        else:
            net_connect.send_config_set(cmds_list)
        net_connect.disconnect()

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


if __name__ == '__main__':
    pass
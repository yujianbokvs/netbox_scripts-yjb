import socket
import struct


# 获取"10.10.1.1/24", 返回{'ip': '10.10.1.1', 'netmask': '255.255.255.0'}
def get_ip_mask(ip_and_prefix):
    try:
        ip_prefix_list = str(ip_and_prefix).split('/')
        ip = ip_prefix_list[0]
        prefix_len = ip_prefix_list[1]
        mask = (1 << 32) - (1 << 32 >> int(prefix_len))
        netmask = socket.inet_ntoa(struct.pack(">L", mask))
        return {'ip': ip, 'netmask': netmask}
    except Exception:
        return


if __name__ == "__main__":
    print(get_ip_mask('10.10.1.1/24'))

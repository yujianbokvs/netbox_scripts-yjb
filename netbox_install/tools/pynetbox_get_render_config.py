# !/usr/bin/python3
# -*- coding=utf-8 -*-

from netbox_install.netbox_0_login_info import netbox_token

import requests

headers = {
    "Authorization": f"Token {netbox_token}"
}


# 获取特定设备的render-config
def get_device_render_config(device_id):
    render_config_url = f"http://10.10.1.200:8000/api/dcim/devices/{device_id}/render-config/"
    response = requests.post(render_config_url, headers=headers)
    return response.json().get('content')


if __name__ == "__main__":
    print(get_device_render_config(1))

# !/usr/bin/python3
# -*- coding=utf-8 -*-

from netbox_install.netbox_0_login_info import netbox_token

import requests

url = "http://10.10.1.200:8000/api/extras/config-templates/"
headers = {
    "Authorization": f"Token {netbox_token}"
}


def get_template(template_name):
    response = requests.get(url, headers=headers)
    data = response.json()
    template_code = ""
    filtered_data = [item for item in data['results'] if item['name'] == template_name]
    if filtered_data:
        template_code = filtered_data[0].get('template_code')

    return template_code


if __name__ == "__main__":
    print(get_template('config_interfaces'))
    print(get_template('config_router_ospf'))

import pynetbox
import json

from netbox_0_login_info import nb
# count_result = nb.dcim.devices.count(site='KVS-site')  # 输出: 5827
# 不加任何参数则返回所有对象的数量。
total_count = nb.dcim.devices.count()  # 输出: 87382
from netbox_info_id  import rack_SH_02,rack_SH_03,rack_SH_04,rack_BG_02,rack_BG_03,rack_BG_04,rack_BG_01,rack_SH_01,rack_SH_05,rack_SH_06,rack_SH_07,rack_SH_08,rack_BG_05,rack_BG_06,rack_BG_07,rack_BG_08
from netbox_info_id import cisco_manufacturer_ID,site_BJ_ID,site_SH_ID,rack_SH_01,rack_BG_01,cisco_device_sw_role_id,cisco_device_nexus_role_id,cisco_device_cisco_c9300_48p_type_id,cisco_device_cisco_n9k_c9364c_type_ID,location_BJ_ID,location_SH_ID,cisco_plaforms_iosxe_id,cisco_plaforms_nxos_id
# export NETBOX_TOKEN="90d3b55069dcbc8523d4bea79c8c72e55cc0a5d3"
# export NETBOX_API="http://192.168.219.42:8000"

from netbox_info_id import  cisco_device_cisco_c9500_48y4c_type_id
# 准备要创建的设备列表
# devices = [
#     {
#         "name": "Nexus_9364-1",
#         "role": cisco_device_nexus_role_id,
#         "site": site_SH_ID,
#         "device_type": cisco_device_cisco_n9k_c9364c_type_ID,
#         "status": "active",
#         "rack": rack_SH_01,
#         "position": 40,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_SH_ID,
#         "platform": cisco_plaforms_nxos_id
#     },
#     {
#         "name": "Nexus_9364-2",
#         "role": cisco_device_nexus_role_id,
#         "site": site_SH_ID,
#         "device_type": cisco_device_cisco_n9k_c9364c_type_ID,
#         "status": "active",
#         "rack": rack_SH_01,
#         "position": 38,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_SH_ID,
#         "platform": cisco_plaforms_nxos_id
#     },
#     {
#         "name": "Nexus_9364-3",
#         "role": cisco_device_nexus_role_id,
#         "site": site_SH_ID,
#         "device_type": cisco_device_cisco_n9k_c9364c_type_ID,
#         "status": "active",
#         "rack": rack_SH_01,
#         "position": 36,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_SH_ID,
#         "platform": cisco_plaforms_nxos_id
#     },
#     {
#         "name": "Nexus_9364-4",
#         "role": cisco_device_nexus_role_id,
#         "site": site_SH_ID,
#         "device_type": cisco_device_cisco_n9k_c9364c_type_ID,
#         "status": "active",
#         "rack": rack_SH_01,
#         "position": 34,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_SH_ID,
#         "platform": cisco_plaforms_nxos_id
#     },
#     {
#         "name": "Nexus_9364-5",
#         "role": cisco_device_nexus_role_id,
#         "site": site_SH_ID,
#         "device_type": cisco_device_cisco_n9k_c9364c_type_ID,
#         "status": "active",
#         "rack": rack_SH_01,
#         "position": 32,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_SH_ID,
#         "platform": cisco_plaforms_nxos_id
#     },
#     {
#         "name": "Nexus_9364-6",
#         "role": cisco_device_nexus_role_id,
#         "site": site_SH_ID,
#         "device_type": cisco_device_cisco_n9k_c9364c_type_ID,
#         "status": "active",
#         "rack": rack_SH_01,
#         "position": 30,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_SH_ID,
#         "platform": cisco_plaforms_nxos_id
#     },
#     {
#         "name": "Nexus_9364-7",
#         "role": cisco_device_nexus_role_id,
#         "site": site_SH_ID,
#         "device_type": cisco_device_cisco_n9k_c9364c_type_ID,
#         "status": "active",
#         "rack": rack_SH_01,
#         "position": 28,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_SH_ID,
#         "platform": cisco_plaforms_nxos_id
#     },
#     {
#         "name": "Nexus_9364-8",
#         "role": cisco_device_nexus_role_id,
#         "site": site_SH_ID,
#         "device_type": cisco_device_cisco_n9k_c9364c_type_ID,
#         "status": "active",
#         "rack": rack_SH_01,
#         "position": 26,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_SH_ID,
#         "platform": cisco_plaforms_nxos_id
#     },
#     {
#         "name": "Nexus_9364-9",
#         "role": cisco_device_nexus_role_id,
#         "site": site_SH_ID,
#         "device_type": cisco_device_cisco_n9k_c9364c_type_ID,
#         "status": "active",
#         "rack": rack_SH_01,
#         "position": 24,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_SH_ID,
#         "platform": cisco_plaforms_nxos_id
#     },
#     {
#         "name": "Catalyst_9300-48P-1",
#         "role": cisco_device_sw_role_id,
#         "site": site_BJ_ID,
#         "device_type": cisco_device_cisco_c9300_48p_type_id,
#         "status": "active",
#         "rack": rack_BG_01,
#         "position": 40,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_BJ_ID,
#         "platform": cisco_plaforms_iosxe_id
#     },
#     {
#         "name": "Catalyst_9300-48P-2",
#         "role": cisco_device_sw_role_id,
#         "site": site_BJ_ID,
#         "device_type": cisco_device_cisco_c9300_48p_type_id,
#         "status": "active",
#         "rack": rack_BG_01,
#         "position": 38,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_BJ_ID,
#         "platform": cisco_plaforms_iosxe_id
#     },
#     {
#         "name": "Catalyst_9300-48P-3",
#         "role": cisco_device_sw_role_id,
#         "site": site_BJ_ID,
#         "device_type": cisco_device_cisco_c9300_48p_type_id,
#         "status": "active",
#         "rack": rack_BG_01,
#         "position": 36,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_BJ_ID,
#         "platform": cisco_plaforms_iosxe_id
#     },
#     {
#         "name": "Catalyst_9300-48P-4",
#         "role": cisco_device_sw_role_id,
#         "site": site_BJ_ID,
#         "device_type": cisco_device_cisco_c9300_48p_type_id,
#         "status": "active",
#         "rack": rack_BG_01,
#         "position": 34,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_BJ_ID,
#         "platform": cisco_plaforms_iosxe_id
#     },
#     {
#         "name": "Catalyst_9300-48P-5",
#         "role": cisco_device_sw_role_id,
#         "site": site_BJ_ID,
#         "device_type": cisco_device_cisco_c9300_48p_type_id,
#         "status": "active",
#         "rack": rack_BG_01,
#         "position": 32,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_BJ_ID,
#         "platform": cisco_plaforms_iosxe_id
#     },
#     {
#         "name": "Catalyst_9300-48P-6",
#         "role": cisco_device_sw_role_id,
#         "site": site_BJ_ID,
#         "device_type": cisco_device_cisco_c9300_48p_type_id,
#         "status": "active",
#         "rack": rack_BG_01,
#         "position": 30,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_BJ_ID,
#         "platform": cisco_plaforms_iosxe_id
#     },
#     {
#         "name": "Catalyst_9300-48P-7",
#         "role": cisco_device_sw_role_id,
#         "site": site_BJ_ID,
#         "device_type": cisco_device_cisco_c9300_48p_type_id,
#         "status": "active",
#         "rack": rack_BG_01,
#         "position": 28,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_BJ_ID,
#         "platform": cisco_plaforms_iosxe_id
#     },
#     {
#         "name": "Catalyst_9300-48P-8",
#         "role": cisco_device_sw_role_id,
#         "site": site_BJ_ID,
#         "device_type": cisco_device_cisco_c9300_48p_type_id,
#         "status": "active",
#         "rack": rack_BG_01,
#         "position": 26,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_BJ_ID,
#         "platform": cisco_plaforms_iosxe_id
#     },
#     {
#         "name": "Catalyst_9300-48P-9",
#         "role": cisco_device_sw_role_id,
#         "site": site_BJ_ID,
#         "device_type": cisco_device_cisco_c9300_48p_type_id,
#         "status": "active",
#         "rack": rack_BG_01,
#         "position": 24,
#         "face": "front",
#         "manufacturer": cisco_manufacturer_ID,
#         "location": location_BJ_ID,
#         "platform": cisco_plaforms_iosxe_id
#     }
# ]
# 使用 pynetbox 创建多个设备
# created_devices = nb.dcim.devices.update(devices)

# 输出已创建设备的信息
# for device in created_devices:
#     print(f"Created device: {device.name}, ID: {device.id}")













# 上海站点的Nexus交换机
shanghai_devices = [
    {
        "name": f"Nexus_9364-{i+1 + (rack_number - 1) * 9}",
        "role": cisco_device_nexus_role_id,
        "site": site_SH_ID,
        "device_type": cisco_device_cisco_n9k_c9364c_type_ID,
        "status": "active",
        "rack": [rack_SH_01, rack_SH_02, rack_SH_03, rack_SH_04,rack_SH_05,rack_SH_06,rack_SH_07,rack_SH_08][rack_number - 1],
        "position": 36 - i * 3,
        "face": "front",
        "manufacturer": cisco_manufacturer_ID,
        "location": location_SH_ID,
        "platform": cisco_plaforms_nxos_id
    } for rack_number in range(1, 9) for i in range(9)
]
shanghai_core_devices = [
    {
        "name": f"Catalyst_9500-SH-{i+1 + (rack_number - 1) }",
        "role": cisco_device_sw_role_id,
        "site": site_SH_ID,
        "device_type": cisco_device_cisco_c9500_48y4c_type_id,
        "status": "active",
        "rack": [rack_SH_01, rack_SH_02, rack_SH_03, rack_SH_04,rack_SH_05,rack_SH_06,rack_SH_07,rack_SH_08][rack_number - 1],
        "position": 40 - i * 2,
        "face": "front",
        "manufacturer": cisco_manufacturer_ID,
        "location": location_SH_ID,
        "platform": cisco_plaforms_iosxe_id
    } for rack_number in range(1, 3) for i in range(1)
]


# 北京站点的Catalyst交换机
beijing_devices = [
    {
        "name": f"Catalyst_9300-48P-{i+1 + (rack_number - 1) * 9}",
        "role": cisco_device_sw_role_id,
        "site": site_BJ_ID,
        "device_type": cisco_device_cisco_c9300_48p_type_id,
        "status": "active",
        "rack": [rack_BG_01, rack_BG_02, rack_BG_03,rack_BG_04,rack_BG_05,rack_BG_06,rack_BG_07,rack_BG_08][rack_number - 1],
        "position": 36 - i * 2,
        "face": "front",
        "manufacturer": cisco_manufacturer_ID,
        "location": location_BJ_ID,
        "platform": cisco_plaforms_iosxe_id
    } for rack_number in range(1, 9) for i in range(9)
]

beijing_core_devices = [
    {
        "name": f"Catalyst_9500-BJ-{i+1 + (rack_number - 1) }",
        "role": cisco_device_sw_role_id,
        "site": site_BJ_ID,
        "device_type": cisco_device_cisco_c9500_48y4c_type_id,
        "status": "active",
        "rack": [rack_BG_01, rack_BG_02, rack_BG_03,rack_BG_04,rack_BG_05,rack_BG_06,rack_BG_07,rack_BG_08][rack_number - 1],
        "position": 40 - i * 2,
        "face": "front",
        "manufacturer": cisco_manufacturer_ID,
        "location": location_BJ_ID,
        "platform": cisco_plaforms_iosxe_id
    } for rack_number in range(1, 3) for i in range(1)
]
# 使用 pynetbox 创建上海站点设备
created_shanghai_devices = nb.dcim.devices.create(shanghai_devices)
created_shanghai_core_devices=nb.dcim.devices.create(shanghai_core_devices)
# 输出已创建设备的信息（上海站点）
for device in created_shanghai_devices:
    print(f"Created Shanghai device: {device.name}, ID: {device.id}")

# 使用 pynetbox 创建北京站点设备
created_beijing_devices = nb.dcim.devices.create(beijing_devices)
created_beijing_core_devices= nb.dcim.devices.create(beijing_core_devices)
# 输出已创建设备的信息（北京站点）
for device in created_beijing_devices:
    print(f"Created Beijing device: {device.name}, ID: {device.id}")






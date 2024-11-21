import pynetbox
from netbox_0_login_info import nb

cisco_manufacturer_ID =nb.dcim.manufacturers.get(name='Cisco').id
print(cisco_manufacturer_ID)


cisco_device_cisco_n9k_c9364c_type_ID = nb.dcim.device_types.get(slug='cisco-n9k-c9364c').id
print(cisco_device_cisco_n9k_c9364c_type_ID)




cisco_device_cisco_c9500_48y4c_type_id=nb.dcim.device_types.get(slug='cisco-c9500-48y4c').id
print(cisco_device_cisco_c9500_48y4c_type_id)



cisco_device_cisco_c9300_48p_type_id=nb.dcim.device_types.get(slug='cisco-c9300-48p').id
print(cisco_device_cisco_c9300_48p_type_id)

cisco_device_nexus_role_id=nb.dcim.device_roles.get(name="KVS-nexus").id
print(cisco_device_nexus_role_id)


cisco_device_sw_role_id=nb.dcim.device_roles.get(name="KVS-sw").id
print(cisco_device_sw_role_id)



site_BJ_ID = nb.dcim.sites.get(name="KVS-BJ-site").id
print(site_BJ_ID)

site_SH_ID=nb.dcim.sites.get(name="KVS-SH-site").id
print(site_SH_ID)





# 北京站点机柜 ID
rack_BG_01 = nb.dcim.racks.get(name="BJ-RACK-01").id
print(rack_BG_01)

rack_BG_02 = nb.dcim.racks.get(name="BJ-RACK-02").id
print(rack_BG_02)

rack_BG_03 = nb.dcim.racks.get(name="BJ-RACK-03").id
print(rack_BG_03)

rack_BG_04 = nb.dcim.racks.get(name="BJ-RACK-04").id
print(rack_BG_04)

rack_BG_05 = nb.dcim.racks.get(name="BJ-RACK-05").id
print(rack_BG_05)

rack_BG_06 = nb.dcim.racks.get(name="BJ-RACK-06").id
print(rack_BG_06)

rack_BG_07 = nb.dcim.racks.get(name="BJ-RACK-07").id
print(rack_BG_07)

rack_BG_08 = nb.dcim.racks.get(name="BJ-RACK-08").id
print(rack_BG_08)

# 上海站点机柜 ID
rack_SH_01 = nb.dcim.racks.get(name="SH-RACK-01").id
print(rack_SH_01)

rack_SH_02 = nb.dcim.racks.get(name="SH-RACK-02").id
print(rack_SH_02)

rack_SH_03 = nb.dcim.racks.get(name="SH-RACK-03").id
print(rack_SH_03)

rack_SH_04 = nb.dcim.racks.get(name="SH-RACK-04").id
print(rack_SH_04)

rack_SH_05 = nb.dcim.racks.get(name="SH-RACK-05").id
print(rack_SH_05)

rack_SH_06 = nb.dcim.racks.get(name="SH-RACK-06").id
print(rack_SH_06)

rack_SH_07 = nb.dcim.racks.get(name="SH-RACK-07").id
print(rack_SH_07)

rack_SH_08 = nb.dcim.racks.get(name="SH-RACK-08").id
print(rack_SH_08)














location_SH_ID=nb.dcim.locations.get(name='ShangHai').id
print(location_SH_ID)

location_BJ_ID=nb.dcim.locations.get(name='Beijing').id
print(location_BJ_ID)

cisco_plaforms_nxos_id=nb.dcim.platforms.get(name='nxos').id
print(cisco_plaforms_nxos_id)

cisco_plaforms_iosxe_id=nb.dcim.platforms.get(name='iosxe').id
print(cisco_plaforms_iosxe_id)
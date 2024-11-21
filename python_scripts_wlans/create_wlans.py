import requests
import json
import os
from dotenv import load_dotenv

# Load the .env file so the API Token can be read by the script
load_dotenv()

# Set the 'token' variable to the value of 'api_token' from the .env file
# Rename file .env to .env and add your own API token
# Remember to add .env to your .gitignore file to avoid uploading the token to your Git repo
token = os.getenv('api_token')
print(token)

nb_host = os.getenv('nb_host')
print(nb_host)
# Set variables to match your own NetBox installation
nb_protocol = 'http' 

nb_port = '8000'
from netbox_0_login_info import  nb
# Build the URL for the API request
url = nb_protocol+'://'+nb_host+':'+nb_port+"/api/wireless/wireless-lans/"
wifi_name1="B_WIFI"
wifi_name2="G_WIFI"
wifi_group="Asia_Pacific_WLANs"
tenant_name="Consulting"


wifi_name1_vlan = nb.ipam.vlans.get(name=wifi_name1).id
print(wifi_name1_vlan)
wifi_name2_vlan = nb.ipam.vlans.get(name=wifi_name2).id
print(wifi_name2_vlan)



wireless_group=nb.wireless.wireless_lan_groups.get(name=wifi_group).id
print(wireless_group)


tenant_id=nb.tenancy.tenants.get(name=tenant_name).id
print(tenant_id)




# Set the payload and headers for the API request
payload = json.dumps([
  {
    "ssid": wifi_name1,
    "description": "Branch Office Wifi",
    "group" : wireless_group,
    "vlan": wifi_name1_vlan,
    "tenant": tenant_id,
    "auth_type": "wpa-enterprise",
    "auth_psk": "5up3r5ecr3tK3y",
    "auth_cipher": "aes"
  },
  {
    "ssid": "G_WIFI",
    "description": "Guest Wifi",
    "group" : wireless_group,
    "vlan": wifi_name2_vlan,
    "tenant": tenant_id,
    "auth_type": "wpa-enterprise",
    "auth_psk": "M3g45ecr3tK3y",
    "auth_cipher": "aes"
  }
  ])
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token '+ token
}

# Send the API request and display the result in pretty json format
response = requests.request("POST", url, headers=headers, data=payload)
pretty_json = json.loads(response.text)
print (json.dumps(pretty_json, indent=4))
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

# Set variables to match your own NetBox installation
nb_protocol = 'http' 
nb_host=os.getenv('nb_host')
print(nb_host)
nb_port = '8000'

# Build the URL for the API request
url = nb_protocol+'://'+nb_host+':'+nb_port+"/api/wireless/wireless-lan-groups/"

# Set the payload and headers for the API request
payload = json.dumps({
  "name": "Asia_Pacific_WLANs",
  "slug": "asia-pacific-wlans",
  "description": "Asia Pacific Wireless Networks"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token '+ token
}

# Send the API request and display the result in pretty json format
response = requests.request("POST", url, headers=headers, data=payload)
pretty_json = json.loads(response.text)
print (json.dumps(pretty_json, indent=4))
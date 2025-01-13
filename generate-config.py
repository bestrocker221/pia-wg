from piawg import piawg
from pick import pick
from getpass import getpass
from datetime import datetime

import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access environment variables
option = os.getenv("region")
PIA_user = os.getenv("PIA_user")  # Returns a string ("True")
PIA_pass = os.getenv("PIA_pass")

pia = piawg()

# Generate public and private key pair
pia.generate_keys()

# Select region
#title = 'Please choose a region: '
#options = sorted(list(pia.server_list.keys()))
#option, index = pick(options, title)
pia.set_region(option)
print("Selected '{}'".format(option))

# Get token
while True:
    username = PIA_user
    password = PIA_pass
    if pia.get_token(username, password):
        print("Login successful!")
        break
    else:
        print("Error logging in, please try again...")

# Add key
status, response = pia.addkey()
if status:
    print("Added key to server!")
else:
    print("Error adding key to server")
    print(response)

# Build config
timestamp = int(datetime.now().timestamp())
location = pia.region.replace(' ', '-')
config_file = 'PIA-{}-{}.conf'.format(location, timestamp)
print("Saving configuration file {}".format(config_file))
with open(config_file, 'w') as file:
    file.write('[Interface]\n')
    file.write('Address = {}\n'.format(pia.connection['peer_ip']))
    file.write('PrivateKey = {}\n'.format(pia.privatekey))
    file.write('DNS = {},{}\n\n'.format(pia.connection['dns_servers'][0], pia.connection['dns_servers'][1]))
    file.write('[Peer]\n')
    file.write('PublicKey = {}\n'.format(pia.connection['server_key']))
    file.write('Endpoint = {}:1337\n'.format(pia.connection['server_ip']))
    file.write('AllowedIPs = 0.0.0.0/0\n')
    file.write('PersistentKeepalive = 25\n')

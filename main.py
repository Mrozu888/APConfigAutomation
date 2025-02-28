from dotenv import dotenv_values
import os

from arp_scan import get_ip_by_mac
from ssh_client import SSHClient
import pandas as pd


secrets = dotenv_values(".env")
ssh_private_key_path = secrets['SSH-PRIVATE-KEY-ROOT']
ssh_private_key_password = secrets['SSH-PRIVATE-KEY-PASSWORD']

# SSH details
ssh_port = 22
ssh_username = 'super'
ssh_password = 'sp-admin'


VSZ_ADDRESS = "63.176.123.97"

ap_password = 'admin123'


subnet = "192.168.0.1"
netmask = "255.255.255.0"


# Load the Excel file
file_path = "template.xlsx"  # Update with your actual file path
df = pd.read_excel(file_path, engine="openpyxl")

# Convert DataFrame to a nested list
ap_list = df.values.tolist()

# Print the list
print(ap_list)

for ap in ap_list:
    try:
        # Create SSH client and execute commands
        ipaddr = get_ip_by_mac(ap[1])
        print(ssh_private_key_path)
        print(ssh_private_key_password)
        ssh = SSHClient(ipaddr, ssh_username, password=ssh_password, key_path=ssh_private_key_path, key_pass="zaq1@WSX")
        # ssh = SSHClient(ipaddr, ssh_username, password=ssh_password)


        # commands = [
        #     "super",
        #     "sp-admin",
        #     ap_password,
        #     ap_password,
        #     f"set device-name {ap[0]}",
        #     f"set scg enable",
        #     f"set scg ip {VSZ_ADDRESS}",
        #     f"set device-location {ap[3]}",
        #     f"set ipaddr wan {ap[2]} {netmask} {subnet}",
        #     "reboot"
        # ]


        # Execute commands
        # for command in commands:
        #     ssh.send(command)

        # waiting for an output after executing commands
        ssh.read_output(timeout=10)

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
    finally:
        # Close SSH connection
        if ssh:
            ssh.close()

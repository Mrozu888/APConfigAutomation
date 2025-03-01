import paramiko
import time
import pandas as pd
import json
from net_util import find_ip_by_mac

with open("config.json", "r") as file:
    config = json.load(file)

# SSH details
ssh_port = 22
ssh_username = "super"
ssh_password = "sp-admin"

VSZ_ADDRESS = config["VSZ_ADDRESS"]
ap_password = config["ap_password"]
file_path = config["file_path"]
subnet = config["ap_subnet_target"]
netmask = config["ap_netmask_target"]
ap_subnet_to_find = config["ap_subnet_to_find"]

# Load the Excel file
df = pd.read_excel(file_path, engine="openpyxl")
ap_list = df.values.tolist()


def ssh_to_ap_and_configure(ap):
    ssh_ip = find_ip_by_mac(ap[1], network=ap_subnet_to_find)
    print(f"🔍 Connecting to {ssh_ip}...")

    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to AP
        client.connect(ssh_ip, port=ssh_port, username=ssh_username, password=ssh_password, timeout=30)
        print("✅ Successfully connected!")

        # Start interactive shell
        shell = client.invoke_shell()
        time.sleep(1)  # Allow the shell to initialize

        # Clear initial output
        if shell.recv_ready():
            initial_output = shell.recv(1024).decode()
            print(f"📜 Initial Output: {initial_output}")

        # Commands to execute
        commands = [
            "super",
            "sp-admin",
            ap_password,
            ap_password,
            "super",
            ap_password,
            f"set device-name {ap[0]}",
            "set scg enable",
            f"set scg ip {VSZ_ADDRESS}",
            f"set ipaddr wan {ap[2]} {netmask} {subnet}",     # uncomment to change IP of AP
            "set autoprov enable"
            # "reboot"
        ]

        for command in commands:
            print(f"➡️ Executing: {command}")
            shell.send(command + "\n")
            time.sleep(1)  # Give time for the command to execute

            # Capture command output
            output = ""
            while shell.recv_ready():
                output += shell.recv(1024).decode()

            print(f"📜 Command Output: {output.strip()}")

        print("✅ Configuration complete")
        client.close()

    except paramiko.AuthenticationException:
        print("❌ Authentication failed, please check credentials.")
    except paramiko.SSHException as e:
        print(f"❌ SSH error: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


# Iterate over AP list and configure each
for ap in ap_list:
    ssh_to_ap_and_configure(ap)

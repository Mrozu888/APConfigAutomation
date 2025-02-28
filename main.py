from dotenv import dotenv_values
import os
from ssh_client import SSHClient

secrets = dotenv_values(".env")

# SSH details
ssh_hostname = '10.0.0.30'
ssh_port = 22
ssh_username = 'super'

ssh_private_key_path = secrets['SSH-PRIVATE-KEY-ROOT']
ssh_private_key_password = secrets['SSH-PRIVATE-KEY-PASSWORD']

# TFTP server details
tftp_server_ip = '192.168.0.123'  # Bind interface
tftp_server_port = 69  # Bind port

fw_name = "H510_200.7.10.202.141.bl7"

commands = ["super", "sp-admin", "fw set host 192.168.0.123", "fw set proto tftp", f"fw set port {tftp_server_port}",
            f"fw set control {fw_name}", "fw update", "reboot"]

# to open file
# with open("template.txt", "r") as file:
#     lines = file.readlines()
#     print(lines)

try:
    # Create SSH client and execute commands
    ssh = SSHClient(ssh_hostname, ssh_username, ssh_private_key_path, ssh_private_key_password)

    # Execute commands
    # for command in commands:
    #     ssh.send(command)
    #
    # # waiting for an output after executing commands
    # ssh.read_output(timeout=10)

except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")
finally:
    # Close SSH connection
    if ssh:
        ssh.close()

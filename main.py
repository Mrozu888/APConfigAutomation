import pexpect
import pandas as pd

# SSH details
ssh_port = 22
ssh_username = 'super'
ssh_password = 'sp-admin'


VSZ_ADDRESS = "63.176.123.97"

ap_password = 'G3n3va_123'


subnet = "192.168.0.1"
netmask = "255.255.255.0"


# Load the Excel file
file_path = "template.xlsx"  # Update with your actual file path
df = pd.read_excel(file_path, engine="openpyxl")

# Convert DataFrame to a nested list
ap_list = df.values.tolist()

# Print the list
print(ap_list)


def ssh_to_ap_and_configure(ap):
    try:
        # Start SSH connection
        # ssh_ip = get_ip_from_mac(ap[1])
        ssh_ip = "192.168.0.102"
        print(ssh_ip)
        ssh_command = f"ssh {ssh_username}@{ssh_ip}"
        child = pexpect.spawn(ssh_command, timeout=30)

        chpasswd = False
        while True:
            try:
                # Matching the exact SSH prompt patterns
                index = child.expect([
                    r"not known by any other names\.\r\nAre you sure you want to continue connecting \(yes/no/\[fingerprint\]\)\?",
                    r"Please login: ",
                    r"password :",
                    r"New password:",
                    r"Confirm password:",
                    r"rkscli:",  # rkscli prompt after login
                    pexpect.EOF,
                    pexpect.TIMEOUT
                ], timeout=10)

                full_output = child.before.decode().strip()  # Get full response
                print("Output:", full_output)  # Debugging: See full response

                if index == 0:  # SSH key verification prompt
                    print("➡️ Sending 'yes' to SSH confirmation")
                    child.sendline("yes")
                elif index == 1:  # Login prompt
                    print("➡️ Sending username")
                    child.sendline(ssh_username)  # Send your SSH username
                elif index == 2:
                    if chpasswd:# Password prompt
                        print("🔑 Sending new password")
                        child.sendline(ap_password)  # Send the password
                    else:
                        print("🔑 Sending default password")
                        child.sendline(ssh_password)  # Send the password
                elif index == 3 or index == 4:  # rkscli prompt (after successful login)
                    print("🔑 Sending new password")
                    chpasswd = True
                    child.sendline(ap_password)  # Send the password
                elif index == 5:  # rkscli prompt (after successful login)
                    print("✅ Successfully connected!")
                    break
                elif index == 6 or index == 7:  # EOF or Timeout
                    print("❌ Connection closed or timed out")
                    return
            except pexpect.TIMEOUT:
                print("❌ SSH Timeout: No response received")
                return

        commands = [
            f"set device-name {ap[0]}",
            f"set scg enable",
            f"set scg ip {VSZ_ADDRESS}",
            # f"set ipaddr wan {ap[2]} {netmask} {subnet}",
            "reboot"
        ]

        for command in commands:
            child.sendline(command)
            child.expect("rkscli:")
            output = child.before.decode().strip()
            print(f"📜 Command Output: {output}")

        child.close()

    except pexpect.exceptions.TIMEOUT:
        print("❌ Timeout: Device did not respond in time.")
    except pexpect.exceptions.EOF:
        print("❌ Connection closed unexpectedly.")
    except KeyboardInterrupt:
        print("❌ Script interrupted by user.")


for ap in ap_list:
    ssh_to_ap_and_configure(ap)

print("dupa")
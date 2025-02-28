import subprocess
import os
import re
import platform

def get_ip_from_mac_windows(mac_address):
    try:
        # Run the arp command
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)

        # Search for the MAC address in the output
        for line in result.stdout.split("\n"):
            if mac_address.lower() in line.lower():
                parts = re.split(r'\s+', line.strip())  # Split by whitespace
                return parts[0]  # IP address is the first column

    except subprocess.CalledProcessError as e:
        print(f"Error running arp: {e}")

    return None

def get_ip_by_mac_linux(mac_address):
    # Run the arp command to get a list of connected devices
    output = os.popen("arp -a").read()

    # Regular expression to find IP and MAC address pairs
    pattern = re.compile(r'\((.*?)\) at ([\w:]+)', re.IGNORECASE)

    for match in pattern.findall(output):
        ip, mac = match
        if mac.lower() == mac_address.lower():
            return ip
    return None



def get_ip_by_mac(mac_address):
    os_name = platform.system()
    if os_name == "Windows":
        return get_ip_from_mac_windows(mac_address)
    else:
        return get_ip_by_mac_linux(mac_address)

# Example MAC address (Replace with the actual MAC address)
mac_address = "56:66:a3:d7:dd:22"
ip_address = get_ip_by_mac(mac_address)

if ip_address:
    print(f"IP Address for MAC {mac_address}: {ip_address}")
else:
    print("MAC Address not found on the network")
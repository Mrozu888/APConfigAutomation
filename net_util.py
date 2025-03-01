import subprocess
import re

def get_ip_from_mac(mac_address):
    try:
        # Run the arp command using subprocess and capture the output
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=True)

        # Search for the MAC address in the output
        for line in result.stdout.splitlines():
            if mac_address.lower() in line.lower():  # match the MAC address (case-insensitive)
                # Extract IP address from the line
                match = re.search(r"\((.*?)\)", line)
                if match:
                    ip_address = match.group(1)
                    return ip_address
        return None

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
    except FileNotFoundError:
        print("Error: arp command not found.")
        return None

# Example MAC address (replace with the MAC address you're looking for)
mac_address = "00:33:58:33:A3:30"  # Replace with the MAC address of the other device

ip_address = get_ip_from_mac(mac_address)

if ip_address:
    print(f"IP Address corresponding to MAC {mac_address}: {ip_address}")
else:
    print(f"MAC address {mac_address} not found in the ARP table.")

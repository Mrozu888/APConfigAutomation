import subprocess
import re


def get_ip_from_mac(mac_address):
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


# Example usage
mac_address = "f4-91-1e-d3-c9-18"  # Ensure MAC format matches output (Windows uses '-')
ip_address = get_ip_from_mac(mac_address)

if ip_address:
    print(ip_address)  # Output only the IP address
else:
    print("Device not found.")

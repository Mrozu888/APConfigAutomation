from scapy.all import ARP, Ether, srp


def find_ip_by_mac(mac_address, network="192.168.0.1/24"):
    # Create an ARP request packet
    arp_request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    # Send packet and receive responses
    answered, _ = srp(packet, timeout=2, verbose=False)

    for sent, received in answered:
        if received.hwsrc.lower() == mac_address.lower():
            return received.psrc  # Return the IP address

    return None


# Example usage:
mac = "00:33:58:33:A3:30"  # Replace with your MAC address
ip = find_ip_by_mac(mac, "192.168.0.0/24")
print(f"IP Address: {ip}" if ip else "MAC Address not found")

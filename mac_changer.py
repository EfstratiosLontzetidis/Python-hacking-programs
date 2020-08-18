#!/usr/bin/env python

# run python mac_changer.py --help for the arguments in command line

# module re for regular expressions
import re

# module subprocess, using function subprocess.call for the commands
import subprocess

# module optparse to get arguments from user and use them
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address for the interface to change")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


# get values from command line
options = get_arguments()

# show current mac address
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

# change mac
change_mac(options.interface, options.new_mac)

# new mac
current_mac = get_current_mac(options.interface)
# compare old mac vs new mac in order to be the function successfull
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")

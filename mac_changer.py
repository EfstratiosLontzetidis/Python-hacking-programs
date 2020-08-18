#!/usr/bin/env python

# run python mac_changer.py --help for the arguments in command line

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
  

options= get_arguments()
change_mac(options.interface, options.new_mac)

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
  return parser.parse_args()


def change_mac(interface, new_mac):
  print("[+] Changing MAC address for " + interface + " to " + new_mac)
  subprocess.call(["ifconfig", interface, "down"])
  subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
  subprocess.call(["ifconfig", interface, "up"])
  

(options, arguments) = get_arguments()
change_mac(options.interface, options.new_mac)

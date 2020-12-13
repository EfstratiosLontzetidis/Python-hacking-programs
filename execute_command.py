#!/usr/bin/env python

import subprocess


command= "msg * you have been hacked"
#subprocess module lets you run commands in the os
subprocess.Popen(command, shell=True)

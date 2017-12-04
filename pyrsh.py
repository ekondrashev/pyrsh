#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
import argparse
import sys
from contextlib import contextmanager
import time

def arguments():
    parser = argparse.ArgumentParser(description='Remote command execution via ssh')
    parser.add_argument('host', help='Hostname', type=str)
    parser.add_argument('user', help='Your user', type=str)
    parser.add_argument('password', help='Your password', type=str)
    parser.add_argument('cmd', help='Your cmd', type=str)
    parser.add_argument('port', nargs='?', default=22, help='Enter your port, default port=22', type=int)
    result = parser.parse_args()
    return result
    
def response(channel):
    while not channel.recv_ready():
        time.sleep(0.1)
    stdout = ''
    while channel.recv_ready():
        stdout += channel.recv(1024)
    return stdout

@contextmanager
def ssh(args):
    connect = paramiko.SSHClient()
    connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connect.connect(hostname=args.host, port=args.port, username=args.user, password=args.password)
    yield connect
    connect.close()

def main(args):
    with ssh(args) as connect:
        channel = connect.invoke_shell()
        channel.send(args.cmd+'\n')
        stdout = response(channel)
        dsgsf = stdout
        return stdout
    
if __name__ == "__main__":
    try:
        args = arguments()
        result = main(args)
        print(result)
    except paramiko.ssh_exception.AuthenticationException as e:
        sys.stderr.write(e + "\n")
        sys.exit(-1)
    except:
        sys.stderr.write("Encountered an error\n")
        sys.exit(-1)

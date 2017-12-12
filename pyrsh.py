#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from app.paramiko import paramiko
from app.defaultssh import defaultssh
from app.telnet import telnet
from app.local import local
   
def arguments():
    parser = argparse.ArgumentParser(description='Remote command execution via ssh')
    parser.add_argument('type', help='Type remote connection. Value: local - local execute cmd; def_li - run a command for Linux without using third-party libraries; def_win - run a command for Linux without using third-party libraries; custom - run a command with using paramiko', type=str)
    parser.add_argument('cmd', help='Command bash', type=str)
    parser.add_argument('user', help='User name to use for authentication', type=str)
    parser.add_argument('password', help='Password to use for authentication', type=str)
    parser.add_argument('host', nargs='?', default="127.0.0.1", help='Hostname to use for authentication', type=str)
    parser.add_argument('port', nargs='?', default=22, help='Port/ID, default port=22', type=int)
    return parser.parse_args()

def main():
    try:
        args = arguments()
        if(args.type == "local"):
            runloc = local(args)
            print(runloc.run())
        elif(args.type == "def_li"):
            conlin = defaultssh(args)
            print(conlin.run())
        elif(args.type == "def_win"):
            conwin = telnet(args)
            print(conwin.run())
        elif(args.type == "custom"):
            conpara = paramiko(args)
            print(conpara.run())
    except:
        sys.stderr.write("Encountered an error\n")
        sys.exit(-1)

if __name__ == "__main__":
    main()

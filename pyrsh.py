#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from app.clparamiko import ClParamiko
from app.defaultssh import DefaultSsh
from app.telnet import ClTelnet
from app.local import Local
   
def arguments():
    parser = argparse.ArgumentParser(description='Remote command execution via ssh')
    parser.add_argument('type', help='Type remote connection. Value: pyr_local - local execute cmd; pyr_ssh - run a command for Linux without using third-party libraries; pyr_telnet - run a command for Linux without using third-party libraries; pyr_paramiko - run a command with using paramiko', type=str)
    parser.add_argument('cmd', help='Command bash', type=str)
    parser.add_argument('user', help='User name to use for authentication', type=str)
    parser.add_argument('password', help='Password to use for authentication', type=str)
    parser.add_argument('host', nargs='?', default="127.0.0.1", help='Hostname to use for authentication', type=str)
    parser.add_argument('port', nargs='?', default=22, help='Port/ID, default port=22', type=int)
    return parser.parse_args()

def main():
    try:
        dicar = {
                    'pyr_local': Local,
                    'pyr_ssh': DefaultSsh,
                    'pyr_telnet': ClTelnet,
                    'pyr_paramiko': ClParamiko,
                }
        args = arguments()
        cl  = dicar.get(args.type)(args) 
        print(cl.run())
    except:
        sys.stderr.write("Encountered an error\n")
        sys.exit(-1)

if __name__ == "__main__":
    main()

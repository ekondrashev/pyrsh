#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import getpass
import sys

from shell.base import Local, Ssh, Telnet, Paramiko

class Password(argparse.Action):

    def __call__(self, parser, namespace, values, option_string):
        setattr(namespace, self.dest, values)
        setattr(namespace, 'password', getpass.getpass())

def arguments():
    parser = argparse.ArgumentParser(description='Remote command execution via ssh')
    parser.add_argument('type', help='Type remote connection. Value: local - local execute cmd; ssh - run a command for Linux without using third-party libraries; telnet - run a command for Linux without using third-party libraries; paramiko - run a command with using paramiko', type=str)
    parser.add_argument('cmd', help='Command bash', type=str)
    parser.add_argument('user', action=Password, help='User name to use for authentication', type=str)
    parser.add_argument('host', nargs='?', default="127.0.0.1", help='Hostname to use for authentication', type=str)
    parser.add_argument('port', nargs='?', default=22, help='Port/ID, default port=22', type=int)
    return parser.parse_args()

def main():
    type_connect = {
                'local': Local,
                'ssh': Ssh,
                'telnet': Telnet,
                'paramiko': Paramiko,
            }
    args = arguments()
    try:
        try:
            with type_connect.get(args.type)(args) as base:
                for cmd in args.cmd.split('#'):
                    print(base.run(cmd))
        except NotImplementedError, msg:
            print msg  
    except:
        sys.stderr.write("Encountered an error\n")
        sys.exit(-1)

if __name__ == "__main__":
    main()

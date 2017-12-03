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
	parser.add_argument('command', help='Your command', type=str)
	parser.add_argument('port', nargs='?', default=22, help='Enter your port, default port=22', type=int)
	result = parser.parse_args()
	return result
	
@contextmanager
def ssh(args):
	try:
		connect = paramiko.SSHClient()
		connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		connect.connect(hostname=args.host, port=args.port, username=args.user, password=args.password)
	except paramiko.ssh_exception.AuthenticationException:
		sys.stderr.write("Authentication failed.\n")
		sys.exit(-1)

	try: 
		yield connect
	finally:
		connect.close()

def main(args):
	with ssh(args) as connect:
		channel = connect.invoke_shell()
		channel.send(args.command+'\n')
		time.sleep(2)
		output = channel.recv(10000)
		return output
	
if __name__ == "__main__":
	try:
		args = arguments()
		result = main(args)
		print(result)
	except:
		sys.stderr.write("Encountered an error\n")
		sys.exit(-1)

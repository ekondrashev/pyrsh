#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
import argparse
import sys
from contextlib import contextmanager
	
def arguments():
	# Create description scrit
	parser = argparse.ArgumentParser(description='Remote command execution via ssh')
	#  specify the name and description argyments
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
		# If you can not find the key when connecting to the server, then by default the key is "discouraged" and called SSHException.
		connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		connect.connect(hostname=args.host, port=args.port, username=args.user, password=args.password)
	except paramiko.ssh_exception.AuthenticationException:
		sys.stderr.write("Authentication failed.\n")
		sys.exit(-1)

	try: 
		if connect:
			yield connect
		else:
			yield False
	finally:
		if connect:
			# close connection
			connect.close()

def main():
	args = arguments()
	try:
		with ssh(args) as connect:
			# implementation commands
			stdin, stdout, stderr = connect.exec_command(args.command)
			# Output the result
			result = stdout.read() + stderr.read()
			print(result)
	except:
		sys.stderr.write("Encountered an error\n")
		sys.exit(-1)

	
if __name__ == "__main__":
	main()

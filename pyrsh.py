#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
import argparse
	
def main(args):
	host = args.host
	user = args.user
	psw = args.password
	port = args.port

	try:
		ssh = paramiko.SSHClient()

		# If you can not find the key when connecting to the server, then by default the key is "discouraged" and called SSHException.
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		
		ssh.connect(hostname=host, port=port, username=user, password=psw)

		# implementation commands
		stdin, stdout, stderr = ssh.exec_command(args.command)

		# Output the result
		result = stdout.read() + stderr.read()
		print(result)

		# For output the list
		# result = stdout.read().splitlines()
		# print(result)

		# close connection
		ssh.close()
		pass
	except:
		print('Connection failed')
		pass



if __name__ == "__main__":
	# Create description scrit
	parser = argparse.ArgumentParser(description='Remote command execution via ssh')
	#  specify the name and description argyments
	parser.add_argument('host', help='Hostname', type=str)
	parser.add_argument('user', help='Your user', type=str)
	parser.add_argument('password', help='Your password', type=str)
	parser.add_argument('command', help='Your command', type=str)
	parser.add_argument('port', nargs='?', default=22, help='Enter your port, default port=22', type=int)
	args = parser.parse_args()
	
	main(args)

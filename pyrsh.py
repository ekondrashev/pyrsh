#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
import argparse

def Main():

	# Описание скрипта
	parser = argparse.ArgumentParser(description='Remote command execution via ssh')
	#  Задаем названия и описания аргументов
	parser.add_argument('host', help='Hostname', type=str)
	parser.add_argument('user', help='Your user', type=str)
	parser.add_argument('password', help='Your password', type=str)
	parser.add_argument('command', help='Your command', type=str)
	args = parser.parse_args()

	host = args.host
	user = args.user
	psw = args.password
	port = 22

	try:
		ssh = paramiko.SSHClient()

		# если при соединении с сервером ключа не найдено, то по умолчанию ключ «отбивается» и вызввается SSHException.
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		
		ssh.connect(hostname=host, port=port, username=user, password=psw)

		# Выполнение команды
		stdin, stdout, stderr = ssh.exec_command(args.command)

		# Выводим результат
		result = stdout.read() + stderr.read()
		print(result)

		# или так если нужно вывести list
		# result = stdout.read().splitlines()
		# print(result)

		# Закрываем соединение
		ssh.close()
	except:
		print('Connection failed')
		pass



if __name__ == "__main__":
	Main()

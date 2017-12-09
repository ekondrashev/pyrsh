import paramiko
import time
from contextlib import contextmanager

class conparamiko:
	def __init__(self, args):
		self.host = args.host
		self.user = args.user
		self.password = args.password
		self.cmd = args.cmd
		self.port = args.port

	@contextmanager
	def connect(self):
		con = paramiko.SSHClient()
		con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		con.connect(hostname=self.host, port=self.port, username=self.user, password=self.password)
		yield con
		con.close()

	def response(self, channel):
		while not channel.recv_ready():
			time.sleep(0.1)
		stdout = ''
		while channel.recv_ready():
			stdout += channel.recv(1024)
		return stdout

	def sendncon(self):
		with self.connect() as connect:
			channel = connect.invoke_shell()
			self.response(channel)
			channel.send(self.cmd+'\n')
			stdout = self.response(channel)
			return stdout

	def run(self):
		try:
			return(self.sendncon())
		except paramiko.ssh_exception.AuthenticationException as e:
			return(e)
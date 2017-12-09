import telnetlib
import time
from contextlib import contextmanager

class conwindows:
	def __init__(self, args):
		self.host = args.host
		self.user = args.user
		self.password = args.password
		self.cmd = args.cmd

	@contextmanager
	def tnconnect(self):
		tn = telnetlib.Telnet(self.host)
		tn.read_until("login: ")
		tn.write(self.user + "\r")
		tn.read_until("password: ")
		tn.write(self.password + "\r")
		yield tn
		tn.close()

	def run(self):
		with self.tnconnect() as connect:			
			time.sleep(1)
			tn.write(self.cmd + "\r")
			return tn.read_all()
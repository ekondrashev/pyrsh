import telnetlib
import time
from contextlib import contextmanager

class telnet(object):
	def __init__(self, args):
		self.host = args.host
		self.user = args.user
		self.password = args.password
		self.cmd = args.cmd

	@contextmanager
	def tnconnect(self):
		tn = telnetlib.Telnet(self.host)
		tn.read_until("login: ")
		tn.write(self.user + "\r\n")
		tn.read_until("password: ")
		tn.write(self.password + "\r\n")
		yield tn
		tn.close()

	def run(self):
		with self.tnconnect() as connect:			
			tn.write(self.cmd + "\r\n")
			time.sleep(1)
			return tn.read_all()
			# return tn.read_very_eager()

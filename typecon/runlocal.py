import subprocess

class runlocal:
	def __init__(self, args):
		self.cmd = args.cmd

	def run(self):
		return subprocess.Popen(self.cmd, shell=True)
import subprocess

from args import Arguments

class Local(Arguments):
    def __init__(self, args):
        Arguments.__init__(self, args)

    def run(self):
        return subprocess.Popen(self.cmd, shell=True)

import subprocess

from args import Arguments
from shell import Shell

class Local(Arguments, Shell):
    def __init__(self, args, password):
        Arguments.__init__(self, args, password)

    def run(self):
        return subprocess.Popen(self.cmd, shell=True)

import subprocess

from shell import Shell
from args import Arguments


class Local(Shell):
    def __init__(self, args):
        self.arg=Arguments(args)
        self.result = {}

    def run(self):
        for cmd in self.arg.getCmd():
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            self.result[cmd] = p.stdout.read()
        return self.result

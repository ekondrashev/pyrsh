import subprocess

from shell import Shell

class Local(Shell):
    def __init__(self, args):
        Shell.__init__(self, args)

    def run(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        return p.stdout.read()

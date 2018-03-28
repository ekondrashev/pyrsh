import subprocess

from args import Arguments


class Local(Arguments):
    def __init__(self, args):
        Arguments.__init__(self, args)

    def run(self):
        for cmd in self.cmds:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            self.result[cmd] = p.stdout.read()
        return self.result

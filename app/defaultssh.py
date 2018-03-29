import subprocess

from args import Arguments
from shell import Shell

class DefaultSsh(Shell):
    def __init__(self, args):
        self.arg=Arguments(args)
        self.result = {}

    def run(self):
        per = str(self.arg.getUser()+'@'+self.arg.getHost())

        for cmd in self.arg.getCmd():
            ssh = subprocess.Popen(['ssh', per, cmd],
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            checkerror = ssh.stdout.readlines()
            if checkerror == []:
                self.result[cmd] = ssh.stderr.readlines()
            else:
                self.result[cmd] = checkerror
        return self.result

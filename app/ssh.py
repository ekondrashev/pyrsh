import subprocess

from shell import Shell

class Ssh(Shell):
    def __init__(self, args):
        Shell.__init__(self, args)

    def run(self, cmd):
        per = str(self.user+'@'+self.host)
        ssh = subprocess.Popen(['ssh', per, cmd],
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        checkerror = ssh.stdout.readlines()
        if checkerror == []:
            return ssh.stderr.readlines()
        else:
            return checkerror

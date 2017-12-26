import subprocess

from args import Arguments

class DefaultSsh(Arguments):
    def __init__(self, args):
        Arguments.__init__(self, args)

    def run(self):
        per = str(self.user+'@'+self.host)
        ssh = subprocess.Popen(['ssh', per, self.cmd],
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
        # error
            return ssh.stderr.readlines()
        else:
            return result

import subprocess

class Local(object):
    def __init__(self, args):
        self.args = args

    def run(self):
        return subprocess.Popen(self.args.cmd, shell=True)

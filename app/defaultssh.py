import subprocess

class DefaultSsh(object):
  def __init__(self, args):
    self.args = args

  def run(self):
    per = str(self.args.user+'@'+self.args.host)
    ssh = subprocess.Popen(['ssh', per, self.args.cmd],
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
      # error
      return ssh.stderr.readlines()
    else:
      return result

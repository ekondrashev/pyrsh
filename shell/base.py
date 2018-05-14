import paramiko
import time
import subprocess
import telnetlib

class Base(object):
    def __init__(self, args):
        self.args = args

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return

    def run(self, *args, **kwargs):
        raise NotImplementedError('Methodethod not implemented.')

class Paramiko(Base):    
    def __enter__(self):
        self.con = paramiko.SSHClient()
        self.con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.con.connect(hostname=self.args.host, port=self.args.port, username=self.args.user, password=self.args.password)
        return self

    def __exit__(self, type, value, traceback):
        self.con.close()       

    def _response(self, channel):
        while not channel.recv_ready():
            time.sleep(0.1)
        stdout = ''
        while channel.recv_ready():
            stdout += channel.recv(1024)
        return stdout

    def run(self, cmd):
        channel = self.con.invoke_shell()
        self._response(channel)
        channel.send(cmd+'\n')
        return self._response(channel)

class Local(Base):
    def run(self, cmd):
        query = subprocess.Popen(cmd,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
                )
        checkerror = query.stdout.readlines()
        if checkerror == []:
            return query.stderr.readlines()
        else:
            return checkerror 

class Ssh(Base):
    def init__(args):
        Base.__init__(self, args)
        self.local = Local(self.args)
        
    def __enter__(self):
        self.local.__enter__()
        return self
    
    def __exit__(self):
        return self.local.__exit__()

    def run(self, cmd):
        per = str(self.args.user+'@'+self.args.host)
        return self.local.run(['ssh', per, cmd])

class Telnet(Base):
    def __enter__(self):
        self.con = telnetlib.Telnet(self.args.host, self.args.port)
        self.con.read_until("login: ")
        self.con.write(self.args.user + "\r\n")
        self.con.read_until("password: ")
        self.con.write(self.args.password + "\r\n")
        return self

    def __exit__(self, type, value, traceback):
        self.con.close()       

    def run(self, cmd):
        self.con.write(cmd + "\r\n")
        time.sleep(1)
        return self.con.read_all()

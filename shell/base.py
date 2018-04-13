import paramiko
import time
import subprocess
import telnetlib

class Base(object):
    def run(self, *args, **kwargs):
        raise NotImplementedError('Abstract method not implemented.')

class ExecutionSubproces(object):
    def run(self, per):
        query = subprocess.Popen(per,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
                )
        checkerror = query.stdout.readlines()
        if checkerror == []:
            return query.stderr.readlines()
        else:
            return checkerror

class Connection(object):
    def __init__(self, args):
        if(args.type == "paramiko"):
            self.con = paramiko.SSHClient()
            self.con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.con.connect(hostname=args.host, port=args.port, username=args.user, password=args.password)
        elif(args.type == "telnet"):
            self.con = telnetlib.Telnet(args.host, args.port)
            self.con.read_until("login: ")
            self.con.write(args.user + "\r\n")
            self.con.read_until("password: ")
            self.con.write(args.password + "\r\n")

    def __enter__(self):
        return self.con

    def __exit__(self, type, value, traceback):
        self.con.close()

class Paramiko(Base):
    def __init__(self, args):
        self.args = args
        self.base = Base()

    def _response(self, channel):
        while not channel.recv_ready():
            time.sleep(0.1)
        stdout = ''
        while channel.recv_ready():
            stdout += channel.recv(1024)
        return stdout

    def _send_connect(self, cmd):
        with Connection(self.args) as connect:
            channel = connect.invoke_shell()
            self._response(channel)
            channel.send(cmd+'\n')
            return self._response(channel)

    def run(self, cmd):
        try:
            return(self._send_connect(cmd))
        except paramiko.ssh_exception.AuthenticationException as e:
            return(e)

class Local(Base):
    def __init__(self, *args):
        self.execution = ExecutionSubproces()

    def run(self, cmd):
        return self.execution.run(cmd)

class Ssh(Base):
    def __init__(self, args):
        self.user = args.user
        self.host = args.host
        self.base = Base()
        self.execution = ExecutionSubproces()

    def run(self, cmd):
        per = str(self.user+'@'+self.host)
        return self.execution.run(['ssh', per, cmd])

class Telnet(Base):
    def __init__(self, args):
        self.args = args
        self.base = Base()

    def run(self, cmd):
        with Connection(self.args) as connect:
            connect.write(cmd + "\r\n")
            time.sleep(1)
            return connect.read_all()

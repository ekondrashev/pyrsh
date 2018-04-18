import paramiko
import time
import subprocess
import telnetlib

class Base(object):
    def __init__(self, args):
        self.con = Connection()._definition_con(args)

    def __enter__(self):
        return self.con

    def __exit__(self, type, value, traceback):
        self.con.close()

    def run(self, *args, **kwargs):
        raise NotImplementedError('Abstract method not implemented.')

class Connection(object):    
    def _definition_con(self, args):
        if(args.type == "paramiko"):
            return self._type_paramiko(args)
        elif(args.type == "telnet"):
            return self._type_telnet(args)

    def _type_paramiko(self, args):
            self.con = paramiko.SSHClient()
            self.con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.con.connect(hostname=args.host, port=args.port, username=args.user, password=args.password)
            return self.con

    def _type_telnet(self, args):
            self.con = telnetlib.Telnet(args.host, args.port)
            self.con.read_until("login: ")
            self.con.write(args.user + "\r\n")
            self.con.read_until("password: ")
            self.con.write(args.password + "\r\n")
            return self.con

class ExecutionSubproces(object):
    def __init__(self, *args):
        self.args = args

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

class Paramiko(Base):
    def __init__(self, args):
        self.args = args
        self.base = Base(self.args)

    def _response(self, channel):
        while not channel.recv_ready():
            time.sleep(0.1)
        stdout = ''
        while channel.recv_ready():
            stdout += channel.recv(1024)
        return stdout

    def _send_connect(self, cmd):
        with self.base as connect:
            channel = connect.invoke_shell()
            self._response(channel)
            channel.send(cmd+'\n')
            return self._response(channel)

    def run(self, cmd):
        try:
            return(self._send_connect(cmd))
        except paramiko.ssh_exception.AuthenticationException as e:
            return(e)

class Ssh(Base):
    def __init__(self, args):
        self.args = args.args
        self.base = Base(self.args)
        self.execution = ExecutionSubproces()

    def run(self, cmd):
        per = str(self.args.user+'@'+self.args.host)
        return self.execution.run(['ssh', per, cmd])

class Telnet(Base):
    def __init__(self, args):
        self.args = args
        self.base = Base(self.args)

    def run(self, cmd):
        with Base(self.args) as connect:
            connect.write(cmd + "\r\n")
            time.sleep(1)
            return connect.read_all()

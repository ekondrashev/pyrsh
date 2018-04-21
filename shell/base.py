import paramiko
import time
import subprocess
import telnetlib

class Base(object):
    def __init__(self, args):
        self.args = args

    def __enter__(self):
        self.con = Connection()._definition_con(self.args)
        return self.con

    def __exit__(self, type, value, traceback):
        self.con.close()

    def run(self, *args, **kwargs):
        raise NotImplementedError('Abstract method not implemented.')

class Connection(object):    
    def _definition_con(self, args):
        if(args.type == "paramiko"):
            return Paramiko(args)._type_paramiko()
        elif(args.type == "telnet"):
            return Telnet(args)._type_telnet()

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
        Base.__init__(self, args)

    def _type_paramiko(self):
            self.con = paramiko.SSHClient()
            self.con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.con.connect(hostname=self.args.host, port=self.args.port, username=self.args.user, password=self.args.password)
            return self.con

    def _response(self, channel):
        while not channel.recv_ready():
            time.sleep(0.1)
        stdout = ''
        while channel.recv_ready():
            stdout += channel.recv(1024)
        return stdout

    def _send_connect(self, cmd):
        with Base(self.args) as connect:
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
        Base.__init__(self, args)
        self.execution = ExecutionSubproces()

    def run(self, cmd):
        per = str(self.args.user+'@'+self.args.host)
        return self.execution.run(['ssh', per, cmd])

class Telnet(Base):
    def __init__(self, args):
        Base.__init__(self, args)

    def _type_telnet(self):
        self.con = telnetlib.Telnet(self.args.host, self.args.port)
        self.con.read_until("login: ")
        self.con.write(self.args.user + "\r\n")
        self.con.read_until("password: ")
        self.con.write(self.args.password + "\r\n")
        return self.con

    def run(self, cmd):
        with Base(self.args) as connect:
            connect.write(cmd + "\r\n")
            time.sleep(1)
            return connect.read_all()

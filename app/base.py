import paramiko as p
import time
from contextlib import contextmanager
import subprocess
import telnetlib

class Base(object):
    def __init__(self, args):
        self.type = args.type
        self.user = args.user
        # self.password = args.password
        self.password = "MndJa1hkPimLDZya"
        self.host = args.host
        self.port = args.port

    @contextmanager
    def _connect(self):
        con = p.SSHClient()
        con.set_missing_host_key_policy(p.AutoAddPolicy())
        con.connect(hostname=self.host, port=self.port, username=self.user, password=self.password)
        yield con
        con.close()

    @contextmanager
    def _tn_connect(self):
        tn = telnetlib.Telnet(self.host, self.port)
        tn.read_until("login: ")
        tn.write(self.user + "\r\n")
        tn.read_until("password: ")
        tn.write(self.password + "\r\n")
        yield tn
        tn.close()

    def _response(self, channel):
        while not channel.recv_ready():
            time.sleep(0.1)
        stdout = ''
        while channel.recv_ready():
            stdout += channel.recv(1024)
        return stdout
    
    def _send_connect(self, cmd):
        with self._connect() as connect:
            channel = connect.invoke_shell()
            self._response(channel)
            channel.send(cmd+'\n')
            return self._response(channel)

    def paramiko(self, cmd):
        try:
            return(self._send_connect(cmd))
        except p.ssh_exception.AuthenticationException as e:
            return(e)

    def local(self, cmd):
        res = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        return res.stdout.read()

    def telnet(self, cmd):
        with self._tn_connect() as connect: 
            tn.write(cmd + "\r\n")
            time.sleep(1)
            return tn.read_all()

    def ssh(self, cmd):
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

    def run(self, cmd):
        dicar = {
                'local': self.local,
                'ssh': self.ssh,
                'telnet': self.telnet,
                'paramiko': self.paramiko,
            }
        return dicar.get(self.type)(cmd)

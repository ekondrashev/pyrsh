import paramiko
import time
from contextlib import contextmanager

from args import Arguments
from shell import Shell

class ClParamiko(Arguments, Shell):
    def __init__(self, args):
        Arguments.__init__(self, args)

    @contextmanager
    def connect(self):
        con = paramiko.SSHClient()
        con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        con.connect(hostname=self.host, port=self.port, username=self.user, password=self.password)
        yield con
        con.close()

    def response(self, channel):
        while not channel.recv_ready():
            time.sleep(0.1)
        stdout = ''
        while channel.recv_ready():
            stdout += channel.recv(1024)
        return stdout

    def send_connect(self):
        with self.connect() as connect:
            channel = connect.invoke_shell()
            self.response(channel)
            channel.send(self.cmd+'\n')
            stdout = self.response(channel)
            return stdout

    def run(self):
        try:
            return(self.send_connect())
        except paramiko.ssh_exception.AuthenticationException as e:
            return(e)

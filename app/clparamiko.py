import paramiko
import time
from contextlib import contextmanager

from args import Arguments

class ClParamiko(Arguments):
    def __init__(self, args):
        Arguments.__init__(self, args)

    @contextmanager
    def _connect(self):
        con = paramiko.SSHClient()
        con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        con.connect(hostname=self.host, port=self.port, username=self.user, password=self.password)
        yield con
        con.close()

    def _response(self, channel):
        while not channel.recv_ready():
            time.sleep(0.1)
        stdout = ''
        while channel.recv_ready():
            stdout += channel.recv(1024)
        return stdout

    def _send_connect(self):
        with self._connect() as connect:
            channel = connect.invoke_shell()
            self._response(channel)
            for cmd in self.cmds:
                channel.send(self.cmd+'\n')
                self.result[cmd] = self._response(channel)
            return self.result

    def run(self):
        try:
            return(self._send_connect())
        except paramiko.ssh_exception.AuthenticationException as e:
            return(e)

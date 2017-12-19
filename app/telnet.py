import telnetlib
import time
from contextlib import contextmanager

from args import Arguments

class ClTelnet(Arguments):
    def __init__(self, args):
        Arguments.__init__(self, args)

    @contextmanager
    def tn_connect(self):
        tn = telnetlib.Telnet(self.host, self.port)
        tn.read_until("login: ")
        tn.write(self.user + "\r\n")
        tn.read_until("password: ")
        tn.write(self.password + "\r\n")
        yield tn
        tn.close()

    def run(self):
        with self.tn_connect() as connect:          
            tn.write(self.cmd + "\r\n")
            time.sleep(1)
            return tn.read_all()

import telnetlib
import time
from contextlib import contextmanager

from args import Arguments

class ClTelnet(Arguments):
    def __init__(self, args):
        Arguments.__init__(self, args)

    @contextmanager
    def _tn_connect(self):
        tn = telnetlib.Telnet(self.host, self.port)
        tn.read_until("login: ")
        tn.write(self.user + "\r\n")
        tn.read_until("password: ")
        tn.write(self.password + "\r\n")
        yield tn
        tn.close()

    def run(self):
        with self._tn_connect() as connect: 
            
            for cmd in self.cmds:
                tn.write(self.cmd + "\r\n")
                time.sleep(1)
                self.result[cmd] = tn.read_all()
            return self.result  

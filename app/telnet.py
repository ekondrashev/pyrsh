import telnetlib
import time
from contextlib import contextmanager

from args import Arguments
from shell import Shell

class ClTelnet(Shell):
    def __init__(self, args):
        self.arg=Arguments(args)
        self.result = {}

    @contextmanager
    def _tn_connect(self):
        tn = telnetlib.Telnet(self.arg.getHost(), self.arg.getPort())
        tn.read_until("login: ")
        tn.write(self.arg.getUser() + "\r\n")
        tn.read_until("password: ")
        tn.write(self.arg.getPassword() + "\r\n")
        yield tn
        tn.close()

    def run(self):
        with self._tn_connect() as connect: 
            
            for cmd in self.arg.getCmd():
                tn.write(cmd + "\r\n")
                time.sleep(1)
                self.result[cmd] = tn.read_all()
            return self.result  

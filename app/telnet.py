import telnetlib
import time
from contextlib import contextmanager

from shell import Shell

class Telnet(Shell):
    def __init__(self, args):
        Shell.__init__(self, args)

    @contextmanager
    def _tn_connect(self):
        tn = telnetlib.Telnet(self.host, self.port)
        tn.read_until("login: ")
        tn.write(self.user + "\r\n")
        tn.read_until("password: ")
        tn.write(self.password + "\r\n")
        yield tn
        tn.close()

    def run(self, cmd):
        with self._tn_connect() as connect: 
            tn.write(cmd + "\r\n")
            time.sleep(1)
            return tn.read_all()

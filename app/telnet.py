import telnetlib
import time
from contextlib import contextmanager

class ClTelnet(object):
    def __init__(self, args):
        self.args = args

    @contextmanager
    def tn_connect(self):
        tn = telnetlib.Telnet(self.args.host, self.args.port)
        tn.read_until("login: ")
        tn.write(self.args.user + "\r\n")
        tn.read_until("password: ")
        tn.write(self.args.password + "\r\n")
        yield tn
        tn.close()

    def run(self):
        with self.tn_connect() as connect:          
            tn.write(self.args.cmd + "\r\n")
            time.sleep(1)
            return tn.read_all()

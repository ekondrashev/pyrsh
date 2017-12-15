#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import SocketServer
from telnetsrv.threaded import TelnetHandler, command


class TelnetServer(SocketServer.TCPServer):
    allow_reuse_address = True

class MyHandler(TelnetHandler):
    authNeedUser = True
    authNeedPass = True

    @command('version')
    def version(self, params):
        self.writeresponse("V1.0")

    def authCallback(self, username, password):
        if username != "a" or password != 'a':
            raise RuntimeError('Wrong password!')


if __name__ == "__main__":
	try:
		server = TelnetServer(("localhost", 10023), MyHandler)
		server.serve_forever()
		server.close()
	except KeyboardInterrupt:
		sys.stderr.write("Exiting telnet server\n")
        sys.exit(-1)
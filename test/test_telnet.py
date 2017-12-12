#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import SocketServer
from argparse import Namespace
from telnetsrv.threaded import TelnetHandler, command

from app.telnet import telnet

def args(cmd, host='localhost', user='a', password='a', port=10023):
    return Namespace(host=host, user=user, password=password, cmd=cmd, port=port)

class TelnetServer(SocketServer.TCPServer):
    allow_reuse_address = True

class MyHandler(TelnetHandler):
    @command('version')
    def version(self, params):
        self.writeresponse("V1.0")

    authNeedUser = True
    authNeedPass = True

    def authCallback(self, username, password):
        if username != "a" or password != 'a':
            raise RuntimeError('Wrong password!')

class TelnetTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = TelnetServer(("localhost", 10023), MyHandler)
        try:
            cls.server.serve_forever()
        except KeyboardInterrupt:
            print("Exiting telnet server")

    @classmethod
    def tearDownClass(cls):
        cls.server.close()

    def test_telnet(self):
        res = telnet(args("version"))
        print( res.run() )
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()

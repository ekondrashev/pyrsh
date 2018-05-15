#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import unittest
from argparse import Namespace

from shell.base import Telnet


def args(cmd, host='localhost', user='a', password='a', port=10023):
    return Namespace(host=host, user=user, password=password, cmd=cmd, port=port)


class TelnetTest(unittest.TestCase):
    def setUp(self):
        self.shell = Telnet(args("cmd"))
        self.shell = self.shell.__enter__()

    def tearDown(self):
        self.shell.__exit__(self, 'var1', 'var1',)
        self.assertTrue(1)


    def test_telnet(self):
        self.assertEqual(self.shell.run("version"), ('V1.0'))

if __name__ == "__main__":
    unittest.main()

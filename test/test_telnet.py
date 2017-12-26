#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import unittest
from argparse import Namespace

from app.telnet import ClTelnet


def args(cmd, host='localhost', user='a', password='a', port=10023):
    return Namespace(host=host, user=user, password=password, cmd=cmd, port=port)


class TelnetTest(unittest.TestCase):
    def test_telnet(self):
        res = ClTelnet(args("version"))
        self.assertEqual(res.run(), ('V1.0'))

if __name__ == "__main__":
    unittest.main()

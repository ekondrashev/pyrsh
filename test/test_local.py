#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
from argparse import Namespace

from app.local import Local


def args(cmd):
    return Namespace(cmd=cmd)

class LocalTest(unittest.TestCase):
    def test_command_help(self):
        loc = Local(args("help"))
        self.assertTrue(loc.run())
        
if __name__ == "__main__":
    unittest.main()

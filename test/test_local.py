#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import unittest
from argparse import Namespace

from shell.base import Local



class LocalTest(unittest.TestCase):

    def setUp(self):
        self.shell = Local(Namespace(cmd="cmd"))
        self.shell = self.shell.__enter__()

    def tearDown(self):
        self.shell.__exit__(self, 'var1', 'var1',)
        self.assertTrue(1)

    def test_command_pwd(self):
        print(self.shell.run("pwd"))

    def test_command_ls(self):
        print(self.shell.run("ls"))

        
if __name__ == "__main__":
    unittest.main()

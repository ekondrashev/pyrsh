#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import time
import unittest
import tempfile
import shutil
import MockSSH
import paramiko
from argparse import Namespace

from shell.base import Paramiko

def args(cmd, host='127.0.0.1', user='testadmin', password='x', port=9999):
    return Namespace(host=host, user=user, password=password, cmd=cmd, port=port)

class PyrshTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #
        # command: pwd
        #
        def pwd_command_success(instance):
            instance.writeln("[OK]")
        def pwd_command_failure(instance):
            instance.writeln("MockSSH: Supported usage: pwd")
        command_pwd = MockSSH.ArgumentValidatingCommand('pwd', [pwd_command_success],
                                                       [pwd_command_failure], *[])
        #
        # command: ls
        #
        def ls_command_success(instance):
            instance.writeln("[OK]")
        def ls_command_failure(instance):
            instance.writeln("MockSSH: Supported usage: ls l")
        command_ls = MockSSH.ArgumentValidatingCommand('ls', [ls_command_success],
                                               [ls_command_failure], *["l"])
        #
        # command: date
        #
        def date_command_success(instance):
            instance.writeln("[OK]")
        def date_command_failure(instance):
            instance.writeln("MockSSH: Supported usage: date")
        command_date = MockSSH.ArgumentValidatingCommand('date', [date_command_success],
                                               [date_command_failure], *[])
        commands = [ command_pwd, command_ls, command_date ]
        users = {'testadmin': 'x'}
        cls.keypath = tempfile.mkdtemp()
        MockSSH.startThreadedServer(
            commands,
            prompt="hostname>",
            keypath=cls.keypath,
            interface="localhost",
            port=9999,
            **users)

    @classmethod
    def tearDownClass(cls):
        MockSSH.stopThreadedServer()
        shutil.rmtree(cls.keypath)
    
    def setUp(self):
        self.shell = Paramiko(args("cmd"))
        self.shell = self.shell.__enter__()

    def tearDown(self):
        self.shell.__exit__(self, 'var1', 'var1',)
        self.assertTrue(1)

    def test_command_pwd(self):
        print(self.shell.run("pwd"))
        self.assertEqual(self.shell.run("pwd"), ('pwd\r\n[OK]\r\nhostname>'))

    def test_command_ls(self):
        print(self.shell.run("ls l"))
        self.assertEqual(self.shell.run("ls l"), ('ls l\r\n[OK]\r\nhostname>'))

    def test_command_date(self):
        print(self.shell.run("date l"))
        self.assertEqual(self.shell.run("date l"), ('date l\r\nMockSSH: Supported usage: date\r\nhostname>'))

if __name__ == "__main__":
    unittest.main()

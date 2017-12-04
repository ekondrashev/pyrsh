#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import unittest
import tempfile
import shutil
import sys
import MockSSH
import paramiko
from pyrsh import main
from argparse import Namespace

def args( cmd, host='127.0.0.1', user='testadmin', password='x', port=9999 ):
    arg = Namespace(host=host, user=user, password=password, cmd=cmd, port=port)
    return arg

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

    def test_command_pwd(self):
        result = main(args('pawdwd'))
        self.assertEqual(result, ('hostname>'))

    def test_command_ls(self):
        result = main(args('ls l'))
        self.assertEqual(result, ('hostname>'))

    def test_command_date(self):
        result = main(args('date'))
        self.assertEqual(result, ('hostname>'))

if __name__ == "__main__":
    unittest.main()

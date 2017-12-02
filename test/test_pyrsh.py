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

def recv_all(channel):
    while not channel.recv_ready():
        time.sleep(0.1)
    stdout = ''
    while channel.recv_ready():
        stdout += channel.recv(1024)
    return stdout


class MockCiscoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):


        try:
            #
            # command: pwd
            #
            def pwd_command_success(instance):
                instance.writeln("[OK]")
            def pwd_command_failure(instance):
                instance.writeln("MockSSH: Supported usage: pwd")
            command_pwd = MockSSH.ArgumentValidatingCommand('pwd', [pwd_command_success],
                                                           [pwd_command_failure], *[])
            commands = [ command_pwd ]
            users = {'testadmin': 'x'}
            cls.keypath = tempfile.mkdtemp()
            MockSSH.startThreadedServer(
                commands,
                prompt="hostname>",
                keypath=cls.keypath,
                interface="localhost",
                port=9999,
                **users)
        except KeyboardInterrupt:
            print "User interrupted"
            sys.exit(1)


    @classmethod
    def tearDownClass(cls):
        print "tearDownClass"
        MockSSH.stopThreadedServer()
        shutil.rmtree(cls.keypath)

    def test_password_reset_success(self):
        args = Namespace(host='127.0.0.1', user='testadmin', password='x', command='pwd', port=9999)
        result = main(args)
        self.assertEqual(result, ('hostname>pwd\r\n[OK]\r\nhostname>'))


if __name__ == "__main__":
    unittest.main()

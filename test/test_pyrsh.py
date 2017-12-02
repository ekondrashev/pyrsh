#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import unittest
import tempfile
import shutil

import MockSSH
import paramiko
from cisco import commands


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
        print "tearDownClass"
        MockSSH.stopThreadedServer()
        shutil.rmtree(cls.keypath)

    def test_password_reset_success(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
        ssh.connect('127.0.0.1', username='testadmin', password='x', port=9999)

        channel = ssh.invoke_shell()
        recv_all(channel)
        
        channel.send('pwd\n')
        stdout = recv_all(channel)
        self.assertEqual(stdout, ('pwd\r\n[OK]\r\nhostname>'))


if __name__ == "__main__":
    unittest.main()

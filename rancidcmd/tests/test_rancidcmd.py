# -*- coding: utf-8 -*-
"""
tests.test_rancid
==================

"""


import unittest
import os
from rancidcmd.rancidcmd import RancidCmd


class UnitTests(unittest.TestCase):
    """ Unit Test """

    def setUp(self):
        """ setup """
        self.rancid_clogin = RancidCmd(
            method='clogin', timeout=10,
            user='rancid', password='password',
            address='192.168.1.1')

        self.rancid_jlogin = RancidCmd(
            method='jlogin', timeout=10,
            user='rancid', password='password',
            address='192.168.1.2')

    def test_rancid(self):
        """ test rancid """
        self.assertEqual(self.rancid_clogin.method, 'clogin')
        self.assertEqual(self.rancid_jlogin.method, 'jlogin')

    def test_cmd_token(self):
        """ test for command token """
        cmd = 'clogin -t 10 -u "rancid" -p "password" -e "password" -c "show version" 192.168.1.1'  # NOQA
        cmd_args = self.rancid_clogin.cmd_token(cmd)
        self.assertEqual(cmd_args, ['clogin',
                                    '-t',
                                    '10',
                                    '-u',
                                    'rancid',
                                    '-p',
                                    'password',
                                    '-e',
                                    'password',
                                    '-c',
                                    'show version',
                                    '192.168.1.1'])

    def test_generate_rancid_cmd(self):
        """ test for generate rancid command """

        cmd = 'show version'

        # clogin
        rancid_cmd = self.rancid_clogin.generate_rancid_cmd(cmd)
        self.assertEqual(
            rancid_cmd,
            'clogin -t 10 -u "rancid" -p "password" -e "password" -c "show version" 192.168.1.1')  # NOQA

        # jlogin
        rancid_cmd = self.rancid_jlogin.generate_rancid_cmd(cmd)
        self.assertEqual(
            rancid_cmd,
            'jlogin -t 10 -u "rancid" -p "password" -c "show version" 192.168.1.2')  # NOQA

        # None support
        rancid_xlogin = RancidCmd(
            method='xlogin', timeout=10,
            user='rancid', password='password',
            address='192.168.1.99')

        rancid_cmd = rancid_xlogin.generate_rancid_cmd(cmd)
        self.assertEqual(rancid_cmd, False)

    def test_clogin_cmd(self):
        """ test for clogin command """

        cmd = 'show version'
        cmd = self.rancid_clogin.clogin_cmd(cmd)
        self.assertEqual(
            cmd,
            'clogin -t 10 -u "rancid" -p "password" -e "password" -c "show version" 192.168.1.1')  # NOQA

    def test_jlogin_cmd(self):
        """ test for jlogin command """

        cmd = 'show version'
        cmd = self.rancid_jlogin.jlogin_cmd(cmd)
        self.assertEqual(
            cmd,
            'jlogin -t 10 -u "rancid" -p "password" -c "show version" 192.168.1.2')  # NOQA

    def test_cmd_exec(self):
        """ test for command execute """
        res = self.rancid_clogin.cmd_exec('echo test')
        self.assertEqual(res, {'std_out': 'test\n', 'std_err': ''})

    def test_touch(self):
        """ test for file touch """
        path = "./_test_touch_file.txt"
        RancidCmd.touch(path)
        is_exists = os.path.isfile(path)
        if is_exists:
            os.remove(path)
        self.assertEqual(is_exists, True)

    def test_check_cloginrc(self):
        """ test for check cloginrc """
        name = '_test_cloginrc'
        path = RancidCmd.check_cloginrc(name=name)
        is_exists = os.path.isfile(path)
        mode = os.stat(path).st_mode
        if is_exists:
            os.remove(path)
        self.assertEqual(is_exists, True)
        self.assertEqual(mode, 33216)  # oct(33216) == '0o100700'

    def test_decode_bytes(self):
        """ test for decode bytes """
        test_str = 'abcdABCD01234$&=+-*%[]#!/"@'
        byte_data = str.encode(test_str)
        decod_data = self.rancid_clogin.decode_bytes(byte_data)
        self.assertEqual(decod_data, test_str)

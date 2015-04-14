# -*- coding: utf-8 -*-

"""UnitTests for rancidcmd."""


import unittest
import os
import uuid
import stat
from rancidcmd.rancidcmd import RancidCmd


class UnitTests(unittest.TestCase):

    """The :class:`UnitTests <UnitTests>` object.

    UnitTests

    """

    def setUp(self):
        """setup."""
        self.rancid_clogin = RancidCmd(
            method='clogin', timeout=10,
            user='rancid', password='password',
            address='192.168.1.1')

        self.rancid_jlogin = RancidCmd(
            method='jlogin', timeout=10,
            user='rancid', password='password',
            address='192.168.1.2')

    def test_rancid(self):
        """Check login method."""
        self.assertEqual(self.rancid_clogin.method, 'clogin')
        self.assertEqual(self.rancid_jlogin.method, 'jlogin')

    def test_timeout_value(self):
        """check timeout value."""
        obj = self.rancid_jlogin = RancidCmd(
            method='clogin', user='rancid',
            password='password', address='192.168.1.2')
        self.assertEqual(obj.timeout, 10)

        timeout = 20
        obj = self.rancid_jlogin = RancidCmd(
            timeout=timeout,
            method='clogin', user='rancid',
            password='password', address='192.168.1.2')
        self.assertEqual(obj.timeout, timeout)

    def test_cmd_token(self):
        """Check command line split."""
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
        """Check rancid command format."""
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
        """Check clogin command format."""
        cmd = 'show version'
        cmd = self.rancid_clogin.clogin_cmd(cmd)
        self.assertEqual(
            cmd,
            'clogin -t 10 -u "rancid" -p "password" -e "password" -c "show version" 192.168.1.1')  # NOQA

    def test_jlogin_cmd(self):
        """Check jlogin command format."""
        cmd = 'show version'
        cmd = self.rancid_jlogin.jlogin_cmd(cmd)
        self.assertEqual(
            cmd,
            'jlogin -t 10 -u "rancid" -p "password" -c "show version" 192.168.1.2')  # NOQA

    def test_cmd_exec(self):
        """Check excecuter result."""
        res = self.rancid_clogin.cmd_exec('echo test')
        self.assertEqual(res, {'std_out': 'test\n', 'std_err': ''})

    def test_touch(self):
        """Check make file."""
        path = '%s.txt' % uuid.uuid4()
        RancidCmd.touch(path)
        is_exists = os.path.isfile(path)
        if is_exists:
            os.remove(path)
        self.assertEqual(is_exists, True)

    def test_touch_permission_error(self):
        """Check file permission error."""
        try:
            path = '%s.txt' % uuid.uuid4()
            with open(path, 'a'):
                os.utime(path, None)
                os.chmod(path, stat.S_IRUSR | stat.S_IXUSR)
            with self.assertRaises(Exception):
                RancidCmd.touch(path)
        finally:
            os.remove(path)

    def test_check_cloginrc(self):
        """Check cloginrc setting file."""
        name = '_test_cloginrc'
        path = RancidCmd.check_cloginrc(name=name)
        is_exists = os.path.isfile(path)
        mode = os.stat(path).st_mode
        if is_exists:
            os.remove(path)
        self.assertEqual(is_exists, True)
        self.assertEqual(mode, 33216)  # oct(33216) == '0o100700'

    def test_decode_bytes(self):
        """Check byte and str changing."""
        test_str = 'abcdABCD01234$&=+-*%[]#!/"@'
        byte_data = str.encode(test_str)
        decod_data = self.rancid_clogin.decode_bytes(byte_data)
        self.assertEqual(decod_data, test_str)

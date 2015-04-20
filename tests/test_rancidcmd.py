# -*- coding: utf-8 -*-

"""UnitTests for rancidcmd."""


import unittest
import os
import uuid
import stat
from rancidcmd import RancidCmd


class UnitTests(unittest.TestCase):

    """The :class:`UnitTests <UnitTests>`.

    UnitTests

    """

    def setUp(self):
        """setup."""
        self.obj1 = RancidCmd(
            login='clogin', user='rancid',
            password='password', enable_password='enable_password',
            address='192.168.1.1')

        self.obj2 = RancidCmd(
            login='clogin', user='rancid', timeout=10,
            password='password', enable_password='enable_password',
            address='192.168.1.2')

        self.obj3 = RancidCmd(
            login='jlogin', timeout=20,
            user='rancid', password='password',
            address='192.168.1.3')

    def test_init(self):
        """check init value."""
        self.assertEqual(self.obj1.login, 'clogin')
        self.assertEqual(self.obj1.user, 'rancid')
        self.assertEqual(self.obj1.password, 'password')
        self.assertEqual(self.obj1.enable_password, 'enable_password')
        self.assertEqual(self.obj1.address, '192.168.1.1')
        self.assertEqual(self.obj1.timeout, 10)
        self.assertEqual(self.obj1.encoding, 'utf-8')

        self.assertEqual(self.obj2.login, 'clogin')
        self.assertEqual(self.obj2.user, 'rancid')
        self.assertEqual(self.obj2.password, 'password')
        self.assertEqual(self.obj2.enable_password, 'enable_password')
        self.assertEqual(self.obj2.address, '192.168.1.2')
        self.assertEqual(self.obj2.timeout, 10)
        self.assertEqual(self.obj2.encoding, 'utf-8')

        self.assertEqual(self.obj3.login, 'jlogin')
        self.assertEqual(self.obj3.user, 'rancid')
        self.assertEqual(self.obj3.password, 'password')
        self.assertEqual(self.obj3.enable_password, None)
        self.assertEqual(self.obj3.address, '192.168.1.3')
        self.assertEqual(self.obj3.timeout, 20)
        self.assertEqual(self.obj3.encoding, 'utf-8')

    def _test_generate_cmd(self):
        """Check command format."""
        cmd = 'show version'

        # clogin
        rancid_cmd = self.obj1.generate_cmd(cmd)
        self.assertEqual(
            rancid_cmd,
            " ".join(['clogin',
                      '-t',
                      '10',
                      '-u',
                      'rancid',
                      '-p',
                      'password',
                      '-e',
                      'enable_password',
                      '-c',
                      'show version',
                      '192.168.1.1']))

        # clogin
        rancid_cmd = self.obj1.generate_cmd(cmd)
        self.assertEqual(
            rancid_cmd,
            " ".join(['clogin',
                      '-t',
                      '10',
                      '-u',
                      'rancid',
                      '-p',
                      'password',
                      '-e',
                      'enable_password',
                      '-c',
                      'show version',
                      '192.168.1.2']))

        # jlogin
        rancid_cmd = self.obj3.generate_cmd(cmd)
        self.assertEqual(
            rancid_cmd,
            " ".join(['clogin',
                      '-t',
                      '30',
                      '-u',
                      'rancid',
                      '-p',
                      'password',
                      '-c',
                      'show version',
                      '192.168.1.3']))

    def test_cmd_exec(self):
        """Check excecuter result."""
        res = self.obj1.cmd_exec('echo test')
        self.assertEqual(res, {'std_out': 'test\n', 'std_err': ''})

    def test_execute(self):
        """Check excecute."""
        obj = RancidCmd(login='clogin',
                        user='admin',
                        password='password',
                        address='127.0.0.1')
        res = obj.execute('show version')
        if res['std_err'] == '':
            self.assertEqual(res['std_err'], '')
            self.assertNotEqual(res['std_out'], '')
        self.assertNotEqual(res['std_err'], '')
        self.assertEqual(res['std_out'], '')

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
        decod_data = self.obj1.decode_bytes(byte_data)
        self.assertEqual(decod_data, test_str)

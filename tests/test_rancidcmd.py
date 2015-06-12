# -*- coding: utf-8 -*-

"""UnitTests for rancidcmd."""


import unittest
import os
import pwd
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
            login='clogin', user='rancid',
            password='password', enable_password='enable_password',
            address='192.168.1.2')

        self.obj3 = RancidCmd(
            login='jlogin',
            user='rancid', password='password',
            address='192.168.1.3')

        self.obj4 = RancidCmd(
            login='clogin',
            user='rancid', password='password',
            option='-d',
            address='192.168.1.4')

        self.obj5 = RancidCmd(
            login='clogin',
            user='rancid', password='password',
            option='-t 30 -d -x "commands.txt"',
            address='192.168.1.5')

        self.obj10 = RancidCmd(
            login='clogin',
            user='admin',
            password='zebra', enable_password='zebra',
            address='127.0.0.1')

    def test_init(self):
        """check init value."""
        self.assertEqual(self.obj1.login, 'clogin')
        self.assertEqual(self.obj1.user, 'rancid')
        self.assertEqual(self.obj1.password, 'password')
        self.assertEqual(self.obj1.enable_password, 'enable_password')
        self.assertEqual(self.obj1.address, '192.168.1.1')
        self.assertEqual(self.obj1.option, None)
        self.assertEqual(self.obj1.encoding, 'utf-8')

        self.assertEqual(self.obj2.login, 'clogin')
        self.assertEqual(self.obj2.user, 'rancid')
        self.assertEqual(self.obj2.password, 'password')
        self.assertEqual(self.obj2.enable_password, 'enable_password')
        self.assertEqual(self.obj2.address, '192.168.1.2')
        self.assertEqual(self.obj2.option, None)
        self.assertEqual(self.obj2.encoding, 'utf-8')

        self.assertEqual(self.obj3.login, 'jlogin')
        self.assertEqual(self.obj3.user, 'rancid')
        self.assertEqual(self.obj3.password, 'password')
        self.assertEqual(self.obj3.enable_password, None)
        self.assertEqual(self.obj3.address, '192.168.1.3')
        self.assertEqual(self.obj3.option, None)
        self.assertEqual(self.obj3.encoding, 'utf-8')

        self.assertEqual(self.obj4.login, 'clogin')
        self.assertEqual(self.obj4.user, 'rancid')
        self.assertEqual(self.obj4.password, 'password')
        self.assertEqual(self.obj4.enable_password, None)
        self.assertEqual(self.obj4.address, '192.168.1.4')
        self.assertEqual(self.obj4.option, '-d')
        self.assertEqual(self.obj4.encoding, 'utf-8')

        self.assertEqual(self.obj5.login, 'clogin')
        self.assertEqual(self.obj5.user, 'rancid')
        self.assertEqual(self.obj5.password, 'password')
        self.assertEqual(self.obj5.enable_password, None)
        self.assertEqual(self.obj5.address, '192.168.1.5')
        self.assertEqual(self.obj5.option, '-t 30 -d -x "commands.txt"')
        self.assertEqual(self.obj5.encoding, 'utf-8')

        self.assertEqual(self.obj10.login, 'clogin')
        self.assertEqual(self.obj10.user, 'admin')
        self.assertEqual(self.obj10.password, 'zebra')
        self.assertEqual(self.obj10.enable_password, 'zebra')
        self.assertEqual(self.obj10.address, '127.0.0.1')
        self.assertEqual(self.obj10.option, None)
        self.assertEqual(self.obj10.encoding, 'utf-8')

    def test_is_option_x(self):
        """Check command command option for "-x"."""
        self.assertEqual(self.obj1.is_option_x(), False)
        self.assertEqual(self.obj2.is_option_x(), False)
        self.assertEqual(self.obj3.is_option_x(), False)
        self.assertEqual(self.obj4.is_option_x(), False)
        self.assertEqual(self.obj5.is_option_x(), True)
        self.assertEqual(self.obj10.is_option_x(), False)

    def _test_generate_cmd(self):
        """Check command format."""
        cmd = 'show version'

        # clogin
        rancid_cmd = self.obj1.generate_cmd(cmd)
        self.assertEqual(
            rancid_cmd,
            " ".join(['clogin',
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
                      '-u',
                      'rancid',
                      '-p',
                      'password',
                      '-c',
                      'show version',
                      '192.168.1.3']))

        # clogin
        rancid_cmd = self.obj4.generate_cmd(cmd)
        self.assertEqual(
            rancid_cmd,
            " ".join(['clogin',
                      '-u',
                      'rancid',
                      '-p',
                      'password',
                      '-c',
                      'show version',
                      '-d',
                      '192.168.1.4']))

        # clogin
        rancid_cmd = self.obj5.generate_cmd(cmd)
        self.assertEqual(
            rancid_cmd,
            " ".join(['clogin',
                      '-u',
                      'rancid',
                      '-p',
                      'password',
                      '-x "commands.txt"',
                      '192.168.1.5']))

        # clogin
        rancid_cmd = self.obj10.generate_cmd(cmd)
        self.assertEqual(
            rancid_cmd,
            " ".join(['clogin',
                      '-u',
                      'admin',
                      '-p',
                      'zebra',
                      '-e',
                      'zebra',
                      '127.0.0.1']))

    def test_show(self):
        """Check command string."""
        import sys
        cmd = 'show version'
        try:
            from StringIO import StringIO
            out = StringIO()
            sys.stdout = out
            self.obj1.show(cmd)
            output = out.getvalue().strip()
        except ImportError:
            import io
            out = io.StringIO()
            sys.stdout = out
            self.obj1.show(cmd)
            output = out.getvalue().strip()

        self.assertEqual(
            output,
            " ".join(['clogin',
                      '-u',
                      '"rancid"',
                      '-p',
                      '"password"',
                      '-e',
                      '"enable_password"',
                      '',
                      '-c',
                      '"show version"',
                      '192.168.1.1']))

    def test_get_home_path(self):
        """Check user directory path."""
        path = RancidCmd.get_home_path()
        _path = pwd.getpwuid(os.getuid())[5]
        self.assertEqual(path, _path)

    def test_cmd_exec(self):
        """Check excecuter result."""
        # Execute true command.
        res = self.obj1.cmd_exec('echo test')
        self.assertEqual(res['rtn_code'], 0)

        # Execute not found command.
        res = self.obj1.cmd_exec('_echo test')
        self.assertNotEqual(res['rtn_code'], 0)

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

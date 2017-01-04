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
            login='clogin',
            user='rancid',
            password='password',
            enable_password='enable_password',
            address='192.168.1.1')

        self.obj2 = RancidCmd(
            login='clogin',
            user='rancid',
            password='password',
            enable_password='enable_password',
            address='192.168.1.2',
            port=23,
            method=u'telnet')

        self.obj3 = RancidCmd(
            login='jlogin',
            user='rancid',
            password='password',
            address='192.168.1.3',
            port=23,
            method=u'telnet')

        self.obj4 = RancidCmd(
            login='clogin',
            user='rancid',
            password='password',
            option='-d',
            address='192.168.1.4',
            port=22,
            method=u'ssh')

        self.obj5 = RancidCmd(
            login='clogin',
            user='rancid',
            password='password',
            option='-t 30 -d -x "commands.txt"',
            address='192.168.1.5',
            port=22,
            method=u'ssh')

        self.obj10 = RancidCmd(
            login='clogin',
            user='admin',
            password='zebra',
            enable_password='zebra',
            address='127.0.0.1',
            port=2601,
            method=u'telnet')

    def test_init(self):
        """check init value."""
        self.assertEqual(self.obj1.login, 'clogin')
        self.assertEqual(self.obj1.user, 'rancid')
        self.assertEqual(self.obj1.password, 'password')
        self.assertEqual(self.obj1.enable_password, 'enable_password')
        self.assertEqual(self.obj1.address, '192.168.1.1')
        self.assertEqual(self.obj1.port, 23)
        self.assertEqual(self.obj1.method, 'telnet')
        self.assertEqual(self.obj1.option, None)
        self.assertEqual(self.obj1.encoding, 'utf-8')

        self.assertEqual(self.obj2.login, 'clogin')
        self.assertEqual(self.obj2.user, 'rancid')
        self.assertEqual(self.obj2.password, 'password')
        self.assertEqual(self.obj2.enable_password, 'enable_password')
        self.assertEqual(self.obj2.address, '192.168.1.2')
        self.assertEqual(self.obj2.port, 23)
        self.assertEqual(self.obj2.method, 'telnet')
        self.assertEqual(self.obj2.option, None)
        self.assertEqual(self.obj2.encoding, 'utf-8')

        self.assertEqual(self.obj3.login, 'jlogin')
        self.assertEqual(self.obj3.user, 'rancid')
        self.assertEqual(self.obj3.password, 'password')
        self.assertEqual(self.obj3.enable_password, None)
        self.assertEqual(self.obj3.address, '192.168.1.3')
        self.assertEqual(self.obj3.port, 23)
        self.assertEqual(self.obj3.method, 'telnet')
        self.assertEqual(self.obj3.option, None)
        self.assertEqual(self.obj3.encoding, 'utf-8')

        self.assertEqual(self.obj4.login, 'clogin')
        self.assertEqual(self.obj4.user, 'rancid')
        self.assertEqual(self.obj4.password, 'password')
        self.assertEqual(self.obj4.enable_password, None)
        self.assertEqual(self.obj4.address, '192.168.1.4')
        self.assertEqual(self.obj4.port, 22)
        self.assertEqual(self.obj4.method, 'ssh')
        self.assertEqual(self.obj4.option, '-d')
        self.assertEqual(self.obj4.encoding, 'utf-8')

        self.assertEqual(self.obj5.login, 'clogin')
        self.assertEqual(self.obj5.user, 'rancid')
        self.assertEqual(self.obj5.password, 'password')
        self.assertEqual(self.obj5.enable_password, None)
        self.assertEqual(self.obj5.address, '192.168.1.5')
        self.assertEqual(self.obj5.port, 22)
        self.assertEqual(self.obj5.method, 'ssh')
        self.assertEqual(self.obj5.option, '-t 30 -d -x "commands.txt"')
        self.assertEqual(self.obj5.encoding, 'utf-8')

        self.assertEqual(self.obj10.login, 'clogin')
        self.assertEqual(self.obj10.user, 'admin')
        self.assertEqual(self.obj10.password, 'zebra')
        self.assertEqual(self.obj10.enable_password, 'zebra')
        self.assertEqual(self.obj10.address, '127.0.0.1')
        self.assertEqual(self.obj10.port, 2601)
        self.assertEqual(self.obj10.method, 'telnet')
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

    def test_generate_cmd(self):
        """Check command format."""
        cmd = 'show version'

        # clogin
        cmd1 = self.obj1.generate_cmd(cmd)
        temp = self.obj1.cloginrc
        cmd2 = " ".join(['clogin',
                         '-c',
                         '"show version"',
                         '-f',
                         temp.name,
                         '192.168.1.1'])

        self.assertEqual(cmd1, cmd2)

        # clogin
        cmd1 = self.obj2.generate_cmd(cmd)
        temp = self.obj2.cloginrc
        cmd2 = " ".join(['clogin',
                         '-c',
                         '"show version"',
                         '-f',
                         temp.name,
                         '192.168.1.2'])

        self.assertEqual(cmd1, cmd2)

        # jlogin
        cmd1 = self.obj3.generate_cmd(cmd)
        temp = self.obj3.cloginrc
        cmd2 = " ".join(['jlogin',
                         '-c',
                         '"show version"',
                         '-f',
                         temp.name,
                         '192.168.1.3'])

        self.assertEqual(cmd1, cmd2)

        # clogin
        cmd1 = self.obj4.generate_cmd(cmd)
        temp = self.obj4.cloginrc
        cmd2 = " ".join(['clogin',
                         '-d',
                         '-c',
                         '"show version"',
                         '-f',
                         temp.name,
                         '192.168.1.4'])

        self.assertEqual(cmd1, cmd2)

        # clogin
        cmd1 = self.obj5.generate_cmd(cmd)
        temp = self.obj5.cloginrc
        cmd2 = " ".join(['clogin',
                         '-t 30',
                         '-d',
                         '-x "commands.txt"',
                         '-f',
                         temp.name,
                         '192.168.1.5'])

        self.assertEqual(cmd1, cmd2)

        # clogin
        cmd1 = self.obj10.generate_cmd(cmd)
        temp = self.obj10.cloginrc
        cmd2 = " ".join(['clogin',
                         '-c',
                         '"show version"',
                         '-f',
                         temp.name,
                         '127.0.0.1'])

        self.assertEqual(cmd1, cmd2)

    def test_show(self):
        """Check command string."""
        import sys
        cmd = 'show version'
        try:
            from StringIO import StringIO
            out = StringIO()
        except ImportError:
            import io
            out = io.StringIO()

        sys.stdout = out
        self.obj1.show(cmd)
        temp = self.obj1.cloginrc
        output = out.getvalue().strip()

        vals = [u'#',
                u'# config',
                u'#',
                u'add user 192.168.1.1 rancid',
                u'add method 192.168.1.1 {telnet:23}',
                u'add password 192.168.1.1 password enable_password',
                u'#',
                u'# command',
                u'#',
                u'clogin -c "show version" -f {0} 192.168.1.1'.format(
                    temp.name)]

        self.assertEqual(output, "\n".join(vals))

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

    # def test_check_cloginrc(self):
    #     """Check cloginrc setting file."""
    #     name = '_test_cloginrc'
    #     path = RancidCmd.check_cloginrc(name=name)
    #     is_exists = os.path.isfile(path)
    #     mode = os.stat(path).st_mode
    #     if is_exists:
    #         os.remove(path)
    #     self.assertEqual(is_exists, True)
    #     self.assertEqual(mode, 33216)  # oct(33216) == '0o100700'

    def test_decode_bytes(self):
        """Check byte and str changing."""
        test_str = 'abcdABCD01234$&=+-*%[]#!/"@'
        byte_data = str.encode(test_str)
        decod_data = self.obj1.decode_bytes(byte_data)
        self.assertEqual(decod_data, test_str)

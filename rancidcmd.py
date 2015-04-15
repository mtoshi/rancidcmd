# -*- coding: utf-8 -*-

"""RancidCmd."""

from subprocess import Popen
from subprocess import PIPE
import shlex
import os
import stat


class RancidCmd(object):

    """The :class:`RancidCmd <RancidCmd>` object.

    RancidCmd

    """

    def __init__(self, **kwargs):
        """Constructor Parameters.

        login, user, password, address, [enable_password], [timeout].
        """
        self.login = kwargs['login']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.address = kwargs['address']
        self.enable_password = kwargs.get('enable_password', None)
        self.timeout = kwargs.get('timeout', 10)
        self.encoding = 'utf-8'
        RancidCmd.check_cloginrc()

    def generate_cmd(self, command):
        """Make login command."""
        if self.enable_password:
            return '%s -t %s -u "%s" -p "%s" -e "%s" -c "%s" %s' % (
                self.login, self.timeout, self.user,
                self.password, self.enable_password, command, self.address)
        return '%s -t %s -u "%s" -p "%s" -c "%s" %s' % (
            self.login, self.timeout, self.user,
            self.password, command, self.address)

    def cmd_token(self, command):
        """Split one line command."""
        return shlex.split(command)

    def decode_bytes(self, byte_data):
        """Change string with encoding setting."""
        return byte_data.decode(self.encoding)

    def cmd_exec(self, command):
        """Login and command execution."""
        proc = Popen(command,
                     shell=True,
                     stdout=PIPE,
                     stderr=PIPE)
        std_out, std_err = proc.communicate()
        return {'std_out': self.decode_bytes(std_out),
                'std_err': self.decode_bytes(std_err)}

    def execute(self, command):
        """Command execution."""
        cmd = self.generate_cmd(command)
        return self.cmd_exec(cmd)

    @staticmethod
    def touch(path):
        """Make empty file."""
        try:
            with open(path, 'a'):
                os.utime(path, None)
                os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        except:
            print('[error] Could not write "%s".' % path)
            raise

    @staticmethod
    def check_cloginrc(name='.cloginrc'):
        """Check rancid settings file (default: .cloginrc)."""
        home = os.environ['HOME']
        path = '%s/%s' % (home, name)
        if not os.path.isfile(path):
            RancidCmd.touch(path)
        return path

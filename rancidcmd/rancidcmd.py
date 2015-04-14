# -*- coding: utf-8 -*-

"""RancidCmd."""

from subprocess import Popen
from subprocess import PIPE
import shlex
import re
import os
import stat


class RancidCmd(object):

    """The :class:`RancidCmd <RancidCmd>` object.

    RancidCmd

    """

    def __init__(self, **kwargs):
        """Parameters: method, user, passwrod, address, [timeout]."""
        self.method = kwargs['method']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.address = kwargs['address']
        self.timeout = kwargs.get('timeout', 10)
        self.encoding = 'utf-8'
        RancidCmd.check_cloginrc()

    def clogin_cmd(self, command):
        """For cloign format."""
        return '%s -t %s -u "%s" -p "%s" -e "%s" -c "%s" %s' % (
            self.method, self.timeout, self.user,
            self.password, self.password, command, self.address)

    def jlogin_cmd(self, command):
        """For jloign format."""
        return '%s -t %s -u "%s" -p "%s" -c "%s" %s' % (
            self.method, self.timeout, self.user,
            self.password, command, self.address)

    def cmd_token(self, command):
        """Split one line command."""
        return shlex.split(command)

    def generate_rancid_cmd(self, command):
        """Assign login command with initialized method."""
        if re.search("jlogin$", self.method):

            return self.jlogin_cmd(command)

        elif re.search("clogin$", self.method):

            return self.clogin_cmd(command)

        print('"[error] Not support "%s"' % self.method)
        return False

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
        rancid_cmd = self.generate_rancid_cmd(command)
        if rancid_cmd:
            return self.cmd_exec(rancid_cmd)
        print('[error] Could not execute')

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

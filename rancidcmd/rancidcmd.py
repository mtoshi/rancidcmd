# -*- coding: utf-8 -*-
"""
rancidcmd
=========

"""

from subprocess import Popen
from subprocess import PIPE
import shlex
import re
import os
import stat


class RancidCmd(object):
    """ The :class:`RancidCmd <RancidCmd>` object.
    """

    def __init__(self, **kwargs):
        """ init """
        self.method = kwargs['method']
        self.timeout = kwargs['timeout']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.address = kwargs['address']
        self.encoding = 'utf-8'
        RancidCmd.check_cloginrc()

    def clogin_cmd(self, command):
        """ clogin command """

        return '%s -t %s -u "%s" -p "%s" -e "%s" -c "%s" %s' % (
            self.method, self.timeout, self.user,
            self.password, self.password, command, self.address)

    def jlogin_cmd(self, command):
        """ jlogin command """

        return '%s -t %s -u "%s" -p "%s" -c "%s" %s' % (
            self.method, self.timeout, self.user,
            self.password, command, self.address)

    def cmd_token(self, command):
        """ command token """
        return shlex.split(command)

    def generate_rancid_cmd(self, command):
        """ generate rancid command """

        if re.search("jlogin$", self.method):

            return self.jlogin_cmd(command)

        elif re.search("clogin$", self.method):

            return self.clogin_cmd(command)

        print('"[error] Not support "%s"' % command)
        return False

    def decode_bytes(self, byte_data):
        """ decode bytes """
        return byte_data.decode(self.encoding)

    def cmd_exec(self, command):
        """ command execute """
        proc = Popen(command,
                     shell=True,
                     stdout=PIPE,
                     stderr=PIPE)
        std_out, std_err = proc.communicate()
        return {'std_out': self.decode_bytes(std_out),
                'std_err': self.decode_bytes(std_err)}

    def execute(self, command):
        """ execute """

        rancid_cmd = self.generate_rancid_cmd(command)

        if rancid_cmd:

            return self.cmd_exec(rancid_cmd)

        print('[error] Could not execute "%s"' % command)

    @staticmethod
    def touch(path):
        """ touch """
        with open(path, 'a'):
            os.utime(path, None)
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

    @staticmethod
    def check_cloginrc(name='.cloginrc'):
        """ check cloginrc """
        home = os.environ['HOME']
        path = '%s/%s' % (home, name)
        if not os.path.isfile(path):
            RancidCmd.touch(path)
        return path

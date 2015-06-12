# -*- coding: utf-8 -*-

"""RancidCmd."""

from subprocess import Popen
from subprocess import PIPE
from os.path import expanduser
import os
import re
import stat


class RancidCmd(object):

    """Class RancidCmd.

    Attributes:

        :login (str): RANCID login command(clogin, jlogin, etc).
        :user (str): Login username.
        :password (str): Login password.
        :address (str): Host name or ip address.
        :enable_password (str, optional): Enable password for clogin.
            Default is None.
        :option(int, optional): Option example: '-d -x "commands.txt"'.
            Default is None.
        :encoding(str, optional): Encoding type.
            Default is 'utf-8'.

    Using example:

        * Please see README.
            https://github.com/mtoshi/rancidcmd/blob/master/README.rst

        * Sample code.
            https://github.com/mtoshi/rancidcmd/blob/master/samples/sample.py

    """

    def __init__(self, **kwargs):
        """Constructor.

        Args:

            :login (str): RANCID login command(clogin, jlogin, etc).
            :user (str): Login username.
            :password (str): Login password.
            :address (str): Host name or ip address.
            :enable_password (str, optional): Enable password for clogin.
                Default is None.
            :option(int, optional): Option example: '-d -x "commands.txt"'.
                Default is None.
            :encoding(str, optional): Encoding type.
                Default is 'utf-8'.

        """
        self.login = kwargs['login']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.address = kwargs['address']
        self.enable_password = kwargs.get('enable_password', None)
        self.option = kwargs.get('option', None)
        self.encoding = 'utf-8'
        RancidCmd.check_cloginrc()

    def is_option_x(self):
        """Check -x option.

        "-c" gets commands from command-line.
        "-x" gets commnads from file.

        These are for command option and exclusive.
        If "-x" option is specified, then "-c" command is ignored.
        """
        if self.option:
            pat = re.compile(r'(\s+)?-x\s+')
            if pat.search(self.option):
                return True
        return False

    def generate_cmd(self, command):
        """Generate command.

        Args:

            :command (str): Example is "show version".

        Returns:

            :str: Return the command string.

            If there is the "enable_password". ::

                'xlogin -u admin -p password -e enable_password
                    -c "show version"'

            If you have not set the "enable_password". ::

                'xlogin -u admin -p password -c "show version"'

        """
        if self.is_option_x():
            command = ''
        else:
            command = '-c "%s"' % command

        option = ''
        if self.option:
            option = self.option

        enable_password = ''
        if self.enable_password:
            enable_password = '-e "%s"' % self.enable_password

        return '%s -u "%s" -p "%s" %s %s %s %s' % (
            self.login, self.user, self.password,
            enable_password, option, command, self.address)

    def decode_bytes(self, byte_data):
        """Change string with encoding setting.

        Args:

            :byte_data (bytes): Popen output.

        """
        return byte_data.decode(self.encoding)

    def cmd_exec(self, command):
        """Login and command execution.

        Args:

            :command (str): Command for execution.

        Returns:

            :dict: Example is below. ::

            {
                'std_err': '',
                'std_out': '',
                'rtn_code': '',
            }
        """
        env = os.environ.copy()
        env['HOME'] = RancidCmd.get_home_path()
        proc = Popen(command,
                     shell=True,
                     env=env,
                     stdout=PIPE,
                     stderr=PIPE)
        std_out, std_err = proc.communicate()
        rtn_code = proc.returncode
        return {'std_out': self.decode_bytes(std_out),
                'std_err': self.decode_bytes(std_err),
                'rtn_code': rtn_code}

    def show(self, command):
        """Execute command string check.

        Args:

            :command (str): Example is "show version".

        Returns:

            :str: Return the command string.
        """
        print(self.generate_cmd(command))

    def execute(self, command):
        """Command execution.

        Args:

            :command (str): Example is "show version".

        Returns:

            :dict: Example is below. ::

            {
                'std_err': '',
                'std_out': '',
                'rtn_code': '',
            }

        """
        cmd = self.generate_cmd(command)
        return self.cmd_exec(cmd)

    @staticmethod
    def touch(path):
        """Make empty file.

        Args:

           :path (str): File path.

        """
        try:
            with open(path, 'a'):
                os.utime(path, None)
                os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        except:
            print('[error] Could not write "%s".' % path)
            raise

    @staticmethod
    def get_home_path():
        """Get home directory path.

        Returns:

            :str: User home directory path.

        """
        return expanduser("~")

    @staticmethod
    def check_cloginrc(name='.cloginrc'):
        """Check rancid settings file.

        Note:

            If RANCID settings file is not exists,
            then make empty settings file.

        Args:

            :name (str, optional): RANCID settings file name.
                 Default is ".cloginrc".

        Returns:

            :str: RANCID settings file path.

        """
        home = RancidCmd.get_home_path()
        path = os.path.join(home, name)
        if not os.path.isfile(path):
            RancidCmd.touch(path)
        return path

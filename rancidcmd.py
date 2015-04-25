# -*- coding: utf-8 -*-

"""RancidCmd."""

from subprocess import Popen
from subprocess import PIPE
import os
import stat


class RancidCmd(object):

    """Class RancidCmd.

    Attributes:

        :login (str): RANCID login command(clogin, jlogin, etc).
        :user (str): Login username.
        :password (str): Login password.
        :address (str): Host name or address.
        :enable_password (str, optional): Enable password for clogin.
            Default is None.
        :timeout(int, optional): Timeout value(seconds).
            Default is 10 seconds.
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
            :address (str): Host name or address.
            :enable_password (str, optional): Enable password for clogin.
                Default is None.
            :timeout(int, optional): Timeout value(seconds).
                Default is 10 seconds.
            :encoding(str, optional): Encoding type.
                Default is 'utf-8'.

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
        """Generate command.

        Args:

            :command (str): Example is "show version".

        Returns:

            :str: Return the command string.

            If there is the "enable_password". ::

                'xlogin -t 10 -u admin -p password -e enable_password
                    -c "show version"'

            If you have not set the "enable_password". ::

                'xlogin -t 10 -u admin -p password -c "show version"'

        """
        if self.enable_password:
            return '%s -t %s -u "%s" -p "%s" -e "%s" -c "%s" %s' % (
                self.login, self.timeout, self.user,
                self.password, self.enable_password, command, self.address)
        return '%s -t %s -u "%s" -p "%s" -c "%s" %s' % (
            self.login, self.timeout, self.user,
            self.password, command, self.address)

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
            }
        """
        proc = Popen(command,
                     shell=True,
                     stdout=PIPE,
                     stderr=PIPE)
        std_out, std_err = proc.communicate()
        return {'std_out': self.decode_bytes(std_out),
                'std_err': self.decode_bytes(std_err)}

    def execute(self, command):
        """Command execution.

        Args:

            :command (str): Example is "show version".

        Returns:

            :dict: Example is below. ::

            {
                'std_err': '',
                'std_out': '',
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
        home = os.environ['HOME']
        path = os.path.join(home, name)
        if not os.path.isfile(path):
            RancidCmd.touch(path)
        return path

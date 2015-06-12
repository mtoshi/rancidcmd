===================================================
rancidcmd
===================================================

Rancidcmd is a utility tool for network operators.
This module is wrapper of RANCID login commands.(like cloing, jlogin ...)
So if you use this module, then you have to install RANCID in some way.
Why did I make this module? As everybody knows RANCID is popular as auto login solutions.
Of course I want to use RANCID. And I wanted to do using without password of ".cloginrc".
This Rancidcmd can use RANCID login command like a clogin with empty ".clgoinrc".

.. image:: https://secure.travis-ci.org/mtoshi/rancidcmd.svg?branch=master
   :target: http://travis-ci.org/mtoshi/rancidcmd
.. image:: https://coveralls.io/repos/mtoshi/rancidcmd/badge.svg?branch=coverall
   :target: https://coveralls.io/r/mtoshi/rancidcmd?branch=coverall
.. image:: https://pypip.in/version/rancidcmd/badge.svg
   :target: https://pypi.python.org/pypi/rancidcmd/
   :alt: Latest Version

Requirements
=============

- Python 2.7, 3.3, 3.4, PyPy


Installation
=============
#. Please install the RANCID in advance.

    For CentOS ::

        $ yum install rancid

    For Debian, Ubuntu ::

        $ apt-get install rancid

    For MacOS X(Port) ::

        $ port install rancid

#. After RANCID, please install Rancidcmd ::

         $ pip install rancidcmd
          
         or
          
         $ git clone https://github.com/mtoshi/rancidcmd
         $ cd rancidcmd
         $ sudo python setup.py install

* Care of "~/.cloginrc" existence is not necessary.
    If executed user doesn't have "~/.cloginrc", then Rancidcmd makes empty "~/.cloginrc".

Using example
==============
Example for cisco(clogin). ::

    >>> from rancidcmd import RancidCmd
    >>> rancidcmd = RancidCmd(login='/usr/libexec/rancid/clogin',
    ...                       user='username',
    ...                       password='xxxx',
    ...                       enable_password='xxxx',
    ...                       address='192.168.1.1')
    >>> rancidcmd.execute("show version")

Example for junos(jlogin). ::

    >>> from rancidcmd import RancidCmd
    >>> rancidcmd = RancidCmd(login='/usr/libexec/rancid/jlogin',
    ...                       user='username',
    ...                       password='xxxx',
    ...                       address='192.168.1.2')
    >>> rancidcmd.execute("show version")

Example for Option ("-d" is enable debug mode and "-t 45" is timeout 45 seconds.). ::

    >>> from rancidcmd import RancidCmd
    >>> rancidcmd = RancidCmd(login='/usr/libexec/rancid/jlogin',
    ...                       user='username',
    ...                       password='xxxx',
    ...                       option='-d -t 45',
    ...                       address='192.168.1.2')
    >>> rancidcmd.execute("show version")

Example for command confirmation (you can use "show" method). ::

    >>> rancidcmd.show("show version")
    /usr/libexec/rancid/clogin -u "username" -p "xxxx" -e "xxxx"  -c "show version" 192.168.1.1
    
    # This show method will be useful for debug by hands.

RancidCmd() init args. ::

    login (str): Login command is xlogin. (such as "clogin, jlogin")
    address (str): Host name or ip address.
    user (str): Login user name.
    password (str): Login user password.
    enable_password (str): Login user enable password.
                           Default is None.(**clogin is must.**)
    option (str): Option is not must.
                  Deafult is None.
                  If you set this value to pass directly to clogin.
    encoding (str): Encoding type.
                    Default is 'utf-8'.

Output format. ::

    {'rtn_code': int, 'std_err': str, 'std_out': str}

Output sucess sample. ::

    {'rtn_code': 0,
     'std_err': '',
     'std_out': '... Copyright (c) 2002-2013, Cisco Systems, Inc. All ...'}

Output error sample. (Not found "clogin") ::

    {'rtn_code': 1,
     'std_err': '/bin/sh: clogin: command not fond\n',
     'std_out': ''}

Please see sample code.

* https://github.com/mtoshi/rancidcmd/blob/master/samples/sample.py


If you want to use another settings(prompt, method, etc), please edit ".cloginrc" same with previus.

Recently almost network devices can use ssh login. If you use ssh to priority, then you should write below into ".cloginrc". ::

    # All targets first action is ssh.
    add method * ssh telnet
    
    or
    
    # For specific targets.
    add method 192.168.1.* ssh telnet

See also
=========
* http://www.shrubbery.net/rancid/

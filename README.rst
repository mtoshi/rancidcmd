===================================================
rancidcmd
===================================================

Rancidcmd is a utility tool for network operators.
This module is wrapper of RANCID login commands.(like cloing, jlogin ...)
So if you use this moudle, then you have to install RANCID in some way.
Why did I make this module? As everybody knows RANCID is popular as auto login solutions.
Of course I want to use RANCID and I thought want to use without password of ".cloginrc".
Rancidcmd can use RANCID login command like a clogin with empty ".clgoinrc".

.. image:: https://secure.travis-ci.org/mtoshi/rancidcmd.svg?branch=master
   :target: http://travis-ci.org/mtoshi/rancidcmd

Requirements
=============

- Python 2.7, 3.3, 3.4, PyPy


Installation
=============
#. Please install the Rancid in advance.

    For CentOS ::

        $ yum install rancid

    For Debian, Ubuntu ::

        $ apt-get install rancid

    For MacOS X(Port) ::

        $ port install rancid

#. After Rancid, please install Rancidcmd ::

         $ pip install rancidcmd
          
         or
          
         $ git clone https://github.com/mtoshi/rancidcmd
         $ cd rancidcmd
         $ sudo python setup.py install


Using example
==============
Example for cisco(clogin). ::

    >>> from rancidcmd import RancidCmd
    >>> rancidcmd = RancidCmd(login='/usr/libexec/rancid/clogin',
    ...                       user='username',
    ...                       password='xxxx',
    ...                       enable_password='xxxx',
    ...                       timeout=10,
    ...                       address='192.168.1.1')
    >>> rancidcmd.execute("show version")

Example for junos(jlogin). ::

    >>> from rancidcmd import RancidCmd
    >>> rancidcmd = RancidCmd(login='/usr/libexec/rancid/jlogin',
    ...                       user='username',
    ...                       password='xxxx',
    ...                       timeout=30,
    ...                       address='192.168.1.2')
    >>> rancidcmd.execute("show version")

* RancidCmd() needs "login, user, password, enable_password, timeout, address".
* "enable_password" is not must for jlogin.
* "enable_password" default value is None.
* "timeout" is not must.
* "timeout" default value is 10(sec).

Output format. ::

    {'std_err': '', 'std_out': ''}

Output sucess sample. ::

    {'std_err': '', 'std_out': '... Copyright (c) 2002-2013, Cisco Systems, Inc. All ...'}

Output error sample. (Not found "clogin") ::

    {'std_err': '/bin/sh: clogin: command not fond\n', 'std_out': ''}

Please see sample code.

* https://github.com/mtoshi/rancidcmd/blob/master/samples/sample.py


If you want to use another settings(prompt, method, etc), please edit ".cloginrc" same with previus.



See also
=========
* http://www.shrubbery.net/rancid/

===================================================
rancidcmd
===================================================

Rancidcmd is a utility tool for network operators.
This module is wrapper of RANCID login commands.(like cloing, jlogin ...)
So if you use this moudle, then you have to install RANCID in some way.
Why did I make this module? As everybody knows RANCID is popular as auto login solutions.
Of course I want to use RANCID and I thought want to use without password of ".cloginrc".
Rancidcmd can use RANCID login command like a clogin with empty ".clgoinrc".


Requirements
=============

- Python 2.7, 3.2, 3.4.


Installation
=============
Please install the Rancid in advance.

For CentOS::

   $ yum install rancid


For Debian, Ubuntu::

   $ apt-get install rancid

For MacOS X(Port)::

   $ port install rancid

After Rancid, please install Rancidcmd::

   $ pip install rancidcmd

   or

   $ git clone https://github.com/mtoshi/rancidcmd
   $ cd rancidcmd
   $ sudo python setup.py install


Using example
==============
::

   Sample codes.


See also
=========
* http://www.shrubbery.net/rancid/
* http://github.com/mtoshi/rancidcmd/
